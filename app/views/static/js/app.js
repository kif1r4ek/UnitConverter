import {UnitConverterUI} from './ui/UnitConverterUI.js';
import {initMobileMenu} from './ui/MobileMenu.js';

document.addEventListener('DOMContentLoaded', () => {
    initMobileMenu();

    const path = location.pathname;
    const type =
        path.includes('length') ? 'length' :
        path.includes('temperature') ? 'temperature' :
        path.includes('weight') ? 'weight' :
        null;

    if (type) {
        new UnitConverterUI(type);
    }
});
