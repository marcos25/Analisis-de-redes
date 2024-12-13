from red import *
d = Red()
d.leer_red("red.txt")

visitados = []
fuentes = []
sumideros = []

fuentes.append('a')

sumideros.append('j')

costo = d.algoritmo_primal(fuentes,sumideros,30)
print("")
print("Flujo final:")
d.imprimir_arcos()

print("")
print("Costo final: ",costo)
