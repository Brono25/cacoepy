from cacoepy.core.utils import pretty_sequences

def align_a_with_bc(a1, a2, b1, b2):

    pair_a = list(zip(a1 , a2 ))
    pair_b = list(zip(b1, b2))

    result_a = []
    result_b = []

    while pair_a and pair_b:
        if pair_b[0][0] == pair_a[0][0]:
            result_a.append(pair_a.pop(0))
            result_b.append(pair_b.pop(0))
        elif pair_b[0][0] == "-":
            result_a.append(("-", "-"))
            result_b.append(pair_b.pop(0))
        else:
            result_b.append(("-", "-"))
            result_a.append(pair_a.pop(0))
    a1, a2 = zip(*result_a)
    b1, b2 = zip(*result_b)
    assert a1 == b1

    return a1, a2, b2

a1 = "a a a a - a".split(" ")
a2 =  "- x x x x x".split(" ")

b1 = "a a a a a".split(" ")
b2 =  "z z z - z".split(" ")


a, b, c = align_a_with_bc(a1, a2, b1, b2)
pretty_sequences(a, b, c)
print()
a, b, c = align_a_with_bc(b1, b2, a1, a2)
pretty_sequences(a, b, c)
