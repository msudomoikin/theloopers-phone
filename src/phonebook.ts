type Phonebook = {
    [country: string]: {
        dialTone: { hz: number[]; on: number; off: number };
        busyTone: { hz: number[]; on: number; off: number };
        pattern?: RegExp; 
    };
};

export const phonebook: Phonebook = {
    Albania: {
        dialTone: { hz: [425, 24], on: 1, off: 4 },
        busyTone: { hz: [425], on: 0.5, off: 0.5 },
        pattern: /^355/,
    },
    Andorra: {
        dialTone: { hz: [425], on: 1.5, off: 3 },
        busyTone: { hz: [425], on: 0.75, off: 0.75 },
        pattern: /^376/,
    },
    SAR: {
        dialTone: { hz: [400], on: 1, off: 1.5 },
        busyTone: { hz: [400], on: 0.5, off: 0.5 },
    },
};