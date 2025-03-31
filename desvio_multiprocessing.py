import json
import os
import time
import math
from multiprocessing import Pool
import sys

def calcular_desvio_padrao(valores):
    n = len(valores)
    if n <= 1:
        return 0.0
    media = sum(valores) / n
    variancia = sum((x - media) ** 2 for x in valores) / n
    return math.sqrt(variancia)

def process_file(filename):
    caminho = os.path.join('vendas', filename)
    with open(caminho, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    categorias = {}
    for venda in dados:
        categoria = venda['categoria']
        valor = venda['valor']
        categorias.setdefault(categoria, []).append(valor)
    return categorias

def main(num_processos):
    inicio = time.time()
    arquivos = [f for f in os.listdir('vendas') if f.endswith('.json')]
    
    with Pool(num_processos) as pool:
        resultados = pool.map(process_file, arquivos)
    
    valores_por_categoria = {}
    for resultado in resultados:
        for categoria, valores in resultado.items():
            valores_por_categoria.setdefault(categoria, []).extend(valores)
    
    desvios = {categoria: calcular_desvio_padrao(valores) for categoria, valores in valores_por_categoria.items()}
    
    print("\nDesvio padrão por categoria:")
    print("-" * 35)
    print("{:<20} | {:>12}".format("Categoria", "Desvio Padrão (R$)"))
    print("-" * 35)
    for categoria in sorted(desvios):
        print("{:<20} | R$ {:>12.2f}".format(categoria, desvios[categoria]))
    print("-" * 35)
    
    print(f"\nTempo com {num_processos} processos: {time.time() - inicio:.2f} segundos")

if __name__ == '__main__':
    num_processos = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    main(num_processos)