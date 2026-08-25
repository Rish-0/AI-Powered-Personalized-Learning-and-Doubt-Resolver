from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.services.chunking.metadata import ChunkMetadata


class TextChunker:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(

            chunk_size=500,

            chunk_overlap=100,

            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

    def chunk_pages(self, pages):

        all_chunks = []

        for page in pages:

            chunks = self.splitter.split_text(
                page["text"]
            )

            for index, chunk in enumerate(chunks):

                metadata = ChunkMetadata.create(

                    source=page["source"],

                    page=page["page"],

                    chunk_index=index

                )

                all_chunks.append({

                    "text": chunk,

                    "metadata": metadata

                })

        return all_chunks