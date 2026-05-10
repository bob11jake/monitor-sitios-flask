import boto3
from flask import Flask, render_template, request, redirect, url_for
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_SESSION_TOKEN

app = Flask(__name__)

# Función para conectar a DynamoDB (así no repetimos código)
def get_dynamodb_table():
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_session_token=AWS_SESSION_TOKEN
    )
    return dynamodb.Table('MonitoreoSitios')

@app.route('/')
def home():
    tabla = get_dynamodb_table()
    try:
        respuesta = tabla.scan()
        sitios = respuesta.get('Items', [])
        # Ordenamos los sitios para que los más nuevos salgan arriba
        sitios.sort(key=lambda x: x.get('ultima_revision', ''), reverse=True)
    except Exception as e:
        print(f"Error al leer DynamoDB: {e}")
        sitios = []
    
    return render_template('home.html', sitios=sitios)

# NUEVA RUTA: Para agregar sitios desde el formulario
@app.route('/agregar', methods=['POST'])
def agregar_sitio():
    url = request.form.get('url_sitio')
    if url:
        # Aseguramos que la URL tenga http o https
        if not url.startswith('http'):
            url = 'https://' + url
            
        tabla = get_dynamodb_table()
        tabla.put_item(Item={
            'url': url,
            'estado': 'Pendiente',  # Aparecerá como pendiente hasta que la Lambda lo revise
            'ultima_revision': 'Esperando revisión...'
        })
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)