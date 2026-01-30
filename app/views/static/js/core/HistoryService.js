/**
 * Service for managing conversion history via Redis API
 */
export class HistoryService {
    constructor(converterType) {
        this.type = converterType;
        this.baseUrl = `/${converterType}`;
    }

    async fetchHistory() {
        try {
            const response = await fetch(`${this.baseUrl}/history`);
            
            if (!response.ok) {
                throw new Error('Failed to fetch history');
            }
            
            const data = await response.json();
            return data.history || [];
            
        } catch (error) {
            console.error('History fetch error:', error);
            return [];
        }
    }

    async clearHistory() {
        try {
            const response = await fetch(`${this.baseUrl}/history`, {
                method: 'DELETE'
            });
            
            if (!response.ok) {
                throw new Error('Failed to clear history');
            }
            
            return true;
            
        } catch (error) {
            console.error('History clear error:', error);
            return false;
        }
    }
}