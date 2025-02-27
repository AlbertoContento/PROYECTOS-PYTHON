import subprocess
import sys
from tkinter import *
import tkinter as tk
import random
import time
from tkinter import ttk

# Instalar dependencias condicionalmente
def instalar_dependencias():
    try:
        # Definir las dependencias necesarias
        dependencias = ['tkinter']  # Asegúrate de agregar cualquier otra dependencia

        for dep in dependencias:
            try:
                __import__(dep)
            except ImportError:
                print(f"Instalando {dep}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
    except Exception as e:
        print(f"Error al intentar instalar dependencias: {e}")

instalar_dependencias()

class AppEscrituraVeloz:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto 3 - Escritura Veloz")
        self.root.geometry("800x600")

        # Texto inicial
        self.text1 = tk.Label(text="Escribe el siguiente Texto", font="bold")
        self.text1.place(x=280, y=10)

        # Cambié el Label por un widget Text para poder aplicar colores
        self.text_display = tk.Text(root, height=6, width=50, font=("Arial", 16), wrap="word", state="disabled")
        self.text_display.place(x=100, y=60)

        # Entrada de texto deshabilitada inicialmente
        self.entrada_texto1 = tk.Text(root, height=6, width=50, font=("Arial", 16), wrap="word", state="disabled")
        self.entrada_texto1.place(x=100, y=300)

        # Resultado
        self.resultado = tk.Label(root, text="", font=("Arial", 18))
        self.resultado.place(x=250, y=210)

        # Botón para comenzar
        self.boton_empezar = tk.Button(root, text="Comenzar Prueba", command=self.comenzar_test)
        self.boton_empezar.place(x=350, y=460)

        # Selector de nivel
        self.text2 = tk.Label(text="Nivel: 1 | 2 | 3", font=("Arial", 12))
        self.text2.place(x=280, y=500)
        self.nivel = tk.StringVar(value="1")
        self.menu_niveles = ttk.Combobox(root, textvariable=self.nivel, values=["1", "2", "3"], state="readonly")
        self.menu_niveles.place(x=400, y=500)

        # Botón para reiniciar
        self.boton_reiniciar = tk.Button(root, text="Reiniciar", command=self.reiniciar)
        self.boton_reiniciar.place(x=250, y=550)

        # Botón para salir (inicialmente deshabilitado)
        self.boton_salir = tk.Button(root, text="Salir", command=self.salir, state="normal")
        self.boton_salir.place(x=550, y=550)

        self.frase_actual = ""  # Almacena la frase actual para comparar
        self.tiempo_inicio = None  # Almacena el tiempo de inicio de la prueba
        self.tiempo_fin = None  # Almacena el tiempo de finalización de la prueba
        self.tiempo_finalizado = False  # Variable para evitar que siga corriendo tras Escape

    def comenzar_test(self):
        """Inicia la prueba de escritura rápida."""
        self.tiempo_inicio = time.time()  # Inicia el tiempo de comienzo
        self.tiempo_fin = None  # Reinicia el tiempo final
        self.tiempo_finalizado = False  # Resetear flag de finalización
        nivel = int(self.nivel.get())
        frase = self.frase_random(nivel)
        self.frase_actual = frase
        # Actualiza la frase a escribir
        self.text_display.config(state="normal")
        self.text_display.delete(1.0, "end")
        self.text_display.insert("end", frase)
        self.text_display.config(state="disabled")

        # Activa el cuadro de texto para la entrada del usuario
        self.entrada_texto1.config(state="normal")
        #ponemos el foco en entrada:_texto1
        self.entrada_texto1.focus_set()  # Ponemos el foco

        # Evento para presionar cualquier tecla
        self.entrada_texto1.bind("<KeyPress>", self.procesar_tecla)
        self.entrada_texto1.bind("<Escape>", self.comprobar_entrada)

        self.resultado.config(text="")
        self.boton_empezar.config(state="disabled")
    
        # Resaltar la primera letra de la frase en rojo
        self.text_display.config(state="normal")
        self.text_display.delete(1.0, "end")  # Limpiar el contenido
        self.text_display.insert("1.0", frase[0], "rojo")  # Resaltar primera letra en rojo
        self.text_display.insert("end", frase[1:])  # Insertar el resto del texto sin cambios
        self.text_display.tag_configure("rojo", foreground="red")
        self.text_display.config(state="disabled")

    def frase_random(self, nivel):
            frases = {
                1: ["El gol es la poesía del fútbol, el momento sublime.",
                    "El estadio rugía como un león al ver la jugada maestra.",
                    "La pelota es el corazón del juego, late en cada pase.",
                    "La victoria es el eco de la estrategia bien ejecutada.",
                    "La derrota es el maestro que enseña las lecciones más duras.",
                    "El balón bailaba al compás de los pies del mago del equipo.",
                    "El portero es el guardián del arco, el último bastión.",
                    "El fuera de juego es el límite entre la oportunidad y la infracción.",
                    "El golpe de cabeza es la demostración de poderío aéreo.",
                    "El regate es la danza del engaño, el arte de la sorpresa.",
                    "La afición es la fuerza que impulsa al equipo hacia la gloria.",
                    "El fútbol es el lenguaje universal que une a las naciones.",
                    "El árbitro es el juez imparcial en el campo de batalla.",
                    "El entrenador es el estratega, el cerebro detrás de cada movimiento.",
                    "El balón es redondo para darle giros inesperados al destino.",
                    "El gol es la explosión de júbilo, el éxtasis colectivo.",
                    "El fútbol es pasión, es amor por los colores que se defienden.",
                    "La táctica es el plan meticuloso que se despliega en el terreno.",
                    "El fútbol es el arte de convertir el sueño en realidad en 90 minutos.",
                    "La historia del fútbol se escribe con goles, con hazañas inolvidables."],
                2: ["El fútbol es mucho más que un deporte, es una pasión que une a personas de todo el mundo. Cada partido es una oportunidad para soñar, ganar y vivir emociones intensas con cada jugada.",
                    "El sonido del silbato final siempre está lleno de emociones. La alegría de la victoria y la tristeza de la derrota son parte de lo que hace al fútbol tan único e impredecible en cada partido.",
                    "Cada pase, cada regate, cada gol es una historia dentro de una historia. El fútbol es un espectáculo que se escribe con cada movimiento y cada esfuerzo de los jugadores en el campo.",
                    "El fútbol tiene el poder de juntar a miles de personas, creando una atmósfera única. Las gradas se llenan de cantos y los corazones laten al ritmo del balón que se mueve sobre el césped.",
                    "Cuando el equipo juega bien, todo parece fluir perfectamente. Las jugadas se suceden con naturalidad y el gol se siente cercano, como si fuera el destino el que lo hubiera escrito para ese momento.",
                    "La pasión de los hinchas es incomparable. Cada gol es una explosión de alegría, y cada derrota es una lección para seguir adelante, siempre con la esperanza de la próxima victoria en el horizonte.",
                    "El fútbol no solo se juega en el campo, sino también en la mente. La estrategia, las decisiones rápidas y la concentración constante son clave para triunfar en un deporte donde todo puede cambiar en segundos.",
                    "El fútbol enseña que no siempre se gana, pero siempre se puede aprender. Cada partido, cada error, cada acierto es una oportunidad para mejorar y crecer, tanto en lo personal como en lo deportivo.",
                    "El instante en que el balón cruza la línea de gol es mágico. Los jugadores celebran, los aficionados gritan de emoción, y el mundo parece detenerse por un segundo, disfrutando de ese logro colectivo.",
                    "El fútbol es un deporte de equipo, donde cada jugador tiene un rol fundamental. No importa cuántos goles marque uno solo, la victoria siempre es el resultado del esfuerzo conjunto de todos los integrantes.",
                    "El fútbol tiene un lenguaje universal. No importa de dónde vengas, todos entienden la emoción de un buen pase, la tensión antes de un penalti o la felicidad de ver el balón dentro de la red.",
                    "A veces, en el fútbol, la victoria no se mide solo en goles, sino en el esfuerzo y la determinación que se pone en cada jugada. Lo importante es dar todo en cada momento y luchar hasta el final.",
                    "La historia del fútbol está llena de momentos inolvidables. Desde los goles más rápidos hasta las remontadas más épicas, el fútbol nunca deja de sorprendernos, regalándonos recuerdos para toda la vida.",
                    "El fútbol no solo es físico, también es mental. La capacidad de mantener la calma en situaciones de presión, de tomar decisiones rápidas y de liderar en momentos claves es lo que define a un gran jugador.",
                    "El fútbol es una danza, una coreografía de movimientos rápidos y sincronizados. Cada jugador es parte de un engranaje que, cuando funciona bien, lleva al equipo a la victoria, como una máquina perfecta."],
                3: ["El fútbol no se juega solo en 90 minutos: cada pase, cada decisión, cada segundo cuenta. El tiempo puede parecer eterno cuando estás a un gol de la gloria o cuando una jugada decisiva puede cambiarlo todo en un instante; la tensión nunca se detiene.",
                    "En la historia del fútbol, hay momentos que quedan grabados: el gol de Maradona en el '86, el penalti fallado por Zidane en la final del '06, y los 3 goles de Messi en la Champions. Todos ellos, simbolizando los altibajos del deporte más impredecible de todos.",
                    "La fórmula de un partido perfecto en fútbol: 100% de esfuerzo, 25% de suerte, 75% de estrategia y, por supuesto, 0% de rendirse. Cada jugador sabe que en cualquier momento la balanza puede inclinarse a favor o en contra, por un simple error o acierto.",
                    "En un partido, todo puede cambiar con un solo gol, y eso no se limita solo a los 90 minutos. Un gol en el minuto 94 puede ser tan decisivo como uno en el primer tiempo; al final, cada jugada es crucial y cada segundo, un pequeño pero significativo reto.",
                    "Los números en fútbol a menudo no reflejan el verdadero valor de un jugador: no solo importa cuántos goles has marcado (como los 500 de Cristiano o los 600 de Messi), sino cómo influencias en el juego, cómo mueves a tu equipo y cómo enfrentas la adversidad.",
                    "En 1999, el Manchester United remontó una final que parecía perdida, ganando 2-1 en los últimos 3 minutos; un gol de Teddy Sheringham y otro de Ole Gunnar Solskjaer, dos jugadores que cambiaron el destino de su equipo en un abrir y cerrar de ojos.",
                    "Las estadísticas dicen mucho, pero no lo dicen todo: un pase preciso, aunque no se traduzca en gol, puede ser tan valioso como el tanto que marca la diferencia. Por eso, no solo se mide el número de goles (3, 5 o 10), sino el trabajo en equipo que los permite.",
                    "Un equipo no se mide solo por su capacidad de marcar goles (3, 5 o 10), sino por su solidez en defensa. La diferencia entre un campeón y un subcampeón muchas veces radica en su capacidad para resistir en los momentos de mayor presión, como el 'último minuto'.",
                    "El fútbol, como la vida, es impredecible. Un equipo puede dominar durante 85 minutos, pero en los últimos 5, el partido puede dar un giro inesperado. Ese es el misterio que mantiene a millones de personas mirando, como si el tiempo se congelara con cada jugada.",
                    "El triunfo no solo se mide en victorias; un empate 0-0 también puede ser un resultado que define una temporada. Las estadísticas son frías, pero el espíritu del equipo, la motivación, y la lucha en cada segundo, son lo que realmente determina la grandeza de un jugador.",
                    "La derrota no significa el fin, sino una lección. Un equipo que pierde 1-2 en los últimos minutos sabe que puede cambiarlo en el próximo partido, que cada jornada es una nueva oportunidad para corregir errores y demostrar su verdadero nivel de juego.",
                    "Un 4-3 en una final es más que un resultado; es un símbolo de lucha, de esfuerzo hasta el último minuto. En fútbol, la diferencia entre ganar y perder puede ser de solo 1 gol, 2 centímetros o 3 segundos. Cada detalle es crucial y cada segundo, irremplazable.",
                    "En el fútbol, los números no lo son todo. A veces, un partido ganado con 1 gol o 5 goles de diferencia importa menos que el esfuerzo, el sacrificio y la unidad mostrada durante esos 90 minutos (más el tiempo añadido, si es necesario).",
                    "El fútbol tiene una matemática simple: 11 jugadores en el campo, un balón, y un objetivo. A veces, es cuestión de estrategia, otras de suerte. Pero lo que siempre importa es cómo los jugadores se comportan bajo presión y cómo aprovechan cada oportunidad.",
                    "Los grandes equipos no solo tienen grandes jugadores; tienen una mentalidad ganadora. Un equipo que sabe cuándo atacar y cuándo defender, que no pierde la calma en los últimos minutos, puede convertir un 1-1 en una victoria gracias a su concentración y esfuerzo."]
            }
            return random.choice(frases.get(nivel, []))
    
    def procesar_tecla(self, event):
        """
        Este método se llama cada vez que el usuario presiona una tecla.
        La letra que corresponde al siguiente carácter de la frase actual se resalta en rojo.
        """
        # Obtiene el texto completo de la frase actual
        frase = self.frase_actual
        # Obtiene el texto escrito por el usuario (sin contar saltos de línea)
        texto_usuario = self.entrada_texto1.get("1.0", "end-1c")

        # Calculamos el índice del siguiente carácter que debería escribir el usuario
        indice_siguiente = len(texto_usuario)

        # Si el índice es menor que la longitud de la frase, resaltar la siguiente letra
        if indice_siguiente < len(frase):
            # Resaltar la siguiente letra de la frase
            parte1 = frase[:indice_siguiente]  # Texto ya escrito
            parte2 = frase[indice_siguiente]  # Letra que debe escribir el usuario
            parte3 = frase[indice_siguiente + 1:]  # Resto del texto

            # Configuramos el texto de text_display
            self.text_display.config(state="normal")
            self.text_display.delete(1.0, "end")  # Limpiar el contenido

            # Ingresamos las partes en el widget Text con formato de color rojo para la letra que debe escribir el usuario
            self.text_display.insert("1.0", parte1)
            self.text_display.insert("end", parte2, "rojo")
            self.text_display.insert("end", parte3)

            # Crear una etiqueta de texto con color rojo para la letra resaltada
            self.text_display.tag_configure("rojo", foreground="red")

            self.text_display.config(state="disabled")
    
    def comprobar_resultado(self):
        """Compara la entrada del usuario con la frase y muestra los errores."""
        entrada_usuario = self.entrada_texto1.get(1.0, "end-1c").strip()

        # Calcular errores de manera eficiente
        errores = self.calcular_errores(entrada_usuario)

        # Calcular el tiempo transcurrido si es posible
        tiempo = self.calcular_tiempo()

        # Calcular el porcentaje de precisión
        porcentaje = self.calcular_precision(entrada_usuario, errores)

        # Mostrar los resultados
        self.mostrar_resultados(errores, tiempo, porcentaje)

    def calcular_errores(self, entrada_usuario):
        """Calcula los errores de la entrada comparada con la frase actual."""
        if entrada_usuario != self.frase_actual:
            return sum(1 for a, b in zip(entrada_usuario, self.frase_actual) if a != b)
        return 0

    def calcular_tiempo(self):
        """Calcula el tiempo transcurrido entre el inicio y el fin de la prueba."""
        if self.tiempo_inicio and self.tiempo_fin:
            return self.tiempo_fin - self.tiempo_inicio
        return 0.0

    def calcular_precision(self, entrada_usuario, errores):
        """Calcula el porcentaje de precisión de la entrada del usuario."""
        if len(self.frase_actual) > 0:
            return (len(entrada_usuario) - errores) / len(self.frase_actual) * 100
        return 0

    def mostrar_resultados(self, errores, tiempo, porcentaje):
        """Muestra los resultados de los errores, el tiempo y la precisión."""
        self.resultado.config(
            text=f"Errores: {errores}\n"
            f"Tiempo: {tiempo:.2f} segundos\n"
            f"Precisión: {porcentaje:.2f}%"
        )

    def reiniciar(self):
        """Reinicia la interfaz a su estado inicial."""
        self.text_display.config(state="normal")
        self.text_display.delete(1.0, "end")
        self.text_display.config(state="disabled")   
        self.entrada_texto1.config(state="normal")
        self.entrada_texto1.delete(1.0, "end")
        self.entrada_texto1.config(state="disabled")
        self.resultado.config(text="")

        # Resetear los tiempos
        self.tiempo_inicio = None
        self.tiempo_fin = None
        self.tiempo_finalizado = False

        # Habilitar el botón de empezar y desactivar otros
        self.boton_empezar.config(state="normal")

        # Deshabilitar otros botones
        self.boton_salir.config(state="disabled")

    def salir(self):
        """Cierra la aplicación."""
        self.root.quit()
    
    def comprobar_entrada(self, event=None):
        """Detiene la prueba al presionar Escape y muestra los resultados correctamente."""
        self.tiempo_finalizado = True  # Marcar que el tiempo ha finalizado
        # Guardar el tiempo de finalización si aún no está registrado
        if self.tiempo_inicio and not self.tiempo_fin:
            self.tiempo_fin = time.time()

        # Asegurar que los resultados se calculen solo una vez
        self.comprobar_resultado()

if __name__ == "__main__":
    root = Tk()
    app = AppEscrituraVeloz(root)
    root.mainloop()