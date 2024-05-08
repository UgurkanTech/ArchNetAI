import numpy as np
from .model import ResultType

class Embedder():
    """
    A class that provides methods for embedding and searching text using a given model.
    """

    embed_dict = {}

    def __init__(self, model):
        """
        Initializes an Embedder object.

        Args:
            model: The model used for embedding text.
        """
        self.model = model

    def embed_text(self, text):
        """
        Embeds the given text using the model and saves the embedding.

        Args:
            text: The text to be embedded.
        """
        self.model.createModelResponse(text)
        emb = self.model.getResponse(resultType=ResultType.EMBEDDING)
        self.save_embedding(text, emb)

    def search_text(self, text):
        """
        Embeds the given text using the model and searches for the best match in the saved embeddings.

        Args:
            text: The text to be searched.

        Returns:
            The best match and its similarity score.
        """
        self.model.createModelResponse(text)
        emb = self.model.getResponse(resultType=ResultType.EMBEDDING)
        best_match, best_similarity = self.find_best_match(emb)
        return best_match, best_similarity

    def save_embedding(self, key, embedding):
        """
        Saves the embedding for a given key.

        Args:
            key: The key associated with the embedding.
            embedding: The embedding to be saved.
        """
        self.embed_dict[key] = embedding
    
    def find_best_match(self, embedding):
        """
        Finds the best match for a given embedding.

        Args:
            embedding: The embedding to be matched.

        Returns:
            The best match and its similarity score.
        """
        best_match = None
        best_similarity = 0
        for key, value in self.embed_dict.items():
            similarity = self.cosine_similarity(embedding, value)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = key
        return best_match, best_similarity

    @staticmethod
    def cosine_similarity(e1, e2):
        """
        Calculate the cosine similarity between two embeddings.

        Args:
            e1 (numpy.ndarray): The first embedding.
            e2 (numpy.ndarray): The second embedding.

        Returns:
            float: The cosine similarity between the two embeddings.
        """
        dot_product = np.dot(e1, e2)
        norm_e1 = np.linalg.norm(e1)
        norm_e2 = np.linalg.norm(e2)
        similarity = dot_product / (norm_e1 * norm_e2)
        return similarity
    
    