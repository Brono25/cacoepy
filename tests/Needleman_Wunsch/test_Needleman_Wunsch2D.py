import pytest
from cacoepy.core.Needleman_Wunsch import NeedlemanWunsch2D, NeedlemanWunschConfig


def test_gap_penalties():
    """
    Checking if introducing gap insertions causes any indexing error.
    """

    def substitution_function(a, b):
        return 1 if a == b else -1

    seq1 = ["a"] * 10 + ["b"] * 10 + ["c"] * 10 + ["d"] * 10
    seq2 = "a b c d".split()

    for gp in [0, 1, 2, 3, 4, 5, 10, 15, 25, 50, 100]:
        config = NeedlemanWunschConfig(
            gap_penalty=gp, substitution=substitution_function
        )
        nw2d = NeedlemanWunsch2D(config=config)
        try:
            aligned_seq1, aligned_seq2 = nw2d(seq1, seq2)
        except Exception as e:
            pytest.fail(f"Test failed with gap_penalty={gp} due to exception: {e}")


def test_correct_output():
    test_cases = [
        ("GATTACA", "GTCGACGCA", 0, 1, -1, "G-T-CGACGCA", "GATT--AC--A"),
        ("GATTACA", "GTCGACGCA", 1, 1, -1, "G-TCGACGCA", "GATT-AC--A"),
    ]

    for i, (seq1, seq2, gap, match, mismatch, exp_seq1, exp_seq2) in enumerate(test_cases):
        seq1 = list(seq1)
        seq2 = list(seq2)
        exp_seq1 = list(exp_seq1)
        exp_seq2 = list(exp_seq2)

        def make_substitution_function(match, mismatch):
            def substitution_function(a, b):
                return match if a == b else mismatch
            return substitution_function

        substitution_function = make_substitution_function(match, mismatch)

        config = NeedlemanWunschConfig(
            gap_penalty=gap, substitution=substitution_function
        )
        nw_aligner = NeedlemanWunsch2D(config)
        out_seq1, out_seq2 = nw_aligner(seq1, seq2)
        assert out_seq1 == exp_seq1, f"CASE {i}:\nExpected: {exp_seq1}, \n     Got: {out_seq1}"
        assert out_seq2 == exp_seq2, f"CASE {i}:\nExpected: {exp_seq2}, \n     Got: {out_seq2}"


if __name__ == "__main__":
    test_correct_output()
