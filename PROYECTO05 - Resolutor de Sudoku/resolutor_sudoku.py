import json
import random
import subprocess
import sys
import pygame
import time

# Instalar dependencias condicionalmente
def instalar_dependencias():
    try:
        # Definir las dependencias necesarias
        dependencias = ['pygame']  # Asegúrate de agregar cualquier otra dependencia

        for dep in dependencias:
            try:
                __import__(dep)
            except ImportError:
                print(f"Instalando {dep}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
    except Exception as e:
        print(f"Error al intentar instalar dependencias: {e}")

instalar_dependencias()

#DEFINICION DE VARIABLES PARA TABLERO
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 240, 255)
ROJO_OSCURO = (178, 34, 34)  # Rojo oscuro
ROJO_CLARO = (255, 69, 69)  # Rojo más claro al hacer hover
tablero_actual = None

#CVONFIGURACION DE PANTALLA
ANCHO = 596
ALTO = 750

# Creo con pygame la ventana de 600x600
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('SUDOKU')

#Fuente
fuente = pygame.font.Font(None, 36)

#CREACION DE TABLERO
def creacion_tablero():
  #Dibujamos el tablero
  for i in range(0, 601, 198):
    pygame.draw.line(pantalla, NEGRO, (i, 0), (i, ANCHO), 4)
    pygame.draw.line(pantalla, NEGRO, (0, i), (ANCHO, i), 4)
    for i in range(0, 601, 66):
      pygame.draw.line(pantalla, NEGRO, (i, 0), (i, ANCHO), 2)
      pygame.draw.line(pantalla, NEGRO, (0, i), (ANCHO, i), 2)
  pygame.display.flip()
  time.sleep(0.1) 

#CREACION DE BOTON EMPEZAR
def creacion_boton_empezar():
  # Definir coordenadas y tamaño del botón
  boton_x, boton_y, boton_ancho, boton_alto = 100, 602, 110, 50
  # Dibujar el botón (rectángulo)
  pygame.draw.rect(pantalla, ROJO_OSCURO, (boton_x, boton_y, boton_ancho, boton_alto), 50)
  # Crear la fuente y renderizar el texto
  texto_boton = fuente.render("Empezar", True, BLANCO)
  # Obtener el tamaño del texto
  text_rect = texto_boton.get_rect(center=(boton_x + boton_ancho // 2, boton_y + boton_alto // 2))
  # Dibujar el texto centrado
  pantalla.blit(texto_boton, text_rect)
  # Actualizar la pantalla
  pygame.display.flip()
  time.sleep(0.1)

#CREACION DE BOTON REINICIAR
def creacion_boton_reiniciar():
  # Definir coordenadas y tamaño del botón
  boton_x, boton_y, boton_ancho, boton_alto = 400, 602, 110, 50
# Dibujar el botón (rectángulo)
  pygame.draw.rect(pantalla, ROJO_CLARO, (boton_x, boton_y, boton_ancho, boton_alto), 50)
  # Crear la fuente y renderizar el texto
  texto_boton = fuente.render("Reiniciar", True, BLANCO)
    # Obtener el tamaño del texto
  text_rect = texto_boton.get_rect(center=(boton_x + boton_ancho // 2, boton_y + boton_alto // 2))
  # Dibujar el texto centrado
  pantalla.blit(texto_boton, text_rect)
  # Actualizar la pantalla
  pygame.display.flip()
  time.sleep(0.1)

#Creacion de boton salir 
def creacion_boton_salir():
  # Definir coordenadas y tamaño del botón
  boton_x, boton_y, boton_ancho, boton_alto = 270, 602, 70, 50
  # Dibujar el botón (rectángulo)
  pygame.draw.rect(pantalla, NEGRO, (boton_x, boton_y, boton_ancho, boton_alto), 50)
  # Crear la fuente y renderizar el texto
  texto_boton = fuente.render("Salir", True, BLANCO)
  # Obtener el tamaño del texto
  text_rect = texto_boton.get_rect(center=(boton_x + boton_ancho // 2, boton_y + boton_alto // 2))
  # Dibujar el texto centrado
  pantalla.blit(texto_boton, text_rect)
  # Actualizar la pantalla
  pygame.display.flip()
  time.sleep(0.1)

#CREACION BOTONES NIVELES
def niveles():
  texto_niveles = fuente.render("Niveles", True, BLANCO)
  pantalla.blit(texto_niveles, (ANCHO // 2 - 60, 20))
  niveles = {
    "Fácil" : pygame.Rect(50, 698, 80, 50),
    "Medio" : pygame.Rect(260, 698, 80, 50), 
    "Difícil" : pygame.Rect(500, 698, 80, 50)
  }
  for nivel, rect in niveles.items():
    pygame.draw.rect(pantalla, AZUL, rect, 50)
    texto_nivel = fuente.render(nivel, True, BLANCO)
    text_rect = texto_nivel.get_rect(center=rect.center)
    pantalla.blit(texto_nivel, text_rect)#DIBUJAR TEXTO
  pygame.display.flip()#REFRESCAR PANTALLA
  return niveles

#FUNCION BORRA BOTONES NIVELES
def borrar_botones_niveles():
  #borrar boton facil
  pygame.draw.rect(pantalla, BLANCO, (50, 698, 80, 50))
  #borrar boton medio
  pygame.draw.rect(pantalla, BLANCO, (260, 698, 80, 50))
  #borrar boton dificil
  pygame.draw.rect(pantalla, BLANCO, (500, 698, 80, 50))

#LEER ARCHIVO TABLEROS
def leer_tableros():
  with open("tableros_sudoku.json", "r") as archivo:
    tableros = json.load(archivo)
  return tableros

#RESOLVER SUDOKU
def resolver_sudoku(tablero):
  for i in range(0,9):
    for j in range(0,9):
      if tablero[i][j] == 0:
        for n in range(1,10):
          if numero_valido(tablero,i,j,n):
            tablero[i][j]=n
            #backtraking
            if resolver_sudoku(tablero):
              return True
            tablero[i][j]=0#si no es valido deshacer el cambios
        return False
  #Se completo el sudoku
  return True

#VALIDAR NUMERO
def numero_valido(tablero,i,j,n):
  fila=tablero[i]
  columna = [tablero[x][j] for x in range(9)]
  if n in fila or n in columna:
    return False
  else:
    subcuadrícula_fila = (i // 3) * 3  # Determinar la fila de la subcuadrícula
    subcuadrícula_columna = (j // 3) * 3  # Determinar la columna de la subcuadrícula
    for a in range(subcuadrícula_fila, subcuadrícula_fila + 3):
      for b in range(subcuadrícula_columna, subcuadrícula_columna + 3): 
        if tablero[a][b] == n:
          return False
    return True

#SUDOKU RESUELTO
def sudoku_resuelto(tablero):
  for i in range(0,9):
    for j in range(0,9):
      if tablero[i][j]==0:
        return False
  return True

#MOSTRAR NUMEROS
def mostrar_numeros(tablero):
  borrar_mostrar_numeros(tablero)
  for fila in range(9):
    for columna in range(9):
      numero = tablero[fila][columna]
      if numero != 0:
        texto = fuente.render(str(numero), True, NEGRO)
        # Calcular la posición para centrar el número en el recuadro
        pos_x = columna * 66 + 33 - texto.get_width() // 2
        pos_y = fila * 66 + 33 - texto.get_height() // 2
        pantalla.blit(texto, (pos_x, pos_y))

#FUNCIONA BORRAR NUMEROS
def borrar_mostrar_numeros(tablero):
    for fila in range(9):
        for columna in range(9):
            # Sobreescribir el contenido de la celda con el color de fondo
            pygame.draw.rect(pantalla, BLANCO, (columna * 66 + 1, fila * 66 + 1, 64, 64)) 
    pygame.display.flip()  # Refrescar la pantalla

#MOSTRAS SOLUCION
def mostrar_solucion(tablero):
    if resolver_sudoku(tablero):  # Intentar resolver antes de verificar
        print("Sudoku Resuelto")
        mostrar_numeros(tablero)  # Actualizar la pantalla con la solución
        mostrar_mensaje_resuelto()
    else:
        print("No se puede resolver el sudoku")

#VER COMO VA RESOLVIENDO EL SUDOKU
def vista_resolucion_sudoku(tablero):
  for i in range(9):
    for j in range(9):
      if tablero[i][j] == 0:
        for n in range(1, 10):
          if numero_valido(tablero, i, j, n):
            tablero[i][j] = n
            mostrar_numeros(tablero)
            pygame.display.flip()
            time.sleep(0.1)  # Pausa para ver el proceso
            if vista_resolucion_sudoku(tablero):
              return True
            tablero[i][j] = 0 #BORRA EL NUMERO SI LA SOLUCION NO ES VALIDA
            mostrar_numeros(tablero)
            pygame.display.flip()
            time.sleep(0.1)  # Pausa para ver el proceso
        return False
  return True

#REINICIAR APLICACION
def reiniciar(tablero):
  borrar_mostrar_numeros(tablero)
  # Creo botones niveles
  niveles()
  #Borro mensaje resuelto
  borrar_mensaje_resuelto()

#SALIR APLICACION
def salir():
  pygame.quit()
  sys.exit()

#Mostrar mensaje resuelto
def mostrar_mensaje_resuelto():
  mensaje = fuente.render("¡Sudoku Resuelto!", True, ROJO_OSCURO)
  pantalla.blit(mensaje, (ANCHO // 2 - mensaje.get_width() // 2, 652))
  pygame.display.flip()

#Borrar mensaje resuelto
def borrar_mensaje_resuelto(): 
  pygame.draw.rect(pantalla, BLANCO, (ANCHO // 2 - 150, 652, 300, 50))
  pygame.display.flip()

#Iniio aplicacion
def main():
  running = True#Variable para controlar el bucle
  pantalla.fill(BLANCO)#Fondo blanco
  creacion_tablero()#Creacion de tablero
  niveles()#Seleccionar nivel
  creacion_boton_empezar()#Creacion de boton empezar
  creacion_boton_reiniciar()#creacion de boton reiniciar
  creacion_boton_salir()#creacion de boton salir
  #Ciclo principal
  while running:
    global tablero_actual #hacer uso de la variable global
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      elif event.type == pygame.MOUSEBUTTONDOWN:#pulsar el mouse
        mouse_pos = event.pos#Obtener la posicion del mouse
        #Verificar si se ha presionado el botón Nivel Fácil
        #Verificar si se ha presionado el botón Salir
        if 270 <= mouse_pos[0] <= 340 and 602 <= mouse_pos[1] <= 672:
          print("Botón Salir presionado")
          salir()
        if 50 <= mouse_pos[0] <= 130 and 698 <= mouse_pos[1] <= 748:
          print("Nivel Fácil")
          #borrando botones niveles
          borrar_botones_niveles()
          tablero_actual = random.choice(leer_tableros()["faciles"])
          # Imprimir el tablero de Sudoku en formato 9x9
          for fila in tablero_actual:
            print(" ".join(str(num) if num != 0 else '.' for num in fila))
          mostrar_numeros(tablero_actual)
        #Verificar si se ha presionado el botón Medio
        if 260 <= mouse_pos[0] <= 340 and 698 <= mouse_pos[1] <= 748:
          print("Nivel Medio")
          #borrando botones niveles
          borrar_botones_niveles()
          tablero_actual = random.choice(leer_tableros()["medios"])
          # Imprimir el tablero de Sudoku en formato 9x9
          for fila in tablero_actual:
            print(" ".join(str(num) if num != 0 else '.' for num in fila))
            mostrar_numeros(tablero_actual)
        #Verificar si se ha presionado el botón Difícil
        if 500 <= mouse_pos[0] <= 580 and 698 <= mouse_pos[1] <= 748:
          print("Nivel Difícil")
          #borrando botones niveles
          borrar_botones_niveles()
          tablero_actual = random.choice(leer_tableros()["dificiles"])
          # Imprimir el tablero de Sudoku en formato 9x9
          for fila in tablero_actual:
            print(" ".join(str(num) if num != 0 else '.' for num in fila))
            mostrar_numeros(tablero_actual)
        #Verificar si se ha presionado el botón Empezar
        elif 100 <= mouse_pos[0] <= 355 and 602 <= mouse_pos[1] <= 652:
          if tablero_actual is None:
            print("¡Selecciona un nivel primero!")
          else:
            print("Botón Empezar presionado")
            mostrar_solucion(tablero_actual)
        #Verificar si se ha presionado el botón Reiniciar    
        elif 400 <= mouse_pos[0] <= 510 and 602 <= mouse_pos[1] <= 652:
          if tablero_actual is None:
            print("¡Selecciona un nivel primero!")
          else:
            print("Botón Reiniciar presionado")
            reiniciar(tablero_actual)
    pygame.display.flip()
  pygame.quit()

if __name__ == '__main__':
  try:
      main()
  except UnboundLocalError as e:
      print(f"Error al acceder a la variable: {e}")
  except Exception as e:
      print(f"Ha ocurrido un error inesperado: {e}")
  finally:
      print("Saliendo...")
