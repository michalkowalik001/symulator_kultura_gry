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

st.write("Źródła danych:")
st.write("Metodologia zgodna z aleks-kapich.com")

st.write("Tabela 'Przewidywana tabela końcowa' została uszeregowana malejąco według kolumny 'Oczekiwane punkty'. Wartości kolumny 'Oczekiwane punkty' (1) oznaczają sumę punktów zespołu we wszystkich symulacjach, podzieloną przez liczbę symulacji.")

st.write("Słupki wykresu 'Forma względem oczekiwań' oznaczają średnią różnicę między punktami oczekiwanymi (zgodnie z definicją (1) wyżej), a rzeczywistymi punktami, zdobytymi przez drużynę. Wartości dodatnie (zielone słupki) oznaczają, że drużyna radzi sobie lepiej od oczekiwań. Wartości ujemne (czerwone słupki) oznaczają, że drużyna radzi sobie gorzej od oczekiwań.")

st.write("Tabela 'Najbliższe mecze' została uszeregowana malejąco według kolumny 'Data'. Kolumny 'Szanse gospodarz', 'Szanse remis', 'Szanse gość' (...)")

