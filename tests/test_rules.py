import unittest


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


def get_suite():
    tests = [
        unittest.TestLoader().loadTestsFromTestCase(TestTableOfContents),
        unittest.TestLoader().loadTestsFromTestCase(TestReplaceVariables),
        unittest.TestLoader().loadTestsFromTestCase(TestSanitizeInternalLinks),
        unittest.TestLoader().loadTestsFromTestCase(TestMoveToTargetDirRelative),
        unittest.TestLoader().loadTestsFromTestCase(TestRenameUniquelyForConfluence),
    ]
    return unittest.TestSuite(tests)


def run_tests():
    import sys

    suite = get_suite()
    unittest.TextTestRunner(stream=sys.stderr).run(suite)


if __name__ == "__main__":
    unittest.main()
