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


st.set_page_config(layout="wide")

hide_default_sidebar = """
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_default_sidebar, unsafe_allow_html=True)

show_sidebar()

st.title("Metodologia")

st.write("Źródła danych: https://fbref.com/en/; http://clubelo.com")
st.write("Metodologia symulacji bazujacych na ELO na podstawie Aleks Kapich, 2025, Mathematics Behind Predicting Football Results — the Poisson Model, Skellam Distribution & ELO Ratings [https://medium.com/@aleks-kapich/mathematics-behind-predicting-football-results-the-poisson-model-skellam-distribution-elo-bf50b8c5727f]")

st.write("Szczegóły działania systemu ELO: http://clubelo.com/System")

st.write("Tabela 'Przewidywana tabela końcowa' została uszeregowana malejąco według kolumny 'Oczekiwane punkty'. Wartości kolumny 'Oczekiwane punkty' (1) oznaczają sumę punktów zespołu we wszystkich symulacjach, podzieloną przez liczbę symulacji.")

st.write("Słupki wykresu 'Forma względem oczekiwań' oznaczają średnią różnicę między punktami oczekiwanymi (zgodnie z definicją (1) wyżej), a rzeczywistymi punktami, zdobytymi przez drużynę. Wartości dodatnie (zielone słupki) oznaczają, że drużyna radzi sobie lepiej od oczekiwań. Wartości ujemne (czerwone słupki) oznaczają, że drużyna radzi sobie gorzej od oczekiwań.")

st.write("Tabela 'Najbliższe mecze' została uszeregowana malejąco według kolumny 'Data'. Kolumny 'Szanse gospodarz', 'Szanse remis', 'Szanse gość' obliczone analitycznie (nie na podstawie symulacji), zgodnie z Kapich (2025), j.w., bez uwzględnienia przewagi własnego boiska")

st.write("W tabeli 'Szanse na mistrzostwo' i na wykresie 'Szanse na poszczególne pozycje', obliczonych symulacyjnie zgodnie z Kapich (2025) uwzględniono przewagę własnego boiska.")

st.write("Założenia symulacji: 
1. Niezmienność ELO w przyszłości
2. Przewaga własnego boiska = 63 ELO")

