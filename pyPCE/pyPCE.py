from Basis.CreateBasis import CreateBasisPC
from Cubatures.Cubatures import Cubatures
from Cubatures.CalculateCoefficients import CalculateCoefficients
import __Evaluation as Evaluation


class pyPCE(object):

    def __init__(self, pceSettings):
        self.__pceSettings = pceSettings
        self.__pceSettings.basis, self.__pceSettings.norm = CreateBasisPC(self.__pceSettings)
        self.__cubature = Cubatures(self.__pceSettings)

    def GetModelInputSamplingScenarios(self):
        return self.__cubature.scenariosScaled

    def SetModelOutput(self, modelOutput):
        self.__modelOutput = modelOutput

    def CalculatePceCoefficients(self):
        self.__pceSettings.coeffs = CalculateCoefficients(self.__modelOutput, self.__pceSettings, self.__cubature)

    def GetModelOutputStd(self, scenarioList):
        return Evaluation.GetCrossStandardDeviation(self.__pceSettings, scenarioList)

    def EvaluatePceModel(self, scenario):
        return Evaluation.EvaluatePce(self.__pceSettings, scenario)