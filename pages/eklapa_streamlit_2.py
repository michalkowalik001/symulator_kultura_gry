import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from data.data import df, df1, df2, df3, df4, df5, df6, calculate_elo_wdl, performance_viz
from utils.sidebar import show_sidebar
import streamlit.components.v1 as components

st.set_page_config(layout="centered")

# Ukryj domyślny sidebar z multipage navigation
hide_default_sidebar = """
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_default_sidebar, unsafe_allow_html=True)

show_sidebar()

st.title("Statystyki i przewidywania ligowe")


#styl tabeli
table_style = """
<style>
table {
    width: 100%;
    border-collapse: collapse;
    font-family: sans-serif;
    font-size: 12px !important;
}
th, td {
    text-align: center !important;
    padding: 8px;
}
th {
    font-weight: bold;
    background-color: #e0e0e0;  /* szare tło nagłówków */
}
/* obramowanie tabeli i komórek */
table, th, td {
    border: 1px solid #ddd;
}
/* kolorowanie co drugiego wiersza danych (nie nagłówków) */
tr:nth-child(even) td {
    background-color: #f0f0f0;
}
</style>
"""

table_style_1 = """
<style>
table {
    width: 100%;
    border-collapse: collapse;
    font-family: sans-serif;
    font-size: 12px !important;
}
th, td {
    text-align: center !important;
    padding: 8px;
}
th {
    font-weight: bold;
    background-color: #e0e0e0;  /* szare tło nagłówków */
}
/* obramowanie tabeli i komórek */
table, th, td {
    border: 1px solid #ddd;
}
/* kolorowanie co drugiego wiersza danych (nie nagłówków) */
tr:nth-child(even) td {
    background-color: #f0f0f0;
}
</style>
"""

# Wczytanie danych
df = df()
df1 = df1()
df1.rename(columns = {"Team":"Drużyna", "exp_points":"Oczekiwane punkty", "elo":"ELO"}, inplace = True)

df2 = df2().head(10)
df2.rename(columns = {'Home':'Gospodarz','Away':'Gość','Date':'Data', 'Day':"Dzień", "Time":"Czas", "Kolejka":"Wk", "HomeElo":"Gospodarz ELO",	
                      "AwayElo":"Gość ELO", "p_home_win":"Szansa gospodarz", "p_draw":"Szansa remis", "p_away_win":"Szansa gość"}, inplace = True)

df3 = df3()
df3['Pozycja'] = range(1, len(df3) + 1)
df3.rename(columns = {'Pos':'Obecna pozycja', 'Team':'Drużyna', 'Matches':"Mecze", 'Wins':"Wygrane", "Draws":"Remisy", "Losses":"Porażki", "Points":'Punkty','exp_points':"Oczekiwane punkty", "elo":"ELO", "GF":'GZ', "GA":"GS"}, inplace = True)
cols1=['Pozycja', 'Drużyna', 'Obecna pozycja', 'Oczekiwane punkty', 'ELO', 'Punkty', 'Mecze']

df4 = df4()
df5 = df5()
df6 = df6()

df2_html_table = table_style_1 + df2.to_html(index=False, escape=False)
df3_html_table = table_style_1 + df3[cols1].to_html(index=False, escape=False)

#########
#cols = [f"{i}" for i in range(1, 19)]
cols = ["Team", "1", "2", "3", "4", "5", "16", "17", "18"]
styled = (
    df[cols]
    .style
    .format({col: "{:.1%}" for col in cols if col != "Team"})
    .background_gradient(cmap="Greens", subset=[c for c in cols if c != "Team"])
)

st.subheader("Szanse na poszczególne pozycje", divider="gray")
st.markdown("<p style='text-align: center; font-weight:normal; font-family:sans-serif;'>Pozycja w tabeli</p>", unsafe_allow_html=True)
html_table = styled.to_html(index = False)
scrollable_html = f"""
<div style="overflow-x: auto; white-space: nowrap;">
{html_table}
</div>
"""

st.markdown(table_style, unsafe_allow_html=True)
st.markdown(scrollable_html, unsafe_allow_html=True)
st.markdown("Więcej w karcie ['Statystyki i przewidywania klubowe'](https://symulator-kultura-gry.streamlit.app/eklapa_klub_site)", unsafe_allow_html=True)
with st.expander("Jak działa ta symulacja?"):
    st.write("""
    Na podstawie różnic w sile zespołów (wskaźnik ELO) wyznaczany jest rozkład prawdopodobieństwa liczby goli obu drużyn.
    Następnie, na bazie rozkładu, każdy mecz (wynik) symulowany jest kilka tysięcy razy. W efekcie powstaje kilka tysięcy finalnych tabel ligowych. 
    Na ich podstawie wyznacza się szansę każdego zespołu na zakończenie ligi na poszczególnym miejscu w tabeli. 
    Szczegóły w zakładce 'Metodologia'.
    """)
###########

st.subheader("Przewidywana tabela końcowa", divider="gray")

scrollable_df3 = f"""
<div style="overflow-x: auto; white-space: nowrap;">
{df3_html_table}
</div>
"""
st.markdown(scrollable_df3, unsafe_allow_html=True)

#####

st.subheader("Forma zespołów", divider="gray")
performance_viz(df6)

with st.expander("O co chodzi w tym wykresie?"):
    st.write("""'Na wykresie przedstawiona jest średnia różnicy punktów rzeczywistych (uzyskanych w rozgrywkach ligowych) i punktów oczekiwanych (wyznaczonych na podstawie symulacji).'""")
### 
st.subheader("Najbliższe mecze", divider="gray")
scrollable_df2 = f"""
<div style="max-height: 300px; overflow-y: auto; padding: 5px;">
    {df2_html_table}
</div>
"""
st.markdown(scrollable_df2, unsafe_allow_html=True)


st.subheader("Oblicz szanse wygranej", divider="gray")
col_a1, col_b1 = st.columns(2)
with col_a1:
    home_choice = st.selectbox("**Wybierz gospodarza**", sorted(df1['Drużyna'].unique()))
with col_b1:
    away_choice = st.selectbox("**Wybierz gościa**", sorted((df1[df1['Drużyna']!=home_choice]['Drużyna'].unique())))

    # ELO
elo_home = df1.loc[df1['Drużyna'] == home_choice, 'ELO'].values[0]
elo_away = df1.loc[(df1['Drużyna'] == away_choice), 'ELO'].values[0]


W, D, L = calculate_elo_wdl(elo_home+63, elo_away)

col_a2, col_b2, col_c2 = st.columns(3)

    # Home
with col_a2:
    with st.container(border = True):
        st.markdown(
            f"<p style='text-align: center; font-weight:bold; font-family:sans-serif;'>{home_choice}</p>", unsafe_allow_html=True)
        st.markdown(
            f"<p style='text-align: center; font-size:20px; font-weight:normal; font-family:sans-serif;'>{W*100:.1f}%</p>",
            unsafe_allow_html=True)

    # Remis
with col_b2:
    with st.container(border = True):
        st.markdown(
            "<p style='text-align: center; font-weight:bold; font-family:sans-serif;'>Remis</p>",
            unsafe_allow_html=True)
        st.markdown(
            f"<p style='text-align: center; font-size:20px; font-weight:normal; font-family:sans-serif;'>{D*100:.1f}%</p>",
            unsafe_allow_html=True)

    # Away
with col_c2:
    with st.container(border = True):
        st.markdown(
            f"<p style='text-align: center; font-weight:bold; font-family:sans-serif;'>{away_choice}</p>",
            unsafe_allow_html=True)
        st.markdown(
            f"<p style='text-align: center; font-size:20px; font-weight:normal; font-family:sans-serif;'>{L*100:.1f}%</p>",
            unsafe_allow_html=True)
#####

st.subheader("Kurs tworzenia symulacji i dashboardów", divider = 'grey')

with st.container(border = False):
        st.markdown("""
            **Chcemy stworzyć kurs, w którym pokażemy jak zostać analitycznym magikiem i być w stanie symulować wyniki meczów i rozgrywek ligowych.**
            
            Zainteresowany? Najpierw jednak musimy dowiedzieć się więcej o Tobie i Twoich potrzebach. 

            📄 **[Wypełnij krótką ankietę](https://docs.google.com/forms/d/e/1FAIpQLSe9c5tmRgRBUVGWg2EGZorGY6Akd4O4bHsrEMFCFcleI-pyYA/viewform?usp=dialog)** 📄
        """)


#####

st.subheader("Największe zaskoczenia", divider="gray")

df5['min_perf'] = df5[['home_performance', 'away_performance']].min(axis=1)
lowest_rows = df5.nsmallest(3, 'min_perf')

for i in range(len(lowest_rows)):
    row = lowest_rows.iloc[i]
    with st.container(border=True):
        col_a2, col_b2, col_c2 = st.columns(3)

        # Home
        with col_a2:
            st.markdown(
                f"<p style='text-align: center; font-size:18px; font-weight: bold; font-family:sans-serif;'>{row['Home']}</p>",
                unsafe_allow_html=True)
            st.markdown(
                f"<p style='text-align: center; font-size:14px; font-weight:normal; font-family:sans-serif;'>{row['HomeElo']:.0f} ELO</p>",
                unsafe_allow_html=True)

        # Score
        with col_b2:
            st.markdown(
                f"<p style='text-align: center; font-size:18px; font-weight: bold; font-family:sans-serif;'>{row['Score']}</p>",
                unsafe_allow_html=True)
            st.markdown(
                f"<p style='text-align: center; font-size:14px; font-weight:normal; font-family:sans-serif;'>{row['Date'].strftime('%d-%m-%Y')}</p>",
                unsafe_allow_html=True)

        # Away
        with col_c2:
            st.markdown(
                f"<p style='text-align: center; font-size:18px; font-weight: bold; font-family:sans-serif;'>{row['Away']}</p>",
                unsafe_allow_html=True)
            st.markdown(
                f"<p style='text-align: center; font-size:14px; font-weight:normal; font-family:sans-serif;'>{row['AwayElo']:.0f} ELO</p>",
                unsafe_allow_html=True)

        # odstęp między kontenerami
        st.markdown("<div style='height: 15px'></div>", unsafe_allow_html=True)


####
st.subheader("Obecna tabela", divider="gray")

cols2 = ['Pozycja', 'Drużyna', "Mecze", "Punkty", 'Wygrane', 'Remisy', 'Porażki', 'GZ', 'GS']

table_style = """
<style>
.scroll-table {
    max-height: 400px;
    overflow-y: auto;
    overflow-x: auto;
}
.scroll-table table {
    width: 100%;
    border-collapse: collapse;
}
</style>
"""

tabela_html = (
    table_style
    + '<div class="scroll-table">'
    + df3[cols2].to_html(index=False, escape=False)
    + '</div>'
)

st.markdown(tabela_html, unsafe_allow_html=True)
####
st.subheader("Podoba Ci się nasz symulator ligowy?", divider = 'gray')
st.write("Stworzenie go pochłonęło sporo pracy. Wesprzyj nas, stawiając nam wirtualną kawę!")

html_buycoffee = """
<div style="width: 100%; max-width: 600px; font-family: Arial, sans-serif; margin: auto;">
    <div style="
        box-sizing: border-box;
        background-color: #FFFFFF;
        padding: 16px;
        border-radius: 16px;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -4px rgba(0,0,0,0.1);
        color: #000000DE;
        text-align: center;
    ">
        <h3 style="font-size: 18px; font-weight: 600; line-height: 1.5; margin: 0;">
            ☕ Postaw kawę za:
        </h3>
    </div>

    <div style="display: flex; gap: 12px; margin-top: 16px; justify-content: center;">
        <a href="https://buycoffee.to/kulturagry?coffeeSize=small" 
           style="display: flex; flex-direction: column; justify-content: center; align-items: center;
                  padding: 16px; border-radius: 16px;
                  box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -4px rgba(0,0,0,0.1);
                  width: 100%; max-width: 150px;
                  text-align: center; background-color: #FFFFFF; color: #000000DE; text-decoration: none;"
           target="_blank" title="Postaw kawę za: 5 zł">
            <img src="https://buycoffee.to/img/coffee-small-white.svg" alt="small coffee icon" style="width: 36px; height: 36px;" />
            <span style="font-size: 16px; font-weight: 700; margin-top: 8px; line-height: 1.5;">5 zł</span>
        </a>

        <a href="https://buycoffee.to/kulturagry?coffeeSize=medium" 
           style="display: flex; flex-direction: column; justify-content: center; align-items: center;
                  padding: 16px; border-radius: 16px;
                  box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -4px rgba(0,0,0,0.1);
                  width: 100%; max-width: 150px;
                  text-align: center; background-color: #FFFFFF; color: #000000DE; text-decoration: none;"
           target="_blank" title="Postaw kawę za: 10 zł">
            <img src="https://buycoffee.to/img/coffee-medium-white.svg" alt="medium coffee icon" style="width: 36px; height: 36px;" />
            <span style="font-size: 16px; font-weight: 700; margin-top: 8px; line-height: 1.5;">10 zł</span>
        </a>

        <a href="https://buycoffee.to/kulturagry?coffeeSize=large" 
           style="display: flex; flex-direction: column; justify-content: center; align-items: center;
                  padding: 16px; border-radius: 16px;
                  box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -4px rgba(0,0,0,0.1);
                  width: 100%; max-width: 150px;
                  text-align: center; background-color: #FFFFFF; color: #000000DE; text-decoration: none;"
           target="_blank" title="Postaw kawę za: 15 zł">
            <img src="https://buycoffee.to/img/coffee-large-white.svg" alt="large coffee icon" style="width: 36px; height: 36px;" />
            <span style="font-size: 16px; font-weight: 700; margin-top: 8px; line-height: 1.5;">15 zł</span>
        </a>
    </div>
</div>
"""

components.html(html_buycoffee, height=300, scrolling=False)
