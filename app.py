import streamlit as st
from data.data import buy_cofee

def card_with_callable(content_html="", callable_inside=None):
    """Tworzy kartę z HTML i opcjonalną funkcją Streamlit wewnątrz."""
    with st.container():
        # cała karta w jednym div
        st.markdown(f"""
        <div style="
            background-color: #f9f9f9; 
            border-radius: 15px; 
            padding: 20px; 
            margin-bottom: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        ">
            {content_html}
        </div>
        """, unsafe_allow_html=True)
        
        # wywołanie np. buy_cofee() pod HTML w tym samym container
        if callable_inside:
            callable_inside()

# przykładowe użycie
card_with_callable('<h3 style="text-align:center;">📊 Statystyki i przewidywania ligowe 📊</h3>')
card_with_callable('<h3 style="text-align:center;">⚽️ Statystyki i przewidywania zespołowe ⚽️</h3>')

newsletter_html = """
<p>Chcemy stworzyć kurs, w którym pokażemy jak zostać analitycznym magikiem...</p>
<iframe data-w-type="embedded" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"
src="https://sy0kh.mjt.lu/wgt/sy0kh/0phq/form?c=f6f3e641" width="100%" style="height: 400px;"></iframe>
<script type="text/javascript" src="https://app.mailjet.com/pas-nc-embedded-v1.js"></script>
"""
card_with_callable(newsletter_html)

coffee_html = "<p>☕ Wspomóż naszą pracę i rozwój kursu!</p>"
card_with_callable(coffee_html, buy_cofee)
