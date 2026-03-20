import streamlit as st
import edge_tts
import asyncio
import re

st.set_page_config(page_title="Hán Ngữ Engine Pro", layout="centered")
st.title("🎙️ Cỗ Máy Phát Âm Hán Ngữ 0.5")

# Thông số vàng để AI không bị ngọng
VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-50%" 
PITCH = "+5Hz"

text_input = st.text_area("Dán giáo án (Chỉ chữ Hán) vào đây:", height=200)

async def generate_audio(text):
    # BƯỚC 1: LỌC NHIỄU TUYỆT ĐỐI
    # Chỉ giữ lại chữ Hán [\u4e00-\u9fff] và dấu chấm 。
    # Xóa sạch mọi dấu cách, tiếng Anh, Pinyin để AI không bị "loạn"
    clean_text = "".join(re.findall(r'[\u4e00-\u9fff。]', text))
    
    if not clean_text:
        return None

    # BƯỚC 2: ÉP SSML CHUẨN TRUNG QUỐC
    # Dấu 。 sẽ được thay bằng lệnh nghỉ 1.2 giây
    processed_text = clean_text.replace("。", " <break time='1200ms'/> ")
    
    ssml_text = f"""
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='zh-CN'>
        <voice name='{VOICE}'>
            <prosody rate='{RATE}' pitch='{PITCH}'>
                {processed_text}
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
    if text_input.strip():
        with st.spinner('AI đang khởi động...'):
            audio = asyncio.run(generate_audio(text_input))
            if audio:
                st.audio(audio)
            else:
                st.error("Lỗi: Không tìm thấy chữ Hán nào!")
