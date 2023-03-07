import unittest
from Sorting.sorting_methods import SortingMethods


class SortingTests(unittest.TestCase):

    def setUp(self):
        self.arr = [5, 7, 3, 9, 15, 1, 0, 39]

    def test_insertion_sort(self):

        self.arr = SortingMethods.InsertionSort(self.arr, reversed=False)
        self.assertEqual(self.arr, [0, 1, 3, 5, 7, 9, 15, 39])

    def test_comb_sort(self):
        self.arr = SortingMethods.CombSort(self.arr, reversed=False)
        self.assertEqual(self.arr, [0, 1, 3, 5, 7, 9, 15, 39])

