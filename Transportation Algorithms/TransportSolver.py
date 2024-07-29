import numpy as np

class NotMatch(Exception): # Not Match
    def __init__(self,message):
        self.message = message

class MatrixUneven(Exception): # Matrix Uneven
    def __init__(self,message):
        self.message = message

class UIException(Exception): # UI - User Input
    def __init__(self,message):
        self.message = message

class NorthWestCornerRule:
    def __init__(self, data, avail, require):
        self.data = np.array(data) # (1)
        self.avail = avail
        self.require = require

        # The Not match exception checks the sum of availabilities and requirements are equal or not if not "Insists on to add a dummy variable".
        if sum(self.avail) != sum(self.require):
            raise NotMatch("Check the sum of Availabilities and Requirements are same...!")

        # The UIException checks the all inputs are balanced are not.
        if len(self.avail) != len(self.data) and len(self.require) != len(self.data[0]) :
            raise UIException("The input data might not be appropriate redress the inputs again")

        # The Matrix uneven exception deprecate jagged matrix, it is optional. The above (1) numpy checks before this.
        self.__len = [len(r) for r in data]
        for r in range(1, len(self.__len)):
            if self.__len[0] != self.__len[r]:
                raise MatrixUneven("Might be the rows or columns values are jagged")

    # Getting position of a cell using North-West corner rule
    def get_position(self):
        arr = self.data
        spot = np.where(arr == arr[0, 0])
        position = (list(spot[0])[0], list(spot[1])[0])
        return position

    # Getting cost of matrix using N-W-C-R
    def get_cost(self):
        return self.data[self.get_position()]

    # Getting quality of matrix using N-W-C-R
    def get_quality(self):
        position = self.get_position()
        quality = min(self.avail[position[0]], self.require[position[1]])
        return quality

    # Displaying the details of current matrix
    def print(self)->None:
        print("Matrix:")
        print(np.array(self.data))
        print("Availabilities:")
        print(self.avail)
        print("Requirements:")
        print(self.require,"\n")

    # Pruning matrix purely instructions based on N-W-C-R algorithm
    def prune_matrix(self):
        # The below condition determines True when there is table. It is more helpful for running loop to generate pruning Tables
        condition = True
        matrix_ = list(self.data)
        matrix = [list(i) for i in matrix_]
        pos_a, pos_r = self.get_position()

        # This IF solves the Two bugs which appears only in matrix 2*1 (or) 1*2 while testing is taken place
        if len(self.data.ravel()) == 2:
            if self.avail[pos_a]>=self.require[pos_r] and len(self.require) == 1:# (1)
                min_ = min(self.avail[1], self.require[0]) 
                return True, [matrix[1]], [min_], [min_]

            if self.avail[pos_a]<=self.require[pos_r] and len(self.avail) == 1:# (2)
                min_ = min(self.avail[0], self.require[1])
                return True, [[matrix[0][1]]], [min_], [min_]

        if len(self.data.ravel()) == 1:
            return False, None, None, None
        else:
            if self.avail[pos_a] >= self.require[pos_r]:# (2)
                self.avail[pos_a] = abs(self.avail[pos_a] - self.require[pos_r])
                for row in matrix:
                    row.pop(pos_r)
                del self.require[pos_r]

            else:# (1)
                self.require[pos_r] = abs(self.require[pos_r] - self.avail[pos_a])
                del matrix[pos_a]
                del self.avail[pos_a]

            return condition, matrix, self.avail , self.require

    # Function to check is there any matrix after pruning
    def is_ThereMatrix(self):
        condition = self.prune_matrix()
        if condition[0] == False:
            print("\nNo there is no matrix")
            return False
        else:
            print("\nYes there is a matrix")
            return condition[0]

class MatrixMinimaMethod(NorthWestCornerRule):
    def __init__(self, data, avail, require):
        super(MatrixMinimaMethod,self).__init__(data=data, avail=avail, require=require)

    # Getting position of a cell using Matrix-Minima method
    def get_position(self):
        arr = self.data
        spot = np.where(arr == arr.min())
        position = (list(spot[0])[0], list(spot[1])[0])
        return position

class VogelApproximationMethod(NorthWestCornerRule):
    def __init__(self, data, avail, require):
        super(VogelApproximationMethod,self).__init__(data=data, avail=avail, require=require)

    # This function returns penalty of either row or column based on the list provided
    def get_penalty(self,data):
        result = sorted(data)
        return result[0] - result[1]

    # This function returns list of penalties in rows as well as in columns as tuple
    def get_penalties(self,data):
        r = data
        c = r.copy().T
        row_pen = [abs(self.get_penalty(i)) for i in r]
        col_pen = [abs(self.get_penalty(j)) for j in c]
        return row_pen, col_pen

    # Getting position of a cell using Vogel-Approximation method
    def get_position(self):
        """ This function is somewhat cryptic because it returns
            position of the smallest value in the largest penalty
            either in row or column if both row will be chosen """
        """ After many trials and errors i defined this function """
        # This condition is for to get cost and quality of last 2 remained values in matrix for this we set the position always (0, 0).
        if len(self.data.ravel())<=2:
            return 0, 0

        try: # This try block to manage code if any unexpected error is encountered at above IF condition.
            r, c = self.get_penalties(self.data)
            max_r, max_c = max(r), max(c)
            index_r = index_c = None
            if max_r >= max_c:
                index_r = r.index(max_r)
            else:
                index_c = c.index(max_c)

            # When column position chooses first
            if index_r == None:
                c_pos = index_c
                temp = list([i[c_pos] for i in self.data])
                min_val = sorted(temp)[0]
                r_pos = temp.index(min_val)
                return r_pos, c_pos

            # When row position chooses first
            else:
                r_pos = index_r
                temp = list(self.data[r_pos])
                min_val = sorted(temp)[0]
                c_pos = temp.index(min_val)
                return r_pos, c_pos

        except Exception as e:
            return 0, 0

# This user_input() function gets input from user directly by terminal or output console in row wise
def user_input():
    matrix = []
    print("Enter 'q' to quit: ")
    count_row = 1
    while True:
        n = input(f"Row {count_row}: " )
        if n == "q":
            break
        matrix.append(list(map(int, n.split())))
        count_row += 1

    avail = list(map(int, input("Enter Availabilities: ").split()))
    require = list(map(int, input("Enter Requirements: ").split()))
    return matrix, avail, require


# This function adjust_matrix() adds dummy variable when availabilities != requirements,The steps below are taken based on the algorithm
def adjust_matrix(data: list[list[int|float]], availabilities: list, requirements: list):

    if len(data) != len(availabilities) or len(data[0]) != len(requirements):
        raise "Might be number of origins and availabilities (or) number of destinations and requirements are not equal"

    # Checking that data provided is a matrix if not raises error
    __len = [len(r) for r in data]
    for r in range(1, len(__len)):
        if __len[0] != __len[r]:
            raise MatrixUneven("The provided data to data parameter is not an matrix, it is  jagged")

    size_of_row = len(requirements)
    size_of_col = len(availabilities) # Unused
    sum_a = sum(availabilities)
    sum_r = sum(requirements)

    if sum_a != sum_r: # Checking if not equal we are going to adjust the matrix and remaining variables
        # Here we are appending dummy column if availabilities > requirements  and adjusting requirements according to algorithm
        if  sum_a > sum_r:
            temp = []
            for i in data:
                i.append(0)
                temp.append(i)
            data = temp
            requirements.append(abs(sum_a - sum_r))
            return  data, availabilities, requirements

        # Here we are appending dummy row if requirements > availabilities and adjusting availabilities according to algorithm
        else:
            data.append([0] * size_of_row)
            availabilities.append(abs(sum_r - sum_a))
            return  data, availabilities, requirements

    else: # Else we return the same data, availabilities, requirements which is provided
        return data, availabilities, requirements

