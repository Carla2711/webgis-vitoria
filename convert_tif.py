import rasterio
from rasterio.plot import show
import numpy as np
from PIL import Image
import os

def convert_tif_to_png(input_tif, output_png):
    print(f"Iniciando conversão do arquivo: {input_tif}")
    print(f"Tamanho do arquivo: {os.path.getsize(input_tif) / (1024*1024):.2f} MB")
    try:
        with rasterio.open(input_tif) as src:
            print(f"Informações do arquivo:")
            print(f"- Dimensões: {src.width}x{src.height}")
            print(f"- Número de bandas: {src.count}")
            print(f"- Tipo de dados: {src.dtypes[0]}")
            if src.count == 1:
                data = src.read(1)
                print(f"Array shape: {data.shape}, dtype: {data.dtype}")
                if data.dtype != np.uint8:
                    print("Normalizando dados grayscale...")
                    data = ((data - data.min()) * (255.0 / (data.max() - data.min()))).astype(np.uint8)
                print(f"Array shape após normalização: {data.shape}, dtype: {data.dtype}")
                img = Image.fromarray(data, mode='L')
            elif src.count >= 3:
                data = src.read([1, 2, 3])
                print(f"Array shape: {data.shape}, dtype: {data.dtype}")
                if data.dtype != np.uint8:
                    print("Normalizando dados RGB...")
                    data = ((data - data.min()) * (255.0 / (data.max() - data.min()))).astype(np.uint8)
                print(f"Array shape após normalização: {data.shape}, dtype: {data.dtype}")
                data = np.transpose(data, (1, 2, 0))
                print(f"Array shape após transpose: {data.shape}, dtype: {data.dtype}")
                img = Image.fromarray(data, mode='RGB')
            else:
                raise Exception(f"Número de bandas não suportado: {src.count}")
            print("Salvando imagem PNG...")
            img.save(output_png, optimize=True)
            print(f"Arquivo convertido com sucesso: {output_png}")
            print(f"Tamanho do arquivo PNG: {os.path.getsize(output_png) / (1024*1024):.2f} MB")
    except Exception as e:
        print(f"Erro durante a conversão: {str(e)}")
        raise

if __name__ == "__main__":
    input_file = "uso do solo Vtoria.tif"
    output_file = "uso_solo_vitoria.png"
    convert_tif_to_png(input_file, output_file) 