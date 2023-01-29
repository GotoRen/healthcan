import unittest
import copy
from unittest import mock
import datetime
import pytz
import decimal
from _pydecimal import Decimal
from model.healthcan import healthcan


class test_healthcan(unittest.TestCase):
    # setUp: mock database creation.
    def setUp(self):
        self.hc = healthcan()
        now = datetime.datetime.now(pytz.timezone("Asia/Tokyo"))
        self.hc.attr["user_id"] = 1
        self.hc.attr["name"] = "HogeFuga"
        self.hc.attr["date"] = "{0:%Y-%m-%d}".format(now.date())
        self.hc.attr["time"] = "{0:%H:%M:%S}".format(now.time())
        self.hc.attr["height"] = Decimal(175.0)
        self.hc.attr["weight"] = Decimal(68.0)
        self.hc.attr["bmi"] = Decimal(22.2)
        self.hc.attr["pro_weight"] = Decimal(67.38)
        self.hc.attr["diff_weight"] = Decimal(0.63)

        patcher = mock.patch(
            "model.healthcan.project.name", return_value="mock_healthcan"
        )
        self.mock_name = patcher.start()
        self.addCleanup(patcher.stop)
        healthcan.migrate()
        self.hc.save()

    # tearDown: clear mockDB after each test.
    def tearDown(self):
        healthcan.db_cleaner()

    # mock01:【find】returns matching elements.
    def test_db_is_working(self):
        hc = healthcan.find(self.hc.attr["id"])
        self.assertTrue(type(hc) is healthcan)
        self.assertTrue(hc.attr["id"] == 1)

    # mock02:【is_valid】attr has the correct value.
    def test_is_valid(self):
        self.assertTrue(self.hc.is_valid())

    # mock03:【is_valid】attr has the wrong value.
    def test_is_valid_with_invalid_attrs(self):
        # id must be None or a int
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["id"] = None
        self.assertTrue(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["id"] = "1"
        self.assertFalse(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["id"] = 1
        self.assertTrue(hc_wrong.is_valid())

        # user_id must be a int
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["user_id"] = None
        self.assertFalse(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["user_id"] = "1"
        self.assertFalse(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["user_id"] = 1
        self.assertTrue(hc_wrong.is_valid())

        # name must be a string
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["name"] = None
        self.assertFalse(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["name"] = "1"
        self.assertTrue(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["name"] = 1
        self.assertFalse(hc_wrong.is_valid())

        # date must be not None and string and int
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["date"] = None
        self.assertFalse(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["date"] = "1"
        self.assertTrue(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["date"] = 1
        self.assertTrue(hc_wrong.is_valid())

        # time must be not None
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["time"] = None
        self.assertFalse(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["time"] = "1"
        self.assertTrue(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["time"] = 1
        self.assertTrue(hc_wrong.is_valid())

        # height must be a Desimal
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["height"] = None
        self.assertFalse(hc_wrong.is_valid())

        # weight must be a Desimal
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["weight"] = None
        self.assertFalse(hc_wrong.is_valid())

        # bmi must be a Desimal
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["bmi"] = None
        self.assertFalse(hc_wrong.is_valid())

        # # pro_weight must be a Desimal
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["pro_weight"] = None
        self.assertFalse(hc_wrong.is_valid())

        # diff_weight must be a Desimal
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["diff_weight"] = None
        self.assertFalse(hc_wrong.is_valid())

    # mock04:【build】create a healthcan instance with a default value. (also used to create an input form with Controller.)
    def test_build(self):
        hc = healthcan.build()
        self.assertTrue(type(hc) is healthcan)

    # mock05:【_index】returns an index list of data.
    def test__index(self):
        self.assertEqual(len(healthcan._index(1)), 1)
        self.assertEqual(healthcan._index(1)[0], 1)


if __name__ == "__main__":
    unittest.main()
