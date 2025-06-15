from flask import Flask
import folium

app = Flask(__name__)

@app.route('/')
def index():
    # Criar mapa básico
    m = folium.Map(location=[-20.2976, -40.2958], zoom_start=8)
    
    # Salvar o mapa
    m.save('templates/map.html')
    
    # Retornar HTML simples
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mapa Simples</title>
    </head>
    <body>
        <iframe src="map.html" width="100%" height="800px" frameborder="0"></iframe>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True) 