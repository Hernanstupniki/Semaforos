import threading
import time
from queue import Queue

# Variables compartidas
max_items = 10  # Máximo número de elementos que se pueden almacenar en la cola
producidos = 0

# Cola para pasar los mensajes entre el productor y el consumidor
cola = Queue(max_items)  # Cola con un límite máximo de 10 elementos
producidos_lock = threading.Lock()  # Añadimos un lock para evitar condiciones de carrera

def producidos1():
    with producidos_lock:
        print(f"Producidos: {producidos}")

def consumir():
    print("Consumiendo...")

def productor(id_productor):
    global producidos
    while True:
        with producidos_lock:
            producidos += 1
        producidos1()
        time.sleep(1)
        item = f"producto de productor {id_productor}"  # El productor genera un "producto"
        cola.put(item)  # Añade el producto a la cola (espera si está llena)
        time.sleep(2)  # Simulación de tiempo de producción

def consumidor():
    global producidos
    while True:
        item = cola.get()  # Extrae un producto de la cola (espera si está vacía)
        consumir()
        with producidos_lock:
            producidos -= 1
        producidos1()
        cola.task_done()  # Indica que el consumidor ha procesado el producto
        time.sleep(1)  # Simulación de tiempo de consumo

if __name__ == "__main__":
    num_productores = 3  # Número de productores
    productores_threads = []

    # Crear hilos para los productores
    for i in range(num_productores):
        productor_thread = threading.Thread(target=productor, args=(i,))
        productores_threads.append(productor_thread)
        productor_thread.start()

    # Crear hilo para el consumidor
    consumidor_thread = threading.Thread(target=consumidor)
    consumidor_thread.start()

    # Esperar a que los hilos de los productores terminen
    for productor_thread in productores_threads:
        productor_thread.join()

    # Esperar a que el hilo del consumidor termine
    consumidor_thread.join()
