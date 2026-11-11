---
tag: K0CNG3
kind: algorithm
slug: one-time-pad
name: One-time pad
aliases:
- Vernam cipher
area: cryptography/symmetric-ciphers
level: intro
summary: XOR the message with a uniformly random key of the same length, used only once. Shannon proved it perfectly secret; a reused key or a changed ciphertext breaks it.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {n: the number of bytes of the message}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true}
prereqs: [symmetric-encryption]
see_also: [perfect-secrecy, shannon-perfect-secrecy-theorem, vigenere-cipher, stream-cipher, pseudorandom-generator, true-random-number-generator, known-plaintext-attack, cryptanalysis]
sources:
  - paper: "Gilbert S. Vernam, Secret signaling system, US Patent 1,310,719, granted 22 July 1919"
    locator: the claims and description of the system that combines each character of the message with a character of a key tape
  - paper: doi:10.1002/j.1538-7305.1949.tb00928.x
    title: Claude E. Shannon, Communication theory of secrecy systems, Bell System Technical Journal 28(4), 1949, pp. 656-715
    locator: Part II, the section on perfect secrecy (the proof that a random key as long as the message, used once, gives perfect secrecy)
  - paper: doi:10.1080/01611194.2011.583711
    title: Steven M. Bellovin, Frank Miller, inventor of the one-time pad, Cryptologia 35(3), 2011, pp. 203-222
    locator: the account of Miller's telegraph code book of 1882 and its one-time key
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Section 2.2 (the one-time pad and the proof of its perfect secrecy)
  - book: isbn:9780684831305
    title: David Kahn, The Codebreakers, revised edition, Scribner, 1996
    locator: the account of Vernam's teleprinter cipher and of Mauborgne's random key that is never repeated
  - paper: "John Earl Haynes and Harvey Klehr, Venona, Decoding Soviet Espionage in America, Yale University Press, 1999"
    locator: the opening chapter on the Venona project and the duplicated one-time pad pages that made the decryptions possible
---

The one-time pad encrypts a message by adding a key of the same length to it, letter by letter or bit by bit. On bytes, the addition is the exclusive or (XOR): $c = m \oplus k$, and decryption is $m = c \oplus k$. If the key is uniformly random, as long as the message, secret, and never used again, then the ciphertext gives no information at all about the message, even to an attacker with unlimited computing power. Shannon proved this in 1949: the one-time pad has [perfect secrecy](/perfect-secrecy/). His [theorem](/shannon-perfect-secrecy-theorem/) also shows that no cipher can do this with a shorter key. The pad is fragile in use: a key used twice leaks the XOR of two messages, which falls to crib dragging, and anyone can flip bits of the ciphertext to change the message in a known way.

## In plain words

Two people share a long list of random numbers, the pad. To send a message, the sender adds the next unused numbers of the pad to the letters of the message, one number for each letter, and then destroys those numbers. The receiver subtracts the same numbers and gets the message.

Because each number is random, each cipher letter could stand for any letter. A code breaker who sees the ciphertext learns nothing about the message except its length.

The rules are strict. The pad must be truly random, as long as all the messages, kept secret, and used only once. If a page is used twice, a code breaker can put the two messages against each other and read them. And the pad does not stop someone from changing the message on the way.

## The problem

Let messages, keys and ciphertexts be strings of $n$ bytes, $\mathcal{M} = \mathcal{K} = \mathcal{C} = \{0, 1\}^{8n}$. The key generator picks $k$ uniformly from $\mathcal{K}$. Encryption is $\mathrm{Enc}_k(m) = m \oplus k$ and decryption is $\mathrm{Dec}_k(c) = c \oplus k$. This is a [symmetric encryption](/symmetric-encryption/) scheme. The security goal is perfect secrecy: for every distribution of the message $M$, every message $m$ and every ciphertext $c$ with $\Pr[C = c] > 0$,
$$\Pr[M = m \mid C = c] = \Pr[M = m].$$

## The algorithm

```pseudo id=main
ONE-TIME-PAD(m)                            ▷ m has n bytes
L1  k ← n bytes from a true random source; never use them again
L2  for i ← 0 to n - 1 do
L3      c[i] ← m[i] ⊕ k[i]
L4  return (k, c)                          ▷ decryption: m[i] ← c[i] ⊕ k[i]
```

The attack on a reused key uses only XOR. If $c_1 = m_1 \oplus k$ and $c_2 = m_2 \oplus k$, then $x = c_1 \oplus c_2 = m_1 \oplus m_2$: the key cancels.

```pseudo id=drag
CRIB-DRAG(x, w)                            ▷ x = c1 ⊕ c2, w a guessed word
L5  for each offset i from 0 to |x| - |w| do
L6      f ← x[i .. i + |w|) ⊕ w
L7      if f consists of letters and spaces then report (i, f)
L8  return the reports
```

If the word $w$ is in one message at offset $i$, then $f$ is the text of the other message at the same offset. The code breaker keeps the fragments that read as language, guesses longer words around them, and XORs those guesses with $x$ to read more of the other message, back and forth.

The code is for study only. It is not constant time, the pad gives no integrity, and key handling is the hard part in practice. To protect real data, use AES-GCM or ChaCha20-Poly1305 from libsodium, from a FIPS 140 validated module, or from the standard library of your language.

## Example

**Encryption.** The message HELLO is the bytes 48 45 4C 4C 4F in hexadecimal. With the key 58 4D 43 4B 59, the ciphertext is

| | H | E | L | L | O |
|---|---|---|---|---|---|
| $m$ | 48 | 45 | 4C | 4C | 4F |
| $k$ | 58 | 4D | 43 | 4B | 59 |
| $c = m \oplus k$ | 10 | 08 | 0F | 07 | 16 |

and XOR with the same key gives HELLO back. For any other message of five bytes, there is exactly one key that gives the same ciphertext, so the ciphertext alone rules out no message.

**A key used twice.** Encrypt two public domain sentences of 71 bytes with the same key: $m_1$ = "We hold these truths to be self-evident, that all men are created equal" and $m_2$ = "Four score and seven years ago our fathers brought forth on this contin". The attacker computes $x = c_1 \oplus c_2 = m_1 \oplus m_2$.

1. Dragging the word " and " gives two offsets where the result is letters and spaces: offset 10 with "ese t" and offset 26 with " slgf". The first looks like English.
2. Guess that "ese t" is part of "hold these truths" in $m_1$ at offset 3. XOR with $x$ gives "r score and seven" in $m_2$.
3. Dragging " that " gives one hit, "rs bro" at offset 40. Guess "fathers brought forth" in $m_2$ at offset 35; XOR gives "dent, that all men ar" in $m_1$.

A few more guesses give both messages, and then $c_1 \oplus m_1$ gives the key. The attack never touches the key; it works on the redundancy of language.

**Malleability.** A ciphertext of "PAY ALICE 0100 DOLLARS" is changed by an attacker who knows the format but not the key: XOR the bytes at offset 10 with "0100" ⊕ "9900". The receiver decrypts "PAY ALICE 9900 DOLLARS". The one-time pad hides the message but does not protect it from change; real systems add a message authentication code.

**Perfect secrecy by enumeration.** Take 2-bit messages with the prior $\Pr[M] = (1/2, 1/4, 1/8, 1/8)$ on 00, 01, 10, 11. With all four keys uniform, the exact posterior $\Pr[M = m \mid C = c]$ equals the prior for every $c$. With only the keys 00 and 11, the ciphertext 00 leaves the messages 00 and 11, with posterior $4/5$ and $1/5$: secrecy fails. On 3-bit messages with a prior that gives every message a positive probability, the code checks all 255 nonempty key sets: the XOR cipher is perfectly secret exactly for the full set of 8 keys. Every smaller key set fails, as Shannon's bound $\lvert \mathcal{K} \rvert \ge \lvert \mathcal{M} \rvert$ requires.

## Correctness

Decryption works because $(m \oplus k) \oplus k = m$. Perfect secrecy holds because, for every message $m$ and ciphertext $c$, exactly one key, $k = m \oplus c$, maps $m$ to $c$, so $\Pr[C = c \mid M = m] = 2^{-8n}$ for every $m$. The ciphertext then has the same distribution whatever the message is, and Bayes' rule gives back the prior. The full proof, and the proofs of the two attacks, are in the proof file below.

## Complexity

Encryption and decryption take $\Theta(n)$ time. The key takes $\Theta(n)$ space, and by [Shannon's theorem](/shannon-perfect-secrecy-theorem/) no perfectly secret cipher can use fewer key bits than the message has, in the sense of entropy. This is the real cost of the pad: the key must be made, carried to the receiver and stored securely, and it is used up as fast as the messages.

| claim | value |
|---|---|
| encryption and decryption | $\Theta(n)$ |
| key length | $n$ bytes, for every message, never reused |
| CRIB-DRAG for a word of $w$ bytes | $\Theta(\lvert x \rvert \cdot w)$ |

## Properties

- **Perfect secrecy.** The ciphertext is independent of the message. The proof needs no assumption about the computing power of the attacker.
- **Every message is possible.** For each ciphertext and each message of the same length, one key links them. This also means that a known plaintext reveals the key of that message, and nothing else.
- **Malleability.** $\mathrm{Enc}_k(m) \oplus \delta = \mathrm{Enc}_k(m \oplus \delta)$. An attacker can change known parts of the message.
- **Reuse is fatal.** Two ciphertexts under one key give $m_1 \oplus m_2$, and natural language has enough redundancy to split this into $m_1$ and $m_2$.
- **The length is not hidden.** The ciphertext has the length of the message.

## Variants and improvements

- **Letters.** On the 26 letters, add the key modulo 26. This is a [Vigenère cipher](/vigenere-cipher/) with a random key as long as the message, and it has perfect secrecy for the same reason.
- **Code books with additive pads.** Diplomatic and spy systems encoded the message into numbers with a code book and then added a pad of random digits modulo 10.
- **Stream ciphers.** A [stream cipher](/stream-cipher/) replaces the random key by the output of a [pseudorandom generator](/pseudorandom-generator/) on a short key. It gives up perfect secrecy for computational security, and it has the same weakness under key and nonce reuse.
- **Authentication.** A one-time message authentication code, with its own random key, protects against change, and also keeps information-theoretic security.

## When to use it

Use it to teach perfect secrecy, the key length bound, and why practical cryptography uses computational security instead. Real uses, such as some diplomatic and military links, need secure transport of large amounts of key material, which is the reason the pad is rare.

## Pitfalls

- **Reusing the pad.** Even a partial reuse leaks the XOR of the two messages. The Soviet pads behind VENONA are the famous case.
- **Weak randomness.** A key from a predictable generator is not a one-time pad. Perfect secrecy needs keys that are uniform and independent of everything else.
- **Short keys.** A key shorter than the message must repeat or be stretched, and then the scheme is a Vigenère cipher or a stream cipher, without perfect secrecy.
- **No integrity.** The pad hides the message but does not stop an attacker from changing it.
- **Known plaintext.** Knowing the plaintext gives the key of that message. This is harmless only if the key is never used again.

## Implementations

## History

Gilbert Vernam, an engineer at AT&T, built a teleprinter cipher in 1917 that added a key tape to the message tape, character by character, with the exclusive or of the five bit Baudot code. He received US Patent 1,310,719 in 1919. His first key was a loop of tape that repeated. Joseph Mauborgne of the US Army Signal Corps saw that the key had to be random and never repeated, and that idea made the system a one-time pad, according to Kahn. In 2011 Steven Bellovin showed that Frank Miller, a banker from Sacramento, had described a one-time pad in a telegraph code book of 1882, so the idea is older than Vernam's patent. Claude Shannon proved perfect secrecy in a report of 1945 that was published in 1949, and he proved that every perfectly secret cipher needs at least as many keys as messages. In the Second World War, Soviet agencies used code books with additive pads. In the early 1940s some pad pages were made twice, and the duplicates were used for different messages. From 1943 the US Army's Signal Intelligence Service collected this traffic, and the VENONA project found matching pages and read parts of a few thousand messages; the work was made public in 1995. VENONA is the standard historical case of a two-time pad.

## References
