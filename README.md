# Transportation Problem Solver
This Python package provides solutions to the transportation problem using three different algorithms: North West Corner Rule, Matrix Minima Method, and Vogel's Approximation Method. The transportation problem is a type of linear programming problem where the goal is to determine the most cost-efficient way to transport goods from multiple suppliers to multiple consumers while satisfying supply and demand constraints.

## Features
- **North West Corner Rule**: A simple and straightforward method for generating an initial feasible solution.
- **Matrix Minima Method**: An improvement over the North West Corner Rule by selecting the cell with the minimum cost.
- **Vogel's Approximation Method** : A heuristic method that often produces better initial solutions by considering the penalties of not using the cheapest routes.

## Installation
- Install the required libraries using:

```pip install numpy```

## Usage
**Importing the Package**

```
from OR import (NorthWestCornerRule,
                MatrixMinimaMethod, 
                VogelApproximationMethod)
from OR import user_input, adjust_matrix 
```
