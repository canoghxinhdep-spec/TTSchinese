import streamlit as st
import edge_tts
import asyncio

# Tối ưu giao diện cho điện thoại và máy tính
st.set_page_config(page_title="Hán Ngữ 0.5 Pro", page_icon="🎙️")
st.title("🎙️ Đài Phát Thanh Tiếng Trung 0.5")
st.markdown("---")

# Ô nhập giáo án (Dán bản "Sạch" của bạn vào đây)
txt = st.text_area("Dán Hán tự vào đây để luyện nghe:", height=300, placeholder="Ví dụ: 1. 安 (ān). 山 (shān).")

async def play_audio():
    if st.button("🔊 BẮT ĐẦU ĐỌC (GIỌNG CHUẨN AI)"):
        if txt.strip():
            with st.spinner('AI đang khởi tạo giọng đọc...'):
                # rate="-50%" là chìa khóa để nghe chậm chuẩn 0.5
                communicate = edge_tts.Communicate(txt, "zh-CN-XiaoxiaoNeural", rate="-50%")
                audio_data = b""
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_data += chunk["data"]
                
                # Trình phát nhạc
                st.audio(audio_data, format='audio/mp3')
                
                # Nút tải file về máy
                st.download_button(
                    label="📥 TẢI FILE MP3 VỀ MÁY",
                    data=audio_data,
                    file_name="hoc_phat_am_05.mp3",
                    mime="audio/mp3"
                )
        else:
            st.error("Lỗi: Bạn chưa dán nội dung chữ Hán!")

if __name__ == "__main__":
    asyncio.run(play_audio())
