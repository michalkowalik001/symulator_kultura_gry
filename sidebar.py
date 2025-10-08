import streamlit as st
import base64
import streamlit.components.v1 as components

def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()
    
twitter_icon = image_to_base64("/Users/michalkowalik/Desktop/Kultura Gry/Struktura/twitter.png")

instagram_icon = image_to_base64("/Users/michalkowalik/Desktop/Kultura Gry/Struktura/instagram.png")

facebook_icon = image_to_base64("/Users/michalkowalik/Desktop/Kultura Gry/Struktura/facebook.png")

html_code = """
    <iframe data-w-type="embedded" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"
    src="https://sy0kh.mjt.lu/wgt/sy0kh/0phq/form?c=f6f3e641" width="100%" style="height: 500px;"></iframe>

    <script type="text/javascript" src="https://app.mailjet.com/pas-nc-embedded-v1.js"></script>
    """

def show_sidebar():
    # ----- SIDEBAR -----
    st.sidebar.image("/Users/michalkowalik/Desktop/Kultura Gry/Logo/logo_czarne.png", width=600)

    st.sidebar.markdown("### Nawigacja")
    st.sidebar.markdown("- Strona główna")
    st.sidebar.markdown("- Statystyki i przewidywania ligowe")
    st.sidebar.markdown("- Statystyki i przewidywania klubowe")
    st.sidebar.markdown("- Kontakt")
    st.sidebar.markdown("- Metodologia")

    st.sidebar.markdown("---")

    st.sidebar.write('Podoba Ci się nasz symulator ligowy? Stworzenie go pochłonęło sporo pracy. Wesprzyj nas, stawiając nam wirtualną kawę!')
    
    st.sidebar.markdown(
            """
            <div style="text-align:center;">
                <a href="https://buycoffee.to/kulturagry" target="_blank">
                    <img src="https://buycoffee.to/img/share-button-primary.png" 
                        style="width: 200px; height: 52px;" 
                        alt="Postaw mi kawę na buycoffee.to">
                </a>
            </div>
            """,
            unsafe_allow_html=True
    )

    st.sidebar.markdown("---")

    st.sidebar.markdown("""
            **Chcemy stworzyć kurs, w którym pokażemy jak symulować wyniki meczów i rozgrywek. To wcale nie takie trudne.**
            
            Najpierw jednak musimy dowiedzieć się więcej o Tobie i Twoich potrzebach. 

            📄 **[Wypełnij krótką ankietę](https://docs.google.com/forms/d/e/1FAIpQLSe9c5tmRgRBUVGWg2EGZorGY6Akd4O4bHsrEMFCFcleI-pyYA/viewform?usp=dialog)** 📄
        """)
    

    
    st.sidebar.markdown("---")

    st.sidebar.markdown(
    f"""
    <div style="text-align:center; margin-top:10px;">
        <a href="https://x.com/kulturagrypl" target="_blank" style="margin:0 8px;">
            <img src="data:image/png;base64,{twitter_icon}" width="32" alt="Twitter">
        </a>
        <a href="https://www.instagram.com/kulturagry.pl/" target="_blank" style="margin:0 8px;">
            <img src="data:image/png;base64,{instagram_icon}" width="32" alt="Twitter">
        </a>
        <a href="https://www.facebook.com/profile.php?id=61581258330019" target="_blank" style="margin:0 8px;">
            <img src="data:image/png;base64,{facebook_icon}" width="32" alt="Twitter">
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

