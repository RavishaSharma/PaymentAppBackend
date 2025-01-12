import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Test numpy
arr = np.array([1, 2, 3, 4, 5])
print("Numpy Array:", arr)

# Test pandas
data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
df = pd.DataFrame(data)
print("\nPandas DataFrame:\n", df)

# Test scikit-learn
scaler = MinMaxScaler()
scaled = scaler.fit_transform(df)
print("\nScaled Data:\n", scaled)
