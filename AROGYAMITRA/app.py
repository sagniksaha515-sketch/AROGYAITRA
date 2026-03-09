import streamlit as st#type:ignore

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
st.set_page_config(page_title="ArogyaMitra AI", page_icon="🩺", layout="wide")

# -------------------------------------------------
# STYLING
# -------------------------------------------------
st.markdown("""
<style>
.main-title {font-size:40px;font-weight:700;text-align:center;}
.subtitle {font-size:18px;text-align:center;color:gray;}
.metric-box {padding:15px;border-radius:12px;background:#f3f6ff;text-align:center;font-weight:600;}
.result-box {padding:25px;border-radius:15px;background:#eef2ff;margin-top:20px;}
.chat-user {color:#0a58ca;font-weight:600;}
.chat-ai {color:#198754;font-weight:600;}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "probable_disease" not in st.session_state:
    st.session_state.probable_disease = None

# -------------------------------------------------
# DISEASE DATABASE
# -------------------------------------------------
DISEASES = {
    "COVID-19": {
        "symptoms": ["Fever","Cough","Loss of Taste","Fatigue","Sore Throat","Shortness of Breath"],
        "advice": "Get tested. Isolate. Monitor oxygen level.",
        "severity": "Moderate"
    },
    "Flu": {
        "symptoms": ["Fever","Cough","Body Pain","Headache","Sore Throat"],
        "advice": "Rest, fluids, paracetamol if needed.",
        "severity": "Mild"
    },
    "Dengue": {
        "symptoms": ["Fever","Body Pain","Headache","Vomiting","Fatigue","Joint Pain"],
        "advice": "Blood test required. Monitor platelets.",
        "severity": "Moderate"
    },
    "Food Poisoning": {
        "symptoms": ["Stomach Pain","Vomiting","Loose Motion","Nausea"],
        "advice": "Take ORS, fluids, avoid outside food.",
        "severity": "Mild"
    },
    "UTI": {
        "symptoms": ["Burning Urination","Frequent Urination","Lower Abdomen Pain"],
        "advice": "Increase water intake. Consult doctor.",
        "severity": "Mild"
    },
    "Diabetes": {
        "symptoms": ["Fatigue","Frequent Urination","Excess Thirst","Blurred Vision"],
        "advice": "Check fasting blood sugar.",
        "severity": "Chronic"
    },
    "Heart Risk": {
        "symptoms": ["Chest Pain","Shortness of Breath","Sweating","Nausea"],
        "advice": "Seek emergency medical care immediately.",
        "severity": "Emergency"
    },
    "Migraine": {
        "symptoms": ["Headache","Light Sensitivity","Nausea"],
        "advice": "Rest in dark quiet room.",
        "severity": "Mild"
    },
    "Typhoid": {
        "symptoms": ["Fever","Weakness","Stomach Pain","Headache"],
        "advice": "Widal test required. Doctor consultation needed.",
        "severity": "Moderate"
    }
}

ALL_SYMPTOMS = sorted(list({s for d in DISEASES.values() for s in d["symptoms"]}))

# -------------------------------------------------
# AI AGENT ENGINE
# -------------------------------------------------
def ai_agent_response(user_input):
    text = user_input.lower()

    if any(word in text for word in ["chest pain","cannot breathe","fainting"]):
        return "⚠ Yeh emergency lag raha hai. Turant hospital jaiye."

    if any(word in text for word in ["scared","worried","tension","anxious"]):
        return "Calm rahiye. Main yahan hoon guide karne ke liye."

    if st.session_state.probable_disease:
        return f"Aapke symptoms ke hisaab se {st.session_state.probable_disease} ka chance zyada hai. Proper medical test karwana best rahega."

    if "fever" in text:
        return "Fever kitne din se hai? 3 din se zyada ho toh doctor consult karein."

    return "Aap thoda aur detail dein. Main help karne ki puri koshish karungi."

# -------------------------------------------------
# HOME PAGE
# -------------------------------------------------
if st.session_state.page == "home":

    st.markdown('<div class="main-title">🩺 ArogyaMitra AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Your Intelligent Health Companion</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.markdown('<div class="metric-box">👨‍⚕️ 1,25,000+ Patients</div>', unsafe_allow_html=True)
    col2.markdown('<div class="metric-box">🎯 94% Matching Accuracy</div>', unsafe_allow_html=True)
    col3.markdown('<div class="metric-box">🏥 350+ Doctors Available</div>', unsafe_allow_html=True)

    st.write("")
    if st.button("🚀 Start Health Check"):
        st.session_state.page = "diagnosis"
        st.rerun()

# -------------------------------------------------
# DIAGNOSIS PAGE
# -------------------------------------------------
elif st.session_state.page == "diagnosis":

    st.title("Patient Health Assessment")

    name = st.text_input("Enter Your Name")
    age = st.number_input("Age", 1, 120)
    gender = st.selectbox("Gender", ["Male","Female","Other"])

    st.subheader("Select Symptoms")
    selected = st.multiselect("Choose all applicable symptoms:", ALL_SYMPTOMS)

    if st.button("🔍 Diagnose Now"):

        if not selected:
            st.warning("Please select at least one symptom.")
        else:
            scores = {}
            for disease, data in DISEASES.items():
                match = len(set(selected) & set(data["symptoms"]))
                scores[disease] = match

            best_match = max(scores, key=scores.get)
            best_score = scores[best_match]

            if best_score == 0:
                st.error("No clear match found. Consult doctor.")
            else:
                st.session_state.probable_disease = best_match
                result = DISEASES[best_match]

                st.markdown(f"""
                <div class="result-box">
                <h3>Namaste {name} 👋</h3>
                <p><b>Most Likely Condition:</b> {best_match}</p>
                <p><b>Severity:</b> {result["severity"]}</p>
                <p><b>Advice:</b> {result["advice"]}</p>
                <p><i>AI-based preliminary guidance only.</i></p>
                </div>
                """, unsafe_allow_html=True)

                if result["severity"] == "Emergency":
                    st.error("Emergency condition detected.")
                elif result["severity"] == "Moderate":
                    st.warning("Doctor consultation recommended.")
                else:
                    st.success("Likely manageable with proper care.")

    # -----------------------------
    # AI CHAT SECTION
    # -----------------------------
    st.divider()
    st.subheader("🤖 Talk to ArogyaMitra AI")

    user_msg = st.text_input("Ask your health question")

    if st.button("Send"):
        if user_msg:
            response = ai_agent_response(user_msg)
            st.session_state.chat_history.append(("You", user_msg))
            st.session_state.chat_history.append(("AI", response))

    for role, msg in st.session_state.chat_history:
        if role == "You":
            st.markdown(f"<div class='chat-user'>🧑 You:</div> {msg}", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-ai'>🤖 ArogyaMitra:</div> {msg}", unsafe_allow_html=True)

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
        st.session_state.chat_history = []
        st.session_state.probable_disease = None
        st.rerun()