from Basis.Utilities import *

class Cubature(object):
   pass

def CreateSparseMultiIndex(level, nNodes):
    tempMultiIndex = np.ndarray([level + 1, nNodes], dtype = object)
    tempMultiIndex[:, 0] = np.split(np.array(range(level + 1)).reshape(level + 1, 1), level + 1)
    for ind0 in range(1, nNodes):
        for ind1 in range(level + 1):
            for ind2 in range(ind1 + 1):
                tempResult = tempMultiIndex[ind1 - ind2, ind0 - 1]
                tempResult = np.append(tempResult, ind2 * np.ones([tempResult.shape[0], 1], dtype = "uint32"), axis = 1)
                if type(tempMultiIndex[ind1, ind0]) == type(None):
                    tempMultiIndex[ind1, ind0] = tempResult
                else:
                    tempMultiIndex[ind1, ind0] = np.append(tempMultiIndex[ind1, ind0], tempResult, axis = 0)
    tempMultiIndex = np.concatenate(tempMultiIndex[:, nNodes - 1])
    return tempMultiIndex

def GetCubature(quadratures, gridLevel, gridType):
    cubature = Cubature()
    cubature.gridType = gridType
    cubature.quadratureRules = quadratures.quadratureTypes
    lenNodes = len(quadratures.nodes)
    if gridType == "full":
        var = np.array([ind + 1 for ind in range(gridLevel)])
        multiIndex = Cartesian(np.tile(var, [lenNodes, 1]))
        multiIndexNorm = multiIndex.sum(1)
        toKeep = multiIndexNorm == multiIndexNorm.max()
        multiIndex = multiIndex[toKeep, :]
    elif gridType == "sparse":
        multiIndex = CreateSparseMultiIndex(gridLevel - 1, lenNodes) + 1
    elif gridType == "sparse-adaptive":
        multiIndex = CreateSparseMultiIndex(gridLevel - 1, lenNodes) + 1
    else:
        assert("Unknown grid type.")

    cubature.multiIndex = multiIndex
    iDim = np.tile(np.array(range(1, lenNodes + 1)).reshape(1, lenNodes), [multiIndex.shape[0], 1])
    neededQuad = Sub2Ind(quadratures.nodes.shape, iDim, multiIndex).transpose() - 1

    cubature.nodes = np.ndarray([1, neededQuad.shape[1]], dtype = object)
    cubature.weights = np.ndarray([1, neededQuad.shape[1]], dtype = object)

    for ind in range(neededQuad.shape[1]):
        cubature.nodes[0, ind] = Cartesian(quadratures.sparseNodes.transpose().flatten()[neededQuad[:, ind]])
        cubature.weights[0, ind] = Cartesian(quadratures.sparseWeights.transpose().flatten()[neededQuad[:, ind]]).prod(1)
    return cubature