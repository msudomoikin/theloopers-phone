import './scss/styles.scss';
import clickSound from './assets/click.mp3';
import { tonePlayer } from './TonePlayer';
import { phonebook } from './phonebook';
import { findMatchingCountry } from './utils';
// const MAX_DIAL_DURATION = 3000;
const NUMPAD_BUTTONS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '#', '*']

const numpadContainer = document.querySelector('.phone__numpad');
const buttonClick = new Audio(clickSound);

enum PhoneState {
    HANG = 'hang',
    IDLE = 'idle',
    CALL = 'call',
}

class Phone {
    pickButton: HTMLElement | null;
    hangButton: HTMLElement | null;
    callButton: HTMLElement | null;
    numpad: NodeListOf<Element>;
    private _screen: Element | null;
    private _state: PhoneState;

    constructor() {
        this.pickButton = document.querySelector('.phone__pick-button');
        this.hangButton = document.querySelector('.phone__hang-button');
        this.callButton = document.querySelector('.phone__call-button');

        this.numpad = document.querySelectorAll('.phone__button');
        this._screen = document.querySelector('.phone__screen');

        this._state = PhoneState.HANG;
        this.hangButton?.classList.add('phone__control-button--disabled')
        this.callButton?.classList.add('phone__control-button--disabled')

        this.pickButton?.addEventListener('click', () => {
            phone.state = PhoneState.IDLE
            this.hangButton?.classList.remove('phone__control-button--disabled')
            this.pickButton?.classList.add('phone__pick-button--active');
            tonePlayer.playIdleTone();
        });

        this.hangButton?.addEventListener('click', () => {
            phone.reset();
        });

        this.callButton?.addEventListener('click', () => {
            if (this.state === PhoneState.IDLE) {
                tonePlayer.stopAll();

                phone.state = PhoneState.CALL;
                const number = this.screen || '';
                const matchingCountry = findMatchingCountry(number);


                if (!matchingCountry) {
                    console.warn('No matching country found for the number:', number);
                    return;
                }

                const dialTone = phonebook[matchingCountry]?.dialTone;

                if (!dialTone) {
                    console.warn(`Dial tone not found for country: ${matchingCountry}`);
                    return;
                }

                tonePlayer.playPattern(dialTone.hz, dialTone.on, dialTone.off);

                // setTimeout(() => {
                //     console.log('Maximum dial duration reached. Hanging up.');
                //     tonePlayer.stopPattern(); // или stopAll()
                //     phone.reset();
                // }, MAX_DIAL_DURATION);

                this.callButton?.classList.add('phone__control-button--disabled');
            }
        });
    }

    get screen(): string | null {
        return this._screen?.textContent ?? null;
    }

    set screen(text: string) {
        if (this._screen) {
            this._screen.textContent += text;
            this.callButton?.classList.remove('phone__control-button--disabled');
        }
    }

    set state(newState: PhoneState) {
        this._state = newState;
        console.log(`Phone state changed to: ${this.state}`);
    }

    get state(): string {
        return this._state;
    }

    reset() {
        this.state = PhoneState.HANG;
        tonePlayer.stopAll();

        if (this._screen) {
            this._screen.textContent = '';
        }
        this.pickButton?.classList.remove('phone__pick-button--active');
        this.hangButton?.classList.add('phone__control-button--disabled')
        this.callButton?.classList.add('phone__control-button--disabled')
    }
}

const phone = new Phone();

numpadContainer?.addEventListener('click', (e) => {
    const target = e.target as HTMLElement;
    const buttonEl = target.closest('.phone__button');

    if (buttonEl) {
        handleNumpadClick(buttonEl);
    }
});

function handleNumpadClick(button: Element) {
    if (phone.state === 'hang') {
        buttonClick.play();
    }

    if (phone.state === 'idle') {
        const buttonText = button.textContent;

        if (buttonText) {
            tonePlayer.playDtmfTone(buttonText);
        }

        console.log(`Button clicked: ${buttonText}`);

        if (phone.screen) {
            phone.screen = `${buttonText}`;
        }
    }
}

document.addEventListener('keyup', event => {

    if (phone.state === 'hang') {
        buttonClick.play();
    }

    if (phone.state === 'idle' && NUMPAD_BUTTONS.includes(event.key)) {
        const buttonText = event.key;
        tonePlayer.playDtmfTone(event.key); // stopAll внутри playDtmfTone

        console.log(`Physical Button clicked: ${buttonText}`);
        if (phone.screen !== null) {
            phone.screen = `${buttonText}`;
        }
    }
})