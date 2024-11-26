import streamlit as st
from dotenv import load_dotenv
import os
from openai import OpenAI
import matplotlib.pyplot as plt

# Load environment variables
load_dotenv()

# Retrieve OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("OpenAI API key not found. Please add it to your `.env` file.")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Streamlit app configuration
st.set_page_config(
    page_title="AI Material Formula Generator",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to generate material formula using OpenAI
@st.cache_data(show_spinner=False)
def generate_material_formula(properties):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a material scientist specializing in advanced material formulas and sustainability."},
                {"role": "user", "content": f"Propose a material formula with the following properties: {properties}"}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

# Function to generate a pie chart for material composition
def create_material_pie_chart(components, percentages):
    try:
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(
            percentages,
            labels=components,
            autopct="%1.1f%%",
            startangle=140,
            colors=["lightblue", "orange", "green", "pink", "purple"]
        )
        ax.set_title("Material Composition Breakdown", fontsize=14)
        return fig
    except Exception as e:
        st.warning(f"Error generating pie chart: {e}")
        return None

# Streamlit UI
st.title("🧪 AI-Powered Material Formula Generator")
st.markdown(
    """
    This tool leverages AI to accelerate material discovery and innovation.
    Use it to explore material formulas tailored to specific properties and applications.
    """
)

# Sidebar for user input
with st.sidebar:
    st.header("Select Desired Properties")
    tensile_strength = st.selectbox("Tensile Strength", ["High", "Medium", "Low"])
    thermal_expansion = st.selectbox("Thermal Expansion", ["Low", "Medium", "High"])
    electrical_resistivity = st.selectbox("Electrical Resistivity", ["Low", "Medium", "High"])
    sustainability_focus = st.checkbox("Consider sustainability metrics")
    properties = (
        f"Tensile strength: {tensile_strength}, "
        f"Thermal expansion: {thermal_expansion}, "
        f"Electrical resistivity: {electrical_resistivity}. "
        f"Focus on sustainability: {sustainability_focus}."
    )

st.markdown(f"### Selected Properties:\n{properties}")

# Generate button
if st.button("Generate Material Formula"):
    with st.spinner("Generating material formula..."):
        result = generate_material_formula(properties)
        if result:
            st.success("Material formula generated successfully!")
            st.markdown("### Proposed Material Formula")
            st.write(result)

            # Dynamically set components and percentages (example based on standard output format)
            components = ["Carbon Fiber", "Epoxy Resin", "Copper Nanoparticles"]
            percentages = [70, 20, 10]  # Adjust based on extracted output or assumed defaults

            # Automatically create and display pie chart
            st.markdown("### Material Composition Diagram")
            pie_chart = create_material_pie_chart(components, percentages)
            if pie_chart:
                st.pyplot(pie_chart)

            # Save the result
            save_option = st.checkbox("Save result to file")
            if save_option:
                try:
                    filename = "material_formula.txt"
                    with open(filename, "w", encoding="utf-8") as file:
                        file.write(f"Desired Properties:\n{properties}\n\n")
                        file.write(f"Proposed Material Formula:\n{result}\n")
                    st.success(f"Result saved successfully to `{filename}`.")
                except Exception as e:
                    st.error(f"Failed to save the result: {e}")

# Footer
st.markdown("---")
st.markdown(
    """
    **Developed by Oluwafemi Idiakhoa**  
    A step forward in combining AI and materials science for sustainable innovation.
    """
)
