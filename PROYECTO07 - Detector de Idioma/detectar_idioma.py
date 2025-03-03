import tkinter as tk
from tkinter import Tk
from langdetect import detect


class DetectarIdioma:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto 7 - Detector de Idioma")
        self.root.geometry("450x400")
        #Cambiamos la imagen de favicon de la ventana
        self.root.iconbitmap("logo-python.ico")
        #Vamos a bloquear el tamaño de la pantalla con True/False o 0/1, que el usu no pueda modificarla
        self.root.resizable(0,0)#ancho y alto
        
        # Texto inicial
        self.texto1 = tk.Label(text="Ingresa el texto para detectar el idioma", font="bold")
        self.texto1.place(x=60, y=10)
        
        #Placeholder
        self.placeholder_text = tk.StringVar()
        self.placeholder_text.set("Escribe aqui el texto")
        
        # Entrada de texto
        self.input_texto = tk.Text(root, width=35, height=5, font=("Arial", 16))
        self.input_texto.place(x=10, y=60)
        
        # Resultado
        self.resultado = tk.Label(root, text="", font=("Arial", 20))
        self.resultado.place(x=20, y=275)
        
        # Botón para comenzar
        self.boton_comprobar = tk.Button(root, text="Comprobar Texto", command=self.detectar_idioma)
        self.boton_comprobar.place(x=175, y=200)

        # Botón para reiniciar
        self.boton_reiniciar = tk.Button(root, text="Reiniciar", state="normal", command=self.reiniciar)
        self.boton_reiniciar.place(x=85, y=350)

        # Botón para salir (inicialmente deshabilitado)
        self.boton_salir = tk.Button(root, text="Salir", state="normal", command=self.salir)
        self.boton_salir.place(x=320, y=350)

    #Detectar idioma
    def detectar_idioma(self):
        if self.input_texto.get(1.0, tk.END) == "":
            self.resultado.config(text="No hay texto para detectar")
            return
        print("Detectar idioma")
        texto = self.input_texto.get(1.0, tk.END)
        print(texto)
        detectado = detect(texto)
        print(detectado)
        nombre_idioma = self.traducir_idioma(detectado)          
        self.resultado.config(text="El idioma detectado es: " + nombre_idioma)

    #Conversion de codigos de idioma a nombre de idioma
    def traducir_idioma(self, idioma):
        idiomas = {
            "af": "Afrikáans",
            "al": "Albanés",
            "de": "Alemán",
            "sq": "Albanés",
            "am": "Amárico",
            "ar": "Árabe",
            "hy": "Armenio",
            "az": "Azerí",
            "eu": "Euskera",
            "bn": "Bengalí",
            "be": "Bielorruso",
            "my": "Birmano",
            "bs": "Bosnio",
            "bg": "Búlgaro",
            "km": "Camboyano",
            "ca": "Catalán",
            "ceb": "Cebuano",
            "ny": "Chichewa",
            "zh": "Chino (simplificado)",
            "zh-TW": "Chino (tradicional)",
            "si": "Cingalés",
            "ko": "Coreano",
            "co": "Corso",
            "ht": "Criollo haitiano",
            "hr": "Croata",
            "cs": "Checo",
            "da": "Danés",
            "sk": "Eslovaco",
            "sl": "Esloveno",
            "es": "Español",
            "eo": "Esperanto",
            "et": "Estonio",
            "tl": "Filipino",
            "fi": "Finlandés",
            "fr": "Francés",
            "fy": "Frisón",
            "gd": "Gaélico escocés",
            "gl": "Gallego",
            "cy": "Galés",
            "ka": "Georgiano",
            "el": "Griego",
            "gu": "Gujarati",
            "ha": "Hausa",
            "haw": "Hawaiano",
            "iw": "Hebreo",
            "hi": "Hindi",
            "hmn": "Hmong",
            "hu": "Húngaro",
            "ig": "Igbo",
            "id": "Indonesio",
            "en": "Inglés",
            "ga": "Irlandés",
            "is": "Islandés",
            "it": "Italiano",
            "ja": "Japonés",
            "jw": "Javanés",
            "kn": "Kannada",
            "kk": "Kazajo",
            "rw": "Kinyarwanda",
        }
        return idiomas.get(idioma, "Idioma no reconocido")

    #salir
    def salir(self):
        print("Salir")
        self.root.destroy()
        
    #reiniciar
    def reiniciar(self):
        print("Reiniciar")
        self.input_texto.delete(1.0, tk.END)
        self.resultado.config(text="")


if __name__ == "__main__":
    root = Tk()
    app = DetectarIdioma(root)
    root.mainloop()