import unittest
import lianliankan as llk

class TestLianLianKan(unittest.TestCase):
    def test_normal_cases(self):
        test_cases = [
            ([[0,0,0,2,0,0,0],
            [0,0,0,2,1,0,0],
            [0,0,0,2,0,0,0],
            [0,0,0,2,0,0,0],
            [0,0,0,2,2,0,0],
            [0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0]], [(5,1),(1,4)], [(5, 1), (5, 5), (1, 5), (1, 4)]),

            ([[0,0,0,2,0,0,0],
            [0,0,0,2,1,0,0],
            [0,0,0,2,0,0,0],
            [0,0,0,2,0,0,0],
            [0,0,0,2,0,0,0],
            [0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0]], [(5,1),(1,4)], [(5, 1), (5, 4), (1, 4)]),

            ([[0,0,0,2,0,0,0],
            [0,0,0,2,1,0,0],
            [0,0,0,2,0,0,0],
            [0,0,0,2,0,0,0],
            [0,0,0,2,0,0,0],
            [0,1,0,0,2,0,0],
            [0,0,0,0,0,0,0]], [(5,1),(1,4)], False),

            ([[0,0,0,2,0,0,0],
            [0,0,0,2,1,0,0],
            [0,0,0,2,0,0,0],
            [0,0,0,2,0,0,0],
            [0,0,0,2,0,0,0],
            [0,1,0,2,0,0,0],
            [0,0,0,0,0,0,0]], [(5,1),(1,4)], [(5, 1), (6, 1), (6, 4), (1, 4)]),

            ([[0,0,0,2,0,0,0],
            [0,0,0,2,1,0,0],
            [0,0,0,2,0,0,0],
            [0,0,0,2,0,0,0],
            [0,0,0,2,0,0,0],
            [0,1,0,2,0,0,0],
            [0,0,0,0,0,0,0]], [(2,3),(1,4)], [(2, 3), (2, 4), (1, 4)]),

        ]
        for test_case in test_cases:
            map, (start, end), result = test_case
            self.assertEqual( llk.checkllk(map, start, end), result)

if __name__ == '__main__':
    unittest.main()
