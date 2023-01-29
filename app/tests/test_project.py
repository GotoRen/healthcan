import unittest
from model.project import project


class test_project(unittest.TestCase):
    # mock01:【name】project name must be of type string and non-null.
    def test_name(self):
        self.assertTrue(type(project.name()) == str)
        self.assertTrue(len(project.name()) > 0)


if __name__ == "__main__":
    unittest.main()
