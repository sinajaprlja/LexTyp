import json
import random
from typing import Any

import networkx as nx



def save_results_to_file(results: Any, filename: str) -> None:
    """
    Saves results to a JSON file.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
        


def random_walk_in_component(component_graph: nx.Graph, start_node: str, walk_length: int) -> str:
    """
    Performs a random walk in a component graph.
    """
    current_node = start_node 

    for _ in range(walk_length - 1):
        neighbors = list(component_graph.neighbors(current_node)) + [current_node]
        next_node = random.choice(neighbors)
        current_node = next_node

    return current_node



def find_longest_path_approx(component_graph: nx.Graph, max_depth: int = None) -> int:
    """
    Get the longest path. 
    :return: Number of nodes of the longest path.
    """
    longest_path_length = 0
    for node in component_graph.nodes:
        # Depth is 2 * number of nodes
        if max_depth is None:
            max_depth = component_graph.number_of_nodes()
        path_length = nx.single_source_shortest_path(component_graph, node, cutoff=max_depth) # not path, lengths
        longest_path_length = max(longest_path_length, len(path_length))
    return longest_path_length



def add_dynamic_legend_to_component_graph(html_file: str) -> None:
    """
    Adds a dynamic legend to the component graph HTML file that updates on click.
    
    
    :params: html_file (str): The path to the HTML file.
    """
    
    js_code = """
    <script>
        // Function to update the legend
        function updateLegend(content) {
            const legend = document.getElementById('language-legend');
            legend.innerHTML = content;
        }

        // Add event listeners to edges using vis.js API
        network.on("hoverEdge", function (params) {
            const edgeId = params.edge;
            const edge = edges.get(edgeId);
            if (edge && edge.languages) {
                const languagesList = edge.languages.split(', ').map(lang => `<li>${lang}</li>`).join('');
                const numLanguages = edge.languages.split(', ').length;
                const nodePair = `${edge.from} - ${edge.to}`;
                updateLegend(`<h3>Languages (${numLanguages}) for ${nodePair}:</h3><ul>${languagesList}</ul>`);
            }
        });

        network.on("blurEdge", function () {
            updateLegend('<h3>Languages:</h3><p>Hover over an edge to see languages.</p>');
        });

        network.on("click", function (params) {
            if (params.edges && params.edges.length > 0) {
                const edgeId = params.edges[0];
                const edge = edges.get(edgeId);
                if (edge && edge.languages) {
                    const languagesList = edge.languages.split(', ').sort().map(lang => `<li>${lang.replaceAll(";;", " - ")}</li>`).join('');
                    const numLanguages = edge.languages.split(', ').length;
                    const title1 = edge.from.replaceAll(";;", "&#10;");
                    const title2 = edge.to.replaceAll(";;", "&#10;");
                    updateLegend(`<h2><div title="${title1}";>${edge.from.split(";;")[0]}</div><div title="${title2}";>${edge.to.split(";;")[0]}</div></h2><br><h3>Languages (${numLanguages})<br></h3><ul>${languagesList}</ul>`);
                }
            }
        });
    </script>
    <style>
        html {
            background: darkgray;
        }
        .container {
            display: flex;
            width: 100%;
            margin-top: 48px;
        }
        #mynetwork {
            flex: 3;
            height: 750px;
            width: 90%
            background-color: #222222;
            border: 1px solid lightgray;
        }
        #language-legend h2 {
            display: flex; 
            flex-direction: column;
            font-weight: bold;
        }
        #language-legend h3 {
             border-bottom: 1px solid black; 
             padding-bottom: 8px
        }
        #language-legend {
            flex: 1;
            margin-left: 20px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            background-color: #f9f9f9;
            overflow-y: auto;
            max-height: 750px;
        }
        #language-legend ul {
            list-style-type: none;
            padding: 0;
        }
        #language-legend li {
            margin: 5px 0;
            font-size: 1.2em;
        }
    </style>
    """

    legend_html = """
    <div id="language-legend">
        <h3>Languages:</h3>
        <p>Click on an edge to see languages.</p>
    </div>
    """

    with open(html_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Put the network and legend in a flex container
    html_content = html_content.replace(
        '<div id="mynetwork" class="card-body"></div>',
        f'<div class="container"><div id="mynetwork" class="card-body"></div>{legend_html}</div>'
    )

    # Insert the JavaScript before the closing </body> tag
    html_content = html_content.replace(
        '</body>',
        f'{js_code}</body>'
    )

    # Save the modified HTML content
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)