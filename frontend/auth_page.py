# =====================================================
# frontend/auth_page.py
# FINAL APPLE-STYLE AUTH PAGE
# =====================================================

import streamlit as st

from components.auth import login_user


# =====================================================
# AUTH PAGE
# =====================================================

def show_auth_page():

    # =====================================================
    # TITLE
    # =====================================================

    st.title(
        "Welcome Back"
    )

    st.markdown(
        """
        <div class="subtitle">

        Sign in to access AI model diagnostics,
        explainability analytics and reliability intelligence.

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")
    st.write("")

    # =====================================================
    # CENTER CARD
    # =====================================================

    left, center, right = st.columns([2,3,2])

    with center:

        st.markdown(
            """
            <div class="glass-card">
            """,
            unsafe_allow_html=True
        )

        st.subheader(
            "Authentication"
        )

        st.write("")

        auth_mode = st.radio(

            "Select Option",

            [

                "Login",

                "Register"
            ],

            horizontal=True
        )

        st.write("")

        username = st.text_input(
            "Username"
        )

        password = st.text_input(

            "Password",

            type="password"
        )

        # =====================================================
        # REGISTER
        # =====================================================

        if auth_mode == "Register":

            confirm_password = st.text_input(

                "Confirm Password",

                type="password"
            )

            st.write("")

            if st.button(
                "Create Account",
                width="stretch"
            ):

                if (
                    username.strip() == ""
                    or
                    password.strip() == ""
                ):

                    st.error(
                        "Please fill all fields."
                    )

                elif password != confirm_password:

                    st.error(
                        "Passwords do not match."
                    )

                else:

                    st.success(
                        "Registration successful."
                    )

                    login_user()

                    st.rerun()

        # =====================================================
        # LOGIN
        # =====================================================

        else:

            st.write("")

            if st.button(
                "Login",
                width="stretch"
            ):

                if (
                    username.strip() == ""
                    or
                    password.strip() == ""
                ):

                    st.error(
                        "Please fill all fields."
                    )

                else:

                    login_user()

                    st.rerun()

        st.write("")
        st.write("")

        if st.button(
            "← Back to Home",
            width="stretch"
        ):

            st.session_state.page = "landing"

            st.rerun()

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )