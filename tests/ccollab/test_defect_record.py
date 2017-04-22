import unittest

from ccollab2eeplatform.ccollab.defect_record import DefectRecord


class TestDefectRecord(unittest.TestCase):

    def setUp(self):
        _record = [
            '137236',
            '85639',
            '2016-11-16 11:21 UTC',
            'pzhong',
            'Patrick Zhong',
            'Major',
            'algorithm/logic',
            'Not Evaluated'
        ]
        self.record = DefectRecord(_record)

    def test_defect_id(self):
        self.assertEqual('137236', self.record.defect_id)

    def test_review_id(self):
        self.assertEqual('85639', self.record.review_id)

    def test_review_creation_date(self):
        self.assertEqual('2016-11-16 11:21 UTC',
                         self.record.review_creation_date)

    def test_creator_login(self):
        self.assertEqual('pzhong', self.record.creator_login)

    def test_creator_full_name(self):
        self.assertEqual('patrick zhong', self.record.creator_full_name)

    def test_severity(self):
        self.assertEqual('major', self.record.severity)

    def test_type_cvb(self):
        self.assertEqual('algorithm/logic', self.record.type_cvb)

    def test_injection_stage(self):
        self.assertEqual('not evaluated', self.record.injection_stage)

    def test_creator_product_name(self):
        self.assertEqual('viewpoint', self.record.creator_product_name)

    def test_review_creation_year(self):
        self.assertEqual('2016', self.record.review_creation_year)

    def test_review_creation_month(self):
        self.assertEqual('2016-11', self.record.review_creation_month)


if __name__ == '__main__':
    unittest.main()
