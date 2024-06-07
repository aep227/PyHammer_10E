import pytest


expected_results_params = [
    ('')]

def test_init(self):
    assert 1 == 1

@pytest.mark.parametrize('expected_result', expected_results_params)
def test_expected_results(self, expected_result):
    assert 1 == 1