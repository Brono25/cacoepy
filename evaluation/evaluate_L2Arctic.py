import json
from cacoepy.aligner import AlignARPAbet2, AlignBasic2
from cacoepy.core.utils import pretty_sequences
import copy
from cacoepy.aligner import AlignBasic2

def load_json_to_dict(filename):
    with open(filename, "r") as file:
        return json.load(file)


def toggle_sil_to_dash(seq):
    new_seq = []
    for e in seq:
        if e == "sil":
            new_seq.append("-")
        elif e == "-":
            new_seq.append("sil")
        else:
            new_seq.append(e)
    return new_seq

def remove_alignment(a):
    a = [x for x in a if x != "-"]
    # a = [x for x in a if x != "sil"]
    return a


def evaluate_sequences(expected, aligned):
    aligner = AlignBasic2()
    res = aligner(expected, aligned)
    return aligner.score


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
    return aligned_src, aligned_dest, None


def run_test(target, perceived, aligner):
    unaligned_perceived = remove_alignment(perceived)
    unaligned_target = remove_alignment(target)
    aligned_target, aligned_perc, _ = aligner(unaligned_target, unaligned_perceived)
    score = evaluate_sequences(perceived, aligned_perc)
    score += evaluate_sequences(target, aligned_target)
    score += score
    return score


if __name__ == "__main__":
    from Levenshtein import editops  # pip install python-Levenshtein

    annotations = load_json_to_dict("data/L2Arctic_annotations.json")
    arpa_aligner = AlignARPAbet2()
    basic_aligner = AlignBasic2()
    arpabet_score = 0
    basic_score = 0
    levi_score = 0
    for file in annotations.keys():

        target = annotations[file]["target_phonemes"].replace("ax", "ah").split(" ")
        perceived = (
            annotations[file]["perceived_phonemes"].replace("ax", "ah").split(" ")
        )
        arpabet_score += run_test(target, perceived, arpa_aligner)
        basic_score += run_test(target, perceived, basic_aligner)
        levi_score += run_test(target, perceived, align_editops)

    print(f"{arpabet_score=} {basic_score=}, {levi_score=}")
    print(f"{((arpabet_score - basic_score) /arpabet_score) * 100 =}")
    print(f"{((arpabet_score - levi_score) /arpabet_score) * 100 =}")
