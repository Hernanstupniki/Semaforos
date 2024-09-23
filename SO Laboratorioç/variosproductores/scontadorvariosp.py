import threading
import time

# Variables compartidas
n = 0
s = threading.Semaphore(1)  # Semáforo para controlar el acceso a 'n'
producidos = 0
elementos_disponibles = threading.Semaphore(0)  # Semáforo contador para los elementos disponibles
espacios_disponibles = threading.Semaphore(10)  # Supongamos que hay un buffer con 10 espacios disponibles

def producidos1():
    print(f"Producidos: {producidos}")

def consumir():
    print("Consumiendo...")

def productor(id_productor):
    global n, producidos
    while True:
        time.sleep(1)  # Simulación de tiempo de producción
        producidos += 1
        producidos1()

        espacios_disponibles.acquire()  # Espera a que haya espacio en el buffer
        s.acquire()  # Controla el acceso a la variable 'n'
        n += 1
        print(f"Productor {id_productor} produjo, n = {n}")
        s.release()  # Libera el semáforo
        elementos_disponibles.release()  # Aumenta el contador de elementos disponibles
        time.sleep(1)  # Simulación de tiempo entre producciones

def consumidor():
    global n, producidos
    while True:
        elementos_disponibles.acquire()  # Espera hasta que haya elementos disponibles
        s.acquire()  # Controla el acceso a la variable 'n'
        n -= 1
        print(f"Consumidor consumió, n = {n}")
        s.release()  # Libera el semáforo
        consumir()
        producidos -= 1
        producidos1()
        espacios_disponibles.release()  # Aumenta el contador de espacios disponibles
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
