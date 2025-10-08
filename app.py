import streamlit as st
import os
import pandas as pd
from data.data import buy_cofee
from utils.sidebar import show_sidebar
import streamlit.components.v1 as components

st.set_page_config(
    page_title="EKSTRAKLASOWE PRZEWIDYWANIA",
    layout="wide"
)

hide_default_sidebar = """
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_default_sidebar, unsafe_allow_html=True)

show_sidebar()

card_style = """
<div style="
    background-color: #f0f0f0; 
    border-radius: 15px; 
    padding: 20px; 
    text-align: center; 
    transition: transform 0.2s;
    margin-bottom: 20px;
">
    <a href="{url}" target="_blank" style="text-decoration: none; color: #000000;">
        <h3 style="margin: 0;">{emoji} {text} {emoji}</h3>
    </a>
</div>
"""

st.markdown(
    card_style.format(
        url="https://twoja-strona.pl",
        emoji="📊",
        text="Statystyki i przewidywania ligowe"
    ),
    unsafe_allow_html=True
)

# Odstęp między kartami
st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

st.markdown(
    card_style.format(
        url="https://twoja-strona.pl",
        emoji="⚽️",
        text="Statystyki i przewidywania zespołowe"
    ),
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    html_code = """
    <iframe data-w-type="embedded" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"
    src="https://sy0kh.mjt.lu/wgt/sy0kh/0phq/form?c=f6f3e641" width="100%" style="height: 500px;"></iframe>

    <script type="text/javascript" src="https://app.mailjet.com/pas-nc-embedded-v1.js"></script>
    """
    with st.container(border = False):
        st.markdown("""
            **Chcemy stworzyć kurs, w którym pokażemy jak zostać analitycznym magikiem i być w stanie przewidywać symulować wyniki meczów i rozgrywek ligowych. To wcale nie takie trudne.**
            
            Niezależnie czy analizujesz dane na codzień, czy jesteś zupełnie zielony i nie masz pojęcia jak się do tego zabrać. Przeprowadzimy Cię przez cały proces od A do Z.
            
            Najpierw jednak musimy dowiedzieć się więcej o Tobie i Twoich potrzebach. 

            📄 **Wypełnij krótką [ankietę](https://docs.google.com/forms/d/e/1FAIpQLSe9c5tmRgRBUVGWg2EGZorGY6Akd4O4bHsrEMFCFcleI-pyYA/viewform?usp=dialog)** 📄
            
            **Lub zapisz się na newsletter, w którym wyślemy Ci postępy w tworzeniu kursu!**
        """)
        components.html(html_code, height=400, scrolling=False)


with col2:
    with st.container(border = False):
        buy_cofee()

