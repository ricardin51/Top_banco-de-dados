import json
import os
import time
from multiprocessing import Pool
import sys

def process_file(filename):
    caminho = os.path.join('vendas', filename)
    with open(caminho, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    categorias = {}
    for venda in dados:
        categoria = venda['categoria']
        valor = venda['valor']
        categorias[categoria] = categorias.get(categoria, 0.0) + valor
    return categorias

def main(num_processos):
    inicio = time.time()
    arquivos = [f for f in os.listdir('vendas') if f.endswith('.json')]
    
    with Pool(num_processos) as pool:
        resultados = pool.map(process_file, arquivos)
    
    soma_final = {}
    for resultado in resultados:
        for categoria, valor in resultado.items():
            soma_final[categoria] = soma_final.get(categoria, 0.0) + valor
    
   
    print("\nSomatório por categoria:")
    print("-" * 35)
    print("{:<20} | {:>18}".format("Categoria", "Total (R$)"))
    print("-" * 35)
    for categoria, total in sorted(soma_final.items()):
        valor_formatado = f"{total:>15,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        print(f"{categoria:<20} | R$ {valor_formatado}")
    print("-" * 35)
    
    print(f"\nTempo com {num_processos} processos: {time.time() - inicio:.2f} segundos")

if __name__ == '__main__':
    num_processos = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    main(num_processos)

