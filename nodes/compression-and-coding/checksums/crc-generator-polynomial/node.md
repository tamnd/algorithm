---
tag: TY4M8X
kind: concept
slug: crc-generator-polynomial
name: CRC generator polynomial
aliases:
- CRC polynomial
area: compression-and-coding/checksums
level: intro
summary: Fixed polynomial over GF(2) whose remainder on the message gives the CRC.
prereqs: [cyclic-redundancy-check, irreducible-polynomial, multiplicative-order]
see_also: [crc-error-detection-guarantees, crc32c, minimum-distance, hamming-distance, cyclic-code, gf2-polynomial-arithmetic, rabin-irreducibility-test, undetected-error-probability]
sources:
  - paper: doi:10.1109/DSN.2004.1311885
    title: Philip Koopman and Tridib Chakravarty, Cyclic redundancy code (CRC) polynomial selection for embedded networks, International Conference on Dependable Systems and Networks (DSN), 2004
    locator: Sections 2 to 5 (Hamming distance as a function of data word length, the weights of undetected errors, and tables of good polynomials of widths 3 to 16)
  - paper: doi:10.1109/26.231911
    title: Guy Castagnoli, Stefan Bräuer and Martin Herrmann, Optimization of cyclic redundancy-check codes with 24 and 32 parity bits, IEEE Transactions on Communications 41(6), 1993
    locator: The search over generators of degree 24 and 32 for a large minimum distance at given lengths, and the classes of factorizations
  - url: https://users.ece.cmu.edu/~koopman/crc/crc8.html
    title: Philip Koopman, CRC polynomial zoo, 8-bit polynomials
    locator: Entries 0x83, 0x97, 0x9b, 0xa6, 0xe7, 0xea, 0x80 and 0x8e (Koopman notation, the reciprocal, and the maximum data length for each Hamming distance)
  - url: https://users.ece.cmu.edu/~koopman/crc/crc32.html
    title: Philip Koopman, CRC polynomial zoo, 32-bit polynomials
    locator: Entries 0x82608edb (IEEE 802.3) and 0x8f6e37a0 (CRC-32C)
  - paper: doi:10.1109/JRPROC.1961.287814
    title: W. W. Peterson and D. T. Brown, Cyclic codes for error detection, Proceedings of the IRE 49(1), 1961
    locator: pp. 228 to 235 (the errors that a generator detects, from its factors and its period)
  - book: isbn:9780521392310
    title: Rudolf Lidl and Harald Niederreiter, Finite Fields, second edition, Cambridge University Press, 1997
    locator: Chapter 3, Section 3.1 (the order of a polynomial and primitive polynomials)
---

The generator polynomial of a [cyclic redundancy check](/cyclic-redundancy-check/) is the fixed polynomial $G(x)$ of degree $r$ over GF(2) that the message is divided by. It decides which errors the CRC always detects: its factors give the guarantees for odd numbers of errors and for pairs of errors, and its weight distribution gives the Hamming distance at each message length. The same generator is written in at least three notations, which is a common source of errors.

## In plain words

A CRC divides the message by a fixed number and keeps the remainder. That fixed number is the generator. All CRCs of the same size have the same cost, but some generators are much better than others. A good one catches every error of up to five or six flipped bits in a message of normal size. A bad one can miss some errors of two flipped bits.

What makes a generator good can be found by computer: try every short pattern of errors, and see whether the generator divides it. Researchers have done this for all generators of small size, and they publish lists of the best ones for each message length.

## The idea

### Notations

A generator of degree $r$ has $r + 1$ coefficients, and the first and the last are always 1. An $r$-bit word can hold only $r$ of them, so each notation leaves one out.

| notation | what it stores | CRC-32 | CRC-32C | CRC-16/ARC | CRC-8/SMBUS |
|---|---|---|---|---|---|
| normal | all terms except $x^r$, $x^{r-1}$ at the top | 0x04C11DB7 | 0x1EDC6F41 | 0x8005 | 0x07 |
| reversed | the normal word with its bits in reverse order | 0xEDB88320 | 0x82F63B78 | 0xA001 | 0xE0 |
| Koopman | all terms except $x^0$, $x^r$ at the top | 0x82608EDB | 0x8F6E37A0 | 0xC002 | 0x83 |
| full | all $r + 1$ terms | 0x104C11DB7 | 0x11EDC6F41 | 0x18005 | 0x107 |

The normal form is the poly of the Williams model and of the catalogue. The reversed form is the constant in right-shifting code such as zlib. The Koopman form shows the degree by its top bit, so one table can list generators of different degrees. The *reciprocal* $x^r G(1/x)$ is a different polynomial: it has the coefficients of $G$ in reverse order. The reversed notation of $G$ is the Koopman notation of the reciprocal. A generator and its reciprocal have the same Hamming distances, because a codeword of one, read backwards, is a codeword of the other.

### What the factors guarantee

An error $E(x)$ is missed exactly when $G(x)$ divides $E(x)$. From this:

- **Single errors.** $G$ has at least two terms, so it never divides $x^i$.
- **Odd numbers of errors.** If $(x + 1)$ divides $G$, then $G(1) = 0$, so every codeword has an even number of 1 bits. So every error of odd weight is detected. $(x + 1)$ divides $G$ exactly when $G$ has an even number of terms.
- **Two errors.** An error $x^i (x^j + 1)$ is missed exactly when $G$ divides $x^j + 1$, that is, when $j$ is a multiple of the period of $G$, the least $e$ with $x^e \equiv 1 \pmod G$. This is the [multiplicative order](/multiplicative-order/) of $x$ modulo $G$. A primitive factor of degree $d$, which is an [irreducible polynomial](/irreducible-polynomial/) modulo which $x$ has the largest possible order, has period $2^d - 1$.
- **Bursts.** Every burst of length at most $r$ is detected, for each $G$ with a term $x^0$. See [CRC error-detection guarantees](/crc-error-detection-guarantees/).

Two classic designs follow:

- **$G$ primitive of degree $r$.** Then the period is $2^r - 1$, and the CRC detects all 1-bit and 2-bit errors in codewords of up to $2^r - 1$ bits, so the Hamming distance is 3 up to $2^r - 1 - r$ data bits. The IEEE CRC-32 has this form: 0x104C11DB7 is irreducible, and $x$ has order $2^{32} - 1$ modulo it. So it has HD 3 up to 4294967263 data bits, which is the first entry in the zoo of Koopman.
- **$G = (x + 1)\, p(x)$ with $p$ primitive of degree $r - 1$.** Then all odd errors and all 2-bit errors up to codeword length $2^{r-1} - 1$ are detected, so the Hamming distance is 4 up to $2^{r-1} - 1 - r$ data bits. CRC-16 0x8005 is $(x + 1)(x^{15} + x + 1)$, with HD 4 up to 32751 data bits. CRC-32C is $(x + 1)$ times a primitive factor of degree 31, with HD 4 up to 2147483615 data bits.

The factors fix the guarantees for weights 1, 2 and odd weights. The guarantees for weight 3 to 6 at practical lengths depend on the whole polynomial, and only a search finds them.

### The Hamming distance profile

For each data length $L$, the [minimum distance](/minimum-distance/) $d(L)$ of the shortened code is the least weight of a nonzero multiple of $G$ with fewer than $L + r$ bits. It does not increase with $L$. Koopman and Chakravarty (2004) describe a generator by the list of the largest $L$ for each [Hamming distance](/hamming-distance/) 3, 4, 5, and so on. Castagnoli, Bräuer and Herrmann (1993) used such a search for widths 24 and 32, and found CRC-32C; Koopman and Chakravarty did it for all generators of widths 3 to 16, and showed that several standard generators are far from the best for their typical message lengths.

The implementation computes the profile by exhaustive search. With syndromes $s_i = x^i \bmod G$, a pattern of positions is a codeword exactly when its syndromes XOR to 0. A codeword of length $N$ that does not use position $N - 1$ is already a codeword of length $N - 1$. So when the length grows by one, only patterns that use the new position need a test: weight 2 and 3 by a set of single and pair syndromes, weight 4 by one pass over the positions, and higher weights by enumeration while the distance is still high. A second, independent check computes $d(L)$ as the least weight of all $2^L - 1$ multiples for $L \le 13$.

### Factoring a generator

To find the factors, the implementation removes square factors with the derivative, splits the rest by degree with $\gcd(G, x^{2^d} - x)$ for $d = 1, 2, \ldots$, and splits factors of equal degree with the trace map of Cantor and Zassenhaus. The [Rabin test](/rabin-irreducibility-test/) uses the same powers $x^{2^d}$.

## Examples

**Notation round trip.** CRC-32 in normal notation is 0x04C11DB7. The full polynomial is 0x104C11DB7 $= x^{32} + x^{26} + x^{23} + x^{22} + x^{16} + x^{12} + x^{11} + x^{10} + x^8 + x^7 + x^5 + x^4 + x^2 + x + 1$. Drop $x^0$ and shift right by one: the Koopman notation 0x82608EDB. Reverse the 32 bits of the normal word: 0xEDB88320.

**Factorizations**, computed by the implementation and checked by multiplication:

| generator (full) | used in | factors |
|---|---|---|
| 0x104C11DB7 | CRC-32 | irreducible, primitive (period $2^{32} - 1$) |
| 0x11EDC6F41 | CRC-32C | $(x + 1) \cdot$ 0xF5B4253F, primitive of degree 31 |
| 0x18005 | CRC-16/ARC, Modbus | $(x + 1)(x^{15} + x + 1)$ |
| 0x11021 | CRC-16 of ITU-T V.41 | $(x + 1) \cdot$ 0xF01F, primitive of degree 15 |
| 0x107 | CRC-8/SMBUS | $(x + 1) \cdot$ 0xFD, primitive of degree 7 |
| 0x101 | none | $(x + 1)^8$, a very poor CRC-8 |

**Hamming distance profiles of 8-bit generators.** The list gives the largest data length in bits for HD 3, 4, 5, …. The search of the implementation gives the same lists as the 8-bit zoo of Koopman for each of these:

| Koopman | full | factors | profile |
|---|---|---|---|
| 0x83 | 0x107 | $(x+1)$, degree 7 | {119, 119} |
| 0x97 | 0x12F | $(x+1)$, degree 7 | {119, 119, 3, 3} |
| 0x9B | 0x137 | $(x+1)^2$, degree 6 | {118, 118, 4, 4} |
| 0xA6 | 0x14D | primitive, degree 8 | {247, 15, 6} |
| 0xE7 | 0x1CF | primitive, degree 8 | {247, 19, 1, 1, 1} |
| 0xEA | 0x1D5 | $(x+1)$, degree 2, degree 5 | {85, 85, 2, 2} |
| 0x8E | 0x11D | primitive, degree 8 | {247, 13, 6} |
| 0x80 | 0x101 | $(x+1)^8$ | {} |

So 0x83 (CRC-8/SMBUS) and 0x97 (the generator of CRC-8/AUTOSAR) both have HD 4 up to 119 bits, but 0x97 also has HD 6 for messages of up to 3 bits. The primitive generators 0xA6 and 0xE7 have HD 3 up to 247 bits, twice as long, but only HD 3. For 0x101, $x^8 + 1$ is a codeword of weight 2, so even two flipped bits 8 apart are missed.

## Where it is used

Each standard CRC fixes a generator: the IEEE CRC-32 in Ethernet, zip, gzip and PNG; [CRC-32C](/crc32c/) in iSCSI, SCTP, ext4 and Btrfs; 0x1021 in HDLC, X.25 and Bluetooth; 0x8005 in USB and Modbus. Designers of new protocols choose a generator from the tables of Koopman for the message lengths they expect, and the expected error weights. The same polynomials over GF(2) are the generators of [cyclic codes](/cyclic-code/), such as the Hamming and BCH codes, and the feedback polynomials of linear feedback shift registers. The probability that a random error is missed also depends on the generator; see [undetected error probability](/undetected-error-probability/).

## References
