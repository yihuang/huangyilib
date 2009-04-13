#!/usr/bin/env python
# coding: utf-8
import unittest
import solution

class TestSolution(unittest.TestCase):

    def test_simple_cases(self):
        simple_cases = [
                ['''3 4 
- - - - 
- * - - 
- * - - 
0 1''', '0 1 No\n'],
                ['''3 4 
- - - - 
- * - * 
- * - - 
1 0''', '1 0 Yes\n'],
                ['''3 4 
- - - - 
- * - * 
- * - - 
1 2''', '1 2 No\n'],
                ['''1 4 
- - - - 
0 1''', '0 1 No\n'],
                ['''5 4 
- - - - 
* * * - 
- - - - 
- - * * 
- - - - 
3 1''', '3 1 Yes\n'],
                ['''5 4 
- - - - 
* * * - 
- - - - 
- * * * 
- - - - 
3 0''', '3 0 No\n']
        ]
        from StringIO import StringIO
        for input, output in simple_cases:
            outfile = StringIO()
            solution.main(StringIO(input), outfile)
            self.assertEqual(outfile.getvalue(), output)

    def test_complicate_cases(self):
        pass # TODO

if __name__ == '__main__':
    unittest.main()
