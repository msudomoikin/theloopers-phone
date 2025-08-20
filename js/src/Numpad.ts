import clickSound from "./assets/click.mp3";
import { tonePlayerVanilla as tonePlayer } from "./TonePlayerVanilla";
import { getDTMFFrequency } from "./dtmfFrequncies";
import { isTouchDevice } from "./utils";

export class Numpad {
  private numpadContainer: Element | null;
  private buttonClick: HTMLAudioElement;
  private buttonIsPressed: boolean = false;
  private readonly NUMPAD_BUTTONS = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "#",
    "*",
  ];

  // Callback functions that will be set by the Phone class
  public onButtonPress: ((buttonText: string) => void) | null = null;
  public canPlayClickSound: (() => boolean) | null = null;
  public canPlayTone: (() => boolean) | null = null;

  constructor() {
    this.numpadContainer = document.querySelector(".phone__numpad");
    this.buttonClick = new Audio(clickSound);

    this.initializeEventListeners();
  }

  private initializeEventListeners(): void {
    // Mouse events
    this.numpadContainer?.addEventListener("mousedown", (e) => {
      if (isTouchDevice()) return;

      const target = e.target as HTMLElement;
      const buttonEl = target.closest(".phone__button");

      if (buttonEl) {
        this.handleNumpadClick(buttonEl);
      }
    });

    this.numpadContainer?.addEventListener("mouseup", () => {
      tonePlayer.stopAll();
    });

    // Touch events
    this.numpadContainer?.addEventListener("touchstart", (e) => {
      const target = e.target as HTMLElement;
      const buttonEl = target.closest(".phone__button");

      if (buttonEl) {
        this.handleNumpadClick(buttonEl);
      }
    });

    // Keyboard events
    document.addEventListener("keydown", (event) => {
      if (isTouchDevice()) return;

      if (!this.NUMPAD_BUTTONS.includes(event.key)) return;

      if (this.canPlayClickSound?.() && !this.buttonIsPressed) {
        this.buttonIsPressed = true;
        this.buttonClick.play();
      }

      if (this.canPlayTone?.() && !this.buttonIsPressed) {
        this.buttonIsPressed = true;
        const buttonText = event.key;
        tonePlayer.start(getDTMFFrequency(event.key));
        console.log(`Physical Button clicked: ${buttonText}`);
      }
    });

    document.addEventListener("keyup", (event) => {
      if (isTouchDevice()) return;

      this.buttonIsPressed = false;

      if (this.canPlayTone?.() && this.NUMPAD_BUTTONS.includes(event.key)) {
        this.onButtonPress?.(event.key);
      }

      tonePlayer.stopAll();
    });
  }

  private handleNumpadClick(button: Element): void {
    const buttonText = button.textContent;

    if (!buttonText) return;

    if (this.canPlayClickSound?.()) {
      this.buttonClick.play();
    }

    if (this.canPlayTone?.()) {
      tonePlayer.start(getDTMFFrequency(buttonText));
      console.log(`Button clicked: ${buttonText}`);
      this.onButtonPress?.(buttonText);
    }
  }

  public getNumpadButtons(): string[] {
    return [...this.NUMPAD_BUTTONS];
  }
}
