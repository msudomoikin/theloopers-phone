import "./scss/styles.scss";
import { Phone } from "./Phone";
import { Phonebook } from "./Phonebook";

// Initialize phonebook
export const phone = new Phone();
const phonebook = new Phonebook();
phonebook.render(".phonebook");