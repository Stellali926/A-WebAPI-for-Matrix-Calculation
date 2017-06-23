import matrixAPI as w3
import requests
import unittest

class testmatrixAPI(unittest.TestCase):
    matrixA={'numrows':3,'numcols':3,'matrixdata':[[1,1,1],[2,2,2],[3,3,3]]}
    matrixB={'numrows':3,'numcols':3,'matrixdata':[[1,2,3],[4,5,6],[7,8,9]]}
    matrixC={'numrows':3,'numcols':2,'matrixdata':[[1,2],[3,4],[5,6]]}
    w3.matrices['A'] = matrixA
    w3.matrices['B'] = matrixB
    w3.matrices['C'] = matrixC

    def test_welcom_page(self):
        response = requests.get('http://127.0.0.1:8080/')
        self.assertEqual(response.status_code, 200)

    #Test add function
    def test_add_func1(self):
        w3.add("D",testmatrixAPI.matrixA,testmatrixAPI.matrixB)
        self.assertEqual(w3.matrices['D']['matrixdata'],[[2, 3, 4], [6, 7, 8], [10, 11, 12]])
    def test_add_func2(self):
        self.assertEqual(w3.matrices['D']['numrows'],3)
    def test_add_func3(self):
        self.assertEqual(w3.matrices['D']['numcols'],3)

    #Test subtraction function
    def test_subtraction_func1(self):
        w3.subtraction("E",testmatrixAPI.matrixA,testmatrixAPI.matrixB)
        self.assertEqual(w3.matrices['E']['matrixdata'],[[0, -1, -2], [-2, -3, -4], [-4, -5, -6]])
    def test_subtraction_func2(self):
        self.assertEqual(w3.matrices['E']['numrows'],3)
    def test_subtraction_func3(self):
        self.assertEqual(w3.matrices['E']['numcols'],3)

    #Test multiplication funciton
    def test_multiplication_func1(self):
        w3.multiplication("G",testmatrixAPI.matrixA,testmatrixAPI.matrixC)
        self.assertEqual(w3.matrices['G']['matrixdata'],[[9,12],[18,24],[27,36]])
    def test_multiplication_func2(self):
        self.assertEqual(w3.matrices['G']['numrows'],3)
    def test_multiplication_func3(self):
        self.assertEqual(w3.matrices['G']['numcols'],2)

if __name__ == "__main__":
    unittest.main()


'''
UNITTEST RESULT:

..........
----------------------------------------------------------------------
Ran 10 tests in 0.016s

OK
'''