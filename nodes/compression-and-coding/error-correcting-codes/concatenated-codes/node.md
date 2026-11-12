---
tag: 5CDZ50
kind: definition
slug: concatenated-codes
name: Concatenated codes
aliases:
- code concatenation
- serial concatenated code
- Forney concatenated code
area: compression-and-coding/error-correcting-codes
level: advanced
summary: "An outer code over a large alphabet whose symbols are each encoded again by a short inner code. The distance is at least the product of the two distances."
history:
  year: 1966
  people: [G. David Forney Jr.]
  note: Forney introduced concatenated codes and generalized minimum distance decoding in 1966. Justesen used them in 1972 for the first explicit asymptotically good binary codes.
prereqs: [reed-solomon-code, minimum-distance]
see_also: [hamming-code, convolutional-code, interleaving, burst-errors, product-codes, gilbert-varshamov-bound, turbo-code, reed-solomon-decoding]
sources:
  - paper: "G. David Forney Jr., Concatenated Codes, MIT Press, Cambridge, MA, 1966 (MIT Research Monograph 37)"
    title: Concatenated Codes
    locator: The construction of an outer code over GF(q^k) with an inner code over GF(q), the product bound on the minimum distance, and the error exponent and decoding complexity of concatenated codes
  - paper: doi:10.1109/TIT.1966.1053873
    title: G. David Forney Jr., Generalized minimum distance decoding, IEEE Transactions on Information Theory 12(2), 1966, pages 125 to 131
    locator: The GMD decoder (erase the least reliable symbols in steps and decode errors and erasures) and the theorem that it corrects every pattern within less than half the minimum distance
  - paper: doi:10.1109/TIT.1972.1054893
    title: Jørn Justesen, A class of constructive asymptotically good algebraic codes, IEEE Transactions on Information Theory 18(5), 1972, pages 652 to 656
    locator: The code with a Reed-Solomon outer code and the inner codes x to (x, α_i x), and its bound on relative distance
  - url: https://ccsds.org/Pubs/131x0b5.pdf
    title: CCSDS 131.0-B-5, TM Synchronization and Channel Coding, Recommended Standard (Blue Book), Issue 5, September 2023
    locator: Section 3.3 (the basic convolutional code, rate 1/2, constraint length 7), Section 4 (the (255,223) Reed-Solomon code for E = 16, the (255,239) code for E = 8, interleaving depths I = 1, 2, 3, 4, 5 and 8), Section 5 (Reed-Solomon outer code and convolutional inner code)
  - paper: "Robert J. McEliece and Laif Swanson, Reed-Solomon codes and the exploration of the solar system, in Stephen B. Wicker and Vijay K. Bhargava (eds.), Reed-Solomon Codes and Their Applications, IEEE Press, 1994"
    title: Reed-Solomon codes and the exploration of the solar system
    locator: The concatenated Reed-Solomon and convolutional coding system of Voyager and its later use as a deep space standard
  - book: isbn:9780444851932
    title: F. J. MacWilliams and N. J. A. Sloane, The Theory of Error-Correcting Codes, North-Holland, 1977
    locator: Chapter 10 (concatenated codes and Justesen codes)
---

A concatenated code encodes a message twice. An *outer code* over a large alphabet first encodes the message into a string of symbols. A short *inner code* then encodes each of those symbols into a block of bits. The result is a binary code whose minimum distance is at least the product of the two distances, and it can be decoded with two small decoders in place of one large one. G. David Forney Jr. introduced concatenated codes in 1966. Reed-Solomon outer codes with convolutional inner codes protected deep space missions for decades.

## Definition

**Notation.** $q$ is a prime power, usually 2. An $[n, k, d]_q$ code is a code over $\mathrm{GF}(q)$ of length $n$, dimension $k$ and [minimum distance](/minimum-distance/) $d$.

**Definition (concatenated code, Forney 1966).** Take

- an *outer code* $A$ with parameters $[N, K, D]_{q^k}$, over the field $\mathrm{GF}(q^k)$;
- an *inner code* $B$ with parameters $[n, k, d]_q$;
- a bijection $\varphi$ from $\mathrm{GF}(q^k)$ to $\mathrm{GF}(q)^k$ that is $\mathrm{GF}(q)$-linear, for example the coordinates in a fixed basis.

The concatenated code $A \circ B$ has the codewords

$$\bigl(B(\varphi(a_1)), B(\varphi(a_2)), \ldots, B(\varphi(a_N))\bigr), \qquad (a_1, \ldots, a_N) \in A.$$

It is a linear code with parameters $[Nn, Kk, \ge Dd]_q$, and rate $(K/N)(k/n)$.

**Lemma (product bound).** The minimum distance of $A \circ B$ is at least $Dd$.

*Proof.* The code is linear, so its distance is its least nonzero weight. A nonzero outer codeword has at least $D$ nonzero symbols. The map $\varphi$ is a bijection and $B$ is injective, so each nonzero symbol becomes a nonzero inner codeword, of weight at least $d$. The weights add over the $N$ blocks, so the total is at least $Dd$. $\square$

The true distance can be larger than $Dd$ for some choices of $\varphi$ and $B$. The proof needs both parts of the structure: the outer distance counts symbols of the big field, and each outer symbol goes through the whole inner code.

**Two-stage decoding.** Decode each inner block to the nearest inner codeword, map it back to an outer symbol, and decode the outer word. Let $t_{\text{in}} = \lfloor (d-1)/2 \rfloor$ and $t_{\text{out}} = \lfloor (D-1)/2 \rfloor$. A wrong inner decision needs at least $t_{\text{in}} + 1$ bit errors in its block, and the outer decoder fails only with at least $t_{\text{out}} + 1$ wrong symbols. So the decoder corrects every pattern of at most $(t_{\text{in}} + 1)(t_{\text{out}} + 1) - 1$ errors, about $Dd/4$: half of what the distance allows.

**Generalized minimum distance decoding (Forney 1966).** GMD decoding recovers the missing half. The inner decoder also reports how far each block was from its decision, a measure of reliability. Then:

1. sort the $N$ outer symbols from the least reliable to the most reliable;
2. for $s = D - 1, D - 3, \ldots$ down to 1 or 0 (each step of two adds one correctable error), erase the $s$ least reliable symbols and run an errors-and-erasures decoder for $A$, which succeeds when $2e + s < D$;
3. from the candidates, keep the one whose concatenated codeword is closest to the received word.

Forney proved that GMD decoding corrects every pattern of fewer than $Dd/2$ bit errors. It runs the outer decoder at most about $D/2$ times, so it stays polynomial when $A$ is a Reed-Solomon code.

**Asymptotic results.**

- *Capacity.* Forney showed that concatenated codes, with a Reed-Solomon outer code and a random-like inner code of fixed length, reach any rate below the capacity of a memoryless channel with error probability that falls exponentially in the length, and with decoding time polynomial in the length.
- *Zyablov bound.* With a Reed-Solomon outer code and the best inner code of each rate, concatenated binary codes of rate $R$ reach relative distance at least $\max_{R \le r \le 1} (1 - R/r)\, H_2^{-1}(1 - r)$, where $H_2^{-1}$ is the inverse of the binary entropy function on $[0, 1/2]$.
- *Justesen codes (1972).* The outer code is a Reed-Solomon code of length $N = 2^m - 1$ over $\mathrm{GF}(2^m)$ with evaluation points $\alpha_1, \ldots, \alpha_N$, the nonzero field elements. Position $i$ uses its own inner code $x \mapsto (x, \alpha_i x)$, a binary $[2m, m]$ code. These inner codes form the *Wozencraft ensemble*: each pair $(u, v)$ with $u, v \ne 0$ lies in exactly one of them, so only a few of them can have small distance. Justesen proved that for rates $R < 1/2$ the relative distance is at least about $(1 - 2R)\, H_2^{-1}(1/2) \approx 0.11 (1 - 2R)$, bounded away from zero as $N$ grows. These were the first explicit binary codes with both rate and relative distance bounded below by constants, which the [Gilbert-Varshamov bound](/gilbert-varshamov-bound/) shows to exist for random codes.

**In practice.** The CCSDS telemetry standard (131.0-B-5, Section 5) defines a concatenated code: the Reed-Solomon $(255, 223)$ code over $\mathrm{GF}(256)$ is the outer code and the rate 1/2, constraint length 7 [convolutional code](/convolutional-code/) is the inner code. The inner code is decoded by the Viterbi algorithm, whose errors come in bursts. [Interleaving](/interleaving/) of depth $I$ (1, 2, 3, 4, 5 or 8) between the two codes spreads each [burst](/burst-errors/) over $I$ outer codewords. McEliece and Swanson describe how this system came from the Voyager missions. [Turbo codes](/turbo-code/) are a *parallel* concatenation of two convolutional codes; the product bound does not apply to them.

## Examples and non-examples

**Reed-Solomon over GF(16) with the Hamming code.** Let $A$ be the [Reed-Solomon code](/reed-solomon-code/) $[6, 3, 4]_{16}$ that evaluates a polynomial of degree less than 3 at the points $1, \alpha, \ldots, \alpha^5$ of $\mathrm{GF}(16)$ (modulus $x^4 + x + 1$). Let $B$ be the [Hamming code](/hamming-code/) $[7, 4, 3]_2$. The concatenated code is a binary $[42, 12]$ code, and the bound gives distance at least $4 \cdot 3 = 12$. Enumeration of all $2^{12}$ codewords gives exactly 12. Other outer codes give the same picture:

| outer code | inner code | concatenated code | product bound | true distance |
|---|---|---|---|---|
| $[5, 2, 4]_{16}$ | $[7, 4, 3]_2$ | $[35, 8]_2$ | 12 | 12 |
| $[6, 3, 4]_{16}$ | $[7, 4, 3]_2$ | $[42, 12]_2$ | 12 | 12 |
| $[7, 3, 5]_{16}$ | $[7, 4, 3]_2$ | $[49, 12]_2$ | 15 | 15 |

**Two-stage decoding against GMD.** The message $(1, 2, 3)$ gives the outer codeword $(0, 9, 12, 5, 8, 4)$ (symbols written as 4-bit integers). Put two bit errors into each of the first two blocks. The inner decoder returns 7 and 14 in place of 0 and 9, each at distance 1 from its block, while the other blocks are at distance 0. Two wrong symbols are too many for the outer code, which corrects one, so two-stage decoding fails with only 4 bit errors. GMD erases the least reliable symbols, the first two, and the outer code fills in the erasures. (The implementation tries every $s$ from 0 to $D - 1$, which includes Forney's choices.) The tests check that two-stage decoding corrects every pattern of at most 3 errors (all $\binom{42}{3} = 11480$ of them), and that GMD corrects 1500 patterns of 4 and 5 errors spread over the blocks in every possible way. With 6 errors the guarantee ends: $0000111$ is a Hamming codeword, so three errors in each of two blocks give two wrong symbols that look fully reliable.

**A small Justesen code.** With $m = 4$ the outer code is a $[15, K]_{16}$ Reed-Solomon code and the inner codes are $[8, 4]$ codes. For $K = 2$ the binary code is $[120, 8]$ with distance 47; for $K = 3$ it is $[120, 12]$ with distance 41. Since the 15 inner codes are distinct, the $D = 16 - K$ nonzero outer symbols give distinct nonzero inner words, so the distance is at least the total weight of the $D$ lightest of these words: 28 and 26 here. At this small size the asymptotic bound of Justesen says nothing useful, but the construction is the same.

**Non-example: the binary image of a Reed-Solomon code.** Writing each symbol of a $[6, 3, 4]_{16}$ codeword as 4 bits gives a binary $[24, 12]$ code. A single nonzero symbol can be a single nonzero bit, so the guaranteed distance is only 4. The inner code is what multiplies the distance.

**Non-example: a turbo code.** A turbo code puts two encoders side by side on the same message, with an interleaver between them. Neither code encodes the other, and its minimum distance is often small; its strength comes from iterative decoding.

## Related definitions

- [Reed-Solomon codes](/reed-solomon-code/): the usual outer code, MDS and over a large field.
- [Hamming codes](/hamming-code/) and [convolutional codes](/convolutional-code/): common inner codes.
- [Product codes](/product-codes/): arrays whose rows and columns are codewords. Their distance is also the product of the two distances, and they are decoded row and column in turn.
- [Interleaving](/interleaving/) and [burst errors](/burst-errors/): the interleaver between inner and outer code turns bursts from the inner decoder into scattered symbol errors.
- [Gilbert-Varshamov bound](/gilbert-varshamov-bound/): Justesen codes give explicit codes with a positive rate and relative distance, below this bound.
- [Reed-Solomon decoding](/reed-solomon-decoding/): errors-and-erasures decoding of the outer code is the core step of GMD.

## References

- G. David Forney Jr., Concatenated Codes, MIT Press, 1966.
- G. David Forney Jr., "Generalized minimum distance decoding", IEEE Transactions on Information Theory 12(2), 1966, pages 125 to 131.
- Jørn Justesen, "A class of constructive asymptotically good algebraic codes", IEEE Transactions on Information Theory 18(5), 1972, pages 652 to 656.
- CCSDS 131.0-B-5, TM Synchronization and Channel Coding, 2023.
- Robert J. McEliece and Laif Swanson, "Reed-Solomon codes and the exploration of the solar system", in Reed-Solomon Codes and Their Applications, IEEE Press, 1994.
- F. J. MacWilliams and N. J. A. Sloane, The Theory of Error-Correcting Codes, North-Holland, 1977, Chapter 10.
