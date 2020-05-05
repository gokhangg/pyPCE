from Basis.CreateBasis import *
from Cubatures.CalculateCoefficients import *
from SettingsFileIO.Settings import *
from Test.ExampleFunctions import *
from Cubatures.Cubatures import *
from Evaluation.StandartDeviations import *
from ExampleSettingsFile import*

import unittest

MONTECARLO_SAMPLESIZE = 200000
TEST_EQUALITYRATIO_DELTA = 4e-2

class TestPCE(unittest.TestCase):

    def test_stdMultiVarFunctions(self):
        MULTIVAR = True
        print("\n\nMultivar Functions")
        for settingsIndex in range(SETTINGSFILE_NUM):
            for functionIndex in range(TEST_MULTIVARFUNCTION_NUM):
                print("TEST SETTINGS FILE:", settingsIndex)
                print("TEST FUNCTION:", functionIndex)
                MonteCarloStd, pceStd = self.TestCase(settingsIndex, functionIndex, MULTIVAR)
                print("MC result:  ", MonteCarloStd, "PCE result: ", pceStd)
                """
                MonteCarlo std and PCE std should be equal.
                """
                self.assertAlmostEqual(MonteCarloStd / pceStd, 1, delta = TEST_EQUALITYRATIO_DELTA)

    def test_stdUniFunctions(self):
        MULTIVAR = False
        print("\n\nUnivar Functions")
        for settingsIndex in range(SETTINGSFILE_NUM):
            for functionIndex in range(TEST_UNIVARFUNCTION_NUM):
                print("TEST SETTINGS FILE:", settingsIndex)
                print("TEST FUNCTION:", functionIndex)
                MonteCarloStd, pceStd = self.TestCase(settingsIndex, functionIndex, MULTIVAR, [functionIndex])
                print("MC result: ", MonteCarloStd, "PCE result: ", pceStd)
                """
                MonteCarlo std and PCE std should be equal.
                """
                self.assertAlmostEqual(MonteCarloStd / pceStd, 1, delta = TEST_EQUALITYRATIO_DELTA)

    @staticmethod
    def GetPceStd(TestFunction, pceSettings, testedParamList):
        pceSettings.basis, pceSettings.norm = CreateBasisPC(pceSettings)
        cubature = Cubatures(pceSettings)
        modelOutput = TestFunction(cubature.scenariosScaled)
        pceSettings.coeffs = CalculateCoefficients(modelOutput, pceSettings, cubature)
        return GetCrossStandardDeviation(pceSettings, testedParamList)

    @staticmethod
    def GetMonteCarloStd(TestFunction, pceSettings):
        scenarios = np.random.randn(MONTECARLO_SAMPLESIZE, len(pceSettings.sDeviations)).dot(np.diag(pceSettings.sDeviations))
        samples = TestFunction(scenarios)
        return samples.std()

    @classmethod
    def TestCase(cls, settingsIndex = 0, functionIndex = 0, multiVar = True, testedParamList = []
                 ):
        TestFunction = GetTestFunction(functionIndex, multiVar)
        settingsFile = GetExampleSettingsFile(settingsIndex)
        pceSettings = LoadSettings(settingsFile)
        pceStd = cls.GetPceStd(TestFunction, pceSettings, testedParamList)
        MonteCarloStd = cls.GetMonteCarloStd(TestFunction, pceSettings)
        return MonteCarloStd, pceStd


if __name__ == '__main__':
    unittest.main()