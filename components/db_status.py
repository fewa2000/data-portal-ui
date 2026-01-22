"""
Database Status Component.
Displays database connection status in the sidebar.
"""

import streamlit as st
from services import api


def render_db_status() -> None:
    """
    Render database connection status indicator.
    Shows connected/disconnected status with database and server info.
    """
    status = api.get_database_status()

    if status["connected"]:
        st.markdown("**Database**")
        st.markdown(f":green[Connected]")
        st.caption(f"DB: {status['database']}")
        st.caption(f"Server: {status['server']}")
    else:
        st.markdown("**Database**")
        st.markdown(f":red[Disconnected]")
        if status["error"]:
            st.caption(f"Error: {status['error'][:50]}...")
