import unittest

from ccollab2eeplatform.ccollab.review_record import ReviewRecord
from ccollab2eeplatform.filters.creator_filter import CreatorFilter


class TestCreatorFilter(unittest.TestCase):

    def setUp(self):
        self._records = [
            ['1', '2016-11-30 11:55 UTC', 'pzhong', '', '0', '0', '0', '0', '0:00:10'],
            ['2', '2016-11-30 11:55 UTC', 'lucy', '', '0', '0', '0', '0', '0:00:10'],
            ['3', '2016-11-30 11:55 UTC', 'pzhong', '', '0', '0', '0', '0', '0:00:10'],
            ['4', '2016-11-30 11:55 UTC', 'lucy', '', '0', '0', '0', '0', '0:00:10'],
            ['5', '2016-11-30 11:55 UTC', 'pzhong', '', '0', '0', '0', '0', '0:00:10'],
            ['6', '2016-11-30 11:55 UTC', 'lily', '', '0', '0', '0', '0', '0:00:10'],
            ['7', '2016-11-30 11:55 UTC', 'pzhong', '', '0', '0', '0', '0', '0:00:10']
        ]
        self.records = [ReviewRecord(record) for record in self._records]

    def test_creator_filter(self):
        creator_filter = CreatorFilter(self.records, '')
        self.assertEqual(len(creator_filter.filter()), 7)

        creator_filter = CreatorFilter(self.records, 'pzhong')
        self.assertEqual(len(creator_filter.filter()), 4)

        creator_filter = CreatorFilter(self.records, ['pzhong'])
        self.assertEqual(len(creator_filter.filter()), 4)

        creator_filter = CreatorFilter(self.records, ['pzhong', 'lily'])
        self.assertEqual(len(creator_filter.filter()), 5)

        creator_filter = CreatorFilter(self.records,
                                       ['pzhong', 'lily', 'lucy'])
        self.assertEqual(len(creator_filter.filter()), 7)

        creator_filter = CreatorFilter(self.records)
        creator_filter.set_keywords('pzhong')
        self.assertEqual(len(creator_filter.filter()), 4)

        creator_filter = CreatorFilter(self.records, 'lily')
        creator_filter.set_keywords('pzhong')
        self.assertEqual(len(creator_filter.filter()), 4)


if __name__ == '__main__':
    unittest.main()
