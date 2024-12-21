import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import re

# Function to parse a single normal form statement
def parse_single_statement(statement):
    """Parses a single normal form statement into axis bounds."""
    pattern = r"(\d*\.?\d+)\s*<=\s*(\w+)\s*<=\s*(\d*\.?\d+)"
    matches = re.findall(pattern, statement)

    bounds = {}
    for match in matches:
        lower, var, upper = match
        lower, upper = float(lower), float(upper)
        var = var.lower()
        if var not in bounds:
            bounds[var] = []
        bounds[var].append((lower, upper))
    return bounds

# Function to parse combined statements (e.g., HB1 + HB2)
def parse_normal_form(statement):
    """Parses combined statements into a list of bounds for each hyperblock."""
    # Split by '+' operator to handle combined hyperblocks
    parts = statement.split('+')
    hyperblocks = []

    for part in parts:
        part = part.strip()
        bounds = parse_single_statement(part)
        hyperblocks.append(bounds)

    return hyperblocks

# Function to visualize the hyperblocks in parallel coordinates
def visualize_hyperblocks(hyperblocks):
    """Visualizes the hyperblocks as polylines in parallel coordinates."""
    # Collect all unique variables
    all_variables = set()
    for bounds in hyperblocks:
        all_variables.update(bounds.keys())
    variables = sorted(all_variables)
    num_axes = len(variables)

    # Generate unique colors for each hyperblock
    colors = list(mcolors.TABLEAU_COLORS.values())

    fig, ax = plt.subplots(figsize=(10, 6))

    for hb_idx, bounds in enumerate(hyperblocks):
        color = colors[hb_idx % len(colors)]  # Cycle through colors if there are many HBs
        for i, var in enumerate(variables):
            if var in bounds:
                intervals = bounds[var]
                for lower, upper in intervals:
                    ax.plot([i, i], [lower, upper], color=color, linewidth=2)

        # Connect intervals between adjacent axes
        for i in range(num_axes - 1):
            var1 = variables[i]
            var2 = variables[i + 1]
            if var1 in bounds and var2 in bounds:
                for l1, u1 in bounds[var1]:
                    for l2, u2 in bounds[var2]:
                        ax.plot([i, i + 1], [u1, u2], color=color, linewidth=1, linestyle="--")
                        ax.plot([i, i + 1], [l1, l2], color=color, linewidth=1, linestyle="--")

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
        hyperblocks = parse_normal_form(statement)
        visualize_hyperblocks(hyperblocks)

if __name__ == "__main__":
    main()
