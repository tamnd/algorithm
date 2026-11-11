---
tag: CZPQ1B
kind: algorithm
slug: caesar-cipher
name: Caesar cipher
aliases:
- shift cipher
area: cryptography/symmetric-ciphers
level: intro
summary: Shift each letter by a fixed key k modulo 26. Suetonius says Caesar used k = 3. With only 26 keys, a search of all shifts with a score of English breaks it at once.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {n: the number of characters of the message}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
prereqs: [symmetric-encryption, congruence]
see_also: [affine-cipher, substitution-cipher, vigenere-cipher, frequency-analysis, exhaustive-key-search, ciphertext-only-attack, cipher-breaking, kerckhoffs-principle]
sources:
  - url: "https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Suetonius/12Caesars/Julius*.html"
    title: Suetonius, The Lives of the Caesars, The Deified Julius, translated by J. C. Rolfe (Loeb Classical Library, 1913), on the LacusCurtius site
    locator: Chapter 56, paragraph 6 (D written for A)
  - book: isbn:9780684831305
    title: David Kahn, The Codebreakers, revised edition, Scribner, 1996
    locator: Chapter 2 (the cipher of Julius Caesar and of Augustus)
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Section 1.3 (the shift cipher and its brute-force attack)
  - book: isbn:9781138197015
    title: Douglas R. Stinson and Maura B. Paterson, Cryptography, Theory and Practice, fourth edition, CRC Press, 2018
    locator: Section 2.1.1 (the shift cipher) and Table 2.1 (letter probabilities of Beker and Piper)
---

The Caesar cipher replaces each letter by the letter $k$ places later in the alphabet, and wraps from Z back to A. It is the simplest [symmetric encryption](/symmetric-encryption/) scheme: the key is one number $k \in \{0, \ldots, 25\}$, and both parties use it. Suetonius reports that Julius Caesar used $k = 3$, so that D stands for A. The general shift cipher has only 26 keys, so an attacker who sees only the ciphertext tries each key and keeps the decryption that looks most like English: an [exhaustive key search](/exhaustive-key-search/) of 26 steps.

## In plain words

Write the alphabet in a ring. To lock a message, move each letter a fixed number of steps forward on the ring. With three steps, A becomes D, B becomes E, and Y becomes B. To unlock, move each letter the same number of steps back. The secret is only the number of steps.

There are only 26 different step sizes, and one of them does nothing. An attacker can try all of them in a moment. Only one of the 26 results reads like English, so the attacker spots it at once. A program can do the same check: it counts the letters of each result and keeps the result whose counts are closest to the counts of normal English text.

## The problem

Identify the letters A to Z with the numbers $0$ to $25$, and work in $\mathbb{Z}_{26}$, the integers [modulo](/congruence/) 26. The key space is $\mathcal{K} = \mathbb{Z}_{26}$, and the message and ciphertext spaces are strings over $\mathbb{Z}_{26}$. For a key $k$,

$$E_k(p_1 \ldots p_n) = c_1 \ldots c_n, \quad c_i = (p_i + k) \bmod 26, \qquad D_k(c_1 \ldots c_n) = p_1 \ldots p_n, \quad p_i = (c_i - k) \bmod 26.$$

The code on this page shifts upper and lower case letters and copies every other character unchanged. A sender and a receiver share $k$; this is an instance of the [symmetric encryption](/symmetric-encryption/) problem. The attack problem is to find $k$, or the plaintext, from the ciphertext alone: a [ciphertext-only attack](/ciphertext-only-attack/).

## The algorithm

```pseudo id=main
CAESAR-ENCRYPT(P, k)                       ▷ P = p1 ... pn, each pi in 0 .. 25
L1  for i ← 1 to n do
L2      ci ← (pi + k) mod 26
L3  return C = c1 ... cn
```

Decryption is CAESAR-ENCRYPT with the key $-k$. The attack decrypts with each key and scores each result with Pearson's chi-squared statistic against a table $f$ of English letter probabilities:

```pseudo id=break
CAESAR-BREAK(C)
L4  for k ← 0 to 25 do
L5      P ← CAESAR-ENCRYPT(C, −k)
L6      Nj ← the number of letters j in P, for j = 0 .. 25; N ← |P|
L7      score[k] ← Σj (Nj − N fj)² / (N fj)
L8  return the keys sorted by score, smallest first
```

A small score means that the letter counts of $P$ are close to those of English. The code uses the probabilities of Beker and Piper, as printed in Stinson and Paterson (Table 2.1), and the same table is used on every classical cipher page of this site. The [frequency analysis](/frequency-analysis/) page explains the statistic.

The code is for study only. It is not constant time, and the cipher gives no protection at all. To protect real data, use an authenticated cipher such as AES-GCM or ChaCha20-Poly1305 from libsodium, from a FIPS 140 validated module, or from the standard library of your language.

## Example

**Encryption.** With Caesar's key $k = 3$, the message VENI VIDI VICI becomes YHQL YLGL YLFL.

| plaintext letter | V | E | N | I | D | C |
|---|---|---|---|---|---|---|
| number $p$ | 21 | 4 | 13 | 8 | 3 | 2 |
| $(p + 3) \bmod 26$ | 24 | 7 | 16 | 11 | 6 | 5 |
| ciphertext letter | Y | H | Q | L | G | F |

**Brute force.** Take the first 40 letters of the Declaration of Independence, WHENINTHECOURSEOFHUMANEVENTSITBECOMESNEC, and encrypt them with $k = 3$. The ciphertext is ZKHQLQWKHFRXUVHRIKXPDQHYHQWVLWEHFRPHVQHF. CAESAR-BREAK scores the 26 decryptions. The four best scores and the score of the key 0 (no decryption) are:

| key $k$ | 3 | 4 | 9 | 2 | 0 |
|---|---|---|---|---|---|
| chi-squared score | 19.0 | 119.4 | 156.3 | 163.7 | 821.7 |

The true key wins by a factor of more than 6. On the full 499-letter sample, the chi-squared search finds each of the 26 keys.

**A text that is too short.** CHEER shifted by 7 is JOLLY. Both are English words, so no score can tell from the five letters JOLLY whether the key was 0 or 7. The chi-squared search ranks the key 7 first, because CHEER has more common letters.

## Correctness

**Decryption inverts encryption.** For each letter, $((p + k) \bmod 26 - k) \bmod 26 = p$, because addition modulo 26 is a group operation with inverse $-k$. So $D_k(E_k(P)) = P$ for each key and each message.

**The search finds the plaintext among its candidates.** The true key $k_0$ is one of the 26 keys, so the list of CAESAR-BREAK holds $D_{k_0}(C) = P$. The score only orders the candidates. The true key is ranked first when $P$ has the smallest chi-squared score of the 26 shifts of $P$. This holds for each key on the sample texts of the tests, but it is a property of the text, not a theorem: the CHEER example shows that it can fail. The full proof of the two facts, and of the fact that the 26 keys give 26 different maps, is in the proof file below.

## Complexity

CAESAR-ENCRYPT runs the loop of line L1 $n$ times, and each pass does one addition and one reduction modulo 26. So encryption and decryption take $\Theta(n)$ time in each case on the [word RAM](/word-ram/), with $\Theta(1)$ extra space beyond the output.

CAESAR-BREAK runs 26 decryptions and 26 counts, each in $\Theta(n)$ time, and the sum of line L7 has 26 terms. So the attack takes $26 \cdot \Theta(n) = \Theta(n)$ time. The key space has $\lg 26 \approx 4.7$ bits of entropy, which is why the search is trivial.

| claim | value |
|---|---|
| encryption, worst, average and best | $\Theta(n)$ |
| extra space | $\Theta(1)$ |
| brute-force attack | 26 decryptions, $\Theta(n)$ |

## Properties

- **Deterministic.** The same key and message give the same ciphertext, so equal letters give equal ciphertext letters. This keeps the letter frequencies, shifted.
- **A group of keys.** Encrypting with $k_1$ and then with $k_2$ is encrypting with $k_1 + k_2$. Encrypting twice adds no security.
- **Monoalphabetic.** Each plaintext letter always maps to the same ciphertext letter. The Caesar cipher is the special case $a = 1$ of the [affine cipher](/affine-cipher/) and a special case of the [substitution cipher](/substitution-cipher/).
- **Keeps the length.** The code also copies spaces and signs, so the ciphertext shows the word lengths. Classical practice removed the spaces or wrote the text in groups of five letters.

## Variants and improvements

- **ROT13.** The shift by 13. Because $13 + 13 = 26$, encryption and decryption are the same map. It hides text from a casual reader, not from an attacker.
- **The affine cipher** maps $x$ to $ax + b \bmod 26$ and has 312 keys. See [affine cipher](/affine-cipher/).
- **The general substitution cipher** uses any permutation of the alphabet, with $26!$ keys. See [substitution cipher](/substitution-cipher/).
- **The Vigenère cipher** uses a different Caesar shift for each position, in a cycle given by a keyword. See [Vigenère cipher](/vigenere-cipher/).
- **The one-time pad** on letters is a Caesar shift with a new random key for each letter. It has [perfect secrecy](/perfect-secrecy/). See [one-time pad](/one-time-pad/).

## When to use it

Use it to teach the parts of a cipher (key, encryption, decryption) and the first attack, the search of all keys. Never use it to protect data. It also shows why [Kerckhoffs's principle](/kerckhoffs-principle/) matters: once the method is known, a key space of 26 is no secret at all.

## Pitfalls

- **Negative remainders.** In C, Java and Go, `(c - k) % 26` is negative when `c < k`. Write `((c - k) % 26 + 26) % 26`. Python's `%` is always non-negative. The test `test_edges` checks the shift by $-1$ of `abc`.
- **Mixed case and other characters.** A shift of `ord(ch)` on the full character set changes digits and spaces. Shift only the ranges A to Z and a to z. The test `test_edges` checks a string of digits and signs.
- **Trusting the best score on short text.** The best score is a guess. CHEER and JOLLY differ by a shift of 7, so five letters can not fix the key (test `test_short_text_is_ambiguous`). Read the top few candidates, or use more ciphertext.
- **A key of 0 or 26.** These keys leave the text unchanged. A key generator must not pick them, but the attack must still try them.

## Implementations

## History

Suetonius writes, in his life of Julius Caesar (chapter 56), that Caesar wrote confidential letters by putting the fourth letter of the alphabet, D, in place of A, and so on for the other letters. In his life of Augustus he says that Augustus used a shift of one place. Kahn's history gives these passages and the later use of shift ciphers. Modern textbooks, for example Katz and Lindell and Stinson and Paterson, use the general shift cipher as the first example of a cipher that falls to a search of all keys.

## References
