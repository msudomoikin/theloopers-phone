import { phonebookRecords } from "./Phonebook"


export function findRingingTone(number: string): string | undefined {
    const record = phonebookRecords.find((record) => {
        return record.code?.test(number)
    })

    return record?.ringTone
}

export function isTouchDevice(): boolean {
    return (
        "ontouchstart" in window ||
        navigator.maxTouchPoints > 0
    );
}