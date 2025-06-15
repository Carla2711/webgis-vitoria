from flask import Flask, render_template
import folium
from folium import plugins
import rasterio
from rasterio.plot import show
import numpy as np
import os
import logging

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('webgis_debug.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)

@app.route('/')
def index():
    try:
        logging.info("Iniciando criação do mapa")
        
        # Criar mapa base
        m = folium.Map(location=[-20.2976, -40.2958], zoom_start=13)
        logging.info("Mapa base criado")
        
        # Adicionar camada de satélite
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Satélite',
            overlay=False
        ).add_to(m)
        logging.info("Camada de satélite adicionada")
        
        # Adicionar camada de ruas
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Ruas',
            overlay=False
        ).add_to(m)
        logging.info("Camada de ruas adicionada")
        
        # Adicionar camada de uso do solo
        try:
            logging.info("Tentando abrir arquivo de uso do solo")
            uso_solo_path = os.path.join('dados', 'uso_solo_2025.tif')
            if not os.path.exists(uso_solo_path):
                logging.error(f"Arquivo não encontrado: {uso_solo_path}")
                raise FileNotFoundError(f"Arquivo não encontrado: {uso_solo_path}")
                
            with rasterio.open(uso_solo_path) as src:
                logging.info("Arquivo de uso do solo aberto com sucesso")
                bounds = src.bounds
                logging.info(f"Bounds do raster: {bounds}")
                
                # Criar overlay do raster
                folium.raster_layers.ImageOverlay(
                    image=src.read(1),
                    bounds=[[bounds.bottom, bounds.left], [bounds.top, bounds.right]],
                    opacity=0.7,
                    name='Uso do Solo'
                ).add_to(m)
                logging.info("Camada de uso do solo adicionada ao mapa")
        except Exception as e:
            logging.error(f"Erro ao adicionar camada de uso do solo: {str(e)}")
            raise
        
        # Adicionar controle de camadas
        folium.LayerControl().add_to(m)
        logging.info("Controle de camadas adicionado")
        
        # Salvar o mapa
        logging.info("Salvando mapa")
        m.save('templates/mapa.html')
        logging.info("Mapa salvo com sucesso")
        
        return render_template('index.html')
        
    except Exception as e:
        logging.error(f"Erro ao criar mapa: {str(e)}")
        return f"Erro ao criar mapa: {str(e)}", 500

if __name__ == '__main__':
    logging.info("Iniciando aplicação Flask")
    app.run(debug=True) 