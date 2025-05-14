from crewai import Agent
from langchain_groq import ChatGroq

def setup_llm():
    """Setup the language model for all agents."""
    try:
        return ChatGroq(
            temperature=0,
            model_name="llama3-70b-8192",
            api_key='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'
        )
    except Exception as e:
        print(f"\n❌ Error connecting to Groq API: {str(e)}")
        print("Please check your internet connection and API key.")
        raise

def create_agents(user_inputs):
    """Create all the agents needed for the nutrition planning system."""
    llm = setup_llm()

    planner = Agent(
        llm=llm,
        role="Nutrition Planner",
        goal=f"Create a structured nutrition plan outline for a {user_inputs['age']} year old from {user_inputs['state']}, {user_inputs['country']} aiming for {user_inputs['health_goal']}. Consider any disease: {user_inputs['disease']}, dietary preferences: {user_inputs['preferences']}, and allergies: {user_inputs['allergies']}.",
        backstory="You design personalized, section-wise health-based meal outlines by analyzing user inputs and goals.",
        allow_delegation=False,
        verbose=True
    )

    writer = Agent(
        llm=llm,
        role="Meal Plan Generator",
        goal=f"Using the outline, generate a 28-day day-wise table-format meal plan for a {user_inputs['age']} year old from {user_inputs['state']}, {user_inputs['country']}, with {user_inputs['health_goal']} as the target. Respect dietary preferences: {user_inputs['preferences']}, allergies: {user_inputs['allergies']}, and disease: {user_inputs['disease']}. Include meal names, portion sizes, and calories.",
        backstory="You craft balanced, creative, detailed meal plans suitable for diverse needs using structured nutrition outlines.",
        allow_delegation=False,
        verbose=True
    )

    editor = Agent(
        llm=llm,
        role="Nutrition Analyst",
        goal=f"Review the generated meal plan for balance and health alignment for a {user_inputs['age']} year old aiming for {user_inputs['health_goal']}. Check alignment with medical history ({user_inputs['disease']}), dietary preferences ({user_inputs['preferences']}), and allergies ({user_inputs['allergies']}). Provide reasoning, improvements, and highlight nutritional optimizations.",
        backstory="You validate meal plans for nutritional accuracy, contextual reasoning, and suggest actionable optimizations.",
        allow_delegation=False,
        verbose=True
    )

    yoga_exercise_coach = Agent(
        llm=llm,
        role="Yoga & Exercise Suggestion Coach",
        goal=f"Design a personalized 7-day yoga and exercise plan for a {user_inputs['age']} year old from {user_inputs['country']}, targeting {user_inputs['health_goal']}. Base this on their current routine: '{user_inputs['fitness_routine']}', any medical limitations: {user_inputs['disease']}, and fitness preferences.",
        backstory="You are an expert yoga and fitness consultant specializing in aligning wellness routines with personal health goals and limitations.",
        allow_delegation=False,
        verbose=True
    )

    regional_customizer = Agent(
        llm=llm,
        role="Regional Meal Customizer",
        goal=f"Adjust the meal plan and suggest 5 regionally appropriate meal options for {user_inputs['state']}, {user_inputs['country']}, considering dietary preferences: {user_inputs['preferences']} and allergies: {user_inputs['allergies']}. Ensure cultural, seasonal, and locally available ingredients are considered.",
        backstory="You're a culinary specialist with knowledge of regional, culturally sensitive meal adaptations for better adherence and satisfaction.",
        allow_delegation=False,
        verbose=True
    )

    reporter = Agent(
        llm=llm,
        role="Final Report Generator",
        goal=f"Compile all generated outputs into a clean, structured markdown wellness report for a {user_inputs['age']} year old from {user_inputs['state']}, {user_inputs['country']}, targeting {user_inputs['health_goal']}. Include nutrition plan outline, 28-day meal plan, analysis, exercise plan, and regional adjustments.",
        backstory="You specialize in assembling wellness recommendations into well-organized, easy-to-follow reports for clients.",
        allow_delegation=False,
        verbose=True
    )

    return planner, writer, editor, yoga_exercise_coach, regional_customizer, reporter
