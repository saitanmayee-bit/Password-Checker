import streamlit as st
from main import check_password

# -------------------- PAGE CONFIGURATION --------------------

st.set_page_config(
    page_title="Smart Password Strength Checker",
    page_icon="🔐",
    layout="centered",
)

# -------------------- COLORS --------------------

COLORS = {
    "Invalid": "#64748B",
    "Weak": "#C62828",
    "Moderate": "#A85D00",
    "Strong": "#1769AA",
    "Very Strong": "#16803C",
}

# -------------------- SESSION STATE --------------------

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "password_input" not in st.session_state:
    st.session_state.password_input = ""

if "show_password" not in st.session_state:
    st.session_state.show_password = False


def clear_fields():
    st.session_state.password_input = ""
    st.session_state.show_password = False
    st.session_state.analysis = None


# -------------------- STYLING --------------------

st.markdown(
    """
    <style>
    /* Main page */
    .stApp {
        background-color: #F4F7FB;
        color: #172033;
    }

    .block-container {
        max-width: 720px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Make headings and normal text readable */
    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp p,
    .stApp label,
    .stApp [data-testid="stWidgetLabel"],
    .stApp [data-testid="stMarkdownContainer"] {
        color: #172033;
    }

    /* Password textbox */
    .stApp [data-testid="stTextInput"] input {
        background-color: #FFFFFF !important;
        color: #172033 !important;
        -webkit-text-fill-color: #172033 !important;
        border: 1px solid #B8C4D6 !important;
        border-radius: 8px;
    }

    .stApp [data-testid="stTextInput"] input::placeholder {
        color: #667085 !important;
        -webkit-text-fill-color: #667085 !important;
        opacity: 1;
    }


    /* Buttons */
    div.stButton > button {
        border-radius: 8px;
        min-height: 2.8rem;
        font-weight: 600;
    }

    /* Score and rating */
    .stApp [data-testid="stMetricLabel"],
    .stApp [data-testid="stMetricValue"] {
        color: #172033 !important;
    }

    /* Warning and information messages */
    .stApp [data-testid="stAlert"] p {
        color: #172033 !important;
    }

    /* Progress bar background */
    .stApp [data-testid="stProgress"] {
        background-color: #DFE6EF;
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# -------------------- HEADER --------------------

st.markdown(
    "<h1 style='text-align:center; color:#172033;'>"
    "🔐 Smart Password Strength Checker"
    "</h1>",
    unsafe_allow_html=True,
)

st.markdown(
    "<p style='text-align:center; color:#526078;'>"
    "Check password strength, identify risks, and get suggestions "
    "to improve your password."
    "</p>",
    unsafe_allow_html=True,
)

st.divider()

# -------------------- PASSWORD INPUT --------------------

st.subheader("Enter the Password")
# st.checkbox("Show password", key="show_password")
password_type = "default" if st.session_state.show_password else "password"

st.text_input(
    "Password",
    key="password_input",
    type=password_type,
    placeholder="Enter your password here",
    label_visibility="collapsed",
)

# -------------------- ACTION BUTTONS --------------------

check_col, clear_col = st.columns(2)

with check_col:
    check_clicked = st.button(
        "🔍 Check Password Strength",
        use_container_width=True,
        type="primary",
    )

with clear_col:
    st.button(
        "Clear",
        use_container_width=True,
        on_click=clear_fields,
    )

# -------------------- ANALYZE PASSWORD --------------------

if check_clicked:
    password = st.session_state.password_input

    if not password:
        st.session_state.analysis = None
        st.warning("Please enter a password first.")
    else:
        try:
            score, rating, suggestions, warnings = check_password(password)

            st.session_state.analysis = {
                "score": score,
                "rating": rating,
                "suggestions": suggestions,
                "warnings": warnings,
            }

        except Exception:
            st.session_state.analysis = None
            st.error(
                "The password could not be analyzed. "
                "Please check your password-checking function."
            )

# -------------------- DISPLAY RESULTS --------------------

analysis = st.session_state.analysis

if analysis is None:
    st.info("Enter a password and click Check Password Strength to see your analysis.")

else:
    score = analysis["score"]
    rating = analysis["rating"]
    suggestions = analysis["suggestions"]
    warnings = analysis["warnings"]

    rating_color = COLORS.get(rating, COLORS["Invalid"])

    st.divider()
    st.subheader("Strength Analysis")

    score_col, rating_col = st.columns(2)

    with score_col:
        st.metric("Strength Score", f"{score}/5")

    with rating_col:
        st.markdown(
            f"<div style='padding-top:8px;'>"
            f"<span style='color:{rating_color}; font-size:1.3rem;"
            f"font-weight:700;'>{rating}</span></div>",
            unsafe_allow_html=True,
        )

    # Strength meter
    st.progress(max(0.0, min(float(score) / 5.0, 1.0)))

    if warnings:
        st.subheader("⚠️ Security Warnings")
        for warning in warnings:
            st.warning(str(warning))
    else:
        st.success("No warnings detected by the current checks.")

    if suggestions:
        st.subheader("💡 Suggestions")
        for suggestion in suggestions:
            st.markdown(f"- {suggestion}")
    else:
        st.write("All basic checks passed.")

    st.caption(
        "A strong score does not guarantee that a password has never "
        "been exposed or cannot be guessed."
    )

# -------------------- FOOTER --------------------

st.divider()
st.caption("Smart Password Strength Checker | Built with Python and Streamlit")
