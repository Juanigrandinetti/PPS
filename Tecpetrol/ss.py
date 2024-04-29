import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats, signal
import numpy as np
dt         = 0.01
tolerancia_planta_operativa = 0.1

def regresion_lineal(data):
  m, b, r_value, p_value, std_err = stats.linregress(range(len(data)), data)
  return m, b

# Importar datos del Excel
# Datos:
# Temperatura Proceso
# Temperatura Ambiente
# Velocidad de vibración
df = pd.read_excel(r'C:\Tecpetrol\00973414\Sushi_Datos.xlsx',
                  sheet_name = 'Sushi_Datos')

# Selección de columnas de interés del Excel
df = df.iloc[:,[2, 3, 4]]

# Selección de rango de datos de interés
#df = df.iloc[60:]

# Convsersión de columna de DataFrame a un array
tProceso = df['Temperatura Proceso'].tolist()
tAmbiente = df['Temperatura Ambiente'].tolist()
tVelocidad = df['Velocidad'].tolist()

# Aproximación de la temperatura ambiente a tavés de una regresíon lineal
# Aprovechar la variación gradual (lenta) de la temperatura ambiente para aproximar la derivada de la temperatura ambiente como una constante
m_tAmbiente, b_tAmbiente = regresion_lineal(tAmbiente)
print(f'Pendiente Temperatura Ambiente: {round(m_tAmbiente, 4)}')

tProcesoD  = []
tAmbienteD = []
tCompresor = []
# Obtener la derivada de la temperatura del proceso
# Obtener la derivada de la temperatura ambiente
for i in range(df.shape[0] - 1):
    if i != df.shape[0]:
        tProcesoD = np.diff(df['Temperatura Proceso'], 1)
        tAmbienteD = np.diff(df['Temperatura Ambiente'], 1)

# Obtener la segunda derivada de la temperatura del proceso
tProcesoDD = []
for i in range(len(tProcesoD) - 1):
  tProcesoDD.append((tProcesoD[i + 1] - tProcesoD[i])/dt)
# Bucle para decidir si el compresor esta prendido o apagado
for i in range(len(tProcesoD)):
  # Verificar que la derivada en t = ti sea distinta de 0 (x/0 = inf)
  if tProcesoD[i] != 0:
    # Verificar que la derivada de la temperatura del proceso sea un x% mayor que la temperatura del ambiente, donde x = 'tolerancia_planta_operativa' (ajustable)
    # Mientras mayor sea esta constante, más seguridad habrá de que el compresor está realmente prendido
    if m_tAmbiente/tProcesoD[i] < tolerancia_planta_operativa:
        # Verificar que la derivada de la temperatura de proceso sea positiva (tempratura del proceso creciente)
        if (tProcesoD[i] > 0):
            # Verificar si la derivada siguiente cayó más del 40% que la actual (compresor apagado)
            if (tProcesoD[i + 1] < 0.6*tProcesoD[i]):
              tCompresor.append(0)
              print(f'i = {i} | Derivada ({tProcesoD[i + 1]}) en i + 1 = {i + 1} cayó más del 40% de la derivada en i = {i} ({tProcesoD[i]}) --> Compresor Apagado')
            else:
               # Verificar si la derivada en 2 iteraciones más cayó más del 40% que la anterior (compresor apagado)
               if (tProcesoD[i + 2] < 0.6*tProcesoD[i + 1]):
                 tCompresor.append(0)
                 print(f'i = {i} | Derivada ({tProcesoD[i + 2]}) en i + 2 = {i + 2} cayó más del 40% de la derivada en i = {i + 1} ({tProcesoD[i + 1]}) --> Derivada Decreciendo --> Compresor Apagado')
               # Verificar si la derivada en 3 iteraciones más cayó más del 40% que la anterior (compresor apagado)
               elif (tProcesoD[i + 3] < 0.6*tProcesoD[i + 2]):
                 tCompresor.append(0)
                 print(f'i = {i} | Derivada ({tProcesoD[i + 3]}) en i + 3 = {i + 3} cayó más del 40% de la derivada en i = {i + 2} ({tProcesoD[i + 2]}) --> Derivada Decreciendo --> Compresor Apagado')
               # Caso contrario el compresor está prendido
               else:
                 tCompresor.append(1)
                 print(f'i = {i} | Derivada en i + 1 = {i + 1}, i + 2 = {i + 2}, i + 3 = {i + 3} no cayeron más del 40% --> Derivada Creciendo--> Compresor Prendido')
        # Si la derivada es negativa, el compresor esta apagado
        else:
          tCompresor.append(0)
          print(f'i = {i} | Derivada ({tProcesoD[i]}) en i = {i} es menor a 0 --> Compresor Apagado')
  # Si la derivada es nula
    # Si i > 0, entonces el valor del compresor es el mismo que en t = ti-1
    # Si i == 0, entonces el compresor esta apagado
  else: tCompresor.append(tCompresor[i - 1]) if i else tCompresor.append(0)

# Bucle para determinar dónde están los máximos de la temperatura del proceso (para la gráfica)
fd   = []
for i in range(1, len(tProcesoD) - 2):
  if ((tProcesoD[i - 1] > 0) & (tProcesoD[i] < 0) or
      (tProcesoD[i - 1] > 0) & ((tProcesoD[i] == 0) & ((tProcesoD[i + 1] < 0))) or
      (tProcesoD[i - 1] > 0) & ((tProcesoD[i] == 0) & ((tProcesoD[i + 1] == 0)) & ((tProcesoD[i + 2] < 0)))): fd.append(i)

plt.figure(1)
plt.plot(tVelocidad, label = 'Velocidad')
plt.plot(tCompresor, label = 'On/Off')
plt.legend()
plt.grid(True)
plt.show()

fig, (x1, x2, x3, x4) = plt.subplots(4, 1, sharex=True)

x1.plot(tProceso, label = 'Temperatura Proceso')
for i in range(len(fd)):
  x1.axvline(fd[i], color = 'black', linestyle = '--')
x1.set_title('Medición Sushi Sensor')
x1.set_ylabel('Temperatura (°C)')
x1.legend()
x1.grid(True)

x2.plot(tProcesoDD, label = 'Segunda Derivada Temperatura Proceso')
x2.set_ylabel('Temperatura (°C)')
x2.legend()
x2.grid(True)

x3.plot(tVelocidad, label = 'Velocidad')
x3.plot(tCompresor, label = 'On/Off')
for i in range(len(fd)):
  x3.axvline(fd[i], color = 'black', linestyle = '--')
x3.set_ylabel('Velocidad (m/s)')
x3.legend()
x3.grid(True)
plt.subplots_adjust(hspace = 0.2)

x4.plot(tProcesoD, label = 'Derivada Temperatura Proceso')
#x4.plot(derivada_integral, label = 'Derivada por integración')
for i in range(len(fd)):
  x4.axvline(fd[i], color = 'black', linestyle = '--')
x4.set_title('Medición Sushi Sensor')
x4.set_xlabel('Tiempo(s)')
x4.set_ylabel('Temperatura (°C)')
x4.legend()
x4.grid(True)
plt.show()
