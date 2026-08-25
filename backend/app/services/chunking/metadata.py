import uuid


class ChunkMetadata:

    @staticmethod
    def create(source, page, chunk_index):

        return {

            "chunk_id": str(uuid.uuid4()),

            "source": source,

            "page": page,

            "chunk_index": chunk_index

        }