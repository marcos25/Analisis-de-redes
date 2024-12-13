from red import *
d = Red()
d.leer_red("red.txt")

visitados = []
fuentes = []
sumideros = []

fuentes.append('a')

sumideros.append('j')

flujo = d.algoritmo_dual(fuentes,sumideros,30)
print("")
print("Flujo final:")
d.imprimir_arcos()

print("")
print("costo final de la red: ",flujo)        



