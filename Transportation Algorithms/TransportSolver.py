import numpy as np

class NotMatch(Exception): 
    """Exception raised when the sum of availabilities and requirements do not match."""
    
    def __init__(self, message):
        self.message = message

class MatrixUneven(Exception): 
    """Exception raised for uneven (jagged) matrices."""
    
    def __init__(self, message):
        self.message = message

class UIException(Exception): 
    """Exception raised for incorrect user inputs that do not form a valid matrix."""
    
    def __init__(self, message):
        self.message = message

class NorthWestCornerRule:
    """Class implementing the North-West Corner Rule for solving transportation problems."""
    
    def __init__(self, data, avail, require):
        """
        Initialize the NorthWestCornerRule instance.
        
        Args:
            data (list[list[int|float]]): Cost matrix for the transportation problem.
            avail (list[int|float]): List of available supplies.
            require (list[int|float]): List of required demands.
            
        Raises:
            NotMatch: If the sum of availabilities and requirements do not match.
            UIException: If the input data dimensions do not match the availability and requirement lengths.
            MatrixUneven: If the input matrix is uneven (jagged).
        """
        self.data = np.array(data)
        self.avail = avail
        self.require = require

        if sum(self.avail) != sum(self.require):
            raise NotMatch("Check that the sum of availabilities and requirements are the same!")

        if len(self.avail) != len(self.data) or len(self.require) != len(self.data[0]):
            raise UIException("The input data dimensions might not be appropriate; redress the inputs again.")

        self.__len = [len(r) for r in data]
        for r in range(1, len(self.__len)):
            if self.__len[0] != self.__len[r]:
                raise MatrixUneven("Rows or columns of the matrix might be uneven.")

    def get_position(self):
        """
        Get the position of the cell in the matrix according to the North-West Corner Rule.
        
        Returns:
            tuple: The position (row, column) of the cell.
        """
        arr = self.data
        spot = np.where(arr == arr[0, 0])
        position = (list(spot[0])[0], list(spot[1])[0])
        return position

    def get_cost(self):
        """
        Get the cost of the cell in the matrix at the current position.
        
        Returns:
            int|float: The cost value at the current position.
        """
        return self.data[self.get_position()]

    def get_quality(self):
        """
        Get the quality of the matrix at the current position using the North-West Corner Rule.
        
        Returns:
            int|float: The minimum value between the availability and requirement at the current position.
        """
        position = self.get_position()
        quality = min(self.avail[position[0]], self.require[position[1]])
        return quality

    def print(self) -> None:
        """
        Display the details of the current matrix, including availabilities and requirements.
        """
        print("Matrix:")
        print(np.array(self.data))
        print("Availabilities:")
        print(self.avail)
        print("Requirements:")
        print(self.require, "\n")

    def prune_matrix(self):
        """
        Prune the matrix based on the North-West Corner Rule algorithm.
        
        Returns:
            tuple: A tuple containing:
                - condition (bool): True if there is a matrix after pruning, False otherwise.
                - matrix (list[list[int|float]]): The pruned matrix.
                - avail (list[int|float]): The pruned availability list.
                - require (list[int|float]): The pruned requirement list.
        """
        condition = True
        matrix_ = list(self.data)
        matrix = [list(i) for i in matrix_]
        pos_a, pos_r = self.get_position()

        if len(self.data.ravel()) == 2:
            if self.avail[pos_a] >= self.require[pos_r] and len(self.require) == 1:
                min_ = min(self.avail[1], self.require[0]) 
                return True, [matrix[1]], [min_], [min_]

            if self.avail[pos_a] <= self.require[pos_r] and len(self.avail) == 1:
                min_ = min(self.avail[0], self.require[1])
                return True, [[matrix[0][1]]], [min_], [min_]

        if len(self.data.ravel()) == 1:
            return False, None, None, None
        else:
            if self.avail[pos_a] >= self.require[pos_r]:
                self.avail[pos_a] = abs(self.avail[pos_a] - self.require[pos_r])
                for row in matrix:
                    row.pop(pos_r)
                del self.require[pos_r]

            else:
                self.require[pos_r] = abs(self.require[pos_r] - self.avail[pos_a])
                del matrix[pos_a]
                del self.avail[pos_a]

            return condition, matrix, self.avail, self.require

    def is_ThereMatrix(self):
        """
        Check if there is any matrix remaining after pruning.
        
        Returns:
            bool: True if a matrix remains, False otherwise.
        """
        condition = self.prune_matrix()
        if condition[0] == False:
            print("\nNo, there is no matrix")
            return False
        else:
            print("\nYes, there is a matrix")
            return condition[0]

class MatrixMinimaMethod(NorthWestCornerRule):
    """Class implementing the Matrix-Minima Method for solving transportation problems."""
    
    def __init__(self, data, avail, require):
        """
        Initialize the MatrixMinimaMethod instance.
        
        Args:
            data (list[list[int|float]]): Cost matrix for the transportation problem.
            avail (list[int|float]): List of available supplies.
            require (list[int|float]): List of required demands.
        """
        super(MatrixMinimaMethod, self).__init__(data=data, avail=avail, require=require)

    def get_position(self):
        """
        Get the position of the cell in the matrix according to the Matrix-Minima Method.
        
        Returns:
            tuple: The position (row, column) of the cell with the minimum value in the matrix.
        """
        arr = self.data
        spot = np.where(arr == arr.min())
        position = (list(spot[0])[0], list(spot[1])[0])
        return position

class VogelApproximationMethod(NorthWestCornerRule):
    """Class implementing the Vogel Approximation Method for solving transportation problems."""
    
    def __init__(self, data, avail, require):
        """
        Initialize the VogelApproximationMethod instance.
        
        Args:
            data (list[list[int|float]]): Cost matrix for the transportation problem.
            avail (list[int|float]): List of available supplies.
            require (list[int|float]): List of required demands.
        """
        super(VogelApproximationMethod, self).__init__(data=data, avail=avail, require=require)

    def get_penalty(self, data):
        """
        Calculate the penalty for a row or column based on the difference between the two smallest values.
        
        Args:
            data (list[int|float]): A row or column of the matrix.
            
        Returns:
            int|float: The penalty value.
        """
        result = sorted(data)
        return result[0] - result[1]

    def get_penalties(self, data):
        """
        Calculate the penalties for all rows and columns in the matrix.
        
        Args:
            data (np.ndarray): The matrix to calculate penalties for.
            
        Returns:
            tuple: A tuple containing the row penalties and column penalties.
        """
        r = data
        c = r.copy().T
        row_pen = [abs(self.get_penalty(i)) for i in r]
        col_pen = [abs(self.get_penalty(j)) for j in c]
        return row_pen, col_pen

    def get_position(self):
        """
        Get the position of the cell in the matrix according to the Vogel Approximation Method.
        
        Returns:
            tuple: The position (row, column) of the cell with the smallest value in the row or column 
            with the largest penalty.
        """
        if len(self.data.ravel()) <= 2:
            return 0, 0

        try:
            r, c = self.get_penalties(self.data)
            max_r, max_c = max(r), max(c)
            index_r = index_c = None
            if max_r >= max_c:
                index_r = r.index(max_r)
            else:
                index_c = c.index(max_c)

            if index_r is None:
                c_pos = index_c
                temp = list([i[c_pos] for i in self.data])
                min_val = sorted(temp)[0]
                r_pos = temp.index(min_val)
                return r_pos, c_pos
            else:
                r_pos = index_r
                temp = list(self.data[r_pos])
                min_val = sorted(temp)[0]
                c_pos = temp.index(min_val)
                return r_pos, c_pos

        except Exception as e:
            return 0, 0

def user_input():
    """
    Get input from the user for the cost matrix, availabilities, and requirements.
    
    Returns:
        tuple: A tuple containing:
            - matrix (list[list[int|float]]): The cost matrix.
            - avail (list[int|float]): The list of available supplies.
            - require (list[int|float]): The list of required demands.
    """
    matrix = []
    print("Enter 'q' to quit: ")
    count_row = 1
    while True:
        n = input(f"Row {count_row}: ")
        if n == "q":
            break
        matrix.append(list(map(int, n.split())))
        count_row += 1

    avail = list(map(int, input("Enter Availabilities: ").split()))
    require = list(map(int, input("Enter Requirements: ").split()))
    return matrix, avail, require

def adjust_matrix(data: list[list[int|float]], availabilities: list, requirements: list):
    """
    Adjust the matrix by adding a dummy row or column if availabilities and requirements do not match.
    
    Args:
        data (list[list[int|float]]): The original cost matrix.
        availabilities (list[int|float]): The list of available supplies.
        requirements (list[int|float]): The list of required demands.
        
    Returns:
        tuple: A tuple containing:
            - data (list[list[int|float]]): The adjusted cost matrix.
            - availabilities (list[int|float]): The adjusted list of available supplies.
            - requirements (list[int|float]]: The adjusted list of required demands.
            
    Raises:
        MatrixUneven: If the provided data is a jagged matrix.
    """
    if len(data) != len(availabilities) or len(data[0]) != len(requirements):
        raise Exception("Number of origins and availabilities or number of destinations and requirements are not equal.")

    __len = [len(r) for r in data]
    for r in range(1, len(__len)):
        if __len[0] != __len[r]:
            raise MatrixUneven("The provided data is a jagged matrix.")

    size_of_row = len(requirements)
    sum_a = sum(availabilities)
    sum_r = sum(requirements)

    if sum_a != sum_r:
        if sum_a > sum_r:
            temp = []
            for i in data:
                i.append(0)
                temp.append(i)
            data = temp
            requirements.append(abs(sum_a - sum_r))
            return data, availabilities, requirements

        else:
            data.append([0] * size_of_row)
            availabilities.append(abs(sum_r - sum_a))
            return data, availabilities, requirements

    else:
        return data, availabilities, requirements
