---
tag: PFEGKF
kind: definition
slug: minimum-distance
name: Minimum distance of a code
aliases:
- minimum distance
area: compression-and-coding/error-correcting-codes
level: core
summary: The least Hamming distance between two different codewords. A code with minimum distance d detects d - 1 errors, corrects (d - 1)/2 rounded down, and fills d - 1 erasures.
prereqs: [hamming-distance, hamming-weight]
see_also: [minimum-distance-problem, singleton-bound, hamming-bound, gilbert-varshamov-bound, maximum-likelihood-decoding, erasure-decoding, error-detection, linear-code]
sources:
  - paper: doi:10.1002/j.1538-7305.1950.tb00463.x
    title: R. W. Hamming, Error detecting and error correcting codes, Bell System Technical Journal 29(2), 1950
    locator: The geometric model of codes in the n-cube, and the link between the minimum distance and the number of errors that a code detects or corrects
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Section 3.3 (the minimum distance of a block code) and Section 3.4 (the error-detecting and error-correcting capabilities of a block code)
  - book: isbn:9780521845045
    title: Ron M. Roth, Introduction to Coding Theory, Cambridge University Press, 2006
    locator: Section 1.3 (block codes and their parameters) and Section 1.5 (levels of error handling, errors and erasures together)
---

The minimum distance of a code is the smallest [Hamming distance](/hamming-distance/) between two different codewords. It is one number, but it fixes how many symbol errors the code is sure to detect, how many it is sure to correct, and how many erased symbols it can fill in. Together with the length $n$ and the number of codewords, it is the third parameter that names a block code, and most bounds in coding theory are bounds on it.

## Definition

Let $\Sigma$ be a finite alphabet with $q$ symbols, and let $C \subseteq \Sigma^n$ be a block code with $M \ge 2$ codewords. The **minimum distance** of $C$ is

$$d(C) = \min \{\, d(x, y) : x, y \in C,\ x \ne y \,\},$$

where $d(x, y)$ is the Hamming distance. A code with these parameters is an $(n, M, d)_q$ code. When $C$ is a [linear code](/linear-code/) of dimension $k$ over $\mathrm{GF}(q)$, one writes $[n, k, d]_q$, and then $d(C)$ is the least [Hamming weight](/hamming-weight/) of a nonzero codeword, because $d(x, y) = \mathrm{wt}(x - y)$ and $x - y$ is again a codeword.

**What $d$ guarantees.** A codeword $c$ is sent. An *error* changes a symbol, and the receiver does not know where; an *erasure* replaces a symbol by a mark $?$, and the receiver knows where. Let $d = d(C)$.

1. **Detection.** Every pattern of $1$ to $d - 1$ errors gives a word that is not a codeword. So the test "is the received word in $C$?" detects it.
2. **Correction.** Every pattern of at most $t = \lfloor (d - 1)/2 \rfloor$ errors leaves $c$ as the only codeword within distance $t$ of the received word, so the nearest codeword is $c$.
3. **Erasures.** Every pattern of at most $d - 1$ erasures leaves $c$ as the only codeword that agrees with the received word on the positions that are not erased.
4. **Errors and erasures together.** If there are $e$ erasures and $\tau$ errors with $2\tau + e < d$, then $c$ is the only codeword that differs from the received word in at most $\lfloor (d - 1 - e)/2 \rfloor$ of the positions that are not erased.
5. **Correction and detection together.** For $t' \le s$ with $t' + s < d$, the decoder that corrects up to $t'$ errors and reports the rest corrects every pattern of at most $t'$ errors and detects every pattern of $t' + 1$ to $s$ errors.

None of these numbers can be raised for every code: two codewords at distance exactly $d$ give a pattern of $d$ errors that turns one into the other, a pattern of $d$ erasures that leaves both possible, and a word with $\lceil d/2 \rceil$ errors that lies at least as close to the wrong codeword as to the right one. The proofs of all five parts and of this tightness are in the proof file. The intuition is geometric: the balls of radius $t$ around the codewords do not meet, because two of them would need $2t \ge d$.

The minimum distance only controls the *worst case* number of errors. A decoder can often correct many patterns of more than $t$ errors, and on a random channel the full list of distances (the weight distribution, for a linear code) matters too.

## Examples and non-examples

**Examples.**

- The [repetition code](/repetition-code/) $\{00000, 11111\}$ is a $[5, 1, 5]_2$ code. It detects 4 errors, corrects 2 by majority vote, and fills 4 erasures.
- The binary even-weight code of length $n$ (all words with an even number of ones, a [parity bit](/parity-bit/) on $n - 1$ bits) is an $[n, n - 1, 2]_2$ code. It detects any single error but corrects none, because $t = 0$. It fills one erasure: the missing bit is the parity of the others.
- The [Hamming code](/hamming-code/) $[7, 4, 3]_2$ corrects one error or detects two, but not both at once. Add an overall parity bit and it becomes the extended $[8, 4, 4]_2$ code. With $d = 4$ it can correct one error and detect two at the same time ($t' = 1$, $s = 2$), or correct one error and one erasure ($2 \cdot 1 + 1 = 3 < 4$), or fill three erasures.
- **A worked case.** In the extended Hamming code, flip one bit of a codeword and erase another. Bounded distance decoding with $e = 1$ uses the radius $\lfloor (4 - 1 - 1)/2 \rfloor = 1$ on the 7 positions that are not erased, and exactly one codeword is that close: the sent one. Now flip two bits and erase nothing. The received word is not a codeword, so the error is detected, but two codewords can be at distance 2 from it, and the decoder must report a failure.
- The ternary tetracode with generator rows $(1, 0, 1, 1)$ and $(0, 1, 1, 2)$ over $\mathrm{GF}(3)$ is a $[4, 2, 3]_3$ code. Its 8 nonzero codewords all have weight 3. It meets the [Singleton bound](/singleton-bound/) $d \le n - k + 1$ and the [Hamming bound](/hamming-bound/) with equality, so it is both MDS and perfect.
- **Reed-Solomon codes.** A [Reed-Solomon code](/reed-solomon-code/) $[n, k]$ over $\mathrm{GF}(q)$ has $d = n - k + 1$, the most that the Singleton bound allows. So $n - k$ check symbols buy $n - k$ erasures, or $\lfloor (n - k)/2 \rfloor$ errors.

**Non-examples.**

- **A code with one codeword** has no pairs, and $d$ is not defined (some books set it to $\infty$ or to $n + 1$). It sends no information.
- **The least weight is not the distance of a code that is not linear.** The code $\{000, 011, 101, 111\}$ has least nonzero weight 2, but $d(011, 111) = 1$, so its minimum distance is 1.
- **The minimum distance is not the error rate.** On a [binary symmetric channel](/binary-symmetric-channel/) a decoder is judged by its average error probability. Two codes with the same $n$, $M$ and $d$ can have different numbers of codeword pairs at distance $d$, and so different error rates. The minimum distance is a worst case guarantee, not the full picture.
- **Bursts.** A code with $d = 3$ fails on a burst of 2 errors, while a code built for [burst errors](/burst-errors/) can correct long bursts with a small $d$. The minimum distance counts errors, not how they cluster.

## Related definitions

- [Hamming distance](/hamming-distance/) and [Hamming weight](/hamming-weight/): the metric on words, and the distance from the zero word.
- [Minimum distance problem](/minimum-distance-problem/): computing $d$ of a linear code from its generator matrix. The direct method used here compares all pairs of codewords, and for linear codes all $q^k - 1$ nonzero weights; the general problem is NP-hard.
- [Singleton bound](/singleton-bound/), [Hamming bound](/hamming-bound/) and [Gilbert-Varshamov bound](/gilbert-varshamov-bound/): limits on how large $d$ can be for a given length and number of codewords, and a guarantee that good codes exist.
- [Maximum likelihood decoding](/maximum-likelihood-decoding/): on a binary symmetric channel with $p < 1/2$ it picks the nearest codeword, and the correction guarantee above is the worst case of it.
- [Erasure decoding](/erasure-decoding/): the decoding of part 3, which for a linear code solves a linear system on the positions that are not erased.
- [Error detection](/error-detection/): the use of part 1, often with a cyclic code such as a CRC.

## References
