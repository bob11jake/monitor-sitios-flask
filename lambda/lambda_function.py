import urllib3
import boto3
from datetime import datetime
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_SESSION_TOKEN, DYNAMODB_TABLE


def lambda_handler(event, context):
    http = urllib3.PoolManager()
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_session_token=AWS_SESSION_TOKEN
    )
    tabla = dynamodb.Table('MonitoreoSitios')

    # Lista de sitios a monitorear (puedes traerlos de la tabla después)
    sitios = ["https://www.google.com", "https://github.com"]
    
    for url in sitios:
        try:
            res = http.request('GET', url, timeout=5.0)
            estado = "Online" if res.status == 200 else "Offline"
        except:
            estado = "Offline"
            
        # Guardar en DynamoDB
        tabla.put_item(Item={
            'url': url,
            'estado': estado,
            'ultima_revision': str(datetime.now())
        })
    
    return {"message": "Revisión completada"}