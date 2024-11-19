import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Carte exploration des accidents", layout="wide", page_icon='🗺️')

st.markdown("# 🗺️ Carte d'exploration des accidents corporels de la circulation routière")

with st.sidebar:
    # Filtrer
    on = st.toggle("Filtrer")

    # Conditions Lumieres
    options_lumieres = {
        "Tous": 0,
        "Plein jour": 1,
        "Crépuscule ou aube": 2,
        "Nuit sans éclairage public": 3,
        "Nuit avec éclairage public non allumé": 4,
        "Nuit avec éclairage public allumé": 5
    }

    # Localisation
    options_agg = {
        "Tous": 0,
        "Hors agglomération": 1,
        "En agglomération": 2
    }

    # Type route
    options_route = {
        "Tous": 0,
        'Autoroute': 1,
        'Route nationale': 2,
        'Route Départementale': 3,
        'Voie Communales': 4,
        'Hors réseau public': 5,
        'Parc de stationnement ouvert à la circulation publique': 6,
        'Routes de métropole urbaine': 7,
        'autre': 9
    }

    # Conditions atmosphériques
    options_atm = {
        "Tous": 0,
        "Non renseigné": -1,
        "Normale": 1,
        "Pluie légère": 2,
        "Pluie forte": 3,
        "Neige - grêle": 4,
        "Brouillard - fumée": 5,
        "Vent fort - tempête": 6,
        "Temps éblouissant": 7,
        "Temps couvert": 8,
        "Autre": 9
    }

    # Type de collision
    options_col = {
        "Tous": 0,
        "Non renseigné": -1,
        "Deux véhicules - frontale": 1,
        "Deux véhicules – par l’arrière": 2,
        "Deux véhicules – par le coté": 3,
        "Trois véhicules et plus – en chaîne": 4,
        "Trois véhicules et plus - collisions multiples": 5,
        "Autre collision": 6,
        "Sans collision": 7
    }

    # Departements
    options_dep = {
        "Tous": 0,
        'Ain': '01',
        'Aisne': '02',
        'Allier': '03',
        'Alpes-de-Haute-Provence': '04',
        'Hautes-Alpes': '05',
        'Alpes-Maritimes': '06',
        'Ardèche': '07',
        'Ardennes': '08',
        'Ariège': '09',
        'Aube': '10',
        'Aude': '11',
        'Aveyron': '12',
        'Bouches-du-Rhône': '13',
        'Calvados': '14',
        'Cantal': '15',
        'Charente': '16',
        'Charente-Maritime': '17',
        'Cher': '18',
        'Corrèze': '19',
        'Côte-d\'Or': '21',
        'Côtes-d\'Armor': '22',
        'Creuse': '23',
        'Dordogne': '24',
        'Doubs': '25',
        'Drôme': '26',
        'Eure': '27',
        'Eure-et-Loir': '28',
        'Finistère': '29',
        'Gard': '30',
        'Haute-Garonne': '31',
        'Gers': '32',
        'Gironde': '33',
        'Hérault': '34',
        'Ille-et-Vilaine': '35',
        'Indre': '36',
        'Indre-et-Loire': '37',
        'Isère': '38',
        'Jura': '39',
        'Landes': '40',
        'Loir-et-Cher': '41',
        'Loire': '42',
        'Haute-Loire': '43',
        'Loire-Atlantique': '44',
        'Loiret': '45',
        'Lot': '46',
        'Lot-et-Garonne': '47',
        'Lozère': '48',
        'Maine-et-Loire': '49',
        'Manche': '50',
        'Marne': '51',
        'Haute-Marne': '52',
        'Mayenne': '53',
        'Meurthe-et-Moselle': '54',
        'Meuse': '55',
        'Morbihan': '56',
        'Moselle': '57',
        'Nièvre': '58',
        'Nord': '59',
        'Oise': '60',
        'Orne': '61',
        'Pas-de-Calais': '62',
        'Puy-de-Dôme': '63',
        'Pyrénées-Atlantiques': '64',
        'Hautes-Pyrénées': '65',
        'Pyrénées-Orientales': '66',
        'Bas-Rhin': '67',
        'Haut-Rhin': '68',
        'Rhône': '69',
        'Haute-Saône': '70',
        'Saône-et-Loire': '71',
        'Sarthe': '72',
        'Savoie': '73',
        'Haute-Savoie': '74',
        'Paris': '75',
        'Seine-Maritime': '76',
        'Seine-et-Marne': '77',
        'Yvelines': '78',
        'Deux-Sèvres': '79',
        'Somme': '80',
        'Tarn': '81',
        'Tarn-et-Garonne': '82',
        'Var': '83',
        'Vaucluse': '84',
        'Vendée': '85',
        'Vienne': '86',
        'Haute-Vienne': '87',
        'Vosges': '88',
        'Yonne': '89',
        'Territoire de Belfort': '90',
        'Essonne': '91',
        'Hauts-de-Seine': '92',
        'Seine-Saint-Denis': '93',
        'Val-de-Marne': '94',
        'Val-d\'Oise': '95',
        'Guadeloupe': '971',
        'Martinique': '972',
        'Guyane': '973',
        'La Réunion': '974',
        'Saint-Pierre-et-Miquelon': '975',
        'Mayotte': '976',
        'Saint-Barthélemy': '977',
        'Saint-Martin': '978',
        'Wallis-et-Futuna': '986',
        'Polynésie française': '987',
        'Nouvelle-Calédonie': '988'
    }
    
    dep_options = st.selectbox("Département", list(options_dep.keys()))
    atm_options = st.selectbox("Conditions atmosphériques", list(options_atm.keys()))
    lumieres_options = st.selectbox("Conditions d'éclairage", list(options_lumieres.keys()))
    agg_options = st.selectbox("Localisation", list(options_agg.keys()))
    route_options = st.selectbox("Catégorie de route", list(options_route.keys()))
    col_options = st.selectbox("Type de collision", list(options_col.keys()))

# Importation des données
df_caracteristiques = pd.read_csv("streamlit/data/carcteristiques-2022.csv", sep=';')  # ../data/carcteristiques-2022.csv for local use
df_lieux = pd.read_csv("streamlit/data/lieux-2022.csv", sep=';', low_memory=False)
df_vehicules = pd.read_csv("streamlit/data/vehicules-2022.csv", sep=';')
df_usagers = pd.read_csv("streamlit/data/usagers-2022.csv", sep=';')

# Transformation des données
df_caracteristiques = df_caracteristiques.rename(columns={"long": "lon", "Accident_Id": "Num_Acc"})
df_caracteristiques['lat'] = df_caracteristiques['lat'].str.replace(',', '.').astype(float)
df_caracteristiques['lon'] = df_caracteristiques['lon'].str.replace(',', '.').astype(float)

# Jointure des données
df = pd.merge(df_caracteristiques, df_lieux, on='Num_Acc', how='left')
df = pd.merge(df, df_vehicules, on='Num_Acc', how='left')
df = pd.merge(df, df_usagers, on=['Num_Acc', 'id_vehicule'], how='left')

# Selectionner la vraie valeur
dep_op = options_dep[dep_options]
lum_op = options_lumieres[lumieres_options]
route_op = options_route[route_options]
agg_op = options_agg[agg_options]
atm_op = options_atm[atm_options]
col_op = options_col[col_options]

if on:
    # Conditions filtres
    filter_conditions = []

    if dep_op != 0:
        filter_conditions.append(df['dep'] == dep_op)
    if atm_op != 0:
        filter_conditions.append(df['atm'] == atm_op)
    if lum_op != 0:
        filter_conditions.append(df['lum'] == lum_op)
    if route_op != 0:
        filter_conditions.append(df['catr'] == route_op)
    if agg_op != 0:
        filter_conditions.append(df['agg'] == agg_op)
    if col_op != 0:
        filter_conditions.append(df['col'] == col_op)

    # Application des filtres
    if filter_conditions:
        df = df[np.logical_and.reduce(filter_conditions)]

# Statistiques générales header
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(label="🚧 Nombre d'accidents", value=f"{df['Num_Acc'].nunique()}")
with col2:
    st.metric(label="🚘 Nombre véhicules impliqués", value=f"{df['id_vehicule'].nunique()}")
with col3:
    st.metric(label="🧍 Nombre d'usagers impliqués", value=f"{df['id_usager'].nunique()}")
with col4:
    df_death = df[df['grav'] == 2]
    st.metric(label="💀 Nombre de décès", value=f"{df_death['id_usager'].nunique()}")
with col5:
    if len(df) > 0:
        st.metric(label="⚰️ Taux de létalité", value=f"{round(df_death['id_usager'].nunique() * 100 / df['Num_Acc'].nunique(), 2)} %")
    else:
        st.metric(label="⚰️ Taux de létalité", value=f"0%")

# Carte
st.map(df[['lat', 'lon']], color="#4b6adb", size=20)

hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """

st.markdown(hide_streamlit_style, unsafe_allow_html=True) 