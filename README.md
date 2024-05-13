# cacoepy
cacoepy is a toolkit designed for aligning sequences of phonemes, considering phoneme similarities. It was created to aid in the evaluation of mispronunciation diagnosis detection (MDD) systems, where a speaker's mispronunciations of a word at the phoneme level are evaluated against the target word's phonemes. This process requires alignment methods that factor in the similarities between certain phonemes.

**Motivation:** Sequence alignment typically identifies matches and mismatches to find the optimal alignment. However, aligning mispronounced word phonemes to target phonemes requires a method that incorporates phoneme similarities to achieve a more realistic fit.
___

## Installation
Download this repository and then run:
`pip install .`


## Method
The alignment tools in this package use the **Needleman-Wunsch** algorithm in conjunction with a custom phoneme similarity matrix for assigning a similarity score between each phoneme pair. Currently only the ARPAbet phonemes are supported.

The similarity matrix is constructed by breaking each phoneme into 34 attribute componants. Then each phoneme is represented as a vector in an attribute space. Each pairing of vectors has there cosine similiarty calculated and placed into a 2D matrix which can be used as a lookup table.



