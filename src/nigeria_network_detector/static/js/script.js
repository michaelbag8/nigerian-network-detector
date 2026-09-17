document.addEventListener('DOMContentLoaded', () => {
    const phoneInput = document.getElementById('phone-input');
    const detectBtn = document.getElementById('detect-btn');
    const resultSection = document.getElementById('result-section');
    const resultCard = document.getElementById('result-card');
    const networkName = document.getElementById('network-name');
    const networkMessage = document.getElementById('network-message');
    const cleanedNumber = document.getElementById('cleaned-number');
    const networkIcon = document.getElementById('network-icon');
    const networkList = document.getElementById('network-list');
    const networkCountBadge = document.getElementById('network-count-badge');

    // Populated once from /api/networks so colors/descriptions/prefixes
    // live in one place (the backend) instead of being duplicated here.
    let networksCache = {};

    loadNetworks();

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
        detectBtn.querySelector('.btn-label').textContent = 'Detecting…';

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
            detectBtn.querySelector('.btn-label').textContent = 'Detect';
        }
    }

    function showResult(data) {
        resultSection.classList.remove('hidden');
        resultCard.classList.remove('is-error');

        const info = networksCache[data.network];
        const color = info ? info.color : '#5c6b5f';
        const description = info ? info.description : 'Not currently mapped to a known carrier';

        networkName.textContent = data.network;
        networkMessage.textContent = description;

        networkIcon.style.setProperty('background', color);
        networkIcon.textContent = data.network.charAt(0);

        cleanedNumber.textContent = formatForDisplay(data.cleaned_number);
    }

    function showError(message) {
        resultSection.classList.remove('hidden');
        resultCard.classList.add('is-error');

        networkIcon.style.setProperty('background', 'transparent');
        networkIcon.textContent = '!';
        networkName.textContent = 'Could not detect network';
        networkMessage.textContent = message;
        cleanedNumber.textContent = '—';
    }

    async function loadNetworks() {
        try {
            const response = await fetch('/api/networks');
            const data = await response.json();

            if (!data.success) {
                return;
            }

            networksCache = data.networks;
            const names = Object.keys(networksCache);
            networkCountBadge.textContent = `${names.length} networks supported`;

            networkList.innerHTML = '';
            for (const [network, info] of Object.entries(networksCache)) {
                const item = document.createElement('div');
                item.className = 'network-item';
                item.style.setProperty('--item-color', info.color);
                item.innerHTML = `
                    <div class="name">${network}</div>
                    <div class="desc">${info.description}</div>
                    <div class="prefixes">${info.prefixes.slice(0, 3).join(', ')}&hellip;</div>
                `;
                networkList.appendChild(item);
            }
        } catch (error) {
            console.error('Failed to load network list:', error);
        }
    }

    function formatForDisplay(cleaned) {
        if (!cleaned || cleaned.length !== 11) {
            return cleaned || '—';
        }
        return cleaned.replace(/(\d{4})(\d{3})(\d{4})/, '$1 $2 $3');
    }
});
