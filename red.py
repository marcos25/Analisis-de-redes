import copy
import operator
import math
from typing import MappingView
from digrafica import *
from estructuras_datos import *
import sys
sys.setrecursionlimit(5000)

class Arco:
    """
        Esta clase representa un arco. Tiene nodos de origen y destino, además de una 
        capacidad mínima, un flujo y una capacidad.
    """
    def __init__(self, origen, destino, res_min=0, flujo=0, capacidad=0, costo=0, Id=None):
        self.origen = origen
        self.destino = destino
        self.res_min = res_min
        self.flujo = flujo
        self.capacidad = capacidad
        self.costo = costo
        self.Id = Id 
#----------------------------------------------------------------

class Nodo:
    """
        Esta clase representa un nodo. Tiene un nombre, restricción mínima y máxima, etiqueta y 
        grados positivo y negativo.
    """
    def __init__(self, nombre, res_min=0, res_max=math.inf, oferta_demanda=0, Id=None):
        self.nombre = nombre
        self.res_min=res_min
        self.res_max=res_max
        self.etiqueta = None
        self.grado_positivo = 0
        self.grado_negativo = 0
        self.oferta_demanda=oferta_demanda
        self.Id = Id

#----------------------------------------------------------------
class Red:
    """
        Esta clase representa una red de transporte y sus operaciones.
    """
    def __init__(self):
        self.__red = {} # Estructura donde se va a guardar la gráfica
        self.__num_nodos = 0 # Contador de nodos
        self.__num_arcos = 0 # Contador de arcos

    def buscar_nodo(self, nombre):
        """
            Este método busca un nodo en la gráfica.
            Parametros:
            ----------
            nodo: Nodo a buscar
            Regresa:
            -------
            True si el nodo se encuentra en la digráfica.
            None si el nodo no se encuentra en la digráfica. 
        """
        for nodo in self.__red:
            if nodo.nombre == nombre:
                return nodo
        return False 
    
    def agregar_nodo(self, nombre, res_min=0, res_max=math.inf, oferta_demanda=0):
        """
            Este método agrega un nodo a la digráfica.
            Parámetros
            ----------
            nodo: Nodo que se desea agregar
            Regresa
            -------
            False: Si el nodo a agregar ya existe
            True: Si el nodo a agregar no existía en la digráfica.
        """
        # Se busca el nodo en la gráfica, si ya existe, se regresa False
        nodo = self.buscar_nodo(nombre)
        if not nodo:
        
            # Si el nuevo nodo no existe, entonces se crea y se le añade un diccionario
            # con dos listas vacías, la lista de nodos "entrantes" y la lista de nodos "salientes"
            nodo = Nodo(nombre, float(res_min), float(res_max), float(oferta_demanda))
            self.__red[nodo] = {"entrantes":[], "salientes":[]}

            # El número de nodos en la digráfica se incrementa y se regresa True
            self.__num_nodos += 1
        return nodo
    
    def agregar_arco(self, a, b, res_min=0, flujo=0, capacidad=0,costo=0, Id=None):
        """
            Este método agrega un arco a la digráfica
            Parámetros
            ----------
            a: Nodo de origen.
            b: Nodo destino.
            res_min: restricción mínima del arco.
            flujo: Flujo del arco
            capacidad: Capacidad del arco
        """
        # Se agregan los nodos a y b (Esto porque le damos la opción al usuario de 
        # agregar arcos directamente sin la necesidad de que los nodos ya existan
        # en la digráfica)
        nodo_a = self.agregar_nodo(a)
        nodo_b = self.agregar_nodo(b)

        # Se construye el arco (a,b)
        arco = Arco(nodo_a, nodo_b, float(res_min), float(flujo), float(capacidad),float(costo), Id)

        # Se agrega el arco (a,b) a los salientes de a, y el grado positivo de a 
        # se incrementa en 1
        self.__red[nodo_a]["salientes"].append(arco)
        nodo_a.grado_positivo += 1

        # Se agrega el arco (a,b) a los entrantes de b, y el grado negativo de b 
        # se incrementa en 1
        self.__red[nodo_b]["entrantes"].append(arco)
        nodo_b.grado_negativo += 1

        # El contador de arcos se incrementa
        self.__num_arcos += 1
        
        return True
    
    def leer_red(self, archivo):
        """
            Este método lee una digráfica desde un archivo
            Parámetros
            ----------
            archivo: Ruta del archivo de texto en donde se encuentra la información
                     de la digráfica de la siguiente manera y separado con Enters:
                     a -> Para agregar el nodo a
                     a,b -> Para agregar el arco (a,b)
                     a,b,5 -> Para agregar el arco (a,b) con peso 5
        """
        file1 = open(archivo, 'r') 
        Lines = file1.readlines() 

        for line in Lines:
            line = line.strip().split(",")
            length = len(line)
            if length == 1:
                self.agregar_nodo(line[0])
            elif length == 2:
                self.agregar_arco(line[0], line[1])
            elif length == 3:
                self.agregar_nodo(line[0], float(line[1]), float(line[2]))
            elif length == 4:
                self.agregar_nodo(line[0], float(line[1]), float(line[2]), float(line[3]))
            elif length == 5:
                self.agregar_arco(line[0], line[1], float(line[2]), float(line[3]), float(line[4]))
            elif length == 6:
                self.agregar_arco(line[0], line[1], float(line[2]), float(line[3]), float(line[4]),float(line[5]))

    def buscar_arco(self, a, b, res_min=0, flujo=0, capacidad=0):
        """
            Este método busca un arco entre dos nodos
            Parámetros
            ----------
            a: Nodo de origen del arco a buscar.
            b: Nodo destino del arco a buscar.
            peso (None por default): Peso del arco a buscar 
            Regresa
            -------
            arco: Si existe, regresa el objeto de la clase Arco que tiene como origen al nodo a, 
                  como destino al nodo b y con peso = peso (en caso de que se haya proporcionado 
                  un peso).
            False: Si el arco no existe.
        """
        # Se busca el nodo de origen
        nodo_a = self.buscar_nodo(a)

        # Si el nodo de origen no existe, la arista buscada tampoco. Se regresa False
        if not nodo_a:
            return False
        
        for arco in self.__red[nodo_a]['salientes']:
            if arco.destino.nombre == b and arco.res_min == res_min and arco.flujo == flujo and arco.capacidad == capacidad:
                return arco
        
        # Si se recorrieron todos los salientes del nodo de origen y no se encontró
        # el arco buscado, entonces se regresa False
        return False
    
    def eliminar_arco(self, a=None, b=None, res_min=0, flujo=0, capacidad=0, obj_arco=None):
        """
            Este método elimina un arco de la digráfica
            Parámetros
            ----------
            a: Nodo de origen del arco
            b: Nodo destino del arco
            peso (None por default): peso del arco
            Regresa
            -------
            True: Si el arco pudo eliminarse (si existía)
            False: Si el arco no pudo eliminarse (si no existía)
        """    

        # Se busca el arco
        if not obj_arco:
            arco = self.buscar_arco(a, b, res_min, flujo, capacidad)
        else:
            arco = obj_arco

        # Si existe el arco, entonces se procede a elminarlo
        if arco:
            # El arco se elimina de los salientes del nodo de origen y el peso positivo
            # de éste se decrementa
            nodo_origen = arco.origen
            self.__red[nodo_origen]["salientes"].remove(arco)
            nodo_origen.grado_positivo -= 1

            # El arco se elimina de los entrantes del nodo destino y el peso negativo
            # de éste se decrementa
            nodo_destino = arco.destino
            self.__red[nodo_destino]["entrantes"].remove(arco)
            nodo_destino.grado_negativo -= 1

            # Se decrementa el número de arcos de la digráfica
            self.__num_arcos -= 1

            # Se regresa True para indicar que el arco se pudo eliminar
            return True
            
        # Si el arco no existe, entonces se regresa False
        return False
    
    def eliminar_nodo(self, nombre):
        """
            Este método elimina un nodo de la digráfica
            Parámetros
            ----------
            nombre: Nombre del nodo que se quiere eliminar
            Regresa
            -------
            True: Si el nodo pudo eliminarse (Sí existía)
            False: Si el nodo no pudo eliminarse (No existía)
        """
        # Si se encuentra el nodo, entonces se procede a eliminarlo
        nodo = self.buscar_nodo(nombre)

        # Para eliminar el nodo, primero necesitamos eliminar sus salientes y entrantes
        if nodo:
            self.vaciar_nodo(nodo.nombre)

            # Cuando todos los arcos incidentes en el nodo se hayan eliminado procedemos a 
            # eliminar el nodo de la digráfica y decrementamos el contador de nodos
            self.__red.pop(nodo)
            self.__num_nodos -= 1

            return True
        else:
            return False
    
    def obtener_grado(self, nombre, tipo="positivo"):
        """
            Este método obtiene el grado positivo de un nodo de la gráfica
            Parámetros
            ----------
            nombre: Nombre del nodo al que se le va a calcular el grado
            tipo: Tipo del grado
                - "positivo" (por default) para el grado positivo
                - "negativo" para el grado negativo
            Regresa
            -------
            - El grado del nodo si éste existe en la digráfica
            - False si el nodo no solicitado no existe en la digráfica.
        """
        # Primero se busca el nodo
        nodo = self.buscar_nodo(nombre)
        # Si exist se regresa el tipo de grado especificado
        if nodo:
            return nodo.grado_negativo if tipo == "negativo" else nodo.grado_positivo
        
        # Si el nodo no existe regresa False
        return False
    
    def obtener_numero_nodos(self):
        """
            Este método obtiene el número de nodos de la gráfica
            Regresa
            -------
            El número de nodos de la gráfica
        """
        # Simplemente regresamos el valor del contador de nodos
        return self.__num_nodos
    
    def obtener_numero_arcos(self):
        """
            Este método obtiene el número de aristas de la gráfica
            Regresa
            -------
            El número de aristas de la gráfica
        """
        # Simplemente regresamos el valor del contador de aristas
        return self.__num_arcos
    
    def vaciar_nodo(self, nombre):
        """
            Este método elimina todos los arcos incidentes de un nodo
            Parámetros
            ----------
            nombre: Nombre del nodo que vamos a vaciar
            Regresa
            -------
            - True si el nodo pudo ser vaciado (si existía en la digráfica)
            - False si el nodo no pudo ser vaciado (si no existía en la digráfica)
        """
        # Si se encuentra el nodo, entonces se procede a vaciarlo
        nodo = self.buscar_nodo(nombre)

        if nodo:
            # Se eliminan todos los arcos salientes
            while self.__red[nodo]["salientes"]:
                arco = self.__red[nodo]["salientes"][0]
                self.eliminar_arco(obj_arco=arco)
            
            # Se eliminan todos los arcos entrantes
            while self.__red[nodo]["entrantes"]:
                arco = self.__red[nodo]["entrantes"][0]
                self.eliminar_arco(obj_arco=arco)
            
            # Se regresa True
            return True
        else:
            # Si el nodo no existe se regresa False
            return False
    
    def vaciar_grafica(self):
        """
            Este método limpia la gráfica
        """
        self.__digrafica = {}
        self.__num_nodos = 0
        self.__num_arcos = 0
    

    def copiar(self):
        """
            Este método realiza una copia de la gráfica
            Regresa
            -------
            Objeto de la clase Digráfica que representa la copia del objeto actual.
        """
        return copy.deepcopy(self)
    
    def __limpiar_etiquetas(self, tipo):
        """
            Este método limpia las etiquetas de los nodos y/o aristas de la gráfica
            Parámetros
            ----------
            tipo: Tipo del objeto del que deseamos eliminar las etiquetas
                - "nodos": Para limpiar las etiquetas de los nodos
                - "arcos": Para limpiar las etiquetas de los arcos
                - "todo": Para limpiar las etiquetas de todos los arcos y aristas
        """
        if tipo == "nodos":
            for nodo in self.__red:
                nodo.etiqueta = None
        elif tipo == "aristas":
            for nodo in self.__red:
                for arco in self.__red[nodo]["entrantes"]:
                    arco.etiqueta = None
                for arco in self.__digrafica[nodo]["salientes"]:
                    arco.etiqueta = None
        elif tipo == "todo":
            for nodo in self.__red:
                for arco in self.__red[nodo]["entrantes"]:
                    arco.etiqueta = None
                for arco in self.__red[nodo]["salientes"]:
                    arco.etiqueta = None
        else:
            raise ValueError(f"Error en el tipo dado ({tipo}). Valores aceptados: 'nodos', 'aristas', 'todos'")

    def imprimir_arcos(self): 
        for nodo in self.__red:
            for arco in self.__red[nodo]["salientes"]:
                print("(",arco.origen.nombre,', ',arco.destino.nombre,', ',arco.res_min,', ',arco.flujo,', ',arco.capacidad,", ",arco.costo,')')

    def fulkerson(self,fuente,sumidero,limite_flujo,sumideros):
            arcos_visitados = []
            cadena = []
           
            # buscamos cadenas aumentantes con busqueda a lo profundo
            self.dfs(fuente,fuente,sumidero,cadena,arcos_visitados)
            bool = False
            # ciclo donde actualizaremos el flujo de las cadenas aumentantes, mientras existan estas cadenas
            while True:
                flujo_cadena = math.inf

                # calculamos el flujo con el que actualizarmos el flujo de la cadena aumentante
                for arco in cadena:       
                    if(arco.etiqueta == "sentidoPropio"):
                         # caso donde el arco va en sentido propio
                        if((arco.capacidad - arco.flujo) < flujo_cadena):
                            flujo_cadena = arco.capacidad - arco.flujo
                    else:
                        # caso donde el arco va en sentido impropio
                        if(arco.etiqueta == "sentidoImpropio"):
                            if(arco.flujo - arco.res_min < flujo_cadena):
                                flujo_cadena = arco.flujo - arco.res_min

                if (sumidero.nombre != "sumideroFicticio"):
                    flujo_actual = 0
                    for nodo in sumideros:
                        for arco in self.__red[self.buscar_nodo(nodo)]["entrantes"]:
                            flujo_actual += arco.flujo
                            
                        for arco in self.__red[self.buscar_nodo(nodo)]["salientes"]:
                            if(arco.destino.nombre != "Z-"):
                                flujo_actual -= arco.flujo
                           
                    if(limite_flujo): 
                        if(flujo_cadena+flujo_actual > limite_flujo):
                            bool = True
                            flujo_cadena =   flujo_cadena - ((flujo_cadena+flujo_actual) - limite_flujo )
                    
                # actualizamos el flujo de los arcos de la cadena aumentante
                for arco in cadena:
                    # caso donde el arco va en sentido propio, sumamos flujo
                    if(arco.etiqueta == "sentidoPropio"):
                        arco.flujo += flujo_cadena

                    # caso donde el arco va en sentido impropio, restamos flujo
                    if(arco.etiqueta == "sentidoImpropio"):
                        arco.flujo -= flujo_cadena

                if(bool == True):
                    break

                cadena= []
                arcos_visitados = []
                # reseteamos las etiquetas de los nodos
                for nodo in self.__red:
                    nodo.etiqueta = None
                # buscamos una nueva cadena aumentante
                self.dfs(fuente,fuente,sumidero,cadena,arcos_visitados)

                # si ya no hay cadenas aumentantes, nos detenemos
                if not cadena:
                    break

    def flujo_maximo(self,fuentes,sumideros,limite_flujo = None,Dual = None):
        
        # revisaremos cuantos nodos fuentes y sumideros hay 
        # si hay mas de un sumireo o mas de un nodo fuente, crearemos un super fuente o un super sumidero
        if len(fuentes) > 1:
            self.agregar_nodo('A+')
            fuente = self.buscar_nodo('A+')
            for nodo in fuentes:
                self.agregar_arco(fuente.nombre, nodo,0,0,math.inf)

        if len(sumideros) > 1:
            self.agregar_nodo('Z-')
            sumidero = self.buscar_nodo('Z-')
            for nodo in sumideros:
                self.agregar_arco(nodo, sumidero.nombre,0,0,math.inf)

        # si solo hay un sumidero o un solo fuente, los definimos
        if(len(fuentes)==1 ):
            fuente = self.buscar_nodo(fuentes[0])
        if(len(sumideros)==1 ):
            sumidero = self.buscar_nodo(sumideros[0])

        # revisaremos el caso donde hay restricciones en uno o mas nodos
        nodos_ficticios = []
        lista_nodos = []
        # lista con los nodos originales de la lista
        for nodo in self.__red:
            lista_nodos.append(nodo)
        
      
        # iteramos los nodos para revisar si tienen restricciones
        for nodo in lista_nodos:
            if nodo.res_min > 0 or nodo.res_max != math.inf:
                # si el nodo tiene restricción, agregamos un nodo ficticio
                self.agregar_nodo(nodo.nombre+ '"')
                # metemos el nodo ficticio creado en una lista
                nodos_ficticios.append(nodo)

                # creamos una lista de los arcos salientes del nodo que tiene restricciones
                lista_arcos = []
                for arco in self.__red[nodo]["salientes"]:
                    lista_arcos.append(arco)

                # creamos un arco ficticio entre el nodo con restricciones y en nuevo nodo ficticio creado
                self.agregar_arco(nodo.nombre, nodo.nombre+ '"',nodo.res_min,0,nodo.res_max)

                for arco in lista_arcos:   
                    # los arcos salientes del nodo con restricciones ahora serán los arcos salientes del nuevo nodo ficticio           
                    self.agregar_arco(nodo.nombre+ '"', arco.destino.nombre,arco.res_min,arco.flujo,arco.capacidad,arco.costo)
                    # eliminamos momentaneamente los arcos salientes del nodo que tiene restricciones
                    self.eliminar_arco(nodo.nombre,arco.destino.nombre,arco.res_min,arco.flujo,arco.capacidad)

        # revisamos los arcos que tienen restriccion y los metemos a una lista
        arcos_con_restriccion = []            
        for nodo in self.__red:
            for arco in self.__red[nodo]["salientes"]:
                if(arco.res_min > 0):
                    arcos_con_restriccion.append(arco)

        # caso donde existen arcos con restriccion
        if(len(arcos_con_restriccion)> 0):
            
            # lista donde guardaremos las restricciones de los arcos con restriccion minima
            restricciones_minimas = []
           
            # para cada arco con restriccion, creamos un arco ficticio desde el origen de ese arco hacia un sumidero ficticio
            # tambien creamos un arco ficticio desde un fuente ficticio hacia el nodo destino del arco con restricción
            for arco in arcos_con_restriccion:
                restricciones_minimas.append(arco.res_min)
                # creamos los arcos ficticios para los arcos que tiene restricción
                self.agregar_arco(arco.origen.nombre, "SumideroFicticio",0,0,arco.res_min)
                self.agregar_arco("FuenteFicticio", arco.destino.nombre,0,0,arco.res_min)

                # actualizamos la capacidad y restricción minima del arco provisionalmente, para que todo los arcos tengan restricción minima de 0
                arco.capacidad = arco.capacidad - arco.res_min
                arco.res_min = 0
            
            # agreamos dos arcos ficticiones que conecten al nodo fuente y al nodo sumidero con capacidad infinita
            self.agregar_arco(fuente.nombre, sumidero.nombre,0,0,math.inf)
            self.agregar_arco(sumidero.nombre, fuente.nombre,0,0,math.inf)

            # guardamos los arcos ficticios en una lista para eliminarlos después
            arcos_fuente_sumidero = []
            arcos_fuente_sumidero.append(self.buscar_arco(fuente.nombre, sumidero.nombre,0,0,math.inf))
            arcos_fuente_sumidero.append(self.buscar_arco(sumidero.nombre, fuente.nombre,0,0,math.inf))
            
            # buscamos los nodos fuete y sumidero ficticios creados para el caso donde hay arcos con restricciones
            fuenteFicticio = self.buscar_nodo("FuenteFicticio")
            sumideroFicticio = self.buscar_nodo("SumideroFicticio")
            
            # aplicamos ford fulkerson a la red, con los nodos fuente y sumidero ficticios
            self.fulkerson(fuenteFicticio,sumideroFicticio,limite_flujo,sumideros)
            

            
            # regresamos a la normalidad los arcos que tenian reestriccion minima
            arcos_sumideroFicticio = []
            for arco in self.__red[sumideroFicticio]['entrantes']:
                arcos_sumideroFicticio.append(arco)
            for arco in arcos_con_restriccion:
                res_min = restricciones_minimas.pop(0)
                # recuperamos la restriccion y capacidad originales de los arcos
                arco.res_min = res_min
                arco.flujo += arcos_sumideroFicticio.pop(0).flujo
                arco.capacidad = arco.capacidad + res_min
            # eliminamos los nodos ficticios creados para el caso donde hay arcos con reestriccion minima
            self.eliminar_nodo(fuenteFicticio.nombre)
            self.eliminar_nodo(sumideroFicticio.nombre)
          

           
            for arco in arcos_fuente_sumidero:
                self.eliminar_arco(arco.origen.nombre,arco.destino.nombre,arco.res_min,arco.flujo,arco.capacidad)
            
      
        if(limite_flujo or Dual):
           
            flujo_actual = 0
            for nodo in sumideros:
                for arco in self.__red[self.buscar_nodo(nodo)]["entrantes"]:
                    flujo_actual += arco.flujo
                    
                for arco in self.__red[self.buscar_nodo(nodo)]["salientes"]:
                    if(arco.destino.nombre != "Z-"):
                        flujo_actual -= arco.flujo
            if(Dual):
               
                # regresamos los nodos con reestriccion particionados a la normalidad
                for nodo in nodos_ficticios:
                    nodo_ficticio = self.buscar_nodo(nodo.nombre+ '"')
                    lista_arcos_ficticios = []
                    for arco in self.__red[nodo_ficticio]["salientes"]:
                        lista_arcos_ficticios.append(arco)
                    
                    for arco in lista_arcos_ficticios:
                        self.agregar_arco(nodo.nombre, arco.destino.nombre,arco.res_min,arco.flujo,arco.capacidad,arco.costo)
                    self.eliminar_nodo(nodo.nombre+ '"')
                costo = 0
                for nodo in self.__red:
                    for arco in self.__red[nodo]["salientes"]:
                        costo += arco.flujo * arco.costo
              
                return flujo_actual
            if(limite_flujo):
                
                if(flujo_actual > limite_flujo and limite_flujo):
                    
                    if(len(fuentes)>1):
                       
                        self.eliminar_nodo('A+')
                    if(len(sumideros)>1):
                        self.eliminar_nodo('Z-')
                    
                    return None
        # aplicamos for fulkerson a la red
        self.fulkerson(fuente,sumidero,limite_flujo,sumideros)
       

        # regresamos los nodos con reestriccion particionados a la normalidad
        for nodo in nodos_ficticios:
            nodo_ficticio = self.buscar_nodo(nodo.nombre+ '"')
            lista_arcos_ficticios = []
            for arco in self.__red[nodo_ficticio]["salientes"]:
                lista_arcos_ficticios.append(arco)
            
            for arco in lista_arcos_ficticios:
                self.agregar_arco(nodo.nombre, arco.destino.nombre,arco.res_min,arco.flujo,arco.capacidad,arco.costo)
            self.eliminar_nodo(nodo.nombre+ '"')

        # eliminamos los nodos super fuente y super sumidero en caso de que fueran requeridos
        # para el caso donde hay mas de un sumidero o mas de una fuente        
        if(len(fuentes)>1):
            self.eliminar_nodo('A+')
        if(len(sumideros)>1):
            self.eliminar_nodo('Z-')

        
        # calculamos el flujo final que reciben los sumideros
        flujo_final = 0
        for nodo in sumideros:
            for arco in self.__red[self.buscar_nodo(nodo)]["entrantes"]:
                flujo_final += arco.flujo
            for arco in self.__red[self.buscar_nodo(nodo)]["salientes"]:
                flujo_final -= arco.flujo

        return flujo_final

    def dfs(self, node,fuente, sumidero, cadena,arcos_visitados):
        bool = False
        node.etiqueta = "marcado"
        for saliente in self.__red[node]["salientes"]: 
            if(saliente.flujo < saliente.capacidad and saliente not in arcos_visitados and saliente.destino.etiqueta != "marcado"): 
      
                bool = True
                arcos_visitados.append(saliente)
                cadena.append(saliente) 
                saliente.etiqueta = "sentidoPropio"
                if(saliente.destino == sumidero):

                    return cadena
                self.dfs(saliente.destino,fuente,sumidero,cadena,arcos_visitados)
                break

        if(bool == False):
            for entrante in self.__red[node]["entrantes"]: 
                if(entrante.flujo > 0 and entrante.flujo > entrante.res_min and entrante not in arcos_visitados and entrante.origen.etiqueta != "marcado"): 
                    bool = True
                    arcos_visitados.append(entrante)
                    cadena.append(entrante) 
                    entrante.etiqueta = "sentidoImpropio"
                    if(entrante.origen == sumidero):
                        return cadena
                    self.dfs(entrante.origen,fuente,sumidero,cadena,arcos_visitados)
                    break
        
        

        if(bool == False):     
            if(len(cadena)>=1):
                if(cadena[len(cadena)-1].etiqueta == "sentidoPropio"):      
                    nodo = cadena[len(cadena)-1].origen
                    cadena.pop(len(cadena)-1)
                    node.etiqueta = None
                    self.dfs(nodo,fuente,sumidero,cadena,arcos_visitados)
                    return None
                elif(cadena[len(cadena)-1].etiqueta == "sentidoImpropio"):
                    nodo = cadena[len(cadena)-1].destino
                    cadena.pop(len(cadena)-1)
                    node.etiqueta = None
                    self.dfs(nodo,fuente,sumidero,cadena,arcos_visitados)
                    return None
        
      
        
    def algoritmo_primal(self,fuentes,sumideros,limite_flujo):
        # aplicamos for fulkerson con el limite de flujo deseado
        flujo = self.flujo_maximo(fuentes,sumideros,limite_flujo)
        
        
        if(flujo):
            # regresamos falso si no se satisface el flujo deseado
            if flujo < limite_flujo:
                return None

            costo = 0
            # lista de arcos de la red original
            
            # caso donde existen nodos con restricciones
            # crearemos un nodo ficticio que particione el nodo con restricciones
            nodos_con_restriccion = []
            nodos_red = []
            for nodo in self.__red:
                nodos_red.append(nodo)
            for nodo in nodos_red:
                if (nodo.res_min > 0 or nodo.res_max != math.inf):
                    nodos_con_restriccion.append(nodo)
                    self.agregar_nodo(nodo.nombre+ '"')
                    # creamos una lista de los arcos salientes del nodo que tiene restricciones
                    lista_arcos = []
                    for arco in self.__red[nodo]["salientes"]:
                        lista_arcos.append(arco)

                    # creamos un arco ficticio entre el nodo con restricciones y en nuevo nodo ficticio creado
                    self.agregar_arco(nodo.nombre, nodo.nombre+ '"',nodo.res_min,0,nodo.res_max,0)
                    arcoNuevo = self.buscar_arco(nodo.nombre, nodo.nombre+ '"',nodo.res_min,0,nodo.res_max)
                    for arco in lista_arcos:   
                        # los arcos salientes del nodo con restricciones ahora serán los arcos salientes del nuevo nodo ficticio           
                        self.agregar_arco(nodo.nombre+ '"', arco.destino.nombre,arco.res_min,arco.flujo,arco.capacidad,arco.costo)
                        # eliminamos momentaneamente los arcos salientes del nodo que tiene restricciones
                        self.eliminar_arco(nodo.nombre,arco.destino.nombre,arco.res_min,arco.flujo,arco.capacidad)
                        arcoNuevo.flujo += arco.flujo
            arcos_red_original = []
            
            #calculamos el costo inicial, en base al primer flujo factible encontrado por ford fulkerson
            for nodo in self.__red:
                for arco in self.__red[nodo]["salientes"]:
                    arcos_red_original.append(arco)
                    costo += arco.flujo * arco.costo
            print("Costo inicial: ",costo)        
         
            #Creamos la red marginal
            red_marginal = Red()
           
            # creamos la red marginal en base a los arcos de la re original
            red_marginal.crear_red_marginal(arcos_red_original)
            
            # aplicamos el algoritmo usando la red marginal
            red_marginal.eliminacion_ciclos_negativos()

            # regresamos los nodos con reestricciones a la normalidad
            for nodo in nodos_con_restriccion:
                nodo_ficticio = self.buscar_nodo(nodo.nombre+ '"')
                lista_arcos_ficticios = []
                for arco in self.__red[nodo_ficticio]["salientes"]:
                    lista_arcos_ficticios.append(arco)
                # recuperamos los arcos que tenia el nodo antes de particionarlo
                for arco in lista_arcos_ficticios:
                    self.agregar_arco(nodo.nombre, arco.destino.nombre,arco.res_min,arco.flujo,arco.capacidad,arco.costo)
                # eliminamos el nodo ficticio creado para la partición
                self.eliminar_nodo(nodo.nombre+ '"')

            #calculamos el costo final
            costo = 0
            for nodo in self.__red:
                for arco in self.__red[nodo]["salientes"]:
                    arcos_red_original.append(arco)
                    costo += arco.flujo * arco.costo
           

            return costo
        else:
            # caso donde no hay un flujo inicial factible en base al flujo deseado
            return None
             
            
    def crear_red_marginal(self, arcos_red_original):
        # creamos los arcos de la red marginal, en base a los arcos de la red original
        for arco in arcos_red_original:
            # revisamos si la capacidad del arco de la red original es mayor al flujo del arco
            # caso donde agregaremos los arcos de la red margial que van en el mismo sentido que los de la red orignal
            if(arco.capacidad > arco.flujo):
                # agregamos el arco a la red marginal
                # la capacidad en este caso será la capacidad del arco menos el flujo, y el costo será el mismo del arco orignal 
                self.agregar_arco(arco.origen.nombre,arco.destino.nombre,0,0,arco.capacidad - arco.flujo,arco.costo)
                # etiquetaremos el nuevo arco de la red marginal con el arco relacionado de la red original
                arcoNuevo = self.buscar_arco(arco.origen.nombre,arco.destino.nombre,0,0,arco.capacidad - arco.flujo)
                arcoNuevo.etiqueta = arco
            
            # revisamos si el flujo del arco de la red original es mayor a la restricción minima
            # caso donde agregaremos los arcos de la red margial que van en el mismo sentido que los de la red orignal
            if(arco.res_min < arco.flujo):
                # agregamos el arco a la red marginal
                # la capacidad en este caso será el flujo del arco menos la restricción minima y el costo será el mismo del arco orignal pero negativo
                self.agregar_arco(arco.destino.nombre,arco.origen.nombre,0,0,arco.flujo - arco.res_min,-arco.costo)
                # etiquetaremos el nuevo arco de la red marginal con el arco relacionado de la red original
                arcoNuevo = self.buscar_arco(arco.destino.nombre,arco.origen.nombre,0,0,arco.flujo - arco.res_min)
                arcoNuevo.etiqueta = arco
    
    def eliminacion_ciclos_negativos(self):
        # creamos el objeto dígrafica que usaremos para aplicar el algoritmo de rutas mas cortas (Floyd)
        # para encontrar ciclos negativos en la red marginal
        d = Digrafica()
        # creamos los arcos de la digrafica tomando los mismos arcos que hay en la red marginal 
            # tomamos el costo de los arcos de la red marginal como peso de los arcos de la digrafica
        nodos_con_restriccion = []
        for nodo in self.__red:
            for arco in self.__red[nodo]["salientes"]:
                d.agregar_arco(arco.origen.nombre,arco.destino.nombre,arco.costo)
                # etiquetamos los arcos de la digrafica con los arcos relacionados correspondientes a la red marginal
                arcoNuevo = d.buscar_arco(arco.origen.nombre,arco.destino.nombre,arco.costo)
                arcoNuevo.etiqueta = arco

    

        # hacemos las iteraciones del algoritmo mientras haya ciclos negativos en la red marginal
        while(True):
            
            # aplicamos el algoritmo de floyd para encontrar ciclos negativos
            ciclo = d.floyd("a")

            # en caso de encontrar algun ciclo negativo, seguimos con el algoritmo
            if ciclo[len(ciclo)-1][0] == 'ciclo':
                # iniciamos el delta con valor infinito
                delta = math.inf
                # variable auxiliar para saber si los objetos de la lista ciclos son arcos o no
                tipo = type(ciclo[0][0])
                # recorremos el ciclo
                for arco in ciclo:
                    # revisamos que el elemento del ciclo sea un objeto arco de de la clase digrafica            
                    if(type(arco[0]) == tipo):
                        capacidad_arco_red_marginal = arco[0].etiqueta.capacidad
                        # comparamos las capacidades de los arcos del ciclo para buscar la mas pequeña y obtener el delta
                        if(capacidad_arco_red_marginal< delta):
                            delta = capacidad_arco_red_marginal
                
                # recorremos los arcos del ciclo para actualizar el flujo de la red original 
                # los arcos del ciclo tiene como etiqueta sus arcos relacionados en la red marginal y los arcos de la red marginal
                # tienen como etiqueta los arcos relacionados en la red original
                for arco in ciclo:
                    # revisamos que el elemento sea un arco de de la clase digrafica            
                    if(type(arco[0]) == tipo):
                        # nodo orgien del arco relacionado de la red original
                        origen_arco_red_original = arco[0].etiqueta.etiqueta.origen.nombre
                        # para acceder a los arcos de la red original desde los arcos de la lista ciclo acccedemos a la etiqueta de la etiqueta
                        # si el arco del ciclo va en el mismo sentido a su arco relacionado en la red original, sumamos delta
                        if(origen_arco_red_original == arco[0].origen.nombre):
                            arco[0].etiqueta.etiqueta.flujo += delta
                            
                        else:
                             # si el arco del ciclo va en el sentido contrario a su arco relacionado en la red original, restamos delta
                            arco[0].etiqueta.etiqueta.flujo -= delta

                # ciclo para actualizar los arcos de la red marginal y eliminar los que no cumplan los requisitos
                # accederemos a los arcos de la red marginal y red orignal desde las etiquetas de los arcos del ciclo encontrado en la digrafica
                for arco in ciclo:
                    # revisamos que el elemento sea un arco de de la clase digrafica            
                    if(type(arco[0]) == tipo):
                        # definimos las variables donde guardaremos los elementos de los arcos de las redes con respecto a las etiquetas de los aros del ciclo
                        origen_arco_red_marginal = arco[0].etiqueta.origen.nombre
                        destino_arco_red_marginal = arco[0].etiqueta.destino.nombre
                        origen_arco_red_original = arco[0].etiqueta.etiqueta.origen.nombre
                        flujo_arco_red_original = arco[0].etiqueta.etiqueta.flujo
                        capacidad_arco_red_marginal = arco[0].etiqueta.capacidad
                        capacidad_arco_red_orginal = arco[0].etiqueta.etiqueta.capacidad
                        res_min_arco_red_original = arco[0].etiqueta.etiqueta.res_min
                        costo_arco_red_marginal = arco[0].etiqueta.costo
                        # caso para los arcos de la red marginal que van en el mismo sentido que su arco correspondiente en la red original
                        if(origen_arco_red_marginal == origen_arco_red_original):
                            # revisamos que se cumpla la condición de que la capacidad sea mayor al flujo
                            if(flujo_arco_red_original < capacidad_arco_red_orginal):
                                # si cumplen la condición, actualizamos la capacidad
                                arco[0].etiqueta.capacidad = capacidad_arco_red_orginal- flujo_arco_red_original
                            else:
                                # si no cumplen la condición eliminamos el arco de la red marginal
                                self.eliminar_arco(origen_arco_red_marginal,destino_arco_red_marginal,0,0,arco[0].etiqueta.capacidad)
                                # eliminamos el arco de la digrafica tambien
                                d.eliminar_arco(origen_arco_red_marginal,destino_arco_red_marginal,costo_arco_red_marginal)
                        else:
                         # caso para los arcos de la red marginal que van en sentido contrario que su arco correspondiente en la red original
                            # revisamos que se cumpla la condición de que el flujo sea mayor a la restricción minima
                            if(flujo_arco_red_original > res_min_arco_red_original):
                                 # si cumplen la condición, actualizamos la capacidad
                                arco[0].etiqueta.capacidad = flujo_arco_red_original - res_min_arco_red_original
                            else:
                                # si no cumplen la condición eliminamos el arco de la red marginal
                                self.eliminar_arco(origen_arco_red_marginal,destino_arco_red_marginal,0,0,arco[0].etiqueta.capacidad)
                                d.eliminar_arco(origen_arco_red_marginal,destino_arco_red_marginal,costo_arco_red_marginal)

                # ciclo para agregar los arcos que cumplan las condiciones a la red marginal
                for arco in ciclo:
                    if(type(arco[0]) == tipo):
                        # definimos las variables donde guardaremos los elementos de los arcos de las redes con respecto a las etiquetas de los aros del ciclo
                        origen_arco_red_original = arco[0].etiqueta.etiqueta.origen.nombre
                        destino_arco_red_original = arco[0].etiqueta.etiqueta.destino.nombre
                        flujo_arco_red_original = arco[0].etiqueta.etiqueta.flujo
                        costo_arco_original = arco[0].etiqueta.etiqueta.costo
                        capacidad_arco_red_orginal = arco[0].etiqueta.etiqueta.capacidad
                        res_min_arco_red_original = arco[0].etiqueta.etiqueta.res_min
                        arco_red_original = arco[0].etiqueta.etiqueta
                        
                        # caso para los arcos de la red marginal que van en el mismo sentido que su arco correspondiente en la red original
                        # revisamos que se cumpla la condición de que la capacidad sea mayor al flujo
                        if(flujo_arco_red_original < capacidad_arco_red_orginal):
                            # booleano para saber si se cumplen las condiciones para agregar el arco a la red marginal
                            bool = False

                            # recorremos los arcos de la red marginal y revisamos si el arco correspondiente ya existe
                            for nodo in self.__red:
                                for arco_red in self.__red[nodo]["salientes"]:
                                    # si el arco en el sentido correspondiente ya existe, el booleano será verdadero
                                    if arco_red.origen.nombre == origen_arco_red_original and arco_red.destino.nombre == destino_arco_red_original and arco_red.etiqueta == arco_red_original:
                                        bool = True
                             # si el arco no existe, lo agregamos ya que si cumple los requisitos para estar en la red marginal
                            if bool == False:
                                self.agregar_arco(origen_arco_red_original,destino_arco_red_original,0,0,capacidad_arco_red_orginal - flujo_arco_red_original,costo_arco_original)
                                # agregamos el arco a la digrafica también
                                d.agregar_arco(origen_arco_red_original,destino_arco_red_original,costo_arco_original)
                                # etiquetamos al nuevo arco de la red marginal con su arco relacionado con respecto a la red original
                                arcoNuevo = self.buscar_arco(origen_arco_red_original,destino_arco_red_original,0,0, capacidad_arco_red_orginal - flujo_arco_red_original)
                                arcoNuevo.etiqueta = arco_red_original
                                # etiquetamos al nuevo arco de digrafica con su arco relacionado con respecto a la red marginal
                                arcoNuevoDigrafica = d.buscar_arco(origen_arco_red_original,destino_arco_red_original,costo_arco_original)
                                arcoNuevoDigrafica.etiqueta = arcoNuevo

                        # caso para los arcos de la red marginal que van en sentido contrario que su arco correspondiente en la red original
                        # revisamos que se cumpla la condición de que el flujo sea mayor a la restricción minima
                        if(flujo_arco_red_original > res_min_arco_red_original):
                            # booleano para saber si se cumplen las condiciones para agregar el arco a la red marginal
                            bool = False
                            # recorremos los arcos de la red marginal y revisamos si el arco correspondiente ya existe
                            for nodo in self.__red:
                                for arco_red in self.__red[nodo]["salientes"]:
                                    # si el arco en el sentido correspondiente ya existe, el booleano será verdadero
                                    if arco_red.destino.nombre == origen_arco_red_original and arco_red.origen.nombre == destino_arco_red_original and arco_red.etiqueta == arco_red_original:
                                        bool = True
                            # si el arco no existe, lo agregamos ya que si cumple los requisitos para estar en la red marginal
                            if bool == False:
                                self.agregar_arco(destino_arco_red_original,origen_arco_red_original,0,0,flujo_arco_red_original - res_min_arco_red_original, -costo_arco_original) 
                                # agregamos el arco a la digrafica también
                                d.agregar_arco(destino_arco_red_original,origen_arco_red_original, -costo_arco_original) 
                                # etiquetamos al nuevo arco de la red marginal con su arco relacionado con respecto a la red original
                                arcoNuevo = self.buscar_arco(destino_arco_red_original,origen_arco_red_original,0,0,flujo_arco_red_original - res_min_arco_red_original)
                                arcoNuevo.etiqueta = arco_red_original
                                # etiquetamos al nuevo arco de digrafica con su arco relacionado con respecto a la red marginal
                                arcoNuevoDigrafica = d.buscar_arco(destino_arco_red_original,origen_arco_red_original, -costo_arco_original)
                                arcoNuevoDigrafica.etiqueta = arcoNuevo

            else: 
                # si no hay ciclos negativos, rompemos el while y se acaba el algoritmo              
                break        
                
            
    def algoritmo_dual(self,fuentes,sumideros,limite_flujo):
        # aplicamos for fulkerson con el limite de flujo deseado
  
        flujo = self.flujo_maximo(fuentes,sumideros,None,True)
      

        # revisamos si nos excedemos del limite de flujo
        if (flujo > limite_flujo):
            if(len(fuentes)>1):
                self.eliminar_nodo('A+')
            if(len(sumideros)>1):
                self.eliminar_nodo('Z-')
            return None

        # revisamos si hay más de un fuente o sumidero
        fuente = []
        sumidero = []
        if(len(fuentes)>1):
            fuente.append("A+")
        else:
            fuente = fuentes
        if(len(sumideros)>1):
            sumidero.append("Z-")
        else:
            sumidero = sumideros

        # aplicamos el algoritmo primal para obtener el flujo de menor costo
        if(flujo>0):
            self.algoritmo_primal(fuente,sumidero,flujo)
        
        costo = 0

        
        # lista de arcos de la red original
        arcos_red_original = []
  
    
        #calculamos el costo inicial, en base al primer flujo factible encontrado por ford fulkerson
        for nodo in self.__red:
            for arco in self.__red[nodo]["salientes"]:
                arcos_red_original.append(arco)
                costo += arco.flujo * arco.costo
        print("Costo inicial: ",costo)

        #Creamos la red marginal
        red_marginal = Red()

        # creamos la red marginal en base a los arcos de la re original
        red_marginal.crear_red_marginal(arcos_red_original)

        salientes_sumideros = []
        entrantes_sumideros = []
        for nodo in sumidero:
            for arco in self.__red[self.buscar_nodo(nodo)]["salientes"]:
                salientes_sumideros.append(arco)
            for arco in self.__red[self.buscar_nodo(nodo)]["entrantes"]:
                entrantes_sumideros.append(arco)

        
     
        # aplicamos el algoritmo usando la red marginal
        bool = red_marginal.rutas_cortas(fuente,sumidero,salientes_sumideros,entrantes_sumideros,limite_flujo)
        
        # regresamos none si no se encuentra una solución
        if not bool:
            return None
        
        if(len(fuentes)>1):
            self.eliminar_nodo('A+')
        if(len(sumideros)>1):
            self.eliminar_nodo('Z-')

        #calculamos e imprimimos el costo final
        costo = 0
        for nodo in self.__red:
            for arco in self.__red[nodo]["salientes"]:
                costo += arco.flujo * arco.costo

        return costo


    def rutas_cortas(self,fuente,sumidero,salientes_sumideros,entrantes_sumideros,flujo):
        # creamos el objeto dígrafica que usaremos para aplicar el algoritmo de rutas mas cortas (Floyd)
        # para encontrar ciclos negativos en la red marginal
        d = Digrafica()
        # creamos los arcos de la digrafica tomando los mismos arcos que hay en la red marginal 
            # tomamos el costo de los arcos de la red marginal como peso de los arcos de la digrafica
        print("ciclo2")
        for nodo in self.__red:
            for arco in self.__red[nodo]["salientes"]:
                d.agregar_arco(arco.origen.nombre,arco.destino.nombre,arco.costo)
                # etiquetamos los arcos de la digrafica con los arcos relacionados correspondientes a la red marginal
                arcoNuevo = d.buscar_arco(arco.origen.nombre,arco.destino.nombre,arco.costo)
                arcoNuevo.etiqueta = arco
        print("ciclo")
        # hacemos las iteraciones del algoritmo mientras haya ciclos negativos en la red marginal
        while(True):
            # aplicamos el algoritmo de floyd para encontrar ciclos negativos
            ruta = d.dikjstra_general(fuente[0],sumidero[0])
         
            # en caso de encontrar alguna ruta, seguimos con el algoritmo
            if ruta :
                # revisamos si encontramos un ciclo negativo
                if type(ruta[0]) == str:
                    return None
               
                # iniciamos el delta con valor infinito
                delta = math.inf
                # variable auxiliar para saber si los objetos de la lista ciclos son arcos o no
                tipo = type(ruta[0])
                
                        

                # calculamos el flujo actual de la red original
                flujo_actual = 0
                for arco in salientes_sumideros:
                    flujo_actual -= arco.flujo
                for arco in entrantes_sumideros:
                    flujo_actual += arco.flujo
                
                if flujo_actual >= flujo:
                    break

                # recorremos la ruta
                for arco in ruta:
                    # revisamos que el elemento de la ruta sea un objeto arco de de la clase digrafica            
                    if(type(arco)== tipo):
                        capacidad_arco_red_marginal = arco.etiqueta.capacidad
                        # comparamos las capacidades de los arcos del ciclo para buscar la mas pequeña y obtener el delta
                        if(capacidad_arco_red_marginal< delta):
                            delta = capacidad_arco_red_marginal
               
                # revisamos si el flujo que tiene actualmente la red mas el delta, se pasan del flujo establecido
                if(flujo_actual + delta > flujo):
                    delta -= flujo_actual + delta - flujo
                

                # recorremos los arcos de la ruta para actualizar el flujo de la red original 
                # los arcos de la ruta tienen como etiqueta sus arcos relacionados en la red marginal y los arcos de la red marginal
                # tienen como etiqueta los arcos relacionados en la red original
                for arco in ruta:
                    # revisamos que el elemento sea un arco de de la clase digrafica            
                    if(type(arco) == tipo):
                        # nodo orgien del arco relacionado de la red original
                        origen_arco_red_original = arco.etiqueta.etiqueta.origen.nombre
                        # para acceder a los arcos de la red original desde los arcos de la lista ciclo acccedemos a la etiqueta de la etiqueta
                        # si el arco del ciclo va en el mismo sentido a su arco relacionado en la red original, sumamos delta
                        if(origen_arco_red_original == arco.origen.nombre):
                            arco.etiqueta.etiqueta.flujo += delta
                            
                        else:
                             # si el arco del ciclo va en el sentido contrario a su arco relacionado en la red original, restamos delta
                            arco.etiqueta.etiqueta.flujo -= delta

                # ciclo para actualizar los arcos de la red marginal y eliminar los que no cumplan los requisitos
                # accederemos a los arcos de la red marginal y red orignal desde las etiquetas de los arcos del ciclo encontrado en la digrafica
                for arco in ruta:
                    # revisamos que el elemento sea un arco de de la clase digrafica            
                    if(type(arco) == tipo):
                        # definimos las variables donde guardaremos los elementos de los arcos de las redes con respecto a las etiquetas de los aros del ciclo
                        origen_arco_red_marginal = arco.etiqueta.origen.nombre
                        destino_arco_red_marginal = arco.etiqueta.destino.nombre
                        origen_arco_red_original = arco.etiqueta.etiqueta.origen.nombre
                        flujo_arco_red_original = arco.etiqueta.etiqueta.flujo
                        capacidad_arco_red_marginal = arco.etiqueta.capacidad
                        capacidad_arco_red_orginal = arco.etiqueta.etiqueta.capacidad
                        res_min_arco_red_original = arco.etiqueta.etiqueta.res_min
                        costo_arco_red_marginal = arco.etiqueta.costo
                        # caso para los arcos de la red marginal que van en el mismo sentido que su arco correspondiente en la red original
                        if(origen_arco_red_marginal == origen_arco_red_original):
                            # revisamos que se cumpla la condición de que la capacidad sea mayor al flujo
                            if(flujo_arco_red_original < capacidad_arco_red_orginal):
                                # si cumplen la condición, actualizamos la capacidad
                                arco.etiqueta.capacidad = capacidad_arco_red_orginal- flujo_arco_red_original
                            else:
                                # si no cumplen la condición eliminamos el arco de la red marginal
                                self.eliminar_arco(origen_arco_red_marginal,destino_arco_red_marginal,0,0,arco.etiqueta.capacidad)
                                # eliminamos el arco de la digrafica tambien
                                d.eliminar_arco(origen_arco_red_marginal,destino_arco_red_marginal,costo_arco_red_marginal)
                        else:
                         # caso para los arcos de la red marginal que van en sentido contrario que su arco correspondiente en la red original
                            # revisamos que se cumpla la condición de que el flujo sea mayor a la restricción minima
                            if(flujo_arco_red_original > res_min_arco_red_original):
                                 # si cumplen la condición, actualizamos la capacidad
                                arco.etiqueta.capacidad = flujo_arco_red_original - res_min_arco_red_original
                            else:
                                # si no cumplen la condición eliminamos el arco de la red marginal
                                self.eliminar_arco(origen_arco_red_marginal,destino_arco_red_marginal,0,0,arco.etiqueta.capacidad)
                                d.eliminar_arco(origen_arco_red_marginal,destino_arco_red_marginal,costo_arco_red_marginal)

                # ciclo para agregar los arcos que cumplan las condiciones a la red marginal
                for arco in ruta:
                    if(type(arco) == tipo):
                        # definimos las variables donde guardaremos los elementos de los arcos de las redes con respecto a las etiquetas de los aros del ciclo
                        origen_arco_red_original = arco.etiqueta.etiqueta.origen.nombre
                        destino_arco_red_original = arco.etiqueta.etiqueta.destino.nombre
                        flujo_arco_red_original = arco.etiqueta.etiqueta.flujo
                        costo_arco_original = arco.etiqueta.etiqueta.costo
                        capacidad_arco_red_orginal = arco.etiqueta.etiqueta.capacidad
                        res_min_arco_red_original = arco.etiqueta.etiqueta.res_min
                        arco_red_original = arco.etiqueta.etiqueta
                        
                        # caso para los arcos de la red marginal que van en el mismo sentido que su arco correspondiente en la red original
                        # revisamos que se cumpla la condición de que la capacidad sea mayor al flujo
                        if(flujo_arco_red_original < capacidad_arco_red_orginal):
                            # booleano para saber si se cumplen las condiciones para agregar el arco a la red marginal
                            bool = False

                            # recorremos los arcos de la red marginal y revisamos si el arco correspondiente ya existe
                            for nodo in self.__red:
                                for arco_red in self.__red[nodo]["salientes"]:
                                    # si el arco en el sentido correspondiente ya existe, el booleano será verdadero
                                    if arco_red.origen.nombre == origen_arco_red_original and arco_red.destino.nombre == destino_arco_red_original and arco_red.etiqueta == arco_red_original:
                                        bool = True
                             # si el arco no existe, lo agregamos ya que si cumple los requisitos para estar en la red marginal
                            if bool == False:
                                self.agregar_arco(origen_arco_red_original,destino_arco_red_original,0,0,capacidad_arco_red_orginal - flujo_arco_red_original,costo_arco_original)
                                # agregamos el arco a la digrafica también
                                d.agregar_arco(origen_arco_red_original,destino_arco_red_original,costo_arco_original)
                                # etiquetamos al nuevo arco de la red marginal con su arco relacionado con respecto a la red original
                                arcoNuevo = self.buscar_arco(origen_arco_red_original,destino_arco_red_original,0,0, capacidad_arco_red_orginal - flujo_arco_red_original)
                                arcoNuevo.etiqueta = arco_red_original
                                # etiquetamos al nuevo arco de digrafica con su arco relacionado con respecto a la red marginal
                                arcoNuevoDigrafica = d.buscar_arco(origen_arco_red_original,destino_arco_red_original,costo_arco_original)
                                arcoNuevoDigrafica.etiqueta = arcoNuevo

                        # caso para los arcos de la red marginal que van en sentido contrario que su arco correspondiente en la red original
                        # revisamos que se cumpla la condición de que el flujo sea mayor a la restricción minima
                        if(flujo_arco_red_original > res_min_arco_red_original):
                            # booleano para saber si se cumplen las condiciones para agregar el arco a la red marginal
                            bool = False
                            # recorremos los arcos de la red marginal y revisamos si el arco correspondiente ya existe
                            for nodo in self.__red:
                                for arco_red in self.__red[nodo]["salientes"]:
                                    # si el arco en el sentido correspondiente ya existe, el booleano será verdadero
                                    if arco_red.destino.nombre == origen_arco_red_original and arco_red.origen.nombre == destino_arco_red_original and arco_red.etiqueta == arco_red_original:
                                        bool = True
                            # si el arco no existe, lo agregamos ya que si cumple los requisitos para estar en la red marginal
                            if bool == False:
                                self.agregar_arco(destino_arco_red_original,origen_arco_red_original,0,0,flujo_arco_red_original - res_min_arco_red_original, -costo_arco_original) 
                                # agregamos el arco a la digrafica también
                                d.agregar_arco(destino_arco_red_original,origen_arco_red_original, -costo_arco_original) 
                                # etiquetamos al nuevo arco de la red marginal con su arco relacionado con respecto a la red original
                                arcoNuevo = self.buscar_arco(destino_arco_red_original,origen_arco_red_original,0,0,flujo_arco_red_original - res_min_arco_red_original)
                                arcoNuevo.etiqueta = arco_red_original
                                # etiquetamos al nuevo arco de digrafica con su arco relacionado con respecto a la red marginal
                                arcoNuevoDigrafica = d.buscar_arco(destino_arco_red_original,origen_arco_red_original, -costo_arco_original)
                                arcoNuevoDigrafica.etiqueta = arcoNuevo
               
            else: 
                # si no hay ciclos negativos, rompemos el while y se acaba el algoritmo              
                break        
                           
        return True

    def metodo_simplex(self):

        # revisamos que la sumatoria de la oferta/demanda sea igual a 0
        b = 0
        for nodo in self.__red:
            b += nodo.oferta_demanda

        # caso donde la sumatoria de la oferta/demanda de los nodos es mayor a cero
        if(b > 0):
            # creamos un nuevo nodo ficticio
            self.agregar_nodo("nodoDemanda")
            nuevoNodo = self.buscar_nodo("nodoDemanda")
            nuevoNodo.oferta_demanda = -b

            # creamos los arcos ficticios que van desde los nodos que de demanda hasta el nuevo nodo 
            for nodo in self.__red:
                if(nodo.oferta_demanda > 0):
                    self.agregar_arco(nodo.nombre,"nodoDemanda",0,0,math.inf,0)
        # caso donde la sumatoria de la oferta/demanda de los nodos es menor a cero
        if(b < 0):
            # creamos un nuevo nodo ficticio
            self.agregar_nodo("nodoOferta")
            nuevoNodo = self.buscar_nodo("nodoOferta")
            nuevoNodo.oferta_demanda = -b

            # creamos los arcos ficticios que van desde el nuevo nodo hacia los nodos que de demanda
            for nodo in self.__red:
                if(nodo.oferta_demanda > 0):
                    self.agregar_arco("nodoOferta",nodo.nombre,0,0,math.inf,0)



        # creamos el nodo ficticio para obtener la solución inicial
        self.agregar_nodo("nodoFicticio")
        # listas donde guardaremos los arcos que estan y no estan en la solución
        arcos_basicos = []
        arco_no_basicos = []

        lista_nodos = []

        # Creamos una lista con los nodos de la red y su oferta/demanda
        for nodo in self.__red:
            if (nodo.nombre != "nodoFicticio"):
                lista_nodos.append([nodo,nodo.oferta_demanda])

        # Calculamos el flujo inicial que tendran los arcos ficticios que crearemos
        # revisamos si hay arcos con restricciones minimas y satisfacemos dichas restricciones
        for nodo in lista_nodos:
            if (nodo[0].nombre != "nodoFicticio"):
                for arco in self.__red[nodo[0]]["salientes"]:
                    # si hay restrcción minima, la satisfacemos
                    if arco.res_min > 0:
                        arco.flujo = arco.res_min
                        # restamos el flujo de la oferta que tenia el nodo de origen del arco
                        nodo[1] -= arco.res_min
        # revisamos el flujo de los arcos entrantes de los nodos para ver que tanta demanda tendran antes de crear los arcos fictcios
        for nodo in lista_nodos:
            if (nodo[0].nombre != "nodoFicticio"):
                for arco in self.__red[nodo[0]]["entrantes"]:
                    if arco.flujo > 0:
                        # disminuimos la demanda de los arcos que inicialmente reciben flujo de los arcos
                        nodo[1] += arco.flujo
        
        # creamos los arcos fictcios entre los nodos originales y el nodo ficticio creado para obtener la solución inicial
        for nodo in lista_nodos:
            if (nodo[0].nombre != "nodoFicticio"):
                flujo_nodo_arco = 0
                # revisamos si el nodo tiene oferta o demanda
                if nodo[1] < 0:   
                    # si el nodo tiene demanda, creamos el arco que va del nodo ficticio al respectivo nodo original    
                    self.agregar_arco("nodoFicticio",nodo[0].nombre,0,-nodo[1],math.inf,9999)
                else:
                    # si el nodo tiene oferta, creamos el arco que va del nodo original al nodo ficticio
                    self.agregar_arco(nodo[0].nombre,"nodoFicticio",0,nodo[1],math.inf,9999)


        # crearemos una lista con los arcos dentro de la solucion y otra con los arcos que no estan en la solución
        # inicialmente los arcos de la solución serán los entrantes y salientes del nodo ficticio
        nodo_ficticio = self.buscar_nodo("nodoFicticio")
        for arco in self.__red[nodo_ficticio]["salientes"]:
            arcos_basicos.append(arco)
        for arco in self.__red[nodo_ficticio]["entrantes"]:
            arcos_basicos.append(arco)
        # llenamos la lista de arcos no basicos con los arcos de la red que no esten en la lista de arcos basicos
        for nodo in self.__red:
            for arco in self.__red[nodo]["salientes"]:
                if arco not in arcos_basicos:
                    arco_no_basicos.append(arco)
    
        # ciclo con el que realizaremos las iteraciones buscando los ciclos ya actualizando los flujos de los arcos
        while(True):

            bool = False
            # variable auxliar donde iremos guardando el peso del ciclo más grande que vayamos encontrando 
            w_max = 0
            # lista donde guardaremos el ciclo de peso más grande que vayamos encontrando
            ciclo_max = []


            # recorremos los arcos que no estan en la solución para ver si mejoran la solución actual
            for arco in arco_no_basicos:
                # variable donde guardaremos el peso de los ciclos
                w = 0
                # lista donde guardaremos los ciclos
                ciclo = []
                # lista donde guardaremos los nodos visitados cuando busquemos ciclos
                visitados = []

                # buscamos ciclos a partir de los arcos no saturados
                if(arco.capacidad - arco.flujo > 0):
                    self.dfs_ciclos(arco.destino,arco,ciclo,visitados,arcos_basicos)
                
                # revisammos si encontramos un ciclo y calculamos su peso
                if(ciclo):
                    # agregamos el arco iterado que posiblemente se unirá a la solución
                    ciclo.append(arco)
                    # lo etiquetamos con sentido propio
                    arco.etiqueta = "sentidoPropio"
 
                    # recorremos las aristas del ciclo para calcular el peso del ciclo
                    for arista in ciclo:
                        # caso donde las aristas van en sentido del ciclo (restamos el costo de la arista)
                        if(arista.etiqueta== "sentidoPropio"):
                                w += -(arista.costo)

                        else: 
                            # caso donde las aristas van en sentido contrario (sumamos el costo de la arista)
                               w += arista.costo
                    # comparamos si el peso del ciclo encontrado es mayor que 0 o mayor que el último ciclo de amyor peso encontrado

                    if(w>w_max):
                        # actualizamos la variable de peso maximo y guardamos el ciclo como el actual ciclo de peso máximo
                        w_max = w
                        ciclo_max = ciclo
                        # guardamos el arco iterado como el arco que se unirá a la solución
                        nuevo_arco_solucion = arco
                       


            # revisamos si encontramos el ciclo de peso más grande
            if (ciclo_max):
                ciclo_max = []
                visitados = []
                # iniciamos el delta con un valor muy grande
                delta = math.inf
                # recuperamos el ciclo de peso más grande a partir del arco que agregaremos a la solución
                self.dfs_ciclos(nuevo_arco_solucion.destino,nuevo_arco_solucion,ciclo_max,visitados,arcos_basicos)
                # agreamos el arco que se unirá a la solución al ciclo
                ciclo_max.append(nuevo_arco_solucion)
                nuevo_arco_solucion.etiqueta = "sentidoPropio"

                # recorremos las aristas del ciclo de peso amyor para calcular el delta
                # buscaremos los maximos y minimos de flujo que le podemos sumar o restar a los flujos de los arcos del ciclo       
                for arista in ciclo_max:

                    # caso donde los arcos van en sentido propio del ciclo 
                    # solo tomamos en cuenta arcos con flujo mayor a 0 para obtener el delta
                    if(arista.etiqueta== "sentidoPropio" and arista.flujo >0 ):
                        if(arista.capacidad != math.inf):
                            # caso donde el flujo es mayor que diferencia entre la capacidad del arco y su flujo
                            if(arista.capacidad - arista.flujo < arista.flujo):

                                delta_arco = arista.capacidad - arista.flujo
                            else:
                                # si el flujo es menor a la diferencia entre capacidad y flujo, entonces podemos tomar como posible delta al flujo del arco
                                delta_arco = arista.flujo
                        else:
                            # si el arco tiene capacidad infinita (gran M) entonces el posible delta será el flujo actual del arco
                            delta_arco = arista.flujo
                            
                        # si el posible delta del arco iterado es menor al último delta, enconces actualizamos el valor del delta
                        if (delta_arco < delta ):
                            delta = delta_arco
                           
                    else:
                        # caso donde los arcos van en sentido contrario al del ciclo
                        # solo tomamos en cuenta arcos con flujo mayor a 0 para obtener el delta
                        if(arista.flujo >0 ):
                            # caso donde el flujo es mayor que diferencia entre la restrcción minima del arco y su flujo
                            if(arista.flujo - arista.res_min < arista.flujo):
                                
                                delta_arco = arista.flujo - arista.res_min
                            else:
                                 # si el flujo es menor a la diferencia entre la res min y el flujo, entonces podemos tomar como posible delta al flujo del arco
                                delta_arco = arista.flujo
                            
                            if (delta_arco < delta ):
                                # si el posible delta del arco iterado es menor al último delta, enconces actualizamos el valor del delta
                                delta = delta_arco
                
                arista_fuera_solucion = None
                # actualizamos el flujo de los arcos del ciclo de acuerdo al delta obtenido
                for arco in ciclo_max:
                    # caso para los arcos que van en sentido del ciclo
                    if(arco.etiqueta== "sentidoPropio"):
                        arco.flujo+=delta
                    else:
                    # caso donde los arcos van en sentido contrario al ciclo
                        arco.flujo-=delta
                        # revisamos si arco saldrá de la solución dependiendo del flujo resultante después de sumar el delta
                        if(arco.flujo == arco.res_min):
                            arista_fuera_solucion = arco
                
         
                # agremos el arco a la lista de los arcos de la solución y lo sacamos de la lista de arcos que no estaban en la solucíon
                arcos_basicos.append(nuevo_arco_solucion)
                arco_no_basicos.remove(nuevo_arco_solucion)

                # sacamos el arco de la lista de arcos de la solución y lo metemos a la lista de arcos que no estan en la solución
                if(arista_fuera_solucion):
                   
                    arcos_basicos.remove(arista_fuera_solucion)
                    arco_no_basicos.append(arista_fuera_solucion)
              
       
                # calculamos el costo actual
                #costo = 0
                #for nodo in self.__red:
                    #for arco in self.__red[nodo]["salientes"]:
                        #costo += arco.flujo * arco.costo
                        #print("costo actual: " costo)
            else:
                # si iteramos todos los arcos que no estan en la solución y no encontramos ningún ciclo, detenemos el algoritmo
                break
        
    
        # eliminamos el nodo y arcos ficticios
        self.eliminar_nodo("nodoFicticio")

        # calculamos el costo final
        costo_final = 0
        for nodo in self.__red:
            for arco in self.__red[nodo]["salientes"]:
                costo_final += arco.flujo * arco.costo
        
        
        
        return costo_final


    

    # función para encontrar ciclos (metodo simplex)
    def dfs_ciclos(self, node,arco,ciclo,arcos_visitados,arcos_basicos):
        bool = False
        node.etiqueta = "marcado"
        for saliente in self.__red[node]["salientes"]: 
            if(saliente in arcos_basicos and saliente not in arcos_visitados and (saliente.capacidad - saliente.flujo)>0): 
                bool = True
                arcos_visitados.append(saliente)
                ciclo.append(saliente) 
                saliente.etiqueta = "sentidoPropio"
                if(saliente.destino == arco.origen):
                    return ciclo

                self.dfs_ciclos(saliente.destino,arco,ciclo,arcos_visitados,arcos_basicos)
                break

        if(bool == False):
            for entrante in self.__red[node]["entrantes"]: 
                if(entrante in arcos_basicos and entrante not in arcos_visitados and ( entrante.flujo - entrante.res_min)>0 and (entrante.capacidad - entrante.flujo)>0): 
                    bool = True
                    arcos_visitados.append(entrante)
                    ciclo.append(entrante) 
                    entrante.etiqueta = "sentidoImpropio"
                    if(entrante.origen == arco.origen):
                        return ciclo
                    self.dfs_ciclos(entrante.origen,arco,ciclo,arcos_visitados,arcos_basicos)
                    break
        
        

        if(bool == False):     
            if(len(ciclo)>=1):
                if(ciclo[len(ciclo)-1].etiqueta == "sentidoPropio"):      
                    nodo = ciclo[len(ciclo)-1].origen
                    ciclo.pop(len(ciclo)-1)
                    node.etiqueta = None
                    self.dfs_ciclos(nodo,arco,ciclo,arcos_visitados,arcos_basicos)
                    return None
                elif(ciclo[len(ciclo)-1].etiqueta == "sentidoImpropio"):
                    nodo = ciclo[len(ciclo)-1].destino
                    ciclo.pop(len(ciclo)-1)
                    node.etiqueta = None
                    self.dfs_ciclos(nodo,arco,ciclo,arcos_visitados,arcos_basicos)
                    return None