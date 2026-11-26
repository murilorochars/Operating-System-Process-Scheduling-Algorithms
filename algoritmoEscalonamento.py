
import threading
import csv
import time
from graficoEscalonamento import gerar_grafico

CAMINHO_CSV = 'datasetProcessos/dataset.csv'
SEGUNDOS_POR_UNIDADE_CPU = 0.1

class Processo:

    def __init__(self, identificacao, tempo_chegada, tempo_cpu, prioridade):
        self.identificacao = identificacao
        self.tempo_chegada = tempo_chegada
        self.tempo_cpu = tempo_cpu
        self.prioridade = prioridade


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


def pegar_tempo_chegada(processo):
    return processo.tempo_chegada

class ThreadFCFS(threading.Thread):

    def __init__(self, lista_processos):
        threading.Thread.__init__(self)
        self.lista_processos = list(lista_processos)
        self.media_espera = 0.0

    def escalonar(self):
        # atende na ordem em que os processos chegaram
        fila_aptos = sorted(self.lista_processos, key=pegar_tempo_chegada)
        print(fila_aptos)
        tempo_relogio = 0
        soma_tempos_espera = 0

        for processo in fila_aptos:
            print(processo)
            if tempo_relogio < processo.tempo_chegada:
                tempo_relogio = processo.tempo_chegada

            tempo_espera = tempo_relogio - processo.tempo_chegada
            soma_tempos_espera += tempo_espera
            print(f'FCFS -> {processo.identificacao} esperou {tempo_espera}')

            print(f'FCFS -> {processo.identificacao} executando...')
            time.sleep(processo.tempo_cpu * SEGUNDOS_POR_UNIDADE_CPU)

            tempo_relogio += processo.tempo_cpu

        return soma_tempos_espera / len(fila_aptos)

    def run(self):
        print('Algoritmo FCFS')
        self.media_espera = self.escalonar()
        print(f'Media de espera FCFS: {self.media_espera:.2f}\n')


# Thread algoritmo SJF (SHORTEST JOB FIRST)
class ThreadSJF(threading.Thread):

    def __init__(self, lista_processos):
        threading.Thread.__init__(self)
        self.lista_processos = list(lista_processos)
        self.media_espera = 0.0

    def escalonar(self):
        processos_pendentes = sorted(self.lista_processos, key=pegar_tempo_chegada)
        quantidade_processos = len(processos_pendentes)

        tempo_relogio = 0
        soma_tempos_espera = 0

        while len(processos_pendentes) > 0:
            # fila de aptos: processos que ja chegaram
            fila_aptos = []
            for processo in processos_pendentes:
                if processo.tempo_chegada <= tempo_relogio:
                    fila_aptos.append(processo)

            # nenhum processo chegou ainda, o relogio avanca
            if len(fila_aptos) == 0:
                tempo_relogio += 1
                continue

            # escolhe o processo com o menor tempo de cpu
            processo_escolhido = fila_aptos[0]
            for processo in fila_aptos:
                if processo.tempo_cpu < processo_escolhido.tempo_cpu:
                    processo_escolhido = processo

            tempo_espera = tempo_relogio - processo_escolhido.tempo_chegada
            soma_tempos_espera += tempo_espera
            print(f'SJF -> {processo_escolhido.identificacao} esperou {tempo_espera}')

            print(f'SJF -> {processo_escolhido.identificacao} executando...')
            time.sleep(processo_escolhido.tempo_cpu * SEGUNDOS_POR_UNIDADE_CPU)

            tempo_relogio += processo_escolhido.tempo_cpu
            processos_pendentes.remove(processo_escolhido)

        return soma_tempos_espera / quantidade_processos

    def run(self):
        print('Algoritmo SJF')
        self.media_espera = self.escalonar()
        print(f'Media de espera SJF: {self.media_espera:.2f}\n')


# Thread algoritmo de PRIORIDADES (menor numero = maior prioridade)
class ThreadPrioridades(threading.Thread):

    def __init__(self, lista_processos):
        threading.Thread.__init__(self)
        self.lista_processos = list(lista_processos)
        self.media_espera = 0.0

    def escalonar(self):
        processos_pendentes = sorted(self.lista_processos, key=pegar_tempo_chegada)
        quantidade_processos = len(processos_pendentes)

        tempo_relogio = 0
        soma_tempos_espera = 0

        while len(processos_pendentes) > 0:
            # fila de aptos: processos que ja chegaram
            fila_aptos = []
            for processo in processos_pendentes:
                if processo.tempo_chegada <= tempo_relogio:
                    fila_aptos.append(processo)

            # nenhum processo chegou ainda, o relogio avanca
            if len(fila_aptos) == 0:
                tempo_relogio += 1
                continue

            # escolhe o processo com a maior prioridade (menor numero)
            processo_escolhido = fila_aptos[0]
            for processo in fila_aptos:
                if processo.prioridade < processo_escolhido.prioridade:
                    processo_escolhido = processo

            tempo_espera = tempo_relogio - processo_escolhido.tempo_chegada
            soma_tempos_espera += tempo_espera
            print(f'Prioridades -> {processo_escolhido.identificacao} esperou {tempo_espera}')

            print(f'Prioridades -> {processo_escolhido.identificacao} executando...')
            time.sleep(processo_escolhido.tempo_cpu * SEGUNDOS_POR_UNIDADE_CPU)

            tempo_relogio += processo_escolhido.tempo_cpu
            processos_pendentes.remove(processo_escolhido)

        return soma_tempos_espera / quantidade_processos

    def run(self):
        print('Algoritmo de Prioridades')
        self.media_espera = self.escalonar()
        print(f'Media de espera Prioridades: {self.media_espera:.2f}\n')


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

    thread_sjf = ThreadSJF(lista_processos)
    thread_sjf.start()
    thread_sjf.join()

    thread_prioridades = ThreadPrioridades(lista_processos)
    thread_prioridades.start()
    thread_prioridades.join()

    # saida do simulador: media de espera de cada algoritmo
    nomes_algoritmos = ['FCFS', 'SJF', 'Prioridades']
    medias_espera = [thread_fcfs.media_espera,
                     thread_sjf.media_espera,
                     thread_prioridades.media_espera]

    print('Resumo das medias de espera:')
    for posicao in range(len(nomes_algoritmos)):
        print(f'{nomes_algoritmos[posicao]}: {medias_espera[posicao]:.2f}')

    gerar_grafico(nomes_algoritmos, medias_espera)


# Ponto de entrada do programa
main()
