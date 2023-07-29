$(function() {

	$('.owl-1').owlCarousel({

    loop:false,
    margin:0,
    nav:false,
    items: 1,
    smartSpeed: 500,
    autoplay: true,
    autoplayHoverPause: true,
    dots:false,
    
    navText: ['<span class="icon-keyboard_arrow_left ">', '<span class="icon-keyboard_arrow_right">']
	});

    // Owl Carousel categ
    var owl = $(".owl-carousel-category");
    owl.owlCarousel({
      items: 4,
      margin: 5,
      loop: false,
      nav: false,
      responsive: {
          0:{
            items: 1
          },
          480:{
            items: 2
          },
          769:{
            items: 3
          },
          1100:{
            items: 4
          },
          1300:{
            items: 5
          },
          1400:{
            items: 6
          }
      }
    });

	
})
