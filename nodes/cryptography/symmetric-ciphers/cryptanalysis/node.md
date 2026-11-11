---
tag: RDK5ZW
kind: concept
slug: cryptanalysis
name: Cryptanalysis
aliases:
- code breaking
area: cryptography/symmetric-ciphers
level: intro
summary: The study of how to break cryptographic systems. It fixes what the attacker sees (the attack model), what counts as a break (the goal), and the cost in data, time and memory.
prereqs: [symmetric-encryption, kerckhoffs-principle]
see_also: [cipher-breaking, ciphertext-only-attack, known-plaintext-attack, chosen-plaintext-attack, chosen-ciphertext-attack, related-key-attack, key-recovery, exhaustive-key-search]
sources:
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 1, Section 1.13 (classes of attacks on encryption schemes) and Chapter 7, Section 7.2 (attack models, data and work complexity, exhaustive key search)
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Section 1.2 (the attack scenarios, from ciphertext-only to chosen-ciphertext attacks) and Section 1.3 (historical ciphers and their cryptanalysis)
  - paper: "Lars R. Knudsen, Block ciphers, a survey, in Ivan Damgård (editor), Lectures on Data Security, Modern Cryptology in Theory and Practice, Lecture Notes in Computer Science 1561, Springer, 1999"
    locator: the classification of attacks on block ciphers by their result (total break, global deduction, instance deduction, information deduction) and by their cost
  - paper: "Mitsuru Matsui, Linear cryptanalysis method for DES cipher, Advances in Cryptology, EUROCRYPT '93, Lecture Notes in Computer Science 765, Springer, 1994, pp. 386-397"
    locator: the known-plaintext attack on DES and its data requirement
---

Cryptanalysis is the study of how to break cryptographic systems, or to show that they are weaker than claimed. Together with cryptography, the design of systems, it forms cryptology. A cryptanalytic result has three parts: the *attack model*, which says what the attacker can see and ask for; the *goal*, which says what counts as a break; and the *cost*, measured in data, time and memory. Following [Kerckhoffs's principle](/kerckhoffs-principle/), the attacker always knows the algorithm, and only the key is secret. Classical cryptanalysis broke hand ciphers with letter statistics; modern cryptanalysis attacks block ciphers, stream ciphers, hash functions and protocols with methods such as [linear](/linear-cryptanalysis/) and [differential cryptanalysis](/differential-cryptanalysis/).

## In plain words

A code breaker wants to read secret messages, or to find the key that unlocks them. What the code breaker can do depends on the situation. Sometimes there are only intercepted messages. Sometimes some messages are known in clear too, because they were greetings, weather reports or published later. Sometimes the code breaker can make the system encrypt or decrypt chosen texts.

A break can also mean different things: finding the key, reading one message, or only telling the cipher apart from random noise. And each attack has a price: how many messages it needs, how much computing, and how much storage. Cryptanalysis describes all three, so that attacks can be compared.

## The idea

**Attack models.** Each model gives the attacker more power than the one before. A cipher that resists a stronger model also resists the weaker ones.

| model | what the attacker has |
|---|---|
| [ciphertext-only attack](/ciphertext-only-attack/) (COA) | ciphertexts only |
| [known-plaintext attack](/known-plaintext-attack/) (KPA) | pairs of plaintext and ciphertext, not chosen by the attacker |
| [chosen-plaintext attack](/chosen-plaintext-attack/) (CPA) | the ciphertexts of plaintexts of its choice; adaptive if each choice may depend on earlier answers |
| [chosen-ciphertext attack](/chosen-ciphertext-attack/) (CCA) | in addition, the decryptions of ciphertexts of its choice, other than the target |
| [related-key attack](/related-key-attack/) | encryptions under several keys with a relation that the attacker chooses, such as a known XOR difference |

The models of modern definitions, such as [IND-CPA](/ind-cpa-security/) and [IND-CCA](/ind-cca-security/) security, turn the CPA and CCA rows into games between an attacker and a challenger.

**Goals.** Knudsen classified the results of attacks on block ciphers, from the strongest to the weakest.

1. **Total break.** The attacker finds the key. This is [key recovery](/key-recovery/).
2. **Global deduction.** The attacker finds an algorithm that encrypts or decrypts like the cipher with the key, without knowing the key.
3. **Instance (local) deduction.** The attacker finds the plaintext of an intercepted ciphertext, or the ciphertext of a given plaintext.
4. **Information deduction.** The attacker learns some information about the key or the plaintexts that it did not have before.

A **distinguishing attack** is a form of information deduction: the attacker tells the cipher with a random key apart from a random permutation, with an advantage that is not negligible. Modern definitions of security for block ciphers and encryption schemes forbid exactly this, so a distinguisher counts as a break of the definition, even if no message is read.

**Cost.** An attack is measured by three resources:

- **Data:** the number of ciphertexts, known pairs, or chosen queries.
- **Time:** usually counted in encryptions of the cipher.
- **Memory:** the storage that the attack needs.

An [exhaustive key search](/exhaustive-key-search/) on a $k$-bit key costs about $2^k$ encryptions, a few known pairs and almost no memory. An attack on a cipher counts as an academic break if it is cheaper than exhaustive search in this sense, even if it is far from practical. Attacks often trade one resource for another: a [meet-in-the-middle attack](/meet-in-the-middle-attack/) on double encryption with two 56-bit keys takes about $2^{57}$ encryptions but $2^{56}$ words of memory, instead of $2^{112}$ encryptions.

## Examples

- **Classical cryptanalysis.** [Frequency analysis](/frequency-analysis/) breaks substitution ciphers in the ciphertext-only model. The [Kasiski examination](/kasiski-examination/) and the [index of coincidence](/index-of-coincidence/) find the period of the [Vigenère cipher](/vigenere-cipher/), which then splits into shift ciphers. These are total breaks with little data. The page on [cipher breaking](/cipher-breaking/) describes the common method.
- **Known plaintext.** A few known letters give the key of the [Hill cipher](/hill-cipher/) by linear algebra. Guessed plaintext, the cribs, made the bombe searches against the [Enigma machine](/enigma-machine/) possible.
- **Linear cryptanalysis of DES.** Matsui's attack of 1993 needed about $2^{47}$ known plaintexts; his improved version of 1994 recovers the key of the [Data Encryption Standard](/data-encryption-standard/) from about $2^{43}$ known plaintexts, faster than exhaustive search of its $2^{56}$ keys. It is a total break in the known-plaintext model, with a large data cost.
- **Differential cryptanalysis of DES.** Biham and Shamir's attack needs about $2^{47}$ chosen plaintexts: a chosen-plaintext attack, with a data cost that is hard to meet in practice.
- **Distinguishers.** Many attacks on reduced versions of the [AES](/advanced-encryption-standard/) start with a distinguisher for a few rounds and extend it into a key recovery for one or two more rounds.

## Where it is used

- **Design and standards.** New ciphers are published and attacked for years before they are trusted. The number of rounds of a block cipher is set with a margin above the best known attacks.
- **Security definitions.** The attack models above are the basis of the formal definitions, and a proof of security says that no efficient attacker in a given model reaches a given goal.
- **History.** Code breaking shaped both World Wars, from the solution of field ciphers to the work on Enigma at Bletchley Park.
- **Teaching.** Classical ciphers are the simplest place to see the attack models, the role of redundancy in language, and the cost of a search.

## References
