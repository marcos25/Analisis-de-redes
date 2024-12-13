import tkinter as tk
from tkinter import simpledialog

class Gui():
    def __init__(self):

        # ----- CREACIÓN DE LA PANTALLA PRINCIPAL -----
        self.root_w = 800 # Ancho de la pantalla principal
        self.root_h = 800 # Alto de la pantalla principal
        # Tamaño de la ventana principal
        self.root_size = f"{self.root_w}x{self.root_h}"
        self.root = tk.Tk() # Se crea la pantalla principal 
        # Se establece el tamaño de la pantalla principal
        self.root.geometry(self.root_size) 

        # ----- CREACIÓN DEL FRAME DE LOS BOTONES -----
        self.buttons_frame_padx = 50 # Padding x del frame de botones
        self.buttons_frame_pady = 5 # Padding y del frame de botones
        # Se crea el frame de los botones en la pantalla principal (root)
        # sin marco (bd=0)
        self.buttons_frame = tk.LabelFrame(self.root, bd=0) 
        # Se añade el frame de botones a la pantalla principal
        self.buttons_frame.pack(padx=self.buttons_frame_padx, pady=self.buttons_frame_pady)

        # ----- CREACIÓN DE LOS BOTONES DE  NODOS Y ARISTAS -----
        # Se añade el botón de nodos al frame de botones alineado a la izquierda
        self.nodes_button = tk.Button(self.buttons_frame, text="Gestionar nodos",
                                      command=self.nodesButtonClick)
        self.nodes_button.pack(side=tk.LEFT, padx=10)
        # Se añade el botón de aristas al framde de botones alienado a la derecha
        self.vertex_button = tk.Button(self.buttons_frame, text="Gestionar aristas",
                                       command=self.vertexButtonClick)
        self.vertex_button.pack(side=tk.RIGHT, padx=10)

        # ----- CREACIÓN DEL CANVAS -----
        self.canvas_w = 700 # Ancho del canvas
        self.canvas_h = 600 # Alto del canvas
        self.canvas_pady = 5 # Margen superior del canvas
        self.canvas_bg = "white" # Color de fondo del canvas
        # Se crea el canvas y se añade a la pantalla principal
        self.canvas = tk.Canvas(self.root, width=self.canvas_w, height=self.canvas_h, bg=self.canvas_bg)# Canvas: En donde se dibujará la gráfica
        self.canvas.pack(pady=self.canvas_pady)

        # ----- CREACIÓN DEL MENÚ DE GESTIÓN DE NODOS -----
        self.nodes_menu = tk.Menu(self.canvas, tearoff = 0)   
        self.nodes_menu.add_command(label ="Eliminar nodo", command=self.removeNode) 
        self.nodes_menu.add_command(label ="Renombrar nodo", command=self.renameNode) 


        self.node_r = 25# Radio de los nodos
        self.node_label = 1# Etiqueta automática de los nodos
        self.min_node_separation = 30# Minima separación que debe existir entre un nodo y otro
        self.drag_data = {"x":0, "y":0, "secure_x":0, "secure_y":0, "item":None} # Información del objeto arrastrado
        self.mouse_state = "" # Estado del mouse ("node", "vertex)
        self.element_selected = ""
        self.node_color ="cyan"

        self.rename_node_window_w = 250
        self.rename_mode_window_h = 100

        self.rename_node_window = None
        self.rename_node_input = None
        self.new_name_node = ""
        
        self.canvas.bind("<Button 1>", self.drawNode)
        self.canvas.bind("<Button 3>", self.onObjectClick)
        self.canvas.bind("<ButtonPress-2>", self.drag_start)
        self.canvas.bind("<B2-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-2>", self.drag_stop)

        self.root.mainloop()

    """
        Este método dibuja un nodo en la gráfica.
        El nodo se representará con un círculo y su etiqueta. Este círculo tendrá radio 'node_r' con 
        centro en la coordenada en donde el usuario dio click.
    """
    def drawNode(self,event):
        # Se obtienen las coordenadas del evento (del click)
        if self.mouse_state != "node":
            return

        x = event.x
        y = event.y
        # Se imprimen las coordenadas del evento (para pruebas)
        print(x,y)
        # Se llama a la variable global 'node_label' para poder modificarla desde aquí
        # Se verifica si se puede dibujar el nodo (círculo) sin que se salga del canvas
        if x-self.node_r >= 0 and x+self.node_r <= self.canvas_w and y-self.node_r >= 0 and y+self.node_r <= self.canvas_h:
            # Se verifica que el nuevo nodo no se traslape con otro existente
            overlapped_items = self.canvas.find_overlapping(x-self.node_r-self.min_node_separation, 
                            y-self.node_r-self.min_node_separation, x+self.node_r+self.min_node_separation, 
                            y+self.node_r+self.min_node_separation)
            if not overlapped_items:
                # Se crea el nodo y con el argumento 'tags' se indica que es un objeto del tipo nodo y su etiqueta
                self.canvas.create_oval(x-self.node_r, y-self.node_r, x+self.node_r, y+self.node_r, fill=self.node_color,
                                    tags=f"node {self.node_label}")
            # Se crea la etiqueta del nodo dentro de éste, con el argumento 'tags' también se indica que
            # es un objeto del tipo nodo y su etiqueta (esto porque también la etiqueta pertenece a dicho nodo)                      
                self.canvas.create_text(x,y, text=str(self.node_label), tags=f"node {self.node_label}")
                
                # Se actualiza la etiqueta del nodo
                self.node_label += 1
    
    """
        Este método detecta si hemos dado click derecho a algún elemento de la gráfica. Esto con el
        fin de desplegar un menú desde donde se podrá modificar el elemento seleccionado.
    """
    def onObjectClick(self, event):
        x, y = event.x, event.y
        # Se encuentra el item que ha sido seleccionado mediante un click. Para ello utilizamos el 
        # método 'find_overlapping' del objeto canvas. Se le dan las coordenadas de la esquina superior
        # izquierda y la esquina inferior derecha de un rectángulo. El método regresará el índice de
        # todos los objetos que el rectángulo dado llegue a tocar. En este caso le damos las coordenadas
        # de solo un punto para tener más precisión al momento de seleccionar elementos.
        item = self.canvas.find_overlapping(
            x, y, x, y)         
        
        # Si se seleccionó un item, entonces se obtienen sus etiquetas en forma de arreglo
        # para saber qué tipo de objeto es (nodo o arista) y además saber su nombre (en caso de que sea 
        # nodo) o su peso (en caso de que se trate de una arista)
        if item:     
            item_tag = self.canvas.itemcget(item, "tags").replace("current", "").strip()
            
            if not self.canvas.itemcget(item, "tags"):
            # Bloque de excepción en caso de que seleccionemos la nada
                try:
                    item = self.canvas.find_overlapping(x-self.node_r, y-self.node_r, x+self.node_r,
                           y+self.node_r)[1] 
                    item_tag = self.canvas.itemcget(item, "tags").replace("current", "").strip()

                except:
                    print("No se encontró elemento en la rebúsqueda")
                    return

            self.element_selected = item

            if "node" in item_tag and self.mouse_state=="node":
                self.nodes_menu.tk_popup(event.x_root, event.y_root)
                print("Nodo seleccionado:", item_tag)
    
    """
        Este método inicializa la información necesaria para poder arrastrar un objeto
    """
    def drag_start(self, event):
        print("----- DRAG BEGIN -----")
        # Se obtienen las coordenadas del click    
        x, y = event.x, event.y

        # Se identifica el elemento seleccionado con un overlapping sobre un solo punto
        # (por eso las coordenadas de las esquinas de la bounding box son iguales)
        selected_item = self.canvas.find_overlapping(
            x, y, x, y) 
        
        # Cuando seleccionamos exatamente la etiqueta de un nodo, la instrucción actual regresa una
        # etiqueta vacía, probablemente es un bug ya que en ese caso la etiqueta y el nodo están
        # exactamente en la misma posición y el programa no sabe qué etiqueta regresar. En este caso,
        # buscamos un objeto cercano hasta una distancia de r. El primero será la etiqueta, el segundo
        # el nodo, así que por eso tomamos el item[1]
        if not self.canvas.itemcget(selected_item, "tags"):
            # Bloque de excepción en caso de que seleccionemos la nada
            try:
                selected_item = self.canvas.find_overlapping(x-self.node_r, y-self.node_r, 
                                x+self.node_r, y+self.node_r)[1] 
            except:
                return
            
        #    print("NO SE ENCONTRÓ PERO AHORA ES:", selected_item)
        # En esta lista se almacenarán todos los objetos de interés, o sea, los que vamos a arrastrar.
        # Se identificarán por sus etiquetas.
        interest_objects = []

        # Se obtiene la etiqueta del item que seleccionamos. Si contiene la palabra "current"
        # se elimina junto con todos los espacios posibles.
        original_tag = self.canvas.itemcget(selected_item, "tags").replace("current", "").strip()

        # Se iteran todos los items del canvas
        for item in self.canvas.find_all():
            # De la misma forma que encontramos la etiqueta del item seleccionado, ahora 
            # se tomará la del item en cuestión
            this_tag = self.canvas.itemcget(item, "tags").replace("current", "").strip()

            print(f"Etiqueta del original: {original_tag}")
            print(f"Etiqueta del actual original: {this_tag}")
            print(f"Las etiquetas son iguales? {this_tag in original_tag}")
            print("\n----------------------------------")

            # Si las etiquetas son iguales, entonces se agrega a la lista de items de interés.
            # Hasta este momento solo tnenemos Nodos y su Etiqueta, por lo tanto, cuando el 
            # arreglo de regiones de interés tenga longitud 2 (nodo y su etiqueta) se rompe el ciclo 
            if this_tag == original_tag:
                interest_objects.append(item)
                if len(interest_objects) == 2:
                    break
        
        print(f"Items de interes: {interest_objects}")

        # Se actualiza el drag data con la información que recolectamos
        self.drag_data["item"] = interest_objects
        self.drag_data["x"] = x
        self.drag_data["y"] = y
        self.drag_data["secure_x"] = x
        self.drag_data["secure_y"] = y
    
    """
        Este método arrastra un conjunto de elementos de una posición a otra dentro del canvas
        siguiendo las restricciones de distancia mínima entre un nodo y otro diferente, además de 
        respetar el límite del canvas
    """
    def drag(self, event):
        # Se toma la posición hasta donde se ha arrastrado el moude
        x, y = event.x, event.y

        # Se calcula hasta dónde se movió el mouse
        delta_x = x - self.drag_data["x"]
        delta_y = y - self.drag_data["y"]
        
        # Se mueve cada item de interés (almacenado en drag_data["item"]) desde la posición en donde
        # estaba, hacia la nueva delta_x y delta_y
        # Además, se agrega un bloque de excepción en caso de que hayamos seleccionado la nada
        # y por lo tanto los items a mover sean None
        try:
            for item in self.drag_data["item"]:
                self.canvas.move(item, delta_x, delta_y)
                # Se actualiza la posición del objeto arrastrado
                self.drag_data["x"] = x
                self.drag_data["y"] = y
        except:
            return
    
    """
        Este método toma la decisión de mantener el elemento a la posición
        hacia la que se arrastró. Si se traslapa con otro elemento diferente, 
        entonces el elemento se regresa a su posición incial
    """
    def drag_stop(self, event):
        """End drag of an object"""
        print("Stoping dragging")
        
        # Se toma la posición actual de los objetos arrastrados 
        x, y = self.drag_data["x"], self.drag_data["y"]

        # Se identifican todos los elementos que están sobrepuestos de acuerdo a los límites de los
        # objetos arrastrados
        overlapped_items = self.canvas.find_overlapping(x-self.node_r-self.min_node_separation, 
                                                   y-self.node_r-self.min_node_separation, 
                                                   x+self.node_r+self.min_node_separation, 
                                                   y+self.node_r+self.min_node_separation)
                                                    
        
        overlapping = False # Bandera para indicar si existe un overlapping

        # Se toma la etiqueta de uno de los items arrastrados (recordemos que en drag_data["item"]
        # se guardan siempre 2 elementos y estos tienen la misma etiqueta)
        # Se agrega un bloque de excepción en caso de que hayamos seleccionado la nada para 
        # arrastrar y los items de interes sean nulos
        try:
            dragged_item = self.canvas.itemcget(self.drag_data["item"][0], "tags").replace("current", "").strip()
        except:
            return
        print("\n\n-----DRAG_STOP-----")
        print("Dragged item:", dragged_item, "\n")

        # Se revisan todos los elementos sobrepuestos 
        for overlapped in overlapped_items:
            # Se obtiene la etiqueta del item sobrepuesto actual
            overlapped_item = self.canvas.itemcget(overlapped, "tags").replace("current", "").strip()
            print("Overlapped item:", overlapped_item)

            # Si la etiqueta del objeto sobrepuesto es diferente a la del objeto arrastrado, etonces
            # hay overlapping y con uno es suficiente para no permitir que el elemento arrastrado se
            # quede en ese lugar
            if dragged_item != overlapped_item:
                print("*Overlapped with this")
                overlapping = True
                break
        
        out_of_bounds = False # Bandera para indicar si arrastramos el objeto fuera del canvas

        # Se revisa si la nueva posición es válida de acuerdo a los límites del canvas
        if x-self.node_r < 0 or x+self.node_r > self.canvas_w or y-self.node_r < 0 or y+self.node_r > self.canvas_h:
            print("Dragged out of canvas bounds")
            out_of_bounds = True

        # Si hay overlapping o se arrastró fuera del canvas, entonces todos los elementos que se 
        # movieron se regresan a su posición anterior (drag_data["secure_x"], drag_data["secure_y"])
        if overlapping or out_of_bounds:
            for item in self.drag_data["item"]:
                self.canvas.move(item, self.drag_data["secure_x"] - event.x, 
                self.drag_data["secure_y"] - event.y)
        else:
            print("Not overlapping nor out of bounds")
        
        # Se resetea la información de arrastre
        self.drag_data["item"] = None
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0
        self.drag_data["secure_x"] = 0
        self.drag_data["secure_y"] = 0
        
        print("Drag Stoped")
        print("\n\n-----")

    """
        Este método prepara todos los atributos al detectar un click sobre el
        botón de Gestión de Nodos
    """
    def nodesButtonClick(self):
        if self.nodes_button["state"] != "disabled":
            self.mouse_state = "node"
            self.nodes_button["state"] = "disabled"
            self.vertex_button["state"] = "normal"

    """
        Este método prepara todos los atributos al detectar un click sobre el
        botón de Gestión de Aristas 
    """
    def vertexButtonClick(self):
        if self.vertex_button["state"] != "disabled":
            self.mouse_state = "vertex"
            self.vertex_button["state"] = "disabled"
            self.nodes_button["state"] = "normal"
    
    """
        Este método elimina un nodo del canvas
    """
    def removeNode(self):
        # Se obtiene la etiqueta del elemento que seleccionamos con el click derecho al momento de 
        # que se  desplegó el menú de edición
        item = self.element_selected
        item_tag = self.canvas.itemcget(item, "tags").replace("current", "").strip()
            
        print("Intentando eliminar:", item_tag)

        # En este arreglo se van a guardar los elementos que conforman al objeto a eliminar
        # (nodo: círculo y etiqueta ; arista: línea y peso)
        elements_to_remove = []

        print("ANTES DE ELIMINAR", len(self.canvas.find_all()))
        
        # Se buscan los elementos que conforman el objeto que deseamos eliminar
        for item2 in self.canvas.find_all():
            # Se busca la etiqueta del item en cuestión y se normaliza
            this_tag = self.canvas.itemcget(item2, "tags").replace("current", "").strip()

            # Si las etiquetas son iguales, entonces se agrega a la lista de objetos a eliminar.
            # Hasta este momento solo tnenemos Nodos y su Etiqueta, por lo tanto, cuando el 
            # arreglo de regiones de interés tenga longitud 2 (nodo y su etiqueta) se rompe el ciclo 
            if this_tag == item_tag:
                elements_to_remove.append(item2)
                if len(elements_to_remove) == 2:
                    break
        
        # Se eliminan del canvas los elementos que conforman al objeto de interés
        for element in elements_to_remove:
            self.canvas.delete(element)
        
        # Se reestablece el atributo que guarda el nombre del elemento que seleccionamos
        self.element_selected = ""
        print("DESPUES DE ELIMINAR", len(self.canvas.find_all()))
    
    """
        Este metodo corresponde al botón de "Cancelar" al momento de renombrar un nodo 
    """
    def cancelRenameNode(self, event=None):
        # Se destruye la pantalla popup y se reestablece su valor al igual que con el campo
        # de texto y la variable que almacenaría el nuevo nombre del nodo
        self.rename_node_window.destroy() 
        self.rename_node_window = None 
        self.rename_node_input = None
        self.new_name_node = ""
    
    """
        Este metodo corresponde al botón de "OK" al momento de renombrar un nodo 
    """
    def okRenameNode(self, event=None):
        # Se obtiene el nuevo nombre
        self.new_name_node = self.rename_node_input.get()
        # Se destruye la pantalla popup y se reestablece su valor al igual que con el campo
        # de texto
        self.rename_node_window.destroy()
        self.rename_node_window = None
        self.rename_node_input = None

        # Se revisa si el usuario ingresó algún nombre
        if self.new_name_node != "":
            # Se obtiene la etiqueta del nodo seleccionado
            item_tag = self.canvas.itemcget(self.element_selected, "tags").replace("current", "").strip()
            # Se buscan los elementos que conforman el objeto que deseamos renombrar. Deben ser 2
            # (nodo y etiqueta), para ello creamos un contador
            edited_counter = 0
            for item2 in self.canvas.find_all():
                # Se obtiene la etiqueta del item en cuestión y se normaliza
                this_tag = self.canvas.itemcget(item2, "tags").replace("current", "").strip()

                # Si la etiqueta en cuestión es la misma que la del objeto seleccionado, entonces
                # debe edistarse
                if this_tag == item_tag:
                    # Si el objeto encontrado es la etiqueta del nodo, entonces se reemplaza el 
                    # texto anterior con el nuevo nombre. Además, se actualizan las tags del 
                    # objeto actual
                    if self.canvas.type(item2) == "text":
                        self.canvas.itemconfig(item2, text=self.new_name_node, tags="node "+self.new_name_node)
                        self.new_name_node = ""
                        edited_counter += 1
                    else:
                        # Si el objeto encontrado es el nodo, entonces nadmás se actualizan sus tags
                        self.canvas.itemconfigure(item2, tags="node "+self.new_name_node)
                        edited_counter += 1
                    # Si ya encontramos los dos elementos que corresponden al objeto seleccionado,
                    # entonces terminamos
                    if edited_counter == 2:
                        return
    
    """
        Con este método gestionamos la edición del nombre de un nodo
    """
    def renameNode(self):
        # Se obtiene la etiqueta del elemento que seleccionamos con el click derecho al momento de 
        # que se  desplegó el menú de edición
        item_tag = self.canvas.itemcget(self.element_selected, "tags").replace("current", "").strip()

        # Se crea la ventana para que el usuario escriba la etiqueta
        # en la posición en donde está el mouse
        self.rename_node_window = tk.Toplevel()
        self.rename_node_window.grab_set() # Se bloquea la pantalla principal
        self.rename_node_window.title("Renombrar nodo") # Se le pone un título a la pantalla
        # Se abre la ventana en la posición en donde tengamos el mouse
        self.rename_node_window.geometry("%dx%d+%d+%d" % (self.rename_node_window_w, 
                                         self.rename_mode_window_h, self.root.winfo_pointerx(), 
                                         self.root.winfo_pointery()))
        # Bindeamos la tecla 'Esc' para que de este modo también se pueda cerrar la pantalla
        self.rename_node_window.bind('<Escape>', self.cancelRenameNode)
        # Se añade un texto indicando la operación
        tk.Label(self.rename_node_window, text="Nueva etiqueta").pack()

        # Se añade el campo de texto para que el usuario escriba
        self.rename_node_input = tk.Entry(self.rename_node_window, justify="center")
        self.rename_node_input.place(x=25,y=25)
        # En el campo de texto se escribe el nombre actual del nodo
        self.rename_node_input.insert(tk.END, item_tag.split(" ")[1]) 
        self.rename_node_input.focus() # Se pone el cursor sobre este campo de texto
        # Bindeamos la tecla "Enter" para que de este modo también se pueda submitear la etiqueta
        self.rename_node_input.bind('<Return>', self.okRenameNode)
        self.rename_node_input.pack() # Se añade el campo de texto a la ventana

        # Se crea un frame para los botones de "OK" y "Cancelar"
        buttons_frame = tk.LabelFrame(self.rename_node_window, pady=20, bd=0) 
        buttons_frame.pack()

        # Se crean los botones de "OK" y "Cancelar" y se agregan a su frame con sus respectivos
        # comandos
        tk.Button(buttons_frame, text="OK", padx=35, command=self.okRenameNode).pack(side=tk.LEFT, padx=15)
        tk.Button(buttons_frame, text="Cancelar", command=self.cancelRenameNode).pack(side=tk.RIGHT,
                                                                                      padx=15)                                                       
        
        

gui = Gui()