import unittest

from ccollab2eeplatform.ccollab.review_record import ReviewRecord
from ccollab2eeplatform.ccollab.defect_record import DefectRecord
from ccollab2eeplatform.statistics.records_statistics import RecordsStatistics


class TestRecordsStatistics(unittest.TestCase):

    def setUp(self):
        self._review_records = [
            # ['ID', 'Review Creation Date', 'Creator Login', 'Creator Full Name', 'Defect Count', 'Comment Count', 'LOC', 'LOC Changed', 'Total Person-Time']
            ['1', '2016-11-30 11:55 UTC', 'pzhong', '', '1', '0', '100', '10', '1d, 01:28:01'],
            ['2', '2016-11-30 11:55 UTC', 'trang', '', '0', '1', '100', '10', '1:00:00'],
            ['3', '2016-11-30 11:55 UTC', 'pzhong', '', '9', '0', '100', '10', '0:30:00'],
            ['4', '2016-11-30 11:55 UTC', 'trang', '', '0', '9', '100', '20', '0:1:59'],
            ['5', '2016-11-30 11:55 UTC', 'yyyang', '', '10', '0', '100', '50', '1d, 11:30:00']
        ]
        self.review_records = [ReviewRecord(record) for record in self._review_records]
        self._defect_records = [
            #['Defect ID', 'Review ID', 'Review Creation Date', 'Creator Login', 'Creator Full Name', 'Severity', 'Type_CVB', 'Injection Stage'],
            ['1', '5', '2016-09-30 19:11 UTC', 'pzhong', '', 'Minor', 'documentation', 'Requirements'],
            ['2', '4', '2016-09-30 19:11 UTC', 'trang', '', 'Minor', 'requirements/design', 'Requirements'],
            ['3', '3', '2016-09-30 22:20 UTC', 'pzhong', '', 'Major', 'N/A', 'N/A'],
            ['4', '2', '2016-09-30 22:20 UTC', 'trang', '', 'Minor', 'N/A', 'N/A'],
            ['5', '1', '2016-09-30 19:06 UTC', 'yyyang', '', 'Major', 'algorithm/logic', 'Code']
        ]
        self.defect_records = [DefectRecord(record) for record in self._defect_records]

    def test_count(self):
        review_stat = RecordsStatistics(self.review_records)
        self.assertEqual(review_stat.count, 5)
        defect_stat = RecordsStatistics(self.defect_records)
        self.assertEqual(defect_stat.count, 5)

    def test_total_defect(self):
        review_stat = RecordsStatistics(self.review_records)
        self.assertEqual(review_stat.total_defect, 20)

    def test_total_comment(self):
        review_stat = RecordsStatistics(self.review_records)
        self.assertEqual(review_stat.total_comment, 10)

    def test_total_loc(self):
        review_stat = RecordsStatistics(self.review_records)
        self.assertEqual(review_stat.total_loc, 500)

    def test_total_loc_changed(self):
        review_stat = RecordsStatistics(self.review_records)
        self.assertEqual(review_stat.total_loc_changed, 100)

    def test_comment_density_uploaded(self):
        review_stat = RecordsStatistics(self.review_records)
        self.assertEqual(review_stat.comment_density_uploaded, 20)

    def test_comment_density_changed(self):
        review_stat = RecordsStatistics(self.review_records)
        self.assertEqual(review_stat.comment_density_changed, 100)

    def test_defect_density_uploaded(self):
        review_stat = RecordsStatistics(self.review_records)
        self.assertEqual(review_stat.defect_density_uploaded, 40)

    def test_defect_density_changed(self):
        review_stat = RecordsStatistics(self.review_records)
        self.assertEqual(review_stat.defect_density_changed, 200)

    def test_total_person_time_in_second(self):
        review_stat = RecordsStatistics(self.review_records)
        self.assertEqual(review_stat.total_person_time_in_second, 225000)
        
    def test_total_person_time_in_hour(self):
        review_stat = RecordsStatistics(self.review_records)
        self.assertEqual(review_stat.total_person_time_in_hour, 62.5)

    def test_inspection_rate(self):
        review_stat = RecordsStatistics(self.review_records)
        self.assertEqual(review_stat.inspection_rate, 0.0016)