const context = new window.AudioContext();

class TonePlayer {
    private context: AudioContext;
    private osc1: OscillatorNode | null = null;
    private osc2: OscillatorNode | null = null;
    private gainNode: GainNode | null = null;
    private filter: BiquadFilterNode | null = null;
    private isPlaying: boolean = false;

    constructor(context: AudioContext) {
        this.context = context;
    }

    private setup(freq1: number, freq2: number): void {
        // Create oscillators
        this.osc1 = this.context.createOscillator();
        this.osc2 = this.context.createOscillator();
        
        // Set frequencies
        this.osc1.frequency.value = freq1;
        this.osc2.frequency.value = freq2;

        // Create gain node with initial value of 0 (silent start)
        this.gainNode = this.context.createGain();
        this.gainNode.gain.value = 0;

        // Create filter
        this.filter = this.context.createBiquadFilter();
        this.filter.type = "lowpass";
        this.filter.frequency.value = 8000;

        // Connect audio graph
        this.osc1.connect(this.gainNode);
        this.osc2.connect(this.gainNode);
        this.gainNode.connect(this.filter);
        this.filter.connect(this.context.destination);

        // Start oscillators (but they're silent due to gain = 0)
        this.osc1.start(0);
        this.osc2.start(0);

        this.isPlaying = true;
    }

    start(freqArray: [number, number]): void {
        // If already playing, smooth transition to new frequencies
        if (this.isPlaying && this.osc1 && this.osc2 && this.gainNode) {
            // Smooth frequency transition
            const now = this.context.currentTime;
            this.osc1.frequency.setValueAtTime(this.osc1.frequency.value, now);
            this.osc1.frequency.linearRampToValueAtTime(freqArray[0], now + 0.005);
            
            this.osc2.frequency.setValueAtTime(this.osc2.frequency.value, now);
            this.osc2.frequency.linearRampToValueAtTime(freqArray[1], now + 0.005);
            return;
        }

        // Stop any existing tone
        this.stopAll();
        
        // Create new tone
        this.setup(freqArray[0], freqArray[1]);
        
        // Smooth fade in to prevent clicks
        const now = this.context.currentTime;
        this.gainNode!.gain.setValueAtTime(0, now);
        this.gainNode!.gain.linearRampToValueAtTime(0.25, now + 0.005); // 5ms fade in
    }

    stopAll(): void {
        if (this.isPlaying && this.gainNode && this.osc1 && this.osc2) {
            const now = this.context.currentTime;
            const fadeTime = 0.005; // 5ms fade out
            
            // Smooth fade out to prevent clicks
            this.gainNode.gain.setValueAtTime(this.gainNode.gain.value, now);
            this.gainNode.gain.linearRampToValueAtTime(0, now + fadeTime);
            
            // Stop oscillators after fade out completes
            this.osc1.stop(now + fadeTime + 0.001);
            this.osc2.stop(now + fadeTime + 0.001);
            
            // Clean up references
            setTimeout(() => {
                this.osc1 = null;
                this.osc2 = null;
                this.gainNode = null;
                this.filter = null;
                this.isPlaying = false;
            }, (fadeTime + 0.01) * 1000);
        }
    }
    playIdleTone() {
        this.start([350, 440])
    }
}

export const tonePlayerVanilla = new TonePlayer(context);