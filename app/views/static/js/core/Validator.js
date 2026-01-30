export function validateConversionInput(value) {
    if (value === null || value === undefined || isNaN(value)) {
        throw new Error('Please enter a valid number');
    }
}
