# =====================================================
# frontend/components/auth.py
# FINAL AUTH HELPERS
# =====================================================

import streamlit as st


# =====================================================
# LOGIN
# =====================================================

def login_user():

    st.session_state.logged_in = True

    st.session_state.page = "analyze"


# =====================================================
# LOGOUT
# =====================================================

def logout_user():

    st.session_state.logged_in = False

    st.session_state.page = "landing"

    st.rerun()


# =====================================================
# CHECK LOGIN
# =====================================================

def is_logged_in():

    return st.session_state.get(
        "logged_in",
        False
    )