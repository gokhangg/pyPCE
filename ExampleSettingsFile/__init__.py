import os

SETTINGSFILE_NUM = 1

selfPath = os.path.dirname(os.path.realpath(__file__))

def GetExampleSettingsFile(index = 0):
    return selfPath + "/ExampleSettings" + str(index) + ".json"