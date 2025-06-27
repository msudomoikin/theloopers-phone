import { phonebook } from './phonebook';

export function findMatchingCountry(number: string): string | undefined {
    return Object.keys(phonebook).find((country) => {
        const pattern = phonebook[country].code;
        return pattern?.test(number);
    });
}