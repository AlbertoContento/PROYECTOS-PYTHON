import threading
import time
import tkinter as tk
from tkinter import Tk
import tkinter as ttk
import json
import random
import webbrowser

class RelojDespertador:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto 8 - Reloj Despertador")
        self.root.geometry("350x300")
        #Cambiamos la imagen de favicon de la ventana
        self.root.iconbitmap("logo-python.ico")
        #Vamos a bloquear el tamaño de la pantalla con True/False o 0/1, que el usu no pueda modificarla
        self.root.resizable(0,0)#ancho y alto

        # Texto inicial
        self.texto1 = tk.Label(text="Ingresa la hora del despertador (HH:SS:SS)", font=("Arial", 12))
        self.texto1.place(x=10, y=10)
        
        #Texto para Hora
        self.texto_hora = tk.Label(text="Hora:", font=("Arial", 8))
        self.texto_hora.place(x=100, y=50)

        #Spinbox para Hora (00-23)
        self.hora = ttk.Spinbox(root, from_=0, to=23, width=2, font=("Arial", 14))
        self.hora.place(x=100, y=70)

        #Texto para Minutos
        self.texto_minutos = tk.Label(text="Minutos:", font=("Arial", 8))
        self.texto_minutos.place(x=146, y=50)

        #Spinbox para Minutos (00-59)
        self.minuto = ttk.Spinbox(root, from_=0, to=59, width=2, font=("Arial", 14))
        self.minuto.place(x=150, y=70)

        #Texto para Segundos
        self.texto_segundos = tk.Label(text="Segundos:", font=("Arial", 8))
        self.texto_segundos.place(x=195, y=50)

        #Spinbox para Segundos (00-59)
        self.segundo = ttk.Spinbox(root, from_=0, to=59, width=2, font=("Arial", 14))
        self.segundo.place(x=200, y=70)
        
        # Botón para comenzar
        self.boton_comprobar = tk.Button(root, text="Programar Alarma", command=self.programar_alarma)
        self.boton_comprobar.place(x=120, y=110)

        # Texto para mostrar si está sonando
        self.texto_sonando = tk.Label(text="", font=("Arial" , 12))
        self.texto_sonando.place(x=130, y=150)

        #Texto de hora actual
        self.hora_actual = tk.Label(text="", font=("Arial" , 12))
        self.hora_actual.place(x=100, y=200)
        self.mostrar_hora_actual()

        # Botón para reiniciar
        self.boton_reiniciar = tk.Button(root, text="Reiniciar", state="normal", command=self.reiniciar)
        self.boton_reiniciar.place(x=20, y=260)

        # Botón para salir (inicialmente deshabilitado)
        self.boton_salir = tk.Button(root, text="Salir", state="normal", command=self.salir)
        self.boton_salir.place(x=300, y=260)

    #Mostrar hora actual
    def mostrar_hora_actual(self):
        hora_actual = time.strftime("%H:%M:%S")
        self.hora_actual.config(text=f"Hora actual: {hora_actual}")
        self.root.after(1000, self.mostrar_hora_actual)  # Llama a la función cada 1 segundo

    # Función para configurar la hora correctamente con dos dígitos
    def configuracion_hora(self):
        hora = f"{int(self.hora.get()):02}"      # Formatea la hora a dos dígitos
        minuto = f"{int(self.minuto.get()):02}"  # Formatea los minutos a dos dígitos
        segundo = f"{int(self.segundo.get()):02}"  # Formatea los segundos a dos dígitos
        self.hora_programada = f"{hora}:{minuto}:{segundo}"  # Construye la hora final
        return self.hora_programada

    # Función para guardar título de canción y URL
    def guardar_cancion(self):
        with open("canciones.json", "r", encoding="utf-8") as file:
            datos = json.load(file)
            # Escoger un título y URL aleatorio
            cancion = random.choice(datos["videos"])
            self.titulo = cancion["titulo"]
            url = cancion["url"]
            print(self.titulo, url)
            return self.titulo, url

    #Mostrar Sonando
    def calcular_centro_sonando(self):
        print("Sonando")
        self.texto_sonando.update_idletasks()  # Asegurar que las dimensiones están actualizadas
        window_width = self.root.winfo_width()  # Ancho de la ventana
        text_width = self.texto_sonando.winfo_reqwidth()  # Ancho requerido del texto
        center_x = (window_width - text_width) // 3  # Cálculo para centrar horizontalmente
        self.texto_sonando.config(text=f"Sonando 🔊\n{self.titulo}")
        self.texto_sonando.place(x=center_x, y=150)  # Ajusta la posición X calculada

    #Programar Alarma
    def cambiar_textos_alarma(self):
        self.configuracion_hora()
        print(self.hora_programada)
        self.texto1.config(text=f"Alarma programada a las: {self.hora_programada}")
        self.texto1.place(x=55, y=10)

    #Programar Alarma
    def programar_alarma(self):
        print("Programar Alarma")
        titulo, url = self.guardar_cancion()
        # Iniciar el hilo que verificará la hora continuamente
        threading.Thread(target=self.verificar_alarma, args=(url,), daemon=True).start()
        # Deshabilitar el botón de programar alarma
        self.boton_comprobar.config(state="disabled")

    # Función para verificar la hora y ejecutar la alarma
    def verificar_alarma(self, url):
        while True:
            # Obtener la hora actua
            hora_actual = time.strftime("%H:%M:%S")
            print(hora_actual)
            self.configuracion_hora()
            print(self.hora_programada)
            # Obtener la hora programada
            if hora_actual == self.hora_programada:
                # Sonar la canción
                print("¡Hora de la alarma!")
                self.root.after(100, self.calcular_centro_sonando)
                self.sonar_cancion(url)  # Sonar la canción
                self.cambiar_textos_alarma() #CAmbiamos los textos
                break  # Detener el bucle después de que se ejecute la alarma
            time.sleep(1)  # Esperar 1 segundo antes de comprobar nuevamente
            if not self.root.winfo_exists():
                break#detener la ejecucion si la ventana se cierra
    
    #Sonar Cancion
    def sonar_cancion(self, url):
        print("Sonar Cancion")
        # Aquí deberías abrir el navegador con la URL de la canción
        webbrowser.open(url)
        # Pero como no puedo hacerlo, solo muestro un mensaje en consola
        print("Abriendo navegador con la canción...")

    #salir
    def salir(self):
        print("Salir")
        self.root.destroy()
        
    #reiniciar
    def reiniciar(self):
        print("Reiniciar")
        self.texto1.config(text="Ingresa la hora del despertador (HH:SS:SS)")
        self.texto1.place(x=10, y=10)
        self.hora.delete(0, tk.END)
        self.minuto.delete(0, tk.END)
        self.segundo.delete(0, tk.END)
        self.boton_comprobar.config(state="normal")
        self.texto_sonando.place_forget()  # Ocultar el widget temporalmente


if __name__ == "__main__":
    root = Tk()
    app = RelojDespertador(root)
    root.mainloop()