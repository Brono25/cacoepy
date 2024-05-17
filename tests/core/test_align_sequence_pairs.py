import pytest
from cacoepy.core.aligner_tools import align_sequence_pairs
from cacoepy.core.exceptions import AlignSequencePairError


def test_reference_mismatch():
    ref_a = "a a".split(" ")
    partner_a = "x -".split(" ")
    ref_b = "a a - a".split(" ")
    partner_b = "x".split(" ")

    with pytest.raises(AlignSequencePairError):
        a, b, c = align_sequence_pairs(ref_a, partner_a, ref_b, partner_b)


def test_reference_partner_mismatch():
    ref_a = "a a".split(" ")
    partner_a = "x - -".split(" ")
    ref_b = "a a -".split(" ")
    partner_b = "x - x".split(" ")

    with pytest.raises(AlignSequencePairError):
        a, b, c = align_sequence_pairs(ref_a, partner_a, ref_b, partner_b)


def test_refa_refb_identical():
    ref_a = "a a a".split(" ")
    partner_a = "x - x".split(" ")
    ref_b = "a a a".split(" ")
    partner_b = "z z z".split(" ")
    a, b, c = align_sequence_pairs(ref_a, partner_a, ref_b, partner_b)

    exp_a = "a a a".split(" ")
    exp_b = "x - x".split(" ")
    exp_c = "z z z".split(" ")
    assert exp_a == a, f"Expected: {exp_a}, \n     Got: {a}"
    assert exp_b == b, f"Expected: {exp_b}, \n     Got: {b}"
    assert exp_c == c, f"Expected: {exp_c}, \n     Got: {c}"


def test_refa_shorter():
    ref_a = "a a a".split(" ")
    partner_a = "x - x".split(" ")
    ref_b = "a a - a".split(" ")
    partner_b = "z z - z".split(" ")
    a, b ,c = align_sequence_pairs(ref_a, partner_a, ref_b, partner_b)

    exp_a = "a a - a".split(" ")
    exp_b = "x - - x".split(" ")
    exp_c = "z z - z".split(" ")
    assert exp_a == a, f"Expected: {exp_a}, \n     Got: {a}"
    assert exp_b == b, f"Expected: {exp_b}, \n     Got: {b}"
    assert exp_c == c, f"Expected: {exp_c}, \n     Got: {c}"


def test_refb_shorter():
    ref_a = "a a a".split(" ")
    partner_a = "x - x".split(" ")
    ref_b = "a a - a".split(" ")
    partner_b = "z z - z".split(" ")
    a, c, b = align_sequence_pairs(ref_b, partner_b, ref_a, partner_a)

    exp_a = "a a - a".split(" ")
    exp_b = "x - - x".split(" ")
    exp_c = "z z - z".split(" ")
    assert exp_a == a, f"Expected: {exp_a}, \n     Got: {a}"
    assert exp_b == b, f"Expected: {exp_b}, \n     Got: {b}"
    assert exp_c == c, f"Expected: {exp_c}, \n     Got: {c}"


def test_refa_much_shorter():
    ref_a = "- a - a - a -".split(" ")
    partner_a = "- x - x - x -".split(" ")
    ref_b = "- - - a - - - - a - - - - a - - -".split(" ")
    partner_b = "- - - z - - - - z - - - - z - - -".split(" ")
    a, b, c = align_sequence_pairs(ref_a, partner_a, ref_b, partner_b)

    exp_a = "- - - a - - - - a - - - - a - - -".split(" ")
    exp_b = "- - - x - - - - x - - - - x - - -".split(" ")
    exp_c = "- - - z - - - - z - - - - z - - -".split(" ")
    assert exp_a == a, f"Expected: {exp_a}, \n     Got: {a}"
    assert exp_b == b, f"Expected: {exp_b}, \n     Got: {b}"
    assert exp_c == c, f"Expected: {exp_c}, \n     Got: {c}"


def test_refb_much_shorter():
    ref_a = "- a - a - a -".split(" ")
    partner_a = "- x - x - x -".split(" ")
    ref_b = "- - - a - - - - a - - - - a - - -".split(" ")
    partner_b = "- - - z - - - - z - - - - z - - -".split(" ")
    a, b, c = align_sequence_pairs(ref_b, partner_b, ref_a, partner_a)

    exp_a = "- - - a - - - - a - - - - a - - -".split(" ")
    exp_b = "- - - z - - - - z - - - - z - - -".split(" ")
    exp_c =  "- - - x - - - - x - - - - x - - -".split(" ")
    assert exp_a == a, f"Expected: {exp_a}, \n     Got: {a}"
    assert exp_b == b, f"Expected: {exp_b}, \n     Got: {b}"
    assert exp_c == c, f"Expected: {exp_c}, \n     Got: {c}"


