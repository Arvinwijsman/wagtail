import unittest


class BaseTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls):
        cls.config_file = 'pytest.ini'

    @classmethod
    def tearDownClass(cls):
        pass
