export class ConverterService {
    constructor(type) {
        this.url = `/${type}/convert`;
    }

    async convert(payload) {
        const response = await fetch(this.url, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(this.extractErrorMessage(data));
        }

        return data;
    }

    extractErrorMessage(error) {
        if (Array.isArray(error.detail)) {
            return error.detail.map(e => e.msg).join(', ');
        }

        return error.detail || 'Conversion failed';
    }
}
