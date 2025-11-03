import streamlit as st
st.title( '나의 첫 웹 서비스 만들기')
name=st.text_input('하하:')
menu=st.selectbox('뭘봐?:',['미안...',꼽냐?'])
if st.button('너 왜 웃니?'):
  st.info(name+'와우!')
  st.warning(menu+'ㅋㅋ?')
      
  st.balloons()
