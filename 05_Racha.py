import streamlit as st
import random
import pandas as pd
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="La Paradoja de la Racha - ITBA", layout="wide", initial_sidebar_state="collapsed")

# --- MEMORIA (Session State) ---
if 'exitos_RM_SAC_RM' not in st.session_state:
    st.session_state.exitos_RM_SAC_RM = 0
    st.session_state.exitos_SAC_RM_SAC = 0
    st.session_state.total_series = 0

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    
    /* Recuadro celeste de contexto */
    .context-box {
        background-color: #e2e8f0;
        border-radius: 15px;
        border-left: 10px solid #0074D9;
        padding: 25px;
        margin-bottom: 25px;
    }
    .context-box p {
        font-size: 20px !important;
        line-height: 1.6;
        color: #1e293b;
        margin: 0;
    }
    
    /* Resaltar y CENTRAR las pestañas de Streamlit */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #e2e8f0;
        padding: 10px;
        border-radius: 10px;
        justify-content: center; /* Centra las pestañas horizontalmente */
    }
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 5px;
        padding: 10px 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid transparent;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0074D9;
        border: 1px solid #001f3f;
    }
    .stTabs [aria-selected="true"] p {
        color: white !important;
        font-weight: bold;
    }

    /* Botón de retorno al Hub */
    .btn-nav {
        display: block;
        width: 100%;
        padding: 12px 0;
        background-color: #001f3f;
        color: #ffffff !important;
        text-align: center;
        border-radius: 10px;
        text-decoration: none !important;
        font-weight: 600;
        font-size: 16px;
        transition: background-color 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-top: 30px;
    }
    .btn-nav:hover, .btn-nav:visited, .btn-nav:active {
        text-decoration: none !important;
        color: white !important;
    }
    .btn-nav:hover {
        background-color: #0074D9;
    }

    /* --- PARCHE RESPONSIVO PARA CELULARES --- */
    @media (max-width: 768px) {
        h1 {
            font-size: 26px !important;
        }
        h3 {
            font-size: 16px !important;
        }
        .context-box {
            padding: 15px !important;
            text-align: center !important;
        }
        .context-box p {
            font-size: 16px !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            flex-wrap: wrap;
            justify-content: center !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- CABECERA ---
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    try:
        st.image('logo_itba.png', width=150)
    except:
        st.write("### ITBA")
with col_titulo:
    st.title("⚽ La Paradoja de la Racha")
st.write("---")

# --- RECUADRO DE CONTEXTO (CELESTE Y RESPONSIVO) ---
st.markdown("""
    <div class="context-box">
        <p>
            No siempre las probabilidades son <b><i>uniformes</i></b> como cuando tiramos un dado o una moneda al azar. 
            Si nuestro equipo juega la final de la Champions League contra el Real Madrid, por ejemplo, 
            lamentablemente será más probable la derrota que la victoria.
        </p>
    </div>
""", unsafe_allow_html=True)

# --- PESTAÑAS (Centradas desde el CSS) ---
tab1, tab2, tab3 = st.tabs(["🤔 El Dilema", "📊 La Simulación", "🧠 La Explicación"])

# --- TAB 1: EL DILEMA ---
with tab1:
    st.subheader("El desafío de la racha")
    st.markdown("""
    Tu equipo recibirá un premio si logra ganar **al menos dos partidos consecutivos** en una serie de 3.
    
    Tenés dos rivales posibles con estas probabilidades de victoria:
    * **Real Madrid (RM):** Muy difícil. Probabilidad: **20%** ($P_{RM}=0.20$).
    * **Sacachispas (SAC):** Más accesible. Probabilidad: **75%** ($P_{SAC}=0.75$).
    
    **¿Qué secuencia elegirías para maximizar tus chances de obtener el premio?** ¡Elegí una de las opciones y luego pasá a la pestaña de **📊 La Simulación** para poner a prueba tu intuición!
    """)
    
    # Recuadro único, más pequeño y centrado para evitar parecer botones
    col_vacia1, col_opciones, col_vacia2 = st.columns([1, 2, 1])
    with col_opciones:
        st.info("""
        **Opción A:** RM ➡️ SAC ➡️ RM
        
        **Opción B:** SAC ➡️ RM ➡️ SAC
        """)

# --- TAB 2: LA SIMULACIÓN ---
with tab2:
    st.subheader("Simulación de Series")
    st.write("Simulemos series de 3 partidos para ver cuál estrategia gana más veces en el largo plazo.")
    
    # Controles de simulación distribuidos en columnas
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    
    simular_10 = col_btn1.button("🏃 Simular 10 series")
    simular_100 = col_btn2.button("🏃 Simular 100 series")
    reiniciar = col_btn3.button("🗑️ Reiniciar Simulación")
    
    # Lógica de los botones
    if reiniciar:
        st.session_state.exitos_RM_SAC_RM = 0
        st.session_state.exitos_SAC_RM_SAC = 0
        st.session_state.total_series = 0
        st.rerun()
        
    series_a_simular = 0
    if simular_10:
        series_a_simular = 10
    elif simular_100:
        series_a_simular = 100
        
    if series_a_simular > 0:
        prob_rm = 0.20
        prob_sac = 0.75
        
        for _ in range(series_a_simular):
            st.session_state.total_series += 1
            
            # Simular RM - SAC - RM
            res_a = [random.random() < prob_rm, random.random() < prob_sac, random.random() < prob_rm]
            if res_a[1] and (res_a[0] or res_a[2]):
                st.session_state.exitos_RM_SAC_RM += 1
                
            # Simular SAC - RM - SAC
            res_b = [random.random() < prob_sac, random.random() < prob_rm, random.random() < prob_sac]
            if res_b[1] and (res_b[0] or res_b[2]):
                st.session_state.exitos_SAC_RM_SAC += 1

    # Gráfico (Responsivo, centrado y en porcentajes)
    if st.session_state.total_series > 0:
        col_graf_vacia1, col_grafico, col_graf_vacia2 = st.columns([1, 2, 1])
        
        with col_grafico:
            fig, ax = plt.subplots(figsize=(6, 4))
            etiquetas = ['RM-SAC-RM', 'SAC-RM-SAC']
            
            # Cálculo de porcentajes
            total = st.session_state.total_series
            pct_a = (st.session_state.exitos_RM_SAC_RM / total) * 100
            pct_b = (st.session_state.exitos_SAC_RM_SAC / total) * 100
            valores = [pct_a, pct_b]
            
            ax.bar(etiquetas, valores, color=['#3498db', '#e67e22'])
            ax.set_ylabel("Porcentaje de éxito (%)")
            # Título actualizado según tu pedido
            ax.set_title(f"% de resultados positivos con cada opción tras {total} series")
            
            # Asegurar que el eje Y tenga espacio para el texto arriba de las barras
            margen_y = max(valores) * 0.15 if max(valores) > 0 else 10
            ax.set_ylim(0, max(valores) + margen_y)
            
            # Etiquetas con formato de porcentaje (1 decimal)
            for i, v in enumerate(valores):
                ax.text(i, v + (margen_y * 0.2), f"{v:.1f}%", ha='center', fontweight='bold')
                
            st.pyplot(fig, use_container_width=True)
            
        st.info(f"💡 Llevamos {st.session_state.total_series} series. Sorprendentemente, jugar dos veces contra el Real Madrid suele dar mejores resultados.")

# --- TAB 3: LA EXPLICACIÓN ---
with tab3:
    st.subheader("🎓 El Veredicto Matemático")
    st.markdown("""
    Al igual que en Monty Hall o el cumpleaños, la intuición nos traiciona porque nos enfocamos en 
    lo "difícil" que es ganarle al Real Madrid. El secreto para entender este problema es identificar 
    cuáles son las combinaciones exitosas para una racha de 2 partidos en una serie de 3.
    
    Existen solo tres combinaciones que garantizan el premio (siendo G=Ganar y P=Perder):
    """)
    
    cols_exito = st.columns(3)
    for idx, combo in enumerate(["G - G - P", "P - G - G", "G - G - G"]):
        with cols_exito[idx]:
            st.success(f"Opción {idx+1}: **{combo}**")
            
    st.markdown("""
    ### La Importancia del Partido Central
    Observá que en los tres casos exitosos, **el segundo partido debe ganarse obligatoriamente**. 
    Si perdés el partido del medio, es imposible tener una racha de 2.
    
    Vamos a calcular las probabilidades para cada secuencia, usando las probabilidades que mencionamos:
    * $P(G_{RM}) = 0.20$ | $P(P_{RM}) = 0.80$
    * $P(G_{SAC}) = 0.75$ | $P(P_{SAC}) = 0.25$
    """)
    st.write("---")

    col_mat_a, col_mat_b = st.columns(2)
    
    with col_mat_a:
        st.markdown("#### Secuencia A: RM ➡️ SAC ➡️ RM")
        data_a = {
            'Combinación': ['GGG', 'GGP', 'PGG'],
            'P1 (RM)': ['0.20', '0.20', '0.80'],
            'P2 (SAC)': ['0.75', '0.75', '0.75'],
            'P3 (RM)': ['0.20', '0.80', '0.20'],
            'Prob (P1*P2*P3)': ['0.03', '0.12', '0.12']
        }
        df_a = pd.DataFrame(data_a)
        st.dataframe(df_a, use_container_width=True)
        st.metric("Probabilidad Total de Premio (Opción A)", "27.0%", help="Sumando: 0.03 + 0.12 + 0.12 = 0.27")

    with col_mat_b:
        st.markdown("#### Secuencia B: SAC ➡️ RM ➡️ SAC")
        data_b = {
            'Combinación': ['GGG', 'GGP', 'PGG'],
            'P1 (SAC)': ['0.75', '0.75', '0.25'],
            'P2 (RM)': ['0.20', '0.20', '0.20'],
            'P3 (SAC)': ['0.75', '0.25', '0.75'],
            'Prob (P1*P2*P3)': ['0.1125', '0.0375', '0.0375']
        }
        df_b = pd.DataFrame(data_b)
        st.dataframe(df_b, use_container_width=True)
        st.metric("Probabilidad Total de Premio (Opción B)", "18.75%")

    st.write("---")
    st.success("""
    💡 **Veredicto Final:** Aunque parezca contraintuitivo jugar dos veces contra el Real Madrid, la Opción A es mejor. 
    Esto se debe a que la **condición de racha** nos obliga a ganar el partido central. Al elegir **SAC-RM-SAC**, 
    estás forzando a tu equipo a superar el obstáculo más difícil (ganarle al Real Madrid) en el partido del medio. 
    En cambio, con **RM-SAC-RM**, el obstáculo central es contra Sacachispas, lo cual es mucho más probable de superar.
    """)

# --- BOTÓN DE RETORNO AL HUB ---
st.write("---")
col_vacia1, col_boton_regreso, col_vacia2 = st.columns([1, 1, 1])
with col_boton_regreso:
    st.markdown('<a href="https://future-day-2026-hub.streamlit.app/" target="_blank" class="btn-nav">🔙 Volver al Hub Principal</a>', unsafe_allow_html=True)
