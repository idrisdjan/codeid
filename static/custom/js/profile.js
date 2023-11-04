const followBtn = document.querySelector('.btn-follow')
const followerBox = document.querySelector('.followers-box')

followBtn.addEventListener('click', event => {
	const userSlug = event.target.dataset.slug
	fetch(`/user/follow/${userSlug}/`, {
		method: 'POST',
		headers: {
			'X-CSRFToken': csrftoken,
			'X-Requested-With': 'XMLHttpRequest',
		},
	})
		.then(response => response.json())
		.then(data => {
			const isBtnPrimary = followBtn.classList.contains('btn-primary')
			const message = data.message || ''

			if (isBtnPrimary) {
				followBtn.classList.remove('btn-primary')
				followBtn.classList.add('btn-danger')
			} else {
				followBtn.classList.remove('btn-danger')
				followBtn.classList.add('btn-primary')
			}
			if (data.status) {
				followerBox.innerHTML += `
                <div class="col-md-2" id="user-slug-${data.slug}">
                    <a href="${data.get_absolute_url}">
                        <img src="${data.avatar}" class="img-fluid rounded-1" alt="${data.slug}"/>
                    </a>
                </div>
            `
			} else {
				const currentUserSlug = document.querySelector(
					`#user-slug-${data.slug}`
				)
				currentUserSlug && currentUserSlug.remove()
			}
			followBtn.innerHTML = message
		})
})
