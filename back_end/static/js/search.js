(function($) {

  $(document).ready(function() {

    $.getJSON('/search_json?' + (window.location.href.substr(window.location.href.indexOf('?') + 1))
, function(data) {
      // Let's first initialize sigma:
      var s = new sigma('search-graph');

      // Then, let's add some data to display:

      for (var i = 0; i < data.length; i++) {
        var color = 'orange';
        if (i == 0) {
          color = 'red';
        } else if (i == data.length - 1) {
          color = 'green';
        }



        s.graph.addNode({
          // Main attributes:
          id: 'n' + i,
          label: data[i].title,
          // Display attributes:
          x: ((i + 0.0) / (data.length + 0.0)),
          y: ((i + 0.0) / (data.length + 0.0)),
          size: 1,
          color: color
        });

        if (i > 0) {
          s.graph.addEdge({
            id: 'e' + (i - 1),
            // Reference extremities:
            source: 'n' + (i - 1),
            target: 'n' + i
          })
        }
      }

      // Finally, let's ask our sigma instance to refresh:
      s.refresh();
    });

  });

})(jQuery);
