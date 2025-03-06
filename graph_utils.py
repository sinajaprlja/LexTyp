def add_dynamic_legend(html_file: str, edge_to_languages: dict, focus_concept: str) -> None:
    """
    Adds a dynamic legend to the HTML file that updates on click.
    
    Args:
        html_file (str): The path to the HTML file.
        edge_to_languages (dict): A dictionary mapping edges to languages.
        focus_concept (str): The focus concept.
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
                    const languagesList = edge.languages.split(', ').map(lang => `<li>${lang.replaceAll(";;", " - ")}</li>`).join('');
                    const numLanguages = edge.languages.split(', ').length;
                    const title1 = edge.from.replaceAll(";;", "&#10;");
                    const title2 = edge.to.replaceAll(";;", "&#10;");
                    updateLegend(`<h2><div title="${title1}";>${edge.from.split(";;")[0]}</div><div title="${title2}";>${edge.to.split(";;")[0]}</div></h2><br><h3>Languages (${numLanguages})<br></h3><ul>${languagesList}</ul>`);
                }
            }
        });
    </script>
    <style>
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

    # Save
    output_file = f"networks/network_{focus_concept}.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)