# WebGIS Vitória

Este é um WebGIS simples que mostra o mapa de uso do solo de Vitória, ES, com as seguintes camadas:
- Google Satellite
- OpenStreetMap
- Mapa de Uso do Solo de Vitória

## Requisitos

- Python 3.7+
- Flask
- Folium
- Rasterio
- NumPy

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/Carla2711/webgis-vitoria.git
cd webgis-vitoria
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Coloque o arquivo do mapa de uso do solo na pasta do projeto:
- Nome do arquivo: `uso do solo Vtoria.tif`
- Localização: pasta raiz do projeto

## Uso

1. Execute o servidor:
```bash
python simple_webgis.py
```

2. Acesse o WebGIS:
- Local: http://localhost:8080
- Rede local: http://SEU_IP_LOCAL:8080

3. Para tornar o WebGIS público:
```bash
ssh -R 80:localhost:8080 serveo.net
```

## Estrutura do Projeto

- `simple_webgis.py`: Aplicação principal
- `requirements.txt`: Dependências do projeto
- `uso do solo Vtoria.tif`: Arquivo do mapa de uso do solo (não incluído no repositório)

## Legenda do Mapa de Uso do Solo

- 0 - Água (Azul)
- 3 - Área Urbana (Vermelho)
- 5 - Vegetação (Verde)
- 9 - Solo Exposto (Amarelo) 