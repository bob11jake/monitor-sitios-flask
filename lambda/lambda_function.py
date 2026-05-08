import urllib3
import boto3
from datetime import datetime

def lambda_handler(event, context):
    http = urllib3.PoolManager()
    dynamodb = boto3.resource('dynamodb')
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