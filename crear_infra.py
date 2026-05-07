import boto3

def crear_tabla():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    
    try:
        tabla = dynamodb.create_table(
            TableName='MonitoreoSitios',
            KeySchema=[{'AttributeName': 'url', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'url', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        print("Creando tabla... espera un momento.")
        tabla.meta.client.get_waiter('table_exists').wait(TableName='MonitoreoSitios')
        print("¡Tabla creada con éxito!")
    except Exception as e:
        print(f"Error o la tabla ya existe: {e}")

if __name__ == "__main__":
    crear_tabla()