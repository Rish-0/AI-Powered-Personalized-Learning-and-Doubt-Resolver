class ContextBuilder:

    @staticmethod
    def build(documents):

        context = []

        for doc in documents:

            context.append(

                f"""
Source : {doc.metadata["source"]}

Page : {doc.metadata["page"]}

{doc.page_content}
"""

            )

        return "\n".join(context)