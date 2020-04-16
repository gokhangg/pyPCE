class Cell(object):
    def __init__(self, cell):
        self.__cell = cell

    @classmethod
    def FromList(cls, lst):
        return cls.FromListWithInitVal(lst)

    @classmethod
    def FromListWithInitVal(cls, lst, initClass = []):
       _cell = cls.__FillList(cls, lst, initClass)
       return Cell(_cell)

    def __FillList(self, dimList, initVal=[]):
        if not len(dimList) == 1:
            return self.__FillList(self, dimList[1:], [initVal for _ in range(dimList[0])])
        else:
            return [initVal for i in range(dimList[0])]

    def GetCell(self):
        return self.__cell

    def __GetItem(self, indicesTuple, cell):
        if not len(indicesTuple) == 1:
            return self.__GetItem(indicesTuple[1:], cell[indicesTuple[0]])
        else:
            return cell[indicesTuple[0]]

    def __SetItem(self, indicesTuple, cell, item):
        if not len(indicesTuple) == 1:
            return self.__GetItem(indicesTuple[1:], cell[indicesTuple[0]])
        else:
            cell[indicesTuple[0]]

    def __getitem__(self, indices):
        if not type(indices) is int:
            itemTuple = list(indices)
            itemTuple.reverse()
        else:
            itemTuple = [indices]
        return self.__GetItem(itemTuple, self.__cell)

    def __setitem__(self, indices, item):
        if not type(indices) is int:
            indicesTuple = list(indices)
            indicesTuple.reverse()
        else:
            indicesTuple = [indices]
        return self.__GetItem(indicesTuple, self.__cell)