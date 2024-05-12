from cacoepy.align_ARPAbet import AlignARPAbet2
from cacoepy.core.utils import pretty_sequences


aligner = AlignARPAbet2()



seq1 = "dh ah m".split(" ")
seq2 = "d iy ah m".split(" ")
a, b = aligner(seq1, seq2)

pretty_sequences(a, b)
