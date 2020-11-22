import numpy as np

def GetSelectedIndices(basis, scenariosList):
    """
    Generates index vector given the desired parameters to be analysis.
    :param basis: Matrix from which the return vector will be extracted.
    :param scenarioList: List containing for which standard deviation will be computed.
    :return: Index vector.
    """
    scenariosList.sort()
    checklist = np.zeros(basis.shape[1], dtype = np.bool)
    checklist[scenariosList] = True
    return ((basis > 0) == checklist).prod(1) > 0


def GetCrossStandardDeviation(pceSettings, scenarioList = []):
    """
    Returns standard deviation vector given the scenarios list.
    :param pceSettings: Constructed PCE settings.
    :param scenarioList: List of parameter
    :return: Standard deviation vector.
    """
    if len(scenarioList) == 0:
        return np.array(np.sqrt((pceSettings.coeffs[:, 1:] ** 2).dot(pceSettings.norm[1:])), dtype="float32")

    scenarioList = np.array(scenarioList)
    scenarioListLen = scenarioList.shape[0]
    basis = pceSettings.basis
    if (scenarioListLen > basis.shape[0]) and (scenarioListLen.max() > basis.shape[0]):
        assert("Requested scenarios and basis shape mismatch.")

    selectionVector = GetSelectedIndices(basis, scenarioList)
    return np.sqrt((pceSettings.coeffs[:, selectionVector] ** 2).dot(pceSettings.norm[selectionVector]))
