
import { findRingingTone } from './utils';
// import { tonePlayer } from './TonePlayer';
import { tonePlayerVanilla as tonePlayer } from './TonePlayerVanilla';

enum PhoneState {
    HANG = 'hang',
    IDLE = 'idle',
    DIALING = 'dialing',
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
                const ringingTone = findRingingTone(number);


                if (!ringingTone) {
                    console.warn('No matching ringing tone found for the number:', number);
                    this.reset()
                    return;
                }


                tonePlayer.playPattern(ringingTone);
                this.callButton?.classList.remove('phone__control-button--active');
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

export const phone = new Phone();