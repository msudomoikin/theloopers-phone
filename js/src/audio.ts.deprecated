import { tonePlayer } from './TonePlayer';
import { phonebook } from './phonebook';
import { findMatchingCountry } from './utils';

const MAX_DIAL_DURATION = 3000;

function getFrequencyFromButton(buttonText: string): [number, number] | number {
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
        'pick': 350, // single-tone for pickup
    };

    return map[buttonText] ?? [440, 440];
}

export function playTone(button: string): void {
    const freq = getFrequencyFromButton(button);

    if (typeof freq === 'number') {
        tonePlayer.playSingleTone(freq);
    } else {
        tonePlayer.playDualTone(freq[0], freq[1]);
    }
}

export function stopTone(): void {
    tonePlayer.stopAll();
}

export function clearTones(): void {
    tonePlayer.stopAll();
}

export function playDialTone(number: string): void {
    const matchingCountry = findMatchingCountry(number);
    if (!matchingCountry) return console.error('No matching country found');

    const dialTone = phonebook[matchingCountry]?.dialTone;
    if (!dialTone) return console.error('Dial tone not found');

    console.log(`Playing dial tone for ${matchingCountry}`);
    tonePlayer.playPattern(dialTone.hz, dialTone.on, dialTone.off);

    setTimeout(() => {
        console.log('Hanging up after max dial duration');
        tonePlayer.stopPattern();
    }, MAX_DIAL_DURATION);
}