---
tag: K5MDB2
kind: concept
slug: kerckhoffs-principle
name: Kerckhoffs's principle
aliases:
- Kerckhoffs's law
- open design principle
area: cryptography/symmetric-ciphers
level: intro
summary: A cipher must stay secure when the enemy knows everything about it except the key. Kerckhoffs stated it in 1883; Shannon wrote "the enemy knows the system"; modern definitions build on it.
prereqs: [symmetric-encryption]
see_also: [cryptanalysis, ciphertext-only-attack, known-plaintext-attack, perfect-secrecy, semantic-security, enigma-machine, advanced-encryption-standard, exhaustive-key-search]
sources:
  - paper: "Auguste Kerckhoffs, La cryptographie militaire, Journal des sciences militaires, vol. IX, January 1883, pp. 5-38, and February 1883, pp. 161-191"
    locator: the first part (January 1883), the list of six desiderata for a military cipher system
  - paper: doi:10.1002/j.1538-7305.1949.tb00928.x
    title: Claude E. Shannon, Communication theory of secrecy systems, Bell System Technical Journal 28(4), 1949, pp. 656-715
    locator: Part I, the description of a secrecy system and the assumption that the enemy knows the system being used
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Section 1.2 (the setting of private-key encryption, Kerckhoffs' principle and the arguments for public algorithms)
  - book: isbn:9780684831305
    title: David Kahn, The Codebreakers, revised edition, Scribner, 1996
    locator: the account of Auguste Kerckhoffs and of La cryptographie militaire
---

Kerckhoffs's principle says that a cipher system must stay secure even when the enemy knows how it works. Only the key needs to be secret. Auguste Kerckhoffs, a Dutch linguist who taught in France, put it in 1883 as the second of six requirements for military ciphers. Claude Shannon restated it in 1949 as the assumption that the enemy knows the system being used, and the short form "the enemy knows the system" is called Shannon's maxim. Every modern security definition builds on the principle: the attacker is given the algorithms, and only the key is hidden.

## In plain words

A lock maker should assume that burglars will buy the same lock, take it apart and study it. The lock must still keep them out without the right key. A cipher is the same. The machines and programs will be captured, copied, leaked or bought. If the secret is in the design, one leak breaks every message ever sent, and the design cannot be changed fast. If the secret is only in the key, a lost key is replaced, and the design can be studied in the open by many experts, who find the flaws before an enemy does.

## The idea

**Kerckhoffs's six desiderata.** In "La cryptographie militaire" (1883), Kerckhoffs listed six requirements for a cipher system for use in the field. The translation below is mine; I tried to keep close to the French text.

1. The system must be in practice, if not mathematically, impossible to decipher.
2. It must not require secrecy, and it must be able to fall into the hands of the enemy without harm.
3. It must be possible to communicate and to remember the key without the help of written notes, and to change or modify it at the will of the correspondents.
4. It must be usable for telegraph correspondence.
5. It must be portable, and its handling or operation must not need the help of several people.
6. Finally, given the conditions in which it is used, the system must be easy to use, and it must not require mental strain or the knowledge of a long series of rules.

The second requirement is the one now called Kerckhoffs's principle. The others are about usability in the field; the first one already separates practical security from mathematical security, an idea that returns in modern computational cryptography.

**Shannon's maxim.** In his paper of 1949, Shannon described a secrecy system as a set of transformations, one for each key, and assumed that the enemy knows the system being used, that is, the set of transformations and the probabilities of the keys. Only the choice of the key is unknown. Under this assumption he defined [perfect secrecy](/perfect-secrecy/) and computed how much ciphertext determines the key.

**Why the principle is the basis of modern definitions.** A modern encryption scheme is a triple of public algorithms $(\mathrm{Gen}, \mathrm{Enc}, \mathrm{Dec})$. A security definition, such as [semantic security](/semantic-security/) or perfect secrecy, quantifies over all attackers, and an attacker may depend on the algorithms in any way: it may run them, analyse them, or have them built into its own code. The only thing it does not know is the key, chosen at random by $\mathrm{Gen}$, and the random choices of the encryption. This has three effects.

- **The secret is small and well defined.** Security is reduced to the secrecy of a random key of a given length, which can be analysed, for example by counting the cost of an [exhaustive key search](/exhaustive-key-search/).
- **The definition does not depend on what the attacker happens to know.** A definition that relied on the secrecy of the design would hold only until the design leaked, and nobody could tell when that happened.
- **Public analysis is possible.** Standards such as the [Advanced Encryption Standard](/advanced-encryption-standard/) were chosen in open competitions, and their security is the result of years of public [cryptanalysis](/cryptanalysis/).

## Examples

- **Enigma.** The Allies rebuilt the wiring of the [Enigma machine](/enigma-machine/) from mathematics, captured machines and documents. Its security had to rest on the daily keys, and where the key handling was weak, the system fell. Kerckhoffs's principle describes the situation of every field cipher.
- **The one-time pad.** The [one-time pad](/one-time-pad/) is the extreme case: the algorithm is public and trivial, and all security lies in the key.
- **Secret designs that failed.** Several proprietary ciphers whose designs were kept secret were broken soon after the designs were found by reverse engineering, among them the Content Scramble System of the DVD and the Crypto-1 cipher of the MIFARE Classic cards. Their designers relied on secrecy instead of public analysis.
- **Public key cryptography.** Here even the encryption key is public. Kerckhoffs's principle is taken to its end: everything except the private key is known.

## Where it is used

- Every attack model, from the [ciphertext-only attack](/ciphertext-only-attack/) to the [known-plaintext attack](/known-plaintext-attack/) and stronger models, assumes that the attacker knows the algorithm.
- Standards bodies publish algorithms and test vectors, and invite analysis before adoption.
- In computer security, the related principle of open design of Saltzer and Schroeder (1975) says that the design of a protection mechanism should not be secret. This is the source of the alias of this page.
- The principle does not forbid secret designs; it says that security must not depend on them. Some agencies keep designs secret as an extra layer, while the analysis assumes that the design is known.

## References
