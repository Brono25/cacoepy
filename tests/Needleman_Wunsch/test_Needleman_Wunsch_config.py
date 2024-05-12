import pytest
from cacoepy.core.Needleman_Wunsch import NeedlemanWunschConfig
from cacoepy.core.exceptions import InvalidSubstitutionError

def test_incorrect_substitution_function():
    def incorrect_substitution_function1(a, b, c):
        pass

    with pytest.raises(
        InvalidSubstitutionError,
        match="Substitution function must have only two arguments.",
    ):
        NeedlemanWunschConfig(
            gap_penalty=4, substitution=incorrect_substitution_function1
        )

    def incorrect_substitution_function2(a):
        pass

    with pytest.raises(
        InvalidSubstitutionError,
        match="Substitution function must have only two arguments.",
    ):
        NeedlemanWunschConfig(
            gap_penalty=4, substitution=incorrect_substitution_function2
        )
