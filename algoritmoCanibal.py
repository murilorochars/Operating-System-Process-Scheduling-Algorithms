'''
Problema do Jantar dos Canibais usando threads e semaforos.
N canibais comem de uma travessa que comporta M porcoes.
Quando a travessa esvazia, um canibal acorda o cozinheiro,
que coloca mais M porcoes na travessa.
'''

import threading


# Classe que representa a travessa compartilhada
class Travessa:

    def __init__(self, capacidade_porcoes):
        self.capacidade_porcoes = capacidade_porcoes
        self.porcoes_disponiveis = 0

        # garante que so um canibal mexe na travessa por vez
        self.mutex_travessa = threading.Semaphore(1)
        # usado para acordar o cozinheiro quando a travessa esta vazia
        self.semaforo_travessa_vazia = threading.Semaphore(0)
        # usado para avisar o canibal que a travessa foi enchida
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
