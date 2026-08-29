class PromptBuilder:

    @staticmethod

    def build(context, question):

        return f"""
You are an AI Tutor.

Answer ONLY using the provided context.

If the context does not contain the answer,

reply:

"I couldn't find sufficient information."

Context

{context}

Question

{question}

Answer:
"""