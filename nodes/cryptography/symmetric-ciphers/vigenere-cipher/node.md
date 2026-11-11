---
tag: 11VG96
kind: algorithm
slug: vigenere-cipher
name: Vigenère cipher
aliases:
area: cryptography/symmetric-ciphers
level: intro
summary: A periodic polyalphabetic cipher. Letter j gets the Caesar shift of key letter j mod m. Kasiski and the index of coincidence find m, then each column falls to frequency analysis.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {n: the number of characters of the message, m: the number of letters of the key}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(m)}
properties: {deterministic: true}
prereqs: [caesar-cipher]
see_also: [kasiski-examination, index-of-coincidence, frequency-analysis, substitution-cipher, one-time-pad, ciphertext-only-attack, cipher-breaking]
sources:
  - book: isbn:9781138197015
    title: Douglas R. Stinson and Maura B. Paterson, Cryptography, Theory and Practice, fourth edition, CRC Press, 2018
    locator: Section 2.1.4 (the Vigenère cipher) and Section 2.2.3 (its cryptanalysis by the Kasiski test and the index of coincidence)
  - book: isbn:9780684831305
    title: David Kahn, The Codebreakers, revised edition, Scribner, 1996
    locator: the chapters on the Renaissance cipher writers (Alberti, Trithemius, Bellaso, Vigenère) and on Kasiski
  - book: isbn:9780385495318
    title: Simon Singh, The Code Book, Anchor Books, 2000
    locator: Chapter 2, Le Chiffre Indéchiffrable (the Vigenère cipher, Babbage and Kasiski)
  - paper: "Friedrich W. Kasiski, Die Geheimschriften und die Dechiffrir-Kunst, E. S. Mittler und Sohn, Berlin, 1863"
    locator: the method of repeated sequences for ciphers with a periodic key
  - paper: "William F. Friedman, The Index of Coincidence and Its Applications in Cryptography, Riverbank Publication No. 22, Riverbank Laboratories, Geneva, Illinois, 1922"
    locator: the index of coincidence as a test for the number of alphabets
---

The Vigenère cipher encrypts with a keyword of $m$ letters. The $j$-th letter of the message gets the [Caesar](/caesar-cipher/) shift of the key letter at position $j \bmod m$, so the cipher uses $m$ alphabets in a cycle. It is a *periodic polyalphabetic* cipher. Giovan Battista Bellaso described it in 1553; it was later credited to Blaise de Vigenère, whose own 1586 cipher was the stronger *autokey* variant. For three centuries it had a name as "le chiffre indéchiffrable". It is not: once the period $m$ is known, the ciphertext splits into $m$ Caesar ciphers, and [Kasiski examination](/kasiski-examination/) and the [index of coincidence](/index-of-coincidence/) both find $m$.

## In plain words

Pick a keyword, for example LEMON. Write it again and again under the message. Each letter of the keyword says how far to move the letter above it in the alphabet: A means do not move, B means move one place, L means move eleven places. The same message letter can now turn into different cipher letters, so a simple letter count no longer shows the message.

The weakness is the repeat. With a keyword of five letters, every fifth letter is moved by the same amount. If a code breaker guesses that the keyword has five letters, they take every fifth letter and get a simple shift cipher, which falls to a letter count. They can find the length of the keyword from repeated pieces of ciphertext or from how often letters match.

## The problem

Identify A to Z with $\mathbb{Z}_{26}$. A key is a word $k = k_0 k_1 \ldots k_{m-1}$ over $\mathbb{Z}_{26}$, and $m$ is the *period*. For a message $p_0 p_1 \ldots p_{n-1}$:

$$c_j = (p_j + k_{j \bmod m}) \bmod 26, \qquad p_j = (c_j - k_{j \bmod m}) \bmod 26.$$

The key space for period $m$ has $26^m$ keys. The code keeps the case of each letter and copies other characters; only letters use up key letters, so $j$ counts letters. This is an instance of [symmetric encryption](/symmetric-encryption/). The attack problem is a [ciphertext-only attack](/ciphertext-only-attack/): find $k$ from $c$ when $p$ is English.

## The algorithm

```pseudo id=main
VIGENERE-ENCRYPT(P, k)                     ▷ k = k0 ... k(m-1), j counts the letters
L1  for each character x of P, with j ← 0 at the start do
L2      if x is a letter then
L3          output (x + k[j mod m]) mod 26
L4          j ← j + 1
L5  return the output, with each other character copied
```

Decryption subtracts the key letter instead of adding it. The classical attack has two stages.

```pseudo id=break
VIGENERE-BREAK(C, P_max)
L6  for m ← 1 to P_max do
L7      split the letters of C into the m columns C_i = c_i c_(i+m) c_(i+2m) ...
L8      I(m) ← the mean of the index of coincidence of C_0, ..., C_(m-1)
L9  m ← the smallest m with I(m) ≥ 0.85 · max I
L10 for i ← 0 to m - 1 do
L11     k_i ← the shift s that makes C_i - s closest to English (smallest chi-squared)
L12 return k_0 ... k_(m-1)
```

Each column $C_i$ is a Caesar cipher with shift $k_i$, so its index of coincidence is that of English, about $0.066$. A wrong $m$ mixes several shifts in one column and the index falls toward $1/26 \approx 0.038$. Multiples of the true period also give large values, which is why line L9 takes the smallest good $m$. The factor $0.85$ is a heuristic choice. Line L11 is [frequency analysis](/frequency-analysis/) of one Caesar cipher with the chi-squared score, as on the [Caesar cipher](/caesar-cipher/) page.

The code is for study only. It is not constant time, and the cipher gives no protection. To protect real data, use AES-GCM or ChaCha20-Poly1305 from libsodium, from a FIPS 140 validated module, or from the standard library of your language.

## Example

**Encryption.** With the key LEMON, ATTACKATDAWN becomes LXFOPVEFRNHR:

| plaintext | A | T | T | A | C | K | A | T | D | A | W | N |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| key | L | E | M | O | N | L | E | M | O | N | L | E |
| shift | 11 | 4 | 12 | 14 | 13 | 11 | 4 | 12 | 14 | 13 | 11 | 4 |
| ciphertext | L | X | F | O | P | V | E | F | R | N | H | R |

The two T letters at positions 1 and 2 give X and F, and the A letters give L, O, E and N. The autokey variant with the primer QUEENLY uses the key QUEENLYATTAC (the primer, then the plaintext), and gives QNXEPVYTWTWP.

**The attack.** Encrypt the 499 letters of the first two sentences of the Declaration of Independence with LEMON. The plaintext has an index of coincidence of $0.0747$; the ciphertext has $0.0434$, close to the uniform value. The mean column index for each trial period:

| $m$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $I(m)$ | .0434 | .0427 | .0429 | .0419 | .0736 | .0444 | .0436 | .0437 | .0409 | .0719 | .0434 | .0444 |

Only $m = 5$ and its multiple $10$ stand out, so $m = 5$. Friedman's formula, derived on the [index of coincidence](/index-of-coincidence/) page, gives the rough estimate $5.47$ from the whole text. For each of the five columns of about 100 letters, the best and the second best shifts have chi-squared values of 27.5 (L) against 297.0, 21.0 (E) against 309.6, 31.7 (M) against 363.8, 54.5 (O) against 353.2, and 18.0 (N) against 369.5. The key LEMON comes out with a wide margin. The [Kasiski examination](/kasiski-examination/) page attacks the same ciphertext through repeated trigrams.

For 120 random keys of length 1 to 12 on the same text, the attack recovers a key that decrypts the whole text each time; the test asks for at least 95%. In a larger trial it failed on a few keys with repeated letters, such as GRR, where two of the three columns share a shift and a wrong period looks almost as good as the right one.

## Correctness

**Encryption.** For the $j$-th letter, decryption computes $((p_j + k_{j \bmod m}) - k_{j \bmod m}) \bmod 26 = p_j$, because both runs use the same counter $j$: it counts letters, and other characters are copied in both runs. So decryption inverts encryption. For the autokey variant, the key letter at position $j \ge m$ is the plaintext letter $p_{j-m}$, which the decryption has already recovered, so an induction on $j$ gives the same result.

**The attack.** Fix $m$ equal to the period. The column $C_i$ holds the letters $c_j$ with $j \equiv i \pmod m$, and each of them is $p_j + k_i$. So $C_i$ is the Caesar encryption with shift $k_i$ of a part of the plaintext, and subtracting the right $s$ gives English text. The attack is a heuristic, because both the choice of $m$ in line L9 and the choice of $s$ in line L11 rely on statistics, which can fail on short or unusual texts. The full proof of the encryption claims is in the proof file below.

## Complexity

Encryption and decryption do one addition modulo 26 per character, so they take $\Theta(n)$ time in each case and $\Theta(m)$ extra space for the key. The attack computes $P_{\max}$ mean indices, each in $\Theta(n)$ time, and then tries 26 shifts for each column, each in time linear in the column length, which is $\Theta(26 n)$ in total. So the attack takes $\Theta(n \cdot P_{\max})$ time.

| claim | value |
|---|---|
| encryption and decryption, each case | $\Theta(n)$ |
| keys of period $m$ | $26^m$ |
| attack with periods up to $P_{\max}$ | $\Theta(n \cdot P_{\max})$ time, $\Theta(n)$ space |

## Properties

- **Periodic.** Letters $m$ apart use the same shift. This is the leak that every classical attack uses.
- **Flatter counts.** The letter counts of the ciphertext are a mixture of $m$ shifted copies of the English counts, so they are flatter than English, and the index of coincidence is lower.
- **Repeats survive when they line up.** The same plaintext piece at two positions whose distance is a multiple of $m$ gives the same ciphertext piece. Kasiski's method rests on this.
- **The key length matters, but only up to a point.** If the key is random and as long as the message and is never used again, the cipher becomes the [one-time pad](/one-time-pad/), which has [perfect secrecy](/perfect-secrecy/).

## Variants and improvements

- **Autokey.** Vigenère's own cipher: after a short primer, the plaintext is the key. The key does not repeat, so the period attack does not apply. It still falls, because the key is English text: a guess at a key piece gives a plaintext piece that must also be English.
- **Running key.** The key is a long text, such as a page of a book. It is broken by the same idea as the autokey, because both texts have the statistics of English.
- **Beaufort and variant Beaufort.** Use $c = k - p$ or $c = p - k$. The attacks are the same.
- **Gronsfeld.** The key is a string of digits, so only shifts 0 to 9 are used.
- **Mixed alphabets.** Each of the $m$ alphabets is a full [substitution](/substitution-cipher/) instead of a shift. The period attack still finds $m$, and each column falls to frequency analysis.

## When to use it

Use it to teach polyalphabetic ciphers, the index of coincidence and Kasiski examination. Never use it to protect data.

## Pitfalls

- **Advancing the key on spaces and punctuation.** Implementations differ; the code here uses a key letter only for letters, and the two ends must agree.
- **Taking a multiple of the period.** The period $2m$ also gives a high index and recovers the key LEMONLEMON. It decrypts correctly, but it doubles the work and halves the column length. Take the smallest good $m$.
- **Short texts.** With few letters per column, both the index and the chi-squared choice become noisy. Rule of thumb: the attack needs a few dozen letters per column.
- **Keys with repeated letters.** A key such as GRR can make a wrong period look right, as in the example.

## Implementations

## History

Leon Battista Alberti described a cipher disk with a changing alphabet around 1467, and Johannes Trithemius gave the square table of all shifts, the tabula recta, in his Polygraphia (1518). Giovan Battista Bellaso published the cipher with a keyword in 1553, in "La cifra del Sig. Giovan Battista Bellaso". Blaise de Vigenère described the stronger autokey cipher in his "Traicté des chiffres" (1586), but the periodic keyword cipher came to carry his name; Kahn tells the history of this misattribution. Charles Babbage broke ciphers of this type in the 1850s, according to Kahn and Singh, but did not publish his method. Friedrich Kasiski published the first general solution in 1863, in "Die Geheimschriften und die Dechiffrir-Kunst". William Friedman introduced the index of coincidence in 1922, in Riverbank Publication No. 22, which gave a statistical test for the period.

## References
