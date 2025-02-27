#improtamos la funcion tkinter
from tkinter import *
import tkinter as tk
#improtamos funcion scrolledtext para insertar la caja de entrada de texto y poder abrir cuadro de dialogos
from tkinter import scrolledtext, filedialog, messagebox
#importamos Image para poner insertar imagenes
from PIL import Image, ImageTk
#importamos modulo ttk para poder usar botones 
from tkinter import ttk

#CREAMOS UN OBJETO PARA NUESTRO EDITOR DE TEXTO
class EditorTexto:
    def __init__(self, root):
        #Creamos titul
        root.title("Proyecto 4 - Editor de Texto")
        #Tamaño de ventana
        root.geometry("900x600")
        #Insertamos el favicon
        root.iconbitmap("../logo-python.ico")
        #Creamos una variable de nuestro menu
        self.menuEditor = Menu(root)
        root.config(menu=self.menuEditor)#menu va a ser nuestra varaible menu
        #Llamo a la funcion que me crea los botones con imganes
        self.agregar_botones_imagenes()
        
        #CREAMOS LA PARTE DE LA VENTANA PARA EL TEXTO
        self.entrada_texto = scrolledtext.ScrolledText(root, wrap=tk.WORD, height = 32, width = 80)#wrap para que las palabras no se corten
        self.entrada_texto.place(x=10, y=20)
        self.entrada_texto.config(undo=True, autoseparators=True)  # Habilitar la funcionalidad de deshacer/rehacer


        #Vamos a crear el Menu-Archivo
        archivoMenu = Menu(self.menuEditor, tearoff=0)#con tearoff=0 quitamos la linea de separacion que aparece por defecto
        #MENU-ARCHIVO
        archivoMenu.add_command(label="Nuevo", command=self.nuevo)
        archivoMenu.add_command(label="Abrir", command=self.abrir_archivo)
        archivoMenu.add_command(label="Guardar", command=self.guardar)
        archivoMenu.add_separator()#con esto agregamos una separacion entre opciones
        archivoMenu.add_command(label="Salir", command=self.salir)#Con command le damos una funcionalidad en este caso: quit= Salir
        
        #Vamos a crear el Menu-Editar
        editarMenu = Menu(self.menuEditor,tearoff=0)#con tearoff=0 quitamos la linea de separacion que aparece por defecto
        #MENU-EDITAR
        editarMenu.add_command(label="Deshacer", command=self.deshacer)
        editarMenu.add_command(label="Rehacer", command=self.rehacer)

        #Vamos a crear el Menu-Diseño
        diseñoMenu = Menu(self.menuEditor, tearoff=0)#con tearoff=0 quitamos la linea de separacion que aparece por defecto
        #MENU-DISEÑO
        diseñoMenu.add_command(label="Negrita", command=self.negrita)
        diseñoMenu.add_command(label="Subrayado", command=self.subrayado)
        diseñoMenu.add_command(label="Cursiva", command=self.cursiva)

        #CREAMOS Y AÑADIMOS AL MENU LAS OPCIONES DE ARCHIVO, EDITAR Y DISEÑO
        self.menuEditor.add_cascade(label="Archivo", menu=archivoMenu)
        self.menuEditor.add_cascade(label="Editar", menu=editarMenu)
        self.menuEditor.add_cascade(label="Diseño", menu=diseñoMenu)

    #FUCNION DE ARCHIVO: PARA RESETEAR LA VENTANA
    def nuevo(self):
        self.entrada_texto.delete(1.0, tk.END)
        self.entrada_texto.focus_set()

    #FUNCION DE ARCHIVO: PARA ABRIR UN ARCHIVO DE NUESTRO ORDENADOR
    def abrir_archivo(self):
        #mostramos un cuadro de dialogo para seleccionar un archivo .txt
        archivo_texto = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if archivo_texto:
            #leemos el contenido del archivo(lectura)
            with open(archivo_texto, 'r') as archivo:
                contenido = archivo.read()
            #borrar lo que habia en el scrolledtext
            self.entrada_texto.delete("1.0", tk.END)   
            #Insertar el contenido del archivo en el scrolledtext
            self.entrada_texto.insert(tk.END, contenido)
    #FUNCION DE ARCHIVO: PARA GUARDAR UN ARCHIVO EN NUESTRO ORDENADOR
    def guardar(self):
        #Mostrar el cuadro de diálogo para seleccionar la ubicacion y el nombre del archivo
        archivo_texto = filedialog.asksaveasfile(defaultextension=".txt")
        if archivo_texto:#obtenemos el contenido del scrolledtext
            contenido = self.entrada_texto.get("1.0", tk.END)
            #Obtener el nombre del archivo desce el objeto de archivo devuelto
            nombre_archivo = archivo_texto.name
            with open(nombre_archivo, 'w') as archivo:
                archivo.write(contenido)#escribir el contenido 

    #FUNCION DE EDITAR: PARA deshacer EL TEXTO
    def deshacer(self):
        self.entrada_texto.focus_set()
        self.entrada_texto.edit_undo()#Deshace la ultima accion en el scrolledtext
        root.update()#actualiza la interfaz grafica
    #FUNCION DE EDITAR: PARA rehacer EL TEXTO
    def rehacer(self):
        self.entrada_texto.focus_set()
        self.entrada_texto.edit_redo()#Rehace la ultima accion en el scrolledtext
        root.update()#actualiza la interfaz grafica

    #FUNCION DE DISEÑO: PARA deshacer EL TEXTO
    def negrita(self):
        self.entrada_texto.tag_configure("bold", font=('Arial', 12, 'bold'))#configuramos bold
        #Obtener el rango selecionado actualmente en entrada de texto
        inicio, fin = self.entrada_texto.tag_ranges(tk.SEL)#representa la seleccion en tkinter
        if inicio and fin:
            # Aplica el formato negrita al rango seleccionado
            self.entrada_texto.tag_add("bold", inicio, fin)#asignamos "bold" al rango de inicio y fin
    #FUNCION DE DISEÑO: PARA rehacer EL TEXTO
    def subrayado(self):
        self.entrada_texto.tag_configure("underline", font=('Arial', 12, 'underline'))#configuramos bold
        #Obtener el rango selecionado actualmente en entrada de texto
        inicio, fin = self.entrada_texto.tag_ranges(tk.SEL)#representa la seleccion en tkinter
        if inicio and fin:
            # Aplica el formato negrita al rango seleccionado
            self.entrada_texto.tag_add("underline", inicio, fin)#asignamos "bold" al rango de inicio y fin
    #FUNCION DE DISEÑO: PARA rehacer EL TEXTO
    def cursiva(self):
        self.entrada_texto.tag_configure("italic", font=('Arial', 12, 'italic'))#configuramos bold
        #Obtener el rango selecionado actualmente en entrada de texto
        inicio, fin = self.entrada_texto.tag_ranges(tk.SEL)#representa la seleccion en tkinter
        if inicio and fin:
            # Aplica el formato negrita al rango seleccionado
            self.entrada_texto.tag_add("italic", inicio, fin)#asignamos "bold" al rango de inicio y fin
    #FUNCION PARA SALIR
    def salir(self):
        texto_actual = self.entrada_texto.get("1.0", tk.END)
        if texto_actual != self.entrada_texto:
            # Si el texto ha cambiado, preguntar si se desea guardar
            response = messagebox.askyesnocancel("¿Desea guardar los cambios antes de salir?")
            if response is None:
                # Cancelar la acción de salir
                return#uso return para que salga de la funcion
            elif response:
                # Guardar antes de salir
                self.guardar()
        # Cerrar la aplicación
        self.root.destroy()

    #FUNCION PARA AGREGAR LOS BOTONES CON IMAGENES
    def agregar_botones_imagenes(self):
        #NUEVO
        # Carga la imagen .png y redimensiona según sea necesario
        imagen = Image.open("imagenes/nuevo.png")#abre la imagen y la carga en un objeto Image de PIL
        imagen = imagen.resize((30, 30), Image.LANCZOS)#con ANTIALIAS mejoramos la calidad
        imagen = ImageTk.PhotoImage(imagen)#Convierte el objeto Image en un objeto PhotoImage de tkinter
        #Crear boron de la imagen
        boton_nuevo = ttk.Button(root, image=imagen, command=self.nuevo)#creamos boton en root con la imagen
        boton_nuevo.image = imagen#Almacena la imagen para que python no la elimine de la memoria
        boton_nuevo.place(x=700, y=40)

        #ABRIR ARCHIVO
        # Carga la imagen .png y redimensiona según sea necesario
        imagen = Image.open("imagenes/abrir.png")#abre la imagen y la carga en un objeto Image de PIL
        imagen = imagen.resize((30, 30), Image.LANCZOS)#con ANTIALIAS mejoramos la calidad
        imagen = ImageTk.PhotoImage(imagen)#Convierte el objeto Image en un objeto PhotoImage de tkinter
        #Crear boron de la imagen
        boton_nuevo = ttk.Button(root, image=imagen, command=self.abrir_archivo)#creamos boton en root con la imagen
        boton_nuevo.image = imagen#Almacena la imagen para que python no la elimine de la memoria
        boton_nuevo.place(x=750, y=40)

        #GUARDAR
        # Carga la imagen .png y redimensiona según sea necesario
        imagen = Image.open("imagenes/guardar.png")#abre la imagen y la carga en un objeto Image de PIL
        imagen = imagen.resize((30, 30), Image.LANCZOS)#con ANTIALIAS mejoramos la calidad
        imagen = ImageTk.PhotoImage(imagen)#Convierte el objeto Image en un objeto PhotoImage de tkinter
        #Crear boton de la imagen
        boton_nuevo = ttk.Button(root, image=imagen, command=self.guardar)#creamos boton en root con la imagen
        boton_nuevo.image = imagen#Almacena la imagen para que python no la elimine de la memoria
        boton_nuevo.place(x=800, y=40)

        #DESHACER
        # Carga la imagen .png y redimensiona según sea necesario
        imagen = Image.open("imagenes/deshacer.png")#abre la imagen y la carga en un objeto Image de PIL
        imagen = imagen.resize((30, 30), Image.LANCZOS)#con ANTIALIAS mejoramos la calidad
        imagen = ImageTk.PhotoImage(imagen)#Convierte el objeto Image en un objeto PhotoImage de tkinter
        #Crear boron de la imagen
        boton_nuevo = ttk.Button(root, image=imagen, command=self.deshacer)#creamos boton en root con la imagen
        boton_nuevo.image = imagen#Almacena la imagen para que python no la elimine de la memoria
        boton_nuevo.place(x=750, y=90)

        #REHACER
        # Carga la imagen .png y redimensiona según sea necesario
        imagen = Image.open("imagenes/rehacer.png")#abre la imagen y la carga en un objeto Image de PIL
        imagen = imagen.resize((30, 30), Image.LANCZOS)#con ANTIALIAS mejoramos la calidad
        imagen = ImageTk.PhotoImage(imagen)#Convierte el objeto Image en un objeto PhotoImage de tkinter
        #Crear boron de la imagen
        boton_nuevo = ttk.Button(root, image=imagen, command=self.rehacer)#creamos boton en root con la imagen
        boton_nuevo.image = imagen#Almacena la imagen para que python no la elimine de la memoria
        boton_nuevo.place(x=750, y=140)

        #NEGRITA
        # Carga la imagen .png y redimensiona según sea necesario
        imagen = Image.open("imagenes/negrita.png")#abre la imagen y la carga en un objeto Image de PIL
        imagen = imagen.resize((30, 30), Image.LANCZOS)#con ANTIALIAS mejoramos la calidad
        imagen = ImageTk.PhotoImage(imagen)#Convierte el objeto Image en un objeto PhotoImage de tkinter
        #Crear boron de la imagen
        boton_nuevo = ttk.Button(root, image=imagen, command=self.negrita)#creamos boton en root con la imagen
        boton_nuevo.image = imagen#Almacena la imagen para que python no la elimine de la memoria
        boton_nuevo.place(x=700, y=190)

        #SUBRAYADO
        # Carga la imagen .png y redimensiona según sea necesario
        imagen = Image.open("imagenes/subrayar.png")#abre la imagen y la carga en un objeto Image de PIL
        imagen = imagen.resize((30, 30), Image.LANCZOS)#con ANTIALIAS mejoramos la calidad
        imagen = ImageTk.PhotoImage(imagen)#Convierte el objeto Image en un objeto PhotoImage de tkinter
        #Crear boron de la imagen
        boton_nuevo = ttk.Button(root, image=imagen, command=self.subrayado)#creamos boton en root con la imagen
        boton_nuevo.image = imagen#Almacena la imagen para que python no la elimine de la memoria
        boton_nuevo.place(x=750, y=190)

        #CURSIVA
        # Carga la imagen .png y redimensiona según sea necesario
        imagen = Image.open("imagenes/cursiva.png")#abre la imagen y la carga en un objeto Image de PIL
        imagen = imagen.resize((30, 30), Image.LANCZOS)#con ANTIALIAS mejoramos la calidad
        imagen = ImageTk.PhotoImage(imagen)#Convierte el objeto Image en un objeto PhotoImage de tkinter
        #Crear boron de la imagen
        boton_nuevo = ttk.Button(root, image=imagen, command=self.cursiva)#creamos boton en root con la imagen
        boton_nuevo.image = imagen#Almacena la imagen para que python no la elimine de la memoria
        boton_nuevo.place(x=800, y=190)

        #SALIR
        # Carga la imagen .png y redimensiona según sea necesario
        imagen = Image.open("imagenes/salir.png")#abre la imagen y la carga en un objeto Image de PIL
        imagen = imagen.resize((30, 30), Image.LANCZOS)#con ANTIALIAS mejoramos la calidad
        imagen = ImageTk.PhotoImage(imagen)#Convierte el objeto Image en un objeto PhotoImage de tkinter
        #Crear boron de la imagen
        boton_nuevo = ttk.Button(root, image=imagen, command=self.salir)#creamos boton en root con la imagen
        boton_nuevo.image = imagen#Almacena la imagen para que python no la elimine de la memoria
        boton_nuevo.place(x=750, y=240)

#Con esto le decimos que es el archivo main(principal de programa)
if __name__ == "__main__":
#Creamos la ventana y se la pasamos a nuestro objeto para configurarla dentro
    root = tk.Tk()
    #Creamos instancia para llamar a la clase AppEscrituraVeloz
    app = EditorTexto(root)
    #Dejamos que la venta este siempre abierta
    root.mainloop()