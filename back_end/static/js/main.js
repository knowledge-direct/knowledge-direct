(function($) {

  $(document).ready(function() {
    $('.next').on('click', function(e) {
      e.preventDefault();
      $('section.target').show();
      $('section.target-button').show();
      $('section.base').hide();
      $('section.base-button').hide();
      $('body').scrollTop(0);
    });
    $('.back').on('click', function(e) {
      e.preventDefault();
      $('section.target').hide();
      $('section.target-button').hide();
      $('section.base').show();
      $('section.base-button').show();
      $('body').scrollTop(0);
    });

    $('.toggle-read').on('click', function() {
      var dataElem = $(this).parent();
      var paper_id = dataElem.data('paper-id');
      console.log(dataElem.data('read'));
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

})(jQuery);
