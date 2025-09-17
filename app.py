import streamlit as st
import pandas as pd

# --- Setup ---
st.set_page_config(page_title="House Refurbishment Game", page_icon="🏠", layout="wide")

# --- Data ---
materials = pd.DataFrame({
    "Material": ["Paint (per 10L)", "Tiles (per m²)", "Wood (per m²)", "Wiring (per m)", "Pipes (per m)"],
    "Cost (£)": [35, 20, 25, 15, 12]
})

manpower = pd.DataFrame({
    "Role": ["Builder", "Electrician", "Plumber", "Painter", "Tiler"],
    "Rate (£/hr)": [25, 40, 38, 22, 28]
})

tasks = ["Painting Living Room", "Tiling Bathroom", "Fitting Kitchen", "Electrical Work", "Plumbing Work"]

budget_limit = 90000
time_limit = 400  # hours (10 weeks x 5 days x 8 hours)

# --- Game Intro ---
st.title("🏠 House Refurbishment Planning Challenge")
st.write("Welcome! Plan the refurbishment project. Stay within **£90,000 budget** and **10 weeks (400 hours)**.")

# --- Show floor plan ---
st.image("house_plan_coloured_final.png", caption="House / Flat Plan (with dimensions)", use_container_width=True)

# --- Interactive Planning Table ---
st.header("📋 Step 1: Enter Your Estimates")

# Build editable dataframe for planning
df = pd.DataFrame({
    "Task": tasks,
    "Assigned Worker": [manpower["Role"].iloc[0]] * len(tasks),
    "Estimated Hours": [0] * len(tasks)
})

edited_df = st.data_editor(
    df,
    column_config={
        "Assigned Worker": st.column_config.SelectboxColumn(
            "Assigned Worker", options=list(manpower["Role"])
        ),
        "Estimated Hours": st.column_config.NumberColumn("Estimated Hours (h)", min_value=1, step=1)
    },
    hide_index=True
)

# --- Calculations ---
results = []
total_cost = 0
total_hours = 0

for i, row in edited_df.iterrows():
    worker = row["Assigned Worker"]
    hours = row["Estimated Hours"]
    rate = manpower.loc[manpower["Role"] == worker, "Rate (£/hr)"].values[0]
    cost = hours * rate
    results.append([row["Task"], worker, hours, cost])
    total_cost += cost
    total_hours += hours

results_df = pd.DataFrame(results, columns=["Task", "Worker", "Hours", "Cost (£)"])

# --- Show results ---
st.header("📊 Step 2: Results")
st.dataframe(results_df, hide_index=True)

weeks = total_hours / 40  # 40h per week
st.write(f"**Total Cost:** £{total_cost}")
st.write(f"**Total Time:** {total_hours} hours (~{weeks:.1f} weeks)")

# --- Feasibility Check ---
st.header("✅ Step 3: Feasibility Check")
if total_cost > budget_limit or total_hours > time_limit:
    st.error("⚠️ Plan NOT feasible. Over budget or time!")
else:
    st.success("🎉 Plan is feasible! You stayed within budget and time.")

# --- Reflection ---
st.header("📝 Step 4: Reflection")
st.text_area("What challenges did you face balancing cost vs. time?")
st.text_area("If you had more budget, what would you improve?")
