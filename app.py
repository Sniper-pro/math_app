import streamlit as st
import random
import os
import time

# 音を鳴らす関数
def play_sound(file_name):
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
    if st.button("最初の画面にもどる"): st.session_state.page = "home"; st.rerun()

elif st.session_state.page == "math":
    if not st.session_state.game_over:
        st.markdown(f"## {st.session_state.count + 1}問目")
        st.markdown(f"<h1 style='text-align: center; font-size: 50px;'>{st.session_state.a} ＋ {st.session_state.b} ＝ ？</h1>", unsafe_allow_html=True)
        
        # キーボード入力を排除し、ドロップダウンのみに限定
        user_ans = st.selectbox("こたえをえらんでね", list(range(0, 21)), key="ans")
        
        if st.button("こたえあわせ"):
            ans = st.session_state.a + st.session_state.b
            if user_ans == ans:
                st.success("せいかい！")
                play_sound('correct.mp3') # 正解の音を呼び出し
                st.session_state.score += 1
            else:
                st.error("ざんねん！")
                play_sound('incorrect.mp3') # 不正解の音を呼び出し
                
                # 5の分解解説ロジック
                a, b = st.session_state.a, st.session_state.b
                a_5 = a - 5
                b_5 = b - 5
                hint = (f"{a} は 5 と {a_5} に わかれるよ。<br>"
                        f"{b} は 5 と {b_5} に わかれるよ。<br>"
                        f"5 と 5 で 10 になるね。<br>"
                        f"のこりの {a_5} と {b_5} を たすと {a_5 + b_5} になるね。<br>"
                        f"あわせて {ans} だよ！")
                
                st.session_state.wrong_list.append({'q': f"{a}+{b}", 'ans': ans, 'hint': hint})
            
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
            # ボタン名を「かいせつ」に変更
            with st.expander(f"{item['q']} の かいせつ"):
                st.write(f"答え: {item['ans']}")
                st.markdown(item['hint'], unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("もういちどあそぶ"): init_game(st.session_state.total_questions); st.rerun()
        with col2:
            if st.button("最初の画面にもどる"): st.session_state.page = "home"; st.rerun()