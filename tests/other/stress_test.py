from cacoepy.core.Needleman_Wunsch import NeedlemanWunsch2D, NeedlemanWunschConfig
import random

"""
Running the algorithm many times to brute force check for any edge cases that may incur
indexing errors.
"""


def generate_random_seq():
    """Generate a random DNA sequence of random length between 0 and 100."""
    length = random.randint(0, 100)  # Random length from 0 to 100
    return "".join(random.choice(" abcdefghijklmnopqrstuvwxyz") for _ in range(length))


def generate_random_aligner():
    def similarity_function(a, b):
        if a == b:
            return random.randint(-10, 10)
        return random.randint(-10, 10)

    gap = random.randint(-10, 10)
    config = NeedlemanWunschConfig(gap_penalty=gap, similarity=similarity_function)
    return NeedlemanWunsch2D(config)


def stress_test_aligner2(num_tests):
    results = []
    for i in range(num_tests):
        left = generate_random_seq()
        right = generate_random_seq()
        aligner = generate_random_aligner()

        try:
            if i % 1000 == 0:
                print(i)
            aligned_left, aligned_right, score = aligner(list(left), list(right))
            results.append((aligned_left, aligned_right, score))

        except Exception as e:
            print(f"Error aligning {left} with {right}: {str(e)}")

    return results

if __name__ == "__main__":
    stress_test_aligner2(10_000)
