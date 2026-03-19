import streamlit as st
import edge_tts
import asyncio

st.set_page_config(page_title="Chinese Pro TTS", page_icon="🎙️")
st.title("🎙️ Chinese Pro TTS - Giọng Nữ Chuẩn")

# Cấu hình cứng theo yêu cầu của bạn
VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-50%"  # Tốc độ 0.5
PITCH = "+5Hz" # Giúp âm thanh thanh thoát, rõ chữ

text_input = st.text_area("Dán Hán tự vào đây (Dùng dấu 。 để ngắt nghỉ):", height=250)

async def generate_audio(text):
    # Sử dụng SSML chuyên nghiệp để điều khiển AI
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

if st.button("🔊 PHÁT ÂM CHUẨN 0.5"):
    if text_input.strip():
        with st.spinner('AI đang xử lý giọng đọc...'):
            audio = asyncio.run(generate_audio(text_input))
            st.audio(audio)
    else:
        st.warning("Bạn chưa nhập nội dung!")
