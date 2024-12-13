import copy
import operator
import math
from typing import MappingView
from estructuras_datos import *

class Arco:
    """
        Esta clase representa un arco. Tiene nodos de origen y destino, además de un peso
        y una etiqueta.
    """
    def __init__(self, origen, destino, peso=None, etiqueta=None, Id=None):
        self.origen = origen
        self.destino = destino
        self.peso = peso
        self.etiqueta = etiqueta
        self.Id = Id
#----------------------------------------------------------------

class Nodo:
    """
        Esta clase representa un nodo. Tiene un nombre, una etiqueta y 
        grados positivo y negativo.
    """
    def __init__(self, nombre, etiqueta=None):
        self.nombre = nombre
        self.etiqueta = etiqueta
        self.grado_positivo = 0
        self.grado_negativo = 0


#----------------------------------------------------------------
class Digrafica:
    """
        Esta clase representa una gráfica dirigia y sus operaciones.
    """
    def __init__(self):
        self.__digrafica = {} # Estructura donde se va a guardar la gráfica
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
        for nodo in self.__digrafica:
            if nodo.nombre == nombre:
                return nodo
        return False 

    def agregar_nodo(self, nombre):
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
        if self.buscar_nodo(nombre):
            return False
        
        # Si el nuevo nodo no existe, entonces se crea y se le añade un diccionario
        # con dos listas vacías, la lista de nodos "entrantes" y la lista de nodos "salientes"
        nodo = Nodo(nombre, etiqueta=None)
        self.__digrafica[nodo] = {"entrantes":[], "salientes":[]}

        # El número de nodos en la digráfica se incrementa y se regresa True
        self.__num_nodos += 1
        return True

    def agregar_arco(self, a, b, peso=None, Id=None):
        """
            Este método agrega un arco a la digráfica
            Parámetros
            ----------
            a: Nodo de origen.
            b: Nodo destino.
            peso: Peso del arco.
        """
        # Se agregan los nodos a y b (Esto porque le damos la opción al usuario de 
        # agregar arcos directamente sin la necesidad de que los nodos ya existan
        # en la digráfica)
        self.agregar_nodo(a)
        self.agregar_nodo(b)

        # Se obtienen los nodos a y b
        nodo_a = self.buscar_nodo(a)
        nodo_b = self.buscar_nodo(b)

        # Se construye el arco (a,b)
        arco = Arco(nodo_a, nodo_b, peso, Id=Id)

        # Se agrega el arco (a,b) a los salientes de a, y el grado positivo de a 
        # se incrementa en 1
        self.__digrafica[nodo_a]["salientes"].append(arco)
        nodo_a.grado_positivo += 1

        # Se agrega el arco (a,b) a los entrantes de b, y el grado negativo de b 
        # se incrementa en 1
        self.__digrafica[nodo_b]["entrantes"].append(arco)
        nodo_b.grado_negativo += 1

        # El contador de arcos se incrementa
        self.__num_arcos += 1
        
        return True

    def leer_digrafica(self, archivo):
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
                self.agregar_arco(line[0], line[1], float(line[2]))

    def buscar_arco(self, a, b, peso=None):
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
        
        # Si el nodo de origen sí existe, entonces se busca el arco en sus salientes
        
        if peso == None:
            peso_minimo = math.inf
            arco_minimo = None
            for arco in self.__digrafica[nodo_a]["salientes"]:
                # Si no se ha especificado un peso, entonces solamente se compara el 
                # nombre del nodo destino y buscamos el de peso menor
                if arco.destino.nombre == b and arco.peso < peso_minimo:
                        arco_minimo = arco
                        peso_minimo = arco.peso
      
            return arco_minimo
              
        else:
            for arco in self.__digrafica[nodo_a]["salientes"]:
                # Si el peso se ha especificado, entonces se compara el nombre del nodo 
                # destino y el peso del arco
                if arco.destino.nombre == b and arco.peso == peso:
                    return arco
        
        # Si se recorrieron todos los salientes del nodo de origen y no se encontró
        # el arco buscado, entonces se regresa False
        return False
    
    
    def eliminar_arco(self, a, b, peso=None):
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
        arco = self.buscar_arco(a, b, peso)

        # Si existe el arco, entonces se procede a elminarlo
        if arco:
            # El arco se elimina de los salientes del nodo de origen y el peso positivo
            # de éste se decrementa
            nodo_origen = arco.origen
            self.__digrafica[nodo_origen]["salientes"].remove(arco)
            nodo_origen.grado_positivo -= 1

            # El arco se elimina de los entrantes del nodo destino y el peso negativo
            # de éste se decrementa
            nodo_destino = arco.destino
            self.__digrafica[nodo_destino]["entrantes"].remove(arco)
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
            # Se eliminan todos los arcos salientes
            while self.__digrafica[nodo]["salientes"]:
                arco = self.__digrafica[nodo]["salientes"][0]
                self.eliminar_arco(arco.origen.nombre, arco.destino.nombre)
            
            # Se eliminan todos los arcos entrantes
            while self.__digrafica[nodo]["entrantes"]:
                arco = self.__digrafica[nodo]["entrantes"][0]
                self.eliminar_arco(arco.origen.nombre, arco.destino.nombre)

            # Cuando todos los arcos incidentes en el nodo se hayan eliminado procedemos a 
            # eliminar el nodo de la digráfica y decrementamos el contador de nodos
            self.__digrafica.pop(nodo)
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
            while self.__digrafica[nodo]["salientes"]:
                arco = self.__digrafica[nodo]["salientes"][0]
                self.eliminar_arco(arco.origen.nombre, arco.destino.nombre)
            
            # Se eliminan todos los arcos entrantes
            while self.__digrafica[nodo]["entrantes"]:
                arco = self.__digrafica[nodo]["entrantes"][0]
                self.eliminar_arco(arco.origen.nombre, arco.destino.nombre)
            
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
            for nodo in self.__digrafica:
                nodo.etiqueta = None
        elif tipo == "aristas":
            for nodo in self.__digrafica:
                for arco in self.__digrafica[nodo]["entrantes"]:
                    arco.etiqueta = None
                for arco in self.__digrafica[nodo]["salientes"]:
                    arco.etiqueta = None
        elif tipo == "todo":
            for nodo in self.__digrafica:
                for arco in self.__digrafica[nodo]["entrantes"]:
                    arco.etiqueta = None
                for arco in self.__digrafica[nodo]["salientes"]:
                    arco.etiqueta = None
        else:
            raise ValueError(f"Error en el tipo dado ({tipo}). Valores aceptados: 'nodos', 'aristas', 'todos'")

    def __str__(self):
        """
            Este método imprime la digráfica
        """
        resultado = ""
        for nodo in self.__digrafica:
            resultado += f"Nodo: {nodo.nombre}\nEntrantes: "
            for arco in self.__digrafica[nodo]["entrantes"]:
                if arco.peso:
                    resultado += f"({arco.origen.nombre}, {arco.peso}), "
                else:
                    resultado += f"{arco.origen.nombre}, "

            resultado = resultado[:-2] + "\nSalientes: "

            for arco in self.__digrafica[nodo]["salientes"]:
                if arco.peso:
                    resultado += f"({arco.destino.nombre}, {arco.peso}), "
                else:
                    resultado += f"{arco.destino.nombre}, "
            
            resultado = resultado[:-2] + "\n\n"
        
        resultado = resultado[:-2]

        return resultado 
    

    def __recuperar_ruta(self, nodo_actual, nodo_inicial):
        # Comenzamos la recuperación de la ruta en el nodo actual
        ruta = []
        arista_antecesor = nodo_actual.etiqueta["antecesor"]
        # Recuperamos arcos mientras el nodo actual no sea el nodo inicial
        while arista_antecesor != nodo_inicial:
            # Tomamos el antecesor del nodo actual mediante su etiqueta
            #antecesor = nodo_actual.etiqueta["antecesor"]
            # Se busca el objeto Arco que va desde el antecesor hasta el nodo actual y 
            # se agrega al principio de la lista, así terminaremos con la ruta ya ordenada
            ruta.insert(0, arista_antecesor)
            # Se actualiza el nodo actual
            arista_antecesor = arista_antecesor.origen.etiqueta["antecesor"]
        # Una vez que alcancemos el nodo inicial en la recuperación de la ruta, ésta
        # se regresa
        return ruta


    def dijkstra(self, nodo_inicial, nodo_final=None):
        # Se obtienen los nodos inicial y final
        a = self.buscar_nodo(nodo_inicial)
        if not a:
            raise ValueError(f"Error. El nodo inicial {nodo_inicial} no existe en la digráfica")

        if nodo_final:
            z = self.buscar_nodo(nodo_final)
            if not z:
                raise ValueError(f"Error. El nodo final {nodo_final} no existe en la digráfica" )
        else:
            z = None

        # el nodo inicial se etiqueta como temporal, como antecesor de él mismo y con una longitud
        # de ruta de 0, además se agrega a la lista de nodos etiquetados temporalmente
        a.etiqueta = {"tipo_etiqueta":"temporal", "antecesor":a, "longitud_ruta":0}
        X = [a]

        # El algoritmo continúa hasta que se acaben los nodos etiquetados temporalmente
        # o encontremos la ruta más corta hasta el nodo final z
        while X:
            # Se obtiene el nodo en X con la longitud de ruta más pequeña
            x = min(X, key=lambda nodo: nodo.etiqueta["longitud_ruta"])

            # x se elimina del conjunto de vértices marcados temporalmente y se marca de forma
            # definitiva
            X.remove(x)
            x.etiqueta["tipo_etiqueta"] = "definitiva"

            # Si x = z recuperamos la ruta y la regresamos. En caso de no especificar el nodo final
            # el algoritmo va a continuar hasta agotar la lista de nodos etiquetados temporalmente
            # para encontrar la ruta más corta desde el nodo inicial hacia todos los demás.
            # En este último caso esta condición también nos sirve ya que z siempre será None y
            # x nunca será None por lo tanto, siempre x != z
            if x == z:
                return self.__recuperar_ruta(x, a)
            
            # Si x != z, entonces se iteran los salientes de x:
            for arco in self.__digrafica[x]["salientes"]:
                # Se toma el destino del arco actual
                v = arco.destino
                # Si no tiene etiqueta, entonces se marca como temporal, con antecesor = x y
                # longitud de L(x) + w(arco). Además, se agrega a la lista de nodos etiquetados
                # temporalmente
                if not v.etiqueta:
                    v.etiqueta = {"tipo_etiqueta":"temporal", "antecesor":arco, "longitud_ruta":x.etiqueta["longitud_ruta"] + arco.peso}
                    X.append(v)

                # Si v tiene etiqueta temporal, entonces se revisa si la ruta desde x es mejor que
                # la que ya tenía
                elif v.etiqueta["tipo_etiqueta"] == "temporal":
                    # Si la longitud de la ruta viniendo desde x mejora la etiqueta de v, entonces
                    # se actualiza esta longitud y su antecesor ahora será X.
                    if x.etiqueta["longitud_ruta"] + arco.peso < v.etiqueta["longitud_ruta"]:
                        v.etiqueta["longitud_ruta"] = x.etiqueta["longitud_ruta"] + arco.peso 
                        v.etiqueta["antecesor"] = arco
        
        # Si llegamos hasta este punto y el usuario había especificado un nodo final, entonces
        # significa que no existe una ruta desde el nodo inicial hasta el nodo final, por lo tanto
        # se regresa una ruta vacía. En caso contrario, recuperamos el sistema de rutas más cortas

        if nodo_final:
            return []
        else:
            rutas = []
            for nodo in self.__digrafica:
                # Buscaremos rutas siempre y cuando el nodo tenga etiqueta, de lo contrario
                # no fue marcado por el algoritmo ya que no existe algúna trayectoria desde el
                # vértice inicial hasta este nodo
                if nodo != a and nodo.etiqueta:
                    rutas =list(set().union(rutas,self.__recuperar_ruta(nodo, a)))
            return rutas


    def dijkstra_general(self, nodo_inicial, nodo_final=None):
        # Se buscan los dos nodos
        nodo_inicial = self.buscar_nodo(nodo_inicial)
        n_final = self.buscar_nodo(nodo_final)

        # Si se especificó un nodo final, pero no existe, entonces regresamos
        if nodo_final and not n_final:
            raise ValueError(f"Error. El nodo final {nodo_final} no existe en la digráfica" )
        
        # Se encuentra la arborescencia temporal con dijkstra normal
        arborescencia = self.dijkstra(nodo_inicial.nombre, None)
        
        # Obtenemos las aristas sin usar
        aristas_sin_usar = []
        
        for nodo in self.__digrafica:
            for arco in self.__digrafica[nodo]["salientes"]:
                # únicamente tomaremos en cuenta los arcos cuyos extremos tengan etiqueta porque
                # en caso contrario, significa que no existe ruta desde el vértice inicial hasta
                # el nodo sin etiqueta
                if arco not in arborescencia and arco.origen.etiqueta and arco.destino.etiqueta:
                    aristas_sin_usar.append(arco)
           
      
        i = 0
        while i < len(aristas_sin_usar):
            # Tomamos la i-ésima arista sin usar
            a = aristas_sin_usar[i]
          
            # Comparamos si la arista sin usar mejora la arborescencia
            if a.origen.etiqueta["longitud_ruta"] + a.peso < a.destino.etiqueta["longitud_ruta"]:
                
                # Si la arista sin usar mejora la ruta, primero checamos si no forma un ciclo negativo
                arista_antecesor = a.origen.etiqueta["antecesor"] 
                # lista donde guardaremos las aristas del ciclo, en caso de que se encuentre uno              
                ciclo = []
                # elemento para identificar si se regresa un ciclo
                ciclo.append('ciclo')
                # agregamos la arista a al ciclo prvisionalmente
                ciclo.append(a)

                # ciclo para revisar ancestros y detectar ciclos
                while arista_antecesor != nodo_inicial:
                    if(arista_antecesor != a):
                        ciclo.append(arista_antecesor)
                
                    # If que revisa si los nodos del arista son ancestros
                    if arista_antecesor ==  a :
                        # calculamos la longitud del ciclo
                        longitud_ciclo = a.origen.etiqueta["longitud_ruta"] + a.peso - a.destino.etiqueta["longitud_ruta"]
                        # agreamos la longitud del ciclo como último elemento de la lista
                        ciclo.append(longitud_ciclo)
                        return ciclo
     
                    
                    arista_antecesor = arista_antecesor.origen.etiqueta["antecesor"]
                
                if(a.destino == nodo_inicial):
                        longitud_ciclo = a.origen.etiqueta["longitud_ruta"] + a.peso - a.destino.etiqueta["longitud_ruta"]
                        ciclo.append(longitud_ciclo)
                        return ciclo
                # Si no se formó ningún ciclo negativo, entonces eliminamos la nueva arista de 
                # las aristas sin usar y la agregamos a la arborescencia. Además, la arista 
                # mejorada se elimina de la arborescencia y se agrega a las aristas sin usar.
                aristas_sin_usar.remove(a)
                arborescencia.append(a)
                aristas_sin_usar.append(a.destino.etiqueta["antecesor"])
                print(a.destino.nombre)
                arborescencia.remove(a.destino.etiqueta["antecesor"])

                # Se actualiza el antecesor del destino de la nueva arista
                a.destino.etiqueta["antecesor"] = a

                # Se calcula el valor con el cuál se van a actualizar las etiquetas de los 
                # descendientes del nodo actualizado
                delta = a.origen.etiqueta["longitud_ruta"] + a.peso - a.destino.etiqueta["longitud_ruta"]

                # Se ejecuta una búsqueda a profundidad para actualizar a los descendientes
                visitados = []
  
                self.dfs(a.destino,visitados, arborescencia, delta)
                
                # Como ahora existe una nueva arista sin usar, entonces volvemos a recorrer la
                # lista de aristas sin usar desde el principio
                i = 0
            else:
                # Si la arista sin usar elegida no mejora la arborescencia, entonces pasamos a 
                # revisar la arista que sigue en la lista de arcos sin usar
                i+=1
        
        # Si se ha especificado un nodo final, entonces se regresa la ruta desde el nodo inicial
        # hacia dicho nodo final. En caso contrario se regresa la arborescencia completa

        if n_final:
            if not n_final.etiqueta:
                return []
            else:
                return self.__recuperar_ruta(n_final, nodo_inicial)

        return arborescencia




    def dfs(self, node,visited, arborescencia, delta):
        if node not in visited:
            visited.append(node) 
            node.etiqueta["longitud_ruta"] += delta
            for saliente in self.__digrafica[node]["salientes"]:   
               if saliente in arborescencia:  
                   self.dfs(saliente.destino,visited,arborescencia,delta) 
    
    def genera_matriz(self,nodos): 
        # Lista de listas donde guardaremos los elementos de la matriz
        lista_matriz = []

        # Recorremos los nodos de la lista de nodos
        for nodo in nodos:
            # Lista que corresponde a los renglones de la matriz del algoritmo
            # donde guardaremos los elementos (aristas y pesos) correspondientes a cada nodo
            lista_nodo = []
            # Recorremos los nodos para buscar si hay un arco del nodo(nodos de los renglones de la matriz) al nodo2(nodos de las columnas)
            for nodo2 in nodos:

                arco = None   

                # si el nodo de origen es igual al nodo destino (elementos de la diagonal de la matriz)
                # agregamos el nodo con longitud 0 (camino de un nodo a si mismo)
                if(nodo2==nodo):
                    lista_nodo.append([nodo,0])
                # otros casos
                else:
                    # si existe un arco entre el nodo1 y nodo2, recuperamos el de peso minimo y lo metemos a la matriz
                    arco = self.buscar_arco(nodo.nombre,nodo2.nombre)

                    # revisamos si se encontró dicho arco
                    if (arco):
                        lista_nodo.append([arco,arco.peso])

                    # si no existe un arco entre el par nodos, agregamos privisionalmente valores basura
                    else:
                        lista_nodo.append(['-',math.inf])

            # agregamos la lista correspondiente a cada nodo a matriz 
            # dicha lista corresponde a los renglones de la matriz
            lista_matriz.append(lista_nodo)

        return lista_matriz

        

    def floyd(self,nodo_origen = None,destino = None):
        # buscamos el nodo de origen y nodo destino 
        origen = self.buscar_nodo(nodo_origen)
        
        if nodo_origen == None:
            return None

        # Creamos una lista con los nodos de la gráfica
        nodos = []
        for nodo in self.__digrafica:
            nodos.append(nodo)
            
        # Ordenamos los nodos de acuerdo a sus nombres
        nodos.sort(key=lambda a:a.nombre)

        # Generamos la matriz inicial del algoritmo
        lista_matriz = self.genera_matriz(nodos)

        # Obtenemos la cantidad de nodos de la gráfica
        num_nodos = len(nodos)

        # Hacemos las iteraciones del algoritmo
        for k in range(num_nodos):
            for i in range(num_nodos):
                for j in range(num_nodos):

                    # Revisamos que no haya infinitos
                    if((lista_matriz[i][k][1] != math.inf) and (lista_matriz[k][j][1] != math.inf) ):

                        # Si el nuevo peso es menor al actual, actualizamos el peso y el nodo de origen 
                        if (lista_matriz[i][j][1]) > (lista_matriz[i][k][1] + lista_matriz[k][j][1]):
                            
                            # Revisamos si un elemento de la diagonal cambió de valor, para ver si hay ciclo
                            if(i == j ):
                               
                                # si uno de los elementos de la diagonal de la matriz cambia de valor, entonces hay un ciclo.

                                # Actualizamos los valores de la dupla del elemento ij (arco y longitud)
                                lista_matriz[i][j][0] = self.buscar_arco(lista_matriz[k][j][0].origen.nombre,nodos[j].nombre)
                                lista_matriz[i][j][1]= lista_matriz[i][k][1] + lista_matriz[k][j][1]
                                if not destino:
                              
                                    # recuperamos la ruta del ciclo
                                    ruta_ciclo = []
                                    ruta_ciclo = self.regresar_ruta_ciclo(i,j,lista_matriz,nodos)
                                
                                    return ruta_ciclo, lista_matriz
                            else:   
                           
                                # si el nuevo peso es menor, actualizamos el arco del elemento ij de la matriz    
                                lista_matriz[i][j][0] = self.buscar_arco(lista_matriz[k][j][0].origen.nombre,nodos[j].nombre)

                                # Si el nuevo peso es menor actualizamos le peso del elemento ij
                                lista_matriz[i][j][1]= lista_matriz[i][k][1] + lista_matriz[k][j][1]


      
        # recuperamos la ruta
        ruta_corta = self.recuperar_ruta_floyd(lista_matriz,origen,nodos,destino)

        return ruta_corta, lista_matriz

    
    def recuperar_ruta_floyd(self,matriz,nodo,lista_nodos, destino = None):
        
        destino = self.buscar_nodo(destino)

        # Obtenemos la posición del nodo de origen dentro de la lista de nodos, 
        # para saber de que renglon de la matriz obtendremos las rutas
        posicion_nodo = lista_nodos.index(nodo)

        # lista de rutas desde el nodo origen hasta los demas nodos
        rutas = []
        if destino:
            # ruta individual desde el origen hasta determinado nodo
            ruta_hacia_nodo = []
            # Agregamos el nodo a la lista para identificar el nodo destino de la ruta
            ruta_hacia_nodo.append(destino)

            # si el nodo de origen es igual al nodo destino, solo agregaremos el elemento correspondiente a ese nodo en la diagonal
            # caso donde el nodo de origen y nodo destino son el mismo
            if nodo == destino:
                ruta_hacia_nodo.append(matriz[posicion_nodo][posicion_nodo][0])
                rutas.append(ruta_hacia_nodo)
            # caso donde obtendremos la ruta del nodo origen a los demas    
            else:
                # obtenemos la posición del nodo destino
                try:
                    posicion_nodo1 = lista_nodos.index(destino)
                except:
                    return None

                if matriz[posicion_nodo][posicion_nodo1][1] == math.inf:
                    return None
                
            
                # ciclo para recuperar ruta del origen al nodo correspondiente (destino)
                while(True):
       
                    if(posicion_nodo == posicion_nodo1):
          
                        if type(matriz[posicion_nodo][posicion_nodo][0])!= Nodo:
                            posicion_nodo1 = lista_nodos.index(matriz[posicion_nodo][posicion_nodo1][0].origen)
                            ruta_ciclo = self.regresar_ruta_ciclo(posicion_nodo,posicion_nodo1,matriz,lista_nodos)
                            return ruta_ciclo
                    # si encontramos un elemento con peso infinito o un nodo, detenemos el ciclo
                    # condicional que se cumplirá cuando ya no haya más camino que recuperar
                    if type(matriz[posicion_nodo][posicion_nodo1][0])== Nodo:
                        break   
                    
                    
                    # agregamos el arco a la ruta             
                    ruta_hacia_nodo.append(matriz[posicion_nodo][posicion_nodo1])
                   
                    # actualizamo la posición del nodo destino, que será el origen del nodo destino anterior
                   
                    posicion_nodo1 = lista_nodos.index(matriz[posicion_nodo][posicion_nodo1][0].origen)


                # agregamos la ruta del nodo origen al nodo correspondiente a la lista con las rutas 
                rutas.append(ruta_hacia_nodo)
        else:
            # recorremos los nodos de la gráfica, correspondiente a las columnas de la matriz
            for nodo1 in lista_nodos:
                # ruta individual desde el origen hasta determinado nodo
                ruta_hacia_nodo = []
                # Agregamos el nodo a la lista para identificar el nodo destino de la ruta
                ruta_hacia_nodo.append(nodo1)

                # si el nodo de origen es igual al nodo destino, solo agregaremos el elemento correspondiente a ese nodo en la diagonal
                # caso donde el nodo de origen y nodo destino son el mismo
                if nodo == nodo1:
                    ruta_hacia_nodo.append(matriz[posicion_nodo][posicion_nodo][0])
                    rutas.append(ruta_hacia_nodo)
                # caso donde obtendremos la ruta del nodo origen a los demas    
                else:
                    # obtenemos la posición del nodo destino
                    posicion_nodo1 = lista_nodos.index(nodo1)

                    # ciclo para recuperar ruta del origen al nodo correspondiente (destino)
                    while(True):
                        # si encontramos un elemento con peso infinito o un nodo, detenemos el ciclo
                        # condicional que se cumplirá cuando ya no haya más camino que recuperar
                        if matriz[posicion_nodo][posicion_nodo1][1] == math.inf or type(matriz[posicion_nodo][posicion_nodo1][0])== Nodo:
                            break   

                        # agregamos el arco a la ruta             
                        ruta_hacia_nodo.append(matriz[posicion_nodo][posicion_nodo1])

                        # actualizamo la posición del nodo destino, que será el origen del nodo destino anterior
                        posicion_nodo1 = lista_nodos.index(matriz[posicion_nodo][posicion_nodo1][0].origen)

                    # invertimos la lista para ordenar los arcos
                    ruta_hacia_nodo.reverse()

                    # agregamos la ruta del nodo origen al nodo correspondiente a la lista con las rutas 
                    rutas.append(ruta_hacia_nodo)  
          

        return rutas
    
    def regresar_ruta_ciclo(self, i, j, lista_matriz, nodos):
        ruta_ciclo = []
        # agregamos un identificador para detectar que se regresó un ciclo y agregamos la longitud del ciclo (dupla)
        ruta_ciclo.append(['ciclo',lista_matriz[i][j][1]])

        # columna inicial del cilo
        posicion_nodo1 = j

        # nodo inicial donde se encontró el ciclo
        nodo_ciclo = lista_matriz[i][j][0].origen

        # ciclo para recuperar arcos del ciclo negativo
        while(True):
            # si encontramos un elemento con peso infinito o un nodo, detenemos el ciclo
            # condicional que se cumplirá cuando ya no haya más camino que recuperar
            if lista_matriz[i][posicion_nodo1][1] == math.inf or type(lista_matriz[i][posicion_nodo1][0])== Nodo:
                break   
          
            # agregamos el arco a la ruta             
            ruta_ciclo.append(lista_matriz[i][posicion_nodo1])
            
            # actualizamo la posición del nodo destino, que será el origen del nodo destino anterior
            posicion_nodo1 = nodos.index(lista_matriz[i][posicion_nodo1][0].origen)
            
            # cuando volvemos al origen, ya tenemos el ciclo completo
            if(lista_matriz[i][posicion_nodo1][0].origen == nodo_ciclo):
                # ordenamos los arcos
                ruta_ciclo.reverse()
                break
       
        return ruta_ciclo

    def imprimir_rutas_floyd(self,nodo1,matriz):
        print('Rutas mas cortas desde el nodo ',nodo1, ' :')
        print("")
        for x in matriz:
            print("Ruta más corta hacia el nodo ",x[len(x)-1].nombre,': ', end="")
            longitud_ruta = math.inf
            if(nodo1 == x[len(x)-1].nombre):
                longitud_ruta = 0
            for y in x:
                if(type(y)!= Nodo):
                    if type(y[0])== Arco:
                        print('(',y[0].origen.nombre,', ', y[0].destino.nombre,')', end="")
                        if(y[0].destino == x[len(x)-1]):
                            longitud_ruta = y[1]
            
                        
            if(longitud_ruta == math.inf):
                print(" No hay ruta más corta :(")
            else: print(', Longitud: ', longitud_ruta)
     
        
    def arcos_floyd(self,rutas): 
        arcos = set()
        for ruta in rutas:
            for arco in ruta:
                if(type(arco)!= Nodo):
                    if type(arco[0])== Arco:
                        arcos.add(arco[0]) 
        return arcos
    
    def ruta_nodos_floyd(self,origen=None,destino=None):

        # verificamos que esixtan los nodos origen y destino
        if (self.buscar_nodo(origen) == None or self.buscar_nodo(destino)== None):
            return None

        # aplicamos el algoritmo
        rutas_origen, matriz = self.floyd(origen,destino)
        if rutas_origen:
            # si se encontró un ciclo negativo, regresamos el ciloc
            if (rutas_origen[len(rutas_origen)-1][0]=="ciclo"):
                return rutas_origen, matriz
            
            # recuperamos la ruta del nodo origen al nodo destino
            ruta = self.arcos_floyd(rutas_origen)
            ruta = list(ruta)
            # agregamos la longitud de la ruta al final de la lista de los arcos
            ruta.append(rutas_origen[len(rutas_origen)-1][1][1])

        
            return ruta, matriz
        else:
            return None, matriz

    def objeto_arco(self):
        return Arco