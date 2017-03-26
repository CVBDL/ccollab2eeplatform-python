"""Data manager module.

Collect data of each defined chart, and send it to EagleEye Platform.
"""

import json

from eeplatform_api.client import EagleEyePlatformClient

import ccollab2eeplatform.google_visualization.gviz_api as gviz_api
from ccollab2eeplatform.settings.charts_settings import ChartsSettings
from ccollab2eeplatform.settings.eeplatform_settings import EEPlatformSettings
from ccollab2eeplatform.statistics.defect_records_statistics import (
    DefectRecordsStatistics
)
from ccollab2eeplatform.statistics.review_records_statistics import (
    ReviewRecordsStatistics
)


class DataManager:
    """Main data manager class.

    Generate all review and defect related charts.

    Args:
        review_records: A list of review records.
        defect_records: A list of defect records.
    Attributes:
        review_records: A list of review records.
        defect_records: A list of defect records.
    """

    def __init__(self, review_records=None, defect_records=None):
        self._client = None
        self.review_records = review_records
        self.defect_records = defect_records
        if review_records is not None:
            self.review_statistics = ReviewRecordsStatistics(review_records)
        if defect_records is not None:
            self.defect_statistics = DefectRecordsStatistics(defect_records)

    def process(self):
        """The entry point of processing all of the charts.

        It will call subprocesses to generate each chart.
        """
        if self.review_records is not None:
            self._process_review_count_by_month()
        if self.defect_records is not None:
            self._process_defect_count_by_product()

    def _get_client(self):
        """Get an EagleEye Platform API client instance.

        Returns:
            An instance of EagleEye Platform client.
        """
        if self._client is None:
            self._client = EagleEyePlatformClient(
                EEPlatformSettings.get_api_root_endpoint()
            )
        return self._client

    def _process_review_count_by_month(self):
        """Review: generate review count by month."""
        settings_key = 'review_count_by_month'
        chart_id = ChartsSettings.get_chart_id(settings_key)
        schema, data = (
            self.review_statistics.calc_review_count_by_month()
        )
        data_table = gviz_api.DataTable(schema, data=data)
        data_table_json_obj = json.loads(data_table.ToJSon().decode('utf-8'))
        client = self._get_client()
        #client.chart.update(chart_id, {'datatable': data_table_json_obj})

    def _process_defect_count_by_product(self):
        """Defect: generate defect count by product."""
        settings_key = 'defect count by product'
        chart_id = ChartsSettings.get_chart_id(settings_key)
        schema, data = (
            self.defect_statistics.calc_defect_count_by_product()
        )
        data_table = gviz_api.DataTable(schema, data=data)
        data_table_json_obj = json.loads(data_table.ToJSon().decode('utf-8'))
        client = self._get_client()
        #client.chart.update(chart_id, {'datatable': data_table_json_obj})
        print(data_table_json_obj)
