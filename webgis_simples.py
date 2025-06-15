from flask import Flask, render_template_string
import folium
import rasterio
import numpy as np
import os
import socket
import sys

app = Flask(__name__)

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

@app.route('/')
def index():
    try:
        print("Iniciando criação do mapa...")
        # Criar mapa base
        m = folium.Map(
            location=[-20.2976, -40.2958],
            zoom_start=8
        )
        print("Mapa base criado com sucesso")

        # Adicionar camada de uso do solo
        raster_path = r"C:\Users\Carla\Desktop\Cursos\QGIS 2025\uso do solo Vtoria.tif"
        print(f"Verificando arquivo raster: {raster_path}")
        
        if not os.path.exists(raster_path):
            print(f"ERRO: Arquivo não encontrado em: {raster_path}")
            raise FileNotFoundError(f"Arquivo não encontrado: {raster_path}")
            
        print("Tentando abrir o arquivo raster...")
        try:
            src = rasterio.open(raster_path)
            print("Arquivo raster aberto com sucesso")
            print(f"Formato do raster: {src.meta}")
            
            try:
                data = src.read(1)
                print(f"Dados lidos com sucesso. Formato: {data.shape}")
                print(f"Valores únicos: {np.unique(data)}")
                
                bounds = src.bounds
                print(f"Limites do raster: {bounds}")
                
                # Normalizar dados para visualização
                data_norm = (data - np.min(data)) / (np.max(data) - np.min(data))
                print("Dados normalizados com sucesso")
                
                # Adicionar ao mapa
                folium.raster_layers.ImageOverlay(
                    image=data_norm,
                    bounds=[[bounds.bottom, bounds.left], [bounds.top, bounds.right]],
                    name='Uso do Solo',
                    opacity=0.7
                ).add_to(m)
                print("Camada raster adicionada ao mapa com sucesso")
                
            except Exception as e:
                print(f"Erro ao processar dados do raster: {str(e)}")
                raise
            finally:
                src.close()
                print("Arquivo raster fechado")
                
        except Exception as e:
            print(f"Erro ao abrir arquivo raster: {str(e)}")
            raise

        # Template HTML
        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>WebGIS - Vitória</title>
            <style>
                body {{ margin: 0; padding: 0; }}
                #map {{ width: 100%; height: 100vh; }}
            </style>
        </head>
        <body>
            <div id="map">
                {m._repr_html_()}
            </div>
        </body>
        </html>
        '''
        
        print("Template HTML gerado com sucesso")
        return render_template_string(html)
        
    except Exception as e:
        print(f"ERRO CRÍTICO: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return f"Erro ao carregar o mapa: {str(e)}"

if __name__ == '__main__':
    try:
        port = find_free_port()
        print(f"Iniciando servidor Flask na porta {port}...")
        print(f"Python version: {sys.version}")
        print(f"Rasterio version: {rasterio.__version__}")
        print(f"Numpy version: {np.__version__}")
        app.run(debug=True, port=port)
    except Exception as e:
        print(f"Erro ao iniciar o servidor: {str(e)}") 