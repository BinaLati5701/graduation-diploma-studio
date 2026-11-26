import streamlit as st
from project import (
    GOWN_STYLES,
    HONORS_LIST,
    Graduate,
    create_diploma_pdf,
    fetch_quote,
    generate_regalia_gif,
)

st.set_page_config(
    page_title="Graduation Diploma & Regalia Studio | Sabina Dovlati",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 Interactive Graduation Diploma & Regalia Studio")
st.caption("Built in Python (OOP, REST API, Pillow GIF Animation & fpdf2 HTML-to-PDF) — Try it live below!")

col_controls, col_preview = st.columns([1, 1.2], gap="large")

with col_controls:
    st.subheader("Customize Your Diploma")
    name = st.text_input("Recipient Name", value="Future Tech Leader")
    degree = st.text_input("Degree or Title", value="Master of Engineering & Innovation")
    gown_style = st.selectbox("Select Regalia Style", list(GOWN_STYLES.keys()))
    honors = st.selectbox("Select Honors Distinction", HONORS_LIST, index=2)
    refresh_quote = st.button("🔄 Fetch New Inspirational Quote (API)")

if "quote" not in st.session_state or refresh_quote:
    st.session_state.quote = fetch_quote()

safe_name = name.strip() or "Honored Guest"
grad = Graduate(name=safe_name, degree=degree, gown_style=gown_style, honors=honors)
gif_path = generate_regalia_gif(grad, "regalia.gif")
pdf_path = create_diploma_pdf(grad, st.session_state.quote, gif_path, "diploma.pdf")

with col_preview:
    st.subheader(f"Live Preview for {grad.name}")
    st.image(gif_path, caption=f"{grad.gown_style} — {grad.honors}", width=320)
    st.info(st.session_state.quote)

    with open(pdf_path, "rb") as pdf_file:
        st.download_button(
            label="📄 Download Personalized Diploma (PDF)",
            data=pdf_file,
            file_name=f"{grad.name.replace(' ', '_')}_Diploma.pdf",
            mime="application/pdf",
            type="primary",
        )

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>&copy; 2026 Sabina Dovlati. All rights reserved. | "
    "<a href='https://github.com/BinaLati5701/graduation-diploma-studio'>Source Code on GitHub</a></p>",
    unsafe_allow_html=True,
)