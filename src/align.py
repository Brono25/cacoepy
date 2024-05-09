# Scoring scheme
LEFT = "←"
UP = "↑"
DIAG = "↖"


class NeedlemanWunsch:

    def __init__(self, seq1, seq2, gap_penalty=1):
        self.gap_penalty = abs(gap_penalty)
        seq1.insert(0, "") #add padding to start of sequences
        seq2.insert(0, "")
        self.row_seq = seq1
        self.col_seq = seq2
        self.N_row = len(self.row_seq)
        self.N_col = len(self.col_seq)
        self.score_matrix, self.trace_matrix = self._init_score_and_trace_matrix()
        self._fill_score_matrix()

    def _init_score_and_trace_matrix(self):
        score_matrix = [[0] * self.N_col for _ in range(self.N_row)]
        trace_matrix = [[0] * self.N_col for _ in range(self.N_row)]
        gap = 0
        for i in range(self.N_row):
            score_matrix[i][0] = gap
            trace_matrix[i][0] = UP
            gap = gap - self.gap_penalty
        gap = 0
        for j in range(self.N_col):
            score_matrix[0][j] = gap
            trace_matrix[0][j] = LEFT
            gap = gap - self.gap_penalty
        trace_matrix[0][0] = "X"
        return score_matrix, trace_matrix

    def _fill_score_matrix(self):
        for i in range(1, self.N_row):
            for j in range(1, self.N_col):
                score, direction = self._score_cell(i, j)
                self.score_matrix[i][j] = score
                self.trace_matrix[i][j] = direction

    def _score_cell(self, i, j):
        row_char = self.row_seq[i]
        col_char = self.col_seq[j]

        q_diag = self.score_matrix[i - 1][j - 1] + self.substitution_score(
            row_char, col_char
        )
        q_up = self.score_matrix[i - 1][j] - self.gap_penalty
        q_left = self.score_matrix[i][j - 1] - self.gap_penalty

        max_score, direction = max(
            (q_diag, DIAG), (q_up, UP), (q_left, LEFT), key=lambda x: x[0]
        )
        return max_score, direction

    def substitution_score(self, char1, char2):
        if char1 == char2:
            return 1
        return -1

    def __str__(self):
        # Create header for score matrix
        score_header = (
            "Score Matrix:\n    "
            + " ".join(f"{phoneme:>3}" for phoneme in self.col_seq)
            + "\n"
        )
        score_rows = ""
        for i, row_phoneme in enumerate(self.row_seq):
            row = (
                f"{row_phoneme:>3} "
                + " ".join(f"{self.score_matrix[i][j]:>3}" for j in range(self.N_col))
                + "\n"
            )
            score_rows += row

        # Create header for trace matrix
        trace_header = (
            "\nTraceback Matrix:\n    "
            + " ".join(f"{phoneme:>3}" for phoneme in self.col_seq)
            + "\n"
        )
        trace_rows = ""
        for i, row_phoneme in enumerate(self.row_seq):
            row = (
                f"{row_phoneme:>3} "
                + " ".join(f"{self.trace_matrix[i][j]:>3}" for j in range(self.N_col))
                + "\n"
            )
            trace_rows += row

        return score_header + score_rows + trace_header + trace_rows


# Example usage
seq1 = "C A G C T A".split(" ")
seq2 = "C A C A T A".split(" ")
scoring_matrix = NeedlemanWunsch(seq2, seq1)

print(scoring_matrix)
