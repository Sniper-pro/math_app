import streamlit as st
import random
import os

def play_sound(file_name):
    path = f'sound/{file_name}'
    if os.path.exists(path):
        audio_file = open(path, 'rb')
        st.audio(audio_file.read(), format='audio/mp3', autoplay=True)

st.title("おべんきょうドリル")

# 初期化関数
def init_game():
    st.session_state.count = 0  # 現在の問題数
    st.session_state.score = 0  # 正解数
    st.session_state.game_over = False
    generate_question()

def generate_question():
    st.session_state.a = random.randint(1, 9)
    st.session_state.b = random.randint(1, 9)
    st.session_state.ans_check = None # 直前の判定状態をリセット

if 'count' not in st.session_state: init_game()

if st.session_state.count < 10:
    st.markdown(f"<h2 style='text-align: center;'>{st.session_state.count + 1}問目</h2>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; font-size: 60px;'>{st.session_state.a} ＋ {st.session_state.b} ＝ ？</h1>", unsafe_allow_html=True)
    
    user_ans = st.selectbox("こたえをえらんでね", list(range(0, 21)), key="user_choice")
    
    if st.button("こたえあわせ"):
        if user_ans == (st.session_state.a + st.session_state.b):
            st.success("せいかい！")
            play_sound('correct.mp3')
            st.session_state.score += 1
        else:
            st.error("ざんねん！")
            play_sound('incorrect.mp3')
        
        st.session_state.count += 1
        if st.session_state.count < 10:
            generate_question()
            st.rerun()
        else:
            st.session_state.game_over = True
            st.rerun()

else:
    st.header("おつかれさま！")
    st.subheader(f"10もんちゅう {st.session_state.score}もん せいかいでした！")
    if st.button("もういちどあそぶ"):
        init_game()
        st.rerun()