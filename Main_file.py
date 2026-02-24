import streamlit as st
import os

# Define pages
home_page = st.Page("Home.py", title="Home", icon="🏠",default=True)
about_us = st.Page("About_us.py", title="About", icon="🎧")

# Navigation
Run = st.navigation([home_page, about_us])

# Fixed Logo Path (Uses relative path now)
if os.path.exists("Audio_Book.jpg"):
   st.logo("Audio_Book.jpg")

st.sidebar.divider()
st.sidebar.write("✨ Your Personal Audio Book Creator")

Run.run()