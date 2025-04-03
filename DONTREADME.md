


# Example of smoothed sparsed matrix

## Getting component probabilities
Imagine we split G into 2 connected components.
One component containing 3 nodes and the other component containing 2 nodes.
<br>
We calculate the random walk probabilties getting two matricies.
The sum of all matrix values per component is 1.
The sum of each row in the corresponding component matrix is (1 / node_count)
where node_count is the number of nodes in the component, which is equal to the 
number of rows/columns in  the component matrix.
The sum of a column represents the probability of landing on that node, no matter
where the reandom walk started.

The "node_content to matrix_index" mapping is saved in a dictionary. The mapping represents
column and rows index.

```python
A = [
    [0.25, 0.25],   # -> sums up to 1/2 = 0.5
    [0.5 , 0   ]    # -> sums up to 1/2 = 0.5
]
sum(A)
# 1
```

<br>and<br> 

```python
B = [
    [0.33, 0   , 0   ], # -> sums up to 1/3 = 0.33...
    [0.16, 0   , 0.16], # -> sums up to 1/3 = 0.33...
    [0.11, 0.11, 0.11]  # -> sums up to 1/3 = 0.33...
]
sum(B)
# 1
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
    [0.25, 0.25, 0   , 0   , 0   ], 
    [0.5 , 0   , 0   , 0   , 0   ], 
    [0   , 0   , 0.33, 0   , 0   ], 
    [0   , 0   , 0.16, 0   , 0.16], 
    [0   , 0   , 0.11, 0.11, 0.11]
]
```
Every row still sums up to 1 / node_count (number of nodes in corresponding component)



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
    [0.225, 0.225, 0    , 0    , 0    ],
    [0.45 , 0    , 0    , 0    , 0    ],
    [0    , 0    , 0.297, 0    , 0    ],
    [0    , 0    , 0.144, 0    , 0.144],
    [0    , 0    , 0.099, 0.099, 0.099]
]
sum(M)
# 2 (=component_count)

# Adding the rest to the zero values
# 0 is replaced by:
# (component_count * smoothing_rate) / zero_count
# (2               * 0.1           ) / 16
# = 0.0125
M = [
    [0.225 , 0.225 , 0.0125, 0.0125, 0.0125],
    [0.45  , 0.0125, 0.0125, 0.0125, 0.0125],
    [0.0125, 0.0125, 0.297 , 0.0125, 0.0125],
    [0.0125, 0.0125, 0.144 , 0.0125, 0.144 ],
    [0.0125, 0.0125, 0.099 , 0.099 , 0.099 ]
]
sum(M)
# 2 (=component_count)
```

Sums may vary a little to rounding/precision errors