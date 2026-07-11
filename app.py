import streamlit as st
import random
import os

# 音を鳴らす関数
def play_sound(file_path):
    if os.path.exists(file_path):
        audio_file = open(file_path, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')

st.title("おべんきょうドリル")

# 冒頭の選択画面
if 'page' not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    st.subheader("やりたいことをえらんでね")
    if st.button("さんすう"):
        st.session_state.page = "math"
        st.rerun()
    if st.button("こくご"):
        st.session_state.page = "japanese"
        st.rerun()

elif st.session_state.page == "math":
    st.header("さんすう")
    if 'a' not in st.session_state:
        st.session_state.a = random.randint(1, 9)
        st.session_state.b = random.randint(1, 9)
    
    st.write(f"{st.session_state.a} ＋ {st.session_state.b} ＝ ？")
    user_input = st.number_input("こたえ", key="ans", min_value=0)
    
    if st.button("こたえあわせ"):
        if user_input == (st.session_state.a + st.session_state.b):
            st.success("せいかい！")
            play_sound('sound/correct.mp3')
            del st.session_state.a
            st.rerun()
        else:
            st.error("もういちど！")