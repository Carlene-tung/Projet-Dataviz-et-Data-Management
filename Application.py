######## PROJET DE STREAMLIT #######
# IMPORT DE BIBLIOTHEQUE NECESSAIRE 
#  
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
from PIL import Image
from datetime import datetime

# PAGE STREAMLIT 
st.set_page_config(page_title="My Streamlit Dashboard", page_icon=":bar_chart:", layout="wide")

# Charger les données
@st.cache_data
def load_data():
    return pd.read_csv("C:/Users/nosty/Desktop/PROJET/donnes.csv", encoding="ISO-8859-1", low_memory=False)

df = load_data()

# Fonctions pour chaque page
def page1():
    st.title("Bonjour et Bienvenue sur notre application Streamlit : PROJET DATA MANAGEMENT ET DATA VIZ")
    current_time = datetime.now().time()
    st.time_input('Il est exactement', value=current_time)
    st.write('Groupe N°4 :  AZIABLE Etse; COULIBALY Kiyali; TUNGAMWESE Carlène')
    
    st.markdown("""
    <div style='background-color: black; padding: 10px; border-radius: 10px;'>
        <h2>Introduction</h2>
        <p>Cette application présente des analyses détaillées des données de prêts, comprenant des statistiques descriptives, des visualisations d'évolutions de prix, et bien plus encore.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader('Statistiques descriptives globales des données')
    st.write(df.describe())

    st.subheader("Statistiques descriptives supplémentaires")
    st.write("""
    - **pm2**: Prix au m² de la surface du logement
    - **vtpz**: Montant du prêt à taux zéro
    - **vtpr**: Montant de l'ensemble de prêts de l'opération
    - **vtpp**: Montant du prêt principal
    - **txno**: Taux nominal annuel du prêt
    """)

    st.subheader("Statistiques annuelles: Valeurs moyennes")
    selected_years = st.multiselect("Sélectionnez les années à afficher", df['an'].unique())
    if selected_years:
        stats_by_an = df[df['an'].isin(selected_years)].groupby('an')[['vtpz', 'vtpr', 'vtpp', 'txno']].mean().reset_index()
        st.write(stats_by_an)
    else:
        st.write("Sélectionnez une ou plusieurs années pour afficher les statistiques correspondantes.")
    
    st.subheader("Statistiques régionales: Valeurs moyennes")
    stat_region = st.multiselect("Sélectionnez les régions à afficher", df['region'].unique())
    if stat_region:
        stats_by_region = df[df['region'].isin(stat_region)].groupby('region')[['vtpz', 'vtpr', 'vtpp', 'txno']].mean().reset_index()
        st.write(stats_by_region)
    else:
        st.write("Sélectionnez une ou plusieurs régions pour afficher les statistiques correspondantes.")

def plot_evolution_prix_m2():
    st.subheader("Évolution des prix au m²")
    mean_pm2 = df.groupby('an')['pm2'].mean()
    fig = px.line(x=mean_pm2.index, y=mean_pm2.values, labels={'x': 'Année', 'y': 'Prix du m²'})
    fig.update_layout(template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

def plot_evolution_taux_interet():
    st.subheader("Évolution annuelle du taux d'intérêt nominal")
    mean_tx = df.groupby('an')['txno'].mean()
    fig = px.line(x=mean_tx.index, y=mean_tx.values, labels={'x': 'Année', 'y': "Taux d'intérêt nominal"})
    fig.update_layout(template='ggplot2')
    st.plotly_chart(fig, use_container_width=True)

def plot_montant_pret_zero():
    st.subheader('Montant annuel moyen du prêt à taux zéro par région')
    mean_montant_region = df.groupby('region')['vtpr'].mean()
    fig = px.bar(x=mean_montant_region.index, y=mean_montant_region.values, text=mean_montant_region.values, 
                 labels={'x': 'Région', 'y': 'Montant annuel moyen'}, color=mean_montant_region.index)
    st.plotly_chart(fig, use_container_width=True)

def plot_montant_total_pret():
    st.subheader('Montant total du prêt par région')
    total_vtpr = df.groupby('region')['vtpr'].sum()
    colors = px.colors.qualitative.Set1
    fig = go.Figure(data=[go.Bar(x=total_vtpr.index, y=total_vtpr.values, marker_color=colors)])
    fig.update_layout(xaxis_title='Région', yaxis_title='Montant total (€)', xaxis_tickangle=45, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)

def plot_evolution_pret_zero_region():
    st.subheader('Évolution du montant du prêt à taux zéro par région')
    selected_regions = st.multiselect("Sélectionnez les régions à afficher", df['region'].unique())
    if selected_regions:
        df_mean = df[df['region'].isin(selected_regions)].groupby(['an', 'region'])[['vtpz']].mean().reset_index()
        fig = px.line(df_mean, x="an", y="vtpz", color="region", title="Évolution de vtpz par région",
                      labels={'an': 'Année', 'vtpz': 'Montant du prêt à taux zéro'})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Sélectionnez une ou plusieurs régions pour afficher l'évolution correspondante.")

def plot_correlation_matrix():
    st.subheader("Matrice de corrélation")
    corr = df.corr(numeric_only=True)
    fig = px.imshow(corr, text_auto=True, aspect="auto", title="Matrice de corrélation")
    st.plotly_chart(fig, use_container_width=True)

def plot_histogram(column):
    st.subheader(f"Histogramme de {column}")
    fig = px.histogram(df, x=column, nbins=50, title=f"Répartition de {column}")
    st.plotly_chart(fig, use_container_width=True)

def plot_market_indices():
    st.subheader("Indices boursiers")
    market_index_image = Image.open("C:/Users/nosty/Desktop/PROJET/credits-immo-pascher (1).jpg")
    st.image(market_index_image, caption="Indice Boursier", use_column_width=True)

def plot_interest_rate_banner():
    st.markdown("""
    <div style='width: 100%; background-color: black; padding: 10px; border-radius: 5px; text-align: center;'>
        <h2>Taux d'intérêt du jour</h2>
        <p style='font-size: 20px;'><b>1.25%</b></p>
    </div>
    """, unsafe_allow_html=True)

def page2():
    st.markdown("<h1 style='color: skyblue;'>Visualisations</h1>", unsafe_allow_html=True)
    
    st.markdown("### Évolution des indicateurs")
    col1, col2 = st.columns(2)
    with col1:
        plot_evolution_prix_m2()
    with col2:
        plot_evolution_taux_interet()
    
    st.markdown("### Prêts par région")
    col3, col4 = st.columns(2)
    with col3:
        plot_montant_pret_zero()
    with col4:
        plot_montant_total_pret()
    
    st.markdown("### Évolution des prêts à taux zéro par région")
    plot_evolution_pret_zero_region()

    st.markdown("### Analyses supplémentaires")
    plot_correlation_matrix()
    selected_column = st.selectbox("Sélectionnez une colonne pour afficher l'histogramme", df.columns)
    plot_histogram(selected_column)

    st.markdown("### Images financières")
    plot_market_indices()
    plot_interest_rate_banner()

# Navigation dans la barre latérale
st.sidebar.title("Navigation")
page = st.sidebar.radio("Sélectionnez une page", ["Statistiques descriptives", "Visualisations"])

# Afficher la page sélectionnée
if page == "Statistiques descriptives":
    page1()
elif page == "Visualisations":
    page2()

# Widgets supplémentaires
st.sidebar.title("Options supplémentaires")
if st.sidebar.checkbox("Show/Hide"):
    st.sidebar.text('Showing or hiding Widget')

status = st.sidebar.radio("What is your status", ['Activate', 'Inactivate'])
if status == 'Activate':
    st.sidebar.success("You're activated")
else:
    st.sidebar.warning("Inactivate")

occupation = st.sidebar.selectbox("Your occupation", ['Banquier', 'Data engineer', 'Etudiant'])
st.sidebar.write('You selected this option', occupation)

location = st.sidebar.multiselect("Where do you work", ['Lille', 'Marseille', 'Paris', 'Autre'])
st.sidebar.write(f"You have selected {len(location)} location/s")

level = st.sidebar.slider("What is your level", 1, 5)

# Exportation des données filtrées au format CSV
if st.sidebar.button('Télécharger les données'):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # encodage en base64
    href = f'<a href="data:file/csv;base64,{b64}" download="filtered_data.csv">Télécharger CSV</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)
