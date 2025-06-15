import folium

# Criar um mapa simples
m = folium.Map(location=[-20.2976, -40.2958], zoom_start=8)

# Adicionar uma camada básica
folium.TileLayer('OpenStreetMap').add_to(m)

# Salvar o mapa
m.save('test_map.html')

print("Mapa criado com sucesso! Abra o arquivo test_map.html no seu navegador.") 