
class ElementNotInVocabError(Exception):
    """Exception raised when a sequence element is not found in the vocabulary of the substitution matrix."""
    def __init__(self, message):
        super().__init__(message)


class InvalidSubstitutionError(Exception):
    """Exception raised for invalid substitution inputs in NeedlemanWunschConfig."""
    def __init__(self, message):
        super().__init__(message)
