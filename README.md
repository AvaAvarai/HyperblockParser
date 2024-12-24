# HyperblockParser

Parses conjunctive normal form hyperblock (HB) notation to parallel coordinates visualization. Reads HBs from the `statements.txt` file and visualizes them with Matplotlib.

![demo HBs](./demo.png)

## Parsing

The parser supports HB statements in the following format:

### Basic Syntax

- Variables: Any alphanumeric variable name (case insensitive)
- Inequalities: `<` (strict) or `<=` (non-strict)
- Values: Decimal numbers between 0 and 1
- Logical operators:
  - `&` for AND
  - `v` for OR
  - `+` to combine multiple hyperblocks
- Parentheses: `()` to group expressions
- Brackets: `[]` to group disjunctions

### Statement Structure

1. Single bounds: `(0.2 <= temperature <= 0.4)`
2. Conjunctions: `(0.2 <= temp <= 0.4) & (0.3 <= pressure <= 0.5)`
3. Disjunctions: `[(0.2 <= humidity <= 0.4) v (0.6 <= humidity <= 0.8)]`
4. Combined hyperblocks: `<hyperblock1> + <hyperblock2>`

### Example

```txt
(0.2 <= x1 <= 0.4) & (0.2 <= x2 <= 0.4) & [(0.2 <= x3 <= 0.4) v (0.6 <= x3 <= 0.8)]
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
