import json
import os
import time
import math

def calcular_desvio_padrao(valores):
    n = len(valores)
    if n <= 1:
        return 0.0
    media = sum(valores) / n
    variancia = sum((x - media) ** 2 for x in valores) / n
    return math.sqrt(variancia)

def main():
    inicio = time.time()
    categorias = {}

    
    if not os.path.exists('vendas'):
        print("Erro: Pasta 'vendas' não encontrada!")
        return

    
    for nome_arquivo in os.listdir('vendas'):
        if nome_arquivo.endswith('.json'):
            caminho = os.path.join('vendas', nome_arquivo)  
            try:
                with open(caminho, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    for venda in dados:
                        
                        categoria = venda['categoria']  
                        valor = venda['valor']           
                        categorias.setdefault(categoria, []).append(valor)
            except Exception as e:
                print(f"Erro em {nome_arquivo}: {str(e)}")

    # Calcular desvio padrão
    desvios = {categoria: calcular_desvio_padrao(valores) for categoria, valores in categorias.items()}

    
    print("\nDesvio padrão por categoria:")
    print("-" * 35)
    print("{:<20} | {:>20}".format("Categoria", "Desvio Padrão (R$)"))
    print("-" * 35)
    for categoria, desvio in sorted(desvios.items()):
        valor_formatado = f"R$ {desvio:>18,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        print(f"{categoria:<20} | {valor_formatado}")
    print("-" * 35)

    tempo_total = time.time() - inicio
    print(f"\nTempo total: {tempo_total:.2f} segundos")

if __name__ == '__main__':
    main()