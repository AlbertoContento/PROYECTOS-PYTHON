import sys
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Verificar si los recursos ya están descargados
nltk_data = ['punkt', 'stopwords', 'wordnet']

for resource in nltk_data:
    try:
        nltk.data.find(f'tokenizers/{resource}')
    except LookupError:
        print(f"El recurso {resource} no está disponible, descargando...")
        nltk.download(resource)


class MiVentana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Proyecto 09 - Sistema de Recomendacion de Netflix")
        self.setGeometry(100, 100, 700, 800)  # Posición (x, y) y tamaño (ancho, alto)

        # Favicon
        self.setWindowIcon(QIcon('../assets/images/favicon.ico'))  # Asegúrate de tener el favicon.ico en el directorio actual

        # Imagen
        self.image_label = QLabel(self)
        self.image_label.setPixmap(QIcon('../assets/images/Netflix_Logo.png').pixmap(220, 120))  # Ajusta la ruta de la imagen
        # Centrar la imagen
        self.image_label.setAlignment(Qt.AlignCenter)

        # Entrada de texto con placeholder
        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("Inserta Pelicula o Serie")
        self.text_input.setStyleSheet("""
            QLineEdit {
                background-color: #2E2E2E;  /* Gris oscuro */
                border: 2px solid #555555;  /* Borde gris */
                border-radius: 8px;        /* Bordes redondeados */
                color: white;               /* Texto blanco */
                padding: 15px;               /* Espaciado interno */
                font-size: 16px;            /* Tamaño pequeño */
                font-weight: bold;         /* Negrita */ 
            }
            QLineEdit:hover {
                border: 2px solid red;      /* Cambiar el borde a rojo en hover */
            }
        """)

        # Crear un botón
        self.boton_recomendar = QPushButton("Recomendar", self)
        self.boton_recomendar.clicked.connect(self.recomendar)
        self.boton_recomendar.setStyleSheet("""
            QPushButton {
                background-color: #E50914; /* Colo rojo */
                color: white;              /* Color del texto blanco */
                border-radius: 8px;        /* Borde redondeado */ 
                padding: 15px 20px;         /* Espaciado */
                font-size: 18px;           /* Tamaño Fuente */ 
                font-weight: bold;         /* Negrita */ 
                text-align: center;        /* Alineacion centrada */
            }
            QPushButton:hover {
                background-color: #a50c13;  /* Fondo más oscuro al hacer hover */
                border: 2px solid #a50c13;  /* Borde más oscuro al hacer hover */
            }
            QPushButton:pressed {
                background-color: #870b11;  /* Fondo cuando se presiona */
                border: 2px solid #870b11;  /* Borde cuando se presiona */
            }
        """)

        # QLabel para mostrar la recomendación basada en el texto de input
        self.recomendacion_label = QLabel(self)
        self.recomendacion_label.setText("Recomendaciones basadas en: Ninguna")
        self.recomendacion_label.setStyleSheet("""
            color: white;
            font-size: 22px;
            font-weight: bold;
            text-align: center; 
            """)
        self.recomendacion_label.setVisible(False) #Lo ocultamos Inicialmente

        # Área de texto
        self.text_area = QTextEdit(self)
        self.text_area.setPlaceholderText("Peliculas Recomendadas")
        self.text_area.setFixedHeight(600)  # Ajusta la altura del área de texto (puedes modificar el valor)
        self.text_area.setReadOnly(True)  # Deshabilitar la edición del área de texto
        self.text_area.setStyleSheet("""
            background-color: #2E2E2E;  /* Gris oscuro */
            border: 2px solid #555555;  /* Borde gris */
            border-radius: 8px;        /* Bordes redondeados */
            color: white;               /* Texto blanco */
            padding: 15px;               /* Espaciado interno */
            font-size: 16px;            /* Tamaño pequeño */
            font-weight: bold;         /* Negrita */ 
            """)

        # Crear un botón Reiniciar
        self.boton_reiniciar = QPushButton("Reiniciar", self)
        self.boton_reiniciar.clicked.connect(self.reiniciar)
        self.boton_reiniciar.setStyleSheet("""
            QPushButton {
                background-color: #E50914; /* Colo rojo */
                color: white;              /* Color del texto blanco */
                border-radius: 8px;        /* Borde redondeado */ 
                padding: 15px 20px;         /* Espaciado */
                font-size: 18px;           /* Tamaño Fuente */ 
                font-weight: bold;         /* Negrita */ 
                text-align: center;        /* Alineacion centrada */
            }
            QPushButton:hover {
                background-color: #a50c13;  /* Fondo más oscuro al hacer hover */
                border: 2px solid #a50c13;  /* Borde más oscuro al hacer hover */
            }
            QPushButton:pressed {
                background-color: #870b11;  /* Fondo cuando se presiona */
                border: 2px solid #870b11;  /* Borde cuando se presiona */
            }
        """)

        # Crear un botón SAlir
        self.boton_salir = QPushButton("Salir", self)
        self.boton_salir.clicked.connect(self.salir)
        self.boton_salir.setStyleSheet("""
            QPushButton {
                background-color: #E50914; /* Colo rojo */
                color: white;              /* Color del texto blanco */
                border-radius: 8px;        /* Borde redondeado */ 
                padding: 15px 20px;         /* Espaciado */
                font-size: 18px;           /* Tamaño Fuente */ 
                font-weight: bold;         /* Negrita */ 
                text-align: center;        /* Alineacion centrada */
            }
            QPushButton:hover {
                background-color: #a50c13;  /* Fondo más oscuro al hacer hover */
                border: 2px solid #a50c13;  /* Borde más oscuro al hacer hover */
            }
            QPushButton:pressed {
                background-color: #870b11;  /* Fondo cuando se presiona */
                border: 2px solid #870b11;  /* Borde cuando se presiona */
            }
        """)

        # Crear un layout horizontal para el input y el botón
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.text_input)
        h_layout.addWidget(self.boton_recomendar)

        # Organizar en un layout vertical
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        # Añadir el layout horizontal al layout principal y estableces layout de la ventana
        layout.addLayout(h_layout)
        layout.addWidget(self.recomendacion_label)
        layout.addWidget(self.text_area)
        layout.addWidget(self.boton_reiniciar)
        layout.addWidget(self.boton_salir)
        self.setLayout(layout)

        # Activar modo oscuro al inicio
        self.set_dark_mode()

    #FUNCION PARA CAMBIAR COLOR
    def set_dark_mode(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(18, 18, 18))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(169, 169, 169))  # Fondo de los campos de texto
        palette.setColor(QPalette.Text, Qt.white)  # Texto en los campos de texto
        palette.setColor(QPalette.Button, QColor(229, 9, 20))  # Color de los botones
        palette.setColor(QPalette.ButtonText, Qt.white)  # Texto en los botones
        self.setPalette(palette)

    #FUNCION MOSTRAR RECOMENDACION_LABEL
    def mostrar_recomendacion_label(self):
        # Obtener el texto del input
        input_text = self.text_input.text()
        # Actualizar el texto del QLabel de recomendación
        self.recomendacion_label.setText(f"Recomendaciones basadas en: {input_text}")
        # Hacer visible el QLabel
        self.recomendacion_label.setVisible(True)

    # Función de preprocesamiento de texto
    def procesar_texto(self, texto):
        # Tokenización: Convertimos el texto en una lista de palabras (tokens)
        tokens = word_tokenize(texto.lower())  # Convertir a minúsculas para asegurar que todo se compare sin importar el caso
        
        # Eliminar stopwords: Filtramos palabras que no aportan información útil para la búsqueda (como "de", "el", "a", etc.)
        tokens = [t for t in tokens if t not in stopwords.words('english')]
        
        # Lemmatización: Reducimos las palabras a su forma base. Por ejemplo, "running" se convierte en "run".
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(t) for t in tokens]
        
        # Devolvemos el texto procesado como una cadena unida de nuevo
        return ' '.join(tokens)

    # FUNCION RECOMENDAR
    def recomendar(self):
        # Mostramos el mensaje de recomendación
        self.mostrar_recomendacion_label()  
        
        # Obtenemos el texto que el usuario ha ingresado en el campo de entrada (text_input)
        texto_input = self.text_input.text()  
        
        # Limpiamos el área de texto donde mostraremos las recomendaciones
        self.text_area.setText("")  
        
        # Variable para verificar si hemos encontrado alguna recomendación
        encontrada = False

        # Verificamos si el usuario ha ingresado texto en el campo de entrada
        if texto_input:
            # Preprocesamos el texto de entrada del usuario (aplicamos tokenización, eliminación de stopwords y lematización)
            texto_input_procesado = self.procesar_texto(texto_input)

            # Cargamos el archivo CSV con los datos de Netflix (películas y series)
            df = pd.read_csv("../assets/data/netflixData.csv")
            
            # Preprocesamos las columnas de 'Title', 'Description' y 'Genres' del DataFrame de manera similar al texto de entrada
            df['Title'] = df['Title'].apply(lambda x: self.procesar_texto(str(x)))  # Preprocesamos el título
            df['Description'] = df['Description'].apply(lambda x: self.procesar_texto(str(x)))  # Preprocesamos la descripción
            df['Genres'] = df['Genres'].apply(lambda x: self.procesar_texto(str(x)))  # Preprocesamos los géneros

            # Creamos una máscara booleana que verifica si el texto de entrada (procesado) se encuentra en alguna de las columnas preprocesadas
            mask = df['Title'].str.contains(texto_input_procesado, case=False) | \
                df['Description'].str.contains(texto_input_procesado, case=False) | \
                df['Genres'].str.contains(texto_input_procesado, case=False)

            # Filtramos las filas del DataFrame que coinciden con la búsqueda y tomamos los primeros 20 resultados
            resultados = df[mask].head(10)  # Mostrar solo los primeros 20 resultados

            # Verificamos si hay resultados
            if not resultados.empty:
                # Si encontramos resultados, los mostramos en el área de texto
                for _, row in resultados.iterrows():
                    self.text_area.append(row["Title"])  # Mostramos el título de las coincidencias
                    encontrada = True  # Marcamos que se ha encontrado al menos una coincidencia

            # Si no se encontraron resultados, mostramos un mensaje indicando que no hay recomendaciones
            if not encontrada:
                self.text_area.append(f"No hay ninguna recomendación con: {texto_input}")
        else:
            # Si el usuario no ha introducido texto, mostramos un mensaje indicando que no se ha introducido ninguna película/serie
            self.recomendacion_label.setText("No has Introducido ninguna Película|Serie")

    #FUNCION REINICIAR
    def reiniciar(self):
        self.text_input.clear() #Limpiamos el input
        self.text_area.clear() #Limpiamos el textarea
        self.recomendacion_label.setVisible(False)  # Ocultar la etiqueta de recomendaciones

    #FUNCION SALIR
    def salir(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MiVentana()
    ventana.show()
    sys.exit(app.exec_())