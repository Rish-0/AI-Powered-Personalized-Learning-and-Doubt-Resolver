class ContextBuilder:

    @staticmethod
    def build(documents):

        context = []

        for document in documents:

            page = document.metadata.get("page")

            source = document.metadata.get("source")

            context.append(

                f"""
Source : {source}
Page : {page}

{document.page_content}
"""

            )

        return "\n\n-----------------------------\n\n".join(context)