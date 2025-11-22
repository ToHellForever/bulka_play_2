  document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('orderModal');
    const closeBtn = document.querySelector('.close');

    // Функция для открытия модального окна
    window.openOrderModal = function() {
      if (modal) {
        modal.style.display = 'block';
      }
    };

    // Закрытие модального окна
    if (closeBtn) {
      closeBtn.onclick = function() {
        if (modal) {
          modal.style.display = 'none';
        }
      };
    }

    // Закрытие модального окна при клике вне его
    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = 'none';
      }
    };

    // Функция для отображения блоков информации
    window.showInfo = function(id) {
      const selectedBlock = document.getElementById(id);
      if (selectedBlock) {
        if (selectedBlock.style.display === 'block') {
          selectedBlock.style.display = 'none';
        } else {
          // Hide all info blocks
          const infoBlocks = document.querySelectorAll('.info-block');
          infoBlocks.forEach(block => {
            block.style.display = 'none';
          });

          // Show the selected info block
          selectedBlock.style.display = 'block';
        }
      }
    };

    // Обработчики для кнопок с классом .button
    const buttons = document.querySelectorAll(".button");
    if (buttons.length > 0) {
      buttons.forEach(button => {
        const img = button.querySelector(".arrow_accorderon");
        if (img) {
          button.addEventListener("click", () => {
            img.classList.toggle("active");
          });
        }
      });
    }
  });
