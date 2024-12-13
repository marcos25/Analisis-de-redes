from grafica import Grafica
from os import system, name
from grafica import Cola
from digrafica import *

def validar(num):
    try:
        int(num)
        return True
    except:
        return False
    

def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

g = Grafica()
g.leer_grafica("grafica.txt")
d = Digrafica()
d.leer_digrafica("digrafica.txt")
copia = Grafica()
seleccion = ""

while (seleccion != "23"):
    clear()
    print("Menu")
    print("1) Agregar arista")
    print("2) Agregar nodo")
    print("3) Eliminar nodo")
    print("4) Eliminar arista")
    print("5) Buscar nodo")
    print("6) Buscar arista")
    print("7) Obtener grado de un nodo")
    print("8) Obtener numero de nodos")
    print("9) Obtener numero de aristas")
    print("10) Vaciar un nodo")
    print("11) Vaciar grafica")
    print("12) Imprimir grafica")
    print("13) Copiar grafica")
    print("14) Ver copia de la grafica")
    print("15) Verificar si la grafica es bipartita")
    print("16) paseo euler")
    print("17) Busqueda a lo ancho")
    print("18) Busqueda a profundidad")
    print("19) Algoritmo de kruskal")
    print("20) Algoritmo de prim")
    print("21) Dijkstra general")
    print("22) Floyd")
    print("23) Salir")

    seleccion = input()
    if validar(seleccion):
        if (int(seleccion) < 1 or int(seleccion) > 23):
            input("Error. Opción inválida. Presione Enter para intentarlo de nuevo...")
        else:
            if (seleccion == "1"):
                error = True
                while(error):
                    naristas = input("Ingrese la cantidad de aristas que desea agregar: ")
                    if not (validar(naristas)):
                        input("Error. Ingrese un número. Presione enter para intentarlo de nuevo...")
                    else:
                        naristas = int(naristas)
                        error = False
                while (naristas >0):
                    nodo1 = input("Ingrese el nodo 1: ")
                    nodo2 = input("Ingrese el nodo 2: ")
                    etiqueta = input("Ingrese la etiqueta del arista: ")
                    if g.agregar_arista(nodo1, nodo2, etiqueta):
                        naristas = naristas - 1
                    else:
                        print(f"La arista ({nodo1}, {nodo2}, {etiqueta}) ya existe")
                input("\nAristas agregadas. Presione Enter para continuar...")

            if (seleccion == "2"):
                nodo = input("Ingrese el nombre del nodo: ")
                if g.agregar_nodo(nodo):
                    print("Nodo", nodo, "agregado")
                else:
                    print("El nodo", nodo, "ya existe")
                input("\nPresione Enter para continuar...")
                
                
            if (seleccion == "3"):
                nodo = input("Ingrese el nombre del nodo que desea eliminar: ")
                if g.eliminar_nodo(nodo):
                    print("Nodo", nodo, "eliminado")
                else:
                    print("El nodo", nodo, "no existe")
                
                input("\nPresione Enter para continuar...")
                
            if (seleccion == "4"):
                nodo1 = input("Nodo 1: ")
                nodo2 = input("Nodo 2: ")
                etiqueta = input("Etiqueta (Enter si desea omitirla): ")
                if etiqueta == "":
                    etiqueta = None

                if g.eliminar_arista(nodo1, nodo2, etiqueta):
                    print(f"Arista eliminada")
                else:
                    print(f"La arista no existe")
                
                input("\nPresione Enter para continuar...")
            
            if (seleccion == "5"):
                nodo = input("Ingrese el nombre del nodo: ")
                if g.buscar_nodo(nodo):
                    print("El nodo", nodo, "existe")
                else:
                    print("El nodo", nodo, "no existe")
                
                input("\nPresione Enter para continuar...")
                
            if (seleccion == "6"):
                nodo1 = input("Nodo 1: ")
                nodo2 = input("Nodo 2: ")
                etiqueta = input("Etiqueta (Enter si desea omitirla): ")
                if etiqueta == "":
                    etiqueta = None

                if (g.buscar_arista(nodo1, nodo2, etiqueta)):
                    print("La arista existe")
                else:
                    print("La arista no existe")
                
                input("\nPresione Enter para continuar...")
            
            if (seleccion == "7"):
                nodo = input("Ingrese el nombre del nodo: ")
                grado = g.obtener_grado(nodo)
                if type(grado) != bool:
                    print("El grado del nodo", nodo, "es:", grado)
                else:
                    print("El nodo", nodo, "no existe")
                        
                input("\nPresione Enter para continuar...")
                
            if (seleccion == "8"):
                print("La gráfica tiene", g.obtener_numero_nodos(), "nodos")
                input("\nPresione Enter para continuar...")
            
            if (seleccion == "9"):
                print("La gráfica tiene", g.obtener_numero_aristas(), "aristas")
                input("\nPresione Enter para continuar...")
                
            if (seleccion == "10"):
                nodo = input("Ingrese el nodo que desee vaciar: ")
                if g.vaciar_nodo(nodo):
                    print("El nodo", nodo, "se ha vaciado.")
                else:
                    print("El nodo", nodo, "no existe")
                        
                input("\nPresione Enter para continuar...")
                        
            if (seleccion == "11"):
                g.vaciar_grafica()
                print("La gráfica se ha vaciado.")
                input("\nPresione Enter para continuar...")
            
            if (seleccion == "12"):
                print(g)
                input("\nPresione Enter para continuar...")
            
            if (seleccion == "13"):
                copia = g.copiar()
                print("Gráfica copiada correctamente: ")
                print(copia)
                input("\nPresione Enter para continuar...")

            if (seleccion == "14"):
                print("Última copia guardada: ")
                print(copia)
                input("\nPresione Enter para continuar...")
                
            if (seleccion == "15"):         
                v1, v2 = g.es_bipartita()
                if v1:
                    print("\n")
                    print("La gráfica SÍ es bipartita :)")
                    print("Gráfica g: ")
                    print(g)
                    print("Conjuntos:")
                    print("V1")
                    print (v1)
                    print("V2")
                    print (v2)
                else:
                    print("Gráfica g: ")
                    print(g)
                    print("La gráfica NO es bipartita :(")

               
                input("\nPresione Enter para continuar...")

            if (seleccion == "16"):  
                paseo_euler = g.paseo_euler()
                if paseo_euler:
                    print("Se encontró el siguiente paseo de Euler:")
                    print(paseo_euler)
                else:
                    print("La gráfica no contiene paseos de Euler")
                
             
                input("\nPresione Enter para continuar...")
            
            if (seleccion == "17"):  
                bosque = g.busqueda_a_lo_ancho()
                if bosque:
                    print("Se encontraron los siguietens árboles de expansión:")
                    print(bosque)
                else:
                    print("La gráfica no contiene árboles de expansiór")
                
             
                input("\nPresione Enter para continuar...")

            if (seleccion == "18"):  
                bosque = g.busqueda_a_profundidad()
                if bosque:
                    print("Se encontraron los siguietens árboles de expansión:")
                    print(bosque)
                else:
                    print("La gráfica no contiene árboles de expansió")
                
             
                input("\nPresione Enter para continuar...")

            if (seleccion == "19"):  
                bosque = g.algoritmo_kruskal()
                if bosque:
                    print("Se encontraron los siguietens árboles de mininma expansión:")
                    print(bosque)
                else:
                    print("La gráfica no contiene árboles de minima expansión")
                
             
                input("\nPresione Enter para continuar...")
            
            if (seleccion == "20"):  
                bosque_prim = g.algoritmo_prim()
                if bosque_prim:
                    print("Se encontraron los siguietens árboles de mininma expansión:")
                    for arbol in bosque_prim:
                        for arista in arbol:
                            print(arista[0].nombre, arista[1].destino, arista[1].peso)
                        print("--------------------------")
                else:
                    print("La gráfica no contiene árboles de minima expansión")
                
             
                input("\nPresione Enter para continuar...")

            if (seleccion == "21"):  
                
                nodo1 = "a"
                nodo2 = "b"
                ruta_mas_corta = d.dijkstra_general(nodo1)


                if ruta_mas_corta:
                    if ruta_mas_corta[0]=='ciclo':
                        ruta_mas_corta.pop(0)
                        longitud_ciclo = ruta_mas_corta.pop(len(ruta_mas_corta)-1)
                        print("Se encontró un ciclo de longitud ",longitud_ciclo, " con los aristas: ")
                        for arco in ruta_mas_corta:
                            print("(",arco.origen.nombre,",",arco.destino.nombre,") ")
                    else:    
                        print(f"De {nodo1} hasta {nodo2}")
                        print("SOLUCION TEMPORAL")
                        for arco in ruta_mas_corta:
                            print(f"({arco.origen.nombre}, {arco.destino.nombre}, {arco.peso})")
                        print("--------------------")
                        print("DIKJSTRA GENERAL")
                        longitud_total = 0
                        for arco in ruta_mas_corta:
                            print(f"({arco.origen.nombre}, {arco.destino.nombre}, {arco.peso})")
                
                input("\nPresione Enter para continuar...")

            if (seleccion == "22"):  

                nodo = input("Ingrese el nombre del nodo que desea encontrar las rutas mas cortas: ")
                
                rutas = d.floyd(nodo)
                if rutas[len(rutas)-1][0] == 'ciclo':
                    print("Se encontró un ciclo negativo de longitud ",rutas[len(rutas)-1][1],' con los siguientes arcos: ')
                    for arco in rutas:
                        if(type(arco[0]) == Arco):
                            print('(',arco[0].origen.nombre,', ',arco[0].destino.nombre,')',end="")
                else: 
                    if (rutas):
                        arcos = d.arcos_floyd(rutas)
                        for arco in arcos:
                            print(arco.origen.nombre,arco.destino.nombre)
                    else:
                        print("Error")
             
                input("\nPresione Enter para continuar...")
                

    else:
        input("Error. Ingrese un número entre 1 y 23. Presione Enter para intentarlo de nuevo...")   
