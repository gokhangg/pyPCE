from Utilities.Utilities import *


class Quadratures(object):
    """
    Quadrature class contains several containers used in the calculation of Gaussian quadrature integration nodes,
    integration weights and their sparse forms. These containers then will be used in further PCE computations.
    """
    def __init__(self, gridLevel, quadratureTypes):
        self.__nTypes = len(quadratureTypes)
        self.__gridLevel = gridLevel
        self.quadratureTypes = quadratureTypes
        self.nodes = np.ndarray([self.__nTypes, self.__gridLevel], dtype = object)
        self.weights = np.ndarray([self.__nTypes, self.__gridLevel], dtype = object)
        self.sparseNodes = np.ndarray([self.__nTypes, self.__gridLevel], dtype = object)
        self.sparseWeights = np.ndarray([self.__nTypes, self.__gridLevel], dtype = object)
        self.__GetQuadratures()

    def __QuadratureFunction(self, quadratureType):
        """
        As per the qudratute type, returns the relevant quadrature creation function.
        :param quadratureType: String denoting the quadrature type.
        :return: Quadrature function.
        """
        if quadratureType == "gauss-hermite":
            return self.__GaussHermiteQuadrature
        elif quadratureType == "gauss-legendre":
            return self.__GaussLegendreQuadrature
        elif quadratureType == "gauss-laguerre":
            return self.__GaussLaguerreQuadrature
        else:
            assert("Invalid quadrature type.")

    def __CalculateQuadrature(self, quadFunct):
        """
        Used in the calculation of the selected quadrature function.
        :param quadFunct: Quadrature function to be calculated.
        :return: Created node and weights.
        """
        nodes = np.ndarray([1, self.__gridLevel], dtype = object)
        weights = np.ndarray([1, self.__gridLevel], dtype = object)
        for ind in range(self.__gridLevel):
            nodes[0, ind], weights[0, ind] = quadFunct(2 * ind + 1)
        return nodes, weights

    def __GetSparseNodesAndWeights(self, index):
        """
        Creates sparse node and its weights.
        :param index: Dimension index.
        :return: Sparse node and weights.
        """
        szY = self.nodes.shape[1]
        sparceNodes = np.ndarray([1, szY], dtype = object)
        sparceWeights = np.ndarray([1, szY], dtype = object)
        sparceNodes[0, 0] = np.copy(self.nodes[index, 0])
        sparceWeights[0, 0] = np.copy(self.weights[index, 0])
        for ind in range(1, szY):
            sparceNodes[0, ind], nodeIndices = Unique(np.append(self.nodes[index, ind], self.nodes[index, ind - 1]))
            sparceWeights[0, ind] = AccumArray(np.array(nodeIndices), np.append(self.weights[index, ind], -self.weights[index, ind - 1]))
        return sparceNodes, sparceWeights

    def __GetQuadratures(self):
        """
        Createst the entire quadratures.
        :return: __Quadratures.
        """
        for ind, it in enumerate(self.quadratureTypes):
            quadFunct = self.__QuadratureFunction(it)
            self.nodes[ind, :], self.weights[ind, :] = self.__CalculateQuadrature(quadFunct)
            self.sparseNodes[ind, :], self.sparseWeights[ind, :] = self.__GetSparseNodesAndWeights(ind)

    @staticmethod
    def __GaussHermiteQuadrature(level):
        """
        Creates Gauss-Hermite quadrature rule.
        :param level: Level of the quadrature to be created.
        :return: Gauss-Hermite quadrature rule
        """
        level = int(level)
        vect = np.sqrt(range(1, level), dtype='float')
        matrix = np.diag(vect, k=-1) + np.diag(vect, k=1)
        w, v = np.linalg.eigh(matrix)
        indices = np.argsort(w)
        nodes = np.sort(w)
        if not level % 2 == 0:
            nodes[int((level - 1) / 2)] = 0
        return nodes, v[0, indices] ** 2

    @staticmethod
    def __GaussLegendreQuadrature(level):
        """
        Creates Gauss-Legendre quadrature rule.
        :param level: Level of the quadrature to be created.
        :return: Gauss-Legendre quadrature rule
        """
        i = np.arange(1, level)
        b = np.sqrt((i ** 2) / ((4 * i ** 2) - 1))
        companionMat = np.diag(b, -1) + np.diag(b, 1)
        w, v = np.linalg.eigh(companionMat)
        sortIndex = w.argsort()
        w.sort()
        if not level % 2 == 0:
            w[int((level - 1) / 2)] = 0
        return w, np.transpose(v[0, sortIndex] ** 2)

    @staticmethod
    def __GaussLaguerreQuadrature(level, alpha=0):
        """
        Creates Gauss-Laguerre quadrature rule.
        :param level: Level of the quadrature to be created.
        :param alpha: Alpha value which may not be used.
        :return: Gauss-Laguerre quadrature rule
        """
        i = np.arange(1, level + 1)
        a = 2 * i - 1 + alpha
        b = np.sqrt(i * (i + alpha))[np.arange(level - 1)]
        companionMat = np.diag(b, -1) + np.diag(b, 1) + np.diag(a, 0)
        w, v = np.linalg.eigh(companionMat)
        sortIndex = w.argsort()
        w.sort()
        return w, np.transpose(v[0, sortIndex] ** 2)