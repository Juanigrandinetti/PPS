import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def regresion_lineal(data):
  m, b, r_value, p_value, std_err = stats.linregress(range(len(data)), data)
  return m, b

# Supongamos que los datos llegan cada 1 segundo
dt = 1

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
df = df.iloc[60:]

# Convsersión de columna de DataFrame a un array
tProceso = df['Temperatura Proceso'].tolist()
tAmbiente = df['Temperatura Ambiente'].tolist()
tVelocidad = df['Velocidad'].tolist()

# El código implementado en CI Server va a empezar con:
# while(1):
# Un alternativa es correr una sub rutina que se active cada vez que recibe un nuevo dato, para que el código no corra innecesariamente
# En este caso, tengo el array con los datos de temperatura asi que será un bucle for
pen = []
temp = []
for i in range(len(tProceso)):
    # Simular que los datos llegan en serie y se guardan en un array
    temp.append(tProceso[i])
    # Necesito al menos 2 datos para calcular la pendiente en 1 punto
    if len(temp) > 1:
        print(len(temp))
        # Cálculo de la pendiente en t = ti
        pen.append(regresion_lineal(temp[:])[0])
    # Si tengo menos de 2 datos no hago nada
    else: continue

#plt.scatter(np.linspace(1, 100, 734), pen)
#plt.show()
fig, ax1 = plt.subplots()
ax1.set_xlabel('Tiempo (s)')
ax1.scatter(np.linspace(0, 734, 734), tProceso[:734], color = 'tab:blue')
ax1.plot(tProceso, color = 'tab:orange')
ax1.tick_params(axis = 'y', labelcolor = 'tab:blue')
ax2 = ax1.twinx()
ax2.plot(pen, color = 'tab:orange')
ax2.scatter(np.linspace(0, 734, 734), pen)
ax2.tick_params(axis = 'y', labelcolor = 'tab:orange')
fig.tight_layout()
plt.show()