import streamlit as st
from data.data import buy_cofee
from utils.sidebar import show_sidebar
import streamlit.components.v1 as components

st.set_page_config(
    page_title="EKSTRAKLASOWE PRZEWIDYWANIA",
    layout="wide"
)

# Ukrycie domyślnego sidebaru
hide_default_sidebar = """
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_default_sidebar, unsafe_allow_html=True)

show_sidebar()

# Funkcja do tworzenia karty
def card(content):
    st.markdown(f"""
    <div style="
        background-color: #f9f9f9; 
        border-radius: 15px; 
        padding: 20px; 
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    ">
        {content}
    </div>
    """, unsafe_allow_html=True)

# Pierwsze dwie karty ze statystykami
content_stats_liga = """
<h3 style="text-align:center;">📊 Statystyki i przewidywania ligowe 📊</h3>
"""
content_stats_zespol = """
<h3 style="text-align:center;">⚽️ Statystyki i przewidywania zespołowe ⚽️</h3>
"""

card(content_stats_liga)
card(content_stats_zespol)

# Trzecia karta - ankieta i newsletter (iframe w środku)
content_newsletter = """
<p><b>Chcemy stworzyć kurs, w którym pokażemy jak zostać analitycznym magikiem i być w stanie przewidywać i symulować wyniki meczów i rozgrywek ligowych. To wcale nie takie trudne.</b></p>

<p>Niezależnie czy analizujesz dane na co dzień, czy jesteś zupełnie zielony i nie masz pojęcia jak się do tego zabrać. Przeprowadzimy Cię przez cały proces od A do Z.</p>

<p>Najpierw jednak musimy dowiedzieć się więcej o Tobie i Twoich potrzebach.</p>

<p>📄 <b>Wypełnij krótką <a href="https://docs.google.com/forms/d/e/1FAIpQLSe9c5tmRgRBUVGWg2EGZorGY6Akd4O4bHsrEMFCFcleI-pyYA/viewform?usp=dialog" target="_blank">ankietę</a></b> 📄</p>

<p><b>Lub zapisz się na newsletter, w którym wyślemy Ci postępy w tworzeniu kursu!</b></p>

<iframe data-w-type="embedded" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"
src="https://sy0kh.mjt.lu/wgt/sy0kh/0phq/form?c=f6f3e641" width="100%" style="height: 400px;"></iframe>
<script type="text/javascript" src="https://app.mailjet.com/pas-nc-embedded-v1.js"></script>
"""

card(content_newsletter)


with st.container():
    # styl karty
    st.markdown("""
    <div style="
        background-color: #f9f9f9; 
        border-radius: 15px; 
        padding: 20px; 
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        text-align: center;
    ">
        <p>☕ Wspomóż naszą pracę i rozwój kursu!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # wywołanie przycisku buy_coffee w tym samym container
    buy_cofee()
