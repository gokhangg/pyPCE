from CreateBasis import *
from GetErrorScenerios import *

class pceSettings:
    pass


pceSettings.polOrder = 4
pceSettings.gridLevel = 3
pceSettings.quadratureType = ["gauss-hermite", "gauss-hermite", "gauss-hermite"]
pceSettings.polTypes = ["hermite", "hermite", "hermite"]
pceSettings.trim =  True
pceSettings.removeSmallElements = True
pceSettings.smallElementThreshold = 1e-7
pceSettings.gridType = "sparse"
pceSettings.sDeviations = [0.5, 1.5, 1.5]

class pce(object):
    pass


pce.sDeviations = pceSettings.sDeviations
pce.polTypes = pceSettings.polTypes
pce.quadratureType = pceSettings.gridType

pce.basis, pce.norm = CreateBasisPC(pce, pceSettings)

cubature = GetErrorScenerios(pceSettings)


