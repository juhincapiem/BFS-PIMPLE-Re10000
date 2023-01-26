import numpy as np
import matplotlib.pyplot as plt

#-----------------------------------------------------------------------------------
#Guardo el nombre del archivo donde tengo almacenada la info de los residuales
name = 'logSimulacion'
residuals = open(name)

#Entro al archivo controlDict dentro de la carpeta system para obtener informacion acerca de la simulacion
controlDict = open("system/controlDict")


#-----------------------------------------------------------------------------------
#Dentro de la carpeta controDict tomo el tiempo total y el delta de tiempo
line = controlDict.readlines()        #Divido el archivo en lineas
words = line[24].split()              #Escojo la linea donde está el tiempo y la divido por espacios
T = float(words[1].split(';')[0])     #Guardo el tiempo final

words = line[26].split()              #Escojo la linea donde está el tiempo y la divido por espacios
dt = float(words[1].split(';')[0])    #Guardo el delta de tiempo

points = int(T/dt)
time = np.zeros(points)               #Inicializo el vector tiempo

#-----------------------------------------------------------------------------------
#Guardo los pasos de tiempo en el vector time
k = -1
for line in residuals:
    line = line.rstrip()              #Quito el newline al final de la linea
    separation = line.split()         #Guarda cada palabra en un vector

    if not 'Time' in separation:
        continue
    elif ':' in separation:
        continue
    else:
        k += 1
        target = separation[2]
        time[k] = float(target)
        
residuals.close()


#-----------------------------------------------------------------------------------
residuals = open(name)

num_iterations = 3
Res_Ux = np.zeros(points)
Res_Uy = np.zeros(points)
Res_Uz = np.zeros(points)

LINE = residuals.readlines()

count = -1
k = -1 
for i in LINE:
    count += 1
    if not i.startswith('PIMPLE:'):
        continue
    elif '{}'.format(num_iterations) != i.split()[2]:
        continue
    else:
        k += 1
        #Para almacenar los residuales de Ux
        phrase = LINE[count+1]
        words = phrase.split()
        target = words[11]
        number = target.split(',')
        Res_Ux[k] = float(number[0])

        #Para almacenar los residuales de Uy
        phrase = LINE[count+2]
        words = phrase.split()
        target = words[11]
        number = target.split(',')
        Res_Uy[k] = float(number[0])

        #Para almacenar los residuales de Uz
        phrase = LINE[count+3]
        words = phrase.split()
        target = words[11]
        number = target.split(',')
        Res_Uz[k] = float(number[0])

residuals.close()

#-----------------------------------------------------------------------------------
#Busco el numero de Courant maximo 
residuals = open(name)

Courant = np.zeros(points+1)

LINE = residuals.readlines()

count = -1
k = -1 
for i in LINE:
    count += 1
    if not i.startswith('Courant'):
        continue
    else:
        k += 1
        #Para almacenar el numero de Courant maximo
        phrase = LINE[count]
        words = phrase.split()
        target = words[5]
        Courant[k] = float(target)

#Antes de que empezara las iteraciones en Openfoam, habia un mensaje con el numero de Courant inicial. Lo elimino
courant = np.zeros(points)
courant = Courant[1:]

#-----------------------------------------------------------------------------------
#Vamos a graficar las componentes de la velocidad y el numero de Courant
fig, axs = plt.subplots(2, 2)
axs[0, 0].plot(time[50:], Res_Ux[50:],)
axs[0, 0].set_title('Residual of Ux from %.3f to %.1f seconds' %(time[50], time[-1]))
axs[0, 0].set_ylabel('Ux [m/s]')

axs[0, 1].plot(time[50:], Res_Uy[50:], 'tab:orange')
axs[0, 1].set_title('Residual of Uy from %.3f to %.1f seconds' %(time[50], time[-1]))
axs[0, 1].set_ylabel('Uy [m/s]')

axs[1, 0].plot(time[50:], Res_Uz[50:], 'tab:green')
axs[1, 0].set_title('Residual of Uz from %.3f to %.1f seconds' %(time[50], time[-1]))
axs[1, 0].set_xlabel('time [s]')
axs[1, 0].set_ylabel('Uz [m/s]')

axs[1, 1].plot(time[50:], courant[50:], 'tab:red')
axs[1, 1].set_title('Max Courant number, from %.3f to %.1f seconds' %(time[50], time[-1]))
axs[1, 1].set_xlabel('time [s]')
axs[1, 1].set_ylabel('max Courant')

for ax in axs.flat:
    ax.grid()
    

plt.show()
