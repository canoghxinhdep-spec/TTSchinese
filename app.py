import streamlit as st
import edge_tts
import asyncio

st.set_page_config(page_title="Hán Ngữ Pro Engine", layout="centered")
st.title("🎙️ Cỗ Máy Phát Âm Hán Ngữ 0.5")

# Thiết lập chuẩn: Giọng Xiaoxiao, Tốc độ 0.5, Pitch thanh thoát
VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-50%" 
PITCH = "+5Hz"

text_input = st.text_area("Dán nội dung chữ Hán vào đây:", height=250, 
                          placeholder="Ví dụ: 哥。哥哥。河。河水。")

async def generate_audio(text):
    if not text.strip():
        return None
    
    # Quy trình: Thay dấu chấm bằng lệnh nghỉ 1.2 giây để người học kịp nhẩm theo
    # Không dùng vòng lặp tách chữ để tránh AI đánh vần Latinh
    ssml_content = text.replace("。", " <break time='1200ms'/> ")
    
    ssml_text = f"""
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='zh-CN'>
        <voice name='{VOICE}'>
            <prosody rate='{RATE}' pitch='{PITCH}'>
                {ssml_content}
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

if st.button("▶️ CHẠY MÁY (PHÁT ÂM CHUẨN)"):
    if text_input:
        with st.spinner('Đang tạo âm thanh...'):
            audio = asyncio.run(generate_audio(text_input))
            if audio:
                st.audio(audio)
    else:
        st.warning("Bạn chưa dán nội dung!")
