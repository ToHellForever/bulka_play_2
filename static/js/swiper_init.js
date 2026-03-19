// Инициализация Swiper для всех каруселей на сайте
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.swiper').forEach((swiperEl) => {
    // Проверяем, является ли это каруселью аренды
    const isRentalCarousel = swiperEl.closest('.carousel-container') &&
    swiperEl.closest('.carousel-container').querySelector('.rental_catalog_landing_h');

    // Проверяем, является ли это каруселью основного товара (мобильная версия)
    const isProductMainSwiperMobile = swiperEl.classList.contains('product-main-swiper-mobile');

    // Проверяем, является ли это каруселью основного товара (десктопная версия)
    const isProductMainSwiperDesktop = swiperEl.classList.contains('product-main-swiper-desktop');

    const swiperParams = {
      slidesPerGroup: 1,
      centeredSlides: true,
      autoplay: {
        delay: 2500,
        disableOnInteraction: false,
      },
      loop: true,
      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      },
      breakpoints: {}
    };

    // Устанавливаем разные параметры для карусели аренды, мобильной карусели товара и остальных каруселей
    if (isRentalCarousel) {
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
      swiperParams.speed = 500;
      swiperParams.allowTouchMove = false;
    } else {
      swiperParams.slidesPerView = 1.5;
      swiperParams.centeredSlides = true;
      swiperParams.spaceBetween = 30;
      swiperParams.breakpoints = {
        320: { slidesPerView: 1.5, spaceBetween: 10 },
        480: { slidesPerView: 2.5, spaceBetween: 20 },
        640: { slidesPerView: 3, spaceBetween: 40 }
      };
    }

    new Swiper(swiperEl, swiperParams);
  });
});