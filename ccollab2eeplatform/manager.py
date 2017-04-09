"""Data manager module.

Collect data of each defined chart, and send it to EagleEye Platform.
"""

import json

from eeplatform_api.client import EagleEyePlatformClient

import ccollab2eeplatform.google_visualization.gviz_api as gviz_api
from ccollab2eeplatform.filters.creator_filter import CreatorFilter
from ccollab2eeplatform.filters.product_filter import ProductFilter
from ccollab2eeplatform.settings.eeplatform_settings import EEPlatformSettings
from ccollab2eeplatform.settings.users_settings import UsersSettings
from ccollab2eeplatform.statistics.records_statistics import RecordsStatistics


class RecordManager:
    """Main data manager class.

    Generate all review and defect related charts.

    Args:
        records: A list of records.
        start_date (str): The start of review creation date.
        end_date (str): The end of review creation date.
    """

    def __init__(self, records, settings, start_date, end_date):
        self._records = records
        self._settings = settings
        self._start_date = start_date
        self._end_date = end_date
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

    def _get_valid_records(self):
        """Return records which we should use to calculate statistics.

        Only the record which creator login name is in users settings
        file is considered to be valid.
        """
        creator_filter = CreatorFilter(self._records,
                                       UsersSettings.list_login_names())
        return creator_filter.filter()

    def _process(self, setting, schema, data):
        chart_id = setting['_id']
        data_table = gviz_api.DataTable(schema, data=data)
        data_table_json_obj = json.loads(data_table.ToJSon().decode('utf-8'))
        client = self._get_client()
        #client.chart.update(chart_id, {'datatable': data_table_json_obj})
        print(chart_id)
        print(data_table_json_obj)
        print()

    def _process_count_by_month_from_product(self, product, setting):
        valid_records = self._get_valid_records()
        product_records = ProductFilter(valid_records, product).filter()
        stat = RecordsStatistics(product_records,
                                 start_date=self._start_date,
                                 end_date=self._end_date)
        schema, data = stat.count_by_month
        self._process(setting, schema, data)

    def process_count_by_month_from_product(self):
        """Generate chart of count by month from product."""
        name = 'count_by_month_from_product'
        for product, setting in self._settings[name].items():
            self._process_count_by_month_from_product(product, setting)

    def process_count_by_product(self):
        """Generate chart of count by product."""
        name = 'count_by_product'
        setting = self._settings[name]
        valid_records = self._get_valid_records()
        stat = RecordsStatistics(valid_records)
        schema, data = stat.count_by_product
        self._process(setting, schema, data)
