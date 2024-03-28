import os
import unittest
from unittest import TestCase
from .. import _rules as rules
from .. import _processing as processing
from .. import _document as document
from .. import _main as main


class TestCommandLineArgs(unittest.TestCase):
    def test_simple(self):
        pass


def getSuite():
    tests = [
        unittest.TestLoader().loadTestsFromTestCase(TestCommandLineArgs),
    ]
    return unittest.TestSuite(tests)


def runTests():
    import sys
    suite = getSuite()
    unittest.TextTestRunner(stream=sys.stderr).run(suite)


if __name__ == "__main__":
    unittest.main()
