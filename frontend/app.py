# =====================================================
# frontend/app.py
# FINAL CLEAN ROUTING
# =====================================================

import streamlit as st

from components.styles import load_css
from components.landing import show_landing
from auth_page import show_auth_page
from components.analyze import show_analyze
from components.dashboard import show_dashboard


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(

    page_title="AI Reliability Platform",

    layout="wide",

    initial_sidebar_state="collapsed"
)


# =====================================================
# LOAD CSS
# =====================================================

load_css()


# =====================================================
# SESSION STATE
# =====================================================

if "page" not in st.session_state:

    st.session_state.page = "landing"

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


# =====================================================
# ROUTING
# =====================================================

page = st.session_state.page


# =====================================================
# LANDING
# =====================================================

if page == "landing":

    show_landing()


# =====================================================
# AUTH
# =====================================================

elif page == "auth":

    show_auth_page()


# =====================================================
# ANALYZE
# =====================================================

elif page == "analyze":

    if st.session_state.logged_in:

        show_analyze()

    else:

        st.session_state.page = "auth"

        st.rerun()


# =====================================================
# DASHBOARD
# =====================================================

elif page == "dashboard":

    if st.session_state.logged_in:

        show_dashboard()

    else:

        st.session_state.page = "auth"

        st.rerun()


# =====================================================
# FALLBACK
# =====================================================

else:

    st.session_state.page = "landing"

    st.rerun()