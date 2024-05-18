"""
1. True-Acceptances , which represent the number of times a recognised
phoneme matches a correctly pronounced phoneme.
2. True-Rejections , which represent the number of times a recognised
phoneme is different from a mispronounced phoneme.
3. False-Acceptances , which represent the number of times a recognised
phoneme matches a mispronounced phoneme.
4. False-Rejections, which represent the number of times a recognised
phoneme is different from a correctly pronounced phoneme.
"""
from cacoepy.core.exceptions import PhonemeSequenceError
from typing import List, Dict


def mdd_phoneme_metrics(
        target: List[str], 
        annotation: List[str], 
        prediction: List[str]
        ) -> Dict:
    
    if not (len(target) == len(annotation) == len(prediction)):
        raise PhonemeSequenceError(
            "The target, annotation and prediction phonemes must be aligned."
            )
    evaluation = {
        "true_acceptance": 0,
        "true_rejection": 0,
        "false_acceptance": 0,
        "false_rejection": 0,
        "correctly_diagnosed": 0,
        "diagnosis_error": 0,
        "false_acceptance_rate": 0,
        "false_rejection_rate": 0,
        "diagnostic_error_rate": 0
    }
 
    iter_phonemes = zip(target, annotation, prediction)
    for target_phoneme, annotation_phoneme, prediction_phoneme in iter_phonemes:
        
        if target_phoneme == annotation_phoneme == prediction_phoneme:
            evaluation["true_acceptance"] += 1
        elif target_phoneme != annotation_phoneme and target_phoneme != prediction_phoneme:
            evaluation["true_rejection"] += 1
            if prediction_phoneme == annotation_phoneme:
                evaluation["correctly_diagnosed"] += 1
            else:
                evaluation["diagnosis_error"] += 1
        elif target_phoneme != annotation_phoneme and annotation_phoneme == prediction_phoneme:
            evaluation["false_acceptance"] += 1
        elif target_phoneme == annotation_phoneme and annotation_phoneme != prediction_phoneme:
            evaluation["false_rejection"] += 1



        print(a,b,c)



a = "A B C".split(" ")
b = "A B C".split(" ")
c = "A B C".split(" ")
mdd_phoneme_metrics(a,b,c)