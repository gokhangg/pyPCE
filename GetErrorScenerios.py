from Basis.Cell import *
from Quadratures import GaussHermiteQuadrature

class Quadratures(object):

    def __init__(self, gridLevel, quadratureTypes):
        self.__quadratureTypes
        self.__nTypes = len(quadratureTypes)
        self.__gridLevel = gridLevel
        self.quadratureTypes = quadratureTypes
        self.nodes = Cell.FromList([self.__nTypes, self.__gridLevel])
        self.weights = Cell.FromList([self.__nTypes, self.__gridLevel])
        self.sparseNodes = Cell.FromList([self.__nTypes, self.__gridLevel])
        self.sparseWeights = Cell.FromList([self.__nTypes, self.__gridLevel])

def QuadratureFunction(quadratureType):
    if quadratureType == "gauss-hermite":
        return GaussHermiteQuadrature.GaussHermite
    else:
        assert("Invalid quadrature type.")

def CalculateQuadrature(quadFunct, gridLevel):
    nodes = Cell.FromList([1, gridLevel])
    weights = Cell.FromList([1, gridLevel])
    for ind in range(gridLevel):
        adjOrd = 2 * ind - 1
        n, w = quadFunct(adjOrd)
        nodes[1, ind], weights[1, ind] = [n], [w]

def GetQuadratures(gridLevel, quadratureTypes):
    quadratures = Quadratures(gridLevel, quadratureTypes)

    for it in quadratureTypes:
        quadFunct = QuadratureFunction(it)
