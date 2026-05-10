import boto3
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_SESSION_TOKEN, DYNAMODB_TABLE

def crear_tabla():
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_session_token=AWS_SESSION_TOKEN
    )
    
    try:
        tabla = dynamodb.create_table(
            TableName='Usuarios',
            KeySchema=[{'AttributeName': 'correo', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'correo', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        print("Creando tabla... espera un momento.")
        tabla.meta.client.get_waiter('table_exists').wait(TableName='Usuarios')
        print("¡Tabla creada con éxito!")
    except Exception as e:
        print(f"Error o la tabla ya existe: {e}")

if __name__ == "__main__":
    crear_tabla()