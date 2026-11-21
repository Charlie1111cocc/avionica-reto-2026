import csv
import matplotlib.pyplot as plt


# Listas donde leeremos  datos
datos = []
datos_limpios = []

altitud_filtrada = []
v_cruda = []
v_filtrada = []
tiempo_apogeo = []

#Abrimos el archivo CSV y leemos los datos
with open("flight_log.csv", mode="r", newline="", encoding="utf-8") as archivo:
    lector = csv.reader(archivo)
    for fila in lector:
        datos.append(fila)

#Contador de filas corruptas
Err = 0
for fila in datos:
    if "ERR" not in fila:
        datos_limpios.append(fila)
    else:
        Err += 1

print("Las filas corruptas son:", Err)

# Ventana elegida para el promedio móvil (5 muestras)
ventana = 5

# Extraemos altitud y tiempo de las filas limpias (sin el encabezado)
altura = [float(fila[1]) for fila in datos_limpios[1:]]
tiempo = [float(fila[0]) for fila in datos_limpios[1:]]
altitud_cruda = altura

# Promedio móvil con ventana deslizante
# Estructra del promedio la saque de gemini
for i in range(len(altura) - ventana + 1):
    suma = 0.0
    for j in range(ventana):
        suma += altura[i + j]

    promedio = suma / ventana
    altitud_filtrada.append(round(promedio, 2))

# Velocidad vertical por diferencias finitas - altitud cruda
# Esta estrcutura tambien la saque de gemini
for i in range(len(altitud_cruda)):
    if i == 0:
        # Diferencia hacia adelante al inicio
        v = (altitud_cruda[1] - altitud_cruda[0]) / (tiempo[1] - tiempo[0])
    elif i == len(altitud_cruda) - 1:
        # Diferencia hacia atrás al final
        v = (altitud_cruda[-1] - altitud_cruda[-2]) / (tiempo[-1] - tiempo[-2])
    else:
        # Diferencia central en el interior
        v = (altitud_cruda[i + 1] - altitud_cruda[i - 1]) / (tiempo[i + 1] - tiempo[i - 1])

    v_cruda.append(v)

# Velocidad vertical por diferencias finitas - altitud filtrada
for i in range(len(altitud_filtrada)):
    if i == 0:
        # Diferencia hacia adelante al inicio
        v = (altitud_filtrada[1] - altitud_filtrada[0]) / (tiempo[1] - tiempo[0])
    elif i == len(altitud_filtrada) - 1:
        # Diferencia hacia atrás al final
        v = (altitud_filtrada[-1] - altitud_filtrada[-2]) / (tiempo[-1] - tiempo[-2])
    else:
        # Diferencia central en el interior
        v = (altitud_filtrada[i + 1] - altitud_filtrada[i - 1]) / (tiempo[i + 1] - tiempo[i - 1])

    v_filtrada.append(v)

# Eventos del vuelo (sobre altitud filtrada)

# El apogeo es el máximo valor de altitud filtrada
apogeo = max(altitud_filtrada)
print("El apogeo es:", apogeo, "metros")

# La altura del despegue es el primer valor de altitud filtrada
despegue = altitud_filtrada[0]
print("El despegue es en:", despegue, "metros")

# La altura del aterrizaje es el último valor de altitud filtrada
aterrizaje = altitud_filtrada[-1]
print("El aterrizaje es en:", aterrizaje, "metros")

# Calculamos en que tiempo se encuntra el apogeo
for i in range(len(altitud_filtrada)):
    if altitud_filtrada[i] == apogeo:
        tiempo_apogeo.append(tiempo[i])
print("El tiempo del apogeo es:", tiempo_apogeo, "segundos")

# la velocidad máxima es el máximo valor de la velocidad filtrada
velocidad_maxima = max(v_filtrada)
print("La velocidad máxima es:", velocidad_maxima, "m/s")

# el tiempo total de vuelo es el último valor de tiempo menos el primer valor de tiempo
tiempo_total = tiempo[-1] - tiempo[0]
print("El tiempo total de vuelo es:", tiempo_total, "segundos")

# Alineamos el tiempo con las muestras filtradas para que zip() no corte filas
tiempo_filtrado = tiempo[:len(altitud_filtrada)]
v_cruda_alineada = v_cruda[:len(altitud_filtrada)]

encabezados = ["Tiempo", "Altitud filtrada", "Altitud cruda", "Velocidad filtrada", "Velocidad cruda"]
filas = zip(tiempo_filtrado, altitud_filtrada, altitud_cruda, v_filtrada, v_cruda_alineada)

with open("flight_processed.csv", mode="w", newline="", encoding="utf-8") as archivo:
    escritor = csv.writer(archivo)
    escritor.writerow(encabezados)
    escritor.writerows(filas)

#Graficas de los datos

# Altitud filtrada vs tiempo
plt.plot(tiempo_filtrado, altitud_filtrada, marker="o", linestyle="-", color="blue")
plt.title("Altitud filtrada vs. Tiempo")
plt.xlabel("Tiempo (s)")
plt.ylabel("Altitud filtrada (m)")
plt.grid(True)
plt.show()

# Altitud cruda vs tiempo
plt.plot(tiempo_filtrado, altitud_cruda[:len(tiempo_filtrado)], marker="o", linestyle="-", color="orange")
plt.title("Altitud cruda vs. Tiempo")
plt.xlabel("Tiempo (s)")
plt.ylabel("Altitud cruda (m)")
plt.grid(True)
plt.show()

# Velocidad filtrada vs tiempo
plt.plot(tiempo_filtrado, v_filtrada, marker="o", linestyle="-", color="green")
plt.title("Velocidad filtrada vs. Tiempo")
plt.xlabel("Tiempo (s)")
plt.ylabel("Velocidad filtrada (m/s)")
plt.grid(True)
plt.show()

# Velocidad cruda vs tiempo
plt.plot(tiempo_filtrado, v_cruda_alineada, marker="o", linestyle="-", color="red")
plt.title("Velocidad cruda vs. Tiempo")
plt.xlabel("Tiempo (s)")
plt.ylabel("Velocidad cruda (m/s)")
plt.grid(True)
plt.show()