import streamlit as st
import random
import os
import time

def play_sound(file_name):
    path = f'sound/{file_name}'
    if os.path.exists(path):
        audio_file = open(path, 'rb')
        st.audio(audio_file.read(), format='audio/mp3', autoplay=True)
        time.sleep(2.0)

def init_game():
    st.session_state.count = 0
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.wrong_list = []  # 間違えた問題を保存するリスト
    generate_question()

def generate_question():
    st.session_state.a = random.randint(1, 9)
    st.session_state.b = random.randint(1, 9)

if 'count' not in st.session_state:
    init_game()

st.title("おべんきょうドリル")

if not st.session_state.game_over:
    st.markdown(f"<h2 style='text-align: center;'>{st.session_state.count + 1}問目</h2>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; font-size: 60px;'>{st.session_state.a} ＋ {st.session_state.b} ＝ ？</h1>", unsafe_allow_html=True)
    
    user_ans = st.selectbox("こたえをえらんでね", list(range(0, 21)), key="user_choice")
    
    if st.button("こたえあわせ"):
        correct_ans = st.session_state.a + st.session_state.b
        if user_ans == correct_ans:
            st.success("せいかい！")
            play_sound('correct.mp3')
            st.session_state.score += 1
        else:
            st.error("ざんねん！")
            play_sound('incorrect.mp3')
            # 間違えた問題と解説をリストに追加
            st.session_state.wrong_list.append({
                'q': f"{st.session_state.a} ＋ {st.session_state.b}",
                'ans': correct_ans,
                'hint': f"{st.session_state.a}こ と {st.session_state.b}こ を あわせると {correct_ans}こ になるよ。"
            })
        
        st.session_state.count += 1
        if st.session_state.count >= 10:
            st.session_state.game_over = True
        else:
            generate_question()
        st.rerun()

else:
    st.header("おつかれさま！")
    st.subheader(f"10もんちゅう {st.session_state.score}もん せいかいでした！")
    
    if st.session_state.wrong_list:
        st.write("---")
        st.write("復習しよう！間違えた問題はこちら：")
        for i, item in enumerate(st.session_state.wrong_list):
            with st.expander(f"{i+1}問目: {item['q']} ＝ ？"):
                st.write(f"答えは {item['ans']} です。")
                st.write(item['hint'])
    
    if st.button("もういちどあそぶ"):
        init_game()
        st.rerun()