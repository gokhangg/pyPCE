import json

class pceSettings:
    pass

def LoadSettings(fileName):
    with open(fileName) as fl:
        data = json.load(fl)
    pceSettings.polOrder = int(data["pol_order"])
    pceSettings.gridLevel = int(data["grid_level"])
    pceSettings.quadratureType = data["quadrature_type"]
    pceSettings.polTypes = data["pol_type"]
    pceSettings.trim = bool(data["trim"])
    pceSettings.removeSmallElements = bool(data["remove_small_elements"])
    pceSettings.smallElementThreshold = float(data["small_element_threshold"])
    pceSettings.gridType = data["grid_type"]
    pceSettings.sDeviations = data["std_devs"]
    for ind in range(len(pceSettings.sDeviations)):
        pceSettings.sDeviations[ind] = float(pceSettings.sDeviations[ind])
    return pceSettings





