import os
from crewai import Agent, Task, Crew
from agents import create_agents
from tasks import create_tasks
from database_utils import DatabaseManager

def get_user_inputs():
    """Collect user inputs for the nutrition plan."""
    print("Please provide the following details:")
    
    user_inputs = {
        "age": input("Age: ").strip(),
        "country": input("Country: ").strip(),
        "state": input("State: ").strip(),
        "health_goal": input("Health Goal (e.g., weight loss, muscle gain): ").strip(),
        "disease": input("Any specific disease (if none, type 'None'): ").strip(),
        "preferences": input("Dietary preferences (e.g., vegan, gluten-free): ").strip(),
        "allergies": input("Any allergies: ").strip(),
        "fitness_routine": input("Your current fitness routine: ").strip(),
        "image_path": input("Path to an image of your food/ingredients (if any, else press Enter): ").strip()
    }
    
    # Validate image path if provided
    if user_inputs["image_path"] and not os.path.exists(user_inputs["image_path"]):
        print(f"\n⚠️ Warning: Image file not found at {user_inputs['image_path']}.")
        print("Image analysis will be skipped.")
        user_inputs["image_path"] = ""
    
    return user_inputs

def get_user_feedback():
    """Collect user feedback about the nutrition plan."""
    print("\n📊 Please rate your nutrition plan (1-5 stars):")
    while True:
        try:
            rating = int(input("Rating (1-5): ").strip())
            if 1 <= rating <= 5:
                break
            print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Please enter a valid number.")
    
    comments = input("Any additional comments or suggestions? ").strip()
    return rating, comments

def main():
    try:
        # Initialize database
        db = DatabaseManager()

        # Get user inputs
        user_inputs = get_user_inputs()

        # Save user inputs to database
        user_input_id = db.save_user_input(user_inputs)

        # Create agents with user inputs
        planner, writer, editor, yoga_exercise_coach, regional_customizer, reporter = create_agents(user_inputs)

        # Create tasks with the agents and user inputs
        tasks = create_tasks(user_inputs, planner, writer, editor, yoga_exercise_coach, regional_customizer, reporter)

        # Create and run the crew
        crew = Crew(
            agents=[planner, writer, editor, yoga_exercise_coach, regional_customizer, reporter],
            tasks=tasks,
            verbose=2
        )

        # Get the final result
        result = crew.kickoff()

        # Save the report to database
        report_id = db.save_report(user_input_id, result)

        # Print the final result
        print("\n\n📝 Final Nutrition Report:\n")
        print(result)

        # Get user feedback
        print("\n💭 We value your feedback!")
        rating, comments = get_user_feedback()

        # Save feedback to database
        db.save_feedback(report_id, rating, comments)
        print("\n✨ Thank you for your feedback! Your nutrition plan has been saved.")

    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print("Please check your internet connection and try again.")

if __name__ == "__main__":
    main()
