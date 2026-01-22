import { validateConversionInput } from '../core/Validator.js';
import { ConverterService } from '../core/ConverterService.js';
import { HistoryService } from '../core/HistoryService.js';
import { formatRelativeDate } from '../utils/date.js';

export class UnitConverterUI {
    constructor(type) {
        this.type = type;
        this.service = new ConverterService(type);
        this.history = new HistoryService(type);

        this.cacheElements();
        this.bindEvents();

        this.loadHistory();
    }

    cacheElements() {
        this.form = document.querySelector(`#${this.type}Form`);
        this.input = document.getElementById('inputValue');
        this.from = document.getElementById('fromUnit');
        this.to = document.getElementById('toUnit');
        this.result = document.getElementById('resultValue');
        this.swapBtn = document.getElementById('swapBtn');
        this.historyList = document.getElementById('historyList');
        this.clearHistoryBtn = document.getElementById('clearHistory');
    }

    bindEvents() {
        if (!this.form) return;

        this.form.addEventListener('submit', e => this.submit(e));
        this.swapBtn?.addEventListener('click', e => this.swap(e));
        this.clearHistoryBtn?.addEventListener('click', e => this.clearHistory(e));
    }

    async submit(e) {
        e.preventDefault();

        try {
            const value = parseFloat(this.input.value);
            validateConversionInput(value, this.type);

            const data = {
                value,
                from_unit: this.from.value,
                to_unit: this.to.value,
            };

            const result = await this.service.convert(data);
            this.showResult(result.result);

            await this.loadHistory();

        } catch (err) {
            this.showError(err.message);
        }
    }

    async loadHistory() {
        if (!this.historyList) return;

        try {
            const history = await this.history.fetchHistory();
            this.renderHistory(history);
        } catch (error) {
            console.error('Failed to load history:', error);
        }
    }

    async clearHistory(e) {
        e?.preventDefault();

        if (!confirm('Are you sure you want to clear all history?')) {
            return;
        }

        const success = await this.history.clearHistory();

        if (success) {
            this.renderHistory([]);
        }
    }

    showResult(value) {
        this.result.value = value;
        this.result.classList.add('is-valid');
        this.result.classList.remove('is-invalid');
    }

    showError(msg) {
        this.result.value = '';
        this.result.placeholder = msg;
        this.result.classList.add('is-invalid');
        alert(msg);
    }

    swap(e) {
        e.preventDefault();

        if (!this.from || !this.to) return;

        const temp = this.from.value;
        this.from.value = this.to.value;
        this.to.value = temp;

        if (this.result) {
            this.result.value = '';
            this.result.classList.remove('is-valid', 'is-invalid');
        }
    }

    renderHistory(history) {
        if (!this.historyList) return;

        if (!history.length) {
            this.historyList.innerHTML = '<div class="history-empty">No conversion history yet</div>';
            return;
        }

        this.historyList.innerHTML = history.map(h => `
            <div class="history-item">
                <div>
                    <strong>${h.value} ${h.from_unit}</strong>
                    → <strong>${h.result} ${h.to_unit}</strong>
                </div>
                <small class="text-muted">${h.created_at_human}</small>
            </div>
        `).join('');
    }
}
