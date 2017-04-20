"""Statistics analysis and save to EagleEye platform."""

import json

from eeplatform_api.client import EagleEyePlatformClient

import ccollab2eeplatform.google_visualization.gviz_api as gviz_api
from ccollab2eeplatform import utils
from ccollab2eeplatform.log import logger
from ccollab2eeplatform.filters.creator_filter import CreatorFilter
from ccollab2eeplatform.filters.date_filter import DateFilter
from ccollab2eeplatform.filters.injection_stage_filter import InjectionStageFilter
from ccollab2eeplatform.filters.product_filter import ProductFilter
from ccollab2eeplatform.settings import charts_settings
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
        #self.count_by_month_from_product()
        #self.count_by_product()
        #self.comment_density_uploaded_by_product()
        #self.comment_density_changed_by_product()
        #self.defect_density_uploaded_by_product()
        #self.defect_density_changed_by_product()
        #self.comment_density_changed_by_month_from_product()
        #self.inspection_rate_by_month_from_product()
        self.count_by_injection_stage()

    def list_valid_records(self):
        """Return records which we should use to calculate statistics.

        Only the record which creator login name is in users settings
        file is considered to be valid.
        """
        creator_filter = CreatorFilter(self._records,
                                       UsersSettings.list_login_names())
        return creator_filter.filter()

    def count_by_month_from_product(self):
        """Records count by month from a product.

        It may generate multiple charts.

        Data table:
        Month    Count
        2016-01  20
        2016-02  0
        2016-03  10
        2016-04  0
        2016-05  25
        """
        def process_product(product, setting):
            schema = [('Month', 'string'), ('Count', 'number')]
            data = []
            valid_records = self.list_valid_records()
            product_records = ProductFilter(valid_records, product).filter()
            for month in utils.month_range(self._start_date, self._end_date):
                month_records = DateFilter(product_records, month).filter()
                try:
                    stat = RecordsStatistics(month_records)
                    data.append([month, stat.count])
                except AttributeError:
                    return 1
            self._save(setting, schema, data)

        # Start to process for all products.
        name = 'count_by_month_from_product'
        if self._settings.get(name):
            for product, setting in self._settings.get(name).items():
                process_product(product, setting)

    def count_by_product(self):
        """Records count by product.

        It'll generate a single chart.

        Data table:
        Product   Count
        ProductA  20
        ProductB  0
        ProductC  16
        """
        name = 'count_by_product'
        schema = [('Product', 'string'), ('Count', 'number')]
        data = []
        valid_records = self.list_valid_records()
        products = charts_settings.list_products()
        for product in products:
            product_records = ProductFilter(valid_records, product).filter()
            try:
                stat = RecordsStatistics(product_records)
                data.append([product, stat.count])
            except AttributeError:
                return 1
        self._save(self._settings.get(name), schema, data)

    def comment_density_uploaded_by_product(self):
        """Comment density(uploaded) by product.

        It'll generate a single chart.

        Data table:
        Product   Comments/KLOC
        ProductA  0.1
        ProductB  0.034
        ProductC  0
        """
        name = 'comment_density_uploaded_by_product'
        schema = [('Product', 'string'), ('Comments/KLOC', 'number')]
        data = []
        valid_records = self.list_valid_records()
        products = charts_settings.list_products()
        for product in products:
            product_records = ProductFilter(valid_records, product).filter()
            try:
                stat = RecordsStatistics(product_records)
                data.append([product, stat.comment_density_uploaded])
            except AttributeError:
                return 1
        self._save(self._settings.get(name), schema, data)

    def comment_density_changed_by_product(self):
        """Comment density(changed) by product.

        It'll generate a single chart.

        Data table:
        Product   Comments/KLOCC
        ProductA  0.1
        ProductB  0.034
        ProductC  0
        """
        name = 'comment_density_changed_by_product'
        schema = [('Product', 'string'), ('Comments/KLOCC', 'number')]
        data = []
        valid_records = self.list_valid_records()
        products = charts_settings.list_products()
        for product in products:
            product_records = ProductFilter(valid_records, product).filter()
            try:
                stat = RecordsStatistics(product_records)
                data.append([product, stat.comment_density_changed])
            except AttributeError:
                return 1
        self._save(self._settings.get(name), schema, data)

    def comment_density_changed_by_month_from_product(self):
        """Comment density(changed) by month.

        It may generate multiple charts.

        Data table:
        Month     Comments/KLOCC
        ProductA  0.1
        ProductB  0.034
        ProductC  0
        """
        name = 'comment_density_changed_by_month_from_product'
        def process_product(product, setting):
            schema = [('Month', 'string'), ('Comments/KLOCC', 'number')]
            data = []
            valid_records = self.list_valid_records()
            product_records = ProductFilter(valid_records, product).filter()
            for month in utils.month_range(self._start_date, self._end_date):
                month_records = DateFilter(product_records, month).filter()
                try:
                    stat = RecordsStatistics(month_records)
                    data.append([month, stat.comment_density_changed])
                except AttributeError:
                    return 1
            self._save(setting, schema, data)

        # Start to process for all products.
        if self._settings.get(name):
            for product, setting in self._settings.get(name).items():
                process_product(product, setting)

    def defect_density_uploaded_by_product(self):
        """Defect density(uploaded) by product.

        It'll generate a single chart.

        Data table:
        Product   Defects/KLOC
        ProductA  0.1
        ProductB  0.034
        ProductC  0
        """
        name = 'defect_density_uploaded_by_product'
        schema = [('Product', 'string'), ('Defects/KLOC', 'number')]
        data = []
        valid_records = self.list_valid_records()
        products = charts_settings.list_products()
        for product in products:
            product_records = ProductFilter(valid_records, product).filter()
            try:
                stat = RecordsStatistics(product_records)
                data.append([product, stat.defect_density_uploaded])
            except AttributeError:
                return 1
        self._save(self._settings.get(name), schema, data)

    def defect_density_changed_by_product(self):
        """Defect density(changed) by product.

        It'll generate a single chart.

        Data table:
        Product   Defects/KLOCC
        ProductA  0.1
        ProductB  0.034
        ProductC  0
        """
        name = 'defect_density_changed_by_product'
        schema = [('Product', 'string'), ('Defects/KLOCC', 'number')]
        data = []
        valid_records = self.list_valid_records()
        products = charts_settings.list_products()
        for product in products:
            product_records = ProductFilter(valid_records, product).filter()
            try:
                stat = RecordsStatistics(product_records)
                data.append([product, stat.defect_density_changed])
            except AttributeError:
                return 1
        self._save(self._settings.get(name), schema, data)

    def inspection_rate_by_month_from_product(self):
        """Inspection rate by month.

        It may generate multiple charts.

        Data table:
        Month    KLOCC/Hour
        2016-01  0.1
        2016-02  0
        2016-03  0.2
        2016-04  0
        2016-05  0.3
        """
        def process_product(product, setting):
            schema = [('Month', 'string'), ('KLOCC/Hour', 'number')]
            data = []
            valid_records = self.list_valid_records()
            product_records = ProductFilter(valid_records, product).filter()
            for month in utils.month_range(self._start_date, self._end_date):
                month_records = DateFilter(product_records, month).filter()
                try:
                    stat = RecordsStatistics(month_records)
                    data.append([month, stat.inspection_rate])
                except AttributeError:
                    return 1
            self._save(setting, schema, data)

        # Start to process for all products.
        name = 'inspection_rate_by_month_from_product'
        if self._settings.get(name):
            for product, setting in self._settings.get(name).items():
                process_product(product, setting)

    def count_by_injection_stage(self):
        """Records count by injection stage.

        It'll generate a single chart.

        Data table:
        InjectionStage     Count
        Not Evaluated      2
        Requirements       0
        High Level Design  4
        Detailed Design    11
        """
        name = 'count_by_injection_stage'
        schema = [('InjectionStage', 'string'), ('Count', 'number')]
        data = []
        valid_records = self.list_valid_records()
        injection_stages = charts_settings.list_injection_stages()
        for injection_stage in injection_stages:
            try:
                injection_stage_filter = InjectionStageFilter(valid_records,
                                                              injection_stage)
                stage_records = injection_stage_filter.filter()
                stat = RecordsStatistics(stage_records)
                data.append([injection_stage, stat.count])
            except AttributeError:
                return 1
        self._save(self._settings.get(name), schema, data)
