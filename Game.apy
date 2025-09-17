import streamlit as st
import pandas as pd

# --- Game Setup ---
st.set_page_config(page_title="House Refurbishment Game", page_icon="🏠", layout="centered")

# --- Data ---
materials = pd.DataFrame({
    "Material": ["Paint (per 10L)", "Tiles (per m²)", "Wood (per m²)", "Wiring (per m)", "Pipes (per m)"],
    "Cost (£)": [35, 20, 25, 15, 12]
})

manpower = pd.DataFrame({
    "Role": ["Builder", "Electrician", "Plumber", "Painter", "Tiler"],
    "Rate (£/hr)": [25, 40, 38, 22, 28]
})

tasks = [
    {"task": "Painting Living Room", "base_hours": 16},
    {"task": "Tiling Bathroom", "base_hours": 20},
    {"task": "Fitting Kitchen", "base_hours": 40},
    {"task": "Electrical Work", "base_hours": 30},
    {"task": "Plumbing Work", "base_hours": 25}
]

budget_limit = 90000
time_limit = 10 * 5 * 8  # 10 weeks * 5 days * 8 hours = 400 hours

# --- Persistent state ---
if "level" not in st.session_state:
    st.session_state.level = 1
if "plan" not in st.session_state:
    st.session_state.plan = []

# --- Levels ---
if st.session_state.level == 1:
    st.title("🏠 House Refurbishment Planning Challenge")
    st.header("Level 1 – Project Briefing")
    st.write("Welcome! You are the project manager for a **house refurbishment project**.")
    st.write(f"- Budget available: **£{budget_limit}**")
    st.write(f"- Deadline: **10 weeks (~400 working hours)**")
    st.write("Your job is to **plan resources, costs, and timeline**.")
    if st.button("Start the Game"):
        st.session_state.level = 2
        st.rerun()

elif st.session_state.level == 2:
    st.header("Level 2 – Resource Planning")
    st.write("📦 **Materials available:**")
    st.table(materials)
    st.write("👷 **Manpower options:**")
    st.table(manpower)
    if st.button("Next: Timeline Planning"):
        st.session_state.level = 3
        st.rerun()

elif st.session_state.level == 3:
    st.header("Level 3 – Timeline & Cost Planning")
    st.write("Assign workers and estimate time for each task.")

    total_cost = 0
    total_hours = 0
    plan = []

    for t in tasks:
        st.subheader(t["task"])
        worker = st.selectbox(
            f"Choose a worker for {t['task']}", manpower["Role"], key=f"{t['task']}_worker"
        )
        hours = st.number_input(
            f"Estimated hours (base {t['base_hours']}h)", min_value=1, value=t["base_hours"], step=1, key=f"{t['task']}_hours"
        )
        rate = manpower.loc[manpower["Role"] == worker, "Rate (£/hr)"].values[0]
        cost = hours * rate
        st.write(f"💰 Cost for {t['task']}: **£{cost}**")
        total_cost += cost
        total_hours += hours
        plan.append({"task": t["task"], "worker": worker, "hours": hours, "cost": cost})

    st.session_state.plan = plan
    st.write("---")
    st.write(f"📊 **Total Estimated Cost:** £{total_cost}")
    st.write(f"⏳ **Total Estimated Time:** {total_hours} hours (~{total_hours/40:.1f} weeks)")

    if st.button("Next: Budget Check"):
        st.session_state.total_cost = total_cost
        st.session_state.total_hours = total_hours
        st.session_state.level = 4
        st.rerun()

elif st.session_state.level == 4:
    st.header("Level 4 – Budget Check")
    cost = st.session_state.total_cost
    hours = st.session_state.total_hours

    if cost > budget_limit or hours > time_limit:
        st.error("⚠️ Your plan is NOT feasible. You exceeded budget or time.")
        if st.button("Revise Plan"):
            st.session_state.level = 3
            st.rerun()
    else:
        st.success("✅ Great job! Your plan fits within budget and deadline.")
        if st.button("Next: Reflection"):
            st.session_state.level = 5
            st.rerun()

elif st.session_state.level == 5:
    st.header("Level 5 – Reflection & Debrief")
    st.write("🎉 You completed the refurbishment planning challenge!")
    st.write("Now reflect on your decisions:")
    st.text_area("What trade-offs did you face between cost and time?")
    st.text_area("If you had more budget, what improvements would you make?")
    st.balloons()
    if st.button("Restart Game"):
        st.session_state.level = 1
        st.rerun()
