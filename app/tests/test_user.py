import unittest
import datetime
import copy
from unittest import mock
from model.project import project
from model.user import user

class test_user(unittest.TestCase):
    # setUp: mock database creation.
    def setUp(self):
        self.u = user.build()
        self.u.attr["email"] = "hoge@fuga.com"
        self.u.attr["name"] = "HogeFuga"
        self.u.attr["password"] = "hogehogefugafuga"
        self.patcher = mock.patch('model.project.project.name', return_value="test_user")
        self.mock_name = self.patcher.start()
        user.migrate()
        self.u.save()

    # tearDown: clear mockDB after each test.
    def tearDown(self):
        user.db_cleaner()
        self.patcher.stop()
        
    # mock01:【find】returns matching elements.
    def test_db_is_working(self):
        u = user.find(self.u.attr["id"])
        self.assertTrue(type(u) is user)
        self.assertTrue(u.attr["id"] == 1)

    # mock02:【find_by_email】returns matching elements.
    def test_find_by_email(self):
        u = user.find_by_email(self.u.attr["email"])
        self.assertTrue(type(u) is user)
        self.assertTrue(u.attr["id"] == 1)
        self.assertTrue(u.attr["email"] == self.u.attr["email"])

    # mock03:【is_valid】attr has the correct value.
    def test_is_valid(self):
        self.assertTrue(self.u.is_valid())

    # mock04:【is_valid】attr has the wrong value.
    def test_is_valid_with_invarid_attrs(self):
        cb_wrong = copy.deepcopy(self.u)
        cb_wrong.attr["id"] = None # id must be None or a int
        self.assertTrue(cb_wrong.is_valid())
        cb_wrong = copy.deepcopy(self.u)
        cb_wrong.attr["id"] = "1" # id must be None or a int
        self.assertFalse(cb_wrong.is_valid())

        cb_wrong = copy.deepcopy(self.u)
        cb_wrong.attr["email"] = 12345 # email must be a sting
        self.assertFalse(cb_wrong.is_valid())

        cb_wrong = copy.deepcopy(self.u)
        cb_wrong.attr["name"] = 12345 # name must be a sting
        self.assertFalse(cb_wrong.is_valid())

        cb_wrong = copy.deepcopy(self.u)
        cb_wrong.attr["password"] = None # password must be a string
        self.assertFalse(cb_wrong.is_valid())

        cb_wrong = copy.deepcopy(self.u)
        cb_wrong.attr["password"] = 12345 # password must be a string
        self.assertFalse(cb_wrong.is_valid())

        cb_wrong = copy.deepcopy(self.u)
        cb_wrong.attr["last_updated"] = None # last_updated must be a datetime.datetime object
        self.assertFalse(cb_wrong.is_valid())

    # mock05:【build】create a user instance with a default value.
    def test_build(self):
        u = user.build()
        self.assertTrue(type(u) is user)

    # mock06:【save】execute insert when id is None.
    def test_db_save_insert(self):
        u = user.build()
        u.attr["id"] = None
        u.attr["email"] = "hoge2@fuga.com"
        u.attr["name"] = "Hoge"
        u.attr["password"] = "HogeHogeFugaFuga"
        result = u.save()
        self.assertTrue(type(result) is int)
        #self.assertTrue(u.attr["id"] is not None)

    # mock07:【save】execute update when id has a value.
    def test_db_save_update(self):
        u = user.build()
        u.attr["id"] = 1
        u.attr["email"] = "new_hoge@fuga.com"
        u.attr["name"] = "new_HogeFuga"
        u.attr["password"] = "new_HogeHogeFugaFuga"
        result = u.save()
        self.assertTrue(type(result) is int)
        self.assertTrue(u.attr["id"] is not None)



if __name__ == "__main__":
    unittest.main()
