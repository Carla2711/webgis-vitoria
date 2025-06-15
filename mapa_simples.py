import folium
import webbrowser
import os

# Criar o mapa
m = folium.Map(location=[-20.2976, -40.2958],  # Vitória, ES
               zoom_start=8,
               control_scale=True)

# Adicionar camadas de fundo
folium.TileLayer('OpenStreetMap', name='OpenStreetMap').add_to(m)
folium.TileLayer('Stamen Terrain', name='Stamen Terrain').add_to(m)
folium.TileLayer('CartoDB positron', name='CartoDB Positron').add_to(m)

# Adicionar controle de camadas
folium.LayerControl().add_to(m)

# Salvar o mapa
arquivo_html = 'mapa_vitoria.html'
m.save(arquivo_html)

# Abrir no navegador
caminho_absoluto = 'file://' + os.path.realpath(arquivo_html)
webbrowser.open(caminho_absoluto)

print(f"Mapa gerado e aberto no navegador!") 