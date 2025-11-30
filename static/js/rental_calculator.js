document.addEventListener('DOMContentLoaded', function() {
    const guestInput = document.getElementById("guestInput");
    const guestSlider = document.getElementById("guestSlider");
    const guestMinCount = document.getElementById("guestMinCount");
    const guestMaxCount = document.getElementById("guestMaxCount");

    function updateRecommendedGames(guests) {
        if (guests < 2) {
            guestMinCount.textContent = '';
            guestMaxCount.textContent = '';
            document.getElementById("gamesLabel").textContent = '';
            return;
        }
        fetch('/calculate_games/?guests=' + guests)
            .then(response => response.json())
            .then(data => {
                guestMinCount.textContent = `${data.min} `;
                guestMaxCount.textContent = ` ${data.max}`;
                document.getElementById("gamesLabel").textContent = 'игр';
            })
            .catch(error => console.error('Ошибка:', error));
    };

    // Обработка изменения слайдера
    guestSlider.addEventListener("input", () => {
        let newValue = Math.max(parseInt(guestSlider.value), 2); // Минимум - 2 человека
        const guestValueDisplay = document.getElementById("guestValueDisplay");
        guestValueDisplay.style.display = "block";
        guestValueDisplay.innerHTML = newValue + ' <span id="guestUnit">чел</span>';
        updateRecommendedGames(newValue); // Отправляем запрос и обновляем рекомендации
        const value = (guestSlider.value - guestSlider.min) / (guestSlider.max - guestSlider.min) * 100;
        guestSlider.style.setProperty('--value', `${value}%`);
    });
});
