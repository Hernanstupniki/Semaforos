import threading
import time
import random

# Semáforos
rw_mutex = threading.Semaphore(1)  # Controla acceso al recurso (lectores y escritores)
mutex = threading.Semaphore(1)      # Controla acceso a lectores_leyendo
lectores_leyendo = 0                # Número de lectores activos

# Recurso compartido (simulación)
recurso = "Recurso compartido"
valor = 0  # Nueva variable que se incrementará con cada escritura

# Función para los escritores
def escritor(id_escritor):
    global recurso, valor
    while True:
        time.sleep(random.uniform(2, 4))  # Simular tiempo de espera aleatorio antes de escribir
        
        # Inicio de sección crítica para escritores
        rw_mutex.acquire()  # Escritor espera acceso exclusivo al recurso
        valor += 1  # Incrementar la variable cada vez que un escritor escribe
        print(f"Escritor {id_escritor} está escribiendo en el recurso con un nuevo valor de: {valor}...")
        time.sleep(random.uniform(3, 5))  # Simular tiempo de escritura
        print(f"Escritor {id_escritor} terminó de escribir.")
        rw_mutex.release()


# Función para los lectores
def lector(id_lector):
    global lectores_leyendo, recurso
    while True:
        time.sleep(random.uniform(3, 6))  # Simular tiempo de espera aleatorio antes de leer
        
        # Inicio de sección crítica para lectores
        mutex.acquire()
        lectores_leyendo += 1
        if lectores_leyendo == 1:
            rw_mutex.acquire()  # El primer lector bloquea el acceso de los escritores
        mutex.release()
        time.sleep(random.uniform(1, 3))  # Simular tiempo de lectura 
        # Sección crítica (lectura)
        print(f"Lector {id_lector} está leyendo el recurso con valor: {valor}...")
        time.sleep(random.uniform(3, 6))  # Simular tiempo de lectura
        print(f"Lector {id_lector} terminó de leer.")
        
        # Fin de sección crítica para lectores
        mutex.acquire()
        lectores_leyendo -= 1
        if lectores_leyendo == 0:
            rw_mutex.release()  # El último lector desbloquea el acceso de los escritores
        mutex.release()

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
