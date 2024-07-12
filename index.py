from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import io
import base64
import nltk
from nltk.tokenize import word_tokenize

app = Flask(__name__, static_url_path='/static')

# Configuración de la base de datos
conectar = {
    'host': 'localhost',
    'user': 'root',
    'port': 3307,
    'password': 'mauro17',
    'database': 'pruebagif'
}

def establecer_conexion():
    try:
        conexion = mysql.connector.connect(**conectar)
        return conexion
    except mysql.connector.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None

def tokenizarpalabras(token):

    listas = word_tokenize(token)

    print(listas)



# Ruta de inicio
@app.route('/')

def index():
    return render_template('index2.html')

# Ruta para la página "Mas Información"
@app.route('/masinformacion')
def sobrenosotros():
    return render_template('masinformacion.html')

# Ruta para buscar un GIF
@app.route('/', methods=['POST'])



def buscar_gif():
    nombregif = request.form['gifName']
    conexion = establecer_conexion()
    palabrasseparadas = tokenizarpalabras(nombregif)
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT GIF FROM frases WHERE nombre_gif = %s", (nombregif,))
        gif_data = cursor.fetchone()
        cursor.close()
        conexion.close()
        if gif_data:
            gif_bytes = io.BytesIO(gif_data[0]) #almacena los datos del gif de la base de datps, pasados a Bytes
            gif_base64 = base64.b64encode(gif_bytes.read()).decode('utf-8') #decodificamos los datos de bytes para que sea leido por un url
            gif_url = f"data:image/gif;base64,{gif_base64}" #gener una url para que el gif se pueda mostrar por la pagina
            return render_template('index2.html', gif=gif_url)
        else:
            return render_template('index2.html', error_message='No se encontró ningún GIF con ese nombre.')
    else:
        return render_template('index2.html', error_message='Error al establecer la conexión con la base de datos.')

        
if __name__ == "__main__":
    app.run(debug=True)
