#Importamos dos librerías principales: Tkinter y Pulp
from tkinter import *
import pulp	
from tkinter import simpledialog
from tkinter import messagebox


#Creación de la raiz
raiz = Tk()
#Configuraciones principales de la raiz
#Configuracion del titulo de la ventana
raiz.title("Modelo de transporte")
#Configuracion del ícono de la ventana
raiz.iconbitmap("imagen.ico") 
#Evita que se cambie el tamaño de la ventana
raiz.resizable(False, False) 


#---------------Creación variables -----------------------------
#Variables que guarda el texto de las fuentes y destinos
fuentesTxt = StringVar()
destinosTxt = StringVar()


#---------------Creación de la ventana -----------------------------

#Creación del Frame
miFrame = Frame()
#Configuraciones principales del Frame
miFrame.pack()
miFrame.config(bg="#F6F5D5")
miFrame.config(width="600",height="390")
#miFrame.config(cursor="target")

#--------------Creación de los Labels de la ventana ---------------

#Label del titulo
miLabel = Label(miFrame, text="Solución para modelos de transporte", bg="#F6F5D5", font=("Verdana",18))
miLabel.place(x=65,y=10)
#Label de la cantidad de fuentes
miLabel2 = Label(miFrame, text="Ingrese la cantidad de fuentes:", bg="#F6F5D5", font=("Verdana",12))
miLabel2.place(x=30,y=60)
#Label de la cantidad de destinos
miLabel3 = Label(miFrame, text="Ingrese la cantidad de destinos:", bg="#F6F5D5", font=("Verdana",12))
miLabel3.place(x=30,y=130)
#Label donde se refiere a la solución del problema
miLabel3 = Label(miFrame, text="Solución del problema:", bg="#F6F5D5", font=("Verdana",11))
miLabel3.place(x=30,y=190)

#--------------Creación de los cuadros de texto en la ventana ---------------

#Entrada del número de fuentes
fuentesEntry = Entry(miFrame, textvariable=fuentesTxt, font=("Verdana",12))
fuentesEntry.place(x=310,y=60)
#Entrada del número de destinos
destinosEntry = Entry(miFrame, textvariable=destinosTxt, font=("Verdana",12))
destinosEntry.place(x=310,y=130)
#Salida de la solución
cuadroTexto = Text(miFrame, width=48, height=9)
cuadroTexto.place(x=30, y=220)

#--------------Creación de los metodos necesarios-------------------------

#Uso de la librería Cplex
def modeloPulp():
	global costos
	#Creamos el problema de transporte utilizando la variable prob
	prob = pulp.LpProblem("Problema_de_distribución", pulp.LpMinimize)
	# Convertimos los costos en un diccionario de PuLP
	costos = pulp.makeDict([ofertas, demandas], costos,0)
	# Creamos una lista de tuplas que contiene todas las posibles rutas de tranporte.
	rutas = [(c,b) for c in ofertas for b in demandas]
	# creamos diccionario x que contendrá la candidad enviada en las rutas
	x = pulp.LpVariable.dicts("Ruta", (ofertas, demandas), lowBound = 0, cat = pulp.LpInteger)
	# Agregamos la función objetivo al problema
	prob += sum([x[c][b]*costos[c][b] for (c,b) in rutas]), \
	"Suma_de_costos_de_transporte"
    # Agregamos la restricción de máxima oferta de cada cervecería al problema.

	for c in ofertas:
	    prob += sum([x[c][b] for b in demandas]) <= ofertas[c], \
	            "Suma_de_Productos_que_salen_de_fuentes_%s"%c

	# Agregamos la restricción de demanda mínima de cada bar
	for b in demandas:
	    prob += sum([x[c][b] for c in ofertas]) >= demandas[b], \
	    "Suma_deProductos_que_entran_en_destinos%s"%b
   	# Resolviendo el problema.
	prob.solve()
	
	cuadroTexto.insert(INSERT, "Valoración del resultado: \n\n")
	cuadroTexto.insert(INSERT, "Estado: {}".format(pulp.LpStatus[prob.status])+"\n\n")
	cuadroTexto.insert(INSERT, "Mejor solución encontrada para cada variable de decisión: \n\n")
	# Imprimimos cada variable con su solución óptima.
	for v in prob.variables():
		cuadroTexto.insert(INSERT,"{0:} = {1:}".format(v.name, v.varValue)+"\n")
	# Imprimimos el valor óptimo de la función objetivo
	cuadroTexto.insert(INSERT, "\nCosto total de transporte: \n \n")
	cuadroTexto.insert(INSERT, "Costo = {}".format(prob.objective.value()))
	

#Función que obtiene toda la inforamción necesaria para usar luego con Cplex
def pedirCostos():
	#Inicialización de variables globales
	global numFuentes
	global numDestinos
	global fuentes
	global destinos
	global costos
	global demandas
	global ofertas
	#Cantidad de fuentes y destinos 
	numFuentes = int(fuentesTxt.get())
	numDestinos = int(destinosTxt.get())
	
	numPosibilidades = numFuentes*numDestinos
	#Inicialización de las listas con las fuentes y destinos
	fuentes = [k for k in range(numFuentes)]
	destinos = [k for k in range(numDestinos)]
	#Inicialización decostos de oferta, demanda y el costo cada variable de decisión
	ofertas = {}
	demandas = {}
	costos = []
	ROOT = Tk()
	ROOT.withdraw()
	#Obteniedno la capacidad de cada fuente
	for i in range(numFuentes):
		ofertaTxt = simpledialog.askstring(title="Oferta", prompt=('Ingrese la capacidad de la fuente: ',i+1)) 
		oferta = int(ofertaTxt)
		ofertas[i] = oferta
	#Obteniedno la demanda de cada destino
	for i in range(numDestinos):
		demandaTxt = simpledialog.askstring(title="Demanda", prompt=('Ingrese demanda del destino: ',i+1)) 
		demanda = int(demandaTxt)
		demandas[i] = demanda
	#Obteniedno el costo para cada variable de desición 
	for i in range(numFuentes):
		costos.append([])
		for j in range(numDestinos):
			costoTxt = simpledialog.askstring(title="Costos", prompt=('Ingrese el costo de la fuente ',i+1,'al destino ',j+1))
			costo = round(float(costoTxt),3)
			costos[i].append(costo)
	
	prueba()
	modeloPulp()

#Función para reiniciar valores
def reiniciar():
	#Varias globales que guardan el numero de fuentes, destinos y matrices necesarias en todo el programa
	global numFuentes
	global numDestinos
	global fuentes
	global destinos
	global costos
	global demandas
	global ofertas
	#Inicialización de las variables principales en cero (0)
	numFuentes = 0
	numDestinos = 0
	fuentes = 0
	destinos = 0
	costos = 0
	demandas = 0
	ofertas = 0
	cuadroTexto.delete("1.0","end")
	fuentesEntry.delete("0","end")
	destinosEntry.delete("0","end")

#Función de prueba del programa
def prueba():
	print("El numero de fuentes es: ", numFuentes)
	print("El numero de destinos es: ", numDestinos)
	print("La tupla de fuentes es: ", fuentes)
	print("La tupla de destinos es: ", destinos)
	print("El diccionario de oferta es: ", ofertas)
	print("El diccionario de demanda es: ", demandas)
	print("El diccionario de costos es: ", costos)

#--------------Creación de los botones en la ventana-------------------------

#Boton para arrancar a correr el programa una vez inicializadas las variables
boton = Button(miFrame, text="Aceptar", command=pedirCostos,font=("Verdana",12) )
boton.place(x=450, y=240)
#Boton para reiniciar y realizar un nuevo ejercicio
boton2 = Button(miFrame, text="Resetear", command=reiniciar,font=("Verdana",12) )
boton2.place(x=450, y=280)


raiz.mainloop()
