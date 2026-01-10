export class HistoryStorage {
    constructor(key) {
        this.key = key;
    }

    get() {
        const data = localStorage.getItem(this.key);
        return data ? JSON.parse(data) : [];
    }

    save(item, limit = 5) {
        const history = [item, ...this.get()].slice(0, limit);
        localStorage.setItem(this.key, JSON.stringify(history));
    }

    clear() {
        localStorage.removeItem(this.key);
    }
}
