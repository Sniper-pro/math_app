import streamlit as st
import random
import os
import time

def play_sound(file_name):
    # ファイル名が正しいか必ず確認してください
    path = f'sound/{file_name}'
    if os.path.exists(path):
        audio_file = open(path, 'rb')
        st.audio(audio_file.read(), format='audio/mp3', autoplay=True)
        time.sleep(2.0)

def init_game(total_questions):
    st.session_state.count = 0
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.wrong_list = []
    st.session_state.total_questions = total_questions
    generate_question()

def generate_question():
    st.session_state.a = random.randint(1, 9)
    st.session_state.b = random.randint(1, 9)

if 'page' not in st.session_state: st.session_state.page = "home"

# --- 画面構成 ---
if st.session_state.page == "home":
    st.title("おべんきょうドリル")
    if st.button("さんすう"): st.session_state.page = "setup"; st.rerun()

elif st.session_state.page == "setup":
    st.header("設定をえらんでね")
    total = st.radio("もんだいすう", [5, 10])
    if st.button("スタート！"):
        init_game(total)
        st.session_state.page = "math"
        st.rerun()

elif st.session_state.page == "math":
    if not st.session_state.game_over:
        st.markdown(f"## {st.session_state.count + 1}問目")
        st.markdown(f"<h1 style='text-align: center; font-size: 50px;'>{st.session_state.a} ＋ {st.session_state.b} ＝ ？</h1>", unsafe_allow_html=True)
        
        user_ans = st.selectbox("こたえ", list(range(0, 21)), key="ans")
        if st.button("こたえあわせ"):
            ans = st.session_state.a + st.session_state.b
            if user_ans == ans:
                st.success("せいかい！")
                play_sound('correct.mp3') # 正解の音
                st.session_state.score += 1
            else:
                st.error("ざんねん！")
                play_sound('incorrect.mp3') # 不正解の音
                # 10の分解解説ロジック
                diff = 10 - st.session_state.a
                remainder = st.session_state.b - diff
                hint = f"{st.session_state.a} に {diff} をたすと 10 になるね。<br>のこりの {remainder} を たすと {ans} になるよ！"
                st.session_state.wrong_list.append({'q': f"{st.session_state.a}+{st.session_state.b}", 'ans': ans, 'hint': hint})
            
            st.session_state.count += 1
            if st.session_state.count >= st.session_state.total_questions:
                st.session_state.game_over = True
            else:
                generate_question()
            st.rerun()
    else:
        st.header("おつかれさま！")
        st.write(f"{st.session_state.total_questions}問中 {st.session_state.score}問 正解！")
        for i, item in enumerate(st.session_state.wrong_list):
            with st.expander(f"{item['q']} の かんがえかた"):
                st.write(f"答え: {item['ans']}")
                st.markdown(item['hint'], unsafe_allow_html=True)
        if st.button("もういちど"): st.session_state.page = "home"; st.rerun()