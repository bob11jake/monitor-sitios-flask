import urllib3
import boto3
from datetime import datetime
# Importamos las credenciales desde tu archivo config
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_SESSION_TOKEN

def lambda_handler(event, context):
    http = urllib3.PoolManager()
    
    # 1. Configuración de Recursos (DynamoDB y SNS)
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_session_token=AWS_SESSION_TOKEN
    )
    
    sns = boto3.client(
        'sns',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_session_token=AWS_SESSION_TOKEN
    )
    
    tabla = dynamodb.Table('MonitoreoSitios')
    
    # REEMPLAZA esto con tu ARN real del SNS
    TOPIC_ARN = 'arn:aws:sns:us-east-1:891377334914:AlertasMonitoreo' 


    try:
        escaneo = tabla.scan()
        sitios_en_db = escaneo.get('Items', [])
    except Exception as e:
        print(f"Error al leer la base de datos: {e}")
        return {"message": "Error al leer DynamoDB"}

    # Si la tabla está vacía, avisamos
    if not sitios_en_db:
        print("No hay URLs registradas en la tabla.")
        return {"message": "Sin sitios para monitorear"}
    
    # 3. Procesar cada sitio encontrado
    for item in sitios_en_db:
        url = item['url']
        
        try:
            # Hacemos la petición con un tiempo de espera de 5 segundos
            res = http.request('GET', url, timeout=5.0)
            # Si el código es 200 (OK), está Online. Cualquier otro es Offline.
            estado_actual = "Online" if res.status == 200 else "Offline"
        except:
            estado_actual = "Offline"
            
        # 4. Actualizar la base de datos con el nuevo estado y la hora
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tabla.put_item(Item={
            'url': url,
            'estado': estado_actual,
            'ultima_revision': ahora
        })

        # 5. Si el sitio se cayó, disparamos la alerta al correo
        if estado_actual == "Offline":
            sns.publish(
                TopicArn=TOPIC_ARN,
                Message=f"¡Alerta! El sitio {url} está caído.\nEstado: {estado_actual}\nFecha: {ahora}",
                Subject="⚠️ Alerta de Monitoreo - Sitio Caído"
            )
            print(f"Alerta enviada para: {url}")
    
    return {"message": f"Revisión de {len(sitios_en_db)} sitios completada."}

# Esto es para que puedas probarlo en Cursor/Terminal dándole a "Play"
if __name__ == "__main__":
    print("Ejecutando prueba local...")
    lambda_handler(None, None)