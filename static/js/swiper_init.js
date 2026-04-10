// Инициализация Swiper для всех каруселей на сайте
document.addEventListener('DOMContentLoaded', () => {
  // Проверяем, что Swiper загружен
  if (typeof Swiper === 'undefined') {
    console.error('Swiper library is not loaded!');
    return;
  }

  document.querySelectorAll('.swiper').forEach((swiperEl) => {
    // Проверяем, является ли это каруселью аренды
    const carouselContainer = swiperEl.closest('.carousel-container');
    const isRentalCarousel = carouselContainer && carouselContainer.querySelector('.rental_catalog_landing_h');

    // Проверяем, является ли это каруселью на главной странице
    const isLandingCarousel = carouselContainer && carouselContainer.querySelector('.game_catalog_h, .rental_catalog_landing_h');

    // Проверяем, является ли это каруселью основного товара (мобильная версия)
    const isProductMainSwiperMobile = swiperEl.classList.contains('product-main-swiper-mobile');

    // Проверяем, является ли это каруселью основного товара (десктопная версия)
    const isProductMainSwiperDesktop = swiperEl.classList.contains('product-main-swiper-desktop');

    // Проверяем наличие кнопок навигации
    const prevButton = swiperEl.parentNode.querySelector('.swiper-button-prev');
    const nextButton = swiperEl.parentNode.querySelector('.swiper-button-next');

    const swiperParams = {
      slidesPerGroup: 1,
      centeredSlides: true,
      autoplay: {
        delay: 2500,
        disableOnInteraction: false,
      },
      loop: true,
      speed: 800,
      easing: 'cubic-bezier(0.4, 0, 0.2, 1)',
      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      },
      touchRatio: 0.5,
      breakpoints: {},
    };

    // Устанавливаем разные параметры для карусели аренды, мобильной карусели товара и остальных каруселей
    if (isLandingCarousel) {
      // Настройки для каруселей на главной странице
      swiperParams.slidesPerView = 1.2;
      swiperParams.spaceBetween = 20;
      swiperParams.loop = true;
      swiperParams.grabCursor = true;
      swiperParams.effect = 'coverflow';
      swiperParams.speed = 1000;
      swiperParams.touchRatio = 0.5;
      swiperParams.coverflowEffect = {
        rotate: 0,
        stretch: 0,
        depth: 100,
        modifier: 2.5,
        slideShadows: true,
      };
      
      swiperParams.breakpoints = {
        758: {
          slidesPerView: 2.1,
          spaceBetween: 30,
          effect: 'coverflow',
          coverflowEffect: {
            rotate: 0,
            stretch: 0,
            depth: 100,
            modifier: 2.5,
            slideShadows: true,
          }
        },
        1100: {
          slidesPerView: 3,
          spaceBetween: 30,
          effect: 'coverflow',
          coverflowEffect: {
            rotate: 0,
            stretch: 0,
            depth: 100,
            modifier: 2.5,
            slideShadows: true,
          }
        }
      };
    } else if (isRentalCarousel) {
      // Настройки для карусели аренды - 1 товар на слайде для мобильных, 3 для десктопа
      swiperParams.slidesPerView = 3;
      swiperParams.spaceBetween = 40;
      swiperParams.breakpoints = {
        320: { slidesPerView: 1, spaceBetween: 10 },
        700: { slidesPerView: 2, spaceBetween: 20 },
        992: { slidesPerView: 2, spaceBetween: 40 },
        1200: { slidesPerView: 3, spaceBetween: 40 }
      };
    } else if (isProductMainSwiperMobile) {
      // Настройки для мобильной карусели товара
      swiperParams.slidesPerView = 1;
      swiperParams.spaceBetween = 0;
      swiperParams.centeredSlides = true;
      swiperParams.loop = true;
      swiperParams.autoplay = false;
      swiperParams.navigation = {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      };
      swiperParams.breakpoints = {
        320: { slidesPerView: 1, spaceBetween: 10 },
        650: { slidesPerView: 2, spaceBetween: 20 },
        992: { slidesPerView: 2, spaceBetween: 40 },
        1200: { slidesPerView: 3, spaceBetween: 40 }
      };
    } else if (isProductMainSwiperDesktop) {
      // Настройки для десктопной карусели товара
      swiperParams.slidesPerView = 1;
      swiperParams.spaceBetween = 0;
      swiperParams.centeredSlides = true;
      swiperParams.loop = true;
      swiperParams.autoplay = {
        delay: 2500,
        disableOnInteraction: false,
      };
      swiperParams.navigation = {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      };
      swiperParams.effect = 'slide';
      swiperParams.speed = 1000;
      swiperParams.allowTouchMove = false;
      swiperParams.touchRatio = 0.5;
    } else {
      swiperParams.slidesPerView = 1.5;
      swiperParams.centeredSlides = true;
      swiperParams.spaceBetween = 30;
      swiperParams.speed = 1000;
      swiperParams.touchRatio = 0.5;
      swiperParams.breakpoints = {
        320: { slidesPerView: 1.5, spaceBetween: 10 },
        480: { slidesPerView: 2.5, spaceBetween: 20 },
        640: { slidesPerView: 3, spaceBetween: 40 }
      };
    }

    const isMobile = window.innerWidth < 768;

    if (isMobile) {
      swiperParams.autoplay.delay = 3500; 
    }

    new Swiper(swiperEl, swiperParams);
  });
});