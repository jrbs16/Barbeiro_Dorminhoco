import threading,time, random


class Barbearia:
    #Construtor
    def __init__(self, cadeiras_espera: int):
        self.cadeiras_espera=cadeiras_espera
        self.cadeiras_ocupadas=0
        self.barbeiro_dormindo=threading.Event()
        self.cliente_chegou=threading.Semaphore(0)
        self.mutex=threading.Lock()

    def cortar_cabelo(self, cliente_id:int):
        with self.mutex:
            if self.cadeiras_ocupadas < self.cadeiras_espera:
                self.cadeiras_ocupadas +=1
                print(f'Cliente {cliente_id} entrou e está esperando para ser atendido')
                print(f'Cadeiras ocupadas: {self.cadeiras_ocupadas}/{self.cadeiras_espera}')
                self.cliente_chegou.release()
            else:
                print(f"Cliente {cliente_id} a barbearia está cheia, e está indo embora")
                return
            
        self.barbeiro_dormindo.set()
        self.cliente_chegou.acquire()

        with self.mutex:
            self.cadeiras_ocupadas -=1
        
        print(f"O cliente {cliente_id} está tendo o cabelo cortado...")
        time.sleep(random.uniform(2,5))
        print(f"Cliente {cliente_id} foi atendido e está saindo.")

    def iniciar_barbeiro(self):
        while True:
            print("Aguardando clientes")
            self.barbeiro_dormindo.wait()
            self.barbeiro_dormindo.clear()
            self.cliente_chegou.acquire()
            with self.mutex:
                self.cadeiras_ocupadas -= 1
            self.atender_cliente(random.randint(1, 100))


class Cliente(threading.Thread):
    def __init__(self, barbearia: Barbearia, cliente_id:int):
        super().__init__()
        self.barbearia=barbearia
        self.cliente_id=cliente_id

    def run(self):
        self.barbearia.cortar_cabelo(self.cliente_id)

## Fazer a main