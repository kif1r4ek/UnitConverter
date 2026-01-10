const ONE_DAY_MS = 24 * 60 * 60 * 1000;

export class HistoryStorage {
    constructor(key, ttl = ONE_DAY_MS) {
        this.key = key;
        this.ttl = ttl;
    }

    save(items) {
        const payload = {
            data: items,
            expiresAt: Date.now() + this.ttl,
        };

        localStorage.setItem(this.key, JSON.stringify(payload));
    }

    get() {
        const raw = localStorage.getItem(this.key);
        if (!raw) return [];

        try {
            const { data, expiresAt } = JSON.parse(raw);

            if (Date.now() > expiresAt) {
                this.clear();
                return [];
            }

            return Array.isArray(data) ? data : [];
        } catch {
            this.clear();
            return [];
        }
    }

    clear() {
        localStorage.removeItem(this.key);
    }
}
