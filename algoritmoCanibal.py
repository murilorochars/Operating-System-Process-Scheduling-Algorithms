

import threading
import time
import random

QUANTIDADE_CANIBAIS = 5 
CAPACIDADE_TRAVESSA = 3 
DURACAO_JANTAR = 4 

class Travessa:

    def __init__(self, capacidade_porcoes):
        self.capacidade_porcoes = capacidade_porcoes
        self.porcoes_disponiveis = 0

        self.mutex_travessa = threading.Semaphore(1)
        self.semaforo_travessa_vazia = threading.Semaphore(0)
        self.semaforo_travessa_cheia = threading.Semaphore(0)

    def servir_porcao(self, nome_canibal):
        self.mutex_travessa.acquire()

        if self.porcoes_disponiveis == 0:
            print(f'{nome_canibal} encontrou a travessa vazia e acordou o cozinheiro')
            self.semaforo_travessa_vazia.release()
            self.semaforo_travessa_cheia.acquire()

        self.porcoes_disponiveis -= 1
        print(f'{nome_canibal} se serviu. Porcoes restantes: {self.porcoes_disponiveis}')

        self.mutex_travessa.release()

    def encher_travessa(self):
        self.semaforo_travessa_vazia.acquire()

        self.porcoes_disponiveis = self.capacidade_porcoes
        print(f'Cozinheiro colocou {self.capacidade_porcoes} porcoes na travessa')

        self.semaforo_travessa_cheia.release()


class Canibal(threading.Thread):

    def __init__(self, nome_canibal, travessa):
        threading.Thread.__init__(self)
        self.nome_canibal = nome_canibal
        self.travessa = travessa
        self.daemon = True

    def comer(self):
        print(f'{self.nome_canibal} esta comendo')
        time.sleep(random.uniform(0.5, 2))

    def run(self):
        while True:
            self.travessa.servir_porcao(self.nome_canibal)
            self.comer()


class Cozinheiro(threading.Thread):

    def __init__(self, travessa):
        threading.Thread.__init__(self)
        self.travessa = travessa
        self.daemon = True

    def run(self):
        while True:
            self.travessa.encher_travessa()


def main():
    travessa = Travessa(CAPACIDADE_TRAVESSA)

    cozinheiro = Cozinheiro(travessa)
    cozinheiro.start()

    for numero in range(1, QUANTIDADE_CANIBAIS + 1):
        canibal = Canibal(f'Canibal {numero}', travessa)
        canibal.start()

    time.sleep(DURACAO_JANTAR)
    print('Fim do jantar')


main()
