

class SortingMethods:
    @staticmethod
    def __Compare(a, b, reversed):
        if reversed == False:
            return a < b
        if reversed == True:
            return a > b

    @staticmethod
    def InsertionSort(list, reversed=False, key=None, cmp=None):
        if cmp is not None and key is not None:
            raise Exception("Conflicting criteria")

        if cmp is None:
            cmp = SortingMethods.__Compare
        if reversed is not True and reversed is not False:
            raise Exception("Invalid reversed state.")

        if key == None:
            key = lambda x: x

        for i in range(1, len(list)):
            curr_element = list[i]

            j = i - 1
            while j >= 0 and cmp(key(curr_element), key(list[j]), reversed) == True:
                list[j + 1] = list[j]
                j = j - 1

            list[j + 1] = curr_element

        return list

    @staticmethod
    def CombSort(list, reversed=False, key=None, cmp=None):
        if cmp is not None and key is not None:
            raise Exception("Conflicting criteria")

        if reversed is not True and reversed is not False:
            raise Exception("Invalid reversed state.")

        if cmp is None:
            cmp = SortingMethods.__Compare

        if key == None:
            key = lambda x: x

        length = len(list)
        shrink = 1.3
        gap = length
        sorted = False

        while not sorted:
            gap = int(gap / shrink)

            if gap <= 1:
                sorted = True
                gap = 1

            for i in range(length - gap):
                j = gap + i
                if cmp(key(list[j]), key(list[i]), reversed) == True:
                    list[i], list[j] = list[j], list[i]
                    sorted = False

        return list