import numpy as np

from btc_signal.models import baseline_classifier, entropy


def test_entropy_is_nonnegative():
    assert entropy(np.array([0.5, 0.5])) > 0


def test_baseline_model_builds():
    model = baseline_classifier()
    assert 'classifier' in model.named_steps
