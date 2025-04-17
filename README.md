# Abstract

Colexification - where a word represents multiple related or unrelated meanings
or concepts - reveals fundamental patterns in how languages encode semantic relationships. Analyzing these patterns computationally is challenging due to the high
dimensionality and sparsity of colexification networks. This thesis explores how
dimensionality reduction can effectively capture cross-linguistic colexification patterns,
bridging linguistic theory with computational methods.
Using multilingual lexical data from the English Wiktionary, a colexification graph
where nodes represent concepts (English words paired with glosses) and edges reflect
shared translations across languages is constructed. After data cleaning and frequencybased filtering to ensure robustness, Multidimensional Scaling (MDS) is applied to
project the graph into a lower-dimensional space. The analysis identifies an optimal
four-dimensional space, validated by stress metrics, which preserves the underlying
semantic relationships while reducing complexity.

# Project Workflow

1) **Data Loading and Preprocessing** <br>
Relevant data is extracted and preprocessed in: [load_and_preprocess.ipynb](https://github.com/sinajaprlja/LexTyp/blob/main/load_and_preprocess.ipynb). <br>
2) **Graph Construction** <br>
The colexification graph is built in: [create_graph.ipynb](https://github.com/sinajaprlja/LexTyp/blob/main/create_graph.ipynb) <br>
3) **Graph Visualization** <br>
To visualize the connected components of the graph (depth = 2), use: [graph_visualization.ipynb](https://github.com/sinajaprlja/LexTyp/blob/main/graph_visualization.ipynb).<br>
4) **Dimensionality Reduction and Analysis**
The final step — creating the distance matrix and applying MDS — is carried out in: [graph_analysis.ipynb](https://github.com/sinajaprlja/LexTyp/blob/main/graph_analysis.ipynb).

Each notebook saves its output but must be run at least once in the order listed above.
