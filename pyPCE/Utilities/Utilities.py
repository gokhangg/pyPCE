import numpy as np

def Cartesian(args):
    """
    Takes cartesian product of the input
    :param args: input vectors whereby cartesian products are computed.
    :return: cartesian product.
    """
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

def Sort(inVect):
    """
    Used to sort elements of input vector or matrix.
    :param inVect: input vector or matrix.
    :return: inVect: sorted vector or matrix.
             sort: indices of sorted elements.
             invSort: inverted sort indices whereby input can be generated back.
    """
    sort = np.arange(inVect.shape[0])
    mask = [[np.array([True for ind in range(inVect.shape[0])])]]
    for indCol in range(0, inVect.shape[1]):
        unq = np.unique(inVect[:, indCol])
        mask.append([])
        for indMask in range(len(mask[indCol])):
            for indUnq in range(len(unq)):
                sort[mask[indCol][indMask]] = sort[mask[indCol][indMask]][inVect[mask[indCol][indMask], indCol].argsort()]
                inVect[mask[indCol][indMask]] = inVect[mask[indCol][indMask]][inVect[mask[indCol][indMask], indCol].argsort()]
                mask[indCol + 1].append(mask[indCol][indMask] & np.isclose(inVect[:, indCol], unq[indUnq]))
    invSort = np.array([(sort == ind).argmax() for ind in range(inVect.shape[0])])
    return inVect, sort, invSort

def Unique(inVect):
    """
    Used to get unique elements of input vector or matrix.
    :param inVect: Input vector or matrix.
    :return: retUnique: Sorted unique form of the input vector or matrix.
             invSOrt: Inverted sort indices whereby input can be generated back.
    """
    if len(inVect.shape) == 1:
        inVect = np.reshape(inVect, [-1, 1])
    ls, _, invSortFull = Sort(inVect)
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

def Sub2Ind(sz, *args):
    """
    Used to get 1D memory location indices of elements in N-D container for the locations in row and col.
    :param sz: Container.
    :param *args: Locations of the selected container elements in N-D space.
    :return: Locations of elements of the container.
    """
    sz = np.array(sz)
    args = list(args)
    args[0] = np.array(args[0])
    retVal = args[0]
    stride = 1
    for ind in range(1, len(args)):
        args[ind] = np.array(args[ind])
        if not args[ind].shape in args[0].shape:
            assert ("Shape mismatch.")
        stride *= sz[ind - 1]
        retVal += stride * (args[ind] - 1)
    return retVal

def AccumArray(subs, val):
    """
    Creates an array retVal by accumulating elements of the
    vector val using the subscripts in SUBS.
    :param subs: Positive integer vector.
    :param val: Values to be summed for the indices in subs.
    :return: Accumulation result.
    """
    subs, val = np.array(subs) + 1, np.array(val)
    mx = subs.max()
    retVal = np.zeros(mx)
    for ind in range(1, mx + 1):
        retVal[ind - 1] += val[subs == ind].sum()
    return retVal

def GetSize(matrix, axis = 0):
    """
    Used to obtain size in a given axis.
    :param matrix: Input matrix whose size in the given axis will return.
    :param axis: Axis to get the size.
    :return: Size
    """
    return matrix.shape[axis]

def ApplyFuncToCellMatrix(cellMatrix, Func, axis = 0):
    """
    Applies a specific function to the input cell.
    :param cellMatrix: The cell matrix on which the operation is to be done.
    :param Func: Function to be applied.
    :param axis: Axis where the funtion is applied.
    :return: Result matrix.
    """
    retVal = []
    cellMatrix = np.reshape(cellMatrix, [-1])
    for ind in range(len(cellMatrix)):
        retVal.append(Func(cellMatrix[ind], axis))
    return retVal

def NodeSizeToSplitSize(nodeSize):
    """
    Used to combine all sub list elements into one.
    :param nodeSize: List with multiple list from which a list is extracted
            by concatanating sub elements.
    :return: List with concatanated elements.
    """
    temp = 0
    nodeSize = list(nodeSize)
    for ind in range(len(nodeSize)):
        temp += nodeSize[ind]
        nodeSize[ind] = temp
    return nodeSize[:-1]

def StringUnique(stringVector):
    """
    Used to get unique elements of input string vector.
    :param stringVector: Input string vector.
    :return: Unique string vector.
    """
    stringVector = np.array(stringVector)
    uStringVector = np.unique(stringVector)
    iUStringVector = np.ones(stringVector.shape[0], dtype = "uint32")
    for ind in range(uStringVector.shape[0]):
        iUStringVector[stringVector == uStringVector[ind]] = ind
    return uStringVector, iUStringVector

def RepMat(inVect, repList):
    """
    Used to repeat a patter in a matrix/
    :param inVect: Input vector or matrix to be repeated.
    :param repList: Patern of the repetition.
    :return: Created repetition matrix.
    """
    vect = np.copy(inVect)
    for ind in range(len(repList)):
        ones_ = np.ones(ind + 1, dtype = "uint32")
        ones_[0] = repList[ind]
        vect = np.tile(vect, ones_)
    return vect.transpose(np.flip(np.arange(len(vect.shape))))