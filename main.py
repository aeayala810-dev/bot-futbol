import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# 1. CONFIGURACIÓN DE PÁGINA Y DISEÑO PRO
st.set_page_config(
    page_title="Fútbol Pro Bot 2026",
    page_icon="⚽",
    layout="wide"
)

# Estilo visual "Dark Mode" con acentos verde neón
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: white; }
    .noticia-box {
        background-color: #161b22;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #00ff88;
        margin-bottom: 15px;
    }
    a { color: #00ff88 !important; text-decoration: none; }
    </style>
    """, unsafe_allow_html=True)

# 2. CONFIGURACIÓN DE DATOS (API Y SCRAPING)
# Pega aquí tu clave de la imagen de API-Sports
API_KEY = "3ec50370b252520f709af687070b1d81" 

def obtener_resultados_vivos():
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': API_KEY
    }
    try:
        response = requests.get(url, headers=headers)
        return response.json().get('response', [])
    except:
        return []

def buscar_noticias_ilimitadas():
    # Scraping de Google News (Ilimitado y Gratis)
    url = "https://news.google.com/rss/search?q=fichajes+futbol+actualidad&hl=es-419&gl=MX&ceid=MX:es-419"
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, features="xml")
        return soup.find_all('item', limit=10)
    except:
        return []

# 3. INTERFAZ DEL BOT
st.title("⚽ Football Intelligence Hub v1.0")
st.write("Datos actualizados al momento • Sin suscripciones")

# Sidebar - Menú Lateral
with st.sidebar:
    st.header("Menú Principal")
    opcion = st.radio("Navegar a:", ["📰 Noticias y Fichajes", "🏟️ Resultados en Vivo", "💰 Mercado y Valores"])
    st.divider()
    st.info("Este bot usa Web Scraping para datos ilimitados.")

# SECCIÓN: NOTICIAS
if opcion == "📰 Noticias y Fichajes":
    st.header("Última Hora: Mercado de Pases")
    if st.button("🔄 Actualizar Noticias"):
        noticias = buscar_noticias_ilimitadas()
        for n in noticias:
            st.markdown(f"""
            <div class="noticia-box">
                <h4>{n.title.text}</h4>
                <p style="font-size: 0.8rem; color: gray;">{n.pubDate.text}</p>
                <a href="{n.link.text}" target="_blank">Leer más →</a>
            </div>
            """, unsafe_allow_html=True)

# SECCIÓN: RESULTADOS EN VIVO
elif opcion == "🏟️ Resultados en Vivo":
    st.header("Marcadores en Tiempo Real")
    partidos = obtener_resultados_vivos()
    
    if not partidos:
        st.warning("No hay partidos en vivo en este momento o la API Key no está configurada.")
    else:
        for p in partidos:
            col1, col2, col3 = st.columns([2, 1, 2])
            with col1:
                st.write(f"**{p['teams']['home']['name']}**")
            with col2:
                st.subheader(f"{p['goals']['home']} - {p['goals']['away']}")
            with col3:
                st.write(f"**{p['teams']['away']['name']}**")
            st.caption(f"Minuto: {p['fixture']['status']['elapsed']}' | {p['league']['name']}")
            st.divider()

# SECCIÓN: MERCADO Y VALORES
elif opcion == "💰 Mercado y Valores":
    st.header("Buscador de Valores de Mercado")
    jugador = st.text_input("Escribe el nombre de un jugador:")
    if jugador:
        st.info(f"Buscando información de {jugador}...")
        col1, col2 = st.columns(2)
        with col1:
            st.success("Valor Estimado: Consultando fuentes públicas...")
            # Enlace directo a Transfermarkt (El estándar de valores)
            tm_url = f"https://www.transfermarkt.es/schnellsuche/ergebnis/schnellsuche?query={jugador.replace(' ', '+')}"
            st.markdown(f"[🔗 Ver ficha financiera en Transfermarkt]({tm_url})")
        with col2:
            st.write("📊 Historial de transferencias disponible en el enlace.")