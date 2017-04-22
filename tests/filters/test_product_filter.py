import unittest

from ccollab2eeplatform.ccollab.review_record import ReviewRecord
from ccollab2eeplatform.filters.product_filter import ProductFilter


class TestProductFilter(unittest.TestCase):

    def setUp(self):
        self._records = [
            ['1', '2016-11-30 11:55 UTC', 'pzhong', '', '0', '0', '0', '0', '0:00:10'],
            ['2', '2016-11-30 11:55 UTC', 'rli1', '', '0', '0', '0', '0', '0:00:10'],
            ['3', '2016-11-30 11:55 UTC', 'pzhong', '', '0', '0', '0', '0', '0:00:10'],
            ['4', '2016-11-30 11:55 UTC', 'yyyang', '', '0', '0', '0', '0', '0:00:10'],
            ['5', '2016-11-30 11:55 UTC', 'pzhong', '', '0', '0', '0', '0', '0:00:10']
        ]
        self.records = [ReviewRecord(record) for record in self._records]

    def test_product_filter(self):
        product_filter = ProductFilter(None)
        self.assertEqual(product_filter.filter(), None)

        product_filter = ProductFilter(self.records)
        self.assertEqual(len(product_filter.filter()), 5)

        product_filter = ProductFilter(self.records, None)
        self.assertEqual(len(product_filter.filter()), 5)

        product_filter = ProductFilter(self.records, 'ViewPoint')
        self.assertEqual(len(product_filter.filter()), 4)

        product_filter = ProductFilter(self.records, 'FTView')
        self.assertEqual(len(product_filter.filter()), 1)

        product_filter = ProductFilter(self.records, ['ViewPoint', 'FTView'])
        self.assertEqual(len(product_filter.filter()), 5)

        product_filter = ProductFilter(self.records)
        product_filter.set_keywords('ViewPoint')
        self.assertEqual(len(product_filter.filter()), 4)

        product_filter = ProductFilter(self.records, 'FTView')
        product_filter.set_keywords('ViewPoint')
        self.assertEqual(len(product_filter.filter()), 4)


if __name__ == '__main__':
    unittest.main()
