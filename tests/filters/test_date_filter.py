import unittest

from ccollab2eeplatform.ccollab.review_record import ReviewRecord
from ccollab2eeplatform.filters.date_filter import DateFilter


class TestDateFilter(unittest.TestCase):

    def setUp(self):
        self._records = [
            ['1', '2017-02-11 11:55 UTC', 'pzhong', '', '0', '0', '0', '0', '0:00:10'],
            ['2', '2017-02-01 11:55 UTC', 'lucy', '', '0', '0', '0', '0', '0:00:10'],
            ['3', '2016-12-30 11:55 UTC', 'pzhong', '', '0', '0', '0', '0', '0:00:10'],
            ['4', '2016-02-30 11:55 UTC', 'lucy', '', '0', '0', '0', '0', '0:00:10'],
            ['5', '2016-02-22 11:55 UTC', 'pzhong', '', '0', '0', '0', '0', '0:00:10'],
            ['6', '2016-02-01 11:55 UTC', 'pzhong', '', '0', '0', '0', '0', '0:00:10']
        ]
        self.records = [ReviewRecord(record) for record in self._records]

    def test_creator_filter(self):
        date_filter = DateFilter(None)
        self.assertEqual(date_filter.filter(), [])

        date_filter = DateFilter(self.records)
        self.assertEqual(len(date_filter.filter()), 6)

        date_filter = DateFilter(self.records, '')
        self.assertEqual(len(date_filter.filter()), 6)

        date_filter = DateFilter(self.records, keywords='2018-12-30')
        self.assertEqual(len(date_filter.filter()), 0)

        date_filter = DateFilter(self.records, keywords='2016-12-30')
        self.assertEqual(len(date_filter.filter()), 1)
        date_filter = DateFilter(self.records, keywords='2016-12')
        self.assertEqual(len(date_filter.filter()), 1)
        date_filter = DateFilter(self.records, keywords='2016-12-30', rule='DAY')
        self.assertEqual(len(date_filter.filter()), 1)
        date_filter = DateFilter(self.records, keywords='2016-12-30', rule='MONTH')
        self.assertEqual(len(date_filter.filter()), 1)
        date_filter = DateFilter(self.records, keywords='2016-12-30', rule='year')
        self.assertEqual(len(date_filter.filter()), 4)

        date_filter = DateFilter(self.records, keywords='2017-02-01')
        self.assertEqual(len(date_filter.filter()), 2)
        date_filter = DateFilter(self.records, keywords='2017-02-01', rule='DAY')
        self.assertEqual(len(date_filter.filter()), 1)
        date_filter = DateFilter(self.records, keywords='2017-02-01', rule='MONTH')
        self.assertEqual(len(date_filter.filter()), 2)
        date_filter = DateFilter(self.records, keywords='2017-02-01', rule='year')
        self.assertEqual(len(date_filter.filter()), 2)


if __name__ == '__main__':
    unittest.main()
