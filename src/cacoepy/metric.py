from cacoepy.core.exceptions import PhonemeSequenceError
from typing import List, Dict, TypedDict


class MetricReport:
    """
    A datatype for holding MDD metrics from mdd_phoneme_metrics.
    """
    def __init__(self):
        self.data = {
            "true_acceptance": 0,
            "true_rejection": 0,
            "false_acceptance": 0,
            "false_rejection": 0,
            "correctly_diagnosed": 0,
            "diagnosis_error": 0,
            "false_acceptance_rate": 0.0,
            "false_rejection_rate": 0.0,
            "diagnostic_error_rate": 0.0,
        }

    def get(self, key):
        return self.data.get(key, None)

    def set(self, key, value):
        if key in self.data:
            self.data[key] = value
        else:
            raise KeyError(f"{key} is not a valid metric key")

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __str__(self):
        output = ""
        max_key_length = max(len(k) for k in self.data.keys())
        for k, v in self.data.items():
            if isinstance(v, float):
                output += f"{k:<{max_key_length}} -> {v:.2f}\n"
            else:
                output += f"{k:<{max_key_length}} -> {v}\n"
        return output.strip()

    def __eq__(self, other):
        if isinstance(other, MetricReport):
            return self.data == other.data
        return False


def mdd_phoneme_metrics(
    target: List[str],
    annotation: List[str],
    prediction: List[str],
    metric: MetricReport = None,
) -> MetricReport:
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
        metric = MetricReport()

    iter_phonemes = zip(target, annotation, prediction)
    for target_phoneme, annotation_phoneme, prediction_phoneme in iter_phonemes:

        if target_phoneme == annotation_phoneme == prediction_phoneme:
            metric["true_acceptance"] += 1
        elif (
            target_phoneme != annotation_phoneme
            and annotation_phoneme == prediction_phoneme
        ):
            metric["false_acceptance"] += 1
        elif target_phoneme != annotation_phoneme:
            metric["true_rejection"] += 1
            if prediction_phoneme == annotation_phoneme:
                metric["correctly_diagnosed"] += 1
            else:
                metric["diagnosis_error"] += 1

        elif (
            target_phoneme == annotation_phoneme
            and annotation_phoneme != prediction_phoneme
        ):
            metric["false_rejection"] += 1

    total = len(target)
    if total > 0:
        metric["false_acceptance_rate"] = metric["false_acceptance"] / total
        metric["false_rejection_rate"] = metric["false_rejection"] / total
        metric["diagnostic_error_rate"] = metric["diagnosis_error"] / total

    return metric


if __name__ == "__main__":
    a = "A B C".split(" ")
    b = "A B C".split(" ")
    c = "A A D".split(" ")
    metric = mdd_phoneme_metrics(a, b, c)
    metric = mdd_phoneme_metrics(a, b, c, metric)
    metric = mdd_phoneme_metrics(a, b, c, metric)

    print(metric)
