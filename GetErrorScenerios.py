from Basis.Utilities import *
from GetCubatures import *
from Quadratures import GaussHermiteQuadrature
import numpy as np


class Quadratures(object):

    def __init__(self, gridLevel, quadratureTypes):
        self.__nTypes = len(quadratureTypes)
        self.__gridLevel = gridLevel
        self.quadratureTypes = quadratureTypes
        self.nodes = np.ndarray([self.__nTypes, self.__gridLevel], dtype = object)
        self.weights = np.ndarray([self.__nTypes, self.__gridLevel], dtype = object)
        self.sparseNodes = np.ndarray([self.__nTypes, self.__gridLevel], dtype = object)
        self.sparseWeights = np.ndarray([self.__nTypes, self.__gridLevel], dtype = object)

def QuadratureFunction(quadratureType):
    if quadratureType == "gauss-hermite":
        return GaussHermiteQuadrature.GaussHermite
    else:
        assert("Invalid quadrature type.")

def CalculateQuadrature(quadFunct, gridLevel):
    nodes = np.ndarray([1, gridLevel], dtype = object)
    weights = np.ndarray([1, gridLevel], dtype = object)
    for ind in range(gridLevel):
        nodes[0, ind], weights[0, ind] = quadFunct(2 * ind + 1)
    return nodes, weights

def GetSparseNodesAndWeights(nodes, weights):
    szY = nodes.shape[1]
    sparceNodes = np.ndarray([1, szY], dtype = object)
    sparceWeights = np.ndarray([1, szY], dtype = object)
    sparceNodes[0, 0] = np.copy(nodes[0, 0])
    sparceWeights[0, 0] = np.copy(weights[0, 0])
    for ind in range(1, szY):
        sparceNodes[0, ind], nodeIndices = Unique(np.append(nodes[0, ind], nodes[0, ind - 1]))
        sparceWeights[0, ind] = AccumArray(np.array(nodeIndices), np.append(weights[0, ind], -weights[0, ind - 1]))
    return sparceNodes, sparceWeights

def GetQuadratures(gridLevel, quadratureTypes):
    quadratures = Quadratures(gridLevel, quadratureTypes)
    for ind, it in enumerate(quadratureTypes):
        quadFunct = QuadratureFunction(it)
        quadratures.nodes[ind, :], quadratures.weights[ind, :] = CalculateQuadrature(quadFunct, gridLevel)
        quadratures.sparseNodes[ind, :], quadratures.sparseWeights[ind, :] = GetSparseNodesAndWeights(quadratures.nodes, quadratures.weights)
    return quadratures

def GetErrorScenerios(pceSettings):
    quadratures = GetQuadratures(pceSettings.gridLevel, pceSettings.quadratureType)
    cubatures = GetCubature(quadratures, pceSettings.gridLevel, pceSettings.gridType)
    cubatures.quadratures = quadratures
    cubatures.scenarios, scenarioIndex = Unique(np.concatenate(cubatures.nodes.transpose()[:, 0]))
    cubatures.scenariosScaled = cubatures.scenarios.dot(np.diag(pceSettings.sDeviations))
    cubatures.totalWeights = AccumArray(scenarioIndex, np.concatenate(cubatures.weights[0, :]))
    nodeSize = ApplyFuncToCellMatrix(cubatures.nodes, GetSize, axis = 0)
    cubatures.fullIndex = np.array(np.split(scenarioIndex, NodeSizeToSplitSize(nodeSize)), dtype = object)
    return cubatures