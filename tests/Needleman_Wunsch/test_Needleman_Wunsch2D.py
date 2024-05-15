import pytest
from cacoepy.core.Needleman_Wunsch import NeedlemanWunsch2D, NeedlemanWunschConfig
from cacoepy.core.utils import pretty_sequences


@pytest.fixture
def setup_aligner():
    def _setup(gap, match, mismatch):
        def make_similarity_function(match, mismatch):
            def similarity_function(a, b):
                return match if a == b else mismatch

            return similarity_function

        sf = make_similarity_function(match, mismatch)
        config = NeedlemanWunschConfig(gap_penalty=gap, similarity=sf)
        return NeedlemanWunsch2D(config)

    return _setup


def test_gap_penalties():
    """
    Checking if introducing gap insertions causes any indexing error.
    """

    def similarity_function(a, b):
        return 1 if a == b else -1

    seq1 = ["a"] * 10 + ["b"] * 10 + ["c"] * 10 + ["d"] * 10
    seq2 = "a b c d".split()

    for gp in [0, 1, 2, 3, 4, 5, 10, 15, 25, 50, 100]:
        config = NeedlemanWunschConfig(gap_penalty=gp, similarity=similarity_function)
        nw2d = NeedlemanWunsch2D(config=config)
        try:
            aligned_seq1, aligned_seq2, _ = nw2d(seq1, seq2)
        except Exception as e:
            pytest.fail(f"Test failed with gap_penalty={gp} due to exception: {e}")


def test_identical(setup_aligner):
    """
    Testing alignment of identical sequences.
    """
    seq1 = list("AGTC")
    seq2 = seq1
    exp_seq1 = seq1
    exp_seq2 = seq1
    aligner = setup_aligner(gap=0, match=1, mismatch=-1)
    aligned_seq1, aligned_seq2, score = aligner(seq1, seq2)
    assert score == 4
    assert aligned_seq1 == exp_seq1, f"Expected: {exp_seq1}, \n     Got: {aligned_seq1}"
    assert aligned_seq2 == exp_seq2, f"Expected: {exp_seq2}, \n     Got: {aligned_seq2}"


def test_all_different(setup_aligner):
    """
    Testing alignment of identical sequences.
    """
    seq1 = list("AGA")
    seq2 = list("XY")
    exp_seq1 = "AGA"
    exp_seq2 = ["-XY", "X-Y", "XY-"]
    aligner = setup_aligner(gap=-1, match=1, mismatch=-1)
    aligned_seq1, aligned_seq2, score = aligner(seq1, seq2)
    print(aligned_seq2)
    assert score == -3
    assert ("").join(
        aligned_seq1
    ) == exp_seq1, f"Expected: {exp_seq1}, \n     Got: {aligned_seq1}"
    assert ("").join(
        aligned_seq2
    ) in exp_seq2, f"Expected: {exp_seq2}, \n     Got: {aligned_seq2}"


def test_repeats(setup_aligner):
    """
    Testing alignment of identical sequences.
    """
    seq1 = list("ATAT")
    seq2 = list("AT")
    exp_seq1 = "ATAT"
    exp_seq2 = ["--AT", "A--T", "AT--"]
    aligner = setup_aligner(gap=-1, match=1, mismatch=-1)
    aligned_seq1, aligned_seq2, score = aligner(seq1, seq2)

    assert score == 0
    assert ("").join(
        aligned_seq1
    ) == exp_seq1, f"Expected: {exp_seq1}, \n     Got: {aligned_seq1}"
    assert ("").join(
        aligned_seq2
    ) in exp_seq2, f"Expected: {exp_seq2}, \n     Got: {aligned_seq2}"


def test_endgaps(setup_aligner):
    """
    Testing alignment of identical sequences.
    """
    seq1 = list("AAAATTTT")
    seq2 = list("TTTTGGGG")
    exp_seq1 = "AAAATTTT----"
    exp_seq2 = ["----TTTTGGGG"]
    aligner = setup_aligner(gap=-1, match=1, mismatch=-1)
    aligned_seq1, aligned_seq2, score = aligner(seq1, seq2)

    assert score == -4
    assert ("").join(
        aligned_seq1
    ) == exp_seq1, f"Expected: {exp_seq1}, \n     Got: {aligned_seq1}"
    assert ("").join(
        aligned_seq2
    ) in exp_seq2, f"Expected: {exp_seq2}, \n     Got: {aligned_seq2}"


def test_palindrone(setup_aligner):
    """
    Testing alignment of identical sequences.
    """
    seq1 = list("AGCTTGA")
    seq2 = list("AGCTGA")
    exp_seq1 = "AGCTTGA"
    exp_seq2 = ["AGC-TGA", "AGCT-GA"]
    aligner = setup_aligner(gap=0, match=1, mismatch=-1)
    aligned_seq1, aligned_seq2, score = aligner(seq1, seq2)

    assert score == 6
    assert ("").join(
        aligned_seq1
    ) == exp_seq1, f"Expected: {exp_seq1}, \n     Got: {aligned_seq1}"
    assert ("").join(
        aligned_seq2
    ) in exp_seq2, f"Expected: {exp_seq2}, \n     Got: {aligned_seq2}"


def test_various_scores(setup_aligner):
    test = [
        ("PNRXJBZKYTGGTPGF", "XBNSWZHOVSSFWE", -2, -16),
        ("UROXNISDQJXCNRQHBR", "XBNSWZHOVSS", -3, -28),
        ("U", "XBNSWZHOVSSFWE", 0, 0),
        ("U", "XBNSWZHOVSSFWE", -1, -14),
        ("OTBZGXSEBLHCR", "IEXUIQQD", 1, 21),
        ("OTBZGXSEBLHCR", "IEXUIQQD", 0, 1),
        ("OTBZGXSEBLHCR", "IEXUIQQD", -1, -11),
        ("OTBZGXSEBLHCR", "IEXUIQQD", -2, -16),
        ("HREFGYGVRGAZJ", "QNQYIASB", 0, 2),
        ("HREFGYGVRGAZJ", "QNQYIASB", -1, -9),
        ("HREFGYGVRGAZJ", "QNQYIASB", -10, -54),
    ]

    for a, b , gap, exp_score in test:
        aligner = setup_aligner(gap=gap, match=1, mismatch=-1)
        a, b, score = aligner(list(a), list(b))
        assert score == exp_score, f"Expected: {exp_score}, \n     Got: {score}"


