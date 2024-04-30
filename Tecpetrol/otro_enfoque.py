from threading import Thread
from time import sleep

def alarma():
    # Intervalo entre 2 muestras
    dt = 1

    # x es un coeficiente que expresa la comparación entre la derivada de la 
    # Temperatura del Proceso contra la derivada de la Temperatura del Ambiente
    x  = 0.1

    # Arrays para almacenar los valores que envían los Sushi Sensor
    # Se van a calcular las pendientes en cada punto asi que se requiere de un
    # array
    tempp = []
    tempa = []

    # El array "sum" será utilizado para comparar la derivada de la Temperatura
    # Ambiente contra la derivada de la Temperatura del Proceso.
    # Se van a comparar de a 5 muestras asi que se requiere de un array
    sum   = []

    # Esta variable será enviada para reportar si el proceso está inactivo
    # Valores: 0/1
    alarma              = 0

    while(1):
        # Lógica para recibir datos del CI Server
        # ---------------------
        # ---------------------
        # Estas variables se van a modificar por el dato que manda el Sushi Sensor
        dato_sushi_proceso  = 0
        dato_sushi_ambiente = 0
        # ---------------------
        # ---------------------
        tempp.append(dato_sushi_proceso)
        tempa.append(dato_sushi_ambiente)

        if len(tempp) > 1:
            mp = (tempp[len(tempp) - 1] - tempp[len(tempp) - 2])/dt
            ma = (tempa[len(tempa) - 1] - tempa[len(tempa) - 2])/dt
            sum.append('on') if abs(ma) < x*abs(mp) else sum.append('off')
            if len(sum) > 4:
                if not 'on' in sum[len(sum) - 5:len(sum)]:
                    alarma = 1
                    # Transmición Sushi Sensor minutos + 5 minutos = 35 minutos = 35*(60 segundos)
                    # GAP de 5 minutos para prevenir retardos
                    # Suponiendo que el Sushi Sensor transmite datos cada 30 minutos
                    sleep(35.0*60.0)
                else:
                    if mp > 0:
                        alarma = 0
                        sleep(35.0*60.0)
                    elif mp == 0:
                        try:
                            alarma = alarma
                            sleep(35.0*60.0)
                        except IndexError:
                            alarma = 1
                            sleep(35.0*60.0)
                    else:
                        alarma = 1
                        sleep(35.0*60.0)
            else:
                if mp > 0:
                    alarma = 0
                    sleep(35.0*60.0)
                elif mp == 0:
                    try:
                        alarma = alarma
                        sleep(35.0*60.0)
                    except IndexError:
                        alarma = 1
                        sleep(35.0*60.0)
                else:
                    alarma = 1
                    sleep(35.0*60.0)
        else:
            sleep(35.0*60.0)
            continue
# Crear un hilo secundario que ejecute la función "alarma"
hilo_secundario_1 = Thread(target = alarma)

# Encolar el hilo secundario en el sistema operativo
hilo_secundario_1.start()

# Obligar al hilo principal, "Ci_Server.py" en este caso, a que espere que termine de ejectuarse el hilo secundario 1
# para poder continuar con el resto del código. En este caso, el hilo secundario nunca termina
hilo_secundario_1.join()
