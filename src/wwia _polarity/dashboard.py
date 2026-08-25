import streamlit as st
import pandas as pd
import plotly.express as px
from .ranking import rank_by_multipolarity_range
from .threshold import apply_threshold_vector, rank_countries_by_risk
from .multipolar import build_multipolar_matrix
from .multipolar_range import multipolar_range
from .gamification import GamificationEngine
from .config import load_config

st.set_page_config(page_title="WWIA Polarity Dashboard", layout="wide")
st.title("WWIA Polarity Bias & Range of Multipolarity Dashboard (v0.4.0)")

cfg = load_config()
clist = [c.strip() for c in cfg.get("default_countries", "US,IL,IR,SA,YE,TR,PK,UA,RU,CN").split(",")]

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Range Ranking", "Multipolar Matrix", "Cluster R(S)", "Threshold Flags", "Gamification"
])

with tab1:
    ranked = rank_by_multipolarity_range(clist)
    df = pd.DataFrame(ranked)
    st.dataframe(df, use_container_width=True)
    fig = px.bar(df, x="country", y="R_C", color="tier", title="Range of Multipolarity Ranking")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    M = build_multipolar_matrix(clist)
    st.dataframe(M.round(3), use_container_width=True)
    fig = px.imshow(M, text_auto=".2f", title="Directed Bias Matrix B_i→j")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    cluster_input = st.text_input("Cluster (comma-separated)", "US,IR,SA,TR,PK")
    if st.button("Compute R(S)"):
        countries = [c.strip() for c in cluster_input.split(",")]
        M = build_multipolar_matrix(countries)
        r = multipolar_range(M, countries)
        st.metric("Range of Multipolarity R(S)", f"{r:.3f}")

with tab4:
    flags = apply_threshold_vector(clist)
    st.json(flags)
    risk = rank_countries_by_risk(clist)
    st.dataframe(pd.DataFrame(risk), use_container_width=True)

with tab5:
    engine = GamificationEngine()
    st.subheader("Leaderboard")
    st.dataframe(pd.DataFrame(engine.leaderboard()), use_container_width=True)
    user = st.text_input("User ID", "analyst1")
    challenge = st.selectbox("Challenge", list(engine.challenges.keys()))
    if st.button("Award XP"):
        res = engine.award(user, challenge)
        st.success(res)
