import streamlit as st
import edge_tts
import asyncio

st.set_page_config(page_title="Hán Ngữ Engine Pro", layout="centered")
st.title("🎙️ Cỗ Máy Phát Âm Hán Ngữ 0.5")

# Thông số vàng: Giọng Xiaoxiao, Tốc độ 0.5, Pitch +8Hz (Giúp âm thanh thanh thoát)
VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-50%" 
PITCH = "+8Hz" 

text_input = st.text_area("Dán thuần chữ Hán vào đây (Dùng dấu 。để nghỉ 1 giây):", height=200)

async def generate_audio(text):
    if not text.strip(): return None
    
    # Kỹ thuật: Chỉ thay dấu chấm bằng lệnh nghỉ, KHÔNG chia nhỏ văn bản.
    # AI sẽ nhận diện được từ ghép và đọc tròn vành rõ chữ.
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

if st.button("▶️ PHÁT ÂM CHUẨN"):
    audio = asyncio.run(generate_audio(text_input))
    if audio: st.audio(audio)
