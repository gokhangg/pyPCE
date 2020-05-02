import numpy as np
from Basis.Utilities import *
from Polynomials.Hermite import *


from pce import *

def GetPolynomialResults(input, uPolOrders, polType):
    if polType == "hermite":
        return Hermite(input, uPolOrders)
    elif polType == "legendre":
        pass
    elif polType == "laguarre":
        pass
    elif polType == "jacobi":
        pass
    else:
        assert("Unknown polynomial type.")



def CalculatePolynomials(pce, cubature):
    polTypes = pce.polTypes
    polOrders = pce.basis
    scenarios = np.transpose(cubature.scenarios)
    uPolTypes, iUPolTypes = StringUnique(polTypes)
    nUPolTypes = uPolTypes.shape[0]
    nPolOrder = polOrders.shape[0]
    nScenarios = scenarios.shape[1]
    polynomialValue = np.zeros([nPolOrder, nScenarios, nUPolTypes])
    for ind in range(nUPolTypes):
        lICurPolOrd = iUPolTypes == ind
        nCurPols = lICurPolOrd.sum()
        curPolOrders = polOrders[:, lICurPolOrd]
        uCurPolOrders = np.unique(curPolOrders)
        polynomialOutput = GetPolynomialResults(scenarios[lICurPolOrd, :], np.array(uCurPolOrders, dtype = "uint32"), uPolTypes[ind])
    return polynomialOutput


def CalculateCoefficients(modelOutput, pce, cubature):
    polValues = CalculateCoefficients(pce, cubature)