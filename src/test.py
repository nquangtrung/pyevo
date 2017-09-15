import numpy as np


def mutate_matrix(m, severity):
    mutated = np.random.randn(m.shape[0], m.shape[1])
    affected = np.random.randint(1, high=100, size=m.shape, dtype=np.int32)

    print(str(affected < severity))
    print(str(mutated))
    print(str(mutated * (affected < severity)))
    print(str(m * (affected > severity)))

    return mutated * (affected < severity) + m * (affected > severity)


m = np.random.randn(4, 5)

print(str(m))

print(str(mutate_matrix(m, 20)))

