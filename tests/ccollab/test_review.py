import unittest

import ccollab2eeplatform.ccollab.review as review


class TestReview(unittest.TestCase):

    def test_create_download_command(self):
        # pylint: disable=protected-access
        creation_date_lo = '2016-10-01'
        creation_date_hi = '2016-10-02'
        command = ''.join([
            'ccollab admin wget \"/go?',
            'reviewCreatorUserLoginVis=y',
            '&numDefectsVis=y',
            '&reviewCreatorUserNameVis=y',
            '&reviewIdVis=y',
            '&reviewPersonDurationVis=y',
            '&reviewCreationDateVis=y',
            '&numCommentsVis=y',
            '&locVis=y',
            '&locChangedVis=y',
            '&data-format=csv',
            '&page=ReportReviewList',
            '&formSubmittedreportConfig=1',
            '&reviewCreationDateFilter=lo%3D2016-10-01%7C%7C%7Chi%3D2016-10-02',
            '\"'
        ])
        created_command = review._create_download_command(creation_date_lo,
                                                          creation_date_hi)
        self.assertEqual(command, created_command)


if __name__ == '__main__':
    unittest.main()
