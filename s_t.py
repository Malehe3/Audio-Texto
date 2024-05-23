import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image, ImageDraw, ImageFont
import time

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

# Configuración del botón de reconocimiento de voz
stt_button = Button(label="Comienza", width=200, button_type="success")
stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if (value.toLowerCase().includes("foto")) {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
"""))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

# Funcionalidad de captura de imagen
if result:
    if "GET_TEXT" in result:
        st.write("¡Se detectó la palabra 'foto'! Capturando imagen...")
        img_file_buffer = st.camera_input("Toma una Foto")

        if img_file_buffer is not None:
            image = Image.open(img_file_buffer)
            st.image(image, caption="Tu Señal de Identificación")

            # Guardar imagen y agregar botón de descarga
            image.save("señal_identificacion.jpg")
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
