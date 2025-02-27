import sys
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import newspaper
from gtts import gTTS
import pygame
import os


# Instalar dependencias condicionalmente
def instalar_dependencias():
    try:
        # Definir las dependencias necesarias
        dependencias = ['gTTs', 'pygame']  # Asegúrate de agregar cualquier otra dependencia

        for dep in dependencias:
            try:
                __import__(dep)
            except ImportError:
                print(f"Instalando {dep}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
    except Exception as e:
        print(f"Error al intentar instalar dependencias: {e}")

instalar_dependencias()

def convert_article_to_audio(entrada_texto, var_opcion_txt_url, var_opcion_idioma, var_opcion_voz):
    """Convierte texto o contenido de una URL a un archivo de audio y lo reproduce."""
    try:
        if var_opcion_txt_url == "URL":
            url = entrada_texto.get("1.0", tk.END).strip()
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            article = newspaper.Article(url)
            article.download()
            article.parse()
            texto = article.text
        else:
            texto = entrada_texto.get("1.0", "end-1c").strip()
            if not texto:
                raise ValueError("NO HAS ESCRITO NADA")
        
        var_idioma_voz = convertir_voz_idioma(var_opcion_idioma, var_opcion_voz)
        voz = gTTS(text=texto, lang=var_idioma_voz)
        audio_file = 'audios/audio_texto.mp3'
        
        # Si el archivo ya existe y está en uso, lo liberamos antes de sobrescribirlo
        if os.path.exists(audio_file):
            try:
                pygame.mixer.quit()
                os.remove(audio_file)
            except PermissionError:
                raise PermissionError("Cierra el audio antes de generar uno nuevo.")
        
        voz.save(audio_file)
        
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
    except Exception as e:
        messagebox.showerror("¡ERROR!", message=str(e))
        return None
    return audio_file

def convertir_voz_idioma(var_opcion_idioma, var_opcion_voz):
    """Devuelve el código del idioma y voz según las opciones elegidas."""
    idiomas = {
        ("Ingles", "Masculina"): "en-GB",
        ("Ingles", "Femenina"): "en-GB",
        ("Español", "Masculina"): "es-ES",
        ("Español", "Femenina"): "es-ES",
    }
    return idiomas.get((var_opcion_idioma, var_opcion_voz), "es-ES")

def salir():
    """Cierra la aplicación."""
    ventana.destroy()

ventana = tk.Tk()
ventana.title("Proyecto 1 - Texto a Voz")
ventana.geometry("400x400")
ventana.iconbitmap("../logo-python.ico")

titulo = tk.Label(ventana, text="CONVERSOR DE TEXTO A VOZ", bg="green")
titulo.pack(fill=tk.X)

opcion_txt_url_label = tk.Label(text="Elige una opción:")
opcion_txt_url_label.pack()
var_opcion_txt_url = tk.StringVar()
desplegable_txt_url = ttk.Combobox(textvariable=var_opcion_txt_url, values=["Texto", "URL"])
desplegable_txt_url.pack()

entrada_texto_label = tk.Label(text="Ingresa el texto o URL:")
entrada_texto_label.pack()
entrada_texto = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, height=10, width=50)
entrada_texto.pack()

opcion_idioma = tk.Label(text="Elige el idioma:")
opcion_idioma.place(x=45, y=255)
var_opcion_idioma = tk.StringVar()
desplegable_idioma = ttk.Combobox(textvariable=var_opcion_idioma, values=["Ingles", "Español"])
desplegable_idioma.place(x=20, y=280)

opcion_voz = tk.Label(text="Elige el tipo de voz:")
opcion_voz.place(x=260, y=255)
var_opcion_voz = tk.StringVar()
desplegable_voz = ttk.Combobox(textvariable=var_opcion_voz, values=["Masculina", "Femenina"])
desplegable_voz.place(x=240, y=280)

boton_reproducir = tk.Button(ventana, text="Reproducir", padx=15, pady=5,
command=lambda: convert_article_to_audio(entrada_texto, var_opcion_txt_url.get(),
var_opcion_idioma.get(), var_opcion_voz.get()))
boton_reproducir.place(x=150, y=310)

boton_salir = tk.Button(ventana, text="Salir", padx=10, pady=3, command=salir)
boton_salir.place(x=320, y=350)

if __name__ == "__main__":
    ventana.mainloop()
