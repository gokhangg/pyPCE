



class pyPCE(object):

    def __init__(self, pceSettings):
        self.__pceSettings = pceSettings
        self.__pceSettings.basis, self.__pceSettings.norm = CreateBasisPC(self.__pceSettings)
        self.__cubature = Cubatures(self.__pceSettings)