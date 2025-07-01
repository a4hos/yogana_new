/*
  Theme Name:  A4 Hospital - Hospital A4 Hospital HTML Template
  Author: LAMA Technologies
  Description: hospital theme
  Version: 1.5
*/

(function($) {
    "use strict";

    $(document).on('ready', function() {


		/* ==================================================
			# Data Background
		 ===============================================*/

		$("[data-background]").each(function(){
			$(this).css("background-image","url(" + $(this).attr("data-background") +")");
		});

        /* ==================================================
            # Wow Init
         ===============================================*/
        var wow = new WOW({
            boxClass: 'wow', // animated element css class (default is wow)
            animateClass: 'animated', // animation css class (default is animated)
            offset: 0, // distance to the element when triggering the animation (default is 0)
            mobile: true, // trigger animations on mobile devices (default is true)
            live: true // act on asynchronously loaded content (default is true)
        });
        wow.init();
	
		
		
        /* ==================================================
            # Smooth Scroll
         =============================================== */
        
		$("body").scrollspy({
            target: ".navbar-collapse",
            offset: 200
        });
        $('a.smooth-menu').on('click', function(event) {
            var $anchor = $(this);
            var headerH = '85';
            $('html, body').stop().animate({
                scrollTop: $($anchor.attr('href')).offset().top - headerH + "px"
            }, 1500, 'easeInOutExpo');
            event.preventDefault();
        });
		
		
		/* ==================================================
            # Button Drop down
         =============================================== */
		
		$('dropdown-toggle').dropdown();
		
		 /* ==================================================
            # Scroll to top
         =============================================== */
			//Get the button
			var mybutton = document.getElementById("scrtop");

			// When the user scrolls down 20px from the top of the document, show the button
			window.onscroll = function() {scrollFunction()};

			function scrollFunction() {
			  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
				mybutton.style.display = "block";
			  } else {
				mybutton.style.display = "none";
			  }
			}

		 /* ==================================================
            # Youtube Video Init
         ===============================================*/
        $('.player').mb_YTPlayer();
	
		/* ==================================================
			# Accordion Menu
		 =============================================== */
		
		  $(document).on('click','.panel-group .panel',function(e) {
			e.preventDefault();
			$(this).addClass('panel-active').siblings().removeClass('panel-active');
		});
		
        /* ==================================================
            # imagesLoaded active
        ===============================================*/
        $('#portfolio-grid,.blog-masonry').imagesLoaded(function() {

            /* Filter menu */
            $('.mix-item-menu').on('click', 'button', function() {
                var filterValue = $(this).attr('data-filter');
                $grid.isotope({
                    filter: filterValue
                });
            });

            /* filter menu active class  */
            $('.mix-item-menu button').on('click', function(event) {
                $(this).siblings('.active').removeClass('active');
                $(this).addClass('active');
                event.preventDefault();
            });

            /* Filter active */
            var $grid = $('#portfolio-grid').isotope({
                itemSelector: '.pf-item',
                percentPosition: true,
                masonry: {
                    columnWidth: '.pf-item',
                }
            });

            /* Filter active */
            $('.blog-masonry').isotope({
                itemSelector: '.blog-item',
                percentPosition: true,
                masonry: {
                    columnWidth: '.blog-item',
                }
            });

        });
		
		
        /* ==================================================
            # Magnific popup init
         ===============================================*/
        $(".popup-link").magnificPopup({
            type: 'image',
            // other options
        });

        $(".popup-gallery").magnificPopup({
            type: 'image',
            gallery: {
                enabled: true
            },
            // other options
        });

        $(".popup-youtube, .popup-vimeo, .popup-gmaps").magnificPopup({
            type: "iframe",
            mainClass: "mfp-fade",
            removalDelay: 160,
            preloader: false,
            fixedContentPos: false
        });

        $('.magnific-mix-gallery').each(function() {
            var $container = $(this);
            var $imageLinks = $container.find('.item');

            var items = [];
            $imageLinks.each(function() {
                var $item = $(this);
                var type = 'image';
                if ($item.hasClass('magnific-iframe')) {
                    type = 'iframe';
                }
                var magItem = {
                    src: $item.attr('href'),
                    type: type
                };
                magItem.title = $item.data('title');
                items.push(magItem);
            });

            $imageLinks.magnificPopup({
                mainClass: 'mfp-fade',
                items: items,
                gallery: {
                    enabled: true,
                    tPrev: $(this).data('prev-text'),
                    tNext: $(this).data('next-text')
                },
                type: 'image',
                callbacks: {
                    beforeOpen: function() {
                        var index = $imageLinks.index(this.st.el);
                        if (-1 !== index) {
                            this.goTo(index);
                        }
                    }
                }
            });
        });
		

        /* ==================================================
            # Partner Carousel
         ===============================================*/
		
        $('.brand-wrapper').owlCarousel({
            loop: true,
            margin:30,
            nav: false,
            navText: [
                "<i class='fa fa-angle-left'></i>",
                "<i class='fa fa-angle-right'></i>"
            ],
            dots: false,
            autoplay: true,
            responsive: {
                0: {
                    items: 2
                },
                600: {
                    items: 3
                },
                1000: {
                    items: 5
                }
            }
        });
		
		 /* ==================================================
            # Review Carousel
         ===============================================*/
		
        $('.f1-wrapper').owlCarousel({
            loop: true,
            margin:30,
            nav: false,
            navText: [
                "<i class='fa fa-angle-left'></i>",
                "<i class='fa fa-angle-right'></i>"
            ],
            dots: true,
            autoplay: true,
            responsive: {
                0: {
                    items: 1
                },
                600: {
                    items: 1
                },
                1000: {
                    items: 2
                }
            }
        });
		
		/* ==================================================
			# Review Carousel
		 ===============================================*/

			$('.fd-sldr').owlCarousel({
				loop: true,
				margin:30,
				nav: false,
				navText: [
					"<i class='fa fa-angle-left'></i>",
					"<i class='fa fa-angle-right'></i>"
				],
				dots: true,
				autoplay: true,
				responsive: {
					0: {
						items: 1
					},
					600: {
						items: 1
					},
					1000: {
						items: 2
					}
				}
			});
		
		/* ==================================================
            # Partner Carousel
         ===============================================*/
		
        $('.hero-sldr').owlCarousel({
            loop: true,
            margin:0,
            nav: false,
            navText: [
                "<i class='fa fa-angle-left'></i>",
                "<i class='fa fa-angle-right'></i>"
            ],
            dots: true,
            autoplay: true,
            responsive: {
                0: {
                    items: 1
                },
                600: {
                    items: 1
                },
                1000: {
                    items: 1
                }
            }
        });
		
		/* ==================================================
            # Cate Carousel
         ===============================================*/
		
        $('.cate-wrapper').owlCarousel({
            loop: true,
            margin:30,
            nav: true,
            navText: [
                "<i class='ti ti-arrow-left'></i>",
                "<i class='ti ti-arrow-right'></i>"
            ],
            dots: false,
            autoplay: true,
            responsive: {
                0: {
                    items: 1
                },
                600: {
                    items: 2
                },
                1000: {
                    items: 4
                }
            }
        });
		
		
		/* ==================================================
            # Team Carousel 
         ===============================================*/
		
        $('.team-sldr').owlCarousel({
            loop: true,
            margin:30,
            nav: false,
            navText: [
                "<i class='fa fa-angle-left'></i>",
                "<i class='fa fa-angle-right'></i>"
            ],
            dots: true,
            autoplay: true,
            responsive: {
                0: {
                    items: 1
                },
                600: {
                    items: 2
                },
                1000: {
                    items: 3
                }
            }
        });
		
		
		
        /* ==================================================
            # Hero Slider Carousel
         ===============================================*/
		
        $('.hero-slider').owlCarousel({
            loop: true,
            nav: true,
            dots: false,
            autoplay: true,
			autoplayTimeout:5000,
            items: 1,
            navText: [
                "<i class='ti-angle-left'></i>",
                "<i class='ti-angle-right'></i>"
            ],
        });
		

		/* ==================================================
            # Feedback
         ===============================================*/
		
			$('.partner-wrapper').owlCarousel({
            loop: true,
            margin:30,
            nav: false,
            navText: [
                "<i class='fa fa-angle-left'></i>",
                "<i class='fa fa-angle-right'></i>"
            ],
            dots: false,
            autoplay: true,
            responsive: {
                0: {
                    items: 1
                },
                600: {
                    items: 4
                },
                1000: {
                    items: 5
                }
            }
        });
		
		
		/* ==================================================
            # Review
         ===============================================*/
		
			$('.review-wrapper').owlCarousel({
            loop: true,
            margin:30,
            nav: false,
            navText: [
                "<i class='fa fa-angle-left'></i>",
                "<i class='fa fa-angle-right'></i>"
            ],
            dots: true,
            autoplay: true,
            responsive: {
                0: {
                    items: 1
                },
                600: {
                    items: 2
                },
                1000: {
                    items: 3
                }
            }
        });
		
		/* ==================================================
            # Review
         ===============================================*/
		
			$('.feed-wrapper').owlCarousel({
            loop: true,
            margin:30,
            nav: false,
            navText: [
                "<i class='fa fa-angle-left'></i>",
                "<i class='fa fa-angle-right'></i>"
            ],
            dots: true,
            autoplay: true,
            responsive: {
                0: {
                    items: 1
                },
                600: {
                    items: 1
                },
                1000: {
                    items: 1
                }
            }
        });
		
		
		/* ==================================================
            # Choose Slider
         ===============================================*/
		
		$('.wh-wrapper').owlCarousel({
            loop: true,
            margin:30,
            nav: false,
            navText: [
                "<i class='fa fa-angle-left'></i>",
                "<i class='fa fa-angle-right'></i>"
            ],
            dots: true,
            autoplay: true,
            responsive: {
                0: {
                    items: 1
                },
                800: {
                    items: 2
                },
                1000: {
                    items: 3
                }
            }
        });
		
		/* ==================================================
            # partner slider
         ===============================================*/
		
		$('.p1-wrapper').owlCarousel({
            loop: true,
            margin:50,
            nav: false,
            navText: [
                "<i class='fa fa-angle-left'></i>",
                "<i class='fa fa-angle-right'></i>"
            ],
            dots: false,
            autoplay: true,
            responsive: {
                0: {
                    items: 2
                },
                768: {
                    items: 4
                },
                1000: {
                    items: 5
                }
            }
        });
		
		/* ==================================================
            # Ab Slider
         ===============================================*/
		
		$('.ab-course-wrapper').owlCarousel({
            loop: true,
            margin:30,
            nav: true,
            navText: [
                "<i class='fa fa-angle-left'></i>",
                "<i class='fa fa-angle-right'></i>"
            ],
            dots: false,
            autoplay: true,
            responsive: {
                0: {
                    items: 1
                },
                800: {
                    items: 2
                },
                1000: {
                    items: 2
                }
            }
        });
		
		/* ==================================================
            # Product  Slider
         ===============================================*/
		
		$('.tba-sldr').owlCarousel({
            loop: true,
            margin:0,
            nav: true,
            navText: [
                "<i class='ti ti-arrow-left'></i>",
                "<i class='ti ti-arrow-right'></i>"
            ],
            dots: false,
            autoplay: false,
            responsive: {
                0: {
                    items: 1
                },
                800: {
                    items: 1
                },
                1000: {
                    items: 1
                }
            }
        });
		
		
		
		
		/* ==================================================
			# Weekly Deals
	 	===============================================*/
		/**
		 * WARNING: I set this coundtown to be running until the end of times.
		 * So when you'll init the plugin, follow how it's done in plugin documentation.
		 * e.g : instead of "month: d.getMonth() + 1" put "month: 10" for October.
		 */
		var d = new Date(),
			countUpDate = new Date();
		d.setDate(d.getDate() + 450);

		// direct element injection & Count Up Example
		var countUp = document.querySelector('.simply-countdown-countup');
		simplyCountdown(countUp, {
			year: countUpDate.getFullYear(),
			month: countUpDate.getMonth() + 1,
			day: countUpDate.getDate() +15,
			hours: countUpDate.getHours() + 14,
			minutes: countUpDate.getMinutes(),
			seconds: countUpDate.getSeconds(),
			countUp: true
		});
		
		// default example
		simplyCountdown('.simply-countdown-one', {
			year: d.getFullYear(),
			month: d.getMonth() + 1,
			day: d.getDate(),
			enableUtc: true
		});

		// inline example
		simplyCountdown('.simply-countdown-inline', {
			year: d.getFullYear(),
			month: d.getMonth() + 1,
			day: d.getDate(),
			inline: true
		});

		//jQuery example
		$('#simply-countdown-losange').simplyCountdown({
			year: d.getFullYear(),
			month: d.getMonth() + 1,
			day: d.getDate(),
			enableUtc: false
		});

		
		
		/* ==================================================
          # Pie Chart 
         ===============================================*/
		
		$('.chart').easyPieChart({
			size:140,
			barColor:'#42538F',
			scaleColor:false,
			lineWidth:15,
			trackColor:'#f5f5f5'
		});

        /* ==================================================
            # Fun Factor Init
        ===============================================*/
// Initialize counter animation
$('.timer').each(function() {
    $(this).countTo({
        onComplete: function() {
            // When counting completes, hide the animated counter
            $(this).hide();
            // Show the display value (e.g., "12k") instead
            $(this).siblings('.display-value').show();
        }
    });
});

// Ensure animation runs when element is in view
$('.fun-fact').appear(function() {
    $(this).find('.timer').countTo();
}, {
    accY: -100
});



        /* ==================================================
            Preloader Init
         ===============================================*/
        $(window).on('load', function() {
            // Animate loader off screen
            $(".se-pre-con").fadeOut("slow");
        });
        
		
		 /* ==================================================
            Contact Form Validations
        ================================================== */
        $('.contact-form').each(function() {
            var formInstance = $(this);
            formInstance.submit(function() {

                var action = $(this).attr('action');

                $("#message").slideUp(750, function() {
                    $('#message').hide();

                    $('#submit')
                        .after('<img src="assets/img/logo/ajax-loader.gif" class="loader" />')
                        .attr('disabled', 'disabled');

                    $.post(action, {
                            name: $('#name').val(),
                            email: $('#email').val(),
							subject: $('#subject').val(),
                            website: $('#website').val(),
                            comments: $('#comments').val()
                        },
                        function(data) {
                            document.getElementById('message').innerHTML = data;
                            $('#message').slideDown('slow');
                            $('.contact-form img.loader').fadeOut('slow', function() {
                                $(this).remove();
                            });
                            $('#submit').removeAttr('disabled');
                        }
                    );
                });
                return false;
            });
        });
		
		/* ==================================================
		# Quantity
		===============================================*/
		
		function wcqib_refresh_quantity_increments() {
			jQuery("div.quantity:not(.buttons_added), td.quantity:not(.buttons_added)").each(function(a, b) {
				var c = jQuery(b);
				c.addClass("buttons_added"), c.children().first().before('<input type="button" value="-" class="minus" />'), c.children().last().after('<input type="button" value="+" class="plus" />')
			})
		}
		String.prototype.getDecimals || (String.prototype.getDecimals = function() {
			var a = this,
				b = ("" + a).match(/(?:\.(\d+))?(?:[eE]([+-]?\d+))?$/);
			return b ? Math.max(0, (b[1] ? b[1].length : 0) - (b[2] ? +b[2] : 0)) : 0
		}), jQuery(document).ready(function() {
			wcqib_refresh_quantity_increments()
		}), jQuery(document).on("updated_wc_div", function() {
			wcqib_refresh_quantity_increments()
		}), jQuery(document).on("click", ".plus, .minus", function() {
			var a = jQuery(this).closest(".quantity").find(".qty"),
				b = parseFloat(a.val()),
				c = parseFloat(a.attr("max")),
				d = parseFloat(a.attr("min")),
				e = a.attr("step");
			b && "" !== b && "NaN" !== b || (b = 0), "" !== c && "NaN" !== c || (c = ""), "" !== d && "NaN" !== d || (d = 0), "any" !== e && "" !== e && void 0 !== e && "NaN" !== parseFloat(e) || (e = 1), jQuery(this).is(".plus") ? c && b >= c ? a.val(c) : a.val((b + parseFloat(e)).toFixed(e.getDecimals())) : d && b <= d ? a.val(d) : b > 0 && a.val((b - parseFloat(e)).toFixed(e.getDecimals())), a.trigger("change")
		});

		
		/* ==================================================
		# Slick nav
		 ===============================================*/

		 $('.testimonial-active').slick({
			slidesToShow: 1,
			slidesToScroll: 1,
			arrows: false,
			fade: true,
			asNavFor: '.test-img-active',
			autoplay: true,
			autoplaySpeed: 5000,
		});

		$('.test-img-active').slick({
			slidesToShow: 1,
			slidesToScroll: 1,
			asNavFor: '.testimonial-active',
			dots: false,
			centerMode: true,
			focusOnSelect: true,
			arrows: false,
		});

		$(".testimonial-active").slick({
			lazyLoad: 'ondemand', // ondemand progressive anticipated
			infinite: true
		});
		
    }); // end document ready function
})(jQuery); // End jQuery