import streamlit as st
import pandas as pd
import plotly.express as px
import os

BASE_DIR = os.getcwd()

@st.cache_data
def df():
    df_path = os.path.join(BASE_DIR, "data", "symulacje.xlsx")
    df = pd.read_excel(df_path)

    # zmiana nazw kolumn
    for i in range(1, 19):
        df.rename(columns={f'Pos_{i}': f"{i}"}, inplace=True)

    # ustawienie 0 dla wartości < 0.01 w kolumnach 1-18
    cols = [str(i) for i in range(1, 19)]
    df[cols] = df[cols].mask(df[cols] < 0.01, 0)

    # sortowanie
    df = df.sort_values(by=['1', '2'], ascending=False).reset_index(drop=True)

    return df

@st.cache_data
def df1():
    df1_path = os.path.join(BASE_DIR, "data", "symulacje_punktowe.xlsx")
    df1 = pd.read_excel(df1_path)
    df1.set_index('Team')
    df1['exp_points'] = pd.to_numeric(df1['exp_points'], errors='coerce')

    return df1

@st.cache_data
def df2():
    df2_path = os.path.join(BASE_DIR, "data", "next_matches.xlsx")
    df2 = pd.read_excel(df2_path)
    for col in ['p_home_win','p_draw','p_away_win']:
        df2[col] = (df2[col]*100).round(0).astype(int).astype(str) + '%'
    df2['Date'] = df2['Date'].dt.date
    df2 = df2[['Date', 'Home', 'Away' ,'p_home_win', 'p_draw', 'p_away_win']]

    return df2

@st.cache_data
def df3():
    df3_path = os.path.join(BASE_DIR, "data", "tabela_eklapa.xlsx")
    df3 = pd.read_excel(df3_path)
    df3 = df3.sort_values('exp_points', ascending = False).round(0)
    return df3

@st.cache_data
def df4():
    df4_path = os.path.join(BASE_DIR, "data", "all_clubs_elo_history.xlsx")
    df4 = pd.read_excel(df4_path)

    club_mapping = {
        "Rakow": "Raków",
        "Legia": "Legia Warsaw",
        "Lech": "Lech Poznań",
        "Jagiellonia": "Jagiellonia",
        "Pogon": "Pogoń Szczecin",
        "Cracovia": "Cracovia",
        "Gornik": "Górnik Zabrze",
        "Piast Gliwice": "Piast Gliwice",
        "Katowice": "Katowice",
        "Korona": "Korona Kielce",
        "Katowice": "Katowice",
        "Widzew": "Widzew Łódź",
        "Radomiak": "Radomiak Radom",
        "Motor Lublin": "Motor Lublin",
        "Lubin": "Zagłębie Lubin",
        "Puszcza Niepolomice": "Puszcza Niepołomice",
        "Stal Mielec": "Stal Mielec",
        "Lechia": "Lechia Gdańsk",
        "Arka":"Arka Gdynia",
        "Plock":"Wisła Płock"
    }

    df4['Team'] = df4['Team'].map(club_mapping)

    return df4

@st.cache_data
def df5():
    df5_path = os.path.join(BASE_DIR, "data", "previous_matches.xlsx")
    df5 = pd.read_excel(df5_path)
    df5 = df5[['Date', 'Home', 'Score', 'Away', 'HomeElo', 'AwayElo', 'home_exp', 'away_exp', 'home_points', 'away_points', 'home_performance', 'away_performance']]
    df5 = df5[df5['Score'].notna()]
    df5['HomeElo'], df5['AwayElo'] = df5['HomeElo'].round(0), df5['AwayElo'].round(0)
    return df5

@st.cache_data
def df6():
    df6_path = os.path.join(BASE_DIR, "data", "performance.xlsx")
    df6 = pd.read_excel(df6_path)
    return df6


def performance_viz(df):
    viz = df.sort_values('performance', ascending=True)
    # stonowane kolory
    viz['color'] = viz['performance'].apply(lambda x: '#0EC262' if x > 0 else '#D6320F')

    fig = px.bar(
        viz,
        x='performance',
        y='Team',
        orientation='h',
        color='color',
        color_discrete_map={'#0EC262':'#0EC262', '#D6320F':'#D6320F'},
        title='Forma oczekiwana vs. rzeczywista',
        labels={'performance':'Średnia punktów na mecz (rzeczywiste - oczekiwane)', 'Team':'Drużyna'}
    )

    # dodaj czarne krawędzie i stonowane kolory
    fig.update_traces(marker_line_color='black', marker_line_width=1)

    fig.update_layout(
        showlegend=False,
        template='plotly_white',
        height=600,
        title_font_size=24,
        xaxis_title_font_size=18,
        yaxis_title_font_size=18,
        xaxis_tickfont_size=16,    
        yaxis_tickfont_size=16, 
        xaxis=dict(
            showgrid=True,     
            gridcolor='lightgray',
            gridwidth=1 
        ),
        yaxis=dict(
            showgrid=True,
            title = ""
        )
    )

    st.plotly_chart(fig, use_container_width=True)

def calculate_elo_wdl(elo1, elo2, r=0.4):
    p = 1 / (1 + 10 ** ((elo2 - elo1) / 400))

    W = r * p * (1 - p) + p**2   # wygrana
    D = 2 * (p - W)              # remis
    L = 1 - W - D                # porażka

    return W, D, L

def szanse(df, selected_team):

    # przykładowy DataFrame
    cols = [str(i) for i in range(1, 19)]
    # wybór wiersza
    team_probs = df[df['Team'] == selected_team][cols].T.reset_index()
    team_probs.columns = ['Pozycja', 'Prawdopodobieństwo']

    team_probs['Prawdopodobieństwo'] = team_probs['Prawdopodobieństwo'] * 100

    fig = px.bar(
        team_probs,
        x='Pozycja',
        y='Prawdopodobieństwo',
        text='Prawdopodobieństwo',
        labels={'Pozycja': 'Pozycja w tabeli', 'Prawdopodobieństwo': 'Szansa [%]'},
        title=f'Szanse na poszczególne pozycje'
    )

    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    
    fig.update_layout(
        xaxis=dict(tickmode='linear', dtick=1),
        yaxis=dict(range=[0, team_probs['Prawdopodobieństwo'].max()*1.3]),
        uniformtext_minsize=8,
        uniformtext_mode='hide',  
        title_font_size=24,         
        xaxis_title_font_size=18,
        yaxis_title_font_size=18,
        xaxis_tickfont_size=16,    
        yaxis_tickfont_size=16,
    )

    return st.plotly_chart(fig, use_container_width=True)

def buy_cofee():
    st.html(
    """
   
      <div style="width: 100%; max-width: 600px; font-family: Arial, sans-serif;">
          <div
            style="
              box-sizing: border-box;
              background-color: #FFFFFF;
              padding: 16px;
              border-radius: 16px;
              box-shadow: 0 0 rgba(0,0,0,0), 0 0 rgba(0,0,0,0), 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
              width: 100%;
              background-color: #FFFFFF;
              color: #000000DE;
              text-align: center;
            "
          >
            <h3 style="font-size: 15px; font-weight: 600; line-height: 1.5; margin: 0;">
              Postaw kawę za:
            </h3>
          </div>
          
          <div style="display: flex; gap: 8px; margin-top: 12px; justify-content: center;">
            
              <a
                href="https://buycoffee.to/kulturagry?coffeeSize=small"
                style="
                  display: flex;
                  flex-direction: column;
                  justify-content: center;
                  align-items: center;
                  padding: 16px;
                  border-radius: 16px;
                  box-shadow: 0 0 rgba(0,0,0,0), 0 0 rgba(0,0,0,0), 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
                  width: 100%;
                  text-align: center;
                  background-color: #FFFFFF;
                  color: #000000DE;
                  text-decoration: none;
                "
                target="_blank"
                title="Postaw kawę za: 5 zł"
              >
                <img src="https://buycoffee.to/img/coffee-small-white.svg" alt="small coffee icon" style="width: 36px; height: 36px;" />
                <span style="font-size: 15px; font-weight: 700; margin-top: 8px; line-height: 1.5;">
                  5 zł
                </span>
              </a>
            
              <a
                href="https://buycoffee.to/kulturagry?coffeeSize=medium"
                style="
                  display: flex;
                  flex-direction: column;
                  justify-content: center;
                  align-items: center;
                  padding: 16px;
                  border-radius: 16px;
                  box-shadow: 0 0 rgba(0,0,0,0), 0 0 rgba(0,0,0,0), 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
                  width: 100%;
                  text-align: center;
                  background-color: #FFFFFF;
                  color: #000000DE;
                  text-decoration: none;
                "
                target="_blank"
                title="Postaw kawę za: 10 zł"
              >
                <img src="https://buycoffee.to/img/coffee-medium-white.svg" alt="medium coffee icon" style="width: 36px; height: 36px;" />
                <span style="font-size: 15px; font-weight: 700; margin-top: 8px; line-height: 1.5;">
                  10 zł
                </span>
              </a>
            
              <a
                href="https://buycoffee.to/kulturagry?coffeeSize=large"
                style="
                  display: flex;
                  flex-direction: column;
                  justify-content: center;
                  align-items: center;
                  padding: 16px;
                  border-radius: 16px;
                  box-shadow: 0 0 rgba(0,0,0,0), 0 0 rgba(0,0,0,0), 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
                  width: 100%;
                  text-align: center;
                  background-color: #FFFFFF;
                  color: #000000DE;
                  text-decoration: none;
                "
                target="_blank"
                title="Postaw kawę za: 15 zł"
              >
                <img src="https://buycoffee.to/img/coffee-large-white.svg" alt="large coffee icon" style="width: 36px; height: 36px;" />
                <span style="font-size: 15px; font-weight: 700; margin-top: 8px; line-height: 1.5;">
                  15 zł
                </span>
              </a>
            
          </div>
      </div>
    """,
)
