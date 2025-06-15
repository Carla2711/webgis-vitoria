from flask import Flask, render_template_string
import folium
import rasterio
import numpy as np
import os
import socket
import sys
import traceback
import logging
import xml.etree.ElementTree as ET
from rasterio.warp import calculate_default_transform, reproject, Resampling
import gc  # Garbage Collector

# Configurar logging
logging.basicConfig(
    filename='webgis_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

app = Flask(__name__)

@app.route('/')
def index():
    try:
        logging.info("Acesso à rota principal /")
        logging.info("Iniciando criação do mapa")
        
        # Criar mapa base
        m = folium.Map(location=[-20.2976, -40.2958], zoom_start=13)
        logging.info("Mapa base criado com sucesso")
        
        # Adicionar camada Google Satellite
        folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
            attr='© Google',
            name='Google Satellite',
            overlay=False
        ).add_to(m)
        logging.info("Camada Google Satellite adicionada")
        
        # Adicionar camada OpenStreetMap
        folium.TileLayer(
            tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            attr='OpenStreetMap',
            name='OpenStreetMap',
            overlay=False
        ).add_to(m)
        logging.info("Camada OpenStreetMap adicionada")
        
        # Adicionar camada raster
        raster_path = os.path.join(os.path.dirname(__file__), 'uso do solo Vtoria.tif')
        logging.info(f"Verificando arquivo raster: {raster_path}")
        
        aux_path = raster_path + '.aux.xml'
        logging.info(f"Verificando arquivo auxiliar: {aux_path}")
        
        if os.path.exists(raster_path):
            logging.info("Tentando abrir o arquivo raster...")
            with rasterio.open(raster_path) as src:
                # Ler dados
                data = src.read(1)
                logging.info(f"Dados lidos com sucesso. Formato: {data.shape}")
                
                # Obter valores únicos
                unique_values = np.unique(data)
                logging.info(f"Valores únicos: {unique_values}")
                
                # Obter limites do raster
                bounds = src.bounds
                logging.info(f"Limites do raster: {bounds}")
                
                # Normalizar dados para visualização
                data_normalized = np.zeros_like(data, dtype=np.uint8)
                data_normalized[data == 0] = 0  # Água
                data_normalized[data == 3] = 85  # Área Urbana
                data_normalized[data == 5] = 170  # Vegetação
                data_normalized[data == 9] = 255  # Solo Exposto
                
                # Adicionar ao mapa
                folium.raster_layers.ImageOverlay(
                    image=data_normalized,
                    bounds=[[bounds.bottom, bounds.left], [bounds.top, bounds.right]],
                    opacity=0.7,
                    name='Uso do Solo',
                    colormap=lambda x: [
                        (0, 0, 255, 255),  # Água - Azul
                        (255, 0, 0, 255),  # Área Urbana - Vermelho
                        (0, 255, 0, 255),  # Vegetação - Verde
                        (255, 255, 0, 255)  # Solo Exposto - Amarelo
                    ][int(x * 3)]
                ).add_to(m)
                logging.info("Camada raster adicionada ao mapa com sucesso")
                
                # Adicionar legenda
                legend_html = '''
                    <div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; background-color: white; padding: 10px; border: 2px solid grey; border-radius: 5px;">
                        <h4>Uso do Solo</h4>
                        <p style="color: blue;">0 - Água</p>
                        <p style="color: red;">3 - Área Urbana</p>
                        <p style="color: green;">5 - Vegetação</p>
                        <p style="color: yellow;">9 - Solo Exposto</p>
                    </div>
                '''
                m.get_root().html.add_child(folium.Element(legend_html))
                logging.info("Legenda adicionada com sucesso")
        else:
            logging.warning(f"Arquivo raster não encontrado: {raster_path}")
        
        # Adicionar controle de camadas
        folium.LayerControl().add_to(m)
        logging.info("Controle de camadas adicionado")
        
        # Gerar HTML
        html = m.get_root().render()
        logging.info("Template HTML gerado com sucesso")
        
        logging.info("Fim do processamento da rota principal /")
        return html
        
    except Exception as e:
        logging.error(f"Erro ao processar requisição: {str(e)}")
        logging.error(traceback.format_exc())
        return f"Erro ao carregar o mapa: {str(e)}"

if __name__ == '__main__':
    try:
        logging.info("Iniciando aplicação Flask")
        port = 8080  # Porta fixa
        logging.info(f"Servidor iniciado na porta {port}")
        print("\n" + "="*50)
        print("SEU WEBGIS ESTÁ DISPONÍVEL EM:")
        print(f"Local: http://localhost:{port}")
        print(f"Rede local: http://SEU_IP_LOCAL:{port}")
        print("\nPara torná-lo público, use o comando:")
        print(f"ssh -R 80:localhost:{port} serveo.net")
        print("="*50 + "\n")
        
        # Configurar o servidor para aceitar conexões externas
        app.run(host='0.0.0.0', port=port, debug=True, threaded=True)
    except Exception as e:
        logging.error(f"Erro ao iniciar servidor: {str(e)}")
        logging.error(traceback.format_exc()) 