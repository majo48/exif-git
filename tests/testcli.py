""" testcases for the recreate app

    functions:
        testRunScripting: test scripting application
        testRunScripting: test GUI application
"""
import unittest
import io
from contextlib import redirect_stdout
from recreate import app
from recreate.common import constants


class TestRunCLI(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testRunScripting(self):
        """ run scripting part of app """
        f = io.StringIO()
        with redirect_stdout(f):
            app.run(constants.mydocuments(), 'stdout')
        out = f.getvalue()
        out = out.splitlines()
        self.assertEqual(out[0], 'SCRIPTING is active...')
        self.assertEqual(out[1], constants.mydocuments())
        self.assertEqual(out[2], 'stdout')

    def testRunGUI(self):
        """ run gui part of app """
        f = io.StringIO()
        with redirect_stdout(f):
            app.run('default', 'default')
        out = f.getvalue()
        out = out.splitlines()
        self.assertEqual(out[0], 'GUI is active in folder '+constants.mydocuments())


if __name__ == '__main__':
    unittest.main()