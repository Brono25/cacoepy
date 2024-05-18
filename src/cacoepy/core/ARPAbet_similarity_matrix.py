import numpy as np
import json


def arpabet_similarity_matrix():
    """
    Generates a similarity matrix for ARPAbet phonemes based on their attributes.

    This function constructs a phoneme similarity matrix by loading phoneme data from a JSON file,
    creating binary vectors for each phoneme based on their attributes, and then calculating similarity
    scores between each pair of phonemes using the cosine similarity method.

    Returns:
        dict: A dictionary where keys are phoneme pairs and values are their similarity scores.
    """
    def build_scoring_matrix():
        def load_phoneme_data(file):
            with open(file, "r") as file:
                data = json.load(file)
            return data

        def create_phoneme_vectors(attributes, phoneme_attribute_map):
            num_attributes = len(attributes)
            phoneme_vectors = {
                x: np.zeros(num_attributes, dtype=int)
                for x in phoneme_attribute_map
            }
            for phone in phoneme_vectors:
                for i, att in enumerate(attributes):
                    if att in phoneme_attribute_map[phone]:
                        phoneme_vectors[phone][i] = 1
            return phoneme_vectors

        def create_phoneme_similarity_matrix(phoneme_vectors):
            similarity_matrix = {}
            for pha, veca in phoneme_vectors.items():
                similarity_matrix[pha] = {}
                for phb, vecb in phoneme_vectors.items():
                    similarity_matrix[pha][phb] = phoneme_similarity_score(veca, vecb)
            return similarity_matrix

        def phoneme_similarity_score(vec_a: np.array, vec_b: np.array):
            norm_a = np.linalg.norm(vec_a)
            norm_b = np.linalg.norm(vec_b)
            if norm_a == 0 or norm_b == 0:
                return 0.0
            normaliser = 1 / (norm_a * norm_b)
            score = normaliser * np.dot(vec_a, vec_b)
            score = round((score - 0.5) * 20)
     
            return score

        data = load_phoneme_data("data/ARPAbet_mapping.json")
        attribute_list = (
                data["consonant_attributes"] + data["vowel_attributes"]
            )
        phoneme_attribute_map = data["phoneme_attribute_map"]
        vectors = create_phoneme_vectors(attribute_list, phoneme_attribute_map)
        matrix = create_phoneme_similarity_matrix(vectors)
        return matrix
    return  build_scoring_matrix()


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    data = arpabet_similarity_matrix()

    keys = list(data.keys())
    matrix = np.array([[data[row][col] for col in keys] for row in keys])

    # Use the 'dark_background' style
    plt.style.use("dark_background")

    # Plotting the matrix
    plt.figure(figsize=(8, 8))

    plt.imshow(matrix, cmap="inferno", interpolation="none")
    plt.colorbar()


    plt.xticks(ticks=np.arange(len(keys)), labels=keys)
    plt.yticks(ticks=np.arange(len(keys)), labels=keys)

    plt.title("ARPAbet Similarity Matrix", fontsize=25)
    plt.xlabel("Phonemes", fontsize=18)
    plt.ylabel("Phonemes", fontsize=18)
    plt.show()

    keys = data.keys()
    matrix = np.array([[data[row][col] for col in keys] for row in keys])

    
    plt.figure(figsize=(8, 8))
    plt.imshow(matrix, cmap="viridis", interpolation="none")
    plt.colorbar()


    plt.xticks(ticks=np.arange(len(keys)), labels=keys)
    plt.yticks(ticks=np.arange(len(keys)), labels=keys)

    plt.title("ARPAbet Similarity Matrix", fontsize=25)
    plt.xlabel("Phonemes", fontsize=18)
    plt.ylabel("Phonemes", fontsize=18)
    plt.show()
