import pyPCE.__Cubatures.CalculateCoefficients as CalCoeff
import numpy as np

def EvaluatePce(pceSettings, scenarios_):
    scenarios = np.copy(scenarios_)
    scenarios = scenarios.dot(np.diag(1. / np.array(pceSettings.sDeviations)))
    polVal = CalCoeff.CalculatePolynomials(pceSettings.polTypes, pceSettings.basis, np.transpose(scenarios))
    return pceSettings.coeffs.dot(polVal)