  document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('orderModal');
    const closeBtn = document.querySelector('.close');

    // Функция для открытия модального окна
    window.openOrderModal = function() {
      modal.style.display = 'block';
    };

    // Закрытие модального окна
    if (closeBtn) {
      closeBtn.onclick = function() {
        modal.style.display = 'none';
      };
    }

    // Закрытие модального окна при клике вне его
    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = 'none';
      }
    };
  });