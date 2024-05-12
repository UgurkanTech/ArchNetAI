import sqlite3
import array
from typing import List
import numpy as np
from .embed import Embedding, EmbeddingPart

class VectorBase:
    # Constructor
    def __init__(self):
        pass
    # Embedding methods
    def add_embedding(self, Embedding) -> int:
        pass
    def get_embedding(self, id) -> Embedding:
        pass
    def delete_embedding(self, id) -> None:
        pass
    # Multiple embeddings methods
    def get_all_embeddings(self) -> List[Embedding]:
        pass
    def delete_all_embedings(self) -> None:
        pass
    # Update part count method
    def update_part_count(self, id, part_count) -> None:
        pass
    # Total Embedding Count method
    def get_count(self) -> int:
        pass
    def get_total_part_count(self) -> int:
        pass
    # Embedding part methods
    def add_embedding_part(self, EmbeddingPart) -> None:
        pass
    def get_embedding_part(self, embedding_id: int, index: int) -> EmbeddingPart:
        pass
    def delete_embedding_part(self, embedding_id: int, index: int) -> None:
        pass
    # Multiple embedding part methods
    def get_all_embedding_parts(self, embedding_id: int) -> List[EmbeddingPart]:
        pass
    def delete_all_embedding_parts(self, embedding_id: int) -> None:
        pass
    #Print method
    def print_db(self):
        pass
    # Deconstructor
    def __del__(self):
        pass


class DictVectorBase(VectorBase):
    def __init__(self):
        super().__init__()
        self.embeddings = {}
        self.embedding_parts = {}

    def add_embedding(self, embedding: Embedding) -> int:
        if embedding.id is None:
            while True:
                embedding.id = np.random.randint(1, 10000000)
                if embedding.id not in self.embeddings:
                    break
        self.embeddings[embedding.id] = embedding
        return embedding.id
    
    def get_embedding(self, id) -> Embedding:
        return self.embeddings[id]
    
    def delete_embedding(self, id) -> None:
        del self.embeddings[id]

    def get_all_embeddings(self) -> List[Embedding]:
        return list(self.embeddings.values())
    
    def delete_all_embedings(self) -> None:
        self.embeddings.clear()

    def update_part_count(self, id, part_count) -> None:
        self.embeddings[id].part_count = part_count

    def get_count(self) -> int:
        return len(self.embeddings)
    
    def get_total_part_count(self) -> int:
        return len(self.embedding_parts)
    
    def add_embedding_part(self, EmbeddingPart) -> None:
        if EmbeddingPart.embedding_id not in self.embedding_parts:
            self.embedding_parts[EmbeddingPart.embedding_id] = {}
        self.embedding_parts[EmbeddingPart.embedding_id][EmbeddingPart.index] = EmbeddingPart

    def get_embedding_part(self, embedding_id: int, index: int) -> EmbeddingPart:
        return self.embedding_parts[embedding_id][index]
    
    def delete_embedding_part(self, embedding_id: int, index: int) -> None:
        del self.embedding_parts[embedding_id][index]

    def get_all_embedding_parts(self, embedding_id: int) -> List[EmbeddingPart]:
        return list(self.embedding_parts[embedding_id].values())
    
    def delete_all_embedding_parts(self, embedding_id: int) -> None:
        del self.embedding_parts[embedding_id]

    def print_db(self):
        print("Embeddings:")
        for key, value in self.embeddings.items():
            print(f"ID: {key}, Source: {value.source}, Content Hash: {value.content_hash}, Type: {value.type}, Part Count: {value.part_count}")
        print("Embedding Parts:")
        for key, value in self.embedding_parts.items():
            for key2, value2 in value.items():
                print(f"Embedding ID: {key}, Index: {key2}, Embeds: {value2.embeds[0]:.4f}... (length: {len(value2.embeds)})")

    def __del__(self):
        self.embeddings.clear()
        self.embedding_parts.clear()

class SQLiteVectorBase(VectorBase):
    def __init__(self, db_path: str = ":memory:"):
        super().__init__()
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        
        self.cursor.execute("CREATE TABLE IF NOT EXISTS embeddings (id INTEGER PRIMARY KEY, source TEXT, content_hash TEXT, type TEXT, part_count INTEGER)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS embedding_parts (embedding_id INTEGER, part_index INTEGER, embeds BLOB, PRIMARY KEY (embedding_id, part_index))")
        self.conn.commit()

    def add_embedding(self, embedding: Embedding) -> int:
        if embedding.id is None:
            while True:
                embedding.id = np.random.randint(1, 10000000)
                self.cursor.execute("SELECT * FROM embeddings WHERE id=?", (embedding.id,))
                row = self.cursor.fetchone()
                if row is None:
                    break
        self.cursor.execute("INSERT INTO embeddings (id, source, content_hash, type, part_count) VALUES (?, ?, ?, ?, ?)", (embedding.id, embedding.source, embedding.content_hash, embedding.type, embedding.part_count))
        self.conn.commit()
        return embedding.id
    
    def get_embedding(self, id) -> Embedding:
        self.cursor.execute("SELECT * FROM embeddings WHERE id=?", (id,))
        row = self.cursor.fetchone()
        if row is None:
            return None
        embedding = Embedding()
        embedding.id = row[0]
        embedding.source = row[1]
        embedding.content_hash = row[2]
        embedding.type = row[3]
        embedding.part_count = row[4]
        return embedding
    
    def delete_embedding(self, id) -> None:
        self.cursor.execute("DELETE FROM embeddings WHERE id=?", (id,))
        self.conn.commit()

    def get_all_embeddings(self) -> List[Embedding]:
        self.cursor.execute("SELECT * FROM embeddings")
        rows = self.cursor.fetchall()
        embeddings = []
        for row in rows:
            embedding = Embedding()
            embedding.id = row[0]
            embedding.source = row[1]
            embedding.content_hash = row[2]
            embedding.type = row[3]
            embedding.part_count = row[4]
            embeddings.append(embedding)
        return embeddings
    
    def delete_all_embedings(self) -> None:
        self.cursor.execute("DELETE FROM embeddings")
        self.conn.commit()

    def update_part_count(self, id, part_count) -> None:
        self.cursor.execute("UPDATE embeddings SET part_count=? WHERE id=?", (part_count, id))
        self.conn.commit()

    def get_count(self) -> int:
        self.cursor.execute("SELECT COUNT(*) FROM embeddings")
        return self.cursor.fetchone()[0]
    
    def get_get_total_part_count(self) -> int:
        self.cursor.execute("SELECT COUNT(*) FROM embedding_parts")
        return self.cursor.fetchone()[0]
    
    def add_embedding_part(self, EmbeddingPart) -> None:
        embeds_bytes = array.array('f', EmbeddingPart.embeds).tobytes()
        self.cursor.execute("INSERT INTO embedding_parts (embedding_id, part_index, embeds) VALUES (?, ?, ?)", (EmbeddingPart.embedding_id, EmbeddingPart.index, embeds_bytes))
        self.conn.commit()
    
    def get_embedding_part(self, embedding_id: int, index: int) -> EmbeddingPart:
        self.cursor.execute("SELECT * FROM embedding_parts WHERE embedding_id=? AND part_index=?", (embedding_id, index))
        row = self.cursor.fetchone()
        if row is None:
            return None
        embedding_part = EmbeddingPart()
        embedding_part.embedding_id = row[0]
        embedding_part.index = row[1]
        embedding_part.embeds = np.frombuffer(row[2], dtype='float32')
        return embedding_part
    
    def delete_embedding_part(self, embedding_id: int, index: int) -> None:
        self.cursor.execute("DELETE FROM embedding_parts WHERE embedding_id=? AND part_index=?", (embedding_id, index))
        self.conn.commit()

    def get_all_embedding_parts(self, embedding_id: int) -> List[EmbeddingPart]:
        self.cursor.execute("SELECT * FROM embedding_parts WHERE embedding_id=?", (embedding_id,))
        rows = self.cursor.fetchall()
        embedding_parts = []
        for row in rows:
            embedding_part = EmbeddingPart()
            embedding_part.embedding_id = row[0]
            embedding_part.index = row[1]
            embedding_part.embeds = np.frombuffer(row[2])
            embedding_parts.append(embedding_part)
        return embedding_parts
    
    def delete_all_embedding_parts(self, embedding_id: int) -> None:
        self.cursor.execute("DELETE FROM embedding_parts WHERE embedding_id=?", (embedding_id,))
        self.conn.commit()

    def print_db(self):
        print("Embeddings:")
        self.cursor.execute("SELECT * FROM embeddings")
        rows = self.cursor.fetchall()
        for row in rows:
            print(f"ID: {row[0]}, Source: {row[1]}, Content Hash: {row[2]}, Type: {row[3]}, Part Count: {row[4]}")
        print("Embedding Parts:")
        self.cursor.execute("SELECT * FROM embedding_parts")
        rows = self.cursor.fetchall()
        for row in rows:
            print(f"Embedding ID: {row[0]}, Index: {row[1]}, Embeds: {np.frombuffer(row[2], dtype='float32')[0]:.4f}... (length: {len(np.frombuffer(row[2], dtype='float32'))})")

    def __del__(self):
        self.cursor.close()
        self.conn.close()