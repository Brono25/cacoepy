from utils import pretty_matrices
import inspect

class NeedlemanWunschConfig:
    def __init__(self, substitution, gap_penalty):
        self.gap_penalty = abs(gap_penalty)
        if callable(substitution):
            self._validate_callable(substitution)
            self.scoring_function = substitution
            self.scoring_matrix = None
        elif isinstance(substitution, dict):
            self.scoring_function = None
            self.scoring_matrix = substitution
        else:
            raise ValueError(
                "substitution must be either a callable or a 2D dictionary"
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


class NeedlemanWunsch:
    def __init__(self, config=NeedlemanWunschConfig):
        self.LEFT = "←"
        self.UP = "↑"
        self.DIAG = "↖"
        self.DONE = "X"
        self.GAP = "-"
        self.config = config

    def __call__(self, seq1, seq2):
        self.top_seq = [""] + seq1
        self.left_seq = [""] + seq2
        self.N_row = len(self.top_seq)
        self.N_col = len(self.left_seq)
        self.score_matrix, self.trace_matrix = self._init_score_and_trace_matrix() 
        self._fill_score_matrix()
        return self._traceback()

    def _init_score_and_trace_matrix(self):
        score_matrix = [[0] * self.N_col for _ in range(self.N_row)]
        trace_matrix = [[0] * self.N_col for _ in range(self.N_row)]
        gap = 0
        for i in range(self.N_row):
            score_matrix[i][0] = gap
            trace_matrix[i][0] = self.UP
            gap = gap - self.config.gap_penalty
        gap = 0
        for j in range(self.N_col):
            score_matrix[0][j] = gap
            trace_matrix[0][j] = self.LEFT
            gap = gap - self.config.gap_penalty
        trace_matrix[0][0] = self.DONE
        return score_matrix, trace_matrix

    def _fill_score_matrix(self):
        for i in range(1, self.N_row):
            for j in range(1, self.N_col):
                score, direction = self._score_cell(i, j)
                self.score_matrix[i][j] = score
                self.trace_matrix[i][j] = direction

    def _traceback(self):
        aligned_top_seq = []
        aligned_left_seq = []
        i = self.N_row - 1
        j = self.N_col - 1
        while i > 0 or j > 0:
            cell = self.trace_matrix[i][j]
            if cell == self.DIAG:
                aligned_top_seq.append(self.top_seq[i])
                aligned_left_seq.append(self.left_seq[j])
                i -= 1
                j -= 1
            elif cell == self.LEFT:
                aligned_top_seq.append(self.GAP)
                aligned_left_seq.append(self.left_seq[j])
                j -= 1
            elif cell == self.UP:
                aligned_top_seq.append(self.top_seq[i])
                aligned_left_seq.append(self.GAP)
                i -= 1
        aligned_top_seq.reverse()
        aligned_left_seq.reverse()
        return aligned_top_seq, aligned_left_seq

    def _score_cell(self, i, j):
        row_char = self.top_seq[i]
        col_char = self.left_seq[j]
        s_ij = self.calculate_score(row_char, col_char)
        q_diag = self.score_matrix[i - 1][j - 1] + s_ij
        q_up = self.score_matrix[i - 1][j] - self.config.gap_penalty
        q_left = self.score_matrix[i][j - 1] - self.config.gap_penalty
        max_score, direction = max(
            (q_diag, self.DIAG),
            (q_up, self.UP),
            (q_left, self.LEFT),
            key=lambda x: x[0],
        )
        return max_score, direction

    def calculate_score(self, char_a, char_b):
        return self.config.apply_scoring(char_a, char_b)

    def __str__(self):
        return pretty_matrices(
            self.top_seq, self.left_seq, self.score_matrix, self.trace_matrix
        )


