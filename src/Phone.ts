import { findRingingTone } from "./utils";
import { tonePlayerVanilla as tonePlayer } from "./TonePlayerVanilla";
import { Numpad } from "./Numpad";

enum PhoneState {
  HANG = "hang",
  IDLE = "idle",
  DIALING = "dialing",
  CALL = "call",
}

export class Phone {
  pickButton: HTMLElement | null;
  hangButton: HTMLElement | null;
  callButton: HTMLElement | null;
  numpad: Numpad;
  private _screen: Element | null;
  private _state: PhoneState;

  constructor() {
    this.pickButton = document.querySelector(".phone__pick-button");
    this.hangButton = document.querySelector(".phone__hang-button");
    this.callButton = document.querySelector(".phone__call-button");

    this._screen = document.querySelector(".phone__screen");
    this._state = PhoneState.HANG;

    // Initialize numpad and set up callbacks
    this.numpad = new Numpad();
    this.setupNumpadCallbacks();

    this.initializeControlButtons();
  }

  private setupNumpadCallbacks(): void {
    // Set callback for when a numpad button is pressed
    this.numpad.onButtonPress = (buttonText: string) => {
      if (this._screen !== null && this.state === "idle") {
        this.screen = buttonText;
      }
    };

    // Set callback to determine if click sound should play
    this.numpad.canPlayClickSound = () => {
      return this.state === "hang";
    };

    // Set callback to determine if tone should play
    this.numpad.canPlayTone = () => {
      return this.state === "idle";
    };
  }

  private initializeControlButtons(): void {
    this.hangButton?.classList.add("phone__control-button--disabled");
    this.callButton?.classList.add("phone__control-button--disabled");

    this.pickButton?.addEventListener("click", () => {
      this.state = PhoneState.IDLE;
      this.hangButton?.classList.remove("phone__control-button--disabled");
      this.pickButton?.classList.add("phone__pick-button--active");
      tonePlayer.playIdleTone();
    });

    this.hangButton?.addEventListener("click", () => {
      this.reset();
    });

    this.callButton?.addEventListener("click", () => {
      if (this.state === PhoneState.IDLE) {
        tonePlayer.stopAll();

        this.state = PhoneState.CALL;
        const number = this.screen || "";
        const ringingTone = findRingingTone(number);

        if (!ringingTone) {
          console.warn(
            "No matching ringing tone found for the number:",
            number
          );
          this.reset();
          return;
        }

        tonePlayer.playPattern(ringingTone);
        this.callButton?.classList.remove("phone__control-button--active");
        this.callButton?.classList.add("phone__control-button--disabled");
      }
    });
  }

  get screen(): string | null {
    return this._screen?.textContent ?? null;
  }

  set screen(text: string) {
    if (this._screen) {
      this._screen.textContent += text;
      this.callButton?.classList.remove("phone__control-button--disabled");
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
      this._screen.textContent = "";
    }
    this.pickButton?.classList.remove("phone__pick-button--active");
    this.hangButton?.classList.add("phone__control-button--disabled");
    this.callButton?.classList.add("phone__control-button--disabled");
  }
}
