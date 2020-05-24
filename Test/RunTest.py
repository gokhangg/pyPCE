
import sys, os
__selfPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(__selfPath))

import pyPCE.SettingsFileIO as Settings
from pyPCE.ExampleSettingsFile import*
from pyPCE.pyPCE import pyPCE as PCE

from Test.ExampleFunctions import *
import numpy as np
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
        pyPce = PCE(pceSettings)

        scenarios = pyPce.GetModelInputSamplingScenarios()
        modelOutput = TestFunction(scenarios)

        pyPce.SetModelOutput(modelOutput)
        pyPce.CalculatePceCoefficients()
        return pyPce.GetModelOutputStd(testedParamList)

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
        pceSettings = Settings.LoadSettings(settingsFile)
        pceStd = cls.GetPceStd(TestFunction, pceSettings, testedParamList)
        MonteCarloStd = cls.GetMonteCarloStd(TestFunction, pceSettings)
        return MonteCarloStd, pceStd


if __name__ == '__main__':
    unittest.main()