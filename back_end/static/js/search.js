(function($) {

  $(document).ready(function() {

    $.getJSON('/search_json?' + (window.location.href.substr(window.location.href.indexOf('?') + 1))
, function(data) {
      var list = data;
      var edges = [];
      var nodes = {};

      console.log(data);

      if ('list_of_papers' in data) {
        list = data['list_of_papers'];
        // edges = data['list_of_papers'][1];
        // nodes = data['list_of_papers'][2];
      }


      // Let's first initialize sigma:
      var s = new sigma('search-graph');

      // Then, let's add some data to display:

      for (var i = 0; i < list.length; i++) {
        var color = 'orange';
        if (i == 0) {
          color = 'red';
        } else if (i == list.length - 1) {
          color = 'green';
        }



        s.graph.addNode({
          // Main attributes:
          id: 'n' + i,
          label: list[i].title,
          // Display attributes:
          x: ((i + 0.0) / (list.length + 0.0)),
          y: ((i + 0.0) / (list.length + 0.0)),
          size: 1,
          color: color
        });

        // nodes[list[i].paper_id] = 'n' + i;

        if (i > 0) {
          s.graph.addEdge({
            id: 'e' + (i - 1),
            // Reference extremities:
            source: 'n' + (i - 1),
            target: 'n' + i
          })
        }
      }

      // for (var i = 0; i < nodes.length; i++) {
      //   try {
      //     s.graph.addNode({
      //       // Main attributes:
      //       id: 'nn' + i,
      //       label: nodes[i].title,
      //       // Display attributes:
      //       x: Math.random(),
      //       y: Math.random(),
      //       size: 1,
      //       color: 'grey'
      //     })
      //
      //     nodes[list[i].paper_id] = 'nn' + i;
      //   } catch (e) {
      //     console.log(e);
      //   }
      // }

      // for (var i = 0; i < edges.length; i++) {
      //   try {
      //     s.graph.addEdge({
      //       id: 'ee' + i,
      //       source: nodes[edges[i][0]],
      //       target: nodes[edges[i][1]]
      //     })
      //   } catch (e) {
      //     console.log(e);
      //   }
      //
      // }

      // console.log(nodes);
      // console.log(edges);

      // Finally, let's ask our sigma instance to refresh:
      s.refresh();
    });

  });

})(jQuery);
