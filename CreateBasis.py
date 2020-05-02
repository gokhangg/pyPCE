
from CreateSparseMultiIndex import *
import math
import numpy as np

def CreateIndicesForBasisFilter(indices):
    indices = np.array(indices, dtype = "uint32")
    for ind, it in enumerate(indices):
        indices[ind] = ind * it
    return indices

def NormKernel(polType, index):
    if polType == "hermite":
        return np.math.factorial(index)
    elif polType == "legendre":
        return 1. / (2 * index+ 1)
    elif polType == "laguerre":
        return 1
    elif polType == "jacobi":
        return np.math.gamma(index + 1) / ((2 * index + 1) * np.math.factorial(index))
    else:
        assert("Unknown polynomial type.")

def CreateNorm(basis, polTypes):
    retVal = np.zeros(basis.shape[0], dtype = "uint32")
    for ind1, base in enumerate(basis):
        retVal[ind1] = 1
        for ind0, polType in enumerate(polTypes):
            retVal[ind1] = retVal[ind1] * NormKernel(polType, base[ind0])
    return retVal

def CreateBasisPC(polOrder, polTypes, gridLevel, trim):
    basis = CreateSparseMultiIndex(len(polTypes), polOrder)
    if trim:
        nDim = basis.shape[1]
        if nDim == 1:
            trimFactor = 1
        elif gridLevel < nDim:
            trimFactor = 1
        else:
            trimFactor = math.log(polOrder) / math.log(nDim)
            trimFactor = trimFactor - 0.01
        iToKeep = np.power(np.sum(np.power(basis, trimFactor), 1), 1 / trimFactor) <= polOrder
        iToKeep = CreateIndicesForBasisFilter(iToKeep)
        basis = basis[iToKeep, :]
        return basis, CreateNorm(basis, polTypes)