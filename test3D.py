from cacoepy.ARPAbet_substitution_matrix import arpabet_substitution_matrix
from cacoepy.utils import pretty_matrices, pretty_sequences
from cacoepy.Needleman_Wunsch3D import NeedlemanWunsch3D
from cacoepy.Needleman_Wunsch import NeedlemanWunschConfig



def run(sa, sb, sc, aligner):
    a, b, c = aligner(sa, sb, sc)
    pretty_sequences(a, b, c)
    print("\n"*2)



if __name__ == "__main__":
    smatrix = arpabet_substitution_matrix()
    config = NeedlemanWunschConfig(gap_penalty=2, substitution=smatrix)
    aligner = NeedlemanWunsch3D(config)
    
    sa = "k ah m p y uw t er".split(" ")
    sb = "g ae b uw ow".split(" ")
    sc = "g ae b uw".split(" ")
    run(sa, sb, sc, aligner)

    sa = "hh eh l ih k aa p t er".split(" ")
    sb = "hh e l ih k aa p t er".split(" ")
    sc = "k eh l ih t aa d er".split(" ")
    run(sa, sb, sc, aligner)


    sa = "l eh m ah n ey d".split(" ")
    sb = "l eh v eh n".split(" ")
    sc = "n ae b er d ey".split(" ")
    run(sa, sb, sc, aligner)


    sa = "th er m aa m ah t er".split(" ")
    sb = "b m ih g ow".split(" ")
    sc = "t er m ao r er".split(" ")
    run(sa, sb, sc, aligner)


    sa = "g r ae s hh aa p er".split(" ")
    sb = "g uh b h ae p er".split(" ")
    sc = "d ae g hh ae t".split(" ")
    run(sa, sb, sc, aligner)


    sa = "b ae s k ah t b ao l".split(" ")
    sb = "b ih g ow".split(" ")
    sc = "p ay g er".split(" ")
    run(sa, sb, sc, aligner)

    sa = "b ae s k ah t b ao l".split(" ")
    sb = "b ih g ow".split(" ")
    sc = "p ay g er".split(" ")
    run(sa, sb, sc, aligner)


    sa = "t r eh zh er".split(" ")
    sb = "g aw w uh l".split(" ")
    sc = "g aw ah".split(" ")
    run(sa, sb, sc, aligner)


    sa = "d ay n ah s ao r".split(" ")
    sb = "d ih k ow".split(" ")
    sc = "t ay g er".split(" ")
    run(sa, sb, sc, aligner)