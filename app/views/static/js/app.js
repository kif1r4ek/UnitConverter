document.addEventListener('DOMContentLoaded', function() {
    console.log('🔄 App.js loaded!'); // Проверка загрузки
    
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const navTabs = document.querySelector('.nav-tabs');
    
    console.log('🔍 Mobile toggle found:', mobileMenuToggle); // Debug
    console.log('🔍 Nav tabs found:', navTabs); // Debug
    
    if (mobileMenuToggle && navTabs) {
        mobileMenuToggle.addEventListener('click', function(e) {
            e.stopPropagation(); // Предотвращаем всплытие события
            navTabs.classList.toggle('show');
            console.log('📱 Menu toggled!', navTabs.classList.contains('show')); // Debug
        });

        document.addEventListener('click', function(event) {
            if (!event.target.closest('.navbar')) {
                navTabs.classList.remove('show');
            }
        });
    } else {
        console.error('❌ Mobile menu elements not found!');
    }
});

class UnitConverter {
    constructor() {
        this.initEventListeners();
        this.loadHistory();
    }

    initEventListeners() {
        // Будем добавлять обработчики событий для форм
        const convertBtn = document.getElementById('convertBtn');
        const swapBtn = document.getElementById('swapBtn');
        
        if (convertBtn) {
            convertBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.convert();
            });
        }
        
        if (swapBtn) {
            swapBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.swapUnits();
            });
        }
    }

    convert() {
        console.log('Convert function - will be implemented');
        // Здесь будет логика конвертации
    }

    swapUnits() {
        const fromSelect = document.getElementById('fromUnit');
        const toSelect = document.getElementById('toUnit');
        
        if (fromSelect && toSelect) {
            const temp = fromSelect.value;
            fromSelect.value = toSelect.value;
            toSelect.value = temp;

            const inputValue = document.getElementById('inputValue');
            if (inputValue && inputValue.value) {
                this.convert();
            }
        }
    }

    saveToHistory(conversion) {
        let history = this.getHistory();

        history.unshift({
            ...conversion,
            timestamp: new Date().toISOString()
        });

        history = history.slice(0, 5);

        localStorage.setItem('conversionHistory', JSON.stringify(history));

        this.displayHistory();
    }

    getHistory() {
        const history = localStorage.getItem('conversionHistory');
        return history ? JSON.parse(history) : [];
    }

    loadHistory() {
        this.displayHistory();
    }

    displayHistory() {
        const historyList = document.getElementById('historyList');
        if (!historyList) return;
        
        const history = this.getHistory();
        
        if (history.length === 0) {
            historyList.innerHTML = '<div class="history-empty">No conversion history yet</div>';
            return;
        }
        
        historyList.innerHTML = history.map(item => `
            <div class="history-item">
                <span>
                    <strong>${item.value} ${item.fromUnit}</strong> 
                    → ${item.result} ${item.toUnit}
                </span>
                <small class="text-muted">${this.formatDate(item.timestamp)}</small>
            </div>
        `).join('');
    }

    formatDate(isoString) {
        const date = new Date(isoString);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        
        if (diffMins < 1) return 'Just now';
        if (diffMins < 60) return `${diffMins}m ago`;
        if (diffMins < 1440) return `${Math.floor(diffMins / 60)}h ago`;
        return date.toLocaleDateString();
    }

    clearHistory() {
        localStorage.removeItem('conversionHistory');
        this.displayHistory();
    }
}

let converter;
document.addEventListener('DOMContentLoaded', function() {
    converter = new UnitConverter();
});

function formatNumber(num, decimals = 4) {
    return parseFloat(num.toFixed(decimals));
}

function isValidNumber(value) {
    return !isNaN(value) && value !== '' && isFinite(value);
}