import streamlit as st
import pandas as pd
import json
import os
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# SAVE / LOAD DATA
DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "mood": 180,
        "sleep": 6,
        "skills": {
            "Coding": 80,
            "Learning": 70,
            "Editing": 60,
            "Gym": 50
        }
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

data = load_data()

# CSS
st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle at top, #1a1a2e, #0b0b17);
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0b0b17;
}

/* Card */
.card {
    background: rgba(255,255,255,0.05);
    padding: 18px;
    border-radius: 18px;
    backdrop-filter: blur(15px);
    border: 1px solid rgba(168,85,247,0.2);
    box-shadow: 0 0 15px rgba(168,85,247,0.15);
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 0 25px rgba(168,85,247,0.6);
}

/* Titles */
h1, h2, h3 {
    background: linear-gradient(90deg, #c084fc, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Progress */
div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #a855f7, #c084fc);
    box-shadow: 0 0 10px #a855f7;
}

</style>
""", unsafe_allow_html=True)

# SIDEBAR 

st.sidebar.title("🎮 Menu")

page = st.sidebar.radio("Go to", ["Dashboard", "Stats"])

st.sidebar.markdown("---")
st.sidebar.subheader("👤 Player")

level = int(sum(data["skills"].values()) / 40)

st.sidebar.write(f"Level: {level}")
st.sidebar.progress(level / 100)

# DASHBOARD PAGE

if page == "Dashboard":

    col1, col2, col3 = st.columns([2,1,1])

    # Mood
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Mood Score")

        data["mood"] = st.slider("Mood", 0, 300, data["mood"])
        st.progress(data["mood"] / 300)

        st.markdown('</div>', unsafe_allow_html=True)

    # Sleep
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Sleep")
        data["sleep"] = st.slider("Hours", 0, 12, data["sleep"])
        st.write(f"{data['sleep']} hrs")
        st.markdown('</div>', unsafe_allow_html=True)

    # Habit chart
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Habits")

        fig = go.Figure(go.Bar(
            x=["M","T","W","T","F"],
            y=[3,5,4,6,7],
            marker_color="#c084fc"
        ))

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white")
        )

        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Skills
    st.subheader("Skills")

    cols = st.columns(len(data["skills"]))

    for i, (skill, val) in enumerate(data["skills"].items()):
        with cols[i]:
            new_val = st.slider(skill, 0, 100, val)
            data["skills"][skill] = new_val
            st.progress(new_val / 100)

    # Save button
    if st.button("💾 Save Progress"):
        save_data(data)
        st.success("Saved!")

# STATS PAGE

if page == "Stats":

    st.subheader("📊 Skill Stats")

    df = pd.DataFrame({
        "Skill": list(data["skills"].keys()),
        "Value": list(data["skills"].values())
    })

    fig = go.Figure(go.Bar(
        x=df["Skill"],
        y=df["Value"],
        marker_color="#c084fc"
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )

    st.plotly_chart(fig, use_container_width=True)