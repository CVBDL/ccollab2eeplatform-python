"""Statistics analysis and save to EagleEye platform."""

import json

from eeplatform_api.client import EagleEyePlatformClient

import ccollab2eeplatform.google_visualization.gviz_api as gviz_api
from ccollab2eeplatform import utils
from ccollab2eeplatform.log import logger
from ccollab2eeplatform.filters.creator_filter import CreatorFilter
from ccollab2eeplatform.filters.product_filter import ProductFilter
from ccollab2eeplatform.settings.eeplatform_settings import EEPlatformSettings
from ccollab2eeplatform.settings.users_settings import UsersSettings
from ccollab2eeplatform.statistics.records_statistics import RecordsStatistics


class RecordManager:
    """Record manager class.

    Args:
        records: A list of records.
        settings: EagleEye chart settings.
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
        """Return an EagleEye Platform API client instance."""
        if not self._client:
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
        if not setting or not setting.get('_id'):
            return
        chart_id = setting.get('_id')
        data_table = gviz_api.DataTable(schema, data=data)
        data_table_json_obj = json.loads(data_table.ToJSon().decode('utf-8'))
        client = self._get_client()
        #client.chart.update(chart_id, {'datatable': data_table_json_obj})
        print(chart_id)
        print(data_table_json_obj)
        print()

    def process(self):
        """Process all charts."""
        self.count_by_month_from_product()
        self.count_by_product()
        self.comment_density_uploaded_by_product()
        self.comment_density_changed_by_product()
        self.defect_density_uploaded_by_product()
        self.defect_density_changed_by_product()
        self.comment_density_changed_by_month_from_product()
        self.inspection_rate_by_month_from_product()

    def count_by_month_from_product(self):
        """Records count by month from product.

        Data table:
        Month    Count
        2016-01  20
        2016-03  10
        2016-05  25
        """
        def process_product(product, setting):
            schema = [('Month', 'string'), ('Count', 'number')]
            data = []
            valid_records = self._get_valid_records()
            product_records = ProductFilter(valid_records, product).filter()
            try:
                count_by_month = {}
                stat = RecordsStatistics(product_records)
                for month, group in stat.groupby_review_creation_month:
                    _stat = RecordsStatistics(list(group))
                    count_by_month[month] = _stat.count
            except AttributeError:
                return 1
            for month in utils.month_range(self._start_date, self._end_date):
                data.append([month, count_by_month.get(month, 0)])
            self._save(setting, schema, data)

        # Start to process for all products.
        name = 'count_by_month_from_product'
        if self._settings.get(name):
            for product, setting in self._settings.get(name).items():
                process_product(product, setting)

    def count_by_product(self):
        """Records count by product.

        Data table:
        Product  Count
        Team1    20
        Team2    16
        """
        name = 'count_by_product'
        schema = [('Product', 'string'), ('Count', 'number')]
        data = []
        valid_records = self._get_valid_records()
        try:
            stat = RecordsStatistics(valid_records)
            for product, group in stat.groupby_creator_product_name:
                _stat = RecordsStatistics(list(group))
                data.append([product, _stat.count])
        except AttributeError:
            return 1
        self._save(self._settings.get(name), schema, data)

    def comment_density_uploaded_by_product(self):
        """Comment density(uploaded) by product.

        Data table:
        Product  Comments/KLOC
        Team1    0.1
        Team2    0.034
        """
        name = 'comment_density_uploaded_by_product'
        schema = [('Product', 'string'), ('Comments/KLOC', 'number')]
        data = []
        valid_records = self._get_valid_records()
        try:
            stat = RecordsStatistics(valid_records)
            for product, group in stat.groupby_creator_product_name:
                _stat = RecordsStatistics(list(group))
                data.append([product, _stat.comment_density_uploaded])
        except AttributeError:
            return 1
        self._save(self._settings.get(name), schema, data)

    def comment_density_changed_by_product(self):
        """Comment density(changed) by product.

        Data table:
        Product  Comments/KLOCC
        Team1    0.1
        Team2    0.034
        """
        name = 'comment_density_changed_by_product'
        schema = [('Product', 'string'), ('Comments/KLOCC', 'number')]
        data = []
        valid_records = self._get_valid_records()
        try:
            stat = RecordsStatistics(valid_records)
            for product, group in stat.groupby_creator_product_name:
                _stat = RecordsStatistics(list(group))
                data.append([product, _stat.comment_density_changed])
        except AttributeError:
            return 1
        self._save(self._settings.get(name), schema, data)

    def comment_density_changed_by_month_from_product(self):
        """Comment density(changed) by month.

        Data table:
        Month    Comments/KLOCC
        2016-01  0.1
        2016-02  0.034
        """
        name = 'comment_density_changed_by_month_from_product'
        def _process(product, setting):
            schema = [('Month', 'string'), ('Comments/KLOCC', 'number')]
            data = []
            valid_records = self._get_valid_records()
            product_records = ProductFilter(valid_records, product).filter()
            try:
                density_by_month = {}
                stat = RecordsStatistics(product_records)
                for month, group in stat.groupby_review_creation_month:
                    _stat = RecordsStatistics(list(group))
                    density_by_month[month] = _stat.comment_density_changed
            except AttributeError:
                return 1
            for month in utils.month_range(self._start_date, self._end_date):
                data.append([month, density_by_month.get(month, 0)])
            self._save(setting, schema, data)

        # Start to process for all products.
        if self._settings.get(name):
            for product, setting in self._settings.get(name).items():
                _process(product, setting)

    def defect_density_uploaded_by_product(self):
        """Defect density(uploaded) by product.

        Data table:
        Product  Defects/KLOC
        Team1    0.1
        Team2    0.034
        """
        name = 'defect_density_uploaded_by_product'
        schema = [('Product', 'string'), ('Defects/KLOC', 'number')]
        data = []
        valid_records = self._get_valid_records()
        try:
            stat = RecordsStatistics(valid_records)
            for product, group in stat.groupby_creator_product_name:
                _stat = RecordsStatistics(list(group))
                data.append([product, _stat.defect_density_uploaded])
        except AttributeError:
            return 1
        self._save(self._settings.get(name), schema, data)

    def defect_density_changed_by_product(self):
        """Defect density(changed) by product.

        Data table:
        Product  Defects/KLOCC
        Team1    0.1
        Team2    0.034
        """
        name = 'defect_density_changed_by_product'
        schema = [('Product', 'string'), ('Defects/KLOCC', 'number')]
        data = []
        valid_records = self._get_valid_records()
        try:
            stat = RecordsStatistics(valid_records)
            for product, group in stat.groupby_creator_product_name:
                _stat = RecordsStatistics(list(group))
                data.append([product, _stat.defect_density_changed])
        except AttributeError:
            return 1
        self._save(self._settings.get(name), schema, data)

    def inspection_rate_by_month_from_product(self):
        """Inspection rate by month.

        Data table:
        Month  KLOCC/Hour
        2016-01  0.1
        2016-03  0.2
        2016-05  0.3
        """
        name = 'inspection_rate_by_month_from_product'
        def _process(product, setting):
            schema = [('Month', 'string'), ('KLOCC/Hour', 'number')]
            data = []
            valid_records = self._get_valid_records()
            product_records = ProductFilter(valid_records, product).filter()
            try:
                stat_by_month = {}
                stat = RecordsStatistics(product_records)
                for month, group in stat.groupby_review_creation_month:
                    _stat = RecordsStatistics(list(group))
                    stat_by_month[month] = _stat.inspection_rate
            except AttributeError:
                return 1
            for month in utils.month_range(self._start_date, self._end_date):
                data.append([month, stat_by_month.get(month, 0)])
            self._save(setting, schema, data)

        # Start to process for all products.
        if self._settings.get(name):
            for product, setting in self._settings.get(name).items():
                _process(product, setting)
