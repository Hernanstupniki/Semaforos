import threading
import time

# Variables compartidas
n = 0
s = threading.Semaphore(1)  # Semáforo binario
producidos = 0
retardo = threading.Semaphore(0)

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
        s.acquire()  # Espera a que el semáforo esté disponible
        añadir()
        n += 1
        if n == 1:
            retardo.release()  # Desbloquea al consumidor si es el primer elemento
        s.release()  # Libera el semáforo
        time.sleep(1)  # Simulación de tiempo de producción

def consumidor():
    global n, producidos
    retardo.acquire()  # Espera hasta que el productor haya producido al menos un elemento
    while True:
        s.acquire()  # Espera a que el semáforo esté disponible
        extraer()
        n -= 1
        s.release()  # Libera el semáforo
        consumir()
        producidos -= 1
        producidos1()
        if n == 0:
            retardo.acquire()  # Si no hay más elementos, espera a que el productor produzca más
        time.sleep(4)  # Simulación de tiempo de consumo

if __name__ == "__main__":
    productor_thread = threading.Thread(target=productor)
    consumidor_thread = threading.Thread(target=consumidor)

    productor_thread.start()
    consumidor_thread.start()

    productor_thread.join()
    consumidor_thread.join()