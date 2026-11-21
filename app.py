"""
CarePulse - Primary Treatment Guide
A complete first-aid website written in 100% Python (Streamlit).

Run:
    pip install streamlit
    streamlit run app.py
"""

import random
import streamlit as st

st.set_page_config(
    page_title="CarePulse | Primary Treatment Guide",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# DATA
# ----------------------------------------------------------------------------
FIRST_AID = {
    "Burns": {
        "icon": "🔥", "category": "Injury", "severity": "Moderate",
        "steps": [
            "Move the person away from the heat source.",
            "Cool the burn under cool (not ice-cold) running water for 20 minutes.",
            "Remove rings, watches or tight clothing near the burn before swelling starts.",
            "Cover loosely with a clean, non-fluffy cloth or cling film.",
            "Give small sips of water if the person is conscious.",
        ],
        "dont": ["Do not apply ice, butter, toothpaste or oil.", "Do not burst blisters.", "Do not remove clothing stuck to the skin."],
        "emergency": "Call 108/112 if the burn is large, deep, on the face/hands/genitals, or caused by chemicals or electricity.",
    },
    "Severe Bleeding / Cuts": {
        "icon": "🩸", "category": "Injury", "severity": "High",
        "steps": [
            "Wash your hands or wear gloves if available.",
            "Press firmly on the wound with a clean cloth or gauze.",
            "Keep pressing continuously; do not lift to check.",
            "Raise the injured limb above heart level if no fracture is suspected.",
            "Add more cloth on top if blood soaks through, then bandage firmly.",
        ],
        "dont": ["Do not remove embedded objects.", "Do not use a tight tourniquet unless trained and bleeding is life-threatening."],
        "emergency": "Call 108/112 if bleeding does not slow after 10 minutes of pressure or the person feels faint.",
    },
    "CPR (Adult)": {
        "icon": "❤️", "category": "Life Saving", "severity": "Critical",
        "steps": [
            "Check for response and breathing. Shout for help and call 108/112.",
            "Place the heel of one hand on the centre of the chest, other hand on top.",
            "Push hard and fast: 5-6 cm deep at 100-120 compressions per minute.",
            "If trained, give 2 rescue breaths after every 30 compressions.",
            "If untrained, continue hands-only compressions without stopping.",
            "Use an AED as soon as one is available and follow its voice prompts.",
            "Continue until help arrives or the person starts breathing.",
        ],
        "dont": ["Do not stop compressions for long pauses.", "Do not give CPR to a person who is awake and breathing normally."],
        "emergency": "Call 108/112 immediately. CPR is for an unresponsive person who is not breathing normally.",
    },
    "Choking (Adult)": {
        "icon": "😮‍💨", "category": "Life Saving", "severity": "Critical",
        "steps": [
            "Ask 'Are you choking?' If they cannot speak, cough or breathe, act fast.",
            "Lean them forward and give up to 5 firm back blows between the shoulder blades.",
            "If still blocked, give up to 5 abdominal thrusts (stand behind, fist above navel, pull inwards and upwards).",
            "Alternate 5 back blows and 5 thrusts until the object comes out.",
            "If the person becomes unresponsive, call for help and start CPR.",
        ],
        "dont": ["Do not slap the back if the person is coughing strongly.", "Do not put fingers blindly in the mouth."],
        "emergency": "Call 108/112 if the blockage is not cleared quickly or the person loses consciousness.",
    },
    "Fracture / Broken Bone": {
        "icon": "🦴", "category": "Injury", "severity": "High",
        "steps": [
            "Keep the person still and calm; do not move the injured part.",
            "Support the limb in the position found using padding or a splint.",
            "Apply a cold pack wrapped in cloth to reduce swelling.",
            "Control any bleeding with gentle pressure around the wound.",
            "Treat for shock: keep warm and lying down.",
        ],
        "dont": ["Do not try to straighten the bone.", "Do not let the person eat or drink in case surgery is needed."],
        "emergency": "Call 108/112 for suspected head, neck, back or thigh bone injury, or if bone is visible.",
    },
    "Nosebleed": {
        "icon": "👃", "category": "Common", "severity": "Low",
        "steps": [
            "Sit upright and lean slightly forward.",
            "Pinch the soft part of the nose firmly for 10 minutes.",
            "Breathe through the mouth and spit out any blood.",
            "Apply a cold cloth on the nose bridge.",
        ],
        "dont": ["Do not tilt the head back.", "Do not blow the nose for several hours."],
        "emergency": "Seek medical help if bleeding lasts more than 20 minutes or follows a head injury.",
    },
    "Fainting": {
        "icon": "😵", "category": "Common", "severity": "Low",
        "steps": [
            "Lay the person flat on their back.",
            "Raise their legs about 30 cm above heart level.",
            "Loosen tight clothing and ensure fresh air.",
            "Check breathing. Once awake, let them sit up slowly and sip water.",
        ],
        "dont": ["Do not give food or drink until fully awake.", "Do not make them stand up quickly."],
        "emergency": "Call 108/112 if they do not wake within 1 minute, are injured, pregnant, or have chest pain.",
    },
    "Heat Stroke": {
        "icon": "🌡️", "category": "Environmental", "severity": "High",
        "steps": [
            "Move the person to a cool, shaded place.",
            "Remove extra clothing and cool the body with wet cloths or fan.",
            "Apply cold packs to the neck, armpits and groin.",
            "Give sips of cool water if fully conscious.",
        ],
        "dont": ["Do not give alcohol or caffeine.", "Do not force fluids on an unconscious person."],
        "emergency": "Call 108/112 - heat stroke (confusion, hot dry skin, very high temperature) is an emergency.",
    },
    "Snake Bite": {
        "icon": "🐍", "category": "Environmental", "severity": "Critical",
        "steps": [
            "Keep the person calm and as still as possible.",
            "Immobilise the bitten limb at or slightly below heart level.",
            "Remove rings, watches and tight items near the bite.",
            "Note the time of the bite and the snake's appearance if safe.",
            "Take the person to the nearest hospital with anti-venom immediately.",
        ],
        "dont": ["Do not cut, suck or burn the wound.", "Do not apply ice or a tight tourniquet.", "Do not try to catch the snake."],
        "emergency": "Call 108/112 immediately for every suspected venomous snake bite.",
    },
    "Poisoning": {
        "icon": "☠️", "category": "Emergency", "severity": "Critical",
        "steps": [
            "Remove the person from the source (fumes, chemicals).",
            "Check breathing and call 108/112 or a poison helpline.",
            "Keep the container or a sample of the substance to show the doctors.",
            "If the person is unconscious but breathing, place in recovery position.",
        ],
        "dont": ["Do not induce vomiting unless a medical professional advises it.", "Do not give anything to eat or drink unless told to."],
        "emergency": "Always call emergency services for suspected poisoning.",
    },
    "Allergic Reaction": {
        "icon": "🤧", "category": "Emergency", "severity": "High",
        "steps": [
            "Help the person avoid the trigger (food, sting, medicine).",
            "If they have an adrenaline (epinephrine) auto-injector, help them use it right away.",
            "Lay them down with legs raised; sit up if breathing is difficult.",
            "Call 108/112 for swelling of face/throat, wheezing or breathlessness.",
        ],
        "dont": ["Do not leave the person alone.", "Do not give oral medicine if they have trouble swallowing."],
        "emergency": "Throat swelling, breathing trouble or collapse (anaphylaxis) needs emergency care.",
    },
    "Seizure": {
        "icon": "⚡", "category": "Emergency", "severity": "High",
        "steps": [
            "Stay calm and note the time the seizure started.",
            "Clear hard or sharp objects away; cushion the head.",
            "Loosen tight clothing around the neck.",
            "When shaking stops, turn them on their side (recovery position).",
        ],
        "dont": ["Do not hold the person down.", "Do not put anything in their mouth."],
        "emergency": "Call 108/112 if it lasts more than 5 minutes, repeats, or it is their first seizure.",
    },
    "Fever": {
        "icon": "🤒", "category": "Common", "severity": "Low",
        "steps": [
            "Rest and drink plenty of fluids.",
            "Wear light clothing and keep the room comfortably cool.",
            "Sponge with lukewarm water if uncomfortable.",
            "Take paracetamol only as directed on the label or by a doctor.",
        ],
        "dont": ["Do not use ice-cold water or alcohol rubs.", "Do not give aspirin to children."],
        "emergency": "See a doctor for fever above 39.5 C, lasting over 3 days, stiff neck, rash, or in infants under 3 months.",
    },
}

SYMPTOMS = {
    "Chest pain / pressure": ("🚨", "Possible heart emergency. Call 108/112 now, keep the person seated and calm.", True),
    "Difficulty breathing": ("🚨", "Sit upright, loosen clothing and call 108/112 immediately.", True),
    "Unconscious / not responding": ("🚨", "Check breathing, call 108/112 and start CPR if not breathing normally.", True),
    "Heavy bleeding": ("🚨", "Apply firm direct pressure and call 108/112.", True),
    "Fever": ("🤒", "Rest, fluids, light clothing. See a doctor if above 39.5 C or lasting 3+ days.", False),
    "Headache": ("🤕", "Rest in a quiet dark room, drink water. Seek care if sudden and severe.", False),
    "Vomiting / diarrhoea": ("🤢", "Sip ORS (oral rehydration solution) frequently. See a doctor if it lasts over 24 hours.", False),
    "Cough / sore throat": ("😷", "Warm fluids, rest. See a doctor if it lasts over a week or breathing is hard.", False),
    "Minor cut / scrape": ("🩹", "Wash with clean water, cover with a clean dressing.", False),
    "Sprain / muscle pain": ("🦵", "Follow RICE: Rest, Ice (wrapped), Compression, Elevation.", False),
    "Dizziness": ("😵‍💫", "Sit or lie down, drink water. Seek care if it keeps happening.", False),
}

QUIZ = [
    ("How long should a burn be cooled under running water?",
     ["2 minutes", "20 minutes", "1 hour", "Never"], 1),
    ("What is the recommended CPR compression rate for adults?",
     ["40-60 per min", "60-80 per min", "100-120 per min", "150-180 per min"], 2),
    ("Which number is the all-in-one emergency number in India?",
     ["100", "112", "1098", "104"], 1),
    ("Which is correct for a nosebleed?",
     ["Tilt head back", "Lean forward and pinch the soft part", "Lie flat", "Blow the nose hard"], 1),
    ("What should you NOT do for a snake bite?",
     ["Keep the person still", "Go to hospital", "Cut and suck the wound", "Note the time"], 2),
]

CONTACTS = [
    ("🚨 National Emergency", "112"),
    ("🚑 Ambulance (Emergency)", "108"),
    ("🏥 Ambulance (Patient Transport)", "102"),
    ("🚓 Police", "100"),
    ("🚒 Fire", "101"),
    ("👶 Child Helpline", "1098"),
    ("💊 Health Helpline", "104"),
]

TIPS = [
    "Keep a first-aid kit at home, in your car and at work.",
    "Learn CPR: it can double or triple survival from cardiac arrest.",
    "Stay calm: a calm helper makes better decisions.",
    "Check the scene is safe before helping anyone.",
    "Drink water regularly, especially during hot weather.",
]

SEVERITY_BADGE = {"Low": "🟢 Low", "Moderate": "🟡 Moderate", "High": "🟠 High", "Critical": "🔴 Critical"}

# ----------------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------------
with st.sidebar:
    st.title("🩺 CarePulse")
    st.caption("Primary Treatment Guide")
    st.divider()
    page = st.radio(
        "Navigate",
        ["🏠 Home", "📖 First Aid Guide", "🔍 Symptom Checker",
         "📊 Health Tools", "🧠 First Aid Quiz", "📞 Emergency Contacts", "ℹ️ About"],
        label_visibility="collapsed",
    )
    st.divider()
    st.error("In an emergency call **112** or **108** first.")


def disclaimer():
    st.caption("⚠️ CarePulse gives general first-aid information only. It is not a substitute for professional medical advice, diagnosis or treatment.")


def guide_card(name, data):
    with st.container(border=True):
        st.subheader(f"{data['icon']} {name}")
        c1, c2 = st.columns(2)
        c1.markdown(f"**Category:** {data['category']}")
        c2.markdown(f"**Severity:** {SEVERITY_BADGE[data['severity']]}")
        st.markdown("#### ✅ What to do")
        for i, s in enumerate(data["steps"], 1):
            st.markdown(f"**{i}.** {s}")
        st.markdown("#### ❌ What NOT to do")
        for d in data["dont"]:
            st.markdown(f"- {d}")
        st.warning(f"🚑 **When to get emergency help:** {data['emergency']}")


# ----------------------------------------------------------------------------
# PAGES
# ----------------------------------------------------------------------------
if page == "🏠 Home":
    st.title("🩺 CarePulse")
    st.header("Your Primary Treatment Guide")
    st.markdown("Quick, clear and reliable first-aid help — **when every second counts.**")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("First-Aid Guides", len(FIRST_AID))
    m2.metric("Symptoms Covered", len(SYMPTOMS))
    m3.metric("Quiz Questions", len(QUIZ))
    m4.metric("Emergency No.", "112")

    st.divider()
    st.subheader("⚡ Quick Access")
    cols = st.columns(4)
    quick = ["CPR (Adult)", "Burns", "Choking (Adult)", "Severe Bleeding / Cuts"]
    for col, name in zip(cols, quick):
        with col.container(border=True):
            st.markdown(f"### {FIRST_AID[name]['icon']}")
            st.markdown(f"**{name}**")
            st.caption(f"Severity: {FIRST_AID[name]['severity']}")

    st.divider()
    left, right = st.columns([2, 1])
    with left:
        st.subheader("🌟 Why CarePulse?")
        st.markdown(
            "- 📖 Step-by-step first-aid instructions\n"
            "- 🔍 Simple symptom guidance\n"
            "- 📊 BMI and hydration tools\n"
            "- 🧠 Quiz to test your knowledge\n"
            "- 📞 Important emergency numbers"
        )
    with right:
        st.subheader("💡 Tip of the Day")
        if "tip" not in st.session_state:
            st.session_state.tip = random.choice(TIPS)
        st.info(st.session_state.tip)
        if st.button("New tip 🔄"):
            st.session_state.tip = random.choice(TIPS)
            st.rerun()
    disclaimer()

elif page == "📖 First Aid Guide":
    st.title("📖 First Aid Guide")
    f1, f2 = st.columns([2, 1])
    query = f1.text_input("🔎 Search a condition", placeholder="e.g. burn, bleeding, snake")
    cats = ["All"] + sorted({d["category"] for d in FIRST_AID.values()})
    cat = f2.selectbox("Category", cats)

    results = {
        n: d for n, d in FIRST_AID.items()
        if (cat == "All" or d["category"] == cat) and query.lower() in n.lower()
    }
    st.caption(f"Showing {len(results)} guide(s)")
    if not results:
        st.info("No matching guide found. Try another keyword.")
    for name, data in results.items():
        with st.expander(f"{data['icon']}  {name}   —   {SEVERITY_BADGE[data['severity']]}"):
            guide_card(name, data)
    disclaimer()

elif page == "🔍 Symptom Checker":
    st.title("🔍 Symptom Checker")
    st.markdown("Select what you are experiencing to get **general guidance** (not a diagnosis).")
    chosen = st.multiselect("Symptoms", list(SYMPTOMS.keys()))
    if st.button("Get Guidance", type="primary"):
        if not chosen:
            st.warning("Please select at least one symptom.")
        else:
            urgent = [s for s in chosen if SYMPTOMS[s][2]]
            if urgent:
                st.error("🚨 **Possible emergency — call 112 / 108 now.**")
            for s in chosen:
                icon, advice, is_urgent = SYMPTOMS[s]
                with st.container(border=True):
                    (st.error if is_urgent else st.success)(f"{icon} **{s}** — {advice}")
            if len(chosen) >= 3 and not urgent:
                st.warning("Multiple symptoms together: consider seeing a doctor.")
    disclaimer()

elif page == "📊 Health Tools":
    st.title("📊 Health Tools")
    tab1, tab2, tab3 = st.tabs(["⚖️ BMI Calculator", "💧 Water Intake", "❤️ Heart Rate Zones"])

    with tab1:
        c1, c2 = st.columns(2)
        weight = c1.number_input("Weight (kg)", 10.0, 250.0, 65.0, 0.5)
        height = c2.number_input("Height (cm)", 80.0, 250.0, 170.0, 0.5)
        bmi = weight / ((height / 100) ** 2)
        if bmi < 18.5:
            label, fn = "Underweight", st.warning
        elif bmi < 25:
            label, fn = "Normal weight", st.success
        elif bmi < 30:
            label, fn = "Overweight", st.warning
        else:
            label, fn = "Obese", st.error
        st.metric("Your BMI", f"{bmi:.1f}")
        st.progress(min(bmi / 40, 1.0))
        fn(f"Category: **{label}** (healthy range 18.5 – 24.9)")

    with tab2:
        w = st.slider("Your weight (kg)", 20, 150, 65, key="water_w")
        active = st.checkbox("I exercise / live in a hot climate")
        litres = w * 0.033 + (0.5 if active else 0)
        st.metric("Suggested daily water", f"{litres:.1f} L", f"≈ {int(litres * 1000 / 250)} glasses")
        st.caption("A general estimate. Needs vary by person.")

    with tab3:
        age = st.slider("Age", 10, 90, 20)
        max_hr = 220 - age
        st.metric("Estimated Max Heart Rate", f"{max_hr} bpm")
        zones = {
            "Light (50–60%)": (0.5, 0.6),
            "Moderate (60–70%)": (0.6, 0.7),
            "Vigorous (70–85%)": (0.7, 0.85),
        }
        for z, (lo, hi) in zones.items():
            st.write(f"**{z}:** {int(max_hr * lo)} – {int(max_hr * hi)} bpm")
    disclaimer()

elif page == "🧠 First Aid Quiz":
    st.title("🧠 First Aid Quiz")
    st.markdown("Test your first-aid knowledge!")
    with st.form("quiz"):
        answers = []
        for i, (q, opts, _) in enumerate(QUIZ):
            answers.append(st.radio(f"**Q{i + 1}. {q}**", opts, index=None, key=f"q{i}"))
        submitted = st.form_submit_button("Submit Quiz", type="primary")
    if submitted:
        if any(a is None for a in answers):
            st.warning("Please answer all questions.")
        else:
            score = sum(QUIZ[i][1].index(a) == QUIZ[i][2] for i, a in enumerate(answers))
            st.metric("Your Score", f"{score} / {len(QUIZ)}")
            st.progress(score / len(QUIZ))
            if score == len(QUIZ):
                st.balloons()
                st.success("🏆 Perfect! You're a first-aid champion.")
            elif score >= 3:
                st.info("👍 Good job! Review the guides to improve further.")
            else:
                st.warning("📚 Keep learning — check the First Aid Guide and retry.")
            with st.expander("See correct answers"):
                for i, (q, opts, correct) in enumerate(QUIZ):
                    st.markdown(f"**Q{i + 1}.** {q}  \n✅ {opts[correct]}")

elif page == "📞 Emergency Contacts":
    st.title("📞 Emergency Contacts (India)")
    cols = st.columns(2)
    for i, (name, num) in enumerate(CONTACTS):
        with cols[i % 2].container(border=True):
            st.markdown(f"### {name}")
            st.markdown(f"## {num}")
    st.divider()
    st.subheader("🧰 Basic First-Aid Kit Checklist")
    items = ["Sterile gauze & bandages", "Adhesive plasters", "Antiseptic solution", "Scissors & tweezers",
             "Disposable gloves", "Digital thermometer", "ORS packets", "Cold pack", "Pain reliever (as advised)"]
    c = st.columns(3)
    for i, it in enumerate(items):
        c[i % 3].checkbox(it, key=f"kit{i}")

else:
    st.title("ℹ️ About CarePulse")
    st.markdown(
        "**CarePulse – Primary Treatment Guide** is an engineering project that provides "
        "quick first-aid knowledge to everyone, built entirely in **Python** using **Streamlit**."
    )
    st.subheader("🛠️ Tech Stack")
    st.markdown("- Python 3\n- Streamlit (UI & navigation)\n- Session state (quiz & tips)")
    st.subheader("✨ Features")
    st.markdown(
        "- Searchable first-aid guide with do's, don'ts and emergency triggers\n"
        "- Symptom checker with urgency alerts\n"
        "- BMI, hydration and heart-rate tools\n"
        "- Interactive quiz with scoring\n"
        "- Emergency contacts and kit checklist"
    )
    st.subheader("🔮 Future Scope")
    st.markdown("- Multi-language support (Hindi, Marathi)\n- Nearby hospital finder\n- AI chatbot assistant")
    disclaimer()
