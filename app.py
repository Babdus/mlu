import streamlit as st
from io import StringIO
from transliterate import transliterate_chat_file


st.title('Transliteration')

uploaded_file = st.file_uploader('Choose CHAT file', type=['cha'], key=1)
if uploaded_file is not None:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = stringio.read()
    new_string_data = transliterate_chat_file(string_data)

    st.download_button('Download transliterated CHAT file', new_string_data, file_name='kat_'+uploaded_file.name, key=2)