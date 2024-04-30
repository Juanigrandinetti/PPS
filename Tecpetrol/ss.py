import pandas as pd
from threading import Thread
from time import sleep

def alarma():
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
  #df = df.iloc[60:]

  # Convsersión de columna de DataFrame a un array
  tProceso = df['Temperatura Proceso'].tolist()
  tAmbiente = df['Temperatura Ambiente'].tolist()

  # El código implementado en CI Server va a empezar con:
  # while(1):
  # Un alternativa es correr una sub rutina que se active cada vez que recibe un nuevo dato, para que el código no corra innecesariamente
  # En este caso, tengo el array con los datos de temperatura asi que será un bucle for
  tempp = []
  tempa = []
  y     = []
  sum   = []

  for i in range(len(tProceso)):
      # Simular que los datos llegan en serie y se guardan en un array
      tempp.append(tProceso[i])
      tempa.append(tAmbiente[i])
      # Necesito al menos 2 datos para calcular la pendiente en 1 punto
      if len(tempp) > 1:
          # Cálculo de la pendiente en t = ti de la Temperatura del Proceso y la Temperatura Ambiente
          mp = (tempp[len(tempp) - 1] - tempp[len(tempp) - 2])/dt
          ma = (tempa[len(tempa) - 1] - tempa[len(tempa) - 2])/dt
          # Verificar si la derivada de la Temperatura del Proceso es un 10% superior a la derivada de la Temperatura Ambiente
          sum.append('on') if abs(ma) < 0.1*abs(mp) else sum.append('off')
          if len(sum) > 4:
            # Verificar si en los últimos 5 datos, la derivada de la temperatura Ambiente fue siempre un 10% mayor que la derviada de la Temperatura del Proceso
            # Caso afirmativo, Proceso Inactivo
            if not 'on' in sum[len(sum) - 5:len(sum)]:
              y.append(0)
              print('!Alarma Encendida!')
              sleep(5)
            # Caso contrario, Proceso Activo
            else:
              if mp > 0:
                y.append(1)
                print('!Alarma Apagada!')
                sleep(5)
              elif mp == 0:
                try:
                  y.append(y[-1])
                  if y[-1] == 0:
                    print('¡Alarma Encendida!')
                    sleep(5)
                  else:
                    print('¡Alarma Apagada!')
                    sleep(5)
                except IndexError:
                  y.append(0)
                  print('!Alarma Encendida!')
                  sleep(5)
              else:
                y.append(0)
                print('!Alarma Encendida!')
                sleep(5)
          # Si no hay 5 datos todavía, realizar el algoritmo sin tener en cuenta la Temperatura Ambiente
          else:
            if mp > 0:
              y.append(1)
              print('!Alarma Apagada!')
              sleep(5)
            elif mp == 0:
              try:
                y.append(y[-1])
                if y[-1] == 0:
                  print('¡Alarma Encendida!')
                  sleep(5)
                else:
                  print('¡Alarma Apagada!')
                  sleep(5)
              except IndexError:
                y.append(0)
                print('!Alarma Encendida!')
                sleep(5)
            else:
              y.append(0)
              print('!Alarma Encendida!')
              sleep(5)
      # Si tengo menos de 2 datos no hago nada
      else:
        print('Datos Insuficientes...')
        sleep(5)
        continue
hilo_secundario_1 = Thread(target = alarma)
hilo_secundario_1.start()
hilo_secundario_1.join()
