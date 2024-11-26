import pandas as pd
import random

def optimize_materials(weights):
    """
    Optimize materials based on the provided weights.

    Args:
        weights (dict): A dictionary of property weights.

    Returns:
        pd.DataFrame: A DataFrame containing the optimized material composition.
    """
    materials = ["Carbon Fibers", "Epoxy Resin", "Glass Fiber", "Silicon Carbide", "Aluminum"]
    scores = [random.uniform(0.1, 1.0) * sum(weights.values()) for _ in materials]
    percentages = [score / sum(scores) * 100 for score in scores]

    return pd.DataFrame({
        "Component": materials,
        "Weighted Score": scores,
        "Percentage (%)": percentages,
    })


def parse_composition(dataframe):
    """
    Parse the composition of materials into components and percentages.

    Args:
        dataframe (pd.DataFrame): The material composition DataFrame.

    Returns:
        tuple: Two lists - components and percentages.
    """
    components = dataframe["Component"].tolist()
    percentages = dataframe["Percentage (%)"].tolist()
    return components, percentages
