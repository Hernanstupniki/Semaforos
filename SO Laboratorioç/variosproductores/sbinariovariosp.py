import threading
import time

# Variables compartidas
n = 0
s = threading.Semaphore(1)  # Semáforo binario
producidos = 0
retardo = threading.Semaphore(0)

def producidos1():
    print(f"Producidos: {producidos}")

def consumir():
    print("Consumiendo...")

def productor(id_productor):
    global n, producidos
    while True:
        producidos += 1
        producidos1()
        time.sleep(1)
        s.acquire()  # Espera a que el semáforo esté disponible
        n += 1
        if n == 1:
            retardo.release()  # Desbloquea al consumidor si es el primer elemento
        s.release()  # Libera el semáforo
        time.sleep(3)  # Simulación de tiempo de producción

def consumidor():
    global n, producidos
    retardo.acquire()  # Espera hasta que el productor haya producido al menos un elemento
    while True:
        s.acquire()  # Espera a que el semáforo esté disponible
        n -= 1
        s.release()  # Libera el semáforo
        consumir()
        producidos -= 1
        producidos1()
        if n == 0:
            retardo.acquire()  # Si no hay más elementos, espera a que el productor produzca más
        time.sleep(1)  # Simulación de tiempo de consumo

if __name__ == "__main__":
    num_productores = 3  # Número de productores que queremos
    productores_threads = []

    # Crear y arrancar múltiples hilos de productores
    for i in range(num_productores):
        productor_thread = threading.Thread(target=productor, args=(i,))
        productores_threads.append(productor_thread)
        productor_thread.start()

    # Consumidor
    consumidor_thread = threading.Thread(target=consumidor)
    consumidor_thread.start()

    # Esperar a que terminen todos los hilos
    for productor_thread in productores_threads:
        productor_thread.join()

    consumidor_thread.join()
