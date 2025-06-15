import folium
import webbrowser
import os

# Criar o mapa
m = folium.Map(
    location=[-20.2976, -40.2958],  # Vitória, ES
    zoom_start=8,
    control_scale=True,
    prefer_canvas=True,  # Melhora a performance
    tiles=None  # Não carrega tiles por padrão
)

# Adicionar apenas duas camadas essenciais
folium.TileLayer(
    'OpenStreetMap',
    name='OpenStreetMap',
    attr='OpenStreetMap contributors'
).add_to(m)

# Google Satellite
folium.TileLayer(
    tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
    attr='Google',
    name='Google Satellite',
    overlay=False
).add_to(m)

# Adicionar controle de camadas
folium.LayerControl().add_to(m)

# Salvar o mapa
arquivo_html = 'mapa_vitoria.html'
m.save(arquivo_html)

# Abrir no navegador
caminho_absoluto = 'file://' + os.path.realpath(arquivo_html)
webbrowser.open(caminho_absoluto)

print(f"Mapa gerado e aberto no navegador!") 