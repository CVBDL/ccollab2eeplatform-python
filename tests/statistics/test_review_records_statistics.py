from unittest.mock import MagicMock
import unittest

from ccollab2eeplatform.ccollab.review_record import ReviewRecord
from ccollab2eeplatform.settings.users_settings import UsersSettings
from ccollab2eeplatform.statistics.review_records_statistics import (
    ReviewRecordsStatistics
)


class TestReviewRecordsStatistics(unittest.TestCase):

    def setUp(self):
        # Mocks
        self.login_names = ['rli1', 'pzhong', 'trang', 'mmo2']
        UsersSettings.list_login_names = MagicMock(
            return_value=self.login_names)

        self._records = [
            ['1', '2017-03-11 11:55 UTC', 'pzhong', '', '0', '0', '0', '0', '0:00:10'],
            ['2', '2017-03-02 11:55 UTC', 'rli1', '', '0', '0', '0', '0', '0:00:10'],
            ['3', '2017-02-11 11:55 UTC', 'trang', '', '0', '0', '0', '0', '0:00:10'],
            ['4', '2017-01-15 11:55 UTC', 'trang', '', '0', '0', '0', '0', '0:00:10'],
            ['5', '2016-11-15 11:55 UTC', 'pzhong', '', '0', '0', '0', '0', '0:00:10'],
            ['6', '2016-09-09 11:55 UTC', 'trang', '', '0', '0', '0', '0', '0:00:10'],
            ['7', '2016-09-01 11:55 UTC', 'trang', '', '0', '0', '0', '0', '0:00:10']
        ]
        self.records = [ ReviewRecord(record) for record in self._records ]
        self.stat = ReviewRecordsStatistics(self.records)

    def test_calc_review_count_by_month(self):
        schema, data = self.stat.calc_count_by_month()
        self.assertEqual(schema, [('Month', 'string'), ('Count', 'number')])
        self.assertEqual(
            data,
            [
                ['2016-09', 2],
                ['2016-11', 1],
                ['2017-01', 1],
                ['2017-02', 1],
                ['2017-03', 2],
            ]
        )


if __name__ == '__main__':
    unittest.main()
