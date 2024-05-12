from Needleman_Wunsch2D import NeedlemanWunschConfig

class NeedlemanWunsch3D:
    def __init__(self, config: NeedlemanWunschConfig):
        self.UP = "U"
        self.LEFT = "L"
        self.BACK = "B"
        self.DIAG = "D"
        self.BACK_UP = "BU"
        self.BACK_LEFT= "BL"
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
        score_matrix = [[[0] * self.N_wid for _ in range(self.N_col)] for _ in range(self.N_row)]
        trace_matrix = [[[''] * self.N_wid for _ in range(self.N_col)] for _ in range(self.N_row)]
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
        s_ij = self.substitution(row_char, col_char)
        s_ik = self.substitution(row_char, back_char)
        s_jk = self.substitution(col_char, back_char) 
        score = {
            self.UP: self.score_matrix[i-1][j][k] - 2 * gap,
            self.LEFT: self.score_matrix[i][j-1][k] - 2 * gap,
            self.BACK: self.score_matrix[i][j][k-1] - 2 * gap,
            self.DIAG: self.score_matrix[i-1][j-1][k] + s_ij - gap,
            self.BACK_UP: self.score_matrix[i-1][j][k-1] + s_ik - gap,
            self.BACK_LEFT: self.score_matrix[i][j-1][k-1] + s_jk - gap,
            self.BACK_DIAG: self.score_matrix[i-1][j-1][k-1] + s_ij + s_ik + s_jk
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


    def substitution(self, char_a, char_b):
        return self.config.apply_scoring(char_a, char_b)

    def __str__(self):
        return "TODO"


