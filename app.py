import streamlit as st
import random
import os
import time
import base64

# 音を鳴らす関数（HTMLで非表示再生する仕組みに変更し、バーを消去・バグを解消）
def play_sound(file_name):
    path = f'sound/{file_name}'
    if os.path.exists(path):
        with open(path, 'rb') as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            # プレイヤーを表示せず、裏側で自動再生させるHTMLタグ
            md = f"""
                <audio autoplay style="display:none;">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            st.markdown(md, unsafe_allow_html=True)
            time.sleep(2.0)

def init_game(total_questions, grade):
    st.session_state.count = 0
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.wrong_list = []
    st.session_state.total_questions = total_questions
    st.session_state.grade = grade
    generate_question()

def generate_question():
    st.session_state.a = random.randint(1, 9)
    st.session_state.b = random.randint(1, 9)

# 1年生向けの「5のまとまり」解説を生成する安全な関数
def generate_hint(a, b, ans):
    if a >= 5 and b >= 5:
        return (f"{a} は 5 と {a - 5} に わかれるね。<br>"
                f"{b} は 5 と {b - 5} に わかれるね。<br>"
                f"5 と 5 で 10 になるよ。<br>"
                f"のこりの {a - 5} と {b - 5} を たすと {(a - 5) + (b - 5)} だね。<br>"
                f"10 と あわせて {ans} になるよ！")
    elif a >= 5 and b < 5:
        return (f"{a} は 5 と {a - 5} に わかれるね。<br>"
                f"のこりの {a - 5} と {b} を たすと {(a - 5) + b} だね。<br>"
                f"5 と あわせて {ans} になるよ！")
    elif a < 5 and b >= 5:
        return (f"{b} は 5 と {b - 5} に わかれるね。<br>"
                f"{a} と のこりの {b - 5} を たすと {a + (b - 5)} だね。<br>"
                f"5 と あわせて {ans} になるよ！")
    else:
        return f"{a}こ と {b}こ を あわせると {ans}こ になるよ。ゆびを つかって かぞえてみよう！"

if 'page' not in st.session_state: st.session_state.page = "home"

# --- 画面構成 ---
if st.session_state.page == "home":
    st.title("おべんきょうドリル")
    st.subheader("やりたいことをえらんでね")
    if st.button("さんすう"): st.session_state.page = "subject"; st.rerun()

elif st.session_state.page == "subject":
    st.header("さんすう：学年をえらんでね")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("1年生"): st.session_state.grade_select = 1; st.session_state.page = "setup"; st.rerun()
        if st.button("2年生"): st.warning("2年生はまだ準備中です！")
    with col2:
        if st.button("3年生〜6年生"): st.warning("準備中です！")
    
    st.write("---")
    if st.button("最初の画面にもどる"): st.session_state.page = "home"; st.rerun()

elif st.session_state.page == "setup":
    st.header(f"{st.session_state.grade_select}年生のさんすう")
    total = st.radio("もんだいすう をえらんでね", [5, 10])
    
    if st.button("スタート！"):
        init_game(total, st.session_state.grade_select)
        st.session_state.page = "math"
        st.rerun()
    
    st.write("---")
    if st.button("最初の画面にもどる"): st.session_state.page = "home"; st.rerun()

elif st.session_state.page == "math":
    if not st.session_state.game_over:
        st.markdown(f"## {st.session_state.count + 1}問目")
        st.markdown(f"<h1 style='text-align: center; font-size: 50px;'>{st.session_state.a} ＋ {st.session_state.b} ＝ ？</h1>", unsafe_allow_html=True)
        
        # キーボード起動を完全に防ぐため、スライダー（つまみ）方式に変更
        user_ans = st.slider("こたえ を あわせてね", min_value=0, max_value=20, value=0, key="ans")
        
        if st.button("こたえあわせ"):
            ans = st.session_state.a + st.session_state.b
            if user_ans == ans:
                st.success("せいかい！")
                play_sound('correct.mp3')
                st.session_state.score += 1
            else:
                st.error("ざんねん！")
                play_sound('incorrect.mp3') # 修正・独立させた不正解音の呼び出し
                hint = generate_hint(st.session_state.a, st.session_state.b, ans)
                st.session_state.wrong_list.append({'q': f"{st.session_state.a} ＋ {st.session_state.b}", 'ans': ans, 'hint': hint})
            
            st.session_state.count += 1
            if st.session_state.count >= st.session_state.total_questions:
                st.session_state.game_over = True
            else:
                generate_question()
            st.rerun()
    else:
        st.header("おつかれさま！")
        st.write(f"{st.session_state.total_questions}問中 {st.session_state.score}問 正解！")
        
        if st.session_state.wrong_list:
            st.write("---")
            st.write("ふくしゅう しよう！")
            for i, item in enumerate(st.session_state.wrong_list):
                with st.expander(f"{item['q']} の かいせつ"):
                    st.write(f"答え: {item['ans']}")
                    st.markdown(item['hint'], unsafe_allow_html=True)
        
        st.write("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("もういちどあそぶ"): init_game(st.session_state.total_questions, st.session_state.grade); st.rerun()
        with col2:
            if st.button("最初の画面にもどる"): st.session_state.page = "home"; st.rerun()