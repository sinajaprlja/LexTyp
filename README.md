# Abstract

Colexification - where a word represents multiple related or unrelated meanings or concepts -reveals fundamental patterns in how languages encode semantic relationships. This thesis explores how dimensionality reduction can effectively capture cross-linguistic colexification patterns, bridging linguistic theory with computational methods.
Using multilingual lexical data from the English Wiktionary, an undirected polysemy network where nodes represent concepts (English words paired with glosses) and edges reflect shared translations across languages is constructed. After data cleaning and frequency-based filtering to ensure robustness, a similarity matrix is computed capturing structural similarity by estimating the probability of reaching each node from every other node, including the starting node, through multiple random walks. This similarity matrix is further transformed into a distance matrix suitable for Multidimensional Scaling (MDS). MDS is then applied to project the polysemy network into a lower-dimensional space. The analysis identifies an optimal four-to-six-dimensional space, validated by stress metrics, which preserves the underlying semantic relationships while reducing complexity.

# Project Workflow

1) **Data Loading and Preprocessing** <br>
Relevant data is extracted and preprocessed in: [load_and_preprocess.ipynb](https://github.com/sinajaprlja/LexTyp/blob/main/load_and_preprocess.ipynb). <br>
2) **Graph Construction** <br>
The colexification graph is built in: [create_graph.ipynb](https://github.com/sinajaprlja/LexTyp/blob/main/create_graph.ipynb) <br>
3) **Graph Visualization** <br>
To visualize the connected components of the graph (depth = 2), use: [graph_visualization.ipynb](https://github.com/sinajaprlja/LexTyp/blob/main/graph_visualization.ipynb).<br>
4) **Dimensionality Reduction and Analysis**<br>
Creating the distance matrix and applying MDS is carried out in: [graph_analysis.ipynb](https://github.com/sinajaprlja/LexTyp/blob/main/graph_analysis.ipynb).

Each notebook saves its output but must be run at least once in the order listed above.
