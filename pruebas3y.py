from red import *
d = Red()
d.leer_red("red.txt")

costo  = d.metodo_simplex()
d.imprimir_arcos()
print("costo final: ", costo)





