// Управление модальным окном новостей
let newsSlideIndex = 0;
let newsSlides = [];

// Открытие модального окна новостей
function openNewsModal(images) {
    const modal = document.getElementById('newsModal');
    const carouselInner = document.querySelector('.news-carousel-inner');

    // Очистка предыдущих слайдов
    carouselInner.innerHTML = '';

    // Добавление новых слайдов
    images.forEach((image, index) => {
        const slide = document.createElement('div');
        slide.className = 'news-carousel-item';
        slide.innerHTML = `<img src="${image}" alt="Слайд ${index + 1}">`;
        carouselInner.appendChild(slide);
    });

    // Обновление списка слайдов
    newsSlides = document.querySelectorAll('.news-carousel-item');

    // Отображение модального окна
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';
    newsSlideIndex = 0;
    showNewsSlide(newsSlideIndex);
}

// Закрытие модального окна новостей
function closeNewsModal() {
    const modal = document.getElementById('newsModal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Показ слайда в карусели новостей
function showNewsSlide(index) {
    if (index >= newsSlides.length) newsSlideIndex = 0;
    if (index < 0) newsSlideIndex = newsSlides.length - 1;

    document.querySelector('.news-carousel-inner').style.transform = `translateX(-${newsSlideIndex * 100}%)`;
}

// Следующий слайд в карусели новостей
function newsNextSlide() {
    newsSlideIndex++;
    showNewsSlide(newsSlideIndex);
}

// Предыдущий слайд в карусели новостей
function newsPrevSlide() {
    newsSlideIndex--;
    showNewsSlide(newsSlideIndex);
}

// Закрытие модального окна при клике вне его
window.addEventListener('click', function(event) {
    const modal = document.getElementById('newsModal');
    if (event.target === modal) {
        closeNewsModal();
    }
});

// Закрытие модального окна при нажатии на Escape
window.addEventListener('keydown', function(event) {
    const modal = document.getElementById('newsModal');
    if (event.key === 'Escape' && modal && modal.style.display === 'block') {
        closeNewsModal();
    }
});

// Обработка кликов по кнопкам "ПОДРОБНЕЕ"
document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.news-card-button');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const newsId = this.getAttribute('data-news-id');
            // Получаем все изображения для новости
            const images = [];
            const newsItem = document.querySelector(`.news-card[data-news-id="${newsId}"]`);
            if (newsItem) {
                // Основное изображение новости
                const mainImage = newsItem.querySelector('.news_card_image');
                if (mainImage) {
                    images.push(mainImage.src);
                }
                // Дополнительные изображения новости
                const additionalImages = newsItem.querySelectorAll('.additional_news_image');
                additionalImages.forEach(img => {
                    images.push(img.src);
                });
            }
            openNewsModal(images);
        });
    });

    // Закрытие модального окна при клике на крестик
    document.querySelector('.news-close').addEventListener('click', closeNewsModal);
});
