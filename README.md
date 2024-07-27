# Transportation Problem Solver
This Python package provides solutions to the transportation problem using three different algorithms: North West Corner Rule, Matrix Minima Method, and Vogel's Approximation Method. The transportation problem is a type of linear programming problem where the goal is to determine the most cost-efficient way to transport goods from multiple suppliers to multiple consumers while satisfying supply and demand constraints.

**NOTE: Supply - Availabilities & Demands - Requirements**<br>
Supply and Demands are also tell as Availabilities and Requirements

## Features
- **North West Corner Rule**: A simple and straightforward method for generating an initial feasible solution.
- **Matrix Minima Method**: An improvement over the North West Corner Rule by selecting the cell with the minimum cost.
- **Vogel's Approximation Method** : A heuristic method that often produces better initial solutions by considering the penalties of not using the cheapest routes.

## Installation
**Install the required libraries using:**

```python
pip install numpy
```

## Usage
**Importing the Package**

```python
from OR import (NorthWestCornerRule,
                MatrixMinimaMethod, 
                VogelApproximationMethod)
from OR import user_input, adjust_matrix 
```

## Sample Data
```python
availabilities = [60, 70, 80]
requirements = [50, 70, 60]
d = [[8, 7, 3], [3, 8, 7], [11, 3, 5]]
```

## Getting User Input
To input the transportation matrix, availabilities, and requirements directly from the console, enter the matrix row by row, with elements separated by spaces:
```
matrix, avail, require = user_input()
```
Console output
```python
Enter 'q' to quit: 
Row 1: 8 7 3
Row 2: 3 8 7
Row 3: 11 3 5
Row 4: q
Enter Availabilities: 60 70 80
Enter Requirements: 50 70 60
```

## Adjusting the Matrix
Ensure that the matrix is balanced (sum of availabilities equals the sum of requirements):
```python
d, availabilities, requirements = adjust_matrix(d, availabilities, requirements)
```

## Solving Using Vogel's Approximation Method
```python
condition = True
print(d, availabilities, requirements)

if __name__ == "__main__":
    costs = []
    quality = []

    while condition:
        obj = VogelApproximationMethod(d, availabilities, requirements)
        obj.print()
        costs.append(a := obj.get_cost())
        print("Cost:", a)
        quality.append(b := obj.get_quality())
        print("Quality:", b)
        condition, d, availabilities, requirements = obj.prune_matrix()
        print("-----------------------------------")

    minimum_cost = zip(costs, quality)
    print("Rs.", sum([i*j for i, j in minimum_cost]), sep="")
```

## Results
This is the result of a sample data which is provided in above
```python
Matrix:
[[ 8  7  3  0]
 [ 3  8  7  0]
 [11  3  5  0]]
Availabilities:
[60, 70, 80]
Requirements:
[50, 70, 60, 30] 

Cost: 3
Quality: 50
-----------------------------------
Matrix:
[[7 3 0]
 [8 7 0]
 [3 5 0]]
Availabilities:
[60, 20, 80]
Requirements:
[70, 60, 30] 

Cost: 0
Quality: 20
-----------------------------------
Matrix:
[[7 3 0]
 [3 5 0]]
Availabilities:
[60, 80]
Requirements:
[70, 60, 10] 

Cost: 3
Quality: 70
-----------------------------------
Matrix:
[[3 0]
 [5 0]]
Availabilities:
[60, 10]
Requirements:
[60, 10] 

Cost: 0
Quality: 10
-----------------------------------
Matrix:
[[3]
 [5]]
Availabilities:
[60, 0]
Requirements:
[60] 

Cost: 3
Quality: 60
-----------------------------------
Matrix:
[[5]]
Availabilities:
[0]
Requirements:
[0] 

Cost: 5
Quality: 0
-----------------------------------
Rs.540
```

## Classes and Methods
### Exceptions
- NotMatch: Raised when the sum of availabilities does not match the sum of requirements.
- MatrixUneven: Raised when the input matrix is jagged (not rectangular).
- UIException: Raised when the input data is not balanced.

### NorthWestCornerRule
 - **get_position():** Returns the position of the current cell according to the North-West Corner Rule.
- **get_cost():** Returns the cost of the current cell.
- **get_quality():** Returns the quantity to be transported from the current cell.
- **print():** Prints the current state of the matrix, availabilities,  and requirements.
- **prune_matrix():** Updates the matrix by removing the fulfilled row or column.
- **is_ThereMatrix():** Checks if there is any remaining matrix to process.

### MatrixMinimaMethod (inherits from NorthWestCornerRule)
- **get_position():** Returns the position of the cell with the minimum cost.

### VogelApproximationMethod (inherits from NorthWestCornerRule)
- **get_penalty(data):** Returns the penalty of either a row or column based on the provided list.
- **get_penalties(data):** Returns a tuple of penalties for rows and columns.
- **get_position():** Returns the position of the smallest value in the highest penalty row or column.

## Contributing
- Contributions are welcome! Please feel free to submit a Pull Request or open an Issue.

## Acknowledgements
- Thanks to the developers of NumPy for providing an efficient numerical computing library.
- Special thanks to our `Statistic's lecturer` who taught me the algorithms manually while pursuing the degree.
