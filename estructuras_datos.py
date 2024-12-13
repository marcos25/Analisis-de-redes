class Cola:
    """ Representa a una cola, con operaciones de encolar y desencolar.
        El primero en ser encolado es también el primero en ser desencolado.
    """

    def __init__(self):
        """ Crea una cola vacía. """
        # La cola vacía se representa por una lista vacía
        self.items=[]

    def imprimir_cola(self):
        for i in range(len(self.items)):
            print(self.items[i])

    def encolar(self, x):
        """ Agrega el elemento x como último de la cola. """
        self.items.append(x)
    def es_vacia(self):
        """ Devuelve True si la cola esta vacía, False si no."""
        return self.items == []
      
    def desencolar(self):
        """ Elimina el primer elemento de la cola y devuelve su
        valor. Si la cola está vacía, levanta ValueError. """
        try:
            return self.items.pop(0)
        except:
            raise ValueError("La cola está vacía")
    
    def vaciar(self):
        self.items = []
        

#----------------------------------------------------------------
class Pila:
    """ Representa una pila con operaciones de apilar, desapilar y
        verificar si está vacía. """

    def __init__(self):
        """ Crea una pila vacía. """
        # La pila vacía se representa con una lista vacía
        self.items=[]
        
    def apilar(self, x):
        """ Agrega el elemento x a la pila. """
        # Apilar es agregar al final de la lista.
        self.items.append(x)

    def es_vacia(self):
    	return self.items == []

    def desapilar(self):
        """ Elimina el primer elemento de la cola y devuelve su
        valor. Si la cola está vacía, levanta ValueError. """
        try:
            return self.items.pop()
        except:
            raise ValueError("La cola está vacía")
    
    def vaciar(self):
        self.items = []
#----------------------------------------------------------------
class UnionBusqueda:
    def __init__(self, vertices):
        self.__items = {}
        for v in vertices:
            self.__items[v] = v
    
    def busqueda(self, v):
        if (v == self.__items[v]):
            return v
        return self.busqueda(self.__items[v])
    
    def union(self, u, v):
        self.__items[self.busqueda(u)] = self.busqueda(v)