import unittest

from ccollab2eeplatform.settings import users_settings


class TestUsersSettings(unittest.TestCase):

    def setUp(self):
        users_settings._users = [
            {
                "login_name": "pzhong",
                "full_name": "Patrick Zhong",
                "product_name": "ViewPoint"
            },
            {
                "login_name": "yyyang",
                "full_name": "Young Yang",
                "product_name": "FTView"
            }
        ]

    def test_list_login_names(self):
        self.assertEqual(
            users_settings.list_login_names(),
            ['pzhong', 'yyyang']
        )

    def test_get_product_by_login(self):
        self.assertEqual(
            users_settings.get_product_by_login('pzhong'),
            'ViewPoint'
        )
        self.assertEqual(
            users_settings.get_product_by_login('yyyang'),
            'FTView'
        )


if __name__ == '__main__':
    unittest.main()
