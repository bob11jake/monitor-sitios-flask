import boto3
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_SESSION_TOKEN, DYNAMODB_TABLE

dynamodb = boto3.resource(
    'dynamodb',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN
)

def reset_tabla():
    try:
        print("Borrando tabla antigua...")
        tabla = dynamodb.Table(DYNAMODB_TABLE)
        tabla.delete()
        tabla.meta.client.get_waiter('table_not_exists').wait(TableName=DYNAMODB_TABLE)
        print("Tabla borrada. Ahora ejecutaremos crear_infra.py para crear la nueva.")
    except Exception as e:
        print(f"La tabla no existía o hubo un error: {e}")

if __name__ == "__main__":
    reset_tabla()
