import sys
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt


class MiVentana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Proyecto 09 - Sistema de Recomendacion de Netflix")
        self.setGeometry(100, 100, 700, 800)  # Posición (x, y) y tamaño (ancho, alto)

        # Favicon
        self.setWindowIcon(QIcon('favicon.ico'))  # Asegúrate de tener el favicon.ico en el directorio actual

        # Imagen
        self.image_label = QLabel(self)
        self.image_label.setPixmap(QIcon('Netflix_Logo.png').pixmap(220, 120))  # Ajusta la ruta de la imagen
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

    #FUNCION RECOMENDAR
    def recomendar(self):
        self.mostrar_recomendacion_label()#Mostramos mensaje
        texto_input = self.text_input.text() #obtengo lo que hay en text_input

        if texto_input:
            with open("netflixData.csv", "r") as file:
                csv_reader = csv_reader(file)
                next(csv_reader) #saltar la cabecera para la fila de encabezado

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