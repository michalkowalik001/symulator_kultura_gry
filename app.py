import streamlit as st
import os
import pandas as pd
from data.data import buy_cofee
from utils.sidebar import show_sidebar
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Symulator Ligi Polskiej",
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
    background-color: #f9f9f9; 
    border-radius: 15px; 
    padding: 30px; 
    margin-bottom: 20px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    text-align: center;
    font-size: 24px;
    color: #333;
">
    <a href="{url}" target="_blank" style="
        text-decoration: none;
        color: inherit;
        font-weight: bold;
    ">
        {emoji} {text}
    </a>
</div>
"""
st.markdown(
    card_style.format(
        url="#",  # albo inny link, np. "https://ekstraklasa.org"
        emoji="⚽",
        text="Symulator Ekstraklasy. Wybierz tryb:"
    ),
    unsafe_allow_html=True
)


st.markdown(
    card_style.format(
        url="https://symulator-kultura-gry.streamlit.app/~/+/eklapa_streamlit_2",
        emoji="📊",
        text="Statystyki i przewidywania ligowe"
    ),
    unsafe_allow_html=True
)

st.markdown(
    card_style.format(
        url="https://symulator-kultura-gry.streamlit.app/~/+/eklapa_klub_site",
        emoji="⚽️",
        text="Statystyki i przewidywania klubowe"
    ),
    unsafe_allow_html=True
)



# Pierwsza karta - ankieta i newsletter
html_code = """
<iframe data-w-type="embedded" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"
src="https://sy0kh.mjt.lu/wgt/sy0kh/0phq/form?c=f6f3e641" width="100%" style="height: 500px;"></iframe>

<script type="text/javascript" src="https://app.mailjet.com/pas-nc-embedded-v1.js"></script>
"""

content_1 = """
<p><b>Chcemy stworzyć kurs, w którym pokażemy jak zostać analitycznym magikiem i symulować wyniki meczów i rozgrywek ligowych.</b></p>

<p>Niezależnie czy analizujesz dane na co dzień, czy jesteś zupełnie zielony i nie masz pojęcia jak się do tego zabrać. Przeprowadzimy Cię przez cały proces od A do Z.</p>

<p>Najpierw jednak musimy dowiedzieć się więcej o Tobie i Twoich potrzebach.</p>

<p>📄📄📄<b><a href="https://docs.google.com/forms/d/e/1FAIpQLSe9c5tmRgRBUVGWg2EGZorGY6Akd4O4bHsrEMFCFcleI-pyYA/viewform?usp=dialog" target="_blank">Wypełnij krótką  ankietę</a></b> 📄📄📄</p>

<p><b>⬇️ Lub zapisz się na newsletter, w którym wyślemy Ci postępy w tworzeniu kursu ⬇️</b></p>
"""

# wstawiamy zawartość bezpośrednio, używając f-string z podwójnymi klamrami w card_style
st.markdown(f"""
<div style="
    background-color: #f9f9f9; 
    border-radius: 15px; 
    padding: 20px; 
    margin-bottom: 20px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    text-align: center;
    font-size: 18px;
">
    {content_1}
</div>
""", unsafe_allow_html=True)

components.html(html_code, height=400, scrolling=False)
