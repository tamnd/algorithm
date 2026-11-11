---
tag: WCAD3J
kind: algorithm
slug: affine-cipher
name: Affine cipher
area: cryptography/symmetric-ciphers
level: intro
summary: Map each letter x to a x + b mod 26, with gcd(a, 26) = 1, so there are 12 × 26 = 312 keys. Decryption multiplies by the inverse of a. Two known letter pairs give the key.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {n: the number of characters of the message}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
prereqs: [caesar-cipher, modular-inverse, greatest-common-divisor]
see_also: [extended-euclidean-algorithm, euler-totient, chinese-remainder-theorem, hill-cipher, substitution-cipher, known-plaintext-attack, frequency-analysis, exhaustive-key-search]
sources:
  - book: isbn:9781138197015
    title: Douglas R. Stinson and Maura B. Paterson, Cryptography, Theory and Practice, fourth edition, CRC Press, 2018
    locator: Section 2.1.3 (the affine cipher and the count of its keys) and Section 2.2.1 (cryptanalysis of the affine cipher)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 7, Section 7.3 (classical ciphers, simple substitution and its special cases)
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Section 1.3 (historical ciphers and their cryptanalysis)
---

The affine cipher encrypts each letter $x \in \mathbb{Z}_{26}$ as $E_{a,b}(x) = (ax + b) \bmod 26$, where the key $(a, b)$ has $\gcd(a, 26) = 1$. The condition makes $x \mapsto ax + b$ a bijection, and decryption is $D_{a,b}(y) = a^{-1}(y - b) \bmod 26$, with the [modular inverse](/modular-inverse/) of $a$. There are $12 \cdot 26 = 312$ keys, so a search of all keys breaks it. A [known-plaintext attack](/known-plaintext-attack/) needs only two letter pairs: two pairs whose plaintext letters do not differ by 0 or 13 fix the key exactly.

## In plain words

The [Caesar cipher](/caesar-cipher/) only slides the alphabet. The affine cipher first stretches it: it multiplies the position of each letter by a fixed number, wraps around the end of the alphabet, and then slides it. Not every stretch works. If the stretch number shares a factor with 26, two different letters land on the same place, and the receiver can not undo it. With a good stretch number, each letter has its own place, and the receiver undoes the slide and then the stretch.

There are 12 good stretch numbers and 26 slides, so 312 keys. A computer tries them all at once. And if an attacker knows two letters of the message and where they went, a little algebra gives the key.

## The problem

Identify A to Z with $0$ to $25$. The key space is

$$\mathcal{K} = \{(a, b) : a, b \in \mathbb{Z}_{26},\ \gcd(a, 26) = 1\},$$

and $|\mathcal{K}| = \varphi(26) \cdot 26 = 12 \cdot 26 = 312$, where $\varphi$ is [Euler's totient](/euler-totient/): the units of $\mathbb{Z}_{26}$ are $1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25$. A message $p_1 \ldots p_n$ is encrypted letter by letter, $c_i = (a p_i + b) \bmod 26$. This is an instance of [symmetric encryption](/symmetric-encryption/). The attack problems are to find $(a, b)$ from the ciphertext alone, or from a few known pairs $(p_i, c_i)$.

## The algorithm

```pseudo id=main
AFFINE-ENCRYPT(P, a, b)                    ▷ P = p1 ... pn, each pi in 0 .. 25
L1  if gcd(a, 26) ≠ 1 then error "a has no inverse"
L2  for i ← 1 to n do ci ← (a · pi + b) mod 26
    return C

AFFINE-DECRYPT(C, a, b)
L3  a′ ← a⁻¹ mod 26                         ▷ extended Euclidean algorithm
L4  for i ← 1 to n do pi ← a′ · (ci − b) mod 26
    return P
```

Line L3 computes the inverse with the [extended Euclidean algorithm](/extended-euclidean-algorithm/): it finds $s, t$ with $sa + 26t = \gcd(a, 26) = 1$, so $sa \equiv 1$. For $a = 5$ the inverse is $21$, because $5 \cdot 21 = 105 = 4 \cdot 26 + 1$.

The key recovery from two known pairs $(x_1, y_1)$ and $(x_2, y_2)$ subtracts the two equations:

```pseudo id=recover
AFFINE-RECOVER(x1, y1, x2, y2)
L5  Δx ← (x1 − x2) mod 26, Δy ← (y1 − y2) mod 26
L6  K ← empty list
L7  for each unit a of Z26 do
L8      if a · Δx ≡ Δy (mod 26) then append (a, (y1 − a · x1) mod 26) to K
L9  return K
```

When $\gcd(\Delta x, 26) = 1$, the loop can be replaced by $a = \Delta y \cdot (\Delta x)^{-1}$. The loop also handles $\Delta x = 2, 4, \ldots$, where $\Delta x$ has no inverse but the key is still unique (see the theorem below).

The code is for study only. It is not constant time, and the cipher gives no protection. To protect real data, use AES-GCM or ChaCha20-Poly1305 from libsodium, from a FIPS 140 validated module, or from the standard library of your language.

## Example

**Encryption.** With the key $(a, b) = (5, 8)$, AFFINE CIPHER becomes IHHWVC SWFRCP.

| letter | A | F | I | N | E | C | P | H | R |
|---|---|---|---|---|---|---|---|---|---|
| $x$ | 0 | 5 | 8 | 13 | 4 | 2 | 15 | 7 | 17 |
| $5x + 8 \bmod 26$ | 8 | 7 | 22 | 21 | 2 | 18 | 5 | 17 | 15 |
| cipher | I | H | W | V | C | S | F | R | P |

Decryption uses $5^{-1} = 21$: the letter C is $21 \cdot (2 - 8) = -126 \equiv 4$, which is E.

**Key recovery from a guess.** The first 60 letters of the Declaration of Independence under $(5, 8)$ give a ciphertext whose most common letters are C (12 times) and Z (4 times, after A, V and U). Guess that C is E and Z is T, so $(x_1, y_1) = (4, 2)$ and $(x_2, y_2) = (19, 25)$. Then $\Delta x = -15 \equiv 11$ and $\Delta y = -23 \equiv 3$. Since $11^{-1} = 19$ (as $11 \cdot 19 = 209 = 8 \cdot 26 + 1$), $a = 3 \cdot 19 = 57 \equiv 5$, and $b = 2 - 5 \cdot 4 = -18 \equiv 8$. The guess gives the true key. A wrong guess gives a key whose decryption is not English, and the attacker tries the next guess.

**Brute force.** The chi-squared search of all 312 keys on the same 60 letters ranks $(5, 8)$ first with the score 16.9. The next keys are $(23, 7)$ with 123.4 and $(17, 15)$ with 125.3.

**Two pairs that are not enough.** The pairs $(0, 8)$ and $(13, 21)$ have $\Delta x = 13$. All 12 units $a$ satisfy $13a \equiv 13 \pmod{26}$, so 12 keys $(a, 8)$ fit both pairs.

## Correctness

**Theorem.** (1) $E_{a,b}$ is a bijection of $\mathbb{Z}_{26}$ if and only if $\gcd(a, 26) = 1$, and then $D_{a,b}(E_{a,b}(x)) = x$. (2) Let $(x_1, y_1), (x_2, y_2)$ be two pairs of a key $(a, b)$, and let $\Delta x = x_1 - x_2 \bmod 26$. If $\Delta x \notin \{0, 13\}$, then $(a, b)$ is the only key that fits both pairs. If $\Delta x \in \{0, 13\}$, exactly 12 keys fit.

*Proof of (2).* A key $(a', b')$ fits both pairs exactly when $a' \Delta x \equiv \Delta y$ and $b' = y_1 - a' x_1$; so $b'$ is fixed by $a'$, and it is enough to count the units $a'$ with $a' \Delta x \equiv a \Delta x \pmod{26}$, that is, $(a' - a)\Delta x \equiv 0$. By the [Chinese remainder theorem](/chinese-remainder-theorem/), this holds modulo 26 if and only if it holds modulo 2 and modulo 13. Each unit is odd, so $a' - a$ is even and the condition modulo 2 always holds. If $13 \nmid \Delta x$, then $\Delta x$ is a unit modulo 13, so $a' \equiv a \pmod{13}$; together with $a' \equiv a \equiv 1 \pmod 2$ this gives $a' = a$. If $13 \mid \Delta x$, that is $\Delta x \in \{0, 13\}$, the condition holds for all 12 units. $\square$

The case $\Delta x$ even and nonzero is the one that a quick reading gets wrong: $\Delta x$ has no inverse modulo 26, but the key is still unique, because the parity of $a$ is known. The full proof of both parts is in the proof file below.

## Complexity

Line L1 runs the Euclidean algorithm on numbers below 26, which is $O(1)$ steps. The loop of line L2 does one multiplication, one addition and one reduction for each letter. So encryption and decryption take $\Theta(n)$ time in each case on the [word RAM](/word-ram/) and $\Theta(1)$ extra space. AFFINE-RECOVER tries at most 12 units, so it takes $O(1)$ time. The search of all keys takes $312 \cdot \Theta(n)$ time.

| claim | value |
|---|---|
| encryption and decryption, each case | $\Theta(n)$ |
| extra space | $\Theta(1)$ |
| key recovery from two pairs | at most 12 trials |
| search of all keys | 312 decryptions |

## Properties

- **Monoalphabetic.** Each letter always maps to the same letter. The letter counts of the ciphertext are a permutation of those of the plaintext, so [frequency analysis](/frequency-analysis/) applies.
- **Contains the Caesar cipher.** The keys $(1, b)$ are the 26 Caesar shifts. The keys $(a, 0)$ are the *decimation* ciphers.
- **Closed under composition.** $E_{a_2, b_2} \circ E_{a_1, b_1} = E_{a_2 a_1,\, a_2 b_1 + b_2}$. Encrypting twice gives one affine map again, so it adds no security.
- **A fixed letter.** When $a \ne 1$, the equation $ax + b \equiv x$ has the solution $x \equiv b(1 - a)^{-1}$ if $1 - a$ is a unit. For $(5, 8)$, $1 - 5 = -4$ is not a unit, and $-4x \equiv 8$ has the two solutions $x = 11$ and $x = 24$: L and Y map to themselves.

## Variants and improvements

- **Larger alphabets.** Over $\mathbb{Z}_m$ the key needs $\gcd(a, m) = 1$, and there are $\varphi(m) \cdot m$ keys. For $m = 29$, a prime, there are $28 \cdot 29 = 812$ keys.
- **Blocks of letters.** The [Hill cipher](/hill-cipher/) replaces the number $a$ by an invertible $n \times n$ matrix and acts on blocks of $n$ letters.
- **Any permutation.** The [substitution cipher](/substitution-cipher/) allows all $26!$ bijections of the alphabet. The affine maps are 312 of them.

## When to use it

Use it to teach the role of the inverse modulo $m$, and as the smallest example of a known-plaintext attack that solves linear equations. The same attack, with matrices, breaks the Hill cipher. Never use it to protect data.

## Pitfalls

- **An even key or 13.** With $a = 2$, both A and N map to $b$, and the text can not be decrypted. Line L1 rejects such a key (test `test_bad_key_is_rejected`).
- **Dividing by Δx when it is not a unit.** The formula $a = \Delta y / \Delta x$ fails for even $\Delta x$, although the key is unique there. Try the 12 units as line L7 does, or solve modulo 13 and use that $a$ is odd. The test `test_two_pairs_recover_the_key` checks every key and every pair of letters.
- **Two pairs with Δx = 13.** Pairs such as A and N carry no information on $a$. Pick another pair.
- **Negative remainders.** In C, Java and Go, write `((a_inv * (y - b)) % 26 + 26) % 26`.

## Implementations

## History

Affine ciphers appear in textbooks as the step from the Caesar shift to general substitution, and as the first cipher whose key space needs the condition $\gcd(a, 26) = 1$. Stinson and Paterson treat the cipher, its 312 keys and its known-plaintext attack in Sections 2.1.3 and 2.2.1. The cipher has no single inventor that the sources name, so this page does not name one.

## References
