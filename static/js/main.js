// Основные переменные
let currentOrderType = '';
let currentRentOption = null;
let maxSelectableGames = 0;

// Сброс формы
function resetForm() {
  const form = document.getElementById('orderForm');
  if (form) {
    form.reset();
    clearErrorMessages();
    const buySection = document.getElementById('buy-section');
    const rentSection = document.getElementById('rent-section');
    const summaryElement = document.getElementById('order-summary');
    const totalElement = document.getElementById('total-price');

    if (buySection) buySection.style.display = 'none';
    if (rentSection) rentSection.style.display = 'none';
    if (summaryElement) summaryElement.style.display = 'none';
    if (totalElement) totalElement.textContent = '0';

    currentOrderType = '';
    currentRentOption = null;
    maxSelectableGames = 0;
  }
}

// Очистка сообщений об ошибках
function clearErrorMessages() {
  document.querySelectorAll('.error-message').forEach(el => {
    el.style.display = 'none';
  });

  // Удаляем все toast уведомления
  const toastContainer = document.querySelector('.toast-container');
  if (toastContainer) {
    toastContainer.remove();
  }
}

// Показ ошибки
function showError(elementId, message) {
  // Создаем контейнер для toast уведомлений, если его нет
  let toastContainer = document.querySelector('.toast-container');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    document.body.appendChild(toastContainer);
  }

  // Создаем элемент toast
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.setAttribute('role', 'alert');
  toast.setAttribute('aria-live', 'assertive');
  toast.setAttribute('aria-atomic', 'true');

  // Создаем тело toast
  const toastBody = document.createElement('div');
  toastBody.className = 'toast-body';
  toastBody.textContent = message;

  // Собираем toast
  toast.appendChild(toastBody);

  // Добавляем toast в контейнер
  toastContainer.appendChild(toast);

  // Показываем toast
  const bootstrapToast = new bootstrap.Toast(toast, { delay: 3000 });
  bootstrapToast.show();

  // Прокручиваем к элементу, если он существует
  const element = document.getElementById(elementId);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
}

// Валидация телефона
function validatePhone(phone) {
  const phoneRegex = /^[\d\s\-()+]{10,}$/;
  return phoneRegex.test(phone);
}

// Переключение типа заказа
function toggleOrderType(type) {
  const buySection = document.getElementById('buy-section');
  const rentSection = document.getElementById('rent-section');

  if (!buySection || !rentSection) return;

  buySection.style.display = 'none';
  rentSection.style.display = 'none';

  if (type === 'buy' || type === 'double_buy') {
    buySection.style.display = 'block';
    currentOrderType = type;
  } else if (type === 'rent') {
    rentSection.style.display = 'block';
    currentOrderType = 'rent';
  }

  updateTotalPrice();
}

// Обновление ограничений для аренды
function updateRentLimits() {
  const select = document.getElementById('rent-options');
  if (!select) return;

  const option = select.options[select.selectedIndex];
  maxSelectableGames = option ? parseInt(option.dataset.gameCount) || 0 : 0;
  const isSpecificGame = option ? option.dataset.isSpecific === 'True' : false;
  const specificGameId = option ? option.dataset.specificGame : '';

  const gameCards = document.querySelectorAll('#rent-games-container .game-card-modal');

  gameCards.forEach(card => {
    if (isSpecificGame) {
      if (card.dataset.gameId === specificGameId) {
        card.style.display = 'block';
        const checkbox = card.querySelector('input[type="checkbox"]');
        if (checkbox) {
          checkbox.checked = true;
          checkbox.disabled = true;
        }
      } else {
        card.style.display = 'none';
        const checkbox = card.querySelector('input[type="checkbox"]');
        if (checkbox) {
          checkbox.checked = false;
          checkbox.disabled = true;
        }
      }
    } else {
      card.style.display = 'block';
      const checkbox = card.querySelector('input[type="checkbox"]');
      if (checkbox) {
        checkbox.disabled = false;
      }
    }
  });

  updateTotalPrice();
}

// Ограничение выбора игр при аренде
function limitGameSelection() {
  const select = document.getElementById('rent-options');
  if (!select) return;

  const option = select.options[select.selectedIndex];
  const isSpecificGame = option ? option.dataset.isSpecific === 'True' : false;

  if (isSpecificGame) {
    const checkedGames = document.querySelectorAll('#rent-games-container input[type="checkbox"]:checked');
    if (checkedGames.length > 1) {
      checkedGames.forEach((game, index) => {
        if (index > 0) {
          game.checked = false;
        }
      });
    }
  } else {
    const checkedGames = document.querySelectorAll('#rent-games-container input[type="checkbox"]:checked');
    if (checkedGames.length > maxSelectableGames) {
      checkedGames.forEach((game, index) => {
        if (index >= maxSelectableGames) {
          game.checked = false;
        }
      });
    }
  }

  updateTotalPrice();
}

// Ограничение выбора игр для покупки 2 игр на одной доске
function limitDoubleGameSelection() {
  if (currentOrderType !== 'double_buy') return;

  const checkedGames = document.querySelectorAll('#buy-games-container input[type="checkbox"]:checked');
  if (checkedGames.length > 2) {
    checkedGames.forEach((game, index) => {
      if (index >= 2) {
        game.checked = false;
      }
    });
  }

  updateTotalPrice();
}
// Обновление итоговой суммы
function updateTotalPrice() {
  const totalElement = document.getElementById('total-price');
  const summaryElement = document.getElementById('order-summary');

  if (!totalElement || !summaryElement) {
    console.error("Элемент итоговой суммы или элемент сводки не найден");
    return;
  }

  let total = 0;

  if (currentOrderType === 'buy' || currentOrderType === 'double_buy') {
    const selectedGames = document.querySelectorAll('#buy-games-container input[type="checkbox"]:checked');
    const selectedGoods = document.querySelectorAll('#additional-goods-container input[type="checkbox"]:checked');
    const doubleGameCountSelect = document.getElementById('double-game-count');

    selectedGames.forEach(game => {
      const price = parseFloat(game.dataset.price.replace(',', '.')) || 0;
      if (currentOrderType === 'double_buy' || (doubleGameCountSelect && doubleGameCountSelect.value === '2')) {
        total += price * 0.9 * 2; // Скидка 10% за покупку двух игр
      } else {
        total += price;
      }
    });

    selectedGoods.forEach(good => {
      const price = parseFloat(good.dataset.price.replace(',', '.')) || 0;
      total += price;
    });

    summaryElement.style.display = total > 0 ? 'block' : 'none';
  }
  else if (currentOrderType === 'rent') {
    const rentOption = document.getElementById('rent-options');
    if (rentOption && rentOption.value) {
      const option = rentOption.options[rentOption.selectedIndex];
      if (option) {
        total = parseFloat(option.dataset.price) || 0;
        summaryElement.style.display = 'block';
      } else {
        summaryElement.style.display = 'none';
      }
    } else {
      summaryElement.style.display = 'none';
    }
  } else {
    summaryElement.style.display = 'none';
  }

  totalElement.textContent = formatPrice(total);
  console.log("Итоговая сумма обновлена:", total);
}

// Отправка формы
function submitOrder(event) {
  event.preventDefault();
  clearErrorMessages();
  let isValid = true;

  // Валидация основных полей
  const name = document.getElementById('name');
  if (!name.value.trim()) {
    showError('name-error', 'Пожалуйста, введите ваше имя');
    isValid = false;
  }

  const phone = document.getElementById('phone');
  if (!phone.value.trim() || !validatePhone(phone.value)) {
    showError('phone-error', 'Пожалуйста, введите корректный номер телефона');
    isValid = false;
  }

  const orderType = document.getElementById('order-type');
  if (!orderType.value) {
    showError('order-type-error', 'Пожалуйста, выберите тип заказа');
    isValid = false;
  }

  // Валидация только для выбранного типа заказа
  if (orderType.value === 'buy') {
    const selectedGames = document.querySelectorAll('#buy-games-container input[type="checkbox"]:checked');
    const selectedGoods = document.querySelectorAll('#additional-goods-container input[type="checkbox"]:checked');

    // Проверка на наличие хотя бы одного выбранного товара (игры или дополнительного товара)
    if (selectedGames.length === 0 && selectedGoods.length === 0) {
      showError('form-error', 'Пожалуйста, выберите хотя бы одну игру или дополнительный товар для покупки');
      isValid = false;
    }

    const address = document.getElementById('delivery-address');
    if (!address.value.trim()) {
      showError('address-error', 'Пожалуйста, введите адрес доставки');
      isValid = false;
    }
  }
  else if (orderType.value === 'double_buy') {
    const selectedGames = document.querySelectorAll('#buy-games-container input[type="checkbox"]:checked');
    const selectedGoods = document.querySelectorAll('#additional-goods-container input[type="checkbox"]:checked');

    // Проверка на наличие ровно двух выбранных игр
    if (selectedGames.length !== 2) {
      showError('form-error', 'Пожалуйста, выберите ровно 2 игры для покупки на одной доске');
      isValid = false;
    }

    const address = document.getElementById('delivery-address');
    if (!address.value.trim()) {
      showError('address-error', 'Пожалуйста, введите адрес доставки');
      isValid = false;
    }
  }
  else if (orderType.value === 'rent') {
    const rentOption = document.getElementById('rent-options');
    if (!rentOption.value) {
      showError('rent-options-error', 'Пожалуйста, выберите тип аренды');
      isValid = false;
    }

    const selectedGames = document.querySelectorAll('#rent-games-container input[type="checkbox"]:checked');
    if (selectedGames.length === 0) {
      showError('form-error', 'Пожалуйста, выберите хотя бы одну игру для аренды');
      isValid = false;
    }
    else if (selectedGames.length !== maxSelectableGames) {
      showError('form-error', `Вы выбрали ${selectedGames.length} игру(ы), но ваш тип аренды требует выбрать ровно ${maxSelectableGames} игру(ы).`);
      isValid = false;
    }

    const date = document.getElementById('rent-date');
    if (!date.value) {
      showError('date-error', 'Пожалуйста, выберите дату аренды');
      isValid = false;
    }

    const address = document.getElementById('rent-address');
    if (!address.value.trim()) {
      showError('rent-address-error', 'Пожалуйста, введите адрес доставки');
      isValid = false;
    }
  }

  if (!isValid) {
    return false;
  }

  submitFormData();
  return false;
}

// Отправка данных формы на сервер
function submitFormData() {
  const form = document.getElementById('orderForm');
  const formData = new FormData(form);
  const submitBtn = document.getElementById('submit-btn');

  // Добавляем выбранные игры в зависимости от типа заказа
  if (currentOrderType === 'buy' || currentOrderType === 'double_buy') {
    const selectedGames = document.querySelectorAll('#buy-games-container input[type="checkbox"]:checked');
    selectedGames.forEach(game => {
      formData.append('buy_games', game.value);
    });

    const selectedGoods = document.querySelectorAll('#additional-goods-container input[type="checkbox"]:checked');
    selectedGoods.forEach(good => {
      formData.append('additional_goods', good.value);
    });
  }
  else if (currentOrderType === 'rent') {
    const selectedGames = document.querySelectorAll('#rent-games-container input[type="checkbox"]:checked');
    selectedGames.forEach(game => {
      formData.append('rent_games', game.value);
    });
  }

  submitBtn.disabled = true;
  submitBtn.textContent = 'Отправка...';

  fetch(form.action, {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
      'X-Requested-With': 'XMLHttpRequest'
    }
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    if (data.success) {
      // Показываем модальное окно поздравления
      const successModal = document.getElementById('successModal');
      if (successModal) {
        successModal.style.display = 'block';
      }

      // Закрываем основное модальное окно
      closeModal();
    } else {
      showError('form-error', data.message || 'Произошла ошибка при оформлении заказа');
    }
  })
  .catch(error => {
    console.error('Error:', error);
    showError('form-error', 'Произошла ошибка при отправке заказа. Пожалуйста, попробуйте позже.');
  })
  .finally(() => {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Оформить заказ';
  });
}

// Функция для закрытия модального окна поздравления
window.closeSuccessModal = function() {
  const successModal = document.getElementById('successModal');
  if (successModal) {
    successModal.style.display = 'none';
  }
};

// Функция для форматирования цены
function formatPrice(price) {
  return parseFloat(price).toFixed(2).replace('.', ',');
}

// Инициализация формы при загрузке
document.addEventListener('DOMContentLoaded', function() {
  const modal = document.getElementById('orderModal');

  window.closeModal = function() {
    if (modal) {
      modal.style.display = 'none';
      document.body.style.overflow = 'auto';
      resetForm();
    }
  };

  window.openOrderModal = function() {
  if (modal) {
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';
    const summaryElement = document.getElementById('order-summary');
    if (summaryElement) {
      summaryElement.style.display = 'none';
    }
    updateTotalPrice();
  }
};

  window.addEventListener('click', function(event) {
    if (event.target === modal) {
      closeModal();
    }
  });

  window.addEventListener('keydown', function(event) {
    if (event.key === 'Escape' && modal && modal.style.display === 'block') {
      closeModal();
    }
  });

  const buyGamesContainer = document.getElementById('buy-games-container');
  if (buyGamesContainer) {
    buyGamesContainer.addEventListener('change', function(e) {
      if (e.target.type === 'checkbox') {
        limitDoubleGameSelection();
        updateTotalPrice();
      }
    });
  }

  const additionalGoodsContainer = document.getElementById('additional-goods-container');
  if (additionalGoodsContainer) {
    additionalGoodsContainer.addEventListener('change', function(e) {
      if (e.target.type === 'checkbox') {
        updateTotalPrice();
      }
    });
  }

  const rentGamesContainer = document.getElementById('rent-games-container');
  if (rentGamesContainer) {
    rentGamesContainer.addEventListener('change', function(e) {
      if (e.target.type === 'checkbox') {
        limitGameSelection.call(e.target);
      }
    });
  }

  const form = document.getElementById('orderForm');
  if (form) {
    form.addEventListener('change', function() {
      updateTotalPrice();
    });
  }

  const dateInput = document.getElementById('rent-date');
  if (dateInput) {
    const today = new Date();
    const minDate = new Date();
    minDate.setDate(today.getDate() + 1);
    dateInput.min = minDate.toISOString().split('T')[0];

    const defaultDate = new Date();
    defaultDate.setDate(today.getDate() + 1);
    dateInput.value = defaultDate.toISOString().split('T')[0];
  }

  // Удаляем обработчики invalid, так как валидация теперь полностью через JavaScript
  const rentDateInput = document.getElementById('rent-date');
  if (rentDateInput) {
    rentDateInput.removeAttribute('required');
  }

  const rentOptionsSelect = document.getElementById('rent-options');
  if (rentOptionsSelect) {
    rentOptionsSelect.removeAttribute('required');
  }

  const rentAddressInput = document.getElementById('rent-address');
  if (rentAddressInput) {
    rentAddressInput.removeAttribute('required');
  }

  const deliveryAddressInput = document.getElementById('delivery-address');
  if (deliveryAddressInput) {
    deliveryAddressInput.removeAttribute('required');
  }
});

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

// Бургер-меню функциональность
document.addEventListener('DOMContentLoaded', function() {
  // Навигационное меню
  const burgerMenuNav = document.getElementById('burgerMenuNav');
  const mobileMenuNav = document.getElementById('mobileMenuNav');

  if (burgerMenuNav && mobileMenuNav) {
    burgerMenuNav.addEventListener('click', function() {
      this.classList.toggle('toggle');
      mobileMenuNav.classList.toggle('active');
    });
  }

  // Меню в подвале
  const burgerMenuFooter = document.getElementById('burgerMenuFooter');
  const mobileMenuFooter = document.getElementById('mobileMenuFooter');

  if (burgerMenuFooter && mobileMenuFooter) {
    burgerMenuFooter.addEventListener('click', function() {
      this.classList.toggle('toggle');
      mobileMenuFooter.classList.toggle('active');
    });
  }
});
