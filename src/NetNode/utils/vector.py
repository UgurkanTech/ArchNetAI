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
        self.embeddings = {}  # Dictionary to store embeddings
        self.embedding_parts = {}  # Dictionary to store embedding parts

    def add_embedding(self, embedding: Embedding) -> int:
        """
        Add an embedding to the dictionary.

        Args:
            embedding (Embedding): The embedding to be added.

        Returns:
            int: The ID of the added embedding.
        """
        if embedding.id is None:
            while True:
                embedding.id = np.random.randint(1, 10000000)
                if embedding.id not in self.embeddings:
                    break
        self.embeddings[embedding.id] = embedding
        return embedding.id
    
    def get_embedding(self, id) -> Embedding:
        """
        Get the embedding with the specified ID.

        Args:
            id: The ID of the embedding.

        Returns:
            Embedding: The embedding with the specified ID.
        """
        return self.embeddings[id]
    
    def delete_embedding(self, id) -> None:
        """
        Delete the embedding with the specified ID.

        Args:
            id: The ID of the embedding.
        """
        del self.embeddings[id]

    def get_all_embeddings(self) -> List[Embedding]:
        """
        Get all embeddings in the dictionary.

        Returns:
            List[Embedding]: A list of all embeddings.
        """
        return list(self.embeddings.values())
    
    def delete_all_embedings(self) -> None:
        """
        Delete all embeddings in the dictionary.
        """
        self.embeddings.clear()

    def update_part_count(self, id, part_count) -> None:
        """
        Update the part count of the embedding with the specified ID.

        Args:
            id: The ID of the embedding.
            part_count: The new part count.
        """
        self.embeddings[id].part_count = part_count

    def get_count(self) -> int:
        """
        Get the count of embeddings in the dictionary.

        Returns:
            int: The count of embeddings.
        """
        return len(self.embeddings)
    
    def get_total_part_count(self) -> int:
        """
        Get the total part count of all embeddings.

        Returns:
            int: The total part count.
        """
        return len(self.embedding_parts)
    
    def add_embedding_part(self, EmbeddingPart) -> None:
        """
        Add an embedding part to the dictionary.

        Args:
            EmbeddingPart: The embedding part to be added.
        """
        if EmbeddingPart.embedding_id not in self.embedding_parts:
            self.embedding_parts[EmbeddingPart.embedding_id] = {}
        self.embedding_parts[EmbeddingPart.embedding_id][EmbeddingPart.index] = EmbeddingPart

    def get_embedding_part(self, embedding_id: int, index: int) -> EmbeddingPart:
        """
        Get the embedding part with the specified embedding ID and index.

        Args:
            embedding_id (int): The ID of the embedding.
            index (int): The index of the embedding part.

        Returns:
            EmbeddingPart: The embedding part with the specified embedding ID and index.
        """
        return self.embedding_parts[embedding_id][index]
    
    def delete_embedding_part(self, embedding_id: int, index: int) -> None:
        """
        Delete the embedding part with the specified embedding ID and index.

        Args:
            embedding_id (int): The ID of the embedding.
            index (int): The index of the embedding part.
        """
        del self.embedding_parts[embedding_id][index]

    def get_all_embedding_parts(self, embedding_id: int) -> List[EmbeddingPart]:
        """
        Get all embedding parts with the specified embedding ID.

        Args:
            embedding_id (int): The ID of the embedding.

        Returns:
            List[EmbeddingPart]: A list of all embedding parts with the specified embedding ID.
        """
        return list(self.embedding_parts[embedding_id].values())
    
    def delete_all_embedding_parts(self, embedding_id: int) -> None:
        """
        Delete all embedding parts with the specified embedding ID.

        Args:
            embedding_id (int): The ID of the embedding.
        """
        del self.embedding_parts[embedding_id]

    def print_db(self):
        """
        Print the embeddings and embedding parts in the dictionary.
        """
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
    """
    A class that provides SQLite-based storage for embeddings and embedding parts.

    Args:
        db_path (str): The path to the SQLite database file. Default is ":memory:" for an in-memory database.

    Attributes:
        db_path (str): The path to the SQLite database file.
        conn (sqlite3.Connection): The SQLite database connection.
        cursor (sqlite3.Cursor): The cursor object for executing SQL queries.

    """

    def __init__(self, db_path: str = ":memory:"):
        super().__init__()
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        
        # Create tables if they don't exist
        self.cursor.execute("CREATE TABLE IF NOT EXISTS embeddings (id INTEGER PRIMARY KEY, source TEXT, content_hash TEXT, type TEXT, part_count INTEGER)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS embedding_parts (embedding_id INTEGER, part_index INTEGER, embeds BLOB, PRIMARY KEY (embedding_id, part_index))")
        self.conn.commit()

    def add_embedding(self, embedding: Embedding) -> int:
        """
        Add an embedding to the database.

        Args:
            embedding (Embedding): The embedding object to be added.

        Returns:
            int: The ID of the added embedding.

        """
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
        """
        Get an embedding from the database by its ID.

        Args:
            id (int): The ID of the embedding.

        Returns:
            Embedding: The retrieved embedding object, or None if not found.

        """
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
        """
        Delete an embedding from the database by its ID.

        Args:
            id (int): The ID of the embedding to be deleted.

        """
        self.cursor.execute("DELETE FROM embeddings WHERE id=?", (id,))
        self.conn.commit()

    def get_all_embeddings(self) -> List[Embedding]:
        """
        Get all embeddings from the database.

        Returns:
            List[Embedding]: A list of all embeddings in the database.

        """
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
        """
        Delete all embeddings from the database.

        """
        self.cursor.execute("DELETE FROM embeddings")
        self.conn.commit()

    def update_part_count(self, id, part_count) -> None:
        """
        Update the part count of an embedding in the database.

        Args:
            id (int): The ID of the embedding.
            part_count (int): The new part count.

        """
        self.cursor.execute("UPDATE embeddings SET part_count=? WHERE id=?", (part_count, id))
        self.conn.commit()

    def get_count(self) -> int:
        """
        Get the total count of embeddings in the database.

        Returns:
            int: The total count of embeddings.

        """
        self.cursor.execute("SELECT COUNT(*) FROM embeddings")
        return self.cursor.fetchone()[0]
    
    def get_get_total_part_count(self) -> int:
        """
        Get the total count of embedding parts in the database.

        Returns:
            int: The total count of embedding parts.

        """
        self.cursor.execute("SELECT COUNT(*) FROM embedding_parts")
        return self.cursor.fetchone()[0]
    
    def add_embedding_part(self, EmbeddingPart) -> None:
        """
        Add an embedding part to the database.

        Args:
            EmbeddingPart: The embedding part object to be added.

        """
        embeds_bytes = array.array('f', EmbeddingPart.embeds).tobytes()
        self.cursor.execute("INSERT INTO embedding_parts (embedding_id, part_index, embeds) VALUES (?, ?, ?)", (EmbeddingPart.embedding_id, EmbeddingPart.index, embeds_bytes))
        self.conn.commit()
    
    def get_embedding_part(self, embedding_id: int, index: int) -> EmbeddingPart:
        """
        Get an embedding part from the database by its embedding ID and index.

        Args:
            embedding_id (int): The ID of the embedding.
            index (int): The index of the embedding part.

        Returns:
            EmbeddingPart: The retrieved embedding part object, or None if not found.

        """
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
        """
        Delete an embedding part from the database by its embedding ID and index.

        Args:
            embedding_id (int): The ID of the embedding.
            index (int): The index of the embedding part to be deleted.

        """
        self.cursor.execute("DELETE FROM embedding_parts WHERE embedding_id=? AND part_index=?", (embedding_id, index))
        self.conn.commit()

    def get_all_embedding_parts(self, embedding_id: int) -> List[EmbeddingPart]:
        """
        Get all embedding parts of an embedding from the database.

        Args:
            embedding_id (int): The ID of the embedding.

        Returns:
            List[EmbeddingPart]: A list of all embedding parts of the embedding.

        """
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
        """
        Delete all embedding parts of an embedding from the database.

        Args:
            embedding_id (int): The ID of the embedding.

        """
        self.cursor.execute("DELETE FROM embedding_parts WHERE embedding_id=?", (embedding_id,))
        self.conn.commit()

    def print_db(self):
        """
        Print the contents of the embeddings and embedding_parts tables in the database.

        """
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