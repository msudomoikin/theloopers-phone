const context = new window.AudioContext();

interface ToneElement {
    frequencies: number[];
    modulated: boolean;
    duration: number;
    noRepeat: boolean;
}

class TonePlayer {
    private context: AudioContext;
    private osc1: OscillatorNode | null = null;
    private osc2: OscillatorNode | null = null;
    private modulatorOsc: OscillatorNode | null = null;
    private gainNode: GainNode | null = null;
    private modulatorGain: GainNode | null = null;
    private filter: BiquadFilterNode | null = null;
    private isPlaying: boolean = false;
    private patternTimeout: NodeJS.Timeout | null = null;
    private currentPattern: ToneElement[] = [];
    private patternIndex: number = 0;
    private shouldRepeat: boolean = true;

    constructor(context: AudioContext) {
        this.context = context;
    }

    private setup(freq1: number, freq2?: number, isModulated: boolean = false): void {
        // Create oscillators
        this.osc1 = this.context.createOscillator();
        if (freq2 && freq2 > 0) {
            this.osc2 = this.context.createOscillator();
        }

        // Set frequencies
        this.osc1.frequency.value = freq1;
        if (this.osc2) {
            this.osc2.frequency.value = freq2!;
        }

        // Create gain node with initial value of 0 (silent start)
        this.gainNode = this.context.createGain();
        this.gainNode.gain.value = 0;

        // Create filter
        this.filter = this.context.createBiquadFilter();
        this.filter.type = "lowpass";
        this.filter.frequency.value = 8000;

        if (isModulated && this.osc2) {
            // Set up amplitude modulation
            this.modulatorGain = this.context.createGain();
            this.modulatorGain.gain.value = 0.95; // 95% modulation index
            
            // Connect modulator to carrier frequency
            this.osc2.connect(this.modulatorGain);
            this.modulatorGain.connect(this.osc1.frequency);
            
            // Connect carrier through gain control to output
            this.osc1.connect(this.gainNode);
        } else {
            // Connect audio graph for single freq or mixture
            this.osc1.connect(this.gainNode);
            if (this.osc2) {
                this.osc2.connect(this.gainNode);
            }
        }
        
        this.gainNode.connect(this.filter);
        this.filter.connect(this.context.destination);

        // Start oscillators (but they're silent due to gain = 0)
        this.osc1.start(0);
        if (this.osc2) {
            this.osc2.start(0);
        }

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
        // Clear any pattern timeout
        if (this.patternTimeout) {
            clearTimeout(this.patternTimeout);
            this.patternTimeout = null;
        }

        if (this.isPlaying && this.gainNode) {
            const now = this.context.currentTime;
            const fadeTime = 0.005; // 5ms fade out
            
            // Smooth fade out to prevent clicks
            this.gainNode.gain.setValueAtTime(this.gainNode.gain.value, now);
            this.gainNode.gain.linearRampToValueAtTime(0, now + fadeTime);
            
            // Stop oscillators after fade out completes
            if (this.osc1) {
                this.osc1.stop(now + fadeTime + 0.001);
            }
            if (this.osc2) {
                this.osc2.stop(now + fadeTime + 0.001);
            }
            if (this.modulatorOsc) {
                this.modulatorOsc.stop(now + fadeTime + 0.001);
            }
            
            // Clean up references
            setTimeout(() => {
                this.osc1 = null;
                this.osc2 = null;
                this.modulatorOsc = null;
                this.gainNode = null;
                this.modulatorGain = null;
                this.filter = null;
                this.isPlaying = false;
            }, (fadeTime + 0.01) * 1000);
        }
    }

    playIdleTone(): void {
        this.start([350, 440]);
    }

    private parseTonePattern(pattern: string): ToneElement[] {
        const elements = pattern.split(',');
        return elements.map(element => {
            const noRepeat = element.startsWith('!');
            const cleanElement = noRepeat ? element.slice(1) : element;
            
            const [freqPart, durationStr] = cleanElement.split('/');
            const duration = durationStr ? parseInt(durationStr, 10) : 1000; // Default 1s
            
            let frequencies: number[] = [];
            let modulated = false;
            
            if (freqPart.includes('*')) {
                // Modulated frequency (f1*f2)
                frequencies = freqPart.split('*').map(f => parseInt(f, 10));
                modulated = true;
            } else if (freqPart.includes('+')) {
                // Mixed frequencies (f1+f2)
                frequencies = freqPart.split('+').map(f => parseInt(f, 10));
                modulated = false;
            } else {
                // Single frequency
                frequencies = [parseInt(freqPart, 10)];
                modulated = false;
            }
            
            return {
                frequencies,
                modulated,
                duration,
                noRepeat
            };
        });
    }

    playPattern(pattern: string): void {
        this.stopAll();
        this.currentPattern = this.parseTonePattern(pattern);
        this.patternIndex = 0;
        
        // Check if pattern should repeat (only if ALL elements have !)
        this.shouldRepeat = !this.currentPattern.every(element => element.noRepeat);
        
        this.playNextElement();
    }

    private playNextElement(): void {
        if (this.patternIndex >= this.currentPattern.length) {
            if (this.shouldRepeat) {
                this.patternIndex = 0;
            } else {
                this.stopAll();
                return;
            }
        }

        const element = this.currentPattern[this.patternIndex];
        
        if (element.frequencies[0] === 0) {
            // Silence
            this.stopCurrentTone();
        } else {
            // Play tone
            this.playToneElement(element);
        }

        // Schedule next element
        this.patternTimeout = setTimeout(() => {
            this.patternIndex++;
            this.playNextElement();
        }, element.duration);
    }

    private playToneElement(element: ToneElement): void {
        this.stopCurrentTone();
        
        const freq1 = element.frequencies[0];
        const freq2 = element.frequencies[1] || 0;
        
        this.setup(freq1, freq2, element.modulated);
        
        // Smooth fade in to prevent clicks
        const now = this.context.currentTime;
        this.gainNode!.gain.setValueAtTime(0, now);
        this.gainNode!.gain.linearRampToValueAtTime(0.25, now + 0.005);
    }

    private stopCurrentTone(): void {
        if (this.isPlaying && this.gainNode) {
            const now = this.context.currentTime;
            const fadeTime = 0.005;
            
            this.gainNode.gain.setValueAtTime(this.gainNode.gain.value, now);
            this.gainNode.gain.linearRampToValueAtTime(0, now + fadeTime);
            
            if (this.osc1) {
                this.osc1.stop(now + fadeTime + 0.001);
                this.osc1 = null;
            }
            if (this.osc2) {
                this.osc2.stop(now + fadeTime + 0.001);
                this.osc2 = null;
            }
            if (this.modulatorOsc) {
                this.modulatorOsc.stop(now + fadeTime + 0.001);
                this.modulatorOsc = null;
            }
            
            this.gainNode = null;
            this.modulatorGain = null;
            this.filter = null;
            this.isPlaying = false;
        }
    }
}

export const tonePlayerVanilla = new TonePlayer(context);