import unittest
from itertools import groupby

from ccollab2eeplatform import utils


class TestUtils(unittest.TestCase):

    def test_to_isoformat(self):
        self.assertEqual(utils.to_isoformat('2017-1-1'), '2017-01-01')
        self.assertEqual(utils.to_isoformat('2017-1-11'), '2017-01-11')
        self.assertEqual(utils.to_isoformat('2017-11-1'), '2017-11-01')
        self.assertEqual(utils.to_isoformat('2017-11-11'), '2017-11-11')
        self.assertEqual(utils.to_isoformat('2017-1-1-1'), '2017-01-01')

        def invalid_params_0():
            utils.to_isoformat(None)
        self.assertRaises(Exception, invalid_params_0)

        def invalid_params_1():
            utils.to_isoformat('')
        self.assertRaises(Exception, invalid_params_1)

        def invalid_params_2():
            utils.to_isoformat('2017-1')
        self.assertRaises(Exception, invalid_params_2)

    def test_month_range(self):
        self.assertEqual(
            utils.month_range('2017-02', '2017-02'),
            ['2017-02']
        )
        self.assertEqual(
            utils.month_range('2017-01', '2017-02'),
            ['2017-01', '2017-02']
        )
        self.assertEqual(
            utils.month_range('2017-10', '2017-12'),
            ['2017-10', '2017-11', '2017-12']
        )
        self.assertEqual(
            utils.month_range('2016-10', '2017-02'),
            ['2016-10', '2016-11', '2016-12', '2017-01', '2017-02']
        )
        self.assertEqual(
            utils.month_range('2017-02', '2016-10'),
            ['2017-02', '2017-01', '2016-12', '2016-11', '2016-10']
        )
        self.assertEqual(
            utils.month_range('2017-02', '2017-01'),
            ['2017-02', '2017-01']
        )

    def test_groupby(self):
        # Setup
        iterable = ['lucy', 'rose', 'lily']

        # Case
        groups = []
        uniquekeys = []
        for k, g in utils.groupby(iterable):
            groups.append(list(g)[0])
            uniquekeys.append(k)
        self.assertEqual(['lily', 'lucy', 'rose'], uniquekeys)
        self.assertEqual(['lily', 'lucy', 'rose'], groups)

        # Case
        groups = []
        uniquekeys = []
        for k, g in utils.groupby(iterable, reverse=True):
            groups.append(list(g)[0])
            uniquekeys.append(k)
        self.assertEqual(list(reversed(['lily', 'lucy', 'rose'])), uniquekeys)
        self.assertEqual(list(reversed(['lily', 'lucy', 'rose'])), groups)

        # Case
        groups = []
        uniquekeys = []
        for k, g in utils.groupby(iterable, key=lambda val: val[1]):
            groups.append(list(g)[0])
            uniquekeys.append(k)
        self.assertEqual(['i', 'o', 'u'], uniquekeys)
        self.assertEqual(['lily', 'rose', 'lucy'], groups)

        # Case
        groups = []
        uniquekeys = []
        for k, g in utils.groupby(iterable, key=lambda val: val[1], reverse=True):
            groups.append(list(g)[0])
            uniquekeys.append(k)
        self.assertEqual(list(reversed(['i', 'o', 'u'])), uniquekeys)
        self.assertEqual(list(reversed(['lily', 'rose', 'lucy'])), groups)

    def test_lower(self):
        @utils.lower
        def return_FOO():
            return 'FOO'
        self.assertEqual('foo', return_FOO())


if __name__ == '__main__':
    unittest.main()
