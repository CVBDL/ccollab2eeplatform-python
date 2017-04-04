"""Data manager module.

Collect data of each defined chart, and send it to EagleEye Platform.
"""

import json

from eeplatform_api.client import EagleEyePlatformClient

import ccollab2eeplatform.google_visualization.gviz_api as gviz_api
from ccollab2eeplatform.filters.creator_filter import CreatorFilter
from ccollab2eeplatform.settings.charts_settings import ChartsSettings
from ccollab2eeplatform.settings.eeplatform_settings import EEPlatformSettings
from ccollab2eeplatform.settings.users_settings import UsersSettings
from ccollab2eeplatform.statistics.defect_records_statistics import (
    DefectRecordsStatistics
)
from ccollab2eeplatform.statistics.review_records_statistics import (
    ReviewRecordsStatistics
)


class RecordManager:
    """Main data manager class.

    Generate all review and defect related charts.

    Args:
        review_records: A list of review records.
        defect_records: A list of defect records.
    """

    def __init__(self, review_records=None, defect_records=None):
        self._review_records = review_records
        self._defect_records = defect_records
        self._client = None

    def process(self, start_date, end_date):
        """The entry point of processing all of the charts.

        It will call subprocesses to generate each chart.

        Args:
            start_date (str): The start of time span for given records.
            end_date (str): The end of time span for given records.
        """
        review_records, defect_records = self._get_valid_records()
        if review_records is not None:
            self._review_statistics = ReviewRecordsStatistics(review_records)
            self._process_review_count_by_month()
            self._process_review_count_by_product()
        if defect_records is not None:
            self._defect_statistics = DefectRecordsStatistics(defect_records)
            self._process_defect_count_by_product()

    def _get_valid_records(self):
        """Return records which we should use to calculate statistics.

        Only the record which creator login name is in users settings
        file is considered to be valid.
        """
        valid_review_record = None
        if self._review_records is not None:
            valid_review_filter = CreatorFilter(
                self._review_records,
                UsersSettings.list_login_names()
            )
            valid_review_record = valid_review_filter.filter()

        valid_defect_record = None
        if self._defect_records is not None:
            valid_defect_filter = CreatorFilter(
                self._defect_records,
                UsersSettings.list_login_names()
            )
            valid_defect_record = valid_defect_filter.filter()

        return valid_review_record, valid_defect_record

    def _process(self, settings_key, schema, data):
        chart_id = ChartsSettings.get_chart_id(settings_key)
        data_table = gviz_api.DataTable(schema, data=data)
        data_table_json_obj = json.loads(data_table.ToJSon().decode('utf-8'))
        client = self._get_client()
        #client.chart.update(chart_id, {'datatable': data_table_json_obj})
        print(data_table_json_obj)

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
        schema, data = (
            self._review_statistics.calc_count_by_month()
        )
        self._process(settings_key, schema, data)

    def _process_review_count_by_product(self):
        """Review: generate review count by product."""
        settings_key = 'review_count_by_product'
        schema, data = (
            self._review_statistics.calc_count_by_product()
        )
        self._process(settings_key, schema, data)

    def _process_defect_count_by_product(self):
        """Defect: generate defect count by product."""
        settings_key = 'defect_count_by_product'
        schema, data = (
            self._defect_statistics.calc_count_by_product()
        )
        self._process(settings_key, schema, data)
