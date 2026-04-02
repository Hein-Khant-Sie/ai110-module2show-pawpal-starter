import streamlit as st
from pawpal_system import CareTask, Pet, PetOwner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

PRIORITY_MAP = {"low": 2, "medium": 3, "high": 5}

# --- Persist PetOwner across reruns ---
if "owner" not in st.session_state:
    st.session_state.owner = PetOwner(name="Jordan", available_minutes=120)

# --- Owner Info ---
st.subheader("Owner Info")
col1, col2 = st.columns(2)
with col1:
    st.session_state.owner.name = st.text_input("Owner name", value=st.session_state.owner.name)
with col2:
    st.session_state.owner.available_minutes = st.number_input(
        "Available time (minutes)", min_value=10, max_value=480, value=st.session_state.owner.available_minutes
    )

owner_name = st.session_state.owner.name
available_minutes = st.session_state.owner.available_minutes

# --- Add Pet Form ---
st.subheader("Add a New Pet")

with st.form("add_pet_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        pet_name = st.text_input("Pet name", value="Mochi")
    with col2:
        species = st.selectbox("Species", ["dog", "cat", "other"])
    with col3:
        pet_age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)

    pet_submitted = st.form_submit_button("Add Pet")

if pet_submitted:
    new_pet = Pet(name=pet_name, species=species, age=int(pet_age))
    st.session_state.owner.add_pet(new_pet)
    st.success(f"Added {new_pet.name} the {new_pet.species}!")

# --- Current Pet List ---
st.subheader("Your Pets")
if st.session_state.owner.pets:
    for pet in st.session_state.owner.pets:
        st.write(f"- **{pet.name}** ({pet.species}, age {pet.age})")
else:
    st.info("No pets added yet. Use the form above!")

st.divider()

# --- Task Entry ---
st.subheader("Tasks")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

with st.form("add_task_form", clear_on_submit=True):
    pet_options = [pet.name for pet in st.session_state.owner.pets]
    assigned_pet = st.selectbox(
        "Assign to pet",
        options=pet_options if pet_options else ["(add a pet first)"],
        disabled=not pet_options,
    )
    col1, col2 = st.columns(2)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
        description = st.text_input("Description", value="Walk in the park")
        category = st.selectbox(
            "Category",
            ["feeding", "exercise", "grooming", "cleaning", "enrichment", "other"],
        )
    with col2:
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        must_do = st.checkbox("Must do today", value=True)

    if st.form_submit_button("Add task"):
        if pet_options:
            st.session_state.tasks.append(
                {
                    "title": task_title,
                    "description": description,
                    "duration_minutes": int(duration),
                    "priority": priority,
                    "must_do": must_do,
                    "category": category,
                    "pet_name": assigned_pet,
                }
            )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "Pet": t["pet_name"],
                "Task": t["title"],
                "Duration (min)": t["duration_minutes"],
                "Priority": t["priority"],
                "Must Do": "Yes" if t["must_do"] else "No",
                "Category": t["category"],
            }
            for t in st.session_state.tasks
        ]
    )
    if st.button("Clear all tasks"):
        st.session_state.tasks = []
        st.rerun()
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Generate Schedule ---
st.subheader("Generate Schedule")

if st.button("Generate schedule", type="primary"):
    if not st.session_state.owner.pets:
        st.warning("Please add at least one pet first.")
    elif not st.session_state.tasks:
        st.warning("Please add at least one task first.")
    else:
        owner = st.session_state.owner
        for pet in owner.pets:
            pet.tasks = []  # clear old tasks before re-adding
            for t in st.session_state.tasks:
                if t["pet_name"] == pet.name:  # only add tasks assigned to this pet
                    pet.add_task(
                        CareTask(
                            name=t["title"],
                            description=t["description"],
                            duration=t["duration_minutes"],
                            frequency="daily",
                            priority=PRIORITY_MAP[t["priority"]],
                            must_do=t["must_do"],
                            category=t["category"],
                        )
                    )

        plan = Scheduler().generate_plan(owner, owner.get_incomplete_tasks())

        pet_names = ", ".join(p.name for p in owner.pets)
        st.success(f"Schedule generated for {owner_name} and {pet_names}!")

        c1, c2, c3 = st.columns(3)
        c1.metric("Tasks Scheduled", len(plan.selected_tasks))
        c2.metric("Tasks Skipped", len(plan.skipped_tasks))
        c3.metric("Time Used", f"{plan.total_time}/{int(available_minutes)} min")

        if plan.selected_tasks:
            st.markdown("### Today's Tasks")
            for i, task in enumerate(plan.selected_tasks, 1):
                with st.expander(f"{i}. {task.name} — {task.duration} min"):
                    st.write(f"**Description:** {task.description}")
                    st.write(f"**Category:** {task.category}")
                    st.write(f"**Priority:** {task.priority}/5")
                    st.write(f"**Must do:** {'Yes' if task.must_do else 'No'}")

        if plan.skipped_tasks:
            st.markdown("### Skipped Tasks")
            for task in plan.skipped_tasks:
                st.write(f"- {task.name} ({task.duration} min)")

        st.markdown("### Scheduling Reasoning")
        for reason in plan.reasoning:
            st.write(f"- {reason}")
