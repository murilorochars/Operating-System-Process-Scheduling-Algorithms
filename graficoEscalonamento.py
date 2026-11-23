'''
Gera o grafico comparativo das medias de espera
de cada algoritmo de escalonamento.
'''

import matplotlib.pyplot as plt


def gerar_grafico(nomes_algoritmos, medias_espera):
    plt.figure(figsize=(7, 5))

    barras = plt.bar(nomes_algoritmos, medias_espera, color='#2a6fb0', width=0.5)

    # escreve o valor da media em cima de cada barra
    for barra in barras:
        altura = barra.get_height()
        posicao_x = barra.get_x() + barra.get_width() / 2
        plt.text(posicao_x, altura + 0.1, f'{altura:.2f}', ha='center')

    plt.title('Comparativo das medias de tempo de espera')
    plt.xlabel('Algoritmo de escalonamento')
    plt.ylabel('Tempo medio de espera')

    plt.savefig('grafico_medias_espera.png')
    plt.show()
