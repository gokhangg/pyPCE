import numpy as np

def Cartesian(args):
    ySize = 1
    stride = [ySize]
    for it in args:
        ySize *= len(it)
        stride += [ySize]
    retVal = np.zeros((ySize, len(args)))
    for ind0 in range(ySize):
        for ind1 in range(len(args)):
            retVal[ind0, ind1] = args[ind1][(int(ind0 / stride[ind1])) % len(args[ind1])]
    return retVal

def Sort(ls):
    sort = np.arange(ls.shape[0])#np.array([ind for ind in range(ls.shape[0])])
    mask = [[np.array([True for ind in range(ls.shape[0])])]]
    for indCol in range(0, ls.shape[1]):
        unq = np.unique(ls[:, indCol])
        mask.append([])
        for indMask in range(len(mask[indCol])):
            for indUnq in range(len(unq)):
                sort[mask[indCol][indMask]] = sort[mask[indCol][indMask]][ls[mask[indCol][indMask], indCol].argsort()]
                ls[mask[indCol][indMask]] = ls[mask[indCol][indMask]][ls[mask[indCol][indMask], indCol].argsort()]
                mask[indCol + 1].append( mask[indCol][indMask] & np.isclose(ls[:, indCol], unq[indUnq]) )
    invSort = np.array([(sort == ind).argmax() for ind in range(ls.shape[0])])
    return ls, sort, invSort

def Unique(n):
    if len(n.shape) == 1:
        n = np.reshape(n, [-1, 1])
    ls, _, invSortFull = Sort(n)
    testFun = lambda a, b: np.all(np.isclose(a, b))
    retSort = [0]
    retUnique = ls[0, :].reshape([1, -1])
    shift = 0
    for ind in range(1, ls.shape[0]):
        this = ls[ind, :]
        if testFun(this, ls[ind - 1, :]):
            shift += 1
        else:
            retUnique = np.append(retUnique, this.reshape([1, -1]), axis = 0)
        retSort.append(ind - shift)
    invertSort = np.array([i for i in range(retUnique.shape[0])])[np.array(retSort)][invSortFull]
    return retUnique, invertSort

def Sub2Ind(sz, row, col):
    sz, row, col = np.array(sz), np.array(row), np.array(col)
    if not row.shape == col.shape:
        assert("Row and column size mismatch.")
    return sz[0] * (col - 1) + row

def AccumArray(subs, val):
    subs, val = np.array(subs) + 1, np.array(val)
    mx = subs.max()
    retVal = np.zeros(mx)
    for ind in range(1, mx + 1):
        retVal[ind - 1] += val[subs == ind].sum()
    return retVal

def GetSize(matrix, axis = 0):
    return matrix.shape[axis]

def ApplyFuncToCellMatrix(cellMatrix, Func, axis = 0):
    retVal = []
    cellMatrix = np.reshape(cellMatrix, [-1])
    for ind in range(len(cellMatrix)):
        retVal.append(Func(cellMatrix[ind], axis))
    return retVal

def NodeSizeToSplitSize(nodeSize):
    temp = 0
    nodeSize = list.copy(nodeSize)
    for ind in range(len(nodeSize)):
        temp += nodeSize[ind]
        nodeSize[ind] = temp
    return nodeSize[:-1]
