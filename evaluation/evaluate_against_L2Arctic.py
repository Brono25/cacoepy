import json
from cacoepy.aligner import AlignARPAbet2, AlignBasic2
from cacoepy.core.utils import pretty_sequences
import sys
from Levenshtein import editops  # pip install python-Levenshtein
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
    output_operations = copy.deepcopy(source_seq)
    adjustments = 0

    for op, src_idx, dest_idx in editops(source_enc, dest_enc):
        adjusted_idx = src_idx + adjustments

        if op == "replace":
            output_operations[adjusted_idx] = dest_seq[dest_idx]
        elif op == "insert":
            output_operations.insert(adjusted_idx, dest_seq[dest_idx])
            adjustments += 1
        elif op == "delete":
            output_operations.pop(adjusted_idx)
            adjustments -= 1

    return output_operations


if __name__ == "__main__":

    annotations = load_json_to_dict("data/L2Arctic_annotations.json")
    aligner = AlignARPAbet2()
    basic = AlignBasic2()
    arpabet_score = 0
    basic_score = 0
    for file in annotations.keys():

        target = annotations[file]["target_phonemes"].replace("ax", "ah").split(" ")
        expected_alignment = (
            annotations[file]["perceived_phonemes"].replace("ax", "ah").split(" ")
        )
        unaligned_expected = remove_alignment(expected_alignment)
        unaligned_target = remove_alignment(target)

        arpabet_target, arpabet_aligned = aligner(unaligned_target, unaligned_expected)
        score = evaluate_sequences(expected_alignment, arpabet_aligned)
        arpabet_score += score
        score = evaluate_sequences(target, arpabet_target)
        arpabet_score += score

        basic_target, basic_aligned = basic(unaligned_target, unaligned_expected)
        score = evaluate_sequences(expected_alignment, basic_aligned)
        basic_score += score
        score = evaluate_sequences(target, basic_target)
        basic_score += score

        levi_aligned = align_editops(unaligned_target, unaligned_expected)
        # num_correct, num_incorrect, total = evaluate_sequences(
        #    expected_alignment, levi_aligned
        # )
        # basic_correct += num_correct
        # basic_incorrect += num_incorrect
        # basic_total += total
        if basic_aligned == expected_alignment and False:
            c += 1
            pretty_sequences(target, expected_alignment)
            print()
            pretty_sequences(basic_target, basic_aligned)
            print()
            pretty_sequences(arpabet_target, arpabet_aligned)
            print("\n"*2)

    print(f"{arpabet_score=} {basic_score=}")
    print(f"{((arpabet_score - basic_score) /arpabet_score) * 100 =}")
