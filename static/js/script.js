(function ($) {
  'use strict';

  // Preloader js    
  $(window).on('load', function () {
    $('.preloader').fadeOut(700);
  });


  // modal video
  $('.videoplay').modalVideo();

  // hero slider
  $(window).on('load', function () {
    var menu = [];
    jQuery('.slide-item').each(function (index) {
      menu.push(jQuery(this).find('.slide-inner').attr('data-text'));
    });

    var interleaveOffset = 0.5;
    var swiperOptions = {
      loop: true,
      speed: 1000,
      parallax: true,
      autoplay: {
        delay: 6500,
        disableOnInteraction: false
      },
      watchSlidesProgress: true,
      pagination: {
        el: '.swiper-pagination',
        clickable: true
      },

      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev'
      },

      on: {
        progress: function () {
          var swiper = this;
          for (var i = 0; i < swiper.slides.length; i++) {
            var slideProgress = swiper.slides[i].progress;
            var innerOffset = swiper.width * interleaveOffset;
            var innerTranslate = slideProgress * innerOffset;
            swiper.slides[i].querySelector('.slide-inner').style.transform =
              'translate3d(' + innerTranslate + 'px, 0, 0)';
          }
        },

        touchStart: function () {
          var swiper = this;
          for (var i = 0; i < swiper.slides.length; i++) {
            swiper.slides[i].style.transition = '';
          }
        },

        setTransition: function (speed) {
          var swiper = this;
          for (var i = 0; i < swiper.slides.length; i++) {
            swiper.slides[i].style.transition = speed + 'ms';
            swiper.slides[i].querySelector('.main-sider-inner').style.transition =
              speed + 'ms';
          }
        }
      }
    };

    var swiper = new Swiper('.swiper-container-horizontal', swiperOptions);

    // gallery slider
    var swiper = new Swiper('#gallery-slider', {
      slidesPerView: 6,
      autoplay: {
        delay: 5000
      },
      loop: true,
      breakpoints: {
        1024: {
          slidesPerView: 4
        },
        768: {
          slidesPerView: 3
        },
        640: {
          slidesPerView: 2
        },
        320: {
          slidesPerView: 1
        }
      }
    });

    // Testimonial Slider
    var myswiper = new Swiper('#testimonial-slider', {
      slidesPerView: 1,
      autoplay: {
        delay: 5000
      }
    });
  });

  // DATA BACKGROUND IMAGE
  var sliderBgSetting = $('.slide-bg-image');
  sliderBgSetting.each(function (indx) {
    if ($(this).attr('data-background')) {
      $(this).css('background-image', 'url(' + $(this).data('background') + ')');
    }
  });

  // magnific popup
  $('.gallery-wrap').each(function () {
    $(this).find('.popup-gallery').magnificPopup({
      type: 'image',
      gallery: {
        enabled: true
      }
    });
  });

  $('.popup-gallery').magnificPopup({
    type: 'image',
    gallery: {
      enabled: true
    }
  });



  // Shuffle js filter and masonry
  var containerEl = document.querySelector('.shuffle-wrapper');
  if (containerEl) {
    var Shuffle = window.Shuffle;
    var myShuffle = new Shuffle(document.querySelector('.shuffle-wrapper'), {
      itemSelector: '.shuffle-item',
      buffer: 1
    });

    jQuery('input[name="shuffle-filter"]').on('change', function (evt) {
      var input = evt.currentTarget;
      if (input.checked) {
        myShuffle.filter(input.value);
      }
    });
  }


  // date picker
  $('#datepicker').data('datepicker')

  // timepicker
  $('#timepicker').clockpicker({
    autoclose: true
  });

  // touchpin
  $("input[name='quantity']").TouchSpin();

  // animate on scroll
  AOS.init({
    once: true
  });


  // instafeed
  if (($('#instafeed').length) !== 0) {
    var userId = $('#instafeed').attr('data-userId');
    var accessToken = $('#instafeed').attr('data-accessToken');
    var userFeed = new Instafeed({
      get: 'user',
      userId: userId,
      resolution: 'low_resolution',
      accessToken: accessToken,
      template: '<div class="swiper-slide"><a class="popup-gallery" href="{{image}}"><img src="{{image}}" class="img-fluid"></a></div>'
    });
    userFeed.run();
  }

})(jQuery);