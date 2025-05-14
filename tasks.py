from crewai import Task

def create_tasks(user_inputs, planner, writer, editor, yoga_exercise_coach, regional_customizer, reporter):
    """Create all tasks for the nutrition planning system."""
    
    plan = Task(
        description=(
            f"Using the user's details:\n"
            f"- Age: {user_inputs['age']}\n"
            f"- Country: {user_inputs['country']}\n"
            f"- State: {user_inputs['state']}\n"
            f"- Health Goal: {user_inputs['health_goal']}\n"
            f"- Disease: {user_inputs['disease']}\n"
            f"- Dietary Preferences: {user_inputs['preferences']}\n"
            f"- Allergies: {user_inputs['allergies']}\n"
            f"- Fitness Routine: {user_inputs['fitness_routine']}\n\n"
            "Create a nutrition plan outline with the following format:\n\n"
            "### Nutrition Plan Outline\n"
            "1. Number of Meals per Day: ...\n"
            "2. Food Groups to Include: ...\n"
            "3. Foods to Avoid: ...\n"
            "4. Caloric & Macronutrient Targets: ...\n"
            "5. Meal Timing Recommendations: ...\n"
            "6. Food Swap Suggestions: ...\n"
        ),
        expected_output="A structured markdown-style Nutrition Plan Outline.",
        agent=planner
    )

    write = Task(
        description=(
            "Using the provided Nutrition Plan Outline, generate a **28-Day Meal Plan** in the following format:\n\n"
            "### 28-Day Meal Plan\n"
            "**Day 1:**\n"
            "- Breakfast: [Item] | [Portion] | [Calories]\n"
            "- Lunch: [Item] | [Portion] | [Calories]\n"
            "- Snack: ...\n"
            "- Dinner: ...\n\n"
            "Repeat for all 28 days ensuring variety, allergies, and goal alignment."
        ),
        expected_output="A cleanly formatted, day-wise meal plan in markdown style.",
        agent=writer
    )

    edit = Task(
        description=(
            "Review the generated 28-Day Meal Plan and create a structured analysis with:\n\n"
            "### Nutrition Analysis\n"
            "1. Balance Review:\n"
            "- Carb/Protein/Fat distribution\n"
            "- Micronutrient coverage\n"
            "- Cultural adaptability\n\n"
            "2. Reasoning Behind Major Choices:\n"
            "- Example: Why oats in breakfast?\n\n"
            "3. Improvement Suggestions:\n"
            "- Suggest 2-3 smart adjustments."
        ),
        expected_output="A structured markdown-style Nutrition Analysis.",
        agent=editor
    )

    exercise = Task(
        description=(
            f"Create a personalized 7-day exercise and yoga plan for the user considering:\n"
            f"- Current fitness routine: {user_inputs['fitness_routine']}\n"
            f"- Health goal: {user_inputs['health_goal']}\n"
            f"- Medical conditions: {user_inputs['disease']}\n\n"
            "Include:\n"
            "1. Daily workout schedule\n"
            "2. Yoga poses and breathing exercises\n"
            "3. Duration and intensity recommendations\n"
            "4. Modifications for different fitness levels"
        ),
        expected_output="A structured 7-day exercise and yoga plan in markdown format.",
        agent=yoga_exercise_coach
    )

    regional = Task(
        description=(
            f"Customize the meal plan for {user_inputs['state']}, {user_inputs['country']} by:\n"
            "1. Suggesting local ingredient substitutes\n"
            "2. Adding regional recipe variations\n"
            "3. Considering seasonal availability\n"
            "4. Incorporating cultural preferences\n"
            "5. Recommending local food sources"
        ),
        expected_output="A list of regional customizations and alternatives in markdown format.",
        agent=regional_customizer
    )

    report = Task(
        description=(
            "Compile all outputs into a **Final Nutrition Report** in this format:\n\n"
            "# Final Nutrition Report\n"
            "## User Details\n"
            "- Age, Country, State, etc.\n\n"
            "## Nutrition Plan Outline\n"
            "[From Task 1]\n\n"
            "## 28-Day Meal Plan\n"
            "[From Task 2]\n\n"
            "## Nutrition Analysis\n"
            "[From Task 3]\n\n"
            "## Exercise & Yoga Plan\n"
            "[From Task 4]\n\n"
            "## Regional Customizations\n"
            "[From Task 5]\n\n"
            "## Final Remarks\n"
            "- Summary advice and motivation."
        ),
        expected_output="A comprehensive Final Nutrition Report in markdown format.",
        agent=reporter
    )

    return [plan, write, edit, exercise, regional, report]
