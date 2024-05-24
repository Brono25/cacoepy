# AlignARPAbet2 Implementation
The `AlignARPAbet2` uses the **Needleman-Wunsch** algorithm with a custom similarity matrix for assigning scores to phoneme pairs. To generate the similarity matrix, the phonemes are broken down into their 35 attributes, which describe how they are articulated. Each phoneme may have several attributes each (see `data/ARPAbet_mapping.json` for the breakdown). By signifying which attributes are present or not, each phoneme is represented as a vector in a 35-dimensional attribute space. Then, the cosine similarity is calculated between each pair of phoneme vectors and placed into a lookup table to be used to inform the **Needleman-Wunsch** algorithm during alignment.
A visual representation of the similarity matrix is shown below. The clear separation of consonants and vowels is apparent in the sub-squares.

<div align="center">
    <img src="../assets/ARPAbet_similarity_matrix_darkmode.png" alt="SimilarityMatrix" width="700" height="600">
</div>