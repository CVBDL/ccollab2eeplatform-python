import unittest

from ccollab2eeplatform.ccollab.defect_record import DefectRecord
from ccollab2eeplatform.filters.injection_stage_filter import InjectionStageFilter


class TestInjectionStageFilter(unittest.TestCase):

    def setUp(self):
        self._records = [
            #['Defect ID', 'Review ID', 'Review Creation Date', 'Creator Login', 'Creator Full Name', 'Severity', 'Type_CVB', 'Injection Stage'],
            ['1', '5', '2016-09-30 19:11 UTC', 'pzhong', '', 'Minor', 'documentation', 'Requirements'],
            ['2', '4', '2016-09-30 19:11 UTC', 'trang', '', 'Minor', 'requirements/design', 'Requirements'],
            ['3', '3', '2016-09-30 22:20 UTC', 'pzhong', '', 'Major', 'N/A', 'N/A'],
            ['4', '2', '2016-09-30 22:20 UTC', 'trang', '', 'Minor', 'N/A', 'Not Evaluated'],
            ['5', '1', '2016-09-30 19:06 UTC', 'yyyang', '', 'Major', 'algorithm/logic', 'High Level Design']
        ]
        self.records = [DefectRecord(record) for record in self._records]

    def test_injection_stage_filter(self):
        injection_stage_filter = InjectionStageFilter(None)
        self.assertEqual(injection_stage_filter.filter(), None)

        injection_stage_filter = InjectionStageFilter(self.records)
        self.assertEqual(len(injection_stage_filter.filter()), 5)

        injection_stage_filter = InjectionStageFilter(self.records, None)
        self.assertEqual(len(injection_stage_filter.filter()), 5)

        injection_stage_filter = InjectionStageFilter(self.records, '')
        self.assertEqual(len(injection_stage_filter.filter()), 0)

        injection_stage_filter = InjectionStageFilter(self.records, 0)
        self.assertEqual(len(injection_stage_filter.filter()), 0)

        injection_stage_filter = InjectionStageFilter(self.records, {})
        self.assertEqual(len(injection_stage_filter.filter()), 0)

        injection_stage_filter = InjectionStageFilter(self.records, 'REQUIREMENTS')
        self.assertEqual(len(injection_stage_filter.filter()), 2)

        injection_stage_filter = InjectionStageFilter(self.records, 'requirements')
        self.assertEqual(len(injection_stage_filter.filter()), 2)

        injection_stage_filter = InjectionStageFilter(self.records, 'Not Evaluated')
        self.assertEqual(len(injection_stage_filter.filter()), 1)

        injection_stage_filter = InjectionStageFilter(
            self.records, ['Not Evaluated', 'Requirements'])
        self.assertEqual(len(injection_stage_filter.filter()), 3)

        injection_stage_filter = InjectionStageFilter(self.records)
        injection_stage_filter.set_keywords('Not Evaluated')
        self.assertEqual(len(injection_stage_filter.filter()), 1)

        injection_stage_filter = InjectionStageFilter(self.records, 'Requirements')
        injection_stage_filter.set_keywords('Not Evaluated')
        self.assertEqual(len(injection_stage_filter.filter()), 1)


if __name__ == '__main__':
    unittest.main()
