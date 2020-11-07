from Utilities.Utilities import *
from Polynomials.Hermite import Hermite
from Polynomials.Legendre import Legendre
from Polynomials.Laguerre import Laguerre
import numpy as np

def GetPolynomialResults(input, uPolOrders, polType):
    """
    Constructs polynomial sub units for polynomial base to for the parameter evaluation.
    :param input: Cubature scenarios for which the polynomials are evaluated.
                    It has N x M shape where N and M are scenarios size and number
                    of parameters analyzed respectively.
    :param uPolOrders: Indicates polynomial orders for which the results are obtained.
    :param polType: Indicates which type of polynomials will be constructed.
    :return:
    """
    if polType == "hermite":
        return Hermite(input, uPolOrders)
    elif polType == "legendre":
        return Legendre(input, uPolOrders)
    elif polType == "laguerre":
        return Laguerre(input, uPolOrders)
    elif polType == "jacobi":
        pass
    else:
        assert("Unknown polynomial type.")

def CalculatePolynomials(polTypes, polOrders, scenarios):
    """
    Constructs polynomial base to for the parameter evaluation.
    :param pceSettings: pce settings class including data for the all performance.
    :param cubature: Previously constructed cubature.
    :return: Constructed polynomial base for PCE parameter estimation. 
    """
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
        polynomialOutput = GetPolynomialResults(scenarios[lICurPolOrd, :], uCurPolOrders, uPolTypes[ind])
        polOutSize = polynomialOutput.shape
        iPolType = RepMat(np.arange(nCurPols) + 1, [1, nPolOrder, nScenarios])
        iPolOrder = RepMat(curPolOrders + 1, [1,1, nScenarios])
        iScenarios = RepMat(np.arange(nScenarios) + 1, [1, nPolOrder, nCurPols])
        iScenarios = iScenarios.transpose(np.flip(np.arange(len(iScenarios.shape))))
        iCurToFull = Sub2Ind(polOutSize, iPolType, iPolOrder, iScenarios)
        polynomialValue[:, :, ind] = np.transpose(polynomialOutput, [2, 1, 0]).reshape(-1)[iCurToFull-1].prod(0)
    return polynomialValue.prod(2)

def CalculateCoefficients(modelOutput, pceSettings, cubature):
    """
    Given the model output whose input parameters are analyzed, it estimates
    PCE parameters.
    :param modelOutput: Output of a model analyzed.
    :param pceSettings: pce settings class including data for the all performance.
    :param cubature: Previously constructed cubature.
    :return: Estimates PCE parameters.
    """
    polValues = CalculatePolynomials(pceSettings.polTypes, pceSettings.basis,  np.transpose(cubature.scenarios))
    coefficients = np.true_divide(modelOutput.dot(np.transpose(polValues * cubature.totalWeights)), pceSettings.norm)
    if pceSettings.removeSmallElements:
        coefficients[np.abs(coefficients) < pceSettings.smallElementThreshold] = 0.
    if len(coefficients.shape) == 1:
        coefficients = coefficients.reshape([1, coefficients.shape[0]])
    return coefficients