import streamlit as st
import random
import pandas as pd
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="La Paradoja de la Racha - ITBA", layout="wide")

# --- MEMORIA (Session State) ---
if 'exitos_RM_SAC_RM' not in st.session_state:
    st.session_state.exitos_RM_SAC_RM = 0
    st.session_state.exitos_SAC_RM_SAC = 0
    st.session_state.total_series = 0

# --- BARRA LATERAL ---
with st.sidebar:
    try:
        st.image('logo_itba.png', use_container_width=True)
    except:
        st.write("ITBA - Future Day")
    
    st.header("Controles")
    if st.button("🗑️ Reiniciar Simulación"):
        st.session_state.exitos_RM_SAC_RM = 0
        st.session_state.exitos_SAC_RM_SAC = 0
        st.session_state.total_series = 0
        st.rerun()

# --- CUERPO PRINCIPAL ---
st.title("⚽ La Paradoja de la Racha")
st.write("---")

tab1, tab2, tab3 = st.tabs(["🤔 El Dilema", "📊 Simulación", "🧠 Explicación Académica"])

# --- TAB 1: EL DILEMA ---
with tab1:
    st.subheader("El desafío de la racha")
    st.markdown("""
    Tu equipo recibirá un premio si logra ganar **al menos dos partidos consecutivos** en una serie de 3.
    
    Tienes dos rivales posibles con estas probabilidades de victoria:
    * **Real Madrid (RM):** Muy difícil. Probabilidad: **20%** ($P_{RM}=0.20$).
    * **Sacachispas (SAC):** Más accesible. Probabilidad: **75%** ($P_{SAC}=0.75$).
    
    Debes elegir una de estas dos secuencias de partidos:
    1.  **RM - SAC - RM** (Jugar dos veces contra el difícil)
    2.  **SAC - RM - SAC** (Jugar dos veces contra el fácil)
    
    **¿Qué secuencia elegirías para maximizar tus chances de obtener el premio?**
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("**Opción A:** RM ➡️ SAC ➡️ RM")
    with col2:
        st.success("**Opción B:** SAC ➡️ RM ➡️ SAC")

# --- TAB 2: SIMULACIÓN ---
with tab2:
    st.subheader("Simulación de Series")
    st.write("Simulemos series de 3 partidos para ver cuál estrategia gana más veces en el largo plazo.")
    
    if st.button("🏃 Simular 10 series de cada tipo"):
        prob_rm = 0.20
        prob_sac = 0.75
        
        for _ in range(10):
            st.session_state.total_series += 1
            
            # Simular RM - SAC - RM
            res_a = [random.random() < prob_rm, random.random() < prob_sac, random.random() < prob_rm]
            # Éxito si hay una racha de 2: GGP o PGG o GGG
            if res_a[1] and (res_a[0] or res_a[2]):
                st.session_state.exitos_RM_SAC_RM += 1
                
            # Simular SAC - RM - SAC
            res_b = [random.random() < prob_sac, random.random() < prob_rm, random.random() < prob_sac]
            if res_b[1] and (res_b[0] or res_b[2]):
                st.session_state.exitos_SAC_RM_SAC += 1

    # Gráfico
    if st.session_state.total_series > 0:
        fig, ax = plt.subplots(figsize=(8, 4))
        etiquetas = ['RM-SAC-RM', 'SAC-RM-SAC']
        valores = [st.session_state.exitos_RM_SAC_RM, st.session_state.exitos_SAC_RM_SAC]
        
        ax.bar(etiquetas, valores, color=['#3498db', '#e67e22'])
        ax.set_ylabel("Cantidad de premios obtenidos")
        ax.set_title(f"Resultados tras {st.session_state.total_series} series")
        
        # Añadir etiquetas de valor sobre las barras
        for i, v in enumerate(valores):
            ax.text(i, v + 0.1, str(v), ha='center', fontweight='bold')
            
        st.pyplot(fig)
        
        st.info(f"💡 Llevamos {st.session_state.total_series} series. Sorprendentemente, jugar dos veces contra el Real Madrid suele dar mejores resultados. ¿Por qué?")

# --- TAB 3: EXPLICACIÓN ---
with tab3:
    st.subheader("🎓 El Veredicto Matemático")
    st.markdown("""
    Al igual que en Monty Hall o el cumpleaños, la intuición nos traiciona porque nos enfocamos en 
    lo "difícil" que es ganarle al Real Madrid. El secreto para entender este problema es identificar 
    cuáles son las combinaciones exitosas para una racha de 2 partidos en una serie de 3.
    
    Existen solo tres combinaciones que garantizan el premio (siendo G=Ganar y P=Perder):
    """)
    
    # Lista de combinaciones exitosas
    cols_exito = st.columns(3)
    for idx, combo in enumerate(["G - G - P", "P - G - G", "G - G - G"]):
        with cols_exito[idx]:
            st.success(f"Opción {idx+1}: **{combo}**")
            
    st.markdown("""
    ### La Importancia del Partido Central
    Observa que en los tres casos exitosos, **el segundo partido debe ganarse obligatoriamente**. 
    Si pierdes el partido del medio, es imposible tener una racha de 2.
    
    Vamos a calcular las probabilidades para cada secuencia, usando los datos de tu imagen:
    * $P(G_{RM}) = 0.20$ | $P(P_{RM}) = 0.80$
    * $P(G_{SAC}) = 0.75$ | $P(P_{SAC}) = 0.25$
    """)
    st.write("---")

    col_mat_a, col_mat_b = st.columns(2)
    
    with col_mat_a:
        st.markdown("#### Secuencia A: RM ➡️ SAC ➡️ RM")
        # Reproducimos la tabla de tu imagen en un DataFrame
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
        # Creamos la tabla análoga para la Secuencia B
        data_b = {
            'Combinación': ['GGG', 'GGP', 'PGG'],
            'P1 (SAC)': ['0.75', '0.75', '0.25'],
            'P2 (RM)': ['0.20', '0.20', '0.20'],
            'P3 (SAC)': ['0.75', '0.25', '0.75'],
            'Prob (P1*P2*P3)': ['0.1125', '0.0375', '0.0375']
        }
        df_b = pd.DataFrame(data_b)
        st.dataframe(df_b, use_container_width=True)
        # Suma: 0.1125 + 0.0375 + 0.0375 = 0.1875
        st.metric("Probabilidad Total de Premio (Opción B)", "18.75%")

    st.write("---")
    st.success("""
    💡 **Veredicto Final:** Aunque parezca contraintuitivo jugar dos veces contra el Real Madrid, la Opción A es mejor. 
    Esto se debe a que la **condición de racha** nos obliga a ganar el partido central. Al elegir **SAC-RM-SAC**, 
    estás forzando a tu equipo a superar el obstáculo más difícil (ganarle al Real Madrid) en el partido del medio. 
    En cambio, con **RM-SAC-RM**, el obstáculo central es contra Sacachispas, lo cual es mucho más probable de superar.
    """)