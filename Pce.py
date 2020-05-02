from CreateBasis import *

def CalculateCoefficients(outVals,)



class PceSettings:
    pass


PceSettings.gridLevel = 3
PceSettings.quadratureType = ["gauss-hermite", "gauss-hermite", "gauss-hermite"]
PceSettings.gridType = "sparse"
PceSettings.deviations = [0.5, 1.5, 1.5]


CreateBasisPC(polOrder, polTypes, gridLevel, trim)



import numpy as np

""""
class Cell(object):
    def __init__(self, cell, dim):
        self.__cell = cell
        self.__dim = dim
        self.__stride = np.array([(dim[: i - len(dim)]).prod() for i in range(len(dim))])

    def GetCellAsLinearList(self):
        return self.__cell

    def GetDimension(self):
         return  self.__dim

    def GetStride(self):
         return  self.__stride

    @classmethod
    def FromList(cls, lst):
        return cls.FromListWithInitVal(lst)

    @classmethod
    def FromListWithInitVal(cls, dimList, initClass = []):
        dim = np.array(dimList)
        return Cell(cls.__InitLinearList(dim, initClass), dim)

    @staticmethod
    def __InitLinearList(dim, initClass = []):
        return [initClass for i in range(dim.prod())]

    def __getitem__(self, *argv):
        return self.__GetItem(np.array(argv[0]))

    def __setitem__(self, *argv):
        self.__SetItem(np.array(argv[0]), argv[-1])

    def __GetItem(self, indices):
        if not (self.__dim < indices).sum() < len(indices):
            assert("Incompatible index")
        return self.__cell[(indices * self.__stride).sum()]

    def __SetItem(self, indices, item):
        if not (self.__dim < indices).sum() < len(indices):
            assert ("Incompatible index")
        self.__cell[(indices * self.__stride).sum()] = item
"""