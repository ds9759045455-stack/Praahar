class MuleGraphVisualizer {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.network = null;
  }

  render(graphData) {
    if (!this.container || !graphData || !graphData.vis_graph) return;

    const data = {
      nodes: new vis.DataSet(graphData.vis_graph.nodes),
      edges: new vis.DataSet(graphData.vis_graph.edges)
    };

    const options = {
      nodes: {
        font: { color: '#ffffff', size: 12, face: 'Inter, sans-serif' },
        borderWidth: 2,
        shadow: true
      },
      edges: {
        width: 1.5,
        smooth: { type: 'continuous' },
        shadow: true
      },
      layout: {
        hierarchical: {
          direction: 'UD', // Up to Down (Layer 1 -> 2 -> 3)
          sortMethod: 'directed',
          levelSeparation: 120,
          nodeSpacing: 160
        }
      },
      physics: {
        hierarchicalRepulsion: {
          nodeDistance: 150
        }
      },
      interaction: {
        hover: true,
        tooltipDelay: 100,
        zoomView: true
      }
    };

    if (this.network) {
      this.network.destroy();
    }

    this.network = new vis.Network(this.container, data, options);

    this.network.on("click", (params) => {
      if (params.nodes.length > 0) {
        const nodeId = params.nodes[0];
        console.log("Selected node:", nodeId);
        if (window.app && window.app.highlightMuleNode) {
          window.app.highlightMuleNode(nodeId);
        }
      }
    });
  }
}

window.MuleGraphVisualizer = MuleGraphVisualizer;
