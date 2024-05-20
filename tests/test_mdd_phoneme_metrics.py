from cacoepy.metric import mdd_phoneme_metrics, MetricReport

def test_true_acceptance():

    target = "A B C".split(" ")
    annotation = "A B C".split(" ")
    prediction= "A B C".split(" ")

    report = mdd_phoneme_metrics(target=target, annotation=annotation, prediction=prediction)
    expected_report = MetricReport()
    expected_report.data =  {
        "true_acceptance": 3,
        "true_rejection": 0,
        "false_acceptance": 0,
        "false_rejection": 0,
        "correctly_diagnosed": 0,
        "diagnosis_error": 0,
        "false_acceptance_rate": 0.0,
        "false_rejection_rate": 0.0,
        "diagnostic_error_rate": 0.0,
    }
    assert expected_report == report


def test_true_rejection():

    target = "A B C".split(" ")
    annotation = "X Y Z".split(" ")
    prediction = "X - C".split(" ")

    report = mdd_phoneme_metrics(
        target=target, annotation=annotation, prediction=prediction
    )
    expected_report = MetricReport()
    expected_report.data = {
        "true_acceptance": 0,
        "true_rejection": 3,
        "false_acceptance": 0,
        "false_rejection": 0,
        "correctly_diagnosed": 0,
        "diagnosis_error": 0,
        "false_acceptance_rate": 0.0,
        "false_rejection_rate": 0.0,
        "diagnostic_error_rate": 0.0,
    }
    print(report)
    assert expected_report == report


test_true_rejection()
