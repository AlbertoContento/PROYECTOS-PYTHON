import tkinter as tk
from tkinter import Tk
import urllib.request
import urllib.error

import requests


class ComprobarSitiosWeb:
  def __init__(self, root):
    self.root = root
    self.root.title("Proyecto 4 - Comprobador de Sitios Web")
    self.root.geometry("450x400")
    #Cambiamos la imagen de favicon de la ventana
    self.root.iconbitmap("logo-python.ico")
    #Vamos a bloquear el tamaño de la pantalla con True/False o 0/1, que el usu no pueda modificarla
    self.root.resizable(0,0)#ancho y alto
    #Vamos a cambiarle el background y el cursor
    self.root.config(bg="aquamarine", cursor="pirate")

    # Texto inicial
    self.texto1 = tk.Label(text="Ingresa el sitio Web a comprobar", font="bold")
    self.texto1.place(x=60, y=10)

    #Placeholder
    self.placeholder_text = tk.StringVar()
    self.placeholder_text.set("Escribe aqui la URL")
    # Entrada de texto
    self.input_texto = tk.Entry(root, textvariable=self.placeholder_text, width=35, font=("Arial", 16))
    self.input_texto.place(x=10, y=60)

    #Manejar el evento de hacer click en el Entry
    self.input_texto.bind("<FocusIn>", self.borrar_placeholder)

    # Resultado
    self.resultado = tk.Label(root, text="", font=("Arial", 18))
    self.resultado.place(x=70, y=200)

    # Botón para comenzar
    self.boton_comprobar = tk.Button(root, text="Comprobar URL", command=self.comprobar_url)
    self.boton_comprobar.place(x=80, y=120)

    # Botón para descargar imagen
    self.boton_descargar = tk.Button(root, text="Descargar Imagen") #command=lambda: self.descargar_imagen(self.input_texto.get().strip()))
    self.boton_descargar.place(x=300, y=120)

    # Botón para reiniciar
    self.boton_reiniciar = tk.Button(root, text="Reiniciar", state="normal", command=self.reiniciar)
    self.boton_reiniciar.place(x=85, y=280)

    # Botón para salir (inicialmente deshabilitado)
    self.boton_salir = tk.Button(root, text="Salir", state="normal", command=self.salir)
    self.boton_salir.place(x=310, y=280)

  #Borrar el placeholder
  def borrar_placeholder(self, event):
    self.placeholder_text.set("")

  #salir
  def salir(self):
    self.root.destroy()
    
  #reiniciar
  def reiniciar(self):
    self.input_texto.delete(0, tk.END)
    self.resultado.config(text="")
    self.boton_reiniciar.config(state="disabled")
    self.boton_salir.config(state="disabled")

  # Comprobación de URL
  def comprobacion_url(self, url):
      # Comprobamos si la URL está vacía
      if not url:
          self.resultado.config(text="Debes ingresar una URL")
          return None  # Salir de la función si la URL está vacía

      # Añadir "http://" si no tiene protocolo (http o https)
      if not url.startswith(("http://", "https://")):
          url = f"http://{url}"

      # Añadir "www." si no lo tiene
      if not url.startswith("http://www.") and not url.startswith("https://www."):
          if "://" in url:
              url = url.replace("://", "://www.")  # Insertar www después del protocolo
          else:
              url = f"http://www.{url}"  # Si no tiene protocolo, añadir http://www.

      # Comprobar si la URL ya tiene un sufijo válido
      if not any(url.endswith(suffix) for suffix in [".com", ".org", ".es", ".net", ".edu", ".gov"]):
          url = f"{url}.com"  # Si no tiene sufijo de dominio, por defecto añadir .com

      return url  # Devuelve la URL modificada

  # Comprobar URL
  def comprobar_url(self):
      url = self.input_texto.get().strip()  # Eliminar espacios extra
      self.boton_reiniciar.config(state="normal")
      self.boton_salir.config(state="normal")
      
      # Asegúrate de que la URL está correctamente formada
      url = self.comprobacion_url(url)
      
      if url is None:
          return  # Salir si la URL es inválida o vacía

      try:
          # Realizamos la solicitud GET
          with urllib.request.urlopen(url) as response:
              if response.status == 200:
                  self.resultado.config(text="El sitio Web está en línea")
              else:
                  self.resultado.config(text="El sitio Web no está en línea")
      except urllib.error.URLError as e:
          # Capturamos errores de conexión, como un fallo de DNS o no disponible
          self.resultado.config(text="El sitio Web no está en línea")
      except urllib.error.HTTPError as e:
          # Capturamos errores HTTP, como una página no encontrada
          self.resultado.config(text="El sitio Web no está en línea")
      except Exception as e:
          # Capturamos cualquier otro error
          self.resultado.config(text="El sitio Web no está en línea")

# # Descargar Imagen
# def descargar_imagen(self, url):
#     url = self.input_texto.get().strip()  # Obtener URL
#     self.boton_reiniciar.config(state="normal")
#     self.boton_salir.config(state="normal")

#     # Verificar si la URL es válida
#     if not url:
#         self.resultado.config(text="Debes ingresar una URL")
#         return

#     self.comprobacion_url(url)  # Comprobar URL formateada correctamente
    
#     try:
#         # Realizamos la solicitud para obtener los encabezados
#         response = requests.head(url)  # Utilizamos HEAD para obtener solo los encabezados
#         content_type = response.headers.get('Content-Type')

#         # Verificar si el tipo de contenido es imagen
#         if content_type and content_type.startswith('image'):
#             # Descargar la imagen si el tipo de contenido es adecuado
#             urllib.request.urlretrieve(url, "imagenes/imagen_descargada.jpg")
#             self.resultado.config(text="Imagen descargada correctamente")
#         else:
#             self.resultado.config(text="La URL no apunta a una imagen válida")
    
#     except requests.exceptions.RequestException as e:
#         self.resultado.config(text="Error al descargar la imagen: {}".format(e))

if __name__ == "__main__":
    root = Tk()
    app = ComprobarSitiosWeb(root)
    root.mainloop()