document.addEventListener('DOMContentLoaded', function() {
    const guestInput = document.getElementById("guestInput");
    const guestSlider = document.getElementById("guestSlider");
    const guestMinCount = document.getElementById("guestMinCount");
    const guestMaxCount = document.getElementById("guestMaxCount");

    function updateRecommendedGames(guests) {
        fetch('/calculate_games/?guests=' + guests)
            .then(response => response.json())
            .then(data => {
                guestMinCount.textContent = `${data.min} `;
                guestMaxCount.textContent = ` ${data.max}`;
            })
            .catch(error => console.error('Ошибка:', error));
    };

    // Ограничиваем минимальное значение двумя гостями
    guestInput.addEventListener("change", () => {
        let newValue = Math.max(parseInt(guestInput.value), 2); // Минимум - 2 человека
        guestInput.value = newValue;
        guestSlider.value = newValue;
        updateRecommendedGames(newValue); // Отправляем запрос и обновляем рекомендации
    });

    // То же самое делаем для слайдера
    guestSlider.addEventListener("input", () => {
        let newValue = Math.max(parseInt(guestSlider.value), 2); // Минимум - 2 человека
        guestInput.value = newValue;
        guestSlider.value = newValue;
        updateRecommendedGames(newValue); // Отправляем запрос и обновляем рекомендации
    });

    guestSlider.addEventListener("input", () => {
        const value = (guestSlider.value - guestSlider.min) / (guestSlider.max - guestSlider.min) * 100;
        guestSlider.style.setProperty('--value', `${value}%`);
    });
});