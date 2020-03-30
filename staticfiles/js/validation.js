// slide show

$(".quick_links_block").ready(function() {
    $("#quickLinks").owlCarousel({
        autoPlay: 1000,loop: true,
        items : 1, // THIS IS IMPORTANT
        nav : true,
        dots : false,
        responsive : {
              480 : { items : 1  }, // from zero to 480 screen width 4 items
              768 : { items : 3  }, // from 480 screen widthto 768 6 items
              1024 : { items : 5   // from 768 screen width to 1024 8 items
              }
          },
    });
});

$(".logo_section_block").ready(function() {
    $("#logoSection").owlCarousel({
        autoPlay: 1000,
        loop: false,
        items : 1, // THIS IS IMPORTANT
        nav : true,
        dots : false,
        responsive : {
              480 : { items : 1  }, // from zero to 480 screen width 4 items
              768 : { items : 3  }, // from 480 screen widthto 768 6 items
              1025 : { items : 4   // from 768 screen width to 1024 8 items
              }
          },
    });
});