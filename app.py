import streamlit as st
import pandas as pd
from data_parsing import parse_composition, optimize_materials
from visualization import plot_material_composition
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("Missing OpenAI API key. Please check your .env configuration.")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Streamlit App Layout
st.title("🧪 AI-Powered Material Formula Generator")
st.write("Objective: Use AI and material science principles to generate optimized material formulas based on key properties like tensile strength, thermal expansion, and electrical resistivity.")

# User Inputs
st.sidebar.header("Material Properties and Comparisons")
tensile_strength = st.sidebar.selectbox("Tensile Strength", ["Low", "Medium", "High"])
thermal_expansion = st.sidebar.selectbox("Thermal Expansion", ["Low", "Medium", "High"])
electrical_resistivity = st.sidebar.selectbox("Electrical Resistivity", ["Low", "Medium", "High"])
sustainability = st.sidebar.checkbox("Consider Sustainability Metrics", value=False)

# Weight Adjustments
st.sidebar.subheader("Weight Adjustments")
weights = {
    "Tensile Strength": st.sidebar.slider("Tensile Strength Weight", 0.0, 1.0, 0.5),
    "Thermal Expansion": st.sidebar.slider("Thermal Expansion Weight", 0.0, 1.0, 0.5),
    "Electrical Resistivity": st.sidebar.slider("Electrical Resistivity Weight", 0.0, 1.0, 0.5),
}

# Generate Formula Button
if st.sidebar.button("Generate Formula"):
    with st.spinner("Processing your request..."):
        try:
            # Material Optimization
            optimized_materials = optimize_materials(weights)
            components, percentages = parse_composition(optimized_materials)

            # Generate Material Explanation using OpenAI
            material_prompt = f"""
            Generate a detailed explanation for a material composition with the following components:
            {', '.join(components)} with respective percentages: {', '.join(map(str, percentages))}.
            The material should meet the criteria of {tensile_strength} tensile strength, 
            {thermal_expansion} thermal expansion, and {electrical_resistivity} electrical resistivity.
            """
            explanation_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": material_prompt}]
            )
            explanation = explanation_response.choices[0].message.content

            # Display Results
            st.subheader("Proposed Material Formula")
            st.dataframe(pd.DataFrame({"Component": components, "Percentage (%)": percentages}))
            st.download_button(
                label="Download Formula as CSV",
                data=pd.DataFrame({"Component": components, "Percentage (%)": percentages}).to_csv(index=False),
                file_name="optimized_materials.csv",
                mime="text/csv",
            )

            # Display Material Explanation
            st.subheader("Material Explanation")
            st.write(explanation)

            # Plot Composition
            st.subheader("Material Composition Diagram")
            plot_material_composition(components, percentages)

        except Exception as e:
            st.error(f"Error generating material formula: {e}")
