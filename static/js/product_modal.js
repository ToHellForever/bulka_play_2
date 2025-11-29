// Управление модальным окном продукта
let productSlideIndex = 0;
let productSlides = [];

// Открытие модального окна продукта
function openProductModal(productId) {
    const modal = document.getElementById('productModal');
    const carouselInner = document.querySelector('.product-carousel-inner');

    // Очистка предыдущих слайдов
    carouselInner.innerHTML = '';
    
    // Получаем основное изображение продукта
    const mainImage = document.querySelector(`.product_detail_image`);
    const additionalImages = document.querySelectorAll(`.additional_images`);

    // Собираем все изображения
    const images = [];
    if (mainImage) {
        images.push(mainImage.src);
    }
    additionalImages.forEach(img => {
        images.push(img.src);
    });

    // Добавление новых слайдов
    images.forEach((image, index) => {
        const slide = document.createElement('div');
        slide.className = 'news-carousel-item';
        slide.innerHTML = `<img src="${image}" alt="Слайд ${index + 1}">`;
        carouselInner.appendChild(slide);
    });

    // Обновление списка слайдов
    productSlides = document.querySelectorAll('.news-carousel-item');

    // Отображение модального окна
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';
    productSlideIndex = 0;
    showProductSlide(productSlideIndex);
}

// Закрытие модального окна продукта
function closeProductModal() {
    const modal = document.getElementById('productModal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Показ слайда в карусели продукта
function showProductSlide(index) {
    if (index >= productSlides.length) productSlideIndex = 0;
    if (index < 0) productSlideIndex = productSlides.length - 1;

    document.querySelector('.product-carousel-inner').style.transform = `translateX(-${productSlideIndex * 100}%)`;
    document.querySelector('.product-carousel-inner').style.display = 'flex';
}

// Следующий слайд в карусели продукта
function productNextSlide() {
    productSlideIndex++;
    showProductSlide(productSlideIndex);
}

// Предыдущий слайд в карусели продукта
function productPrevSlide() {
    productSlideIndex--;
    showProductSlide(productSlideIndex);
}

// Закрытие модального окна при клике вне его
window.addEventListener('click', function(event) {
    const modal = document.getElementById('productModal');
    if (event.target === modal) {
        closeProductModal();
    }
});

// Закрытие модального окна при нажатии на Escape
window.addEventListener('keydown', function(event) {
    const modal = document.getElementById('productModal');
    if (event.key === 'Escape' && modal && modal.style.display === 'block') {
        closeProductModal();
    }
});
