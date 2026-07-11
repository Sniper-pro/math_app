import streamlit as st
import random

# タイトル
st.title("けいさんけいさん！")

# 初期化
if 'a' not in st.session_state:
    st.session_state.a = random.randint(1, 9)
    st.session_state.b = random.randint(1, 9)
    st.session_state.msg = ""

def check():
    if st.session_state.user_input == (st.session_state.a + st.session_state.b):
        st.session_state.msg = "せいかい！すごい！"
        st.session_state.a = random.randint(1, 9)
        st.session_state.b = random.randint(1, 9)
    else:
        st.session_state.msg = "ざんねん、もういちど！"

st.subheader(f"{st.session_state.a} ＋ {st.session_state.b} は？")
st.number_input("こたえをいれてね", min_value=0, max_value=20, key="user_input", on_change=check)
st.write(st.session_state.msg)