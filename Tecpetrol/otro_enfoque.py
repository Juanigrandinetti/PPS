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
df = pd.read_excel(r'C:\Users\juani\PPS\Tecpetrol\Sushi_Datos.xlsx',
                  sheet_name = 'Sushi_Datos')

# Selección de columnas de interés del Excel
df = df.iloc[:,[2, 3, 4]]

# Selección de rango de datos de interés
df = df.iloc[60:]

# Convsersión de columna de DataFrame a un array
tProceso = df['Temperatura Proceso'].tolist()
tAmbiente = df['Temperatura Ambiente'].tolist()
tVelocidad = df['Velocidad'].tolist()
# Regresión Lineal de la Temperatura Ambiente
m1, b = regresion_lineal(tAmbiente)
ta = []
for i in range(len(tAmbiente)):
    ta.append((m1*i) + b)
# Visualizar la gráfica de la Temperatura Ambiente
plt.plot(ta)
plt.scatter(np.linspace(0, len(tAmbiente), len(tAmbiente)), tAmbiente, color = 'blue')
plt.plot(tAmbiente, color = 'orange')
plt.show()
# Conclusión: la derivada de la Temperatura del Proceso, si está operativo, entonces será relativamente mayor que la derivada de la
# Temperatura Ambiente.

# El código implementado en CI Server va a empezar con:
# while(1):
# Un alternativa es correr una sub rutina que se active cada vez que recibe un nuevo dato, para que el código no corra innecesariamente
# En este caso, tengo el array con los datos de temperatura asi que será un bucle for
tempp = []
tempa = []
tpd   = []
tad   = []
y     = []
for i in range(len(tProceso)):
    # Simular que los datos llegan en serie y se guardan en un array
    tempp.append(tProceso[i])
    tempa.append(tAmbiente[i])
    # Necesito al menos 2 datos para calcular la pendiente en 1 punto
    if len(tempp) > 1:
        # Cálculo de la pendiente en t = ti de la Temperatura del Proceso y la Temperatura Ambiente
        mp = regresion_lineal(tempp[len(tempp) - 2:len(tempp)])[0]
        ma = regresion_lineal(tempa[len(tempa) - 2:len(tempa)])[0]
        tpd.append(mp)
        tad.append(ma)
        # Si la Temperatura Ambiente no es parecida a la Temperatura del Proceso
        if mp > 0: y.append(1)
        elif mp == 0:
            try:
                y.append(y[i - 1])
            except IndexError: y.append(0)
        else: y.append(0)
        # La Temperatura del Proceso se asemeja a la Temperatura Ambiente, el proceso probablemente esté inactivo
    # Si tengo menos de 2 datos no hago nada
    else: continue
fig2, axp = plt.subplots()
axp.set_xlabel = ('Tiempo (s)')
axp.plot(y, color = 'orange')
axp.tick_params(axis = 'y', labelcolor = 'tab:orange')
axs = axp.twinx()
axs.plot(tProceso, color = 'blue')
axp.tick_params(axis = 'y', labelcolor = 'tab:blue')
fig2.tight_layout()
plt.show()
#plt.scatter(np.linspace(1, 100, 734), pen)
#plt.show()
fig, ax1 = plt.subplots()
ax1.set_xlabel('Tiempo (s)')
ax1.scatter(np.linspace(0, 734, 734), tProceso[:734], color = 'tab:blue')
ax1.plot(tProceso, color = 'tab:orange')
ax1.tick_params(axis = 'y', labelcolor = 'tab:blue')
ax2 = ax1.twinx()
ax2.plot(tpd, color = 'tab:orange')
ax2.scatter(np.linspace(0, 734, 734), tpd)
ax2.tick_params(axis = 'y', labelcolor = 'tab:orange')
fig.tight_layout()
plt.show()
