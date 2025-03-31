import os
import time
import json

def calcular_vendas_categorias(pasta='vendas'):
    inicio = time.time()
    
    if not os.path.exists(pasta):
        print(f"Erro: diretório não existente '{pasta}'")
        return

    categorias = {}  

    # Percorre a pasta vendas e subpastas
    for root, dirs, files in os.walk(pasta):
        for nome_arquivo in files:
            if nome_arquivo.endswith('.json'):
                caminho_completo = os.path.join(root, nome_arquivo)
                with open(caminho_completo, 'r', encoding='utf-8') as f:
                    try:
                        dados = json.load(f)
                        for venda in dados:
                            
                            categoria = venda['categoria']  
                            valor = venda['valor']         
                            
                            if categoria not in categorias:
                                categorias[categoria] = []
                            categorias[categoria].append(valor)
                    except Exception as e:
                        print(f"Erro ao ler {caminho_completo}: {str(e)}")

    # Cálculo do somatório
    somatorio = {categoria: sum(valores) for categoria, valores in categorias.items()}

    # Exibição
    print("\nSomatório por categoria:")
    print("-" * 35)
    print("{:<20} | {:>12}".format("Categoria", "Total (R$)"))
    print("-" * 35)
    for categoria, total in sorted(somatorio.items()):
        print(f"{categoria:<20} | R$ {total:>15,.2f}".replace(",","x".replace(".",",").replace("x",".")))
    print("-" * 35)
    
    tempo_total = time.time() - inicio
    print(f"Tempo total: {tempo_total:.2f} segundos")

if __name__ == '__main__':
    calcular_vendas_categorias()