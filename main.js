// Live category prediction while the user types the expense description.
document.addEventListener('DOMContentLoaded', function () {
    const descriptionInput = document.getElementById('id_description');
    const categorySelect = document.getElementById('id_category');
    const predictedBadge = document.getElementById('predicted-badge');

    if (!descriptionInput || !categorySelect) {
        return;
    }

    let debounceTimer;
    let userChangedCategory = false;

    categorySelect.addEventListener('change', function () {
        userChangedCategory = true;
    });

    descriptionInput.addEventListener('input', function () {
        clearTimeout(debounceTimer);
        const text = descriptionInput.value.trim();

        if (!text) {
            if (predictedBadge) predictedBadge.classList.add('d-none');
            return;
        }

        debounceTimer = setTimeout(function () {
            fetch(`/predict-category/?description=${encodeURIComponent(text)}`)
                .then((res) => res.json())
                .then((data) => {
                    if (data.category) {
                        if (!userChangedCategory) {
                            categorySelect.value = data.category;
                        }
                        if (predictedBadge) {
                            predictedBadge.textContent = 'Predicted: ' + data.category;
                            predictedBadge.classList.remove('d-none');
                        }
                    }
                })
                .catch(() => {});
        }, 400);
    });
});

// Confirm before deleting an expense (extra client-side safety net).
document.addEventListener('DOMContentLoaded', function () {
    const deleteForms = document.querySelectorAll('.delete-confirm-form');
    deleteForms.forEach(function (form) {
        form.addEventListener('submit', function (event) {
            const confirmed = window.confirm('Are you sure you want to delete this expense?');
            if (!confirmed) {
                event.preventDefault();
            }
        });
    });
});
