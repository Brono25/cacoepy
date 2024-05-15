def pretty_matrices(matrix,  top_seq=None, left_seq=None, trace_highlight=None):
    N_row = len(matrix)  
    N_col = len(matrix[0]) 
    RED_START = "\033[31m"
    RED_END = "\033[0m"
    if not top_seq:
        top_seq = [""] * (N_col + 1)
    if not left_seq:
        left_seq = [""] * (N_row + 1)

    display_matrix = []
    display_matrix.append([""] + top_seq)

    for i in range(N_row):
        display_matrix.append([left_seq[i]] + matrix[i])

    for i in range(N_row):
        for j in range(N_col):
            if trace_highlight and (i, j) in trace_highlight:
                display_matrix[i][j] = RED_START +  str(display_matrix[i][j]) + RED_END
            else:
                display_matrix[i][j] = str(display_matrix[i][j])

    #max_width = max(max(len(str(item)) for row in display_matrix for item in row) + 2, 5)
    max_width = 4
    formatted_matrix = "\n".join(
        "".join(f"{str(item):>{max_width}}" for item in row) for row in display_matrix
    )
    return formatted_matrix


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
