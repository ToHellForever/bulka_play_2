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
}

// Показ ошибки
function showError(elementId, message) {
  const errorElement = document.getElementById(elementId);
  if (errorElement) {
    errorElement.textContent = message;
    errorElement.style.display = 'block';
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

  if (type === 'buy') {
    buySection.style.display = 'block';
    currentOrderType = 'buy';
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

  const checkedGames = document.querySelectorAll('#rent-games-container input[type="checkbox"]:checked');
  if (checkedGames.length > maxSelectableGames) {
    checkedGames.forEach((game, index) => {
      if (index >= maxSelectableGames) {
        game.checked = false;
      }
    });
  }

  updateTotalPrice();
}

// Ограничение выбора игр при аренде
function limitGameSelection() {
  const checkedGames = document.querySelectorAll('#rent-games-container input[type="checkbox"]:checked');
  if (checkedGames.length > maxSelectableGames) {
    alert(`Вы можете выбрать не более ${maxSelectableGames} игр для этого типа аренды`);
    this.checked = false;
  }
  updateTotalPrice();
}

// Обновление итоговой суммы
function updateTotalPrice() {
  const totalElement = document.getElementById('total-price');
  const summaryElement = document.getElementById('order-summary');

  if (!totalElement || !summaryElement) return;

  let total = 0;

  if (currentOrderType === 'buy') {
    const selectedGames = document.querySelectorAll('#buy-games-container input[type="checkbox"]:checked');
    const selectedGoods = document.querySelectorAll('#additional-goods-container input[type="checkbox"]:checked');

    selectedGames.forEach(game => {
      total += parseFloat(game.dataset.price) || 0;
    });

    selectedGoods.forEach(good => {
      total += parseFloat(good.dataset.price) || 0;
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

  totalElement.textContent = total.toFixed(2);
}

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
    if (selectedGames.length === 0) {
      showError('form-error', 'Пожалуйста, выберите хотя бы одну игру для покупки');
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
    else if (selectedGames.length > maxSelectableGames) {
      showError('form-error', `Вы можете выбрать не более ${maxSelectableGames} игр для этого типа аренды`);
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
    const firstError = document.querySelector('.error-message[style="display: block;"]');
    if (firstError) {
      firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    return false;
  }

  submitFormData();
  return false;
}

function submitFormData() {
  const form = document.getElementById('orderForm');
  const formData = new FormData(form);
  const submitBtn = document.getElementById('submit-btn');

  // Добавляем выбранные игры в зависимости от типа заказа
  if (currentOrderType === 'buy') {
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
      alert('Ваш заказ успешно оформлен! Мы свяжемся с вами в ближайшее время.');
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
    if (selectedGames.length === 0) {
      showError('form-error', 'Пожалуйста, выберите хотя бы одну игру для покупки');
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
    else if (selectedGames.length > maxSelectableGames) {
      showError('form-error', `Вы можете выбрать не более ${maxSelectableGames} игр для этого типа аренды`);
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
    const firstError = document.querySelector('.error-message[style="display: block;"]');
    if (firstError) {
      firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
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
  if (currentOrderType === 'buy') {
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
      alert('Ваш заказ успешно оформлен! Мы свяжемся с вами в ближайшее время.');
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
