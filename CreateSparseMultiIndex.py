import numpy as np

def InitList(maxVal, nDim):
    return [[[np.array([i], dtype = "uint32")] if j == 0 else [[]] for j in range(nDim)] for i in range(maxVal + 1)]

def CreateSparseMultiIndex(nDim, maxVal):
    arr = InitList(maxVal, nDim);
    for iDim in range(1, nDim):
        for iVal in range(0, maxVal + 1):
            for iInter in range(0, iVal + 1):
                tempRes = np.copy(arr[iVal - iInter][iDim - 1])
                tempRes = np.hstack((tempRes, iInter * np.ones((tempRes.shape[0], 1))))
                arr[iVal][iDim] = tempRes if len(arr[iVal][iDim][0]) == 0 else np.vstack((arr[iVal][iDim], tempRes))
    retVal = arr[0][nDim - 1]
    for i in range(1, maxVal + 1):
        retVal = np.vstack((retVal , arr[i][nDim - 1]))
    return retVal


