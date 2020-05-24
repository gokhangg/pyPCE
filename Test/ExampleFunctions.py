TEST_MULTIVARFUNCTION_NUM = 2

def TestFunction0(input):
    return input[:, 0]**2 + 3 * input[:, 0] + 6 * input[:, 1] \
           + input[:, 1]**3 + 7 * input[:, 2] + 1.5 * input[:, 2]**3

def TestFunction1(input):
    return input[:, 0]**2 + input[:, 1]**2 + input[:, 2]**2 + 7 * input[:, 1] \
           + 6 * input[:, 2] + input[:, 1]**3

TEST_UNIVARFUNCTION_NUM = 3
def TestUniVarFunction0(input):
    return input[:, 0]**3

def TestUniVarFunction1(input):
    return input[:, 1]**3

def TestUniVarFunction2(input):
    return input[:, 2]**3

def GetTestFunction(index = 0, multiVar = True):
    """
    From the index and multivar inputs selects the functions above.
    :param index: Index of the function requested.
    :param multiVar: If the function requestes is multivar or not.
    :return:
    """
    if multiVar:
        funcName = "TestFunction" + str(index)
    else:
        funcName = "TestUniVarFunction" + str(index)
    return globals()[funcName]


