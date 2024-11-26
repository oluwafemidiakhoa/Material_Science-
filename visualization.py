import matplotlib.pyplot as plt
import streamlit as st

def plot_material_composition(components, percentages):
    """
    Plot a pie chart for the material composition.

    Args:
        components (list): A list of component names.
        percentages (list): A list of corresponding percentages.
    """
    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax.pie(
        percentages, labels=components, autopct='%1.1f%%', startangle=140
    )
    ax.set_title("Material Composition Breakdown")

    # Set properties of texts and autotexts for better readability
    for text in texts:
        text.set_fontsize(10)
    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_color("white")

    ax.legend(wedges, components, title="Components", loc="center left", bbox_to_anchor=(1, 0.5))
    st.pyplot(fig)
