import threading,time, random

class Barbearia:
    #Construtor
    def __init__(self, cadeiras_espera: int, max_clientes:int ):
        self.cadeiras_espera=cadeiras_espera
        self.cadeiras_ocupadas=0
        self.barbeiro_dormindo=threading.Event()
        self.cliente_chegou=threading.Semaphore(0)
        self.max_clientes=max_clientes
        self.clientes_atendidos=0
        self.mutex=threading.Lock()
        self.fila_clientes=[]
        self.expediente_encerrado = False

    def iniciar_barbeiro(self):
        while True:
            self.cliente_chegou.acquire()
    
            with self.mutex:
                 if self.expediente_encerrado and not self.fila_clientes:
                    print("Encerrando o expediente")
                    break
                 if self.fila_clientes:
                    cliente_id=self.fila_clientes.pop(0)
                    self.cadeiras_ocupadas -=1
                    self.clientes_atendidos +=1
                 else:
                    continue
                 
            print(f"O cliente {cliente_id} está tendo o cabelo cortado...\n")
            time.sleep(random.uniform(2,5))
            print(f"Cliente {cliente_id} foi atendido e está saindo. \n")

    def cortar_cabelo(self, cliente_id:int):
        with self.mutex:
            if  self.clientes_atendidos >= self.max_clientes:
                print(f"O máximo de clientes foi atingido. Cliente {cliente_id} não será atendido. ")
                return
            if self.cadeiras_ocupadas < self.cadeiras_espera:
                self.cadeiras_ocupadas +=1
                self.fila_clientes.append(cliente_id)
                print(f'Cliente {cliente_id} entrou e está esperando para ser atendido')
                print(f'Cadeiras ocupadas: {self.cadeiras_ocupadas}/{self.cadeiras_espera}')
                self.cliente_chegou.release()
                self.barbeiro_dormindo.set()
            else:
                print(f"Cliente {cliente_id} a barbearia está cheia, e está indo embora")
                return
        
class Cliente(threading.Thread):
    def __init__(self, barbearia: Barbearia, cliente_id:int):
        super().__init__()
        self.barbearia=barbearia
        self.cliente_id=cliente_id
    def run(self):
        self.barbearia.cortar_cabelo(self.cliente_id)

def main():
    #Adicionando um máx de clientes para não ter um loop infinito
    max_clientes=15
    barbearia=Barbearia(cadeiras_espera=10, max_clientes=max_clientes)
    barbeiro_thread=threading.Thread(target=barbearia.iniciar_barbeiro,daemon=True)
    barbeiro_thread.start() #daemon é um thread especial que
    #interrompe a execução da thread assim que a main é encerrada
    cliente_id=1
    while cliente_id<= max_clientes:
        time.sleep(random.uniform(0.5,2))
        Cliente(barbearia,cliente_id).start()
        cliente_id +=1

    with barbearia.mutex:
        barbearia.expediente_encerrado=True
    barbearia.cliente_chegou.release()

    barbeiro_thread.join()
    print("Todos os clientes foram atendidos !!")

if __name__ == "__main__":
    main()
