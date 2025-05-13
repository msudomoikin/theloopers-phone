import * as Tone from 'tone';

class TonePlayer {
    private oscillator1?: Tone.Oscillator;
    private oscillator2?: Tone.Oscillator;
    private patternInterval: number | null = null;



    playIdleTone() {
        this.stopAll();
        this.playSingleTone(350, Infinity);
    }

    playSingleTone(hz: number, durationMs: number = Infinity): void {
        this.stopAll();

        this.oscillator1 = new Tone.Oscillator(hz, 'sine').toDestination();
        this.oscillator1.volume.value = -12;
        this.oscillator1.start();

        if (durationMs < Infinity) {
            setTimeout(() => {
                this.oscillator1?.stop().dispose();
                this.oscillator1 = undefined;
            }, durationMs);
        }
    }

    playDualTone(freq1: number, freq2: number, durationMs: number = 350): void {
        this.stopAll();

        this.oscillator1 = new Tone.Oscillator(freq1, 'sine').toDestination();
        this.oscillator2 = new Tone.Oscillator(freq2, 'sine').toDestination();

        this.oscillator1.volume.value = -12;
        this.oscillator2.volume.value = -12;

        this.oscillator1.start();
        this.oscillator2.start();

        if (durationMs > 0) {
            setTimeout(() => this.stopAll(), durationMs);
        }
    }

    private patternOscillator1?: Tone.Oscillator;
    private patternOscillator2?: Tone.Oscillator;


    playPattern(hz: number[], onDuration: number, offDuration: number): void {
        this.stopAll();

        this.patternOscillator1 = new Tone.Oscillator(hz[0], 'sine').toDestination();
        this.patternOscillator2 = new Tone.Oscillator(hz[1], 'sine').toDestination();
        this.patternOscillator1.volume.value = -12;
        this.patternOscillator2.volume.value = -12;

        let isPlaying = true;

        const startTone = () => {
            this.patternOscillator1?.start();
            this.patternOscillator2?.start();
            setTimeout(() => {
                this.patternOscillator1?.stop();
                this.patternOscillator2?.stop();
                setTimeout(() => {
                    if (isPlaying) startTone();
                }, offDuration * 1000);
            }, onDuration * 1000);
        };

        startTone();

        this.patternInterval = window.setInterval(() => { }, 1);
    }



    playDtmfTone(buttonText: string) {
        this.stopAll();

        const frequencies = this.getDTMFFrequency(buttonText);
        if (typeof frequencies === 'number') {
            this.playSingleTone(frequencies, 350);
        } else {
            this.playDualTone(frequencies[0], frequencies[1], 350);
        }
    }

    private getDTMFFrequency(buttonText: string): [number, number] | number {
        const map: Record<string, [number, number] | number> = {
            '1': [697, 1209],
            '2': [697, 1336],
            '3': [697, 1477],
            '4': [770, 1209],
            '5': [770, 1336],
            '6': [770, 1477],
            '7': [852, 1209],
            '8': [852, 1336],
            '9': [852, 1477],
            '*': [941, 1209],
            '0': [941, 1336],
            '#': [941, 1477],
            // pick → можно оставить как отдельный случай
        };

        return map[buttonText] || [440, 440];
    }

    stopPattern(): void {
        if (this.patternInterval !== null) {
            clearInterval(this.patternInterval);
            this.patternInterval = null;
        }

        this.patternOscillator1?.stop().dispose();
        this.patternOscillator2?.stop().dispose();
        this.patternOscillator1 = undefined;
        this.patternOscillator2 = undefined;
    }

    stopAll(): void {
        if (this.patternInterval !== null) {
            this.stopPattern();
        }
        this.oscillator1?.stop().dispose();
        this.oscillator2?.stop().dispose();
        this.oscillator1 = undefined;
        this.oscillator2 = undefined;
    }

}

export const tonePlayer = new TonePlayer();