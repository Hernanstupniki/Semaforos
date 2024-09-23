import threading
import time

# Variables compartidas
n = 0  # Recurso compartido que representa el número de elementos disponibles
max_items = 10  # Máximo número de elementos que se pueden almacenar
producidos = 10

# Semáforos contadores
s_espacios = threading.Semaphore(max_items)  # Contador de espacios disponibles para producir
s_elementos = threading.Semaphore(0)  # Contador de elementos disponibles para consumir

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
    global n, producidos
    while True:
        producir()
        producidos += 1
        producidos1()
        time.sleep(1)
        s_espacios.acquire()  # Espera a que haya un espacio disponible para producir
        añadir()
        n += 1  # Añadir un producto
        print(f"Productor produjo, n = {n}")
        s_elementos.release()  # Señala que hay un nuevo elemento disponible para consumir
        time.sleep(1)  # Simulación de tiempo de producción

def consumidor():
    global n, producidos
    while True:
        s_elementos.acquire()  # Espera a que haya al menos un elemento disponible para consumir
        extraer()
        n -= 1  # Extraer un producto
        print(f"Consumidor consumió, n = {n}")
        s_espacios.release()  # Señala que hay un espacio disponible para producir
        consumir()
        producidos -= 1
        producidos1()
        time.sleep(4)  # Simulación de tiempo de consumo

if __name__ == "__main__":
    productor_thread = threading.Thread(target=productor)
    consumidor_thread = threading.Thread(target=consumidor)

    productor_thread.start()
    consumidor_thread.start()

    productor_thread.join()
    consumidor_thread.join()
