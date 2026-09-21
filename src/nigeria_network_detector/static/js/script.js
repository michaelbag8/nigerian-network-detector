document.addEventListener('DOMContentLoaded', () => {
    const phoneInput = document.getElementById('phone-input');
    const detectBtn = document.getElementById('detect-btn');
    const resultSection = document.getElementById('result-section');
    const resultCard = document.getElementById('result-card');
    const networkName = document.getElementById('network-name');
    const networkMessage = document.getElementById('network-message');
    const cleanedNumber = document.getElementById('cleaned-number');
    const networkIcon = document.getElementById('network-icon');
    let networksCache = {};

    // Event listeners
    detectBtn.addEventListener('click', detectNetwork);
    phoneInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            detectNetwork();
        }
    });

    // Auto-format as the user types: group digits into 4-3-4.
    phoneInput.addEventListener('input', () => {
        let value = phoneInput.value.replace(/\D/g, '');
        if (value.length >= 4) {
            value = value.replace(/(\d{4})(?=\d)/g, '$1 ');
        }
        phoneInput.value = value;
    });

    async function detectNetwork() {
        const phoneNumber = phoneInput.value.trim();

        if (!phoneNumber) {
            showError('Please enter a phone number');
            return;
        }

        detectBtn.disabled = true;
        detectBtn.textContent = 'Detecting...';
        resultSection.classList.add('hidden');

        try {
            const response = await fetch('/api/detect', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ phone_number: phoneNumber }),
            });

            const data = await response.json();

            if (data.success) {
                showResult(data);
            } else {
                showError(data.error);
            }
        } catch (error) {
            showError(`Network error: ${error.message}`);
        } finally {
            detectBtn.disabled = false;
            detectBtn.textContent = 'Detect Network';
        }
    }

    function showResult(data) {
        resultSection.classList.remove('hidden');
        resultCard.classList.remove('is-error');

        const info = networksCache[data.network];

        networkName.textContent = data.network;
        
        // Format cleaned number for display
        const formattedNumber = data.cleaned_number.replace(/(\d{4})(\d{3})(\d{4})/, '$1 $2 $3');
        cleanedNumber.textContent = formattedNumber;
        
        // Use the provider metadata returned by the API for consistent styling.
        const color = info ? info.color : '#5c6b5f';
        const description = info ? info.description : 'Network provider';
        
        networkIcon.style.backgroundColor = color;
        networkIcon.textContent = data.network.charAt(0);
        networkMessage.textContent = description;
    }

    function showError(message) {
        // Remove any existing error
        const existingError = document.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        
        resultSection.parentNode.insertBefore(errorDiv, resultSection);
        resultSection.classList.add('hidden');
    }

});
