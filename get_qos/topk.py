import numpy as np
K=4
a = np.array([0, 8, 0, 4, 5, 8, 8, 0, 4, 2])
a[np.argpartition(a,-K)[-K:]]