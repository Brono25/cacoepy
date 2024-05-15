class ElementNotInVocabError(Exception):
    """Exception raised when a sequence element is not found in the vocabulary of the Similarity matrix."""
    def __init__(self, message):
        super().__init__(message)


class InvalidSimilarityError(Exception):
    """Exception raised for invalid similarity inputs in NeedlemanWunschConfig."""
    def __init__(self, message):
        super().__init__(message)


class TracebackIndexError(Exception):
    """Exception raised for indexing error during traceback"""
    def __init__(self, message):
        super().__init__(message)
