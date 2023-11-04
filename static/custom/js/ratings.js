const ratingButtons = document.querySelectorAll('.rating-buttons')

ratingButtons.forEach(button => {
	button.addEventListener('click', event => {
		// Получаем значение рейтинга из data-атрибута кнопки
		const value = parseInt(event.target.dataset.value)
		const articleId = parseInt(event.target.dataset.article)
		const ratingSum = button.querySelector('.rating-sum')
		// Создаем объект FormData для отправки данных на сервер
		const formData = new FormData()
		// Добавляем id статьи, значение кнопки
		formData.append('article_id', articleId)
		formData.append('value', value)
		// Отправляем AJAX-Запрос на сервер
		fetch('/rating/', {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrftoken,
				'X-Requested-With': 'XMLHttpRequest',
			},
			body: formData,
		})
			.then(response => response.json())
			.then(data => {
				// Обновляем значение на кнопке
				ratingSum.textContent = data.rating_sum
			})
			.catch(error => console.error(error))
	})
})
