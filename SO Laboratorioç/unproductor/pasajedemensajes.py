import threading
import time
from queue import Queue

# Variables compartidas
max_items = 10  # Máximo número de elementos que se pueden almacenar en la cola
producidos = 0

# Cola para pasar los mensajes entre el productor y el consumidor
cola = Queue(max_items)  # Cola con un límite máximo de 10 elementos

def producidos1():
    print(f"Producidos: {producidos}")

def producir():
    print("Produciendo...")

def añadir():
    print("Añadiendo...")

def extraer():
    print("Extrayendo...")

def consumir():
    print("Consumiendo...")

def productor():
    global producidos
    while True:
        producir()
        producidos += 1
        producidos1()
        time.sleep(1)
        item = "producto"  # El productor genera un "producto"
        cola.put(item)  # Añade el producto a la cola (espera si está llena)
        añadir()
        time.sleep(1)  # Simulación de tiempo de producción

def consumidor():
    global producidos
    while True:
        item = cola.get()  # Extrae un producto de la cola (espera si está vacía)
        extraer()
        consumir()
        producidos -= 1
        producidos1()
        cola.task_done()  # Indica que el consumidor ha procesado el producto
        time.sleep(4)  # Simulación de tiempo de consumo

if __name__ == "__main__":
    productor_thread = threading.Thread(target=productor)
    consumidor_thread = threading.Thread(target=consumidor)

    productor_thread.start()
    consumidor_thread.start()

    productor_thread.join()
    consumidor_thread.join()
