import threading
import time
import random

# Semáforos
mutex = threading.Semaphore(1)      # Controla acceso a lectores_leyendo
lectores_mutex = threading.Semaphore(1)  # Controla la actualización del recurso al final de la escritura
lectores_leyendo = 0                # Número de lectores activos

# Recurso compartido (simulación)
recurso = "Recurso compartido"
recurso_estable = recurso  # Versión estable del recurso que los lectores pueden leer
valor = 1  # Nueva variable que se incrementará con cada escritura

# Función para los lectores
def lector(id_lector):
    global lectores_leyendo, recurso_estable
    while True:
        time.sleep(random.uniform(2, 10))  # Simular tiempo de espera aleatorio antes de leer
        
        # Inicio de sección crítica para lectores
        mutex.acquire()
        lectores_leyendo += 1
        mutex.release()

        # Determinar si el lector leerá el recurso estable o no (probabilidad del 20%)
        if random.random() < 0.2:
            # Sección crítica (lectura de la versión estable del recurso)
            print(f"Lector {id_lector} está leyendo la versión estable del recurso con valor: {valor}...")
        else:
            print(f"Lector {id_lector} está leyendo la nueva versión del recurso con valor: {valor}...")     
        time.sleep(random.uniform(3, 6))  # Simular tiempo de lectura
        print(f"Lector {id_lector} terminó de leer.")

        # Fin de sección crítica para lectores
        mutex.acquire()
        lectores_leyendo -= 1
        if lectores_leyendo == 0:
            lectores_mutex.release()  # Permitir al escritor actualizar el recurso si no hay lectores
        mutex.release()

# Función para los escritores
def escritor(id_escritor):
    global recurso, recurso_estable, valor
    while True:
        time.sleep(random.uniform(2, 4))  # Simular tiempo de espera aleatorio antes de escribir
        
        # El escritor espera que no haya lectores antes de actualizar el recurso estable
        lectores_mutex.acquire()

        # Actualizar el recurso pero no la versión estable aún
        nuevo_valor = valor + 1
        nuevo_recurso = f"Recurso modificado con un nuevo valor {nuevo_valor}"
        print(f"Escritor {id_escritor} está escribiendo en el recurso con un nuevo valor de: {nuevo_valor}...")
        time.sleep(random.uniform(3, 10))  # Simular tiempo de escritura

        # Una vez que termina la escritura, se actualiza la versión estable
        recurso_estable = nuevo_recurso
        valor = nuevo_valor
        print(f"Escritor {id_escritor} terminó de escribir. Nuevo recurso estable: {valor}")

        # Liberar el semáforo para permitir a los lectores continuar
        lectores_mutex.release()

# Crear múltiples lectores y escritores
num_lectores = 5
num_escritores = 2

# Crear hilos para lectores
for i in range(num_lectores):
    hilo_lector = threading.Thread(target=lector, args=(i+1,))
    hilo_lector.start()

# Crear hilos para escritores
for i in range(num_escritores):
    hilo_escritor = threading.Thread(target=escritor, args=(i+1,))
    hilo_escritor.start()
