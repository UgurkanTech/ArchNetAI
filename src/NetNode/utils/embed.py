import io
import os
from typing import List, Tuple
import numpy as np
from .response import ResultType
from .tools import Hasher
from enum import Enum

class EmbeddingPart:
    embedding_id: int # Foreign key. The id of the embedding this part belongs to.
    index: int # Index of the part in the file.txt. Starts from 0.
    embeds: np.ndarray # The embedding vector.

class Embedding:
    id: int = None # Primary key. Auto-generated and AUTO INCREMENT.
    source: str # Source of the embedding file.txt
    content_hash: str # Hash of the embedding file.txt contents.
    type: str # Type of the embedding. For filtering purposes.
    part_count: int # Number of parts of the embedding.

class InputType(Enum):
    """
    Represents the type of input for a network node.

    Attributes:
        TEXT (int): Represents text input.
        FILE_PATH (int): Represents input from a file path.
    """
    TEXT = 1
    FILE_PATH = 2

class CalculateMethod(Enum):
    """
    A class representing different calculation methods.

    Attributes:
        COSINE (int): Constant representing the cosine calculation method.
        EUCLIDEAN (int): Constant representing the Euclidean calculation method.
    """
    COSINE = 1
    EUCLIDEAN = 2

class Embedder:
    """
    A class that provides methods for embedding and searching text using a given model.
    """

    embed_dict = {}

    def __init__(self, model, vector_base, n_ctx):
        """
        Initializes an Embedder object.

        Args:
            model: The model used for embedding text.
        """
        self.model = model
        self.vector_base = vector_base
        self.n_ctx = n_ctx
        self.virt_io = {}


    def embed(self, input, inputType : InputType, content_hash : str = None, content_type : str = None):
            """
            Embeds the input data into an embedding object.

            Args:
                input: The input data to be embedded. It can be a file path or a string.
                inputType (InputType): The type of the input data.
                content_hash (str, optional): The hash value of the input data. Defaults to None.
                content_type (str, optional): The content type of the input data. Defaults to None.

            Raises:
                ValueError: If an invalid input type is provided.

            Returns:
                None
            """

            embedding = Embedding()

            match inputType:
                case InputType.FILE_PATH:
                    input = open(input, "r")
                    file_size = os.path.getsize(input.name)
                    embedding.source = input.name
                case InputType.TEXT:
                    while True:
                        embedding.source = "StringIO-" + str(np.random.randint(1, 10000000))
                        if self.virt_io.get(embedding.source) is None:
                            break
                    self.virt_io[embedding.source] = io.StringIO(input)
                    input = self.virt_io[embedding.source]
                    file_size = len(input.getvalue())
                case _:
                    raise ValueError("Invalid input type.")           

            embedding.part_count = file_size // self.n_ctx
            if file_size % self.n_ctx != 0:
                embedding.part_count += 1
            else:
                embedding.part_count = 1

            if content_hash == None:
                embedding.content_hash = Hasher.hash(input)
                input.seek(0) #reset the cursor!

            if content_type == None:
                embedding.type = "DEFAULT"

            embedding.id = self.vector_base.add_embedding(embedding)

            part_count = 0
            while True:
                content = input.read(self.n_ctx)
                if not content:
                    break

                part = EmbeddingPart()
                part.embedding_id = embedding.id
                part.index = part_count

                self.model.createModelResponse(content)
                part.embeds = self.model.getResponse(resultType=ResultType.EMBEDDING)

                self.vector_base.add_embedding_part(part)

                part_count += 1

            match inputType:
                case InputType.FILE_PATH:
                    input.close()
                case InputType.TEXT:
                    pass #Do not close StringIO! It breaks them.
                case _:
                    raise ValueError("Not implemented. This should not happen.")
    

    def get_file_context_from_part(self, Embedding, EmbeddingPart):
        """
        Retrieves the context from a file for a specific part of an embedding.

        Args:
            Embedding (object): The embedding object containing the source file information.
            EmbeddingPart (object): The embedding part object containing the index information.

        Returns:
            str: The context read from the file for the specified part.

        Raises:
            FileNotFoundError: If the source file specified in the embedding object does not exist.
        """
        if Embedding.source.startswith("StringIO"):
            return self.virt_io[Embedding.source].getvalue()
        else:
            try:
                with open(Embedding.source, "r") as file:
                    file.seek(EmbeddingPart.index * self.n_ctx)
                    return file.read(self.n_ctx)
            except FileNotFoundError:
                raise FileNotFoundError("The source file specified in the embedding object does not exist.")


    def find_best_matches(self, prompt, n_matches=3, method : CalculateMethod = CalculateMethod.COSINE) -> List[Tuple[Embedding, EmbeddingPart, float]]:
            """
            Finds the best matches for a given prompt by calculating the similarity between the prompt and each embedding part.

            Args:
                prompt (str): The prompt to find matches for.
                n_matches (int, optional): The number of best matches to return. Defaults to 3.
                method (CalculateMethod, optional): The method used to calculate similarity. Defaults to CalculateMethod.COSINE.

            Returns:
                List[Tuple[Embedding, EmbeddingPart, float]]: A list of tuples containing the best matches, where each tuple consists of an Embedding object, an EmbeddingPart object, and the similarity score.
            """

            self.model.createModelResponse(prompt)
            prompt_embedding = self.model.getResponse(resultType=ResultType.EMBEDDING)

            embeddings = self.vector_base.get_all_embeddings()
            best_matches = []

            for embedding in embeddings:
                for index in range(embedding.part_count):
                    part = self.vector_base.get_embedding_part(embedding.id, index)
                    if part is None: #How?
                        continue
                    similarity = self.calculate(prompt_embedding, part.embeds, method)
                    best_matches.append((embedding, part, similarity))
                    if len(best_matches) > (n_matches * 2):
                        best_matches.sort(key=lambda x: x[2], reverse=True)
                        best_matches = best_matches[:n_matches]
            
            best_matches.sort(key=lambda x: x[2], reverse=True)
            best_matches = best_matches[:n_matches]

            return best_matches
        
    def calculate(self, e1, e2, method):
            """
            Calculate the similarity or distance between two embeddings.

            Args:
                e1: The first embedding.
                e2: The second embedding.
                method: The method to use for calculation. Should be one of CalculateMethod.COSINE or CalculateMethod.EUCLIDEAN.

            Returns:
                The similarity or distance between the two embeddings.

            Raises:
                ValueError: If an invalid method is provided.
            """
            match method:
                case CalculateMethod.COSINE:
                    return self.cosine_similarity(e1, e2)
                case CalculateMethod.EUCLIDEAN:
                    return self.euclidean_distance(e1, e2)
                case _:
                    raise ValueError("Invalid method.")
        
    def euclidean_distance(self, e1, e2):
        """
        Calculate the Euclidean distance between two embeddings.

        Args:
            e1 (numpy.ndarray): The first embedding.
            e2 (numpy.ndarray): The second embedding.

        Returns:
            float: The Euclidean distance between the two embeddings.
        """
        e1_normalized = e1 / np.linalg.norm(e1)
        e2_normalized = e2 / np.linalg.norm(e2)
        euclidean_distance = np.linalg.norm(e1_normalized - e2_normalized)
        return 1 / (1 + euclidean_distance)

    def cosine_similarity(self, e1, e2):
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

    def print_virtio(self):
        for item in self.virt_io.items():
            print(f"VirtIO Item: {item[0], item[1].getvalue()}")
