import boto3
import requests
import time
from datetime import datetime
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_SESSION_TOKEN, DYNAMODB_TABLE

# Conexión a DynamoDB
dynamodb = boto3.resource(
    'dynamodb',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN
)
tabla = dynamodb.Table(DYNAMODB_TABLE)

def revisar_sitios():
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Iniciando revisión...")
    
    try:
        # 1. Obtenemos todos los sitios de la base de datos
        respuesta = tabla.scan()
        sitios = respuesta.get('Items', [])

        for sitio in sitios:
            url = sitio['url']
            usuario = sitio['usuario']
            print(f"Revisando {url}...", end=" ")

            try:
                # 2. Intentamos conectar con la web (tiempo de espera de 5 segundos)
                res = requests.get(url, timeout=5)
                # Si el código es 200-299, está Online
                nuevo_estado = "Online" if res.status_code == 200 else "Offline"
            except:
                nuevo_estado = "Offline"

            # 3. Actualizamos DynamoDB con el nuevo estado y la hora
            ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            tabla.update_item(
                Key={'usuario': usuario, 'url': url},
                UpdateExpression="set estado = :e, ultima_revision = :t",
                ExpressionAttributeValues={
                    ':e': nuevo_estado,
                    ':t': ahora
                }
            )
            print(f"[{nuevo_estado}]")

    except Exception as e:
        print(f"Error general: {e}")

if __name__ == "__main__":
    print("Monitor Local Iniciado. Presiona Ctrl+C para detener.")
    while True:
        revisar_sitios()
        print("Esperando 60 segundos para la próxima revisión...")
        time.sleep(60) # Revisa cada minuto
