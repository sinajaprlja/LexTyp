from collections import defaultdict
import json
import random
import networkx as nx
from networkx import NetworkXError
from pyvis.network import Network

from edge import Edge
import settings



def create_graph(focus_concept: str, graph: nx.Graph, edge_map: dict) -> None:
    """
    Creates an interactive network and saves it as a HTML file.
    
    Args:
        focus_concept (str): The concept for which the network should be created.
        For Example: "free;;(social) unconstrained.;;not imprisoned or enslaved."
    """
    ## Validate input TODO
    try:
        # Get all neighbors of the focus concept
        neighbors = list(graph.neighbors(focus_concept))
    except NetworkXError:
        print(f"Invalid focus_concept={focus_concept}. Dataset does not contain this concept.")
        return

    # Create a pyvis network
    net = Network(notebook=False, height="750px", width="100%", bgcolor="#222222", font_color="white")

    # Create a subgraph containing the focus concept and its neighbors
    local_subgraph = graph.subgraph([focus_concept] + neighbors)

    # Map edges to the languages that connect them
    edge_to_languages = defaultdict(tuple)

    subgraph_maximum = 0
    for pair in local_subgraph.edges():
        pair = tuple(sorted(list(pair)))
        edge = edge_map[pair]
        edge_to_languages[pair] = edge.value

        if edge.weight > subgraph_maximum:
            subgraph_maximum = edge.weight


    # Add nodes to the pyvis network
    for node in local_subgraph.nodes:
        net.add_node(node, title=node, label=node.split(settings.SEPERATOR)[0])

    # Add edges with language information
    for pair, languages in edge_to_languages.items():
        edge: Edge = edge_map[pair]
        value = edge.weight
        width = edge.normalized(subgraph_maximum)
        net.add_edge(*pair, value=value, languages=', '.join(languages), width=width)

    # Save graph to a temporary file
    temp_file = "resources/temp_network.html"
    net.save_graph(temp_file)

    # Add dynamic legend to the HTML file
    add_dynamic_legend_to_component_graph(temp_file)

    print(f"Saved html Network '{focus_concept}'.")



def save_results_to_file(results, filename):
    """
    Saves results to a JSON file.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
        


def random_walk_in_component(component_graph, start_node, walk_length):
    """
    Performs a random walk in a component. Ganz oft aufrufen auf dem gleichen (für alle im graphen) Knoten udn dann wahrscheinlichkeitsverteilung über output (5% dieser Knoten, 10% anmderer usw.)
    """
    current_node = start_node 

    for _ in range(walk_length - 1):
        neighbors = list(component_graph.neighbors(current_node)) + [current_node]
        next_node = random.choice(neighbors)
        current_node = next_node

    return current_node



def find_longest_path_approx(component_graph, max_depth=None) -> int:
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
    
    Args:
        html_file (str): The path to the HTML file.
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

    # Create the initial legend HTML
    legend_html = """
    <div id="language-legend">
        <h3>Languages:</h3>
        <p>Click on an edge to see languages.</p>
    </div>
    """

    # Read the HTML file
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