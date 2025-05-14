import os
import streamlit as st
from crewai import Agent, Task, Crew
from agents import create_agents
from tasks import create_tasks
from database_utils import DatabaseManager

def display_agent_output(title, content):
    """Helper function to display agent output in a formatted way"""
    st.subheader(f"🤖 {title}")
    st.markdown(content)
    st.markdown("---")

def main():
    st.title("🍽️ AI-Powered Personalized Nutrition Assistant")
    st.write("Get your customized nutrition and fitness plan powered by AI agents.")

    # Initialize database
    db = DatabaseManager()

    with st.form("user_input_form"):
        st.subheader("👤 Personal Details")
        age = st.text_input("Age")
        country = st.text_input("Country")
        state = st.text_input("State")
        health_goal = st.text_input("Health Goal (e.g., weight loss, muscle gain)")
        disease = st.text_input("Any specific disease (if none, type 'None')")
        preferences = st.text_input("Dietary preferences (e.g., vegan, gluten-free)")
        allergies = st.text_input("Any allergies")
        fitness_routine = st.text_input("Your current fitness routine")
        image_file = st.file_uploader("Upload an image of your food/ingredients (optional)", type=['png', 'jpg', 'jpeg'])

        submitted = st.form_submit_button("Generate Nutrition Plan")

    if submitted:
        user_inputs = {
            "age": age,
            "country": country,
            "state": state,
            "health_goal": health_goal,
            "disease": disease,
            "preferences": preferences,
            "allergies": allergies,
            "fitness_routine": fitness_routine,
            "image_path": ""
        }

        # Save uploaded image temporarily
        if image_file is not None:
            image_path = os.path.join("temp_uploads", image_file.name)
            os.makedirs("temp_uploads", exist_ok=True)
            with open(image_path, "wb") as f:
                f.write(image_file.getbuffer())
            user_inputs["image_path"] = image_path

        # Save user inputs to database
        user_input_id = db.save_user_input(user_inputs)

        # Create agents and tasks
        planner, writer, editor, yoga_exercise_coach, regional_customizer, reporter = create_agents(user_inputs)
        tasks = create_tasks(user_inputs, planner, writer, editor, yoga_exercise_coach, regional_customizer, reporter)

        # Create tabs for different sections
        plan_tab, meal_tab, analysis_tab, exercise_tab, regional_tab, final_tab = st.tabs([
            "Nutrition Plan", "Meal Plan", "Analysis", "Exercise Plan", "Regional", "Final Report"
        ])

        # Run each task individually and display results
        with st.spinner("🤖 Generating your personalized nutrition plan..."):
            # Run planner task
            with plan_tab:
                plan_result = tasks[0].execute()
                display_agent_output("Nutrition Plan Outline", plan_result)
            
            # Run writer task
            with meal_tab:
                meal_result = tasks[1].execute()
                display_agent_output("28-Day Meal Plan", meal_result)
            
            # Run editor task
            with analysis_tab:
                analysis_result = tasks[2].execute()
                display_agent_output("Nutrition Analysis", analysis_result)
            
            # Run yoga/exercise task
            with exercise_tab:
                exercise_result = tasks[3].execute()
                display_agent_output("Exercise & Yoga Plan", exercise_result)
            
            # Run regional customization task
            with regional_tab:
                regional_result = tasks[4].execute()
                display_agent_output("Regional Customizations", regional_result)
            
            # Run final report task
            with final_tab:
                final_result = tasks[5].execute()
                st.subheader("📝 Final Nutrition Report")
                st.markdown(final_result)

            # Save the final report to database
            report_id = db.save_report(user_input_id, final_result)

        # Feedback Section
        st.subheader("💭 We value your feedback!")
        rating = st.slider("Rate your nutrition plan (1-5 stars)", 1, 5, 3)
        comments = st.text_area("Additional comments or suggestions")

        if st.button("Submit Feedback"):
            db.save_feedback(report_id, rating, comments)
            st.success("✨ Thank you for your feedback! Your nutrition plan has been saved.")

if __name__ == "__main__":
    main()
