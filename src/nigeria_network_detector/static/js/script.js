document.addEventListener('DOMContentLoaded', function() {
    const phoneInput = document.getElementById('phone-input');
    const detectBtn = document.getElementById('detect-btn');
    const resultSection = document.getElementById('result-section');
    const networkName = document.getElementById('network-name');
    const networkMessage = document.getElementById('network-message');
    const cleanedNumber = document.getElementById('cleaned-number');
    const networkIcon = document.getElementById('network-icon');
    // Event listeners
    detectBtn.addEventListener('click', detectNetwork);
    phoneInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            detectNetwork();
        }
    });

    // Auto-format phone number as user types
    phoneInput.addEventListener('input', function() {
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

        // Show loading state
        detectBtn.disabled = true;
        detectBtn.textContent = 'Checking...';
        resultSection.classList.add('hidden');

        try {
            const response = await fetch('/api/detect', {
                method: 'POST', 
                headers: {
                    'Content-Type': 'application/json', 
                }, 
                body: JSON.stringify({ phone_number: phoneNumber })
            });

            const data = await response.json();

            if (data.success) {
                showResult(data);
            } else {
                showError(data.error);
            }
        } catch (error) {
            showError('Network error: ' + error.message);
        } finally {
            detectBtn.disabled = false;
            detectBtn.textContent = 'Detect';
        }
    }

    function showResult(data) {
        resultSection.classList.remove('hidden');
        
        // Set network name and message
        networkName.textContent = data.network;
        
        // Format cleaned number for display
        const formattedNumber = data.cleaned_number.replace(/(\d{4})(\d{3})(\d{4})/, '$1 $2 $3');
        cleanedNumber.textContent = formattedNumber;
        
        // Set network-specific styling and message
        const networkDescriptions = {
            'MTN': 'Largest network in Nigeria', 
            'Glo': 'Affordable data provider', 
            'Airtel': 'Quality network provider', 
            '9mobile': 'Former Etisalat network', 
            'Ntel': '4G LTE provider', 
            'Smile': '4G broadband services'
        };

        const description = networkDescriptions[data.network] || 'Network provider';
        
        networkIcon.dataset.network = data.network;
        networkIcon.textContent = data.network === 'Glo' ? 'glo' : data.network;
        networkMessage.textContent = description;
    }

    function showError(message) {
        // Remove any existing error
        const existingError = document.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }

        networkName.textContent = 'Could not detect';
        networkMessage.textContent = message;
        cleanedNumber.textContent = '';
        networkIcon.dataset.network = 'error';
        networkIcon.textContent = '!';
        resultSection.classList.remove('hidden');
    }
});
