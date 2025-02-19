# cacoepy
**cacoepy** *noun* [ *kuh-koh-uh-pee* ]  
*Bad or incorrect pronunciation.*  

A collection of tools I have developed—or plan to develop—to assist in working with mispronunciation detection and diagnosis (MDD) systems.

___

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install cacopey.

```bash
pip install cacoepy
```

## Usage
### AlignARPAbet2
The `AlignARPAbet2` class is used to align two sequences of ARPAbet phonemes, taking into account phoneme similarities. Typically sequence aligners focus on identifying matches and mismatches. However, for a more realistic alignment of phonemes in mispronounced speech versus the intended phonemes, it is important to consider the similarity between phoneme pairs.
<br>
When creating the instance, specify a gap penalty. A more negative value discourages the insertion of gaps.
```python
from cacoepy.aligner import AlignARPAbet2
from cacoepy.core.utils import pretty_sequences

aligner = AlignARPAbet2(gap_penalty=-4)
target_phonemes = "th er m aa m ah t er".split(" ")
mispronounced_phonemes = "uw ao m eh d er".split(" ")

aligned_mispronounced, aligned_target, score = aligner(mispronounced_phonemes, target_phonemes)
pretty_sequences(aligned_target, aligned_mispronounced)
```

**Output**:
```bash
th  er  m  aa  m  ah  t  er
-   uw  -  ao  m  eh  d  er
```
In this example, many of the phonemes are substituted or deleted in this child’s transcription of “thermometer.” Despite this, the `AlignARPAbet2` has found a good alignment by factoring in the similarities between pairs such as *er* and *uw*. For comparison, the Python package `Levenshtein editops` alignment of the same sequences was:

```
th  er  m  aa  m  ah  t  er
uw  ao  m  eh  d  -   -  er
```
Where it only aligns based on exact matches.

### Implementation Details
The `AlignARPAbet2` tool uses the **Needleman-Wunsch** algorithm with a custom similarity matrix to score phoneme pairs. This matrix is created by breaking phonemes down into **35 articulatory attributes** that describe how they are produced. Each phoneme is represented as a **35-dimensional one-hot encoded vector**, where each dimension corresponds to the presence (1) or absence (0) of a specific attribute (see [`ARPAbet_mapping.json`](data/ARPAbet_mapping.json) for details).  
The **cosine similarity** between these vectors is calculated for every phoneme pair and stored in a lookup table. This table helps the **Needleman-Wunsch** algorithm align phonemes more accurately.  
The visual representation below shows the similarity matrix, where consonants and vowels form distinct sub-groups.  

<p align="center">
  <a href="assets/ARPAbet_similarity_matrix_darkmode.png" target="_blank">
    <img src="assets/ARPAbet_similarity_matrix_darkmode.png" alt="Similarity Matrix" width="400">
  </a>
</p>

To use the scoring matrix with a different alignment algorithm, you can access the similarity matrix in JSON format [here](data/arpabet_similarity.json). Alternatively, you can generate the similarity matrix by running this [script](src/cacoepy/core/ARPAbet_similarity_matrix.py).


### align_prediction_to_annotation_and_target
Given three sets of phoneme sequences:
- `target`: The phonemes the speaker is attempting to say.
- `annotation`: The annotation of how the speaker pronounced the target.
- `prediction`: The output of an MDD system predicting what the speaker said.
<br>
This function aligns the prediction sequence to the annotation sequence while preserving the existing alignment between annotation and target.

```python
from cacoepy.aligner import align_prediction_to_annotation_and_target
from cacoepy.core.utils import pretty_sequences

target = "th er m aa m ah t er".split(" ")
annotation = "- uw - ao m eh d er".split(" ")
prediction = "uw aa ao m eh d uh er".split(" ")

aligned_pred, aligned_ann, aligned_tar = align_prediction_to_annotation_and_target(
    target_aligned_with_annotation=target,
    annotation_aligned_with_target=annotation,
    prediction=prediction,
)
pretty_sequences(aligned_tar, aligned_ann, aligned_pred)
```
**Output**
```bash
th  er  m   aa  m  ah  t  -   er
-   uw  -   ao  m  eh  d  -   er
-   uw  aa  ao  m  eh  d  uh  er
```

## Future Features
- `AlignARPAbet3` - Aligns 3 sets of phonemes.
- `mdd_phoneme_metrics` - Evaluation metrics for MDD systems.




## License

[MIT](https://choosealicense.com/licenses/mit/)
