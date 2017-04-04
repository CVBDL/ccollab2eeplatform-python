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
from ccollab2eeplatform.statistics.records_statistics import RecordsStatistics
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

    def __init__(self, start_date, end_date,
                 review_records=None, defect_records=None):
        self._start_date = start_date
        self._end_date = end_date
        self._review_records = review_records
        self._defect_records = defect_records
        self._review_statistics = None
        self._defect_statistics = None
        self._client = None

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

    def _get_valid_records(self, records):
        """Return records which we should use to calculate statistics.

        Only the record which creator login name is in users settings
        file is considered to be valid.
        """
        creator_filter = CreatorFilter(records,
                                       UsersSettings.list_login_names())
        return creator_filter.filter()

    def _statistics_factory(self):
        valid_review_records = self._get_valid_records(self._review_records)
        valid_defect_records = self._get_valid_records(self._defect_records)
        if valid_review_records is not None:
            self._review_statistics = ReviewRecordsStatistics(
                valid_review_records)
        if valid_defect_records is not None:
            self._defect_statistics = DefectRecordsStatistics(
                valid_defect_records)

    def process(self):
        """The entry point of processing all of the charts.

        It will call subprocesses to generate each chart.
        """
        self._statistics_factory()
        if self._review_statistics is not None:
            self._process_review()
        if self._defect_statistics is not None:
            self._process_defect()

    def _process_review(self):
        self._process_review_count_by_month()
        self._process_review_count_by_product()

    def _process_defect(self):
        self._process_defect_count_by_product()

    def _process(self, settings_key, schema, data):
        chart_id = ChartsSettings.get_chart_id(settings_key)
        data_table = gviz_api.DataTable(schema, data=data)
        data_table_json_obj = json.loads(data_table.ToJSon().decode('utf-8'))
        client = self._get_client()
        #client.chart.update(chart_id, {'datatable': data_table_json_obj})
        print(data_table_json_obj)

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
