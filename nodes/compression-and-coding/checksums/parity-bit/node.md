---
tag: XJCSTS
kind: definition
slug: parity-bit
name: Parity bit
aliases:
- Parity-check code
- parity bit
- single parity bit
- vertical redundancy check
area: compression-and-coding/checksums
level: intro
summary: One extra bit making the count of 1s even (even parity) or odd, which detects any single-bit error.
prereqs: [checksum]
see_also: [longitudinal-redundancy-check, product-codes, erasure-codes, hamming-code, repetition-code, linear-code, syndrome, cyclic-redundancy-check]
sources:
  - paper: doi:10.1002/j.1538-7305.1950.tb00463.x
    title: R. W. Hamming, Error detecting and error correcting codes, Bell System Technical Journal 29(2), 1950
    locator: Section 1, Introduction (the single parity check, which detects one error and every odd number of errors)
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 3 (the single-parity-check code as a linear block code of minimum distance 2) and the section on product codes in Chapter 4
  - paper: "Peter Elias, Error-free coding, Transactions of the IRE Professional Group on Information Theory 4(4), 1954"
    title: Error-free coding
    locator: The iterated code, with parity checks on the rows and on the columns of a rectangle of bits
  - paper: doi:10.1145/50202.50214
    title: David A. Patterson, Garth Gibson and Randy H. Katz, A case for redundant arrays of inexpensive disks (RAID), ACM SIGMOD International Conference on Management of Data, 1988
    locator: The sections on the fourth and fifth level RAID (one parity disk for a group, and parity spread over all disks)
---

A parity bit is one extra bit added to a group of bits so that the total number of 1 bits is even (even parity) or odd (odd parity). The receiver counts the 1 bits again, and a wrong count shows that an odd number of bits changed. A parity bit is the smallest possible [checksum](/checksum/): it detects every single-bit error, but it misses every even number of errors. Parity in two directions can also correct one error, and parity over disk blocks lets RAID rebuild a lost disk.

## Definition

Let $b_1, \ldots, b_k$ be bits. The *even parity bit* is

$$p = b_1 \oplus b_2 \oplus \cdots \oplus b_k,$$

so that the $k + 1$ bits $b_1, \ldots, b_k, p$ have an even number of 1 bits. The *odd parity bit* is $1 \oplus p$, so that the count is odd. The receiver gets $k + 1$ bits and computes their XOR; it accepts if the result is 0 for even parity, or 1 for odd parity.

The words with even parity form the *single-parity-check code*, a [linear code](/linear-code/) of length $k + 1$, dimension $k$ and [minimum distance](/minimum-distance/) 2. Its [parity-check matrix](/parity-check-matrix/) is the one row $(1, 1, \ldots, 1)$, and its [syndrome](/syndrome/) is the parity of the received word. Its [dual code](/dual-code/) is the [repetition code](/repetition-code/) of length $k + 1$.

An error pattern $e$ is detected if and only if its [Hamming weight](/hamming-weight/) is odd, because the XOR of the received bits is the XOR of the sent bits plus the parity of $e$. So a parity bit detects every error of 1, 3, 5, … bits, and no error of 2, 4, 6, … bits. Odd parity has the same detection power as even parity. It has one practical advantage: the all-zero word has the wrong parity, so a line or a memory that is stuck at 0 is detected.

**Two-dimensional parity.** Write $k = a \cdot b$ data bits as $a$ rows of $b$ bits. Add an even parity bit to each row, then a row of parity bits for each column, and a corner bit that is the parity of the parity row. This is the [product code](/product-codes/) of two single-parity-check codes, with $(a + 1)(b + 1)$ bits and minimum distance $2 \cdot 2 = 4$. A single error makes exactly one row and one column fail, and the crossing locates the bit, so the decoder flips it. Two errors are always detected. Three errors are always detected when the decoder only detects, but an L-shaped triple, errors at three corners of a rectangle, makes one row and one column fail at the fourth corner, and a decoder that corrects then adds a fourth error. Four errors at the corners of a rectangle are not seen at all.

**Vertical and longitudinal.** On punched tape and in old character protocols, each character was a column on the tape, so its parity bit was a *vertical redundancy check* (VRC). A parity character over the whole block, one bit for each bit position, is the [longitudinal redundancy check](/longitudinal-redundancy-check/). VRC and LRC together are two-dimensional parity.

## Examples and non-examples

**Examples.**

- ASCII "A" is 0x41 = 100 0001, with two 1 bits. With even parity in bit 7 it is sent as 0x41; with odd parity as 0xC1. "C" is 0x43 = 100 0011, with three 1 bits, so it is sent as 0xC3 with even parity and 0x43 with odd parity. A serial line set to "7E1" sends 7 data bits, an even parity bit and one stop bit.
- Memory with one parity bit per byte detects a single flipped bit in a byte and stops the machine; memory with ECC uses a [Hamming code](/hamming-code/) with an extra parity bit to correct it.
- The x86 parity flag holds the even parity of the low 8 bits of a result, not of the whole word. Software computes the parity of a 64-bit word by a population count, or by XOR folding: `x ^= x >> 32; x ^= x >> 16; x ^= x >> 8; x ^= x >> 4; x ^= x >> 2; x ^= x >> 1; return x & 1`.
- **2D parity.** The implementation encodes all $2^{12}$ blocks of 3 rows and 4 columns and finds that the least weight of a nonzero codeword is 4. For 40 random codewords it checks that every single error is corrected, every double error is reported, and every triple error gives a nonzero syndrome. It also shows a rectangle of four errors that passes, and an L-shaped triple that the decoder turns into that rectangle.
- **RAID 4 and RAID 5.** A disk array stores, for each stripe of $k$ data blocks $D_1, \ldots, D_k$, a parity block $P = D_1 \oplus \cdots \oplus D_k$. This is one parity bit for each bit position across the disks. A failed disk reports its own failure, so its block is an erasure, not an unknown error. One parity block can then fill in one lost block: $D_i = P \oplus \bigoplus_{j \ne i} D_j$. RAID 4 keeps all parity on one disk; RAID 5 spreads it over all disks, so that writes do not all wait on the parity disk. To survive two failed disks, RAID 6 adds a second check that is not a parity; see [erasure codes](/erasure-codes/).

**Non-examples.**

- A [cyclic redundancy check](/cyclic-redundancy-check/) of 8 bits is not 8 parity bits of the simple kind: each bit of the remainder is a parity over a different, spread-out set of message bits, chosen so that errors of 2 and 3 bits are detected too. The CRC with generator $x + 1$, however, is exactly the parity bit.
- The [repetition code](/repetition-code/) adds copies, not parity. Its words have distance $n$, and it can correct errors.
- A [Hamming code](/hamming-code/) uses several parity bits over overlapping sets of positions, so one error can be located. Each of its check bits is a parity bit, but the code as a whole is not a single parity check.

## Related definitions

- [Longitudinal redundancy check](/longitudinal-redundancy-check/): parity of each bit column over a block.
- [Product codes](/product-codes/): the general form of two-dimensional parity.
- [Hamming distance](/hamming-distance/): the single-parity-check code is the largest binary code of length $k + 1$ with distance 2.
- [Erasure codes](/erasure-codes/): XOR parity is the simplest erasure code, which fills in one lost block.
- [Checksum](/checksum/): the general notion of a check value.

## References
