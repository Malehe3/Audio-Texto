import os
import streamlit as st
from PIL import Image
from gtts import gTTS
from googletrans import Translator

st.set_page_config(
    page_title="CocinaFacil - Tu Asistente de Cocina Personalizado",
    page_icon=":shrimp:",
    layout="wide"
)

# Estilo CSS para el botón
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border-radius: 5px;
        border-color: #000000;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        width: 200px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("CocinaFacil - Tu Asistente de Cocina Personalizado")

image = Image.open('RatitaChef3.png')
st.image(image, width=200, caption='Tu:')

st.write("¡Bienvenido a CocinaFacil con ChefIA, tu asistente de cocina personal! Aquí podrás narrar tus recetas para que otras personas puedan conocer y disfrutar al máximo de tus creaciones culinarias.")

st.write("Toca el botón y cuéntanos tu receta")

# HTML personalizado para el botón
button_html = """
<div class="stButton">
  <button onclick="startRecording()">Comienza</button>
</div>
<script>
function startRecording() {
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
        if (value !== "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    };
    recognition.start();
}
</script>
"""

# Mostrar el botón HTML personalizado
st.markdown(button_html, unsafe_allow_html=True)

# Recibir el resultado del reconocimiento de voz
result = st._server_ctx.events.get('GET_TEXT')

if result:
    st.write(result)
    try:
        os.mkdir("temp")
    except:
        pass
    st.title("Texto a Audio")
    translator = Translator()
    
    text = str(result)
    in_lang = st.selectbox(
        "Selecciona el lenguaje de Entrada",
        ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés"),
    )
    if in_lang == "Inglés":
        input_language = "en"
    elif in_lang == "Español":
        input_language = "es"
    elif in_lang == "Bengali":
        input_language = "bn"
    elif in_lang == "Coreano":
        input_language = "ko"
    elif in_lang == "Mandarín":
        input_language = "zh-cn"
    elif in_lang == "Japonés":
        input_language = "ja"
    
    out_lang = st.selectbox(
        "Selecciona el lenguaje de salida",
        ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés"),
    )
    if out_lang == "Inglés":
        output_language = "en"
    elif out_lang == "Español":
        output_language = "es"
    elif out_lang == "Bengali":
        output_language = "bn"
    elif out_lang == "Coreano":
        output_language = "ko"
    elif out_lang == "Mandarín":
        output_language = "zh-cn"
    elif out_lang == "Japonés":
        output_language = "ja"
    
    english_accent = st.selectbox(
        "Selecciona el acento",
        (
            "Defecto",
            "Español",
            "Reino Unido",
            "Estados Unidos",
            "Canada",
            "Australia",
            "Irlanda",
            "Sudáfrica",
        ),
    )
    
    if english_accent == "Defecto":
        tld = "com"
    elif english_accent == "Español":
        tld = "com.mx"
    
    elif english_accent == "Reino Unido":
        tld = "co.uk"
    elif english_accent == "Estados Unidos":
        tld = "com"
    elif english_accent == "Canada":
        tld = "ca"
    elif english_accent == "Australia":
        tld = "com.au"
    elif english_accent == "Irlanda":
        tld = "ie"
    elif english_accent == "Sudáfrica":
        tld = "co.za"
    
    
    def text_to_speech(input_language, output_language, text, tld):
        translation = translator.translate(text, src=input_language, dest=output_language)
        trans_text = translation.text
        tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
        try:
            my_file_name = text[0:20]
        except:
            my_file_name = "audio"
        tts.save(f"temp/{my_file_name}.mp3")
        return my_file_name, trans_text
    
    
    display_output_text = st.checkbox("Mostrar el texto")
    
    if st.button("Convertir"):
        result, output_text = text_to_speech(input_language, output_language, text, tld)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown(f"## Tú audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)
    
        if display_output_text:
            st.markdown(f"## Texto de salida:")
            st.write(f" {output_text}")
    
    
    def remove_files(n):
        mp3_files = glob.glob("temp/*mp3")
        if len(mp3_files) != 0:
            now = time.time()
            n_days = n * 86400
            for f in mp3_files:
                if os.stat(f).st_mtime < now - n_days:
                    os.remove(f)
                    print("Deleted ", f)

    remove_files(7)
