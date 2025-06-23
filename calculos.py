import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import shapiro
from collections import Counter
from scipy.stats import norm
import random

# PASO 3: Convertir entradas en validas para el sistema
def procesarEntrada(p, aleatorios):
    exitos = aleatorios <= p
    return np.sum(exitos) # PASO 4: Transformar las entradas en salidas

# PASO 2: Generar los numeros aleatorios
def generarAleatorios (n_balls, n_levels):
    aleatorios = []
    for _ in range(n_balls):
        aleatorios.append(np.random.uniform(0, 1, n_levels))
    return aleatorios

# Funcion para obtener numeros aleatorios para el triangulo especifico
def transformarAleatorios (aleatorios):
    primeros_aleatorios = []
    for x in range(len(aleatorios)):
        primeros_aleatorios.append(aleatorios[x][0:3])
    segundos_aleatorios = []
    if len(aleatorios) > 4:
        for x in range(len(aleatorios)):
            segundos_aleatorios.append(aleatorios[x][4:(len(aleatorios) - 1)])
    triangulo_aleatorios = []
    for x in aleatorios:
        triangulo_aleatorios.append(x[3])
    return primeros_aleatorios, segundos_aleatorios, triangulo_aleatorios

def simular_triangulo(n_balls=100, n_levels=10, aleatorios = None):
    results = np.zeros(n_levels + 1) # Genero array de receptáculos (arrancan en 0 para contar la cantidad de bolas)
    if aleatorios is None: # Me fijo si tengo que generar numeros aleatorios
        aleatorios = generarAleatorios(n_balls, n_levels)
        
    for b in range(n_balls): 
        right_moves = procesarEntrada(0.5, aleatorios[b]) # Por bola calculo el receptaculo donde cae
        results[right_moves] += 1 # Sumo la bola al receptaculo
    return results

# Funcion para simular el triangulo especifico
def simular_triangulo_especifico (n_balls=100, n_levels=10, triangulo=-1, aleatorios = None):
    # En caso de tener 3 o menos renglones lo hago sin esta funcion
    if n_levels <= 3:
        return simular_triangulo(n_balls, n_levels, aleatorios)
    
    results = np.zeros(n_levels + 1) # Genero array de receptáculos (arrancan en 0 para contar la cantidad de bolas)
    
    # Si no tengo la posicion del triangulo la genero
    triangulo = int(random.random() * 4) if triangulo < 0 else triangulo
    
    primeros_aleatorios, segundos_aleatorios, triangulo_aleatorios = transformarAleatorios(generarAleatorios(n_balls, n_levels) if aleatorios is None else aleatorios)

    for b in range(n_balls):
        # Calculo el triangulo donde va a caer
        right_moves = procesarEntrada(0.5, primeros_aleatorios[b])
        
        # En caso de que coincida el trianguo o no varío la probabilidad
        if right_moves == triangulo:
            p = procesarEntrada(0.3, triangulo_aleatorios[b])
            right_moves += p
        else:
            right_moves += procesarEntrada(0.5, triangulo_aleatorios[b])
        
        # Por ultimo sigo haciendo el resto de iteraciones hasta que llegue al receptaculo
        if (len(segundos_aleatorios) > 0):
            right_moves += procesarEntrada(0.5, segundos_aleatorios[b])
            
        results[right_moves] += 1 # Agrego la bola al receptaculo
    return results

# PASO 5: Realizar contabilidad y estadistica de los resultados

def generar_aproximacion(datos, numero):

    # Paso los receptaculos para que arranquen en 1
    for d in range(len(datos)):
        datos[d] += 1
    
    # Se pasa a frecuencia los valores para manejar las estadisticas
    freqs = Counter(datos)
    valores = sorted(freqs.keys())
    cantidades = [freqs[val] for val in valores]

    plt.figure()

    total = sum(cantidades)
    densidades = [c / total for c in cantidades]
    plt.bar(valores, densidades, width=0.8, color='skyblue', edgecolor='black')

    media = np.mean(datos) # Calculo de media
    std_dev = np.std(datos, ddof=0) # Calculo de desvio estandar
    x = np.linspace(min(valores)-1, max(valores)+1, 200)
    pdf_normal = norm.pdf(x, loc=media, scale=std_dev)
    plt.plot(x, pdf_normal, 'r--')

    # Etiquetas
    plt.title('Comparación con distribución normal')
    plt.xlabel('Receptáculo')
    plt.ylabel('Cantidad de bolas')
    plt.legend()
    plt.grid(True)
    plt.savefig(f"img/aproximacion{numero}.png")
    plt.close()

def analizar_normalidad (datos):
    stat, p_value = shapiro(datos) # Utilizamos Scipy para hacer uso de Shapiro-Wilk
    
    # Coeficiente de variación
    media = np.mean(datos)
    std_dev = np.std(datos, ddof=0)
    cv = std_dev / media
    return cv, cv <= 0.25, p_value, p_value > 0.05