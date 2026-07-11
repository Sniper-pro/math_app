import streamlit as st
import random
import os

# 音を鳴らす汎用関数
def play_sound(file_name):
    path = f'sound/{file_name}'
    if os.path.exists(path):
        audio_file = open(path, 'rb')
        st.audio(audio_file.read(), format='audio/mp3', autoplay=True)

st.title("おべんきょうドリル")

if 'page' not in st.session_state: st.session_state.page = "home"

if st.session_state.page == "home":
    if st.button("さんすう"): st.session_state.page = "math_grade"; st.rerun()

elif st.session_state.page == "math_grade":
    st.header("学年をえらんでね")
    if st.button("1年生"): st.session_state.grade = 1; st.session_state.page = "math"; st.rerun()

elif st.session_state.page == "math":
    st.header("1年生のさんすう")
    if 'a' not in st.session_state:
        st.session_state.a = random.randint(1, 9)
        st.session_state.b = random.randint(1, 9)
    
    # 巨大なフォントで問題を表示
    st.markdown(f"<h1 style='text-align: center; font-size: 60px;'>{st.session_state.a} ＋ {st.session_state.b} ＝ ？</h1>", unsafe_allow_html=True)
    
    # タップしやすいドロップダウン（0〜20まで）
    options = list(range(0, 21))
    user_ans = st.selectbox("こたえをえらんでね", options)
    
    if st.button("こたえあわせ"):
        if user_ans == (st.session_state.a + st.session_state.b):
            st.success("せいかい！")
            play_sound('correct.mp3')
            del st.session_state.a
        else:
            st.error("もういちど！")
            play_sound('incorrect.mp3')

    if st.button("もどる"): st.session_state.page = "math_grade"; st.rerun()