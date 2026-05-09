import boto3
from flask import Flask, render_template
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_SESSION_TOKEN, DYNAMODB_TABLE

app = Flask(__name__)

@app.route('/')
def home():
    # Conectamos con DynamoDB
    # Importante: us-east-1 es la región estándar de los labs de AWS
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_session_token=AWS_SESSION_TOKEN
)
    
    tabla = dynamodb.Table('MonitoreoSitios')
    
    # Traer todos los datos de la tabla (scan lee toda la tabla)
    try:
        respuesta = tabla.scan()
        sitios = respuesta.get('Items', [])
    except Exception as e:
        print(f"Error al leer DynamoDB: {e}")
        sitios = [] # Si falla, mandamos la lista vacía para que no se rompa la web
    
    # Pasamos la lista 'sitios' al HTML
    return render_template('home.html', sitios=sitios)

if __name__ == '__main__':
    # Agregamos el paréntesis que faltaba y activamos el modo debug
    app.run(debug=True)