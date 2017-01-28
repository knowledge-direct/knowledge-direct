(function($) {

  $(document).ready(function() {
    $.getJSON('/logged_in', function (data) {
      if (data['status']) {
        $('.user-name').text(data['name']);
        $('.logged-in').removeClass('hide');
      } else {
        $('.logged-out').removeClass('hide');
      }
    });
  });

})(jQuery);
