import json
from cacoepy.core.ARPAbet_similarity_matrix import arpabet_similarity_matrix
from cacoepy.core.Needleman_Wunsch import NeedlemanWunsch2D, NeedlemanWunschConfig
from cacoepy.core.exceptions import ElementNotInVocabError
from cacoepy.core.aligner_tools import align_sequence_pairs


def align_prediction_to_annotation_and_target(
    prediction: list[str],
    annotation_aligned_with_target: list[str],
    target_aligned_with_annotation: list[str],
    gap_char="-",
    gap_penalty=-5,
):
    """
    Align the phoneme predictions from a Mispronunciation Diagnosis and Detection (MDD) system to annotated phonemes of mispronounced speech and their aligned target phonemes.
    """
    bare_annotation = list(filter(lambda x: x != gap_char, annotation_aligned_with_target))
    aligner = AlignARPAbet2(gap_penalty=gap_penalty)
    annotation_aligned_with_pred, pred_aligned_with_annotation, _ = aligner(
        bare_annotation, prediction
    )
    aligned_annotation, aligned_target, aligned_prediction =  align_sequence_pairs(
        ref_a=annotation_aligned_with_target,
        ref_b=annotation_aligned_with_pred,
        partner_a=target_aligned_with_annotation,
        partner_b=pred_aligned_with_annotation,
    )
    return aligned_prediction, aligned_annotation, aligned_target


class AlignBasic2:
    def __init__(self):
        self.gap_penalty = -1
        self.match_score = 1
        self.mismatch_score = -1
        self._score = None

        def _similarity_function(a, b):
            return 1 if a == b else -1

        self._config = NeedlemanWunschConfig(
            gap_penalty=self.gap_penalty, similarity=_similarity_function
        )
        self._needleman_wunsch2d = NeedlemanWunsch2D(config=self._config)

    def __call__(self, seq1, seq2):
        aligned_seq1, aligned_seq2, score = self._needleman_wunsch2d(
            seq1=seq1, seq2=seq2
        )
        self._score = score
        return aligned_seq1, aligned_seq2, score

    @property
    def score(self):
        return self._score


class AlignARPAbet2:
    def __init__(self, gap_penalty=-4):
        self._similarity_matrix = arpabet_similarity_matrix()
        self._vocab = self._load_vocab()
        self._config = NeedlemanWunschConfig(
            gap_penalty=gap_penalty, similarity=self._similarity_matrix
        )
        self._needleman_wunsch2d = NeedlemanWunsch2D(config=self._config)
        self._score = None

    def __call__(self, seq1, seq2):
        if self._is_phonemes_in_vocab(seq1) and self._is_phonemes_in_vocab(seq2):
            aligned_seq1, aligned_seq2, score = self._needleman_wunsch2d(
                seq1=seq1, seq2=seq2
            )
            self._score = score
            return aligned_seq1, aligned_seq2, score
        return None, None, None

    def _load_vocab(self):
        with open("data/ARPAbet_mapping.json", "r") as file:
            data = json.load(file)
        vocab = data["phoneme_attribute_map"].keys()
        return list(vocab)

    def _is_phonemes_in_vocab(self, seq):
        for phone in seq:
            if phone not in self._vocab:
                msg = f'A sequence contains "{phone}" which is not an ARPAbet phoneme.'
                raise ElementNotInVocabError(message=msg)
        return True

    @property
    def ARPABet_vocab(self):
        return self._vocab

    @property
    def similarity_matrix(self):
        return self._similarity_matrix

    @property
    def score(self):
        return self._score

    def __str__(self):
        return str(self._needleman_wunsch2d)


class AlignARPAbet3:
    def __init__(self, gap_penalty=4):
        pass
