import os
import json
from cacoepy.core.ARPAbet_substitution_matrix import arpabet_substitution_matrix
from core.Needleman_Wunsch import NeedlemanWunsch2D, NeedlemanWunschConfig
from cacoepy.core.exceptions import ElementNotInVocabError



class AlignARPAbet2:
    def __init__(self, gap_penalty=4):
        self._substitution_matrix = arpabet_substitution_matrix()
        self._vocab = self._load_vocab()
        self._config = NeedlemanWunschConfig(
            gap_penalty=gap_penalty, substitution=self._substitution_matrix
            )
        self._needleman_wunsch2d = NeedlemanWunsch2D(config=self._config)

    def __call__(self, seq1, seq2):
        if self._is_phonemes_in_vocab(seq1) and self._is_phonemes_in_vocab(seq2):
            aligned_seq1, aligned_seq2 = self._needleman_wunsch2d(seq1=seq1, seq2=seq2)
            return aligned_seq1, aligned_seq2
        return None, None
    
    def _load_vocab(self):
        with open("data/ARPAbet_mapping.json", 'r') as file:
            data = json.load(file)
        vocab = data["phoneme_attribute_map"].keys()
        return list(vocab)
    
    def _is_phonemes_in_vocab(self, seq):  
        for phone in seq:
            if phone not in self._vocab:
                msg = f"A sequence contains \"{phone}\" which is not an ARPAbet phoneme."
                raise ElementNotInVocabError(message=msg, element=phone)
        return True

    @property
    def ARPABet_vocab(self):
        return self._vocab

    @property
    def substitution_matrix(self):
        return self._substitution_matrix

