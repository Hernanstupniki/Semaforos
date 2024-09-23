import threading
import time

# Variables globales
contador_con_carrera = 0
contador_sin_carrera = 0
veces_a_incrementar = 100000
numero_de_hilos = 10
semaforo = threading.Lock()  # Usamos un Lock como semáforo

# Función con condición de carrera (sin semáforo)
def incrementar_sin_sincronizacion():
    global contador_con_carrera
    for _ in range(veces_a_incrementar):
        valor_temporal = contador_con_carrera
        time.sleep(0.000001)  # Simular retraso
        contador_con_carrera = valor_temporal + 1

# Función sin condición de carrera (con semáforo)
def incrementar_con_semaforo():
    global contador_sin_carrera
    for _ in range(veces_a_incrementar):
        with semaforo:  # Solo un hilo puede ejecutar este bloque a la vez
            contador_sin_carrera += 1

# Crear y ejecutar los hilos para la condición de carrera
def simulacion_con_carrera():
    global contador_con_carrera
    contador_con_carrera = 0  # Reiniciar el contador
    hilos = []
    for _ in range(numero_de_hilos):
        hilo = threading.Thread(target=incrementar_sin_sincronizacion)
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()

# Simulación sin carrera (con semáforo)
def simulacion_sin_carrera():
    global contador_sin_carrera
    contador_sin_carrera = 0  # Reiniciar el contador
    hilos = []
    for _ in range(numero_de_hilos):
        hilo = threading.Thread(target=incrementar_con_semaforo)
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()

# Ejecutar simulaciones
simulacion_con_carrera()
simulacion_sin_carrera()

# Resultados
print(f"Valor esperado sin condición de carrera (con semáforo): {contador_sin_carrera}")
print(f"Valor obtenido con condición de carrera: {contador_con_carrera}")
