import streamlit as st
import edge_tts
import asyncio
import re
import unicodedata

st.set_page_config(page_title="Hán Ngữ Engine Sạch", layout="centered")
st.title("🎙️ Cỗ Máy Phát Âm Hán Ngữ 0.5 (Auto-Clean)")

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-50%" 
PITCH = "+5Hz"

text_input = st.text_area("Dán nội dung vào đây (App sẽ tự động 'rửa' sạch rác):", height=200)

async def generate_audio(text):
    if not text.strip(): return None
    
    # BƯỚC 1: "RỬA" VĂN BẢN - Loại bỏ định dạng ẩn và chuẩn hóa Unicode
    text = unicodedata.normalize('NFKC', text)
    
    # BƯỚC 2: CHỈ GIỮ CHỮ HÁN VÀ DẤU CHẤM TRUNG QUỐC
    clean_text = "".join(re.findall(r'[\u4e00-\u9fff。]', text))
    
    if not clean_text: return None

    # BƯỚC 3: ÉP ĐỌC THEO CỤM (NGÔN NGỮ) KHÔNG ĐÁNH VẦN
    ssml_text = f"""
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='zh-CN'>
        <voice name='{VOICE}'>
            <prosody rate='{RATE}' pitch='{PITCH}'>
                <p>{clean_text.replace("。", " <break time='1000ms'/> ")}</p>
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
    with st.spinner('Đang thanh lọc dữ liệu...'):
        audio = asyncio.run(generate_audio(text_input))
        if audio:
            st.audio(audio)
        else:
            st.error("Không tìm thấy chữ Hán hợp lệ!")
