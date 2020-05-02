from CreateBasis import *
from GetErrorScenerios import *
from CalculateCoefficients import *

class pceSettings:
    pass

pceSettings.polOrder = 4
pceSettings.gridLevel = 3
pceSettings.quadratureType = ["gauss-hermite", "gauss-legendre", "gauss-laguerre"]
pceSettings.polTypes = ["hermite", "laguerre", "laguerre"]
pceSettings.trim = True
pceSettings.removeSmallElements = True
pceSettings.smallElementThreshold = 1e-9
pceSettings.gridType = "sparse"
pceSettings.sDeviations = [0.5, 1.5, 1.5]

class pce(object):
    pass


pce.sDeviations = pceSettings.sDeviations
pce.polTypes = pceSettings.polTypes
pce.quadratureType = pceSettings.gridType

pceSettings.basis, pceSettings.norm = CreateBasisPC(pce, pceSettings)


cubature = Cubatures(pceSettings)

def TestFunction(input):
    return input[:, 0]**2 + 3 * input[:, 0] + 6 * input[:, 1] + input[:, 1]**3 + 7 * input[:, 2] + 1.5 * input[:, 2]**3;

modelOutput = TestFunction(cubature.scenariosScaled)
modelOutput = np.array(modelOutput, dtype="float")
modelOutput = np.tile(modelOutput, [1024*1024,1])
pce.coeffs = EvaluateCoefficients(modelOutput, pceSettings, cubature)

print(pce.coeffs[0])