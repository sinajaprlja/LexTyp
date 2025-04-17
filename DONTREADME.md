# Excecution flow

load_and_preprocess.ipynb
-> create_graph.ipynb
-> graph_visualization.ipynb
-> graph_analysis.ipynb 

Every Notebook saves its results, but has to be executed at least once
in this order.


# Example of smoothed sparsed matrix

## Getting component probabilities
Imagine we split G into 2 connected components.
One component containing 3 nodes and the other component containing 2 nodes.
<br>
We calculate the random walk probabilties getting two matricies.
The sum of all matrix values per component is the number of nodes.
The sum of each row in the corresponding component matrix is 1
where node_count is the number of nodes in the component, which is equal to the 
number of rows/columns in  the component matrix.

The "node_content to matrix_index" mapping is saved in a dictionary. The mapping represents
column and rows index.

```python
A = [
    [0.5, 0.5],   # -> sums up to 1
    [1  , 0  ]    # -> sums up to 1
]
sum(A)
# 2
```

<br>and<br> 

```python
B = [
    [1   , 0   , 0   ], # -> sums up to 1
    [0.5 , 0   , 0.5 ], # -> sums up to 1
    [0.33, 0.33, 0.33]  # -> sums up to 1
]
sum(B)
# 3
```

# Constructing sparse matrix from component matrices

```python
M = [
    [*A0,   0, ... ,   0],
    [0  , *A1,          ],
    [.  ,    .          ],
    [.  ,      .        ],
    [.  ,        .      ],
    [0  ,          , *An]
]
```

using the values above

```python
M = [
    [0.5 , 0.5 , 0   , 0   , 0   ], 
    [1   , 0   , 0   , 0   , 0   ], 
    [0   , 0   , 1   , 0   , 0   ], 
    [0   , 0   , 0.5 , 0   , 0.5 ], 
    [0   , 0   , 0.33, 0.33, 0.33]
]
sum(M)
# 5
```
Every row still sums up to 1



# Smoothing the sparse matrix
- Multiply every (non-zero) value by `1 - smoothing_rate`
- Set every zero-value to `(component_count * smoothing rate) / zero_count`

Using above values that would look like the following:
```python
component_count = 2
smoothing_rate = 0.1
zero_count = 16

# Subtract smoothing
M = [
    [0.45 , 0.45 , 0    , 0    , 0    ],
    [0.9  , 0    , 0    , 0    , 0    ],
    [0    , 0    , 0.9  , 0    , 0    ],
    [0    , 0    , 0.45 , 0    , 0.45 ],
    [0    , 0    , 0.297, 0.297, 0.297]
]
sum(M)
# 4.5 (= 5 * (1 - 0.1))

# Adding the rest to the zero values
# 0 is replaced by:
# 0.1 / num_zeroes              
M = [
    [0.45  , 0.45  , 0.033 , 0.033 , 0.033 ],
    [0.9   , 0.025 , 0.025 , 0.025 , 0.025 ],
    [0.025 , 0.025 , 0.9   , 0.025 , 0.025 ],
    [0.033 , 0.033 , 0.45  , 0.033 , 0.45  ],
    [0.05  , 0.05  , 0.297 , 0.297 , 0.297 ]
]
sum(M)
# 5
```

Sums may vary a little to rounding/precision errors.

# Make the Matrix symmetric

We make the matrix symmetric by iterating over all entries below the diagonal. <br>
For each pair of asymmetric elements $\text{matrix}_{i,j}$ and $\text{matrix}_{j,i}$ it replaces both with their average, so that:

$$
\text{matrix}_{i,j} = \text{matrix}_{j,i} = \frac{\text{matrix}_{i,j} + \text{matrix}_{j,i}}{2}
$$


This ensures that the final matrix is symmetric - i.e., it satisfies:

$$
\text{matrix}_{i,j} = \text{matrix}_{j,i} \quad \text{for all } i, j
$$


While different aggregation functions such as 
min, max or the average can be used, this version uses the average to preserve balance between the original values.

The choice of the average function helps balance the connections between nodes in the distance matrix. Specifically, using the minimum could cause isolated nodes that are only connected to a densely interconnected "hub" to be pushed too far out, because such nodes rarely connect directly to other nodes. Using the maximum would make it easier for these outer nodes to remain closer, but at the cost of exaggerating the connection strength.

By averaging the distances, we achieve a middle ground, allowing the network's weaker and stronger connections to be represented more fairly. From a conceptual perspective, this balance is intuitive because it reflects a balance of two viewpoints: on one hand, nodes strongly connected to a "hub" should not be excluded by overly distorting their connections, and on the other hand, weakly connected nodes can still "find their way" into the overall network structure through the averaging of their connections. This approach provides a more reliable and balanced representation of the strength of connections across all nodes.

# Creating a Distance Matrix

Given a similarity matrix $\text{M}$, the corresponding distance matrix $\text{D}$ can be obtained by the following operation:

$$
D_{i,j} = 1 - M_{i,j}
$$

where $\text{M}_{i,j}$ represents the value in the original matrix, and $\text{D}{i,j}$) represents the distance between the elements. This transformation assumes that the values in the original matrix $\text{M}$ represent some form of similarity or relatedness, and the resulting matrix $\text{D}$ represents the dissimilarity or distance.

# Checking the Triangle Inequality

The triangle inequality for a distance matrix $\text{D}$ states that for any triplet of points $\text{i}$, $\text{j}$, and $\text{k}$, the following condition must hold:

$$
D_{i,j} \leq D_{i,k} + D_{k,j}
$$

The `check_triangle_inequality` function randomly samples triplets $\text{i, j, k}$ from the distance matrix $\text{D}$ and checks whether the above inequality holds for each triplet. Specifically, for each sampled triplet, the function verifies:

$$
D_{i,j} \leq D_{i,k} + D_{k,j}
$$

If the inequality is violated, a violation count is incremented. <br>
The function returns the total number of violations found, indicating how many of the checked triplets fail to satisfy the triangle inequality.


# Filling the Diagonal of a Distance Matrix

In a distance matrix, the diagonal elements represent the distance from each point to itself, which is typically zero. To ensure this, we use the function `np.fill_diagonal` to set the diagonal of the distance matrix $\text{D}$ to zeros. Mathematically, this is represented as:

$$
D_{i,i} = 0 \quad \text{for all} \quad i
$$

where $\text{D}_{i,i}$ represents the distance from point $\text{i}$ to itself.


By setting the diagonal to zero, we remove the direct self-reference (i.e., no node has a distance to itself). However, the information that a node can reference itself is not lost. Instead, the probability (or weight) associated with self-references is redistributed. As a result, the sum of probabilities for each node no longer equals 1, and the distances between other nodes are adjusted accordingly. This ensures that the overall structure of relationships between the nodes remains intact.

# Multidimensional Scaling (MDS) and Stress Calculation

Multidimensional Scaling (MDS) is a technique used to visualize the similarity or dissimilarity between objects in a lower-dimensional space. In this case, we are performing MDS on a distance matrix  $\text{D}$ to reduce the dimensionality of the data while preserving the distances as much as possible.

The **stress** value measures the quality of the embedding in the lower-dimensional space. Lower stress values indicate that the low-dimensional configuration better represents the original distances.

Given a distance matrix  $\text{D}$, MDS aims to find a configuration of points in  $\text{d}$-dimensional space such that the pairwise distances between points in the new configuration are as close as possible to the original distances in the matrix. The stress value is calculated as:

$$
\text{Stress}(d) = \sqrt{\frac{\sum_{i < j} (D_{i,j} - \hat{D}_{i,j})^2}{\sum_{i < j} D_{i,j}^2}}
$$

where  $\text{D}_{i, j}$ represents the original distance between points  $\text{i}$ and  $\text{j}$, and $\hat{\text{D}}_{i,j}$ represents the distance between points $\text{i}$ and $\text{j}$ in the reduced $\text{d}$-dimensional space.

After performing MDS for various dimensions, we can evaluate the stress vs. dimension curve. A key goal in dimensionality reduction is to identify the optimal number of dimensions that balances low stress with the simplicity of the model.

# Finding the Optimal Number of Dimensions (Elbow Method)
We can visualize how the stress value changes as the dimensionality increases. A useful method for choosing the number of dimensions is to look for the "elbow" or "knee" in the stress curve, which is the point where further increasing the number of dimensions provides diminishing returns.

After performing MDS for various dimensions, we found that the elbow occurred at dimension 4, suggesting that 4 is the optimal number of dimensions to balance stress and dimensionality.

Additionally, the stress curve was found to be strictly convex, meaning that the stress consistently decreased as we increased the dimensions, and adding more dimensions would not significantly improve the embedding.


