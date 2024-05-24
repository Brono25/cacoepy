from cacoepy.core.exceptions import AlignSequencePairError
from typing import List, Tuple

def align_sequence_pairs(
        ref_a: List[str], 
        partner_a: List[str], 
        ref_b: List[str], 
        partner_b: List[str], 
        gap_char: str ="-"
        ) -> Tuple[List[str], List[str], List[str]]:
    """
    Align two pairs of sequences where ref_a and ref_b are the same sequence 
    with different padding.

    Parameters:
        ref_a (list): The reference sequence aligned with partner_a.
        partner_a (list): The sequence aligned to ref_a.
        ref_b (list): The reference sequence aligned with partner_b.
        partner_b (list): The sequence aligned to ref_b.
        gap_char (str): Character used to represent gaps in the alignments, default is '-'.
    Returns:
        aligned_reference_a: The globally aligned ref_a
        aligned_partner_a: The globally aligned parter of a.
        aligned_partner_b:  The globally aligned parter of b.
    """
    pair_a = list(zip(ref_a, partner_a))
    pair_b = list(zip(ref_b, partner_b))
    result_a, result_b = [], []
    if len(ref_a) != len(partner_a) or len(ref_b) != len(partner_b):
        raise AlignSequencePairError(
            "The ref_x and partner_x sequences must be the same length."
        )
    elif [x for x in ref_a if x != gap_char] != [x for x in ref_b if x != gap_char]:
        raise AlignSequencePairError(
            "The reference sequences ref_a and ref_b must be equal when padding is removed."
        )

    while pair_a or pair_b:
        if pair_a and pair_b:
            if pair_b[0][0] == pair_a[0][0]:
                result_a.append(pair_a.pop(0))
                result_b.append(pair_b.pop(0))
            elif pair_b[0][0] == gap_char:
                result_a.append((gap_char, gap_char))
                result_b.append(pair_b.pop(0))
            else:
                result_b.append((gap_char, gap_char))
                result_a.append(pair_a.pop(0))
        elif pair_a and not pair_b:
            result_b.append((gap_char, gap_char))
            result_a.append(pair_a.pop(0))
        else:
            result_a.append((gap_char, gap_char))
            result_b.append(pair_b.pop(0))

    aligned_ref_a, aligned_partner_a = zip(*result_a)
    aligned_ref_b, aligned_partner_b = zip(*result_b)

    if aligned_ref_a != aligned_ref_b:
        raise AlignSequencePairError(
            "Something went wrong. The reference sequences do not match after alignment."
        )
    return list(aligned_ref_a), list(aligned_partner_a), list(aligned_partner_b)
