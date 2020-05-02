import math
import numpy as np

def InitList(maxVal, nDim):
    return [[[np.array([i], dtype = "uint32")] if j == 0 else [[]] for j in range(nDim)] for i in range(maxVal + 1)]

def CreateSparseMultiIndex(nDim, maxVal):
    arr = InitList(maxVal, nDim);
    for iDim in range(1, nDim):
        for iVal in range(0, maxVal + 1):
            for iInter in range(0, iVal + 1):
                tempRes = np.copy(arr[iVal - iInter][iDim - 1])
                tempRes = np.hstack((tempRes, iInter * np.ones((tempRes.shape[0], 1), dtype = "uint32")))
                arr[iVal][iDim] = tempRes if len(arr[iVal][iDim][0]) == 0 else np.vstack((arr[iVal][iDim], tempRes))
    retVal = arr[0][nDim - 1]
    for i in range(1, maxVal + 1):
        retVal = np.vstack((retVal , arr[i][nDim - 1]))
    return retVal

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
    retVal = np.zeros(basis.shape[0], dtype = "float")
    for ind1, base in enumerate(basis):
        retVal[ind1] = 1
        for ind0, polType in enumerate(polTypes):
            retVal[ind1] = retVal[ind1] * NormKernel(polType, base[ind0])
    return retVal

def CreateBasisPC(pce, pceSettings):
    polOrder, polTypes, gridLevel, trim = pceSettings.polOrder, pceSettings.polTypes, pceSettings.gridLevel, pceSettings.trim
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