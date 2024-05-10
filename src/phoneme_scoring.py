import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

_PLACES_OF_ARTICULATION = [
    "alveolar",
    "palatal",
    "glottal",
    "dental",
    "labial",
    "bilabial",
    "labiodental",
    "coronal",
    "dorsal",
    "anterior",
    "posterior",
]
_MANNER_OF_ARTICULATION = [
    "semivowel",
    "fricative",
    "nasal",
    "stop",
    "approximant",
    "affricate",
    "liquid",
    "retroflex",
    "velar",
    "sonorant",
    "obstruent",
    "continuant",
]
_CONSONANT_ATTRIBUTES = _PLACES_OF_ARTICULATION + _MANNER_OF_ARTICULATION
_VOWEL_ATTRIBUTES = [
    "long",
    "short",
    "low",
    "mid",
    "high",
    "front",
    "central",
    "back",
    "round",
    "diphthong",
]

ATTRIBUTES = ["voiced"] + _CONSONANT_ATTRIBUTES + _VOWEL_ATTRIBUTES

# fmt: off
PHONEME_ATTRIBUTE_MAP = {
    # Consonants
    "b": ["labial", "bilabial", "anterior", "stop", "obstruent", "voiced"],
    "ch": ["palatal", "coronal", "posterior", "affricate", "obstruent"],
    "d": ["alveolar", "coronal", "anterior", "stop", "obstruent", "voiced"],
    "g": ["dorsal", "posterior", "stop", "velar", "obstruent", "voiced"],
    "jh": ["palatal", "coronal", "posterior", "affricate", "obstruent", "voiced"],
    "k": ["dorsal", "posterior", "stop", "velar", "obstruent"],
    "p": ["labial", "bilabial", "anterior", "stop", "obstruent"],
    "t": ["alveolar", "coronal", "anterior", "stop", "obstruent"],
    "dh": ["dental", "coronal", "anterior", "fricative", "obstruent", "continuant","voiced"],
    "f": ["labial", "labiodental", "coronal", "anterior", "fricative", "obstruent", "continuant"],
    "hh": ["glottal",  "dorsal","posterior", "fricative", "obstruent","continuant"],
    "l": ["alveolar", "coronal", "anterior", "approximant","liquid", "sonorant", "continuant","voiced"],
    "m": ["labial", "bilabial", "anterior", "nasal", "sonorant", "continuant", "voiced"],
    "n": ["alveolar", "coronal", "anterior", "nasal", "sonorant", "continuant", "voiced"],
    "ng": ["dorsal", "posterior", "nasal", "velar", "sonorant", "continuant", "voiced"],
    "r": ["alveolar", "coronal", "anterior", "approximant", "liquid", "retroflex", "sonorant", "continuant", "voiced"],
    "s": ["alveolar", "coronal", "anterior", "fricative", "obstruent", "continuant"],
    "sh": ["palatal", "coronal", "posterior", "fricative", "obstruent", "continuant"],
    "th": ["dental", "coronal", "anterior", "fricative", "obstruent", "continuant"],
    "v": ["labial", "labiodental","coronal", "anterior", "fricative", "obstruent", "continuant", "voiced"],
    "w": ["labial", "bilabial", "anterior", "semivowel", "approximant","sonorant", "continuant", "voiced"],
    "y": ["palatal", "coronal", "posterior", "semivowel",  "approximant","sonorant", "continuant", "voiced"],
    "z": ["alveolar", "coronal", "anterior", "fricative", "obstruent", "continuant", "voiced"],
    "zh": ["palatal", "coronal", "posterior", "fricative", "obstruent", "continuant", "voiced"],
    # Vowels
    "aa": ["long", "low", "back", "voiced"],
    "ae": ["long", "low", "front", "voiced"],
    "ah": ["short", "mid", "back", "voiced"],
    "ao": ["long", "mid", "back", "round", "voiced"],
    "eh": ["short", "mid", "front", "voiced"],
    "er": ["short", "mid", "central", "voiced"],
    "ih": ["short", "high", "front", "voiced"],
    "iy": ["long", "high", "front", "voiced"],
    "uh": ["short", "high", "back", "round", "voiced"],
    "uw": ["long", "high", "back", "round", "voiced"],
    "aw": ["long", "low", "central", "round", "diphthong", "voiced"],
    "ay": ["long", "low", "central", "diphthong", "voiced"],
    "ey": ["long", "mid", "front", "diphthong", "voiced"],
    "ow": ["long", "mid", "central", "round", "diphthong", "voiced"],
    "oy": ["long", "mid", "back", "round", "diphthong", "voiced"]
}
# fmt: on


def phoneme_similarity_score(vec_a: np.array, vec_b: np.array):
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    normaliser = 1 / (norm_a * norm_b)
    score = normaliser * np.dot(vec_a, vec_b)
    score = round((score - 0.5) * 20)
    return score


def create_phoneme_vectors():
    phoneme_vectors = {
        x: np.zeros(len(ATTRIBUTES), dtype=int) for x in PHONEME_ATTRIBUTE_MAP
    }
    for phone in phoneme_vectors:
        for i, att in enumerate(ATTRIBUTES):
            if att in PHONEME_ATTRIBUTE_MAP[phone]:
                phoneme_vectors[phone][i] = 1
    return phoneme_vectors


def create_phoneme_similarity_matrix():
    phoneme_vectors = create_phoneme_vectors()
    similarity_matrix = {}
    for pha, veca in phoneme_vectors.items():
        similarity_matrix[pha] = {}
        for phb, vecb in phoneme_vectors.items():
            similarity_matrix[pha][phb] = phoneme_similarity_score(veca, vecb)
    return similarity_matrix

if __name__ == "__main__":
    similarity_matrix = create_phoneme_similarity_matrix()
    df = pd.DataFrame.from_dict(similarity_matrix, orient='index').reset_index(drop=True)
    print(df.to_string(index=False))


"""
# Visualize the similarity matrix
plt.imshow(similarity_matrix, cmap="viridis", interpolation="nearest")
plt.colorbar()
plt.title("Phoneme Similarity Matrix")
plt.xlabel("Phonemes")
plt.ylabel("Phonemes")
plt.xticks(
    ticks=np.arange(len(phoneme_vectors)), labels=phoneme_vectors.keys(), rotation=90
)
plt.yticks(ticks=np.arange(len(phoneme_vectors)), labels=phoneme_vectors.keys())
plt.show()
"""
