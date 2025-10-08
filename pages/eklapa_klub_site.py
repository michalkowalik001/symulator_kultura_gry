import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
import plotly.graph_objects as go
import psutil, os
import time
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
from data.data import df, df1, df2, df3, df4, df5, calculate_elo_wdl, szanse
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

st.title("Statystyki i przewidywania klubowe")

teams = [
    "Arka Gdynia",
    "Cracovia",
    "Górnik Zabrze",
    "Jagiellonia",
    "Katowice",
    "Korona Kielce",
    "Legia Warsaw",
    "Lech Poznań",
    "Lechia Gdańsk",
    "Motor Lublin",
    "Piast Gliwice",
    "Pogoń Szczecin",
    "Puszcza Niepołomice",
    "Raków",
    "Radomiak Radom",
    "Stal Mielec",
    "Widzew Łódź",
    "Wisła Płock",
    "Zagłębie Lubin"
]


selected_team = st.selectbox("**Wybierz zespół**", teams)

st.header(selected_team, divider = 'grey')

df = df()
df2 = df2()
df2 = df2[(df2['Home']==selected_team) | (df2['Away']==selected_team)].sort_values(by = 'Date')
df2.rename(columns = {'Home':'Gospodarz','Away':'Gość','Date':'Data', 'Day':"Dzień", "Time":"Czas", "Kolejka":"Wk", "HomeElo":"Gospodarz ELO",	
                      "AwayElo":"Gość ELO", "p_home_win":"Szansa gospodarz", "p_draw":"Szansa remis", "p_away_win":"Szansa gość"}, inplace = True)
df2_html_table = df2.to_html(index=False, escape=False)
df4 = df4()
df5 = df5()
df5 = df5[(df5['Home']==selected_team) | (df5['Away']==selected_team)].sort_values(by = 'Date')
exp_points = f"Oczekiwane Punkty"
points = f"Punkty"
mask_home = df5['Home'] == selected_team
mask_away = df5['Away'] == selected_team
df5[exp_points] = None
df5[points] = None
df5.loc[mask_home, exp_points] = df5.loc[mask_home, 'home_exp'].round(1)
df5.loc[mask_away, exp_points] = df5.loc[mask_away, 'away_exp'].round(1)
df5.loc[mask_home, points] = df5.loc[mask_home, 'home_points'].round(1)
df5.loc[mask_away, points] = df5.loc[mask_away, 'away_points'].round(1)
df5.rename(columns = {'Date':"Data", "Home":"Gospodarz", "Score":"Wynik", 'Away':"Gość"}, inplace = True)
df5_html_table = df5[['Data', 'Gospodarz','Wynik','Gość', exp_points, points]].to_html(index=False, escape=False)

szanse(df, selected_team)

team_df = df4[(df4['Team'] == selected_team)&(df4['To']>"2015-01-01")].sort_values('To')

fig = px.line(
    team_df,
    x='To',
    y='Elo',
    markers=True,
    title=f'Ewolucja ELO',
    labels={'To': 'Date', 'Elo': 'Elo Rating'},
    hover_data={'To': True, 'Elo': True, 'Team': True}
)

fig.update_layout(
    title_font_size=24,         
    xaxis_title="Czas",         
    yaxis_title="ELO",
    xaxis_title_font_size=18,
    yaxis_title_font_size=18,
    xaxis_tickfont_size=16,    
    yaxis_tickfont_size=16,  
)

st.plotly_chart(fig, use_container_width=True)

table_style = """
<style>
table {
    width: 100%;
    border-collapse: collapse;
    font-family: sans-serif;
    font-size: 14px;
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
####
st.subheader("Kurs symulacji i tworzenia dashboardów", divider = 'grey')

with st.container(border = False):
        st.markdown("""
            **Chcemy stworzyć kurs, w którym pokażemy jak zostać analitycznym magikiem i być w stanie symulować wyniki meczów i rozgrywek ligowych.**
            
            Zainteresowany? Najpierw jednak musimy dowiedzieć się więcej o Tobie i Twoich potrzebach. 

            📄 **[Wypełnij krótką ankietę](https://docs.google.com/forms/d/e/1FAIpQLSe9c5tmRgRBUVGWg2EGZorGY6Akd4O4bHsrEMFCFcleI-pyYA/viewform?usp=dialog)** 📄
        """)

####
st.subheader("Dotychczasowe mecze", divider="gray")
st.markdown(table_style + df5_html_table, unsafe_allow_html=True)


st.subheader("Pozostałe mecze", divider="gray")
st.markdown(table_style + df2_html_table, unsafe_allow_html=True)

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
