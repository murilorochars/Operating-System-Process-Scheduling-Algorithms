'''
Simulador de Algoritmos de Escalonamento de Processos usando threads.
Algoritmos: FCFS, SJF e Prioridades (todos nao preemptivos).
'''

import threading
import csv
from graficoEscalonamento import gerar_grafico

CAMINHO_CSV = 'datasetProcessos/dataset.csv'


# Classe que representa o processo
class Processo:

    def __init__(self, identificacao, tempo_chegada, tempo_cpu, prioridade):
        self.identificacao = identificacao
        self.tempo_chegada = tempo_chegada
        self.tempo_cpu = tempo_cpu
        self.prioridade = prioridade


# Le o arquivo .csv e cria a lista de processos
def ler_processos_csv(caminho_arquivo):
    lista_processos = []

    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            processo = Processo(linha['id'],
                                int(linha['chegada']),
                                int(linha['cpu']),
                                int(linha['prioridade']))
            lista_processos.append(processo)

    return lista_processos


# Funcao usada para ordenar os processos pelo tempo de chegada
def pegar_tempo_chegada(processo):
    return processo.tempo_chegada


# Funcao principal
def main():
    lista_processos = ler_processos_csv(CAMINHO_CSV)

    print('Processos lidos do arquivo:')
    for processo in lista_processos:
        print(f'{processo.identificacao} | chegada: {processo.tempo_chegada} '
              f'| cpu: {processo.tempo_cpu} | prioridade: {processo.prioridade}')


# Ponto de entrada do programa
main()
