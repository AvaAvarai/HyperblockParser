# HyperblockParser

A Hyperblock (HB) is mathematically defined as an n-orthotope by a set of n-dimensional (n-D) points $`\{ \mathbf{x} = (x_1, x_2, \ldots, x_n) \} `$, with center n-D point $` \mathbf{c} = (c_1, c_2, \ldots, c_n) `$, and side lengths $` \mathbf{L} = (L_1, L_2, \ldots, L_n) `$, such that $` \forall_i \| x_i - c_i \| \leq \frac{L_i}{2} `$.

We can write this in mathematical notation as a conjunctive normal form (CNF) statement of variables, inequalities, and logical operators; such as here are the three Fisher Iris data flower species HB statements in the form of a CNF statement which are combined by the `+` operator to one PC graph:

```txt
[(4.30 <= sepal_length <= 5.80) & (2.30 <= sepal_width <= 4.40) & (1.00 <= petal_length <= 1.90) & (0.10 <= petal_width <= 0.60)] + [(4.90 <= sepal_length <= 7.00) & (2.00 <= sepal_width <= 3.40) & (3.00 <= petal_length <= 5.10) & (1.00 <= petal_width <= 1.80)] + [(4.90 <= sepal_length <= 7.90) & (2.20 <= sepal_width <= 3.80) & (4.50 <= petal_length <= 6.90) & (1.40 <= petal_width <= 2.50)]
```

This project parses the statement into a list of bounds for each variable or attribute and visualizes the resultant HB as a graph in parallel coordinates (PC) where the graph is a upper and lower bound for each attribute connected by polylines by the logical operators.

![demo HB](./screenshots/demo_hb.png)

The current project reads all statements in the `statements.txt` file and visualizes them sequentially with Matplotlib as PC n-D graphs.

![demo HBs](./screenshots/demo.png)

## Parsing

The parser supports CNF HB statements in the following format:

### Basic Syntax

- Variables: Any alphanumeric variable name (case insensitive)
- Inequalities: `<` (strict, open circle) or `<=` (non-strict, closed circle)
- Values: Decimal numbers
- Logical operators:
  - `&` for AND
  - `v` for OR
  - `+` to combine multiple hyperblocks
- Parentheses: `()` to group expressions
- Brackets: `[]` to group disjunctions

The lower and upper bounds of the HB PC graph are determined by the global min and max of all the bounds in the statement.

### Statement Structure

1. Single bounds: `(0.2 < temperature <= 0.4)`
2. Conjunctions: `(0.2 < temp <= 0.4) & (0.3 <= pressure <= 0.5)`
3. Disjunctions: `[(0.2 < humidity <= 0.4) v (0.6 <= humidity <= 0.8)]`
4. Combined hyperblocks: `<hyperblock1> + <hyperblock2>`

Please see the `statements.txt` file for more indepth examples.

## Todo

1. Count cases per class label within HB statements for some given CSV data
2. Interactive REPL interface alongside static statement loading

## License

HyperblockParser is licensed under the MIT License, free to use and modify, commercially and non-commercially, see the `LICENSE` file for more details.
