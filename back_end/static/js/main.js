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
  });

})(jQuery);
