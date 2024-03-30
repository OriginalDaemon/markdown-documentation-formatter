import os.path
import unittest
from pathlib import Path

from mddocproc import ProcessingSettings, ProcessingContext, Document, rules


class TestTableOfContents(unittest.TestCase):
    def test_empty_toc(self):
        context = ProcessingContext(ProcessingSettings())
        input_md = "# Title\n" "## Table of contents\n" "${create_table_of_contents}\n" "...\n" "...\n" "...\n"
        expected = "# Title\n" "## Table of contents\n" "\n" "...\n" "...\n" "...\n"
        doc = Document(Path("test.md"), input_md)
        rules.create_table_of_contents(context, doc)
        self.assertEqual(expected, doc.contents)

    def test_full_toc(self):
        context = ProcessingContext(ProcessingSettings())
        input_md = (
            "# Title\n"
            "## Table of contents\n"
            "${create_table_of_contents}\n"
            "## Section 1\n"
            "...\n"
            "### Subsection 1.1\n"
            "...\n"
            "### Subsection 1.2\n"
            "...\n"
            "## Section 2\n"
            "...\n"
            "### Subsection 2.1\n"
            "...\n"
        )
        expected = (
            "# Title\n"
            "## Table of contents\n"
            " - [Section 1](<#Section 1>)\n"
            "   - [Subsection 1.1](<#Subsection 1.1>)\n"
            "   - [Subsection 1.2](<#Subsection 1.2>)\n"
            " - [Section 2](<#Section 2>)\n"
            "   - [Subsection 2.1](<#Subsection 2.1>)\n"
            "## Section 1\n"
            "...\n"
            "### Subsection 1.1\n"
            "...\n"
            "### Subsection 1.2\n"
            "...\n"
            "## Section 2\n"
            "...\n"
            "### Subsection 2.1\n"
            "...\n"
        )
        doc = Document(Path("test.md"), input_md)
        rules.create_table_of_contents(context, doc)
        self.assertEqual(expected, doc.contents)


class TestApplyMacros(unittest.TestCase):
    def test_single_const_macro(self):
        settings = ProcessingSettings(const_macros={"hello": "world"})
        context = ProcessingContext(settings)
        doc = Document(Path("test.md"), "Example macro ${hello}")
        rules.apply_macros(context, doc)
        self.assertEqual("Example macro world", doc.contents)

    def test_multiple_const_macros(self):
        settings = ProcessingSettings(const_macros={"hello": "world", "hello2": "world2"})
        context = ProcessingContext(settings)
        doc = Document(Path("test.md"), "Example macro ${hello} and another ${hello2}")
        rules.apply_macros(context, doc)
        self.assertEqual("Example macro world and another world2", doc.contents)

    def test_single_function_macro_no_args(self):
        settings = ProcessingSettings(function_macros={"hello": lambda: "world"})
        context = ProcessingContext(settings)
        doc = Document(Path("test.md"), "Example macro ${hello()}")
        rules.apply_macros(context, doc)
        self.assertEqual("Example macro world", doc.contents)

    def test_multiple_function_macros_no_args(self):
        settings = ProcessingSettings(function_macros={"hello": lambda: "world", "hello2": lambda: "world2"})
        context = ProcessingContext(settings)
        doc = Document(Path("test.md"), "Example macro ${hello()} and another ${hello2()}")
        rules.apply_macros(context, doc)
        self.assertEqual("Example macro world and another world2", doc.contents)

    def test_single_function_macro_with_args(self):
        settings = ProcessingSettings(function_macros={"hello": lambda x, y: f"x={x} y={y}"})
        context = ProcessingContext(settings)
        doc = Document(Path("test.md"), "Example macro ${hello(a, b)}")
        rules.apply_macros(context, doc)
        self.assertEqual("Example macro x=a y=b", doc.contents)

    def test_multiple_function_macros_with_args(self):
        settings = ProcessingSettings(
            function_macros={
                "hello": lambda x, y: f"x={x} y={y}",
                "hello2": lambda x, y, z: f"x={x} y={y} z={z}",
            }
        )
        context = ProcessingContext(settings)
        doc = Document(Path("test.md"), "Example macro ${hello(a, b)} and another ${hello2(c, d, e)}")
        rules.apply_macros(context, doc)
        self.assertEqual("Example macro x=a y=b and another x=c y=d z=e", doc.contents)

    def test_const_not_defined(self):
        settings = ProcessingSettings()
        context = ProcessingContext(settings)
        doc = Document(Path("test.md"), "Example macro ${hello}")
        with self.assertLogs("mddocproc", level="WARNING"):
            rules.apply_macros(context, doc)
        self.assertEqual("Example macro ${hello}", doc.contents)

    def test_function_not_defined(self):
        settings = ProcessingSettings()
        context = ProcessingContext(settings)
        doc = Document(Path("test.md"), "Example macro ${hello()}")
        with self.assertLogs("mddocproc", level="WARNING"):
            rules.apply_macros(context, doc)
        self.assertEqual("Example macro ${hello()}", doc.contents)

    def test_function_with_const(self):
        settings = ProcessingSettings(function_macros={"hello": lambda x: f"x={x}"}, const_macros={"hello2": "world2"})
        context = ProcessingContext(settings)
        doc = Document(Path("test.md"), "Example macro ${hello(${hello2})}")
        rules.apply_macros(context, doc)
        self.assertEqual("Example macro x=world2", doc.contents)

    def test_function_wrong_arg_count(self):
        settings = ProcessingSettings(
            function_macros={
                "hello": lambda x, y: "world",
            }
        )
        context = ProcessingContext(settings)
        doc = Document(Path("test.md"), "Example macro ${hello(a)}")
        with self.assertLogs("mddocproc", level="ERROR"):
            rules.apply_macros(context, doc)
        self.assertEqual("Example macro ${hello(a)}", doc.contents)

    def test_function_is_not_a_function(self):
        settings = ProcessingSettings(
            const_macros={
                "hello": "world",
            }
        )
        context = ProcessingContext(settings)
        doc = Document(Path("test.md"), "Example macro ${hello(a)}")
        with self.assertLogs("mddocproc", level="ERROR"):
            rules.apply_macros(context, doc)
        self.assertEqual("Example macro ${hello(a)}", doc.contents)

    def test_function_raises_exception(self):
        def _raise_exception():
            raise RuntimeError("Example error")

        settings = ProcessingSettings(
            function_macros={
                "hello": _raise_exception,
            }
        )
        context = ProcessingContext(settings)
        doc = Document(Path("test.md"), "Example macro ${hello()}")
        with self.assertLogs("mddocproc", level="ERROR"):
            rules.apply_macros(context, doc)
        self.assertEqual("Example macro ${hello()}", doc.contents)

    def test_no_macros(self):
        settings = ProcessingSettings(
            const_macros={"hello": "world"},
            function_macros={"hello2": lambda x: ""}
        )
        context = ProcessingContext(settings)
        doc = Document(Path("test.md"), "Example without any macros in it.")
        rules.apply_macros(context, doc)
        self.assertEqual("Example without any macros in it.", doc.contents)


class TestSanitizeInternalLinks(unittest.TestCase):
    @staticmethod
    def _create_test_data(link):
        doc_root = Path(os.path.join(os.path.dirname(__file__), "data", "docs"))
        context = ProcessingContext(ProcessingSettings(doc_root))
        context.add_document(Document(doc_root / Path("sub dir/relative - file.md"), "### sub - section"))
        doc = Document(Path(doc_root / "test dir/test.md"), link)
        context.add_document(doc)
        return context, doc

    def test_external_link_unchanged(self):
        context = ProcessingContext(ProcessingSettings())
        input_md = "[link](https://www.google.com)"
        expected = input_md
        doc = Document(Path("test.md"), input_md)
        rules.santize_internal_links(context, doc)
        self.assertEqual(expected, doc.contents)

    def test_internal_file_relative_link(self):
        cases = [
            "[link](<../sub dir/relative - file.md>)",
            "[link](../sub%20dir/relative%20-%20file.md)",
            "[link](<../sub%20dir/relative%20-%20file.md>)",
        ]
        expected = "[link](<../sub dir/relative - file.md>)"
        for i, case in enumerate(cases):
            with self.subTest(i=i):
                context, doc = self._create_test_data(case)
                rules.santize_internal_links(context, doc)
                self.assertEqual(expected, doc.contents)

    def test_internal_file_relative_link_with_subsection(self):
        cases = [
            "[link](<../sub dir/relative - file.md#sub - section>)",
            "[link](../sub%20dir/relative%20-%20file.md#sub%20-%20section)",
            "[link](<../sub%20dir/relative%20-%20file.md#sub%20-%20section>)",
            "[link](../sub%20dir/relative%20-%20file.md#sub---section)",
            "[link](<../sub%20dir/relative%20-%20file.md#sub---section>)",
        ]
        expected = "[link](<../sub dir/relative - file.md#sub - section>)"
        for i, case in enumerate(cases):
            with self.subTest(i=i):
                context, doc = self._create_test_data(case)
                rules.santize_internal_links(context, doc)
                self.assertEqual(expected, doc.contents)

    def test_internal_root_relative_link(self):
        cases = [
            "[link](<sub dir/relative - file.md>)",
            "[link](sub%20dir/relative%20-%20file.md)",
            "[link](<sub%20dir/relative%20-%20file.md>)",
        ]
        expected = "[link](<../sub dir/relative - file.md>)"
        for i, case in enumerate(cases):
            with self.subTest(i=i):
                context, doc = self._create_test_data(case)
                rules.santize_internal_links(context, doc)
                self.assertEqual(expected, doc.contents)

    def test_internal_root_relative_link_with_subsection(self):
        cases = [
            "[link](<sub dir/relative - file.md#sub - section>)",
            "[link](sub%20dir/relative%20-%20file.md#sub%20-%20section)",
            "[link](<sub%20dir/relative%20-%20file.md#sub%20-%20section>)",
            "[link](sub%20dir/relative%20-%20file.md#sub---section)",
            "[link](<sub%20dir/relative%20-%20file.md#sub---section>)",
        ]
        expected = "[link](<../sub dir/relative - file.md#sub - section>)"
        for i, case in enumerate(cases):
            with self.subTest(i=i):
                context, doc = self._create_test_data(case)
                rules.santize_internal_links(context, doc)
                self.assertEqual(expected, doc.contents)


class TestMoveToTargetDirRelative(unittest.TestCase):
    pass


class TestRenameUniquelyForConfluence(unittest.TestCase):
    pass


def get_suite():
    tests = [
        unittest.TestLoader().loadTestsFromTestCase(TestTableOfContents),
        unittest.TestLoader().loadTestsFromTestCase(TestApplyMacros),
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
