import './scss/styles.scss';
import clickSound from './assets/click.mp3';
import { playTone, stopTone, clearTones } from './audio';

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
            playTone('pick');
            this.pickButton?.classList.add('phone__pick-button--active');
        });

        this.hangButton?.addEventListener('click', () => {
            stopTone('pick');
            phone.reset();
        });

        this.callButton?.addEventListener('click', () => {
            if (this.state === 'idle') {
                phone.state = PhoneState.CALL;
                console.log('Calling...');
            }
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
        clearTones();
        if (this._screen) {
            this._screen.textContent = '';
        }
        this.pickButton?.classList.remove('phone__pick-button--active');
        this.hangButton?.classList.add('phone__control-button--disabled')
        this.callButton?.classList.add('phone__control-button--disabled')
    }
}

const phone = new Phone();

phone.numpad.forEach((button) => {
    //TODO change to event delegation
    button.addEventListener('click', () => {
        handleNumpadClick(button);
    });
});

function handleNumpadClick(button: Element) {
    if (phone.state === 'hang') {
        buttonClick.play();
    }
    if (phone.state === 'idle') {
        playTone(button.textContent || '');
        console.log(`Button clicked: ${button.textContent}`);
        if (phone.screen !== null) {
            phone.screen = `${button.textContent}`;
        }
    }
}