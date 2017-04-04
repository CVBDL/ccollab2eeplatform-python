import unittest

from ccollab2eeplatform.ccollab.review_record import ReviewRecord


class TestReviewRecord(unittest.TestCase):

    def setUp(self):
        _record = [
            '88369',
            '2016-11-30 11:55 UTC',
            'pzhong',
            'Patrick Zhong',
            '0',
            '14',
            '8728',
            '162',
            '0:11:32'
        ]
        self.record = ReviewRecord(_record)
        _record_1 = [
            '88369',
            '2016-11-30 11:55 UTC',
            'pzhong',
            'Patrick Zhong',
            '0',
            '14',
            '8728',
            '162',
            '1d, 11:11:11'
        ]
        self.record_1 = ReviewRecord(_record_1)

    def test_id(self):
        self.assertEqual('88369', self.record.id)

    def test_review_creation_date(self):
        self.assertEqual('2016-11-30 11:55 UTC',
                         self.record.review_creation_date)

    def test_creator_login(self):
        self.assertEqual('pzhong', self.record.creator_login)

    def test_creator_full_name(self):
        self.assertEqual('Patrick Zhong', self.record.creator_full_name)

    def test_defect_count(self):
        self.assertEqual('0', self.record.defect_count)

    def test_comment_count(self):
        self.assertEqual('14', self.record.comment_count)

    def test_loc(self):
        self.assertEqual('8728', self.record.loc)

    def test_loc_changed(self):
        self.assertEqual('162', self.record.loc_changed)

    def test_total_person_time(self):
        self.assertEqual('0:11:32', self.record.total_person_time)

    def test_total_person_time_in_second(self):
        self.assertEqual((11 * 60 + 32),
                         self.record.total_person_time_in_second)
        self.assertEqual((1 * 24 * 60 * 60 + 11 * 60 * 60 + 11 * 60 + 11),
                         self.record_1.total_person_time_in_second)

    def test_creator_product_name(self):
        self.assertEqual('ViewPoint', self.record.creator_product_name)

    def test_review_creation_year(self):
        self.assertEqual('2016', self.record.review_creation_year)

    def test_review_creation_month(self):
        self.assertEqual('2016-11', self.record.review_creation_month)


if __name__ == '__main__':
    unittest.main()
