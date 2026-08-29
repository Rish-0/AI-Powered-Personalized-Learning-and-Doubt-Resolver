class PromptBuilder:

    @staticmethod
    def build(context, question):

        return f"""
You are an AI Tutor.

Answer ONLY using the supplied context.

If the answer cannot be found,

reply exactly:

I couldn't find the answer in the uploaded document.

----------------------------

Context

{context}

----------------------------

Question

{question}

----------------------------

Answer:
"""