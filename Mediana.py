import json
import os
import time

def calcular_mediana(valores):
    if not valores:
        return 0.0
    ordenados = sorted(valores)
    n = len(ordenados)
    meio = n // 2
    return ordenados[meio] if n % 2 == 1 else (ordenados[meio - 1] + ordenados[meio]) / 2

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

    # Calcular medianas
    medianas = {categoria: calcular_mediana(valores) for categoria, valores in categorias.items()}

    print("\nMediana por categoria:")
    print("-" * 35)
    print("{:<20} | {:>15}".format("Categoria", "Mediana (R$)"))
    print("-" * 35)
    for categoria, mediana in sorted(medianas.items()):
        print(f"{categoria:<20} | R$ {mediana:>15,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    print("-" * 35)

    print(f"\nTempo total: {time.time() - inicio:.2f} segundos")

if __name__ == '__main__':
    main()