import matplotlib.pyplot as plt
import numpy as np
import re

# Function to parse the normal form statements
def parse_normal_form(statement):
    """Parses a normal form statement into axis bounds."""
    # Regular expression to extract variable names and their bounds
    pattern = r"(\d*\.?\d+)\s*<=\s*(\w+)\s*<=\s*(\d*\.?\d+)"
    matches = re.findall(pattern, statement)

    # Dictionary to store bounds for each variable
    bounds = {}
    for match in matches:
        lower, var, upper = match
        lower, upper = float(lower), float(upper)
        # Normalize variable names to handle case variations
        var = var.lower()
        if var not in bounds:
            bounds[var] = []
        bounds[var].append((lower, upper))

    # Handle OR statements (v)
    or_pattern = r"\[(.*?)\]"
    or_matches = re.findall(or_pattern, statement)
    for or_match in or_matches:
        # Split OR statement by 'v' and parse each part
        or_parts = or_match.split('v')
        for part in or_parts:
            sub_matches = re.findall(pattern, part)
            for sub_match in sub_matches:
                lower, var, upper = sub_match
                lower, upper = float(lower), float(upper)
                var = var.lower()
                if var not in bounds:
                    bounds[var] = []
                bounds[var].append((lower, upper))

    return bounds

# Function to visualize the hyperblocks in parallel coordinates
def visualize_hyperblocks(bounds):
    """Visualizes the hyperblocks as polylines in parallel coordinates."""
    # Get unique variables (case-insensitive)
    variables = sorted(list(set(var.lower() for var in bounds.keys())))
    num_axes = len(variables)

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot all intervals for each variable
    for i, var in enumerate(variables):
        intervals = bounds[var]
        for lower, upper in intervals:
            ax.plot([i, i], [lower, upper], color="blue", linewidth=2)

    # Connect intervals between adjacent axes
    for i in range(num_axes - 1):
        var1 = variables[i]
        var2 = variables[i + 1]
        for l1, u1 in bounds[var1]:
            for l2, u2 in bounds[var2]:
                ax.plot([i, i + 1], [u1, u2], color="blue", linewidth=1, linestyle="--")
                ax.plot([i, i + 1], [l1, l2], color="blue", linewidth=1, linestyle="--")

    # Set axis labels
    ax.set_xticks(range(num_axes))
    ax.set_xticklabels(variables)
    ax.set_xlim(-0.5, num_axes - 0.5)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Attributes")
    ax.set_ylabel("Values")
    ax.set_title("Hyperblocks in Parallel Coordinates")

    plt.show()

# Main program
def main():
    # Read the normal form statements from a file
    filename = "statements.txt"
    try:
        with open(filename, "r") as file:
            statements = file.readlines()
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return

    # Process each statement and visualize
    for statement in statements:
        statement = statement.strip()
        print(f"Parsing statement: {statement}")
        bounds = parse_normal_form(statement)
        visualize_hyperblocks(bounds)

if __name__ == "__main__":
    main()