import re


class TextCleaner:

    @staticmethod
    def clean(text: str) -> str:
        """
        Clean extracted PDF text.
        """

        if not text:
            return ""

        # Remove multiple spaces
        text = re.sub(r"[ \t]+", " ", text)

        # Remove excessive blank lines
        text = re.sub(r"\n{2,}", "\n", text)

        # Remove leading/trailing spaces
        text = text.strip()

        return text