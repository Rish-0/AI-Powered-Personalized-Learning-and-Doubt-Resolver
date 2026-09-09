import re


class AnalyticsService:

    def extract_topics(self, question):

        words = re.findall(

            r"[A-Za-z]+",

            question

        )

        words = [

            word.capitalize()

            for word in words

            if len(word) > 4

        ]

        return list(set(words))