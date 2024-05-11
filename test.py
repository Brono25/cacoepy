from cacoepy.ARPAbet_substitution_matrix import arpabet_substitution_matrix
from cacoepy.Needleman_Wunsch import NeedlemanWunsch, NeedlemanWunschConfig
from cacoepy.utils import pretty_sequences


def compare_schemes(seq1, seq2, basic_aligner, arpabet_aligner):
    basic_seq1, basic_seq2 = basic_aligner(seq2, seq1)
    arpa_seq1, arpa_seq2 = arpabet_aligner(seq2, seq1)
    print("Basic:")
    pretty_sequences(basic_seq1, basic_seq2)
    print()
    print("Custom:")
    pretty_sequences(arpa_seq1, arpa_seq2)
    print()

if __name__ == "__main__":

    def basic_score_method(a, b):
        if a == b:
            return 5
        else:
            return -5

    gap_penalty = 4

    basic_config = NeedlemanWunschConfig(gap_penalty=gap_penalty, substitution=basic_score_method)
    basic_aligner = NeedlemanWunsch(config=basic_config)

    arpabet_matrix = arpabet_substitution_matrix()
    arpabet_config = NeedlemanWunschConfig(gap_penalty=gap_penalty, substitution=arpabet_matrix)
    arpabet_aligner = NeedlemanWunsch(config=arpabet_config)

    seq1 = "dh ah m".split(" ")
    seq2 = "d iy ah m".split(" ")
    compare_schemes(seq1, seq2, basic_aligner, arpabet_aligner)

    seq1 = "k ah m p y uw t er".split(" ")
    seq2 = "g ae b uw ow".split(" ")
    compare_schemes(seq1, seq2, basic_aligner, arpabet_aligner)

    seq1 = "d ay n ah s ao r".split(" ")
    seq2 = "d ih k ow".split(" ")
    compare_schemes(seq1, seq2, basic_aligner, arpabet_aligner)

    seq1 = "k ih ng".split(" ")
    seq2 = "k ey n th".split(" ")
    compare_schemes(seq1, seq2, basic_aligner, arpabet_aligner)

    seq1 = "s w ih ng".split(" ")
    seq2 = "sh ih ng".split(" ")
    compare_schemes(seq1, seq2, basic_aligner, arpabet_aligner)

    seq1 = "s k uw l".split(" ")
    seq2 = "g w uh l".split(" ")
    compare_schemes(seq1, seq2, basic_aligner, arpabet_aligner)

    seq1 = "th er m aa m ah t er".split(" ")
    seq2 = "th ah m aa m ah d ao r".split(" ")
    compare_schemes(seq1, seq2, basic_aligner, arpabet_aligner)

    seq1 = "hh eh l ih k aa p t er".split(" ")
    seq2 = "hh eh l ih k aa p d aa ng".split(" ")
    compare_schemes(seq1, seq2, basic_aligner, arpabet_aligner)

    seq1 = "b ae s k ah t b ao l".split(" ")
    seq2 = "b ae s ih n b aa".split(" ")
    compare_schemes(seq1, seq2, basic_aligner, arpabet_aligner)

    seq1 = "b ae s k ah t b ao l".split(" ")
    seq2 = "b ae s ih b ao".split(" ")
    compare_schemes(seq1, seq2, basic_aligner, arpabet_aligner)

    seq1 = "s w ih ng".split(" ")
    seq2 = "sh n iy n k".split(" ")
    compare_schemes(seq1, seq2, basic_aligner, arpabet_aligner)

    seq1 = "g ey t".split(" ")
    seq2 = "g ae n k".split(" ")
    compare_schemes(seq1, seq2, basic_aligner, arpabet_aligner)

    seq1 = "t r eh zh er".split(" ")
    seq2 = "d r eh g ih t".split(" ")
    compare_schemes(seq1, seq2, basic_aligner, arpabet_aligner)

    seq1 = "th er m aa m ah t er".split(" ")
    seq2 = "uw ao m eh d er".split(" ")
    compare_schemes(seq1, seq2, basic_aligner, arpabet_aligner)

    seq1 = "eh l ah f ah n t".split(" ")
    seq2 = "eh l ah f ih".split(" ")
    compare_schemes(seq1, seq2, basic_aligner, arpabet_aligner)

    seq1 = "th er m aa m ah t er".split(" ")
    seq2 = "r ae m ih d ah".split(" ")
    compare_schemes(seq1, seq2, basic_aligner, arpabet_aligner)

    # print(arpabet_aligner)
    print(arpabet_matrix["r"]["m"])
    print(arpabet_matrix["r"]["er"])
