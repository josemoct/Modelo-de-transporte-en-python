#Importamos dos librerías principales: Tkinter y Docplex
from tkinter import *
from docplex.mp.model import Model
from tkinter import simpledialog
from tkinter import messagebox


#Creación de la raiz
raiz = Tk()
#Configuraciones principales de la raiz
raiz.title("Modelo de transporte")
raiz.iconbitmap("imagen.ico") 
raiz.resizable(False, False) 


#---------------Creación variables -----------------------------
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

miLabel = Label(miFrame, text="Solución para modelos de transporte", bg="#F6F5D5", font=("Verdana",18))
miLabel.place(x=30,y=10)

miLabel2 = Label(miFrame, text="Ingrese la cantidad de fuentes:", bg="#F6F5D5", font=("Verdana",12))
miLabel2.place(x=30,y=60)

miLabel3 = Label(miFrame, text="Ingrese la cantidad de destinos:", bg="#F6F5D5", font=("Verdana",12))
miLabel3.place(x=30,y=130)

miLabel3 = Label(miFrame, text="Solución del problema:", bg="#F6F5D5", font=("Verdana",10))
miLabel3.place(x=30,y=190)

#--------------Creación de los cuadros de texto en la ventana ---------------


fuentesEntry = Entry(miFrame, textvariable=fuentesTxt, font=("Verdana",12))
fuentesEntry.place(x=310,y=60)

destinosEntry = Entry(miFrame, textvariable=destinosTxt, font=("Verdana",12))
destinosEntry.place(x=310,y=130)

cuadroTexto = Text(miFrame, width=48, height=9)
cuadroTexto.place(x=30, y=220)

#--------------Creación de los metodos necesarios-------------------------

#Uso de la librería Cplex
def modeloCplex():
	#Creacion del modelo 
	mdl = Model('transp')
	x = mdl.integer_var_dict(arcos, name='x')
	#Creación de la función objetivo
	mdl.minimize(mdl.sum(x[i]*costos[i] for i in arcos))
	#Agregando las restricciones
	#Restriccion de la capacidad
	for k in fuentes:
		mdl.add_constraint(mdl.sum(x[(k,j)] for j in destinos) <= ofertas[k])
	#Restriccion de la oferta
	for k in destinos:
		mdl.add_constraint(mdl.sum(x[(i,k)] for i in fuentes) <= demandas[k])
	#Imprimiendo el modelo conseguido
	modelo = mdl.export_to_string()
	cuadroTexto.insert(INSERT, "TRANSPOLANDO A PROBLEMA DE MINIMIZACIÓN \n \n")
	cuadroTexto.insert(INSERT, modelo)
	cuadroTexto.insert(INSERT, "\n")

	
	#-----------------Solucíón por medio de Cplex ---------------------------
	cuadroTexto.insert(INSERT, "SOLUCIÓN OPTIMA PARA CADA VARIABLE DE DESICIÓN \n \n")

	solucion = mdl.solve(log_output=True)
	print("Estatus de la solucion: ",mdl.get_solve_status())
	cuadroTexto.insert(INSERT, solucion)
#Función que obtiene toda la inforamción necesaria para usar luego con Cplex
def pedirCostos():
	#Inicialización de variables globales
	global numFuentes
	global numDestinos
	global fuentes
	global destinos
	global arcos
	global costos
	global demandas
	global ofertas
	#Iniciialización de variables locales
	cont = 0
	#Cantidad de fuentes y destinos 
	numFuentes = int(fuentesTxt.get())
	numDestinos = int(destinosTxt.get())
	
	numPosibilidades = numFuentes*numDestinos
	#Inicialización de las listas con las fuentes y destinos
	fuentes = [k for k in range(numFuentes)]
	destinos = [k for k in range(numDestinos)]
	#Creacion de los arcos 
	arcos = [(i,j) for i in fuentes for j in destinos]
	#Inicialización decostos de oferta, demanda y el costo cada variable de decisión
	ofertas = {}
	demandas = {}
	costos = {}
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
	for i in arcos:
		costoTxt = simpledialog.askstring(title="Costos", prompt=('Ingrese el costo de la fuente ',i[0]+1,'al destino ',i[1]+1))
		costo = round(float(costoTxt),3)
		costos[i] = costo
	
	prueba()
	modeloCplex()

#Función de prueba del programa
def prueba():
	print("El numero de fuentes es: ", numFuentes)
	print("El numero de destinos es: ", numDestinos)
	print("La tupla de fuentes es: ", fuentes)
	print("La tupla de destinos es: ", destinos)
	print("La tupla de arcos es: ", arcos)
	print("El diccionario de oferta es: ", ofertas)
	print("El diccionario de demanda es: ", demandas)
	print("El diccionario de costos es: ", costos)

#--------------Creación de los botones en la ventana-------------------------

boton = Button(miFrame, text="Aceptar", command=pedirCostos,font=("Verdana",12) )
boton.place(x=450, y=240)
raiz.mainloop()