import streamlit as st
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Tableau de bord", layout="wide", page_icon='📊')

st.markdown("# 🚗 Étude et analyse des accidents corporels de la circulation routière")

# Chargement des fichiers CSV
df_caracteristiques = pd.read_csv("streamlit/data/carcteristiques-2022.csv", sep=';') # ../data/carcteristiques-2022.csv for local use
df_lieux = pd.read_csv("streamlit/data/lieux-2022.csv", sep=';', low_memory=False)
df_vehicules = pd.read_csv("streamlit/data/vehicules-2022.csv", sep=';')
df_usagers = pd.read_csv("streamlit/data/usagers-2022.csv", sep=';')

# Renommer les colonnes
df_caracteristiques = df_caracteristiques.rename(columns={"long": "lon", "Accident_Id": "Num_Acc"})

# Jointure des DataFrames avec 'Num_Acc'
df = pd.merge(df_caracteristiques, df_lieux, on='Num_Acc', how='left')
df = pd.merge(df, df_vehicules, on='Num_Acc', how='left')
df = pd.merge(df, df_usagers, on=['Num_Acc', 'id_vehicule'], how='left')

# Transformations
df_caracteristiques['jour'] = pd.to_datetime(df_caracteristiques['jour'].astype(str) + '-' + df_caracteristiques['mois'].astype(str) + '-' + df_caracteristiques['an'].astype(str), dayfirst=True)

# Mapping des types de collision
collision_mapping = {
    -1: 'Non renseigné',
    1: 'Deux véhicules - frontale',
    2: 'Deux véhicules – par l’arrière',
    3: 'Deux véhicules – par le coté',
    4: 'Trois véhicules et plus – en chaîne',
    5: 'Trois véhicules et plus - collisions multiples',
    6: 'Autre collision',
    7: 'Sans collision'
}

# Mapping des catégories de véhicules
catv_mapping = {
    0: "Indéterminable",
    1: "Bicyclette",
    2: "Cyclomoteur <50cm3",
    3: "Voiturette (Quadricycle à moteur carrossé)",
    4: "Référence inutilisée depuis 2006 (scooter immatriculé)",
    5: "Référence inutilisée depuis 2006 (motocyclette)",
    6: "Référence inutilisée depuis 2006 (side-car)",
    7: "VL seul",
    8: "Référence inutilisée depuis 2006 (VL + caravane)",
    9: "Référence inutilisée depuis 2006 (VL + remorque)",
    10: "VU seul 1,5T <= PTAC <= 3,5T",
    11: "Référence inutilisée depuis 2006 (VU (10) + caravane)",
    12: "Référence inutilisée depuis 2006 (VU (10) + remorque)",
    13: "PL seul 3,5T <PTCA <= 7,5T",
    14: "PL seul > 7,5T",
    15: "PL > 3,5T + remorque",
    16: "Tracteur routier seul",
    17: "Tracteur routier + semi-remorque",
    18: "Référence inutilisée depuis 2006 (transport en commun)",
    19: "Référence inutilisée depuis 2006 (tramway)",
    20: "Engin spécial",
    21: "Tracteur agricole",
    30: "Scooter < 50 cm3",
    31: "Motocyclette > 50 cm3 et <= 125 cm3",
    32: "Scooter > 50 cm3 et <= 125 cm3",
    33: "Motocyclette > 125 cm3",
    34: "Scooter > 125 cm3",
    35: "Quad léger <= 50 cm3 (Quadricycle à moteur non carrossé)",
    36: "Quad lourd > 50 cm3 (Quadricycle à moteur non carrossé)",
    37: "Autobus",
    38: "Autocar",
    39: "Train",
    40: "Tramway",
    41: "3RM <= 50 cm3",
    42: "3RM > 50 cm3 <= 125 cm3",
    43: "3RM > 125 cm3",
    50: "EDP à moteur",
    60: "EDP sans moteur",
    80: "VAE",
    99: "Autre véhicule"
}

# Mapping de la gravité des accidents
severity_mapping = {
    1: 'Indemne',
    2: 'Tué',
    3: 'Blessé hospitalisé',
    4: 'Blessé léger'
}

# Mapping du sexe des usagers
sexe_mapping = {
    1: 'Homme',
    2: 'Femme',
    -1: 'Non renseigné'
}

# Mapping des mois
mois_mapping = {
    1: 'Janvier',
    2: 'Février',
    3: 'Mars',
    4: 'Avril',
    5: 'Mai',
    6: 'Juin',
    7: 'Juillet',
    8: 'Août',
    9: 'Septembre',
    10: 'Octobre',
    11: 'Novembre',
    12: 'Décembre'
}

# Mapping des types de trajet
trajet_mapping = {
    -1: 'Non renseigné',
    0: 'Non renseigné',
    1: 'Domicile - Travail',
    2: 'Domicile - Ecole',
    3: 'Courses - achats',
    4: 'Utilisation professionnelle',
    5: 'Promenade – loisirs',
    6: 'Autre'
}

# Mapping des obstacles mobiles heurtés
obsm_mapping = {
    -1: 'Non renseigné',
    0: 'Aucun',
    1: 'Piéton',
    2: 'Véhicule',
    4: 'Véhicule sur rail',
    5: 'Animal domestique',
    6: 'Animal sauvage',
    9: 'Autre'
}

# Mapping des conditions atmosphériques
atm_mapping = {
    -1: 'Non renseigné',
    1: 'Normale',
    2: 'Pluie légère',
    3: 'Pluie forte',
    4: 'Neige - grêle',
    5: 'Brouillard - fumée',
    6: 'Vent fort - tempête',
    7: 'Temps éblouissant',
    8: 'Temps couvert',
    9: 'Autre'
}

# Application des mappings au colonnes
df_caracteristiques['mois_nom'] = df_caracteristiques['mois'].map(mois_mapping)
df_caracteristiques['atm'] = df_caracteristiques['atm'].map(atm_mapping)

df['col'] = df['col'].map(collision_mapping)
df['catv'] = df['catv'].map(catv_mapping)
df['grav'] = df['grav'].map(severity_mapping)
df['sexe'] = df['sexe'].map(sexe_mapping)
df['trajet'] = df['trajet'].map(trajet_mapping)
df['obsm'] = df['obsm'].map(obsm_mapping)
df['atm'] = df['atm'].map(atm_mapping)

# Division de la page en 5 colonnes pour les KPIs
col1, col2, col3, col4, col5 = st.columns(5)

# Statistiques générales
with col1:
    st.metric(label="🚧 Nombre d'accidents", value=f"{len(df_caracteristiques)}")
with col2:
    st.metric(label="🚘 Nombre véhicules impliqués", value=f"{df['id_vehicule'].nunique()}")
with col3:
    st.metric(label="🧍 Nombre d'usagers impliqués", value=f"{df['id_usager'].nunique()}")
with col4:
    df_death = df[df['grav'] == 'Tué']
    st.metric(label="💀 Nombre de décès", value=f"{len(df_death)}")
with col5:
    if len(df) > 0:
        st.metric(label="⚰️ Taux de létalité", value=f"{round(df_death['id_usager'].nunique() * 100 / df['Num_Acc'].nunique(), 2)} %")
    else:
        st.metric(label="⚰️ Taux de létalité", value=f"0%")

# Division de la page en 2 colonnes pour les graphiques
stat_col1, stat_col2 = st.columns(2)

with stat_col1:
    # Grouper par mois et compter le nombre d'accidents
    accidents_par_mois = df_caracteristiques.groupby(['mois', 'mois_nom']).size().reset_index(name='nb_acc')

    # Triés les mois numériquement
    accidents_par_mois = accidents_par_mois.sort_values('mois')
    
    # Créer le graphique avec Plotly
    st.subheader("Nombre d'accidents par mois")
    fig_acc = px.bar(accidents_par_mois, x='mois_nom', y='nb_acc', labels={'mois_nom': 'Mois', 'nb_acc': "Nombre d'accidents"})
    st.plotly_chart(fig_acc, theme=None)

    # Graphique des accidents par gravité
    st.subheader("Nombre d'usagers par gravité d'accident")
    accidents_par_gravite = df['grav'].value_counts().reset_index(name='Total').sort_values(by="Total")

    fig = px.pie(accidents_par_gravite, values='Total', names='grav')
    fig.update_traces(sort=False) 
    st.plotly_chart(fig, theme=None)

    # Graphique des types de trajet
    st.subheader("Répartition des accidents par types de trajet")
    trajets_par_type = df['trajet'].value_counts().reset_index(name='nb_trajets').sort_values(by="nb_trajets", ascending=False)
    fig_trajet = px.bar(trajets_par_type, x='trajet', y='nb_trajets', labels={'trajet': 'Type de trajet', 'nb_trajets': "Nombre de trajets"}, color="trajet")
    st.plotly_chart(fig_trajet, theme=None)

    # Graphique des accidents par conditions atmosphériques
    st.subheader("Nombre d'accidents par conditions atmosphériques")
    accidents_par_atm = df_caracteristiques['atm'].value_counts().reset_index(name='nb_acc')
    fig_atm = px.bar(accidents_par_atm, x='atm', y='nb_acc', labels={'atm': 'Conditions atmosphériques', 'nb_acc': "Nombre d'accidents"}, color="atm")
    st.plotly_chart(fig_atm, theme=None)
    
with stat_col2:
    # Graphique des accidents par jour
    st.subheader("Nombre d'accidents par jour")
    accidents_par_jour = df_caracteristiques.groupby(df_caracteristiques['jour'].dt.date).size().to_frame('nb_acc')
    st.line_chart(accidents_par_jour, height=450)

    # Graphique des accidents par catégorie de véhicule
    st.subheader("Catégories de véhicule impliqué")
    accidents_par_vehicule = df['catv'].value_counts().reset_index(name='nb_vec')
    accidents_par_vehicule = accidents_par_vehicule.sort_values(by='nb_vec', ascending=False)
    accidents_par_vehicule = accidents_par_vehicule[:8]
    fig_vec = px.bar(accidents_par_vehicule, x='catv', y='nb_vec', labels={'catv': 'Catégorie de véhicule', 'nb_vec': "Nombre d'accidents"})
    st.plotly_chart(fig_vec, theme=None)

    # Graphique des accidents par sexe des usagers
    st.subheader("Répartition des usagers par sexe")
    accidents_par_sexe = df['sexe'].value_counts().reset_index(name='nb_acc').sort_values(by="nb_acc")

    fig_sexe = px.pie(accidents_par_sexe, names='sexe', values='nb_acc')
    fig_sexe.update_traces(sort=False) 
    st.plotly_chart(fig_sexe, theme=None)

    # Graphique des obstacles mobiles heurtés
    st.subheader("Répartition des obstacles mobiles heurtés")
    obstacles_par_type = df['obsm'].value_counts().reset_index(name='nb_obstacles').sort_values(by="nb_obstacles", ascending=False)
    fig_obstacle = px.bar(obstacles_par_type, x='obsm', y='nb_obstacles', labels={'obsm': 'Obstacle mobile', 'nb_obstacles': "Nombre d'obstacles heurtés"}, color="obsm")
    st.plotly_chart(fig_obstacle, theme=None)   


hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """

st.markdown(hide_streamlit_style, unsafe_allow_html=True) 