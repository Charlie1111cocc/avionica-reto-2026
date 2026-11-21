import csv
import math
import random

#Muestreo cada 100ms 10 Hz
# Columnas tiempo, altitud, aceleracion, temperatura
# Cinco fases con comportamientos distintos
# El gradiente térmico de la atmósfera estándar en la troposfera es de -0,65 °C por cada 100 metros
# Ruido gaussiano sigma= 0.5m
# Variables iniciales


tiempo = 0
altitud = 0 #apogeo en 480 m
velocidad = 0
aceleracion = 0 
temperatura = 20 #temperatura inicial (Valor arbitrario)

time_ms = []
altitude_m = []
accel_z_ms2 = []
temp_c = []


#Fase 1 : En rampa (2s) altitud cte
    #Aqui altitud y temperatura son constantes, velocidad y aceleracion son 0

for i in range (20): 
    tiempo += 0.1         
    altitud = 0.0         # En rampa la altitud es 0
    accel_z = -9.81        # Gravedad en reposo
    temp = 20.0

    tiempo =round(tiempo,1)
    alt_ruido = altitud + random.gauss(0.0, 0.5)  # Ruido gaussiano
    altitude_m.append(alt_ruido)
    time_ms.append(tiempo)
    accel_z_ruido = accel_z + random.gauss(0.0, 0.5)
    accel_z_ms2.append(accel_z_ruido)
    temp_ruido = temp + random.gauss(0.0, 0.5)
    temp_c.append(temp_ruido)

# Lineas corruptas

altitude_m.append("ERR")
time_ms.append("ERR")
accel_z_ms2.append("ERR")
temp_c.append("ERR")


#fase 2 propulsion durannte 1.5 segundos y una aceleracion de 60m/s^2
for i in range (15): # 1.5 segundos a 10 Hz
    tiempo += 0.1
    aceleracion = 60.0
    velocidad += aceleracion * 0.1  # v = v0 + a*t
    altitud += velocidad * 0.1       # h = h0 + v*t
    temp = temperatura - 0.65 * (altitud / 100.0)          # La temperatura disminuye ligeramente

    tiempo = round(tiempo, 1)
    alt_ruido = altitud + random.gauss(0.0, 0.5)
    altitud = round(altitud, 1)
    altitude_m.append(alt_ruido)
    time_ms.append(tiempo)
    accel_z_ruido = aceleracion + random.gauss(0.0, 0.5)
    accel_z_ms2.append(accel_z_ruido)
    temp_ruido = temp + random.gauss(0.0, 0.5)
    temp_c.append(temp_ruido)

altitude_m.append("ERR")
time_ms.append("ERR")
accel_z_ms2.append("ERR")
temp_c.append("ERR")


#fase 3 Vuelo balistico, sin propulsion hasta 480m
#Primero calculamos el tiempo que tarda en llegar a los 480m
# t = (v - v0) / -a

#print(f"Tiempo hasta que la velocidad sea 0: {t} segundos")
#Lo redondeamos a 9s

for i in range (90): # 9 segundos a 10 Hz
    tiempo += 0.1
    aceleracion = -9.81
    velocidad += aceleracion * 0.1  # v = v0 + a*t
    altitud += velocidad * 0.1       # h = h0 + v*t
    temp = temperatura - 0.65 * (altitud / 100.0)        

    tiempo = round(tiempo, 1)
    altitud = round(altitud, 1)
    alt_ruido = altitud + random.gauss(0.0, 0.5)
    altitude_m.append(alt_ruido)
    time_ms.append(tiempo)
    accel_z_ruido = aceleracion + random.gauss(0.0, 0.5)
    accel_z_ms2.append(accel_z_ruido)
    temp_ruido = temp + random.gauss(0.0, 0.5)
    temp_c.append(temp_ruido)

altitude_m.append("ERR")
time_ms.append("ERR")
accel_z_ms2.append("ERR")
temp_c.append("ERR")

#Suponiendo que el paracaidas se abre a 480 m. Inicia fase 4, descenso con paracaidas, aceleracion de -5 m/s^2 hasta llegar a 0 m
#Calculamos el tiempo que tarda en llegar a 0 m
# t = h/v ==> t = 480 / 6 = 80 segundos
# Fase 4: Descenso con paracaídas a velocidad constante de 6 m/s
for i in range(800): 
    tiempo += 0.1
    aceleracion = -9.81       # Velocidad terminal constante (sin aceleración neta)
    velocidad = -6.0           # Velocidad de descenso fija de 6 m/s
    altitud += velocidad * 0.1 # Resta 0.6 metros en cada paso de 0.1s
    temp = temperatura - 0.65 * (altitud / 100.0)          # La temperatura disminuye ligeramente

    tiempo = round(tiempo, 1)
    altitud = round(altitud, 1)
    alt_ruido = altitud + random.gauss(0.0, 0.5)
    altitude_m.append(alt_ruido)
    time_ms.append(tiempo)
    accel_z_ruido = aceleracion + random.gauss(0.0, 0.5)
    accel_z_ms2.append(accel_z_ruido)
    temp_ruido = temp + random.gauss(0.0, 0.5)
    temp_c.append(temp_ruido)

#Fase 5 t=3segundos
 
for i in range(30): # 3 segundos a 10 Hz
    tiempo += 0.1
    aceleracion = 0.0
    velocidad = 0.0
    altitud = 0.0
    temp = 20.0

    tiempo = round(tiempo, 1)
    alt_ruido = altitud + random.gauss(0.0, 0.5)
    altitude_m.append(alt_ruido)
    time_ms.append(tiempo)
    accel_z_ruido = aceleracion + random.gauss(0.0, 0.5)
    accel_z_ms2.append(accel_z_ruido)
    temp_ruido = temp + random.gauss(0.0, 0.5)
    temp_c.append(temp_ruido   )

print(altitude_m)  # Imprime la lista de altitudes para verificar
print(time_ms)  # Imprime la lista de tiempos para verificar
print(accel_z_ms2)  # Imprime la lista de aceleraciones para verificar
print(temp_c)  # Imprime la lista de temperaturas para verificar  

# Creamos el archivo CSV 

encabezados = ["Tiempo", "Altitud", "Aceleracion", "Temperatura",]
filas = zip(time_ms, altitude_m, accel_z_ms2, temp_c,)

with open("flight_log.csv", mode="w", newline="", encoding="utf-8") as archivo:
  escritor = csv.writer(archivo)
  escritor.writerow(encabezados)
  escritor.writerows(filas)

#Fin de la parte A
