from cacoepy.aligner import align_prediction_to_annotation_and_target
from cacoepy.core.utils import pretty_sequences

target = "g r ae s hh aa p er".split(" ")
ann =    "g - uh b hh ae p er".split(" ")
pred = "ah b ae".split(" ")


a,b, c = align_prediction_to_annotation_and_target(pred, ann, target)

pretty_sequences(c, b, a)
