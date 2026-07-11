import streamlit as st
import random
import os

# 音を鳴らすための改良関数
def play_correct_sound():
    if os.path.exists('sound/correct.mp3'):
        # 音データを読み込む
        audio_file = open('sound/correct.mp3', 'rb')
        audio_bytes = audio_file.read()
        # autoplayをTrueにし、ユーザーの操作に合わせて実行されるようにする
        st.audio(audio_bytes, format='audio/mp3', autoplay=True)

st.title("おべんきょうドリル")

if 'page' not in st.session_state: st.session_state.page = "home"
if 'grade' not in st.session_state: st.session_state.grade = None

if st.session_state.page == "home":
    st.subheader("やりたいことをえらんでね")
    if st.button("さんすう"): st.session_state.page = "subject"; st.rerun()
    if st.button("こくご"): st.session_state.page = "japanese"; st.rerun()

elif st.session_state.page == "subject":
    st.header("さんすう：学年をえらんでね")
    if st.button("1年生"): st.session_state.grade = 1; st.session_state.page = "math"; st.rerun()
    # 2年生以降のボタンはレイアウト調整のため簡略化
    if st.button("2年生"): st.session_state.grade = 2; st.session_state.page = "math"; st.rerun()
    if st.button("もどる"): st.session_state.page = "home"; st.rerun()

elif st.session_state.page == "math":
    if st.session_state.grade == 1:
        st.header("1年生のさんすう")
        if 'a' not in st.session_state:
            st.session_state.a = random.randint(1, 9)
            st.session_state.b = random.randint(1, 9)
        
        st.write(f"{st.session_state.a} ＋ {st.session_state.b} ＝ ？")
        user_ans = st.number_input("こたえ", key="ans", min_value=0)
        
        # こたえあわせボタンを押した時に音が鳴るようにする
        if st.button("こたえあわせ"):
            if user_ans == (st.session_state.a + st.session_state.b):
                st.success("せいかい！")
                play_correct_sound()
                del st.session_state.a
            else:
                st.error("もういちど！")
    else:
        st.write(f"{st.session_state.grade}年生は準備中です。")
    
    if st.button("もどる"): st.session_state.page = "subject"; st.rerun()