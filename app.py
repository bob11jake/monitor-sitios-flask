import boto3
from flask import Flask, render_template, request, redirect, url_for, session
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_SESSION_TOKEN
from werkzeug.security import generate_password_hash, check_password_hash   
app = Flask(__name__)

app.secret_key = 'tu_clave_secreta_aqui' # Esto permite usar sesiones

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

def get_usuarios_table():
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_session_token=AWS_SESSION_TOKEN
    )
    return dynamodb.Table('Usuarios')
    

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

#Ruta oara login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contraseña = request.form.get('password')

        # Buscar el usuario en DynamoDB
        tabla = get_usuarios_table()
        respuesta = tabla.get_item(Key={'correo': correo})

        if 'Item' in respuesta:
            user = respuesta['Item']
            if check_password_hash(user['contraseña'], contraseña):
                # Iniciar sesión
                session['correo'] = correo
                return redirect(url_for('usuario_home'))

    return render_template('login.html')

@app.route('/usuario_home')
def usuario_home():
    if 'correo' not in session:
        return redirect(url_for('login'))
    return render_template('usuario_home.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contraseña = request.form.get('password')

        # Hash de la contraseña
        contraseña_hash = generate_password_hash(contraseña)
        
        # Guardar en DynamoDB
        tabla = get_usuarios_table()
        tabla.put_item(Item={
            'correo': correo,
            'contraseña': contraseña_hash
        })
        
        return redirect(url_for('login'))
    
    return render_template('registro.html')

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

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)