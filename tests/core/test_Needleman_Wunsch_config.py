import pytest
from cacoepy.core.Needleman_Wunsch import NeedlemanWunschConfig
from cacoepy.core.exceptions import InvalidSimilarityError

def test_incorrect_similarity_function():
    def incorrect_similarity_function1(a, b, c):
        pass

    with pytest.raises(
        InvalidSimilarityError,
        match="Similarity function must have only two arguments.",
    ):
        NeedlemanWunschConfig(
            gap_penalty=-4, similarity=incorrect_similarity_function1
        )

    def incorrect_similarity_function2(a):
        pass

    with pytest.raises(
        InvalidSimilarityError,
        match="Similarity function must have only two arguments.",
    ):
        NeedlemanWunschConfig(
            gap_penalty=-4, similarity=incorrect_similarity_function2
        )
