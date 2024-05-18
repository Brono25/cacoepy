from cacoepy.core.exceptions import PhonemeSequenceError
from typing import List, Dict, TypedDict

class MetricDict(TypedDict):
    true_acceptance: int
    true_rejection: int
    false_acceptance: int
    false_rejection: int
    correctly_diagnosed: int
    diagnosis_error: int
    false_acceptance_rate: float
    false_rejection_rate: float
    diagnostic_error_rate: float

def mdd_phoneme_metrics(
        target: List[str], 
        annotation: List[str], 
        prediction: List[str],
        metric: MetricDict = None
        ) -> MetricDict:
    """
    Calculate MDD metrics at the phoneme level.

    Parameters:
    - target (List[str]): Intended correct pronunciation phonemes.
    - annotation (List[str]): Actually pronounced phonemes.
    - prediction (List[str]): Predicted phonemes by the model.
    - metric (MetricDict, optional): Dictionary to store metric counts and rates.

    Returns:
    - MetricDict: Dictionary with counts and rates of MDD metrics.

    Raises:
    - PhonemeSequenceError: If the lengths of target, annotation, and prediction sequences are not equal.
    """
    if not (len(target) == len(annotation) == len(prediction)):
        raise PhonemeSequenceError(
            "The target, annotation and prediction phonemes must be aligned."
            )
    
    if metric is None:
        metric: MetricDict = {
            "true_acceptance": 0,
            "true_rejection": 0,
            "false_acceptance": 0,
            "false_rejection": 0,
            "correctly_diagnosed": 0,
            "diagnosis_error": 0,
            "false_acceptance_rate": 0.0,
            "false_rejection_rate": 0.0,
            "diagnostic_error_rate": 0.0
        }
 
    iter_phonemes = zip(target, annotation, prediction)
    for target_phoneme, annotation_phoneme, prediction_phoneme in iter_phonemes:
        
        if target_phoneme == annotation_phoneme == prediction_phoneme:
            metric["true_acceptance"] += 1
        elif target_phoneme != annotation_phoneme and target_phoneme != prediction_phoneme:
            metric["true_rejection"] += 1
            if prediction_phoneme == annotation_phoneme:
                metric["correctly_diagnosed"] += 1
            else:
                metric["diagnosis_error"] += 1
        elif target_phoneme != annotation_phoneme and annotation_phoneme == prediction_phoneme:
            metric["false_acceptance"] += 1
        elif target_phoneme == annotation_phoneme and annotation_phoneme != prediction_phoneme:
            metric["false_rejection"] += 1

    total = len(target)
    if total > 0:
        metric["false_acceptance_rate"] = metric["false_acceptance"] / total
        metric["false_rejection_rate"] = metric["false_rejection"] / total
        metric["diagnostic_error_rate"] = metric["diagnosis_error"] / total
    
    return metric

    

metric = {
    "true_acceptance": 1,
    "true_rejection": 0,
    "false_acceptance": 0,
    "false_rejection": 0,
    "correctly_diagnosed": 1,
    "diagnosis_error": 0,
    "false_acceptance_rate": 0.0,
    "false_rejection_rate": 0.0,
    "diagnostic_error_rate": 0.0
}

a = "A B C".split(" ")
b = "A B C".split(" ")
c = "A A D".split(" ")
metric = mdd_phoneme_metrics(a,b,c)
for k,v in metric.items():
    print(k, v)