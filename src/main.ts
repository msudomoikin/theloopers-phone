import './scss/styles.scss';
import clickSound from './assets/click.mp3';
// import { tonePlayer } from './TonePlayer';
import { phone } from './Phone';
import { tonePlayerVanilla as tonePlayer } from './TonePlayerVanilla';
import { getDTMFFrequency } from './dtmfFrequncies';


let buttonIsPressed: boolean = false
const NUMPAD_BUTTONS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '#', '*']

const numpadContainer = document.querySelector('.phone__numpad');
const buttonClick = new Audio(clickSound);


numpadContainer?.addEventListener('mousedown', (e) => {
    const target = e.target as HTMLElement;
    const buttonEl = target.closest('.phone__button');

    if (buttonEl) {
        handleNumpadClick(buttonEl);
    }
});

numpadContainer?.addEventListener('mouseup', () => {
    tonePlayer.stopAll();
})

numpadContainer?.addEventListener('touchstart', (e) => {
    const target = e.target as HTMLElement;
    const buttonEl = target.closest('.phone__button');

    if (buttonEl) {
        handleNumpadClick(buttonEl);
    }
});

// mouse click on button

function handleNumpadClick(button: Element) {
    if (phone.state === 'hang') {
        buttonClick.play();
    }

    if (phone.state === 'idle') {
        const buttonText = button.textContent;

        if (buttonText) {
            tonePlayer.start(getDTMFFrequency(buttonText));
        }

        console.log(`Button clicked: ${buttonText}`);

        if (phone.screen !== null) {
            phone.screen = `${buttonText}`;
        }
    }
}

// click on physical button
document.addEventListener('keydown', event => {

    if (!NUMPAD_BUTTONS.includes(event.key)) {
        return
    }

    if (phone.state === 'hang' && !buttonIsPressed) {
        buttonIsPressed = true;
        buttonClick.play();
    }

    if (phone.state === 'idle' && !buttonIsPressed) {
        buttonIsPressed = true;

        const buttonText = event.key;
        tonePlayer.start(getDTMFFrequency(event.key));
        console.log(`Physical Button clicked: ${buttonText}`);

    }
});

document.addEventListener('keyup', event => {
    buttonIsPressed = false;
    if (phone.screen !== null && phone.state === 'idle' && NUMPAD_BUTTONS.includes(event.key)) {
        phone.screen = `${event.key}`;
    }
    tonePlayer.stopAll();

})