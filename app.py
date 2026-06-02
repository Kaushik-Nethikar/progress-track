import streamlit as st
from datetime import datetime

from utils.calendar_ui import (
    month_grid,
    build_entry_lookup,
    get_day_info
)

from utils.database import (
    get_person_entries,
    get_entry,
    save_entry
)

from utils.stats import (
    calculate_current_streak,
    calculate_best_streak,
    calculate_success_rate
)

PERSON_1 = "Kaushik"
PERSON_2 = "Kiran"

st.markdown("""
<style>

.block-container {
    max-width: 95%;
    padding-top: 1rem;
}            

.stApp {
    background-color: #0F172A;
}

.calendar-card {
    border-radius: 12px;
    padding: 6px;
    text-align: center;
    color: white;
    font-weight: bold;
    min-height: 65px;
    margin-bottom: 6px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.25);
}

.day-number {
    font-size: 15px;
}

.day-status {
    font-size: 18px;
}

.day-note {
    font-size: 18px;
}

.legend-box {
    background: #1E293B;
    padding: 12px;
    border-radius: 12px;
    color: white;
    margin-bottom: 20px;
}

.stButton button {
    width: 100%;
    border-radius: 10px;
}
            
</style>
""", unsafe_allow_html=True)

def render_stats(person, entries):

    current = calculate_current_streak(
        entries
    )

    best = calculate_best_streak(
        entries
    )

    success = calculate_success_rate(
        entries
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "🔥 Current",
        f"{current}"
    )

    c2.metric(
        "🏆 Best",
        f"{best}"
    )

    c3.metric(
        "📈 Success %",
        f"{success}%"
    )

def render_calendar(
    person,
    year,
    month,
    entries
):

    lookup = build_entry_lookup(
        entries
    )

    weeks = month_grid(
        year,
        month
    )

    weekdays = [
        "Sun",
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat"
    ]

    cols = st.columns(
    7,
    gap="small"
    )

    for i, day in enumerate(weekdays):

        cols[i].markdown(
            f"**{day}**"
        )

    for week in weeks:

        cols = st.columns(
        7,
        gap="small"
    )

        for i, day in enumerate(week):

            if day == 0:

                cols[i].empty()

                continue

            info = get_day_info(
                lookup,
                year,
                month,
                day
            )

            note_icon = (
                "📝"
                if info["note"]
                else ""
            )

            cols[i].markdown(
    f"""
    <div style="
        background:{info['color']};
        border-radius:12px;
        padding: 8px;
        min-height: 90px;
        text-align:center;
        color:white;
        font-weight:bold;
    ">
        <div style="
        font-size:14px;
        margin-bottom:5px;
        ">
        {day}
        </div>
        <div>{info['emoji']}</div>
        <div>{note_icon}</div>
    </div>
    """,
    unsafe_allow_html=True
)
            if cols[i].button(
            "✏️",
            key=f"{person}-{year}-{month}-{day}",
            use_container_width=True
            ):
                st.session_state[
                f"selected_{person}"
                ] = day

from datetime import date

def render_editor(person, year, month):

    selected_key = f"selected_{person}"

    if selected_key not in st.session_state:
        return

    day = st.session_state[selected_key]

    selected_date = date(
        year,
        month,
        day
    )

    existing = get_entry(
        person,
        selected_date
    )

    st.divider()

    st.subheader(
        f"📅 {selected_date.strftime('%d %B %Y')}"
    )

    status_options = [
        "excellent",
        "good",
        "average",
        "bad"
    ]

    default_status = "good"
    default_note = ""

    if existing:

        default_status = existing["status"]

        default_note = (
            existing["note"]
            if existing["note"]
            else ""
        )

    status = st.selectbox(
    "Status",
    status_options,
    index=status_options.index(default_status)
    )

    note = st.text_area(
    "Note",
    value=default_note,
    height=120
    )

    if st.button(
    "💾 Save",
    key=f"save_{person}_{day}"
    ):

        save_entry(
            person,
            selected_date,
            status,
            note
        )

        del st.session_state[
            f"selected_{person}"
        ]

        st.rerun()

def render_person_section(
    person,
    year,
    month
):

    entries = get_person_entries(
        person
    )

    st.markdown(
        f"## 👤 {person}"
    )

    render_stats(
        person,
        entries
    )

    render_calendar(
        person,
        year,
        month,
        entries
    )

    render_editor(
        person,
        year,
        month
    )

today = datetime.today()

if "month" not in st.session_state:
    st.session_state.month = today.month

if "year" not in st.session_state:
    st.session_state.year = today.year


st.title("🔥 Progress Arena")

col1, col2, col3 = st.columns([1,3,1])

with col1:
    if st.button("⬅ Previous"):

        if st.session_state.month == 1:
            st.session_state.month = 12
            st.session_state.year -= 1
        else:
            st.session_state.month -= 1

with col3:
    if st.button("Next ➡"):

        if st.session_state.month == 12:
            st.session_state.month = 1
            st.session_state.year += 1
        else:
            st.session_state.month += 1

st.markdown(
    f"""
    <h2 style="
        color:white;
        text-align:center;
    ">
        {datetime(
    st.session_state.year,
    st.session_state.month,
    1
).strftime("%B %Y")}
    </h2>
    """,
    unsafe_allow_html=True
)

left, right = st.columns(
    [1, 1],
    gap="large"
)

with left:

    render_person_section(
        PERSON_1,
        st.session_state.year,
        st.session_state.month
    )

with right:

    render_person_section(
        PERSON_2,
        st.session_state.year,
        st.session_state.month
    )

st.markdown("""
<div class="legend-box">

🔥 Excellent &nbsp;&nbsp;
✅ Good &nbsp;&nbsp;
➖ Average &nbsp;&nbsp;
❌ Bad &nbsp;&nbsp;
📝 Note Available

</div>
""", unsafe_allow_html=True)
