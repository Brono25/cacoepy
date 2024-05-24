from typing import Callable, Dict, Union, List, Tuple
import inspect
from cacoepy.core.utils import pretty_matrices
from cacoepy.core.exceptions import InvalidSimilarityError, TracebackIndexError


class NeedlemanWunschConfig:
    def __init__(
            self, 
            similarity: Union[Callable[[str, str], float], Dict[str, Dict[str, float]]], 
            gap_penalty:float
        ) -> None:
        """
        Configuration class for the Needleman-Wunsch algorithm.

        This class handles the configuration for the Needleman-Wunsch algorithm,
        including the similarity scoring and gap penalty.

        Args:
            similarity (Union[Callable[[str, str], float], Dict[str, Dict[str, float]]]): 
                A function or a 2D dictionary to compute similarity scores between characters.
            gap_penalty (float): The penalty score for introducing gaps in the alignment.

        Raises:
            InvalidSimilarityError: If the similarity parameter is neither a callable nor a 2D 
            dictionary. InvalidSimilarityError: If the similarity function does not have 
            exactly two arguments.
        """
        self.gap_penalty = gap_penalty
        if callable(similarity):
            self._validate_callable(similarity)
            self.scoring_function = similarity
            self.scoring_matrix = None
        elif isinstance(similarity, dict):
            self.scoring_function = None
            self.scoring_matrix = similarity
        else:
            raise InvalidSimilarityError(
                "Similarity must be either a callable or a 2D dictionary"
            )

    def _validate_callable(self, func):
        sig = inspect.signature(func)
        if len(sig.parameters) != 2:
            raise InvalidSimilarityError(
                "Similarity function must have only two arguments."
            )
        
    def _apply_scoring(self, char_a, char_b):
        if self.scoring_function:
            return self.scoring_function(char_a, char_b)
        elif self.scoring_matrix:
            return self.scoring_matrix.get(char_a, {}).get(char_b, 0)
        else:
            raise InvalidSimilarityError("No valid scoring method available.")


class NeedlemanWunsch2D:
    """
    Performs sequence alignment using the Needleman-Wunsch algorithm with a given configuration.

    Args:
        config (NeedlemanWunschConfig): Configuration object containing the scoring function 
        or matrix and gap penalty.
    """
    def __init__(self, config: NeedlemanWunschConfig):
        self.LEFT = "←"
        self.UP = "↑"
        self.DIAG = "↖"
        self.DONE = "X"
        self.GAP = "-"
        self.config = config
        self._path_idx = []

    def __call__(
            self, 
            seq1: List[str], 
            seq2: List[str]
        ) -> Tuple[List[str], List[str], float]:
        """
        Aligns two sequences using the Needleman-Wunsch algorithm.

        Args:
            seq1 (str): The first sequence to align.
            seq2 (str): The second sequence to align.

        Returns:
            Tuple[List[str], List[str], float]: A tuple containing the aligned 
            first sequence, aligned second sequence, and the alignment score.
        """
        self.left_seq = [""] + seq1
        self.top_seq = [""] + seq2
        self.N_col = len(self.top_seq)
        self.N_row = len(self.left_seq)
        self.score_matrix, self.trace_matrix = self._init_score_and_trace_matrix() 
        self._fill_score_matrix()
        aligned_left_seq, aligned_top_seq, score = self._traceback()
        return aligned_left_seq, aligned_top_seq, score

    def _init_score_and_trace_matrix(self):
        score_matrix = [[0] * self.N_col for _ in range(self.N_row)]
        trace_matrix = [[0] * self.N_col for _ in range(self.N_row)]
        gap = 0
        for i in range(self.N_row):
            score_matrix[i][0] = gap
            trace_matrix[i][0] = self.UP
            gap = gap + self.config.gap_penalty
        gap = 0
        for j in range(self.N_col):
            score_matrix[0][j] = gap
            trace_matrix[0][j] = self.LEFT
            gap = gap + self.config.gap_penalty
        trace_matrix[0][0] = self.DONE
        return score_matrix, trace_matrix

    def _fill_score_matrix(self):
        for i in range(1, self.N_row):
            for j in range(1, self.N_col):
                score, direction = self._score_cell(i, j)
                self.score_matrix[i][j] = score
                self.trace_matrix[i][j] = direction

    def _score_cell(self, i, j):
        left_char = self.left_seq[i]
        top_char = self.top_seq[j]
        s_ij = self.similarity_score(top_char, left_char)
        score = {
            self.DIAG: self.score_matrix[i - 1][j - 1] + s_ij,
            self.UP: self.score_matrix[i - 1][j] + self.config.gap_penalty,
            self.LEFT: self.score_matrix[i][j - 1] + self.config.gap_penalty,
        }
        max_score, direction = self._choose_path(score)
        return max_score, direction

    def _choose_path(self, score):
        max_value = max(score.values())
        max_keys = [key for key, value in score.items() if value == max_value]
        if self.UP in max_keys:
            return max_value, self.UP
        elif self.LEFT in max_keys:
            return max_value, self.LEFT
        return max_value, self.DIAG

    def _traceback(self):
        aligned_top_seq = []
        aligned_left_seq = []
        left_idx = self.N_row - 1
        top_idx = self.N_col - 1
        score = self.score_matrix[left_idx][top_idx]
        cell = None
        while cell != self.DONE:
            self._path_idx.append((left_idx, top_idx))
            cell = self.trace_matrix[left_idx][top_idx]
            if cell == self.DIAG:
                aligned_top_seq.append(self.top_seq[top_idx])
                aligned_left_seq.append(self.left_seq[left_idx])
                left_idx -= 1
                top_idx -= 1
            elif cell == self.LEFT:
                aligned_top_seq.append(self.top_seq[top_idx])
                aligned_left_seq.append(self.GAP)
                top_idx -= 1
            elif cell == self.UP:
                aligned_top_seq.append(self.GAP)
                aligned_left_seq.append(self.left_seq[left_idx])
                left_idx -= 1

            if left_idx < 0 or top_idx < 0:
                raise TracebackIndexError(f"{left_idx=}, {top_idx=}")

        aligned_top_seq.reverse()
        aligned_left_seq.reverse()

        return aligned_left_seq, aligned_top_seq, score

    def similarity_score(self, char_a, char_b):
        return self.config._apply_scoring(char_a, char_b)

    def __str__(self):
        m1 = pretty_matrices(self.score_matrix, self.top_seq, self.left_seq)
        m2 = pretty_matrices(self.trace_matrix, self.top_seq, self.left_seq)
        return m1 + "\n"*3 + m2


class NeedlemanWunsch3D:
    def __init__(self, config: NeedlemanWunschConfig):
        self.UP = "U"
        self.LEFT = "L"
        self.BACK = "B"
        self.DIAG = "D"
        self.BACK_UP = "BU"
        self.BACK_LEFT = "BL"
        self.BACK_DIAG = "BD"
        self.DONE = "X"
        self.GAP = "-"
        self.config = config

    def __call__(self, seq1, seq2, seq3):
        self.top_seq = [""] + seq1
        self.left_seq = [""] + seq2
        self.back_seq = [""] + seq3
        self.N_row = len(self.top_seq)
        self.N_col = len(self.left_seq)
        self.N_wid = len(self.back_seq)
        self.score_matrix, self.trace_matrix = self._init_score_and_trace_matrix()
        self._fill_score_matrix()
        return self._traceback()

    def _init_score_and_trace_matrix(self):
        score_matrix = [
            [[0] * self.N_wid for _ in range(self.N_col)] for _ in range(self.N_row)
        ]
        trace_matrix = [
            [[""] * self.N_wid for _ in range(self.N_col)] for _ in range(self.N_row)
        ]
        gap = 0
        for i in range(self.N_row):
            for j in range(self.N_col):
                score_matrix[i][j][0] = gap
                trace_matrix[i][j][0] = self.BACK
                gap -= self.config.gap_penalty
        gap = 0
        for j in range(self.N_col):
            for k in range(self.N_wid):
                score_matrix[0][j][k] = gap
                trace_matrix[0][j][k] = self.LEFT
                gap -= self.config.gap_penalty
        gap = 0
        for i in range(self.N_row):
            for k in range(self.N_wid):
                score_matrix[i][0][k] = gap
                trace_matrix[i][0][k] = self.UP
                gap -= self.config.gap_penalty
        trace_matrix[0][0][0] = self.DONE
        return score_matrix, trace_matrix

    def _fill_score_matrix(self):
        for i in range(1, self.N_row):
            for j in range(1, self.N_col):
                for k in range(1, self.N_wid):
                    score, direction = self._score_cell(i, j, k)
                    self.score_matrix[i][j][k] = score
                    self.trace_matrix[i][j][k] = direction

    def _score_cell(self, i, j, k):
        gap = self.config.gap_penalty
        row_char = self.top_seq[i]
        col_char = self.left_seq[j]
        back_char = self.back_seq[k]
        s_ij = self.similarity(row_char, col_char)
        s_ik = self.similarity(row_char, back_char)
        s_jk = self.similarity(col_char, back_char)
        score = {
            self.UP: self.score_matrix[i - 1][j][k] - 2 * gap,
            self.LEFT: self.score_matrix[i][j - 1][k] - 2 * gap,
            self.BACK: self.score_matrix[i][j][k - 1] - 2 * gap,
            self.DIAG: self.score_matrix[i - 1][j - 1][k] + s_ij - gap,
            self.BACK_UP: self.score_matrix[i - 1][j][k - 1] + s_ik - gap,
            self.BACK_LEFT: self.score_matrix[i][j - 1][k - 1] + s_jk - gap,
            self.BACK_DIAG: self.score_matrix[i - 1][j - 1][k - 1] + s_ij + s_ik + s_jk,
        }
        direction = max(score, key=score.get)
        max_score = score[direction]
        return max_score, direction

    def _traceback(self):
        aligned_top_seq = []
        aligned_left_seq = []
        aligned_back_seq = []

        i = self.N_row - 1
        j = self.N_col - 1
        k = self.N_wid - 1

        while i > 0 or j > 0 or k > 0:
            try:
                cell = self.trace_matrix[i][j][k]
            except IndexError:
                print(f"IndexError at i={i}, j={j}, k={k}")
                print("")
                break

            if cell == self.DIAG:
                aligned_top_seq.append(self.top_seq[i])
                aligned_left_seq.append(self.left_seq[j])
                aligned_back_seq.append(self.GAP)
                i -= 1
                j -= 1
            elif cell == self.BACK_UP:
                aligned_top_seq.append(self.top_seq[i])
                aligned_left_seq.append(self.GAP)
                aligned_back_seq.append(self.back_seq[k])
                i -= 1
                k -= 1
            elif cell == self.BACK_LEFT:
                aligned_top_seq.append(self.GAP)
                aligned_left_seq.append(self.left_seq[j])
                aligned_back_seq.append(self.back_seq[k])
                j -= 1
                k -= 1
            elif cell == self.BACK:
                aligned_top_seq.append(self.GAP)
                aligned_left_seq.append(self.GAP)
                aligned_back_seq.append(self.back_seq[k])
                k -= 1
            elif cell == self.LEFT:
                aligned_top_seq.append(self.GAP)
                aligned_left_seq.append(self.left_seq[j])
                aligned_back_seq.append(self.GAP)
                j -= 1
            elif cell == self.UP:
                aligned_top_seq.append(self.top_seq[i])
                aligned_left_seq.append(self.GAP)
                aligned_back_seq.append(self.GAP)
                i -= 1
            elif cell == self.BACK_DIAG:
                aligned_top_seq.append(self.top_seq[i])
                aligned_left_seq.append(self.left_seq[j])
                aligned_back_seq.append(self.back_seq[k])
                i -= 1
                j -= 1
                k -= 1
            else:
                print(f"Breaking loop: i={i}, j={j}, k={k}, cell={cell}")
                break

        aligned_top_seq.reverse()
        aligned_left_seq.reverse()
        aligned_back_seq.reverse()

        return aligned_top_seq, aligned_left_seq, aligned_back_seq

    def similarity(self, char_a, char_b):
        return self.config.apply_scoring(char_a, char_b)

    def __str__(self):
        return "TODO"
