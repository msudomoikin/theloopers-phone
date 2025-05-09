import './scss/styles.scss';

const screen = document.querySelector('.phone__screen');
const buttons = document.querySelectorAll('.phone__button');

buttons.forEach((button) => {
    button.addEventListener('click', () => {
        console.log(`Button clicked! ${button.textContent}`);
        
        if (screen) {
            screen.textContent += `${button.textContent}`;
        }
    });
});