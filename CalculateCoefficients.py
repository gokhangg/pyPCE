import numpy as np
from Basis.Utilities import *

def CalculatePolynomials(pce, cubature):
    polTypes = pce.polType
    polOrders = pce.polOrders
    scenarios = cubature.scenarios
    uPolTypes = np.unique(polTypes)
    nPolOrder = polOrders.shape[0]
    nScenarios = scenarios.shape[1]
    nUPolTypes = uPolTypes.shape[0]
    polynomialValue = np.zeros([nPolOrder, nScenarios, nUPolTypes])
    for ind in range(nUPolTypes):
        lUPolType = uPolTypes == polTypes[ind]



def CalculateCoefficients(modelOutput, pce, cubature):
    polValues = CalculateCoefficients(pce, cubature)