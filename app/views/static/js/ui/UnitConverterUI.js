import { validateConversionInput } from '../core/Validator.js';
import { ConverterService } from '../core/ConverterService.js';
import { HistoryStorage } from '../core/HistoryStorage.js';
import { formatRelativeDate } from '../utils/date.js';

export class UnitConverterUI {
    constructor(type) {
        this.type = type;
        this.service = new ConverterService(type);
        this.history = new HistoryStorage(`${type}_history`);

        this.cacheElements();
        this.bindEvents();

        this.cleanupHistory();
        this.renderHistory();
    }

    cleanupHistory() {
        this.history.get();
    }

    cacheElements() {
        this.form = document.querySelector(`#${this.type}Form`);
        this.input = document.getElementById('inputValue');
        this.from = document.getElementById('fromUnit');
        this.to = document.getElementById('toUnit');
        this.result = document.getElementById('resultValue');
        this.swapBtn = document.getElementById('swapBtn');
        this.historyList = document.getElementById('historyList');
    }

    bindEvents() {
        if (!this.form) return;

        this.form.addEventListener('submit', e => this.submit(e));
        this.swapBtn?.addEventListener('click', e => this.swap(e));
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

            const history = this.history.get();
            history.unshift({
                ...data,
                result: result.result,
                timestamp: new Date().toISOString(),
            });

            this.history.save(history);
            this.renderHistory();
        } catch (err) {
            this.showError(err.message);
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

    renderHistory() {
        if (!this.historyList) return;

        const history = this.history.get();
        if (!history.length) {
            this.historyList.innerHTML = 'No history yet';
            return;
        }

        this.historyList.innerHTML = history.map(h => `
            <div>
                <strong>${h.value} ${h.from_unit}</strong>
                → ${h.result} ${h.to_unit}
                <small>${formatRelativeDate(h.timestamp)}</small>
            </div>
        `).join('');
    }
}
