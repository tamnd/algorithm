---
tag: DFWYWR
kind: concept
slug: bit-packing
name: Bit packing
aliases:
- packed integers
- bit-packed arrays
area: techniques/bit-tricks
level: intro
summary: Storing values in the minimum number of bits needed, packing several per word.
prereqs: [bitwise-operations, bitmask]
see_also: [bit-set, bit-vector, bitboard, pfor-delta, variable-byte-encoding, elias-fano-encoding, simd-within-a-register, succinct-data-structures]
sources:
  - paper: doi:10.1002/spe.2203
    title: Daniel Lemire and Leonid Boytsov, Decoding billions of integers per second through vectorization, Software Practice and Experience 45(1), 2015
    locator: pp. 1 to 29
  - paper: doi:10.1109/ICDE.1998.655800
    title: Jonathan Goldstein, Raghu Ramakrishnan and Uri Shaft, Compressing relations and indexes, Proceedings of the 14th International Conference on Data Engineering (ICDE 1998)
    locator: pp. 370 to 379
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.1.3, Bitwise Tricks and Techniques
---

Bit packing stores each value of a sequence in exactly $b$ bits, where $b$ is the fewest bits that hold the largest value, and puts the fields one after another in an array of words without gaps. An array of $n$ values below $2^b$ then takes $\lceil nb / w \rceil$ words instead of $n$ words, and the value at index $i$ is read with one or two word reads, a shift and a mask. It is the basic layout of [bit sets](/bit-set/), [bitboards](/bitboard/), compressed integer lists such as [PFOR-delta](/pfor-delta/), and [succinct data structures](/succinct-data-structures/), and it is what makes [SIMD within a register](/simd-within-a-register/) possible.

## In plain words

Most programs store each number in a full word of 32 or 64 bits, even when the number is small. If every number in a list is below 8, three bits are enough for each one. Bit packing writes the numbers one after another, three bits each, with no space between them, so a 64-bit word holds 21 of them instead of one.

To read a number back, you work out where its three bits start, take the word or the two words that hold them, shift the bits down, and cut away everything else. The list gets much smaller, and reading it costs only a few extra steps.

## The idea

**Width.** For values $0 \le v_i \le V$, the width is $b = \lceil \lg (V + 1) \rceil$, at least 1. Signed values are first mapped to unsigned ones, for example by an offset or by the zigzag map $v \mapsto 2v$ for $v \ge 0$ and $v \mapsto -2v - 1$ for $v < 0$.

**Layout.** Value $i$ occupies the bit positions $ib, \ldots, ib + b - 1$ of the array, counted from bit 0 of word 0. With $p = ib$, the field starts in word $q = \lfloor p / w \rfloor$ at offset $r = p \bmod w$, and it runs into word $q + 1$ when $r + b > w$.

**Access.** For $b \le w$,
$$ \operatorname{get}(i) = \bigl( (W[q] \gg r) \mathbin{|} [r + b > w] \cdot (W[q + 1] \ll (w - r)) \bigr) \mathbin{\&} (2^b - 1), $$
computed modulo $2^w$. A write clears the field with the complement of the shifted mask and ORs in the new value, in one or two words. Both take $O(1)$ word operations. If $b$ divides $w$, no field crosses a word boundary and the second term never applies.

**Space.** $\lceil nb / w \rceil$ words, against $n$ words unpacked, so a saving by the factor $w / b$. The information-theoretic minimum for $n$ arbitrary values below $2^b$ is $nb$ bits, so the layout is optimal for such values; it is not optimal when the values have a skewed distribution, where codes of variable length do better.

**Bulk decoding.** Reading values one at a time costs a branch or a second word read per value. For fixed $b$, a decoder for blocks of 32 or 64 values can be unrolled into straight-line shifts and masks, and vector instructions decode several values at once. Lemire and Boytsov show that such decoders unpack billions of integers per second.

## Examples

Pack the values $5, 3, 7, 0, 6, 2$ with $b = 3$ into 8-bit words. The fields occupy the bit positions 0 to 2, 3 to 5, 6 to 8, 9 to 11, 12 to 14 and 15 to 17, so value 2 straddles words 0 and 1, and value 5 straddles words 1 and 2. The words, written with bit 7 on the left, are

| word | bits | hex |
| --- | --- | --- |
| 0 | 11 011 101 | 0xDD |
| 1 | 0 110 000 1 | 0x61 |
| 2 | 000000 01 | 0x01 |

To read value 2: $p = 6$, $q = 0$, $r = 6$, and $r + b = 9 > 8$. Then $W[0] \gg 6 = 11_2$, $W[1] \ll 2 = 110000100_2$, and the OR masked to 3 bits is $111_2 = 7$.

Other examples:

- A [bit set](/bit-set/) or [bit vector](/bit-vector/) is bit packing with $b = 1$.
- A chess [bitboard](/bitboard/) packs 64 squares, one bit each, into one word.
- DNA bases A, C, G and T take 2 bits each, 32 bases to a 64-bit word.
- A date with a day (5 bits), a month (4 bits) and a year offset (7 bits) fits in 16 bits, as in the date format of the FAT file system.

## Where it is used

- **Integer compression.** Frame of reference, from Goldstein, Ramakrishnan and Shaft, subtracts the minimum of a block and packs the differences with the width of the largest one. [PFOR-delta](/pfor-delta/) packs most values of a block with a small $b$ and stores the few large ones as exceptions. These codes compress the posting lists of search engines and the columns of analytic databases.
- **Succinct and compact structures.** Rank and select structures, wavelet trees and the arrays of [Elias-Fano encoding](/elias-fano-encoding/) store their small counters and low bits in packed arrays. See [succinct data structures](/succinct-data-structures/).
- **Bit-parallel algorithms.** Packing several small values in a word lets one instruction work on all of them, as in [SIMD within a register](/simd-within-a-register/) and in the word RAM algorithms that pack keys for sorting and searching.
- **Hash tables and filters.** Fingerprint filters and counting Bloom filters keep small counters or fingerprints of a few bits each in packed arrays.
- **Network and file formats.** Protocol headers pack flags and short fields into bytes and words; reading them needs the same shift and mask, and the byte order of the format.

Bit packing differs from codes of variable length such as [variable-byte encoding](/variable-byte-encoding/) or Elias-Fano: there, the position of a value depends on the values before it, so random access needs an index, while a packed array with fixed $b$ has direct access.

## References
