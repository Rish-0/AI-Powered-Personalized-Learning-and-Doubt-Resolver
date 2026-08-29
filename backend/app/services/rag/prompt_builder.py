class PromptBuilder:

    @staticmethod
    def build(context: str, question: str):

        return f"""
You are an AI Tutor.

Answer ONLY using the provided context.

If the answer is not present in the context, reply exactly:

"I couldn't find the answer in the uploaded document."

-----------------------------------------

Context

{context}

-----------------------------------------

Question

{question}

-----------------------------------------

Answer:
"""