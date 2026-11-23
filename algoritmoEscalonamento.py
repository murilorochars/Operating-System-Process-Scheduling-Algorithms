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


# Thread algoritmo FCFS (FIRST-COME, FIRST-SERVED)
class ThreadFCFS(threading.Thread):

    def __init__(self, lista_processos):
        threading.Thread.__init__(self)
        self.lista_processos = list(lista_processos)
        self.media_espera = 0.0

    def escalonar(self):
        # atende na ordem em que os processos chegaram
        fila_aptos = sorted(self.lista_processos, key=pegar_tempo_chegada)

        tempo_relogio = 0
        soma_tempos_espera = 0

        for processo in fila_aptos:
            # se a cpu ficou livre antes do processo chegar, o relogio avanca
            if tempo_relogio < processo.tempo_chegada:
                tempo_relogio = processo.tempo_chegada

            tempo_espera = tempo_relogio - processo.tempo_chegada
            soma_tempos_espera += tempo_espera
            print(f'FCFS -> {processo.identificacao} esperou {tempo_espera}')

            tempo_relogio += processo.tempo_cpu

        return soma_tempos_espera / len(fila_aptos)

    def run(self):
        print('Algoritmo FCFS')
        self.media_espera = self.escalonar()
        print(f'Media de espera FCFS: {self.media_espera:.2f}\n')


# Funcao principal
def main():
    lista_processos = ler_processos_csv(CAMINHO_CSV)

    print('Processos lidos do arquivo:')
    for processo in lista_processos:
        print(f'{processo.identificacao} | chegada: {processo.tempo_chegada} '
              f'| cpu: {processo.tempo_cpu} | prioridade: {processo.prioridade}')
    print()

    thread_fcfs = ThreadFCFS(lista_processos)
    thread_fcfs.start()
    thread_fcfs.join()


# Ponto de entrada do programa
main()
