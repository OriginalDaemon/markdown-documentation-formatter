from mddocformatter import ProcessingContext, Document, document_rule


@document_rule("*.md")
def my_rule(context: ProcessingContext, document: Document):
    pass
