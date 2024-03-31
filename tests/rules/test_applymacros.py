import unittest

from pathlib import Path
from mddocproc import ProcessingSettings, ProcessingContext, Document, rules


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

    def test_const_is_a_function(self):
        settings = ProcessingSettings(
            function_macros={
                "hello": lambda: "",
            }
        )
        context = ProcessingContext(settings)
        doc = Document(Path("test.md"), "Example macro ${hello}")
        with self.assertLogs("mddocproc", level="ERROR"):
            rules.apply_macros(context, doc)
        self.assertEqual("Example macro ${hello}", doc.contents)

    def test_function_is_a_const(self):
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
        settings = ProcessingSettings(const_macros={"hello": "world"}, function_macros={"hello2": lambda x: ""})
        context = ProcessingContext(settings)
        doc = Document(Path("test.md"), "Example without any macros in it.")
        rules.apply_macros(context, doc)
        self.assertEqual("Example without any macros in it.", doc.contents)
