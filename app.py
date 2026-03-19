import streamlit as st
import edge_tts
import asyncio

st.set_page_config(page_title="Hán Ngữ Engine", layout="centered")
st.title("🎙️ Cỗ Máy Phát Âm Hán Ngữ 0.5")

# Thiết lập cố định để đạt độ chuẩn như Gemini 2.0
VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-50%"  # Tốc độ chậm để luyện tai
PITCH = "+5Hz" # Tăng độ thanh để không bị bẹt âm

text_input = st.text_area("Dán Hán tự vào đây (Dấu 。 để nghỉ 1 giây):", height=200)

async def generate_audio(text):
    # Ép AI nhận diện chuẩn tiếng Trung và ngắt nghỉ theo dấu chấm
    ssml_text = f"""
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='zh-CN'>
        <voice name='{VOICE}'>
            <prosody rate='{RATE}' pitch='{PITCH}'>
                {text.replace("。", " <break time='1000ms'/> ")}
            </prosody>
        </voice>
    </speak>
    """
    communicate = edge_tts.Communicate(ssml_text, VOICE)
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return audio_data

if st.button("▶️ CHẠY MÁY"):
    if text_input.strip():
        audio = asyncio.run(generate_audio(text_input))
        st.audio(audio)
