import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from data.data import df, df1, df2, df3, df4, df5, df6, calculate_elo_wdl, performance_viz
from utils.sidebar import show_sidebar

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
    font-size: 12px;
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
    font-size: 11px;
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

###########

st.subheader("Przewidywana tabela końcowa", divider="gray")
st.markdown(df3_html_table, unsafe_allow_html=True)

st.subheader("Forma względem oczekiwań", divider="gray")
performance_viz(df6)


st.subheader("Najbliższe mecze", divider="gray")
st.markdown(df2_html_table, unsafe_allow_html=True)


st.subheader("Oblicz szanse wygranej", divider="gray")
col_a1, col_b1 = st.columns(2)
with col_a1:
    home_choice = st.selectbox("**Wybierz gospodarza**", sorted(df1['Drużyna'].unique()))
with col_b1:
    away_choice = st.selectbox("**Wybierz gościa**", sorted((df1[df1['Drużyna']!=home_choice]['Drużyna'].unique())))

    # ELO
elo_home = df1.loc[df1['Drużyna'] == home_choice, 'ELO'].values[0]
elo_away = df1.loc[(df1['Drużyna'] == away_choice), 'ELO'].values[0]


home_adv = st.checkbox("Uwzględnij przewagę własnego boiska")

if home_adv:
    W, D, L = calculate_elo_wdl(elo_home+63, elo_away)
else:
    W, D, L = calculate_elo_wdl(elo_home, elo_away)


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

st.subheader("Kurs symulacji i tworzenia dashboardów", divider = 'grey')

with st.container(border = False):
        st.markdown("""
            **Chcemy stworzyć kurs, w którym pokażemy jak zostać analitycznym magikiem i być w stanie symulować wyniki meczów i rozgrywek ligowych.**
            
            Zainteresowany? Najpierw jednak musimy dowiedzieć się więcej o Tobie i Twoich potrzebach. 

            📄 **[Wypełnij krótką ankietę](https://docs.google.com/forms/d/e/1FAIpQLSe9c5tmRgRBUVGWg2EGZorGY6Akd4O4bHsrEMFCFcleI-pyYA/viewform?usp=dialog)** 📄
        """)

#########
cols = [f"{i}" for i in range(1, 19)]
styled = df.style.format({col: "{:.1%}" for col in cols}).background_gradient(cmap="Greens", subset=cols)
st.subheader("Szanse na mistrzostwo", divider="gray")
st.markdown("<p style='text-align: center; font-weight:normal; font-family:sans-serif;'>Pozycja w tabeli</p>", unsafe_allow_html=True)
st.markdown(styled.to_html(index='Team'), unsafe_allow_html=True)

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
cols2=['Pozycja', 'Drużyna', "Mecze", "Punkty", 'Wygrane', 'Remisy', 'Porażki', 'GZ', 'GS']
tabela_html = table_style + df3[cols2].to_html(index=False, escape=False)
st.markdown(tabela_html, unsafe_allow_html=True)
