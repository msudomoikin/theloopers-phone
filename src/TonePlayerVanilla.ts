const context = new window.AudioContext;

class TonePlayer {
    private context: AudioContext;
    private gainNode: GainNode;
    private filter: BiquadFilterNode;

    private osc1!: OscillatorNode;
    private osc2!: OscillatorNode;

    constructor(context: AudioContext) {
        this.context = context;

        // Create shared nodes (can be reused)
        this.gainNode = this.context.createGain();
        this.gainNode.gain.value = 0.25;

        this.filter = this.context.createBiquadFilter();
        this.filter.type = "lowpass";
        this.filter.frequency.value = 8000;

        this.gainNode.connect(this.filter);
        this.filter.connect(this.context.destination);
    }

    private setup(freq1: number, freq2: number): void {
        // Always create new oscillators
        this.osc1 = this.context.createOscillator();
        this.osc2 = this.context.createOscillator();

        this.osc1.frequency.value = freq1;
        this.osc2.frequency.value = freq2;

        // Connect them to shared graph
        this.osc1.connect(this.gainNode);
        this.osc2.connect(this.gainNode);

        // Start them
        this.osc1.start(0);
        this.osc2.start(0);
    }

    start(freqArray: [number, number]): void {
        this.stopAll(); // Ensure old oscillators are cleaned up
        this.setup(freqArray[0], freqArray[1]);
    }

    stopAll(): void {
        if (this.osc1) {
            this.osc1.stop(0);
            this.osc1.disconnect();
        }
        if (this.osc2) {
            this.osc2.stop(0);
            this.osc2.disconnect();
        }
    }

    playIdleTone(): void {
        this.start([350, 440]);
    }
}

export const tonePlayerVanilla = new TonePlayer(context);