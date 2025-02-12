
import numpy as np
from joblib import Parallel, delayed

# Example data
x = np.random.rand(100, 30, 30)



# Define a function to process each slice
def compute_slice_sum(i, data):
    return data[i, :, :]

# Parallelize across all CPU cores
n_jobs = -1  # Use all available cores
results = Parallel(n_jobs=n_jobs)(
    delayed(compute_slice_sum)(i, x) for i in range(x.shape[0])
)

sums = np.array(results)  # Convert to array