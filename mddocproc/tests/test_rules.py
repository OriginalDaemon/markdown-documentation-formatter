import os
import unittest
from .. import _rules as rules
from .. import _processing as processing
from .. import _document as document


class TestTableOfContents(unittest.TestCase):
    pass


class TestReplaceVariables(unittest.TestCase):
    pass


class TestSanitizeInternalLinks(unittest.TestCase):
    pass


class TestMoveToTargetDirRelative(unittest.TestCase):
    pass


class TestRenameUniquelyForConfluence(unittest.TestCase):
    pass


def getSuite():
    tests = [
        unittest.TestLoader().loadTestsFromTestCase(TestTableOfContents),
        unittest.TestLoader().loadTestsFromTestCase(TestReplaceVariables),
        unittest.TestLoader().loadTestsFromTestCase(TestSanitizeInternalLinks),
        unittest.TestLoader().loadTestsFromTestCase(TestMoveToTargetDirRelative),
        unittest.TestLoader().loadTestsFromTestCase(TestRenameUniquelyForConfluence),
    ]
    return unittest.TestSuite(tests)


def runTests():
    import sys

    suite = getSuite()
    unittest.TextTestRunner(stream=sys.stderr).run(suite)


if __name__ == "__main__":
    unittest.main()
