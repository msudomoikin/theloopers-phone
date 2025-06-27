type PhonebookRecord = {
    country: string,
    flagUrl: string,
    ringTone: string,
    busyTone: string,
    countries?: string[],
    code?: RegExp;

};

export const phonebookRecords: PhonebookRecord[] = [
    {
        country: 'Russia',
        countries: ['Kyrgyzstan', 'Lithuania', 'Moldova', 'Russia', 'Tajikistan'],
        flagUrl: 'https://upload.wikimedia.org/wikipedia/commons/f/f3/Flag_of_Russia.svg',
        ringTone: "425\/800,0\/3200",
        busyTone: '',
        code: /^7/,
    },
    {
        country: 'Jamaica',
        countries: ['Antigua and Barbuda', 'Bahamas', 'Barbados', 'Bermuda', 'British Virgin Islands', 'Canada', 'Cuba', 'Dominica', 'Grenada', 'Jamaica', 'Montserrat', 'Saint Kitts and Nevis', 'Trinidad and Tobago', 'Turks and Caicos Islands', 'USA'],
        flagUrl: 'https://upload.wikimedia.org/wikipedia/commons/0/0a/Flag_of_Jamaica.svg',
        ringTone: "440+480\/2000,0\/4000",
        busyTone: '',
        code: /^1/,
    },
    {
        country: 'Australia',
        countries: ['Fiji', 'Nauru'],
        flagUrl: 'https://upload.wikimedia.org/wikipedia/commons/b/b9/Flag_of_Australia.svg',
        ringTone: "425*25\/400,0\/200,425*25\/400,0\/2000",
        busyTone: '',
        code: /^61/,
    },
    {
        country: 'Japan',
        countries: [],
        flagUrl: 'https://upload.wikimedia.org/wikipedia/commons/9/9e/Flag_of_Japan.svg',
        ringTone: "400*16\/1000,0\/2000",
        busyTone: '',
        code: /^81/,
    },
    {
        country: 'India',
        countries: ['India', 'Bhutan'],
        flagUrl: 'https://upload.wikimedia.org/wikipedia/commons/4/41/Flag_of_India.svg',
        ringTone: "400*25\/400,0\/200,400*25\/400,0\/2600",
        busyTone: '',
        code: /^91/,
    },
    {
        country: 'Austria',
        countries: ['Germany'],
        flagUrl: 'https://upload.wikimedia.org/wikipedia/commons/4/41/Flag_of_Austria.svg',
        ringTone: "450\/1000,0\/5000",
        busyTone: '',
        code: /^43/,
    },
    {
        country: 'Serbia',
        countries: [],
        flagUrl: 'https://upload.wikimedia.org/wikipedia/commons/f/ff/Flag_of_Serbia.svg',
        ringTone: "450*25\/1000,0\/9000",
        busyTone: '',
        code: /^381/,
    },
    {
        country: 'Guinea',
        countries: [],
        flagUrl: 'https://upload.wikimedia.org/wikipedia/commons/e/ed/Flag_of_Guinea.svg',
        ringTone: "450\/400,0\/200",
        busyTone: '',
        code: /^224/,
    },
    {
        country: 'Pakistan',
        countries: [],
        flagUrl: 'https://upload.wikimedia.org/wikipedia/commons/3/32/Flag_of_Pakistan.svg',
        ringTone: "400\/1000,0\/2000",
        busyTone: '',
        code: /^92/,
    }
]




export class Phonebook {
    constructor() { }

    render(elementClass: string) {
        const elementToMount: HTMLDivElement = document.querySelector(elementClass) as HTMLDivElement;

        if (!elementToMount) {
            console.error("can't find element to render phonebook at");
        }

        const listEl = document.createElement('ul');
        listEl.classList.add('phonebook__list');

        phonebookRecords.forEach(record => {
            const listItemEl = document.createElement('li');
            listItemEl.classList.add('phonebook__item');


            const recordFlag = document.createElement('img');
            recordFlag.src = record.flagUrl
            recordFlag.alt = `Flag of ${record.country}`
            recordFlag.height = 10
            recordFlag.width = 30

            const recordTitle = document.createElement('h2');
            recordTitle.classList.add('phonebook__item-title');
            recordTitle.textContent = record.country

            const flagTitleWrapper = document.createElement('div');
            flagTitleWrapper.classList.add('phonebook__flag-title-wrapper')
            flagTitleWrapper.append(recordFlag, recordTitle)

            const recordNumber = document.createElement('span');
            recordNumber.classList.add('phonebook__item-number');
            recordNumber.textContent = String(record.code).replace('/', '').replace('^', '').replace('/', '')

            listItemEl.append(flagTitleWrapper)
            listItemEl.append(recordNumber)


            listEl.append(listItemEl)
        });

        elementToMount.append(listEl)
    }
}
