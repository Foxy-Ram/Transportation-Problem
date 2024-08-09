from TransportSolver import (NorthWestCornerRule,
                             MatrixMinimaMethod,
                             VogelApproximationMethod)
from TransportSolver import user_input, adjust_matrix

availabilities = [60, 70, 80]
requirements = [50, 70, 60]
d = [[8, 7, 3], [3, 8, 7], [11, 3, 5]]
# d, availabilities, requirements = user_input()

d, availabilities, requirements = adjust_matrix(d, availabilities, requirements)
condition = True
print(d,availabilities, requirements)
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
    print("Rs.",sum([i*j for i, j in minimum_cost]), sep="")
