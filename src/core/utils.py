def pretty_matrices(top_seq, left_seq, score_matrix, trace_matrix):
    N_col = len(left_seq)
    N_row = len(top_seq)

    # Create header for score matrix
    score_header = (
        "Score Matrix:\n    " + " ".join(f"{phoneme:>3}" for phoneme in left_seq) + "\n"
    )
    score_rows = ""
    for i, row_phoneme in enumerate(top_seq):
        row = (
            f"{row_phoneme:>3} "
            + " ".join(f"{score_matrix[i][j]:>3}" for j in range(N_col))
            + "\n"
        )
        score_rows += row

    # Create header for trace matrix
    trace_header = (
        "\nTraceback Matrix:\n    "
        + " ".join(f"{phoneme:>3}" for phoneme in left_seq)
        + "\n"
    )
    trace_rows = ""
    for i, row_phoneme in enumerate(top_seq):
        row = (
            f"{row_phoneme:>3} "
            + " ".join(f"{trace_matrix[i][j]:>3}" for j in range(N_col))
            + "\n"
        )
        trace_rows += row

    return score_header + score_rows + trace_header + trace_rows


def pretty_sequences(*arrays):
    max_length = max(len(arr) for arr in arrays)
    padded_arrays = [
        list(map(str, arr)) + [""] * (max_length - len(arr)) for arr in arrays
    ]
    column_widths = [
        max(len(padded_arrays[j][i]) for j in range(len(padded_arrays)))
        for i in range(max_length)
    ]
    for array in padded_arrays:
        print(
            "  ".join(
                element.ljust(width) for element, width in zip(array, column_widths)
            )
        )


