import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np

# Título de la aplicación
st.title("¡Aprende Lenguaje de Señas Colombiano!")

# Descripción de la sección
st.write("""
### Básico: Tu Señal de Identificación

En esta sección, puedes crear tu propia señal de identificación personalizada. 
En la comunidad de personas sordas, la presentación de los nombres se realiza de manera única y significativa a través del lenguaje de señas. 
Este proceso no solo implica deletrear el nombre con el alfabeto manual, sino también, en muchas ocasiones, incluir un "nombre en señas". 
Este nombre en señas, va más allá de la mera identificación, es un reflejo de la identidad y la conexión social dentro de la comunidad.
""")

# Video explicativo
st.write("""
Mira este video para conocer más detalles sobre la señal de identificación.
""")
video_url = "https://www.youtube.com/watch?v=sGg6p03wADw" 
st.video(video_url)

# Sección para poner en práctica
st.write("""
## ¡Ponlo en Práctica!
Captura una característica distintiva, ya sea física, de personalidad o relacionada con una experiencia memorable y crea tu propia seña:
""")

# Función para capturar imagen desde la cámara
def take_photo():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Captura de imagen', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Presiona 'q' para salir
            break
    cap.release()
    cv2.destroyAllWindows()
    return frame

# Función para detectar la palabra clave y capturar la imagen
def detect_and_capture(keyword):
    captured_image = None
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Captura de imagen', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Presiona 'q' para salir
            break
        if keyword in st.microphone_input("Habla ahora...", key="my_mic"):
            captured_image = frame
            break
    cap.release()
    cv2.destroyAllWindows()
    return captured_image

# Capturar imagen al detectar la palabra clave "foto"
if st.button("Tomar Foto"):
    st.write("Escucha la palabra 'foto' para capturar la imagen...")
    keyword = "foto"
    captured_image = detect_and_capture(keyword)
    if captured_image is not None:
        # Convertir la imagen capturada a formato Pillow y mostrarla
        captured_image = cv2.cvtColor(captured_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(captured_image)
        st.image(pil_image, caption="Tu Señal de Identificación")

        # Guardar la imagen y agregar botón de descarga
        pil_image.save("señal_identificacion.jpg")
        st.download_button(
            label="Descargar",
            data=open("señal_identificacion.jpg", "rb").read(),
            file_name="señal_identificacion.jpg",
            mime="image/jpeg"
        )

# Sección para compartir la señal
st.write("""
### ¡Comparte tu Señal!
Una vez que hayas creado tu señal de identificación, compártela con tus amigos y familiares para que puedan reconocerte fácilmente en la comunidad.
""")

