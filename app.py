from flask import Flask, render_template

app = Flask(__name__)

# Esta es la ruta principal (el home)
@app.route('/')
def home():
    return render_template('inicio.html')

if __name__ == '__main__':
    # debug=True sirve para que el servidor se reinicie solo al guardar cambios
    app.run(debug=True)