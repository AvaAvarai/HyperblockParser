import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import re

# Function to parse a single normal form statement
def parse_single_statement(statement):
    """Parses a single normal form statement into axis bounds."""
    # Pattern to match the bounds of a single statement
    pattern = r"(\d*\.?\d+)\s*([<](?:=)?)\s*(\w+)\s*([<](?:=)?)\s*(\d*\.?\d+)"
    matches = re.findall(pattern, statement)

    bounds = {}
    # Track order of variables as they appear
    var_order = []
    for match in matches:
        lower, lower_op, var, upper_op, upper = match
        lower, upper = float(lower), float(upper)
        var = var.lower()
        # Store the operator types along with the bounds
        if var not in bounds:
            bounds[var] = []
            var_order.append(var)
        bounds[var].append((lower, upper, lower_op, upper_op))
    return bounds, var_order

# Function to parse combined statements (e.g., HB1 + HB2)
def parse_normal_form(statement):
    """Parses combined statements into a list of bounds for each hyperblock."""
    # Split by '+' operator to handle combined hyperblocks
    parts = statement.split('+')
    hyperblocks = []
    all_var_orders = []

    for part in parts:
        part = part.strip()
        bounds, var_order = parse_single_statement(part)
        hyperblocks.append(bounds)
        all_var_orders.append(var_order)

    # Combine variable orders while preserving first appearance order
    final_var_order = []
    for order in all_var_orders:
        for var in order:
            if var not in final_var_order:
                final_var_order.append(var)

    return hyperblocks, final_var_order

# Function to visualize the hyperblocks in parallel coordinates
def visualize_hyperblocks(hyperblocks, variables):
    """Visualizes the hyperblocks as parallel coordinates."""
    num_axes = len(variables)

    # Generate unique colors for each hyperblock
    colors = list(mcolors.TABLEAU_COLORS.values())

    # Find global min and max bounds across all variables
    global_min = float('inf')
    global_max = float('-inf')
    for bounds in hyperblocks:
        for var in bounds:
            for lower, upper, _, _ in bounds[var]:
                global_min = min(global_min, lower)
                global_max = max(global_max, upper)

    fig, ax = plt.subplots(figsize=(10, 6))

    for hb_idx, bounds in enumerate(hyperblocks):
        color = colors[hb_idx % len(colors)]
        for i, var in enumerate(variables):
            if var in bounds:
                intervals = bounds[var]
                for lower, upper, lower_op, upper_op in intervals:
                    # Draw main interval line
                    ax.plot([i, i], [lower, upper], color=color, linewidth=2)
                    
                    # Add endpoint markers
                    # 'o' for empty circle, 'C' for filled circle
                    lower_marker = 'o' if '<' in lower_op and '=' not in lower_op else 'o'
                    upper_marker = 'o' if '<' in upper_op and '=' not in upper_op else 'o'
                    
                    # Lower endpoint
                    ax.plot(i, lower, color=color, marker=lower_marker, 
                           fillstyle='none' if '<' in lower_op and '=' not in lower_op else 'full',
                           markersize=10)
                    
                    # Upper endpoint
                    ax.plot(i, upper, color=color, marker=upper_marker,
                           fillstyle='none' if '<' in upper_op and '=' not in upper_op else 'full',
                           markersize=10)

        # Connect intervals between adjacent axes
        for i in range(num_axes - 1):
            var1 = variables[i]
            var2 = variables[i + 1]
            if var1 in bounds and var2 in bounds:
                for l1, u1, l1_op, u1_op in bounds[var1]:
                    for l2, u2, l2_op, u2_op in bounds[var2]:
                        ax.plot([i, i + 1], [u1, u2], color=color, linewidth=1, linestyle="--")
                        ax.plot([i, i + 1], [l1, l2], color=color, linewidth=1, linestyle="--")

    # Set axis labels
    ax.set_xticks(range(num_axes))
    ax.set_xticklabels(variables)
    ax.set_xlim(-0.5, num_axes - 0.5)
    # Set y limits based on global min/max with small padding
    padding = (global_max - global_min) * 0.05
    ax.set_ylim(global_min - padding, global_max + padding)
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
        hyperblocks, var_order = parse_normal_form(statement)
        visualize_hyperblocks(hyperblocks, var_order)

if __name__ == "__main__":
    main()
