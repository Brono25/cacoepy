from cacoepy.core.Needleman_Wunsch import NeedlemanWunsch2D, NeedlemanWunschConfig
import random
from cacoepy.core.ARPAbet_similarity_matrix import arpabet_similarity_matrix
from cacoepy.aligner import AlignARPAbet2
from Levenshtein import editops
import copy
from cacoepy.core.utils import pretty_sequences

def align_editops(source_seq, dest_seq):
    vocab = set(source_seq + dest_seq)
    w2c = {c: i for i, c in enumerate(vocab)}
    source_enc = "".join([chr(w2c[c]) for c in source_seq])
    dest_enc = "".join([chr(w2c[c]) for c in dest_seq])
    aligned_src = copy.deepcopy(source_seq)
    aligned_dest = copy.deepcopy(dest_seq)
    for op, src_idx, dest_idx in editops(source_enc, dest_enc):
        if op == "replace":
            continue
        elif op == "insert":
            aligned_src.insert(dest_idx, "-")
        elif op == "delete":
            aligned_dest.insert(src_idx, "-")
    return aligned_src, aligned_dest

    # Example usage
seq1 = "th er m aa m ah t er".split(" ")
seq2 = "uw ao m eh d er".split(" ")
a, b = align_editops(seq1, seq2)
pretty_sequences(a, b)

print()

aligner = AlignARPAbet2(gap_penalty=-4)
a,b, _ = aligner(seq1, seq2)
pretty_sequences(a, b)
