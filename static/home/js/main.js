$(function () {

  var infinite = new Waypoint.Infinite({
    element: $('.infinite-container')[0],
    offset: '50%',
    onBeforePageLoad: function () {
        $('.loading').show();
    },
    onAfterPageLoad: function () {
        $('.loading').hide();
    }
    });
    
  if ($('.owl-2').length > 0) {
    $('.owl-2').owlCarousel({
      center: false,
      items: 2,
      loop: true,
      stagePadding: 0,
      margin: 0,
      smartSpeed: 1000,
      autoplay: true,
      nav: false,
      dots: true,
      pauseOnHover: true,
      responsive: {
        400: {
          padding: 0,
          nav: false,
          items: 2
        },
        600: {
          padding: 0,
          nav: false,
          items: 3
        },

        800: {
          padding: 0,
          nav: false,
          items: 4
        },
        1024: {
          padding: 0,
          nav: false,
          items: 5
        },
        1200: {
          margin: 0,
          stagePadding: 0,
          nav: false,
          items: 5
        },

        1800: {
          padding: 20,
          nav: false,
          items: 6
        },
      }
    });
  }

  if ($('.owl-3').length > 0) {
    $('.owl-3').owlCarousel({
      center: false,
      items: 2,
      loop: true,
      stagePadding: 0,
      margin: 0,
      padding: 0,
      smartSpeed: 1000,
      autoplay: false,
      nav: true,
      dots: true,
      pauseOnHover: false,
      responsive: {
        400: {
          padding: 0,
          nav: true,
          items: 2
        },
        600: {
          padding: 0,
          nav: true,
          items: 3
        },

        800: {
          padding: 0,
          nav: true,
          items: 4
        },
        1024: {
          padding: 0,
          nav: true,
          items: 5
        },
        1200: {
          margin: 0,
          stagePadding: 0,
          nav: true,
          items: 6
        },

        1800: {
          padding: 20,
          nav: true,
          items: 8
        },
      }
    });
  }
  if ($('.owl-4').length > 0) {
    $('.owl-4').owlCarousel({
      center: false,
      items: 2,
      loop: true,
      stagePadding: 0,
      margin: 0,
      smartSpeed: 1000,
      autoplay: true,
      nav: true,
      dots: true,
      pauseOnHover: true,

      responsive: {
        400: {
          padding: 0,
          nav: true,
          items: 2
        },
        600: {
          padding: 0,
          nav: true,
          items: 3
        },

        800: {
          padding: 0,
          nav: true,
          items: 4
        },
        1024: {
          padding: 0,
          nav: true,
          items: 5
        },
        1200: {
          margin: 0,
          stagePadding: 0,
          nav: true,
          items: 6
        },

        1800: {
          padding: 20,
          nav: true,
          items: 8
        },
      }
    });
  }
  
  if ($('.owl-5').length > 0) {
    $('.owl-5').owlCarousel({
      center: false,
      items: 3,
      loop: true,
      stagePadding: 0,
      margin: 0,
      padding: 0,
      smartSpeed: 1000,
      autoplay: true,
      nav: true,
      dots: true,
      pauseOnHover: true,
      responsive: {
        400: {
          padding: 0,
          nav: true,
          items: 4
        },
        600: {
          padding: 0,
          nav: true,
          items: 5
        },

        800: {
          padding: 0,
          nav: true,
          items: 6
        },
        1024: {
          padding: 0,
          nav: true,
          items: 6
        },
        1200: {
          margin: 0,
          stagePadding: 0,
          nav: true,
          items: 8
        },

        1400: {
          padding: 20,
          nav: true,
          items: 9
        },
      }
    });
  }
  
  
  if ($('.owl-6').length > 0) {
    $('.owl-6').owlCarousel({
      center: false,
      items: 3,
      loop: true,
      stagePadding: 0,
      margin: 0,
      padding: 0,
      smartSpeed: 1000,
      autoplay: true,
      nav: true,
      dots: true,
      pauseOnHover: false,
      responsive: {
        400: {
          padding: 0,
          nav: true,
          items: 4
        },
        600: {
          padding: 0,
          nav: true,
          items: 5
        },

        800: {
          padding: 0,
          nav: true,
          items: 6
        },
        1024: {
          padding: 0,
          nav: true,
          items: 8
        },
        1200: {
          margin: 0,
          stagePadding: 0,
          nav: true,
          items: 10
        },

        1800: {
          padding: 20,
          nav: true,
          items: 12
        },
      }
    });
  }

  
  if ($('.owl-7').length > 0) {
    $('.owl-7').owlCarousel({
      center: true,
      items: 2,
      loop: true,
      stagePadding: 0,
      margin: 0,
      padding: 0,
      smartSpeed: 1000,
      autoplay: false,
      nav: true,
      dots: true,
      pauseOnHover: true,
      responsive: {
        400: {
          padding: 0,
          nav: true,
          items: 2
        },

        800: {
          padding: 0,
          nav: true,
          items: 3
        },
        1200: {
          margin: 0,
          stagePadding: 0,
          nav: true,
          items: 4
        },

        1800: {
          padding: 20,
          nav: true,
          items: 5
        },
      }
    });
  }

  if ($('.owl-8').length > 0) {
    $('.owl-8').owlCarousel({
      center: false,
      items: 2,
      loop: true,
      stagePadding: 0,
      margin: 0,
      padding: 0,
      smartSpeed: 1000,
      autoplay: false,
      nav: true,
      dots: true,
      pauseOnHover: false,
      
      responsive: {
        400: {
          padding: 0,
          nav: true,
          items: 2
        },

        800: {
          padding: 0,
          nav: true,
          items: 3
        },
        1200: {
          margin: 0,
          stagePadding: 0,
          nav: true,
          items: 5
        },

        1800: {
          padding: 20,
          nav: true,
          items: 6
        },
      }
    });
  }

  
  if ($('.owl-9').length > 0) {
    $('.owl-9').owlCarousel({
      center: false,
      items: 3,
      loop: true,
      stagePadding: 0,
      margin: 0,
      padding: 0,
      smartSpeed: 1000,
      autoplay: false,
      nav: true,
      dots: true,
      pauseOnHover: false,
      responsive: {
        400: {
          padding: 0,
          nav: true,
          items: 5
        },
        600: {
          padding: 0,
          nav: true,
          items: 6
        },

        800: {
          padding: 0,
          nav: true,
          items: 7
        },
        1024: {
          padding: 0,
          nav: true,
          items: 8
        },
        1200: {
          margin: 0,
          stagePadding: 0,
          nav: true,
          items: 9
        },

        1400: {
          padding: 20,
          nav: true,
          items: 10
        },
      }
    });
  }

  if ($('.owl-10').length > 0) {
    $('.owl-10').owlCarousel({
      center: false,
      items: 1,
      loop: true,
      stagePadding: 0,
      margin: 0,
      padding: 0,
      smartSpeed: 1000,
      autoplay: true,
      nav: true,
      dots: true,
      pauseOnHover: false,
      responsive: {
        768: {
          padding: 0,
          nav: false,
          items: 2
        },
        1800: {
          padding: 0,
          nav: true,
          items: 4
        },
      }

    });
  }
  

})