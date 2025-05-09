import './scss/styles.scss';
import clickSound from './assets/click.mp3';

const buttonClick = new Audio(clickSound);

enum PhoneState {
    HANG = 'hang',
    IDLE = 'idle',
    CALL = 'call',
}

class Phone {
    pickButton: Element | null;
    hangButton: Element | null;
    callButton: Element | null;
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


        this.callButton?.addEventListener('click', () => {
            if (this.state === 'idle') {
                phone.state = PhoneState.CALL;
                console.log('Calling...');
            }
        });

        this.hangButton?.addEventListener('click', () => {
            phone.state = PhoneState.HANG;
        });

        this.pickButton?.addEventListener('click', () => {
            phone.state = PhoneState.IDLE
        });
    }
    get screen(): string | null {
        return this._screen?.textContent ?? null;
    }
    set screen(text: string) {
        if (this._screen) {
            this._screen.textContent += text;
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
        if (this._screen) {
            this._screen.textContent = '';
        }
    }
}

const phone = new Phone();

phone.numpad.forEach((button) => {
    //TODO change to event delegation
    button.addEventListener('click', () => {
        handleNumpadClick(button);
    });
});

phone.hangButton?.addEventListener('click', () => {
    phone.reset();
});



function handleNumpadClick(button: Element) {
    if (phone.state === 'hang') {
        buttonClick.play();
    }
    if (phone.state === 'idle') {
        console.log(`Button clicked: ${button.textContent}`);
        if (phone.screen !== null) {
            phone.screen = `${button.textContent}`;
        }
    }
}