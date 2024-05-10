import inspect

class Config:
    def __init__(self, scoring_method, gap_penalty):
        self.gap_penalty = abs(gap_penalty)
        if callable(scoring_method):
            self._validate_callable(scoring_method)
            self.scoring_function = scoring_method
            self.scoring_matrix = None
        elif isinstance(scoring_method, dict):
            self.scoring_function = None
            self.scoring_matrix = scoring_method
        else:
            raise ValueError(
                "scoring_method must be either a callable or a 2D dictionary"
            )

    def _validate_callable(self, func):
        sig = inspect.signature(func)
        if len(sig.parameters) != 2:
            raise ValueError("scoring_function must accept exactly two parameters")


    def apply_scoring(self, char_a, char_b):
        if self.scoring_function:
            return self.scoring_function(char_a, char_b)
        elif self.scoring_matrix:
            return self.scoring_matrix.get(char_a, {}).get(char_b, 0)
        else:
            raise ValueError("No valid scoring method available.")
