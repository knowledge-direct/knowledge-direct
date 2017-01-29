(function($) {

  $(document).ready(function() {

    $('.toggle-read').on('click', function() {
      var dataElem = $(this).parent();
      var paper_id = dataElem.data('paper-id');
      if (dataElem.data('read') == 0) {
        $.post("/mark_read", { paper: paper_id }, function(data) {
          dataElem.data('read', 1);
          dataElem.addClass('read');
          dataElem.removeClass('unread');
        });
      } else {
        $.post("/mark_unread", { paper: paper_id }, function(data) {
          dataElem.data('read', 0);
          dataElem.removeClass('read');
          dataElem.addClass('unread');
        });
      }
    });
  });

  $('.paper-search').on('keyup', function() {
    $('.paper-list li').each(function() {
      if ($('.paper-search').val() != '') {
        if ($(this).text().toLowerCase().indexOf($('.paper-search').val()) > -1) {
          $(this).removeClass('hide');
        } else {
          $(this).addClass('hide');
        }
      } else {
        $(this).removeClass('hide');
      }
    });
  });

})(jQuery);
