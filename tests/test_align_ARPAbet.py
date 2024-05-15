import pytest
from cacoepy.aligner import AlignARPAbet2
from cacoepy.core.exceptions import ElementNotInVocabError

def test_phoneme_not_in_vocab():
    aligner = AlignARPAbet2()
    seq1 = "y ow y x".split(" ")
    seq2 = "y ow y ow".split(" ")

    with pytest.raises(ElementNotInVocabError):
        aligner(seq1, seq2)


def test_correct_output():
    test_cases = [
        ("dh ah m", "d iy ah m", 0, "dh - ah m", "d iy ah m"),
        ("dh ah m", "d iy ah m", -1, "dh - ah m", "d iy ah m"),
        ("dh ah m", "d iy ah m", -4, "dh - ah m", "d iy ah m"),
        ("d ay n ah s ao r", "d ih k ow", -4, "d ay n ah s ao r", "d - - ih k ow -"),
        ("d ay n ah s ao r", "d", -4, "d ay n ah s ao r", "d - - - - - -"),
        ("d", "d ay n ah s ao r", -4, "d - - - - - -", "d ay n ah s ao r"),
        ("d ay n ah s ao r", "ow", -4, "d ay n ah s ao r", "- ow - - - - -"),
        #("ow", "d ay n ah s ao r", -4, "- ow - - - - - -", "d ay n ah s ao r"),
    ]

    for i, (seq1, seq2, gap, exp_seq1, exp_seq2) in enumerate(test_cases):
        seq1 = seq1.split(" ")
        seq2 = seq2.split(" ")
        exp_seq1 = exp_seq1.split(" ")
        exp_seq2 = exp_seq2.split(" ")

        nw_aligner = AlignARPAbet2(gap_penalty=gap)
        out_seq1, out_seq2, _ = nw_aligner(seq1, seq2)

        assert (
            out_seq1 == exp_seq1
        ), f"CASE {i}:\nExpected: {exp_seq1}, \n     Got: {out_seq1}"
        assert (
            out_seq2 == exp_seq2
        ), f"CASE {i}:\nExpected: {exp_seq2}, \n     Got: {out_seq2}"
