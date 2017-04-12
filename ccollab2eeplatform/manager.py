"""Data manager module.

Collect data of each defined chart, and send it to EagleEye Platform.
"""

import json

from eeplatform_api.client import EagleEyePlatformClient

import ccollab2eeplatform.google_visualization.gviz_api as gviz_api
from ccollab2eeplatform import utils
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

    def _save(self, setting, schema, data):
        """Save data table to EagleEye platform."""
        chart_id = setting['_id']
        data_table = gviz_api.DataTable(schema, data=data)
        data_table_json_obj = json.loads(data_table.ToJSon().decode('utf-8'))
        client = self._get_client()
        #client.chart.update(chart_id, {'datatable': data_table_json_obj})
        print(chart_id)
        print(data_table_json_obj)
        print()

    def process_count_by_month_from_product(self):
        """Count by month from product."""
        name = 'count_by_month_from_product'

        def _process_count_by_month_from_product(product, setting):
            """Record count by month.

            Data table:
            Month    Count
            2016-01  20
            2016-03  10
            2016-05  25
            """
            schema = [('Month', 'string'), ('Count', 'number')]
            data = []
            valid_records = self._get_valid_records()
            product_records = ProductFilter(valid_records, product).filter()
            stat = RecordsStatistics(product_records)
            count_by_month = {}
            for month, group in stat.groupby_review_creation_month:
                count_by_month[month] = RecordsStatistics(list(group)).count
            month_range = utils.month_range(self._start_date, self._end_date)
            for month in month_range:
                data.append([month, count_by_month.get(month, 0)])
            self._save(setting, schema, data)

        # Start to process for all products.
        for product, setting in self._settings[name].items():
            _process_count_by_month_from_product(product, setting)

    def process_count_by_product(self):
        """Record count by product.

        Data table:
        Product  Count
        Team1    20
        Team2    16
        """
        name = 'count_by_product'
        setting = self._settings[name]
        schema = [('Product', 'string'), ('Count', 'number')]
        data = []
        valid_records = self._get_valid_records()
        stat = RecordsStatistics(valid_records)
        for product, group in stat.groupby_creator_product_name:
            _stat = RecordsStatistics(list(group))
            data.append([product, _stat.count])
        self._save(setting, schema, data)

    def process_comment_density_uploaded_by_product(self):
        """Comment density(uploaded) by product.

        Data table:
        Product  Comments/KLOC
        Team1    0.1
        Team2    0.034
        """
        name = 'comment_density_uploaded_by_product'
        setting = self._settings[name]
        schema = [('Product', 'string'), ('Comments/KLOC', 'number')]
        data = []
        valid_records = self._get_valid_records()
        stat = RecordsStatistics(valid_records)
        for product, group in stat.groupby_creator_product_name:
            _stat = RecordsStatistics(list(group))
            data.append([product, _stat.comment_density_uploaded])
        self._save(setting, schema, data)

    def process_comment_density_changed_by_product(self):
        """Comment density(changed) by product.

        Data table:
        Product  Comments/KLOCC
        Team1    0.1
        Team2    0.034
        """
        name = 'comment_density_changed_by_product'
        setting = self._settings[name]
        schema = [('Product', 'string'), ('Comments/KLOCC', 'number')]
        data = []
        valid_records = self._get_valid_records()
        stat = RecordsStatistics(valid_records)
        for product, group in stat.groupby_creator_product_name:
            _stat = RecordsStatistics(list(group))
            data.append([product, _stat.comment_density_changed])
        self._save(setting, schema, data)

    def process_comment_density_changed_by_month_from_product(self):
        """Generate chart of comment density(changed) by month from product."""
        name = 'comment_density_changed_by_month_from_product'

        def _process_comment_density_changed_by_month_from_product(
                product, setting):
            """Comment density(changed) by month.

            Data table:
            Month    Comments/KLOCC
            2016-01  0.1
            2016-02  0.034
            """
            schema = [('Month', 'string'), ('Comments/KLOCC', 'number')]
            data = []
            valid_records = self._get_valid_records()
            product_records = ProductFilter(valid_records, product).filter()
            stat = RecordsStatistics(product_records)
            density_by_month = {}
            for month, group in stat.groupby_review_creation_month:
                _stat = RecordsStatistics(list(group))
                density_by_month[month] = _stat.comment_density_changed
            month_range = utils.month_range(self._start_date, self._end_date)
            for month in month_range:
                data.append([month, density_by_month.get(month, 0)])
            self._save(setting, schema, data)

        # Start to process for all products.
        for product, setting in self._settings[name].items():
            _process_comment_density_changed_by_month_from_product(
                product, setting)

    def process_defect_density_uploaded_by_product(self):
        """Defect density(uploaded) by product.

        Data table:
        Product  Defects/KLOC
        Team1    0.1
        Team2    0.034
        """
        name = 'defect_density_uploaded_by_product'
        setting = self._settings[name]
        schema = [('Product', 'string'), ('Defects/KLOC', 'number')]
        data = []
        valid_records = self._get_valid_records()
        stat = RecordsStatistics(valid_records)
        for product, group in stat.groupby_creator_product_name:
            _stat = RecordsStatistics(list(group))
            data.append([product, _stat.defect_density_uploaded])
        self._save(setting, schema, data)

    def process_defect_density_changed_by_product(self):
        """Defect density(changed) by product.

        Data table:
        Product  Defects/KLOCC
        Team1    0.1
        Team2    0.034

        Returns:
            A tuple of column definition and data.
        """
        name = 'defect_density_changed_by_product'
        setting = self._settings[name]
        schema = [('Product', 'string'), ('Defects/KLOCC', 'number')]
        data = []
        valid_records = self._get_valid_records()
        stat = RecordsStatistics(valid_records)
        for product, group in stat.groupby_creator_product_name:
            _stat = RecordsStatistics(list(group))
            data.append([product, _stat.defect_density_changed])
        self._save(setting, schema, data)

    def process_inspection_rate_by_month_from_product(self):
        """Inspection rate by month from product."""
        name = 'inspection_rate_by_month_from_product'

        def _process_inspection_rate_by_month_from_product(product, setting):
            """Inspection rate by month.

            Data table:
            Month  KLOCC/Hour
            2016-01  0.1
            2016-03  0.2
            2016-05  0.3

            Returns:
                A tuple of column definition and data.
            """
            schema = [('Month', 'string'), ('KLOCC/Hour', 'number')]
            data = []
            valid_records = self._get_valid_records()
            product_records = ProductFilter(valid_records, product).filter()
            stat = RecordsStatistics(product_records)
            stat_by_month = {}
            for month, group in stat.groupby_review_creation_month:
                _stat = RecordsStatistics(list(group))
                stat_by_month[month] = _stat.inspection_rate
            month_range = utils.month_range(self._start_date, self._end_date)
            for month in month_range:
                data.append([month, stat_by_month.get(month, 0)])
            self._save(setting, schema, data)

        # Start to process for all products.
        for product, setting in self._settings[name].items():
            _process_inspection_rate_by_month_from_product(
                product, setting)
