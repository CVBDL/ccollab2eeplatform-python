import unittest

import ccollab2eeplatform.ccollab.defect as defect


class TestDefect(unittest.TestCase):

    def test_create_download_command(self):
        creation_date_lo = '2016-10-01'
        creation_date_hi = '2016-10-02'
        command = ''.join([
            'ccollab admin wget \"/go?',
            'type_cvbVis=y',
            '&defectIdVis=y',
            '&severityVis=y',
            '&defectReviewIdVis=y',
            '&defectCreatorUserNameVis=y',
            '&reviewCreatedVis=y',
            '&defectCreatorUserLoginVis=y',
            '&injectionStageVis=y',
            '&page=ReportDefectList',
            '&component=ErrorsAndMessages',
            '&data-format=csv',
            '&groupDepth=0',
            '&formSubmittedreportConfig=1',
            '&reviewCreationDateFilter=lo%3D2016-10-01%7C%7C%7Chi%3D2016-10-02',
            '\"'
        ])
        created_command = defect._create_download_command(creation_date_lo,
                                                          creation_date_hi)
        self.assertEqual(command, created_command)


if __name__ == '__main__':
    unittest.main()
