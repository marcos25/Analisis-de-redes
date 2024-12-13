import copy
import operator
import math
from estructuras_datos import *

class Arista:
    """
        Esta clase representa una arista. Tiene un nodo destino
        y una etiqueta. De esta forma es más fácil agregar otros
        atributos, por ejemplo, un peso.
    """
    def __init__(self, origen, destino, Id, peso=0, etiqueta=None):
        self.origen = origen
        self.destino = destino
        self.Id = Id
        self.peso = peso
        self.etiqueta = etiqueta
#----------------------------------------------------------------

class Nodo:
    """
        Esta clase representa un nodo. Tiene un nombre y una etiqueta que
        siempre será None por defecto.
    """
    def __init__(self, nombre, etiqueta=None):
        self.nombre = nombre
        self.etiqueta = etiqueta
        self.grado = 0


#----------------------------------------------------------------
class Grafica:
    """
        Esta clase representa una gráfica y sus operaciones.
    """
    def __init__(self):
        self.__grafica = {} # Estructura donde se va a guardar la gráfica
        self.__num_nodos = 0 # Contador de nodos
        self.__num_aristas = 0 # Contador de aristas

    """
        Este método busca un nodo en la gráfica.
        Parametros:
        nodo: Nodo a buscar
        Regresa:
        True si el nodo se encuentra en la gráfica.
        None si el nodo no se encuentra en la gráfica. 
    """
    def buscar_nodo(self, nombre):
        for nodo in self.__grafica:
            if nodo.nombre == nombre:
                return nodo
        return False 

    """
        Este método agrega un nodo a la gráfica.
        Parámetros
        ----------
        nodo: Nodo que se desea agregar
    """
    def agregar_nodo(self, nombre):
        # Se busca el nodo en la gráfica, si no está, entonces
        # se agrega y el contador de nodos se incrementa
        if self.buscar_nodo(nombre):
            return False

        nodo = Nodo(nombre, etiqueta=None)
        self.__grafica[nodo] = []
        self.__num_nodos += 1
        return True 
    
    def editar_nombre_nodo(self, nombre_actual, nombre_nuevo):
        """
            Este método edita el nombre de un nodo

            Parámetros
            ----------
            nombre_actual: Nombre actual del nodo
            nombre_nuevo: Nombre nuevo del nodo

        """
        nodo = self.buscar_nodo(nombre_actual)
        if not nodo:
            return False

        nodo.nombre = nombre_nuevo 
        return True


    """
        Este método agrega una arista a la gráfica
        Parámetros
        ----------
        a: Nodo 1 de la arista.
        b: Nodo 2 de la arista.
        etiqueta: Etiqueta de la arista.
    """
    def agregar_arista(self, a, b, Id=None, peso=None):
        self.agregar_nodo(a)
        self.agregar_nodo(b)

        nodo_a = self.buscar_nodo(a)
        nodo_b = self.buscar_nodo(b)

        self.__grafica[nodo_a].append( Arista(nodo_a, nodo_b, Id, peso) )

        # Si no se trata de un lazo, entonces la arista también se agrega en el nodo b
        # y se aumenta en 1 el grado de a y el grado de b
        if a != b:
            self.agregar_nodo(b)
            nodo_b = self.buscar_nodo(b)


            # Se agrega el nodo b y después se agrega una arista hacia
            # a con la etiqueta a su lista
            self.__grafica[nodo_b].append( Arista(nodo_b, nodo_a, Id, peso) )

        nodo_a.grado += 1
        nodo_b.grado += 1
     


        # El contador de aristas se incrementa
        self.__num_aristas += 1
        
        return True

    """
        Este método lee una gráfica desde un archivo
    """
    def leer_grafica(self, archivo):
        file1 = open(archivo, 'r') 
        Lines = file1.readlines() 

        for line in Lines:
            line = line.strip().split(",")
            length = len(line)
            if length == 1:
                self.agregar_nodo(line[0])
            elif length == 2:
                self.agregar_arista(line[0], line[1])
            elif length == 3:
                self.agregar_arista(line[0], line[1], line[2])

    """
        Este método busca una arista. En caso de que un nodo
        tenga varias aristas sin etiqueta hacia otro mismo nodo,
        entonces únicamente se va a eliminar la primer ocurrencia.
        Parámetros
        ----------
        etiqueta: Etiqueta de la arista a buscar
        Regresa
        -------
        Si se encuentra la arista, regresa el nodo en donde se encontró
        Si no se encuentra, entonces regresa None
        
        Si no se encuentra la arista, regresa None, None
    """
    def buscar_arista(self, a, b, peso=None):
        nodo_a = self.buscar_nodo(a)

        if not nodo_a:
            return False
          
        for arista in self.__grafica[nodo_a]:
            if peso == None:
                if arista.destino.nombre == b:
                    return arista
            else:
                if arista.destino.nombre == b and arista.peso == peso:
                    return arista 
        return False
    
    """
        Este método elimina una arista de la gráfica
        Parámetros
        ----------
        etiqueta: Etiqueta de la arista
    """    
    def eliminar_arista(self, a, b, peso=None):
        # Si existe la arista, entonces se procede a elminarla
        if self.buscar_arista(a, b, peso):
            # Se busca el nodo a para eliminar la arista a,b
            nodo_a = self.buscar_nodo(a)
            for arista in self.__grafica[nodo_a]:
                if peso == None:
                    if arista.destino.nombre == b:
                        arista1 = arista
                        break
                else:
                    if arista.destino.nombre == b and arista.peso == peso:
                        arista1 = arista
                        break
            self.__grafica[nodo_a].remove(arista1)

            # Si no se trata de un lazo, entonces se busca el nodo b para eliminar la arista b,a
            # y el grado de ambos nodos se decrementa en 1
            if a != b:
                nodo_b = self.buscar_nodo(b)
                for arista in self.__grafica[nodo_b]:
                    if peso == None:
                        if arista.destino.nombre == a:
                            arista2 = arista
                            break
                    else:
                        if arista.destino.nombre == a and arista.peso == peso:
                            arista2 = arista
                            break
                
                self.__grafica[nodo_b].remove(arista2)
                nodo_a.grado -= 1
                nodo_b.grado -= 1
            # Si se trata de un lazo, entonces no es necesario eliminar la arista b,a (pues es la misma)
            # simplemente se decrementa el grado de a en 2
            else:
                nodo_a.grado -= 2

            # Sea cual sea el caso, el número de aristas se decrementa en 1
            self.__num_aristas -= 1

            return True

        return False

    """
        Este método elimina un nodo de la gráfica
        Parámetros
        ----------
        nodo: Nodo que se quiere eliminar
    """
    def eliminar_nodo(self, nombre):
        # Si se encuentra el nodo, entonces se procede a eliminarlo
        nodo = self.buscar_nodo(nombre)
        if nodo:
            # Antes de eliminar el nodo debemos eliminar todas las aristas que
            # inciden en él. Lo hacemos con el método eliminar_arista() y usamos
            # la bandera unSentido=True porque no se necesita borrar la arista del nodo que
            # vamos a eliminar.
            while self.__grafica[nodo]:
                self.eliminar_arista(nombre, self.__grafica[nodo][0].destino.nombre)
    
            # Cuando todas las aristas del nodo se hayan eliminado procedemos a 
            # eliminar el nodo de la gráfica y decrementamos el contador de nodos
            self.__grafica.pop(nodo)
            self.__num_nodos -= 1
            return True
        else:
            return False
    
    """
        Este método obtiene el grado de un nodo de la gráfica
        Parámetros
        ----------
        nodo: Nodo al que se le va a calcular el grado
        Regresa
        -------
        El grado del nodo
    """
    def obtener_grado(self, nombre):
        # Primero se busca el nodo
        nodo = self.buscar_nodo(nombre)
        if nodo:
            # El grado se calcula con la longitud de su lista de aristas
            return nodo.grado
        return False
    
    """
        Este método obtiene el número de nodos de la gráfica
        Regresa
        -------
        El número de nodos de la gráfica
    """
    def obtener_numero_nodos(self):
        # Simplemente regresamos el valor del contador de nodos
        return self.__num_nodos
    
    """
        Este método obtiene el número de aristas de la gráfica
        Regresa
        -------
        El número de aristas de la gráfica
    """
    def obtener_numero_aristas(self):
        # Simplemente regresamos el valor del contador de aristas
        return self.__num_aristas
    
    """
        Este método elimina todas las aristas de un nodo
        Parámetros
        ----------
        nodo: Nodo del cuál vamos a eliminar las aristas
    """
    def vaciar_nodo(self, nombre):
        # Se elimina cada arista en ambos sentidos
        nodo = self.buscar_nodo(nombre)
        if nodo:
            while self.__grafica[nodo]:
                self.eliminar_arista(nombre, self.__grafica[nodo][0].destino.nombre)
            return True
        else:
            return False
    """
        Este método limpia la gráfica
    """
    def vaciar_grafica(self):
        self.__grafica = {}
        self.__num_nodos = 0
        self.__num_aristas = 0
    
    """
        Este método imprime la gráfica en forma de lista.
        Primero aparecerán todos los nodos, después, todas
        las aristas
    """

    def copiar(self):
        return copy.deepcopy(self)
    
    def __limpiar_etiquetas(self, tipo):
        if tipo == "nodos":
            for nodo in self.__grafica:
                nodo.etiqueta = None
        elif tipo == "aristas":
            for nodo in self.__grafica:
                for arista in self.__grafica[nodo]:
                    arista.etiqueta = None
        elif tipo == "todo":
            for nodo in self.__grafica:
                nodo.etiqueta = None
                for arista in self.__grafica[nodo]:
                    arista.etiqueta = None
        else:
            raise ValueError(f"Error en el tipo dado ({tipo}). Valores aceptados: 'nodos', 'aristas', 'todos'")
            
    
    def es_bipartita(self):
        # if not self.es_conexa():
        #     return -1, -1
        # Cola auxiliar del algoritmo

        # Lista de los nodos que no han sido etiquetados por el algoritmos
        nodos_sin_etiqueta = [nodo for nodo in self.__grafica]
        
        cola = Cola()
        
        particion_1 = []
        particion_2 = []

        # Mientras existan nodos sin etiquetar se efectuará el algoritmo para encontrar
        # particiones en todas las componentes
        while nodos_sin_etiqueta:
            # Se obtiene el primer nodo de la gráfica
            nodo_inicial = nodos_sin_etiqueta.pop(0)

            # Lista en donde se almacenarán las particiones. Se agrega el primer nodo
            # automáticamente a la partición 1
            nodo_inicial.etiqueta = 1
            particion_1.append(nodo_inicial)
            
            # Se encola el primer nodo
            cola.encolar(nodo_inicial)

            # El algoritmo continúa mientras la cola no esté vacía. Si se termina exitosamente, 
            # entonces la gráfica es bipartita, de lo contrario terminará antes.
            while not cola.es_vacia():
                # Se desencola un vértice 
                nodo_actual = cola.desencolar()
                # Se decide hacia qué partición enviar a sus vecinos de acuerdo a la etiqueta
                # que el nodo desencolado tenga
                if nodo_actual.etiqueta == 1:
                    etiqueta = 2
                else:
                    etiqueta = 1
                # Se  agregan a la partición contraria  todos los vértices vecinos que no tengan
                # etiqueta. Si cumplen con esta condición, se encolan.
                # En caso de que tengan etiqueta y sea la misma que la del nodo actual, entonces
                # la gráfica no es bipartita
                for arista in self.__grafica[nodo_actual]:
                    nodo_vecino = arista.destino
                    if not nodo_vecino.etiqueta:
                        nodo_vecino.etiqueta = etiqueta
                        if etiqueta == 1:
                            particion_1.append(nodo_vecino)
                        else:
                            particion_2.append(nodo_vecino)
                            
                        cola.encolar(nodo_vecino)
                        nodos_sin_etiqueta.remove(nodo_vecino)

                    else:
                        if nodo_vecino.etiqueta == nodo_actual.etiqueta:
                            self.__limpiar_etiquetas("nodos")
                            return None, None
        
        self.__limpiar_etiquetas("nodos")
        return particion_1, particion_2

    def diccionario(self):
    	return self.__grafica
    
    def es_conexa(self):
        """
            Este método hace una búsqueda a lo profundo en cada nodo
            para saber si la gráfica es conexa
        """

        # Algoritmo de búsqueda
        visitados = []
        pila = Pila()
        try:
            pila.apilar(list(self.__grafica.items())[0][0])
        except:
            return True
        while not pila.es_vacia():
            nodo_actual = pila.desapilar()
            for arista in self.__grafica[nodo_actual]:
                nodo_adyacente = arista.destino
                if nodo_adyacente not in visitados:
                    pila.apilar(nodo_adyacente)
            if nodo_actual not in visitados:
                visitados.append(nodo_actual)

        # Si la gráfica es conexa, entonces todos los nodos deberían
        # estar presentes en la lista de visitados
        if len(visitados) == self.__num_nodos:
            return True
        else: 
            return False
    
    def imprimir_aristas(self):
        aristas = []
        for nodo in self.__grafica:
            for arista in self.__grafica[nodo]:
                aristas.append((arista.origen.nombre, arista.destino.nombre))

        print(aristas)        

    def paseo_euler(self):
        
        if not self.es_conexa():
            return -1

        nodos_iniciales = []
        copia = self.copiar().diccionario()
        
        # Se cuentan los nodos con grado impar
        for nodo in self.__grafica:
            if nodo.grado % 2 != 0:
                nodos_iniciales.append(nodo)
                
        if len(nodos_iniciales) > 0 and len(nodos_iniciales) != 2:
        	return False
        
        # Cola y pila del algoritmo
        cola = Cola()
        pila = Pila()
        
        # Si existen nodos iniciales, los tomamos (Paseo abierto desde vp a vc)
        if nodos_iniciales:
            vp = nodos_iniciales[0]
            vc = nodos_iniciales[1]
            
            
        else:
            vp = vc = list(self.__grafica.keys())[0]
        
        # Si no, tomamos por default el primer nodo (Paseo cerrado)
        cola.encolar(vc)
        pila.apilar(vp)
       
        while vp.grado>0 and vc.grado>0:
            # Si vc tiene aristas...
           
            if self.__grafica[vc]:
                # ... se elige cualquier arista (vc,w) tal que el grado de w no sea 1...
                arista_a_eliminar = None
                contador = 0
                for arista in self.__grafica[vc]:
                    contador+=1
                    if arista.destino.grado != 1 :
                        
                        arista_a_eliminar = arista
                        w = arista_a_eliminar.destino
                        id_arista = arista_a_eliminar.Id
                        self.eliminar_arista(vc.nombre, w.nombre)

                        # si un nodo queda con grado cero, lo eliminamos
                        if(vc.grado == 0):
                            self.eliminar_nodo(vc.nombre)
                        
                        # revisamos que el arco a eliminar no sea puente
                        # si solo hay un arco disponible, lo borramos aunque sea puente
                        if self.es_conexa() or vc.grado == contador:
                            break
                        else:
                            # en caso de que el arco sea puente, lo volvemos a agregar a la grafica
                            self.agregar_arista(vc.nombre, w.nombre)
                
                # ... si tal arista existe, eliminar (vc,w) de la gráfica y agregar w a la cola.
                # Hacer vc = w
                if arista_a_eliminar:
                    cola.encolar(w)
                    vc = w

            
            # Si vp tiene grado 1, elegir la única arista (vp, k), eliminar (vp, k) de la gráfica y
            # agregar ka a la pila. Hacer vp = k
            if vp.grado == 1:
                arista_a_eliminar = self.__grafica[vp][0]
                k = arista_a_eliminar.destino
                self.eliminar_arista(vp.nombre, k.nombre)
                # si el nodo queda con grado cero, lo eliminamos
                if(vp.grado == 0):
                            self.eliminar_nodo(vp.nombre)
                pila.apilar(k)
                vp = k
        
        # ---------- RECUPERAMOS EL PASEO ----------
        pila.desapilar() # Ignoramos el primero de la pila
        paseo = []

        # Se desencolan todos los vértices de la cola
        while(not cola.es_vacia()):
            paseo.append(cola.desencolar().nombre)
        
        # Se desapilan todos los vértices de la pila
        while not pila.es_vacia():
            paseo.append(pila.desapilar().nombre)
        
        # Restauramos la gráfica
        self.__grafica = copia

        return paseo
    

    """
        Esta función ejecuta una búsqueda a profundidad en la gráfica para encontrar árboles de
        expansión.
        Regresa
        -------
        bosque: lista de listas. Cada lista corresponde al árbol de expansión
                de una componente de la gráfica. Cada arista de los árboles
                de expansión se representan con una tupla.
    """
    def busqueda_a_profundidad(self):
        # Lista en donde se almacenarán los árboles de expansión para cada
        # componente de la gráfica
        bosque = [] 

        # Lista de los nodos que no han sido etiquetados por el algoritmo
        nodos_sin_etiqueta = [nodo for nodo in self.__grafica]

        # Pila auxiliar del algoritmo
        pila = Pila()
        

        # Mientras existan nodos sin etiquetar se efectuará el algoritmo de 
        # búsqueda
        while True:
            # ----- ALGORITMO DE BÚSQUEDA A PROFUNDIDAD -----
            
            arbol = []

            # Se toma el primer vértice y se etiqueta
            v = nodos_sin_etiqueta.pop()
            v.etiqueta = 1


            # Mientras falte algún nodo por etiquetar en la gráfica, el algoritmo de búsqueda 
            # continúa          
            while nodos_sin_etiqueta:
                # Se busca alguna arista válida de v, es decir, que su destino no esté etiquetado
                arista = None
                for a in self.__grafica[v]:
                    if not a.destino.etiqueta:
                        arista = a 
                        break
                
                # Si existe alguna arista válida, entonces se marca la arista y el otro
                # extremo; además se apila v y se hace v = w. Luego, se repite el algoritmo
                # hasta este punto
                if arista:
                    # Se obtiene w
                    w = arista.destino
                    # Se etiqueta la arista válida de v a w
                    arista.etiqueta = 1
                    # Se añade la arista al árbol. También necesitamos guardar el nodo de origen
                    # (en este caso, v) para identificar más rápido la arista en el árbol
                    arbol.append(arista)
                    # También se etiqueta la misma arista válida pero de w a v
                    arista.etiqueta = 1
                    # Se etiqueta w y se saca de los nodos sin etiqueta
                    w.etiqueta = 1
                    nodos_sin_etiqueta.remove(w)
                    # Se apila v
                    pila.apilar(v)
                    # Se hace v = w
                    v = w
                    continue
                # Si no existen aristas válidas y la pila tiene elementos, entonces
                # se desapila un elemento y se repite el algoritmo hasta este punto
                if not pila.es_vacia():
                    v = pila.desapilar()
                # Si la pila ya está vacía, continuar con la siguiente parte del algoritmo
                else:
                    break
            
            # Si el árbol de expansión no contiene aristas, significa que la componente actual está
            # formada de un solo vértice (v)
            if len(arbol) == 0:
                arbol.append(v)
            
            # Se añade el árbol al bosque
            bosque.append(arbol)

            # Si todos los nodos están etiquetados, entonces se termina
            if not nodos_sin_etiqueta:
                break
            
        
        # Se limpian las etiquetas del árbol y se regresa el bosque
        self.__limpiar_etiquetas("todo")

        return bosque


    """
        Esta función ejecuta una búsqueda a lo ancho en la gráfica para encontrar árboles de
        expansión.
        Regresa
        -------
        bosque: lista de listas. Cada lista corresponde al árbol de expansión
                de una componente de la gráfica. Cada arista de los árboles
                de expansión se representan con una tupla.
    """
    def busqueda_a_lo_ancho(self):
        # Lista en donde se almacenarán los árboles de expansión para cada
        # componente de la gráfica
        bosque = [] 

        # Lista de los nodos que no han sido etiquetados por el algoritmo
        nodos_sin_etiqueta = [nodo for nodo in self.__grafica if not nodo.etiqueta]


        # Cola auxiliar del algoritmo
        cola = Cola()


        # Mientras existan nodos sin etiquetar se efectuará el algoritmo de 
        # búsqueda
        while True:
            # ----- ALGORITMO DE BÚSQUEDA A LO ANCHO -----
            
            # Árbol en donde vamos a guardar el árbol de mínima expansión para la componente
            # actual
            arbol = []

            # Se elige un vértice no etiquetado, se etiqueta y se encola
            v = nodos_sin_etiqueta.pop()
            v.etiqueta = 1
            cola.encolar(v)

            # El algoritmo continúa mientras la cola no esté vacía y 
            # haya vértices sin marcar
            while not cola.es_vacia() and nodos_sin_etiqueta:
                # Se desencola un vértice t
                t = cola.desencolar()

                # Se marcan todas las aristas de t tal que su otro extremo w
                # no esté marcado; además, se encola a w
                for arista in self.__grafica[t]:
                    w = arista.destino
                    if not w.etiqueta:
                        # Se etiqueta el nodo
                        w.etiqueta = 1
                        # Se etiqueta la arista de v a w (arista) y también en sentido contrario
                        # (de w a v)
                        arista.etiqueta = 1
                        arista.etiqueta = 1
                        # Se añade la arista al árbol junto con su origen
                        arbol.append(arista)
                        # Se encola w y como ya está marcado, entonces se elimina de la lista de 
                        # nodos sin marcar
                        nodos_sin_etiqueta.remove(w)
                        cola.encolar(w)
            
            # Si el árbol de expansión no contiene aristas, significa que la componente actual está
            # formada de un solo vértice (v)
            if len(arbol) == 0:
                arbol.append(v)
            
            # Se añade el árbol al bosque
            bosque.append(arbol)

            # Si todos los nodos están etiquetados, entonces se termina
            if not nodos_sin_etiqueta:
                break

            cola.vaciar()
        
        # Se limpian las etiquetas del árbol y se regresa el bosque
        self.__limpiar_etiquetas("todo")

        return bosque

    def algoritmo_kruskal(self):
    	# Introducir todas las aristas a una lista
        aristas = []
        for nodo in self.__grafica:
            for arista in self.__grafica[nodo]:
                if not arista.etiqueta:
                    aristas.append(arista)
                    arista.etiqueta = 1
                    self.buscar_arista(arista.destino.nombre, nodo.nombre, arista.peso).etiqueta = 1

        
        # Ordenar las aristas de mayor a menor de acuerdo a su peso
        aristas.sort(key=lambda a:float(a.peso), reverse=True)
        
        # Inicializar la estructura Unión-Búsqueda
        unionBusqueda = UnionBusqueda([n for n in self.__grafica])
        
        # ----- ALGORITMO DE KRUSKAL -----
        # Arreglo en donde se almacenarán las aristas del árbol de mínima expansión
        arbol = [] 
        
        # El algoritmo se ejecuta hasta que el número de aristas del árbol
        # sea igual al númer de vértices - 1, además, deben existir aristas
        # no seleccionadas en caso de que la gráfica no sea conexa
        num_nodos = self.obtener_numero_nodos()
        while len(arbol) < num_nodos - 1 and aristas:
            # Obtenemos una arista
            arista = aristas.pop()
            # Se busca el padre de cada arista. Si tienen padres distintos, 
            # entonces no se formará un ciclo y por lo tanto se agregan al árbol
            # y se unen
            if unionBusqueda.busqueda(arista.origen) != unionBusqueda.busqueda(arista.destino):
                arbol.append(arista)                                
                unionBusqueda.union(arista.origen, arista.destino)
        
        
        arbol.sort(key=lambda a:float(a.peso))
        self.__limpiar_etiquetas("aristas")

        # Tomamos todos los nodos que no tengan aristas
        arbol = arbol + [n for n in self.__grafica if n.grado == 0]

        # Tomamos todos los nodos aislados que tengan solo ciclos
        nodos_aislados_con_ciclos = []
        for n in self.__grafica:
            if n.grado != 0:
                if n.grado / len(self.__grafica[n]) == 2:
                    nodos_aislados_con_ciclos.append(n)

        arbol = arbol + nodos_aislados_con_ciclos


        return arbol
    
    def algoritmo_prim(self):
        # Se obtienen todos los nodos sin etiqueta
        nodos_sin_etiqueta = [n for n in self.__grafica]
        # Se inicializa el bosque vacío
        bosque = []

        # Se buscarán árboles de mínima expansión mientras existan nodos sin etiqueta. Esto para
        # encontrar lo árboles de todas las componentes en caso de que la gráfica no sea conexa
        while nodos_sin_etiqueta:
            # Se inicializa la lista de nodos marcados
            nodos_marcados = []

            # Se obtiene un nodo inicial y se agrega a la lista de nodos marcados
            nodo_inicial = nodos_sin_etiqueta.pop()
            nodo_inicial.etiqueta = 1
            nodos_marcados.append(nodo_inicial)

            # Se inicializa el árbol de la componente actual
            arbol = []

            # El algoritmo debe ejecutarse mientras exista una arista válida
            while True:

                # Se inicializan las variables 
                peso_minimo = math.inf 
                arista_minima = None

                # Se recorren todas las aristas que iniciden en los nodos marcados, es decir, 
                # los que ya están dentro del árbol de expansión
                for nodo in nodos_marcados:
                    for arista in self.__grafica[nodo]:
                        # Si el peso de la arista es menor que el peso mínimo actual y el destino
                        # no tiene etiqueta, entonces esta arista es un candidato a arista mínima
                        if float(arista.peso) < peso_minimo and not arista.destino.etiqueta:
                            arista_minima = arista
                            peso_minimo = float(arista.peso)
                
                # Si al final existe una arista mínima se agrega al árbol
                if arista_minima:
                    arbol.append(arista_minima)
                    # Se agrega el nodo destino de la arista mínima a la lista de nodos marcados
                    arista_minima.destino.etiqueta = 1
                    nodos_marcados.append(arista_minima.destino)
                    # El nodo destino de la arista mínima se elimina de la lista de nodos sin etiqueta
                    nodos_sin_etiqueta.remove(arista_minima.destino)
                else:
                    break
            
            # Cuando ya no existe arista válida entonces hemos terminado de encontrar el árbol de
            # mínima expansión en la componente actual, por lo tanto, éste se agrega al bosque.
            arbol.sort(key=lambda a:float(a.peso))
            bosque.append(arbol)
        
        self.__limpiar_etiquetas("nodos")

        # Tomamos todos los nodos que no tengan aristas
        bosque[-1] += [n for n in self.__grafica if n.grado == 0]

        # Tomamos todos los nodos aislados que tengan solo ciclos
        nodos_aislados_con_ciclos = []
        for n in self.__grafica:
            if n.grado != 0:
                if n.grado / len(self.__grafica[n]) == 2:
                    nodos_aislados_con_ciclos.append(n)

        bosque[-1] += nodos_aislados_con_ciclos
        return bosque

    def dijkstra(self, origen, destino):
        X = []
        
        self.agregar_arista_digrafica(origen,origen,0)
        v = self.buscar_arista(origen,origen,0)
        X.append([v,0])
        Y = []
        minimo = -math.inf
        
        while(X):
            # ordenamos los aristas marcados temporalmente por peso
            X.sort(key=lambda x:float(x[1]), reverse=False)
            #agarramos el elemento de la lista con los aristas etiquetados temporalmente
            x = X[0]
            # lo sacamos de la lista de marcados temporal
            X.remove(X[0])
            # le ponemos etiqueta a la aristas
            x[0].destino.etiqueta="1"
            # lo agregamos a la lista de marcados permanentes
            Y.append(x)
            
            booleano=False
   
            # recorremos los aristas del nodo recien marcado de forma permanente
            for arista in self.__grafica[x[0].destino]: 
                booleano=False
                # checamos si el nodo destino de la arista está marcado permanentemente
                if(arista.destino.etiqueta != "1"):      
                    for nodo in X: # recorremos los nodos marcados temporalmente
                        # checamos si el nodo destino del arista recorrido ya está marcado temporalmente
                        if(nodo[0].destino == arista.destino): 
                            booleano=True
                            # comparamos pesos entre la etiqueta actual del nodo y la posible nueva etiqueta
                            if(nodo[1] > float(arista.peso)+x[1]):  
                                # actualizamos la etiqueta                      
                                nodo[0]=arista                                    
                                nodo[1]=float(arista.peso)+x[1] 
                    # si el nodo destino del arista no  estaba marcado, lo marcamos con etiqueta temporal.                                                              
                    if booleano==False:    
                        X.append([arista,float(arista.peso)+x[1]])

        # revisamos si todos nodos fueron marcados permanentemente
        if(len(Y)==len(self.__grafica)):
            # regresamos la lista con las etiquetas permanentes encontradass
            return Y
        else:
            return False


    def __str__(self):
        resultado = ""
        for nodo in self.__grafica:
            resultado += f"{nodo.nombre}: "
            for arista in self.__grafica[nodo]:
                resultado += f"({arista.destino.nombre}, {arista.peso}) "
            resultado += '\n'
        return resultado 