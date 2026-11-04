---
tag: MX3208
kind: problem
slug: bit-reversal
name: Bit reversal
aliases:
- reverse bits
- bit-reversal permutation
area: techniques/bit-tricks
level: core
summary: Reversing the order of the bits of an integer, used in FFT data reordering.
model: word-ram
complexity:
  vars: {w: the word size in bits}
  time: {worst: O(log w)}
prereqs: [bitwise-operations, bitmask]
see_also: [bit-reversal-permutation, iterative-fft, endianness-conversion, bit-matrix-transpose, table-lookup, bit-interleaving]
sources:
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition
    locator: Section 7-1, Reversing Bits and Bytes
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.1.3, Bitwise Tricks and Techniques (bit reversal by swaps of bit fields)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 30, Polynomials and the FFT (the iterative FFT and the procedure BIT-REVERSE-COPY)
---

Bit reversal is the problem of reversing the order of the $w$ bits of a word, so that bit $i$ moves to bit $w - 1 - i$. It is the index map of the [bit-reversal permutation](/bit-reversal-permutation/) that puts the input of an [iterative FFT](/iterative-fft/) in order, and a step of many codes and hashes. On the [word RAM](/word-ram/) it takes $O(\log w)$ steps by swapping halves, quarters and so on with masks, or a few lookups with a [table](/table-lookup/) of byte reversals. The related problem of reversing the bytes, not the bits, is [endianness conversion](/endianness-conversion/).

## In plain words

Write a number in binary with a fixed number of digits, for example 32. Read the digits from right to left and write them down in that order. The new string of digits is the answer. So 1 with 32 digits, which has its only 1 at the right end, becomes the number with its only 1 at the left end.

The slow way moves one digit at a time. A faster way swaps the two halves of the word, then swaps the two halves of each half, and so on, until single digits are swapped. Each of these steps works on the whole word at once, so a 32-digit word needs only five steps.

## Definition

**Input.** A word $x = \sum_{i=0}^{w-1} x_i 2^i$ with bits $x_i \in \{0, 1\}$ and a word size $w \ge 1$.

**Output.**
$$ \operatorname{rev}_w(x) = \sum_{i=0}^{w-1} x_i \, 2^{w-1-i} . $$

The map $\operatorname{rev}_w$ is a bijection on $\{0, \ldots, 2^w - 1\}$ and an involution: $\operatorname{rev}_w(\operatorname{rev}_w(x)) = x$. It keeps the number of ones. It is linear over $\mathrm{GF}(2)$: $\operatorname{rev}_w(x \oplus y) = \operatorname{rev}_w(x) \oplus \operatorname{rev}_w(y)$, and the same holds for AND and OR, since it only moves bits.

## Variants

- **Reverse the low $k$ bits.** For $x < 2^k$ and $k \le w$, $\operatorname{rev}_k(x) = \operatorname{rev}_w(x) \gg (w - k)$. This is the form in the FFT, where $k = \lg n$ for an array of $n = 2^k$ items.
- **Reverse each byte.** Reverse the bits inside each byte and keep the order of the bytes. This is $\operatorname{rev}_w$ followed by a byte swap.
- **Reversed increment.** Given $\operatorname{rev}_k(i)$, compute $\operatorname{rev}_k(i + 1)$. A loop over $i$ in FFT order uses it to avoid a full reversal at each step.
- **The permutation of an array.** Move each item $A[i]$ to $A[\operatorname{rev}_k(i)]$, for $n = 2^k$ items. Swapping $A[i]$ and $A[\operatorname{rev}_k(i)]$ for each $i < \operatorname{rev}_k(i)$ does it in place. See the [bit-reversal permutation](/bit-reversal-permutation/).
- **Byte reversal.** Reversing the order of the bytes, not of the bits, is [endianness conversion](/endianness-conversion/).

## Examples

| $w$ | $x$ | binary of $x$ | $\operatorname{rev}_w(x)$ |
| --- | --- | --- | --- |
| 3 | 1 | 001 | 4 = 100 |
| 3 | 6 | 110 | 3 = 011 |
| 8 | 0x0D | 00001101 | 0xB0 = 10110000 |
| 16 | 13 | 0000000000001101 | 0xB000 = 1011000000000000 |
| 32 | 1 | a single 1 at bit 0 | 0x80000000 |
| 32 | 0x12345678 | 0001 0010 0011 0100 0101 0110 0111 1000 | 0x1E6A2C48 |

For $w = 3$ the reversals of $0, 1, \ldots, 7$ are $0, 4, 2, 6, 1, 5, 3, 7$, the order in which an iterative radix-2 FFT of 8 points reads its input.

## Known algorithms

- **Bit by bit.** Shift the bits out of $x$ at the bottom and into the result at the bottom, $w$ times. $O(w)$ steps.
- **Swap stages.** With $w = 2^k$, swap adjacent bits, then adjacent pairs, then nibbles, and so on: for 32 bits,

  ```
  x = (x & 0x55555555) << 1 | (x >> 1) & 0x55555555
  x = (x & 0x33333333) << 2 | (x >> 2) & 0x33333333
  x = (x & 0x0F0F0F0F) << 4 | (x >> 4) & 0x0F0F0F0F
  x = (x << 24) | ((x & 0xFF00) << 8) | ((x >> 8) & 0xFF00) | (x >> 24)
  ```

  The first three lines reverse the bits inside each byte, and the last line reverses the order of the four bytes. In all $\lg w$ stages of $O(1)$ word operations each, so $O(\log w)$ time. Warren gives code of this form in Section 7-1.
- **Table lookup.** Keep a table of the 256 reversed bytes. Reverse each byte of $x$ with one lookup, and put the results in the opposite byte order: $w/8$ lookups, shifts and ORs. With a table of $2^b$ entries the cost is $\lceil w/b \rceil$ lookups. See [table lookup](/table-lookup/).
- **Multiply and modulo for one byte.** For an 8-bit $b$, the expression $((b \cdot \mathtt{0x0202020202}) \mathbin{\&} \mathtt{0x010884422010}) \bmod 1023$ equals $\operatorname{rev}_8(b)$ with 64-bit arithmetic. The multiplication makes five shifted copies of the byte, the mask keeps one or two bits of each copy, and the remainder modulo $2^{10} - 1$ adds the 10-bit groups of the product, which brings the kept bits together in reversed order.
- **Hardware.** Some instruction sets have one instruction for it, for example RBIT on ARM. Where there is only a byte-swap instruction, the first three lines above followed by that instruction do the job.

## Bounds

- **Upper bound.** $O(\log w)$ time on the [word RAM](/word-ram/) with shifts and Boolean operations, by the swap stages. With a table of $2^{w/c}$ entries, $O(c)$ time; so $O(1)$ time with $2^{\varepsilon w}$ words of table for a fixed $\varepsilon > 0$.
- **Lower bound.** This page claims only the trivial $\Omega(1)$ in the word RAM.
- **Hardware model.** As a circuit, $\operatorname{rev}_w$ is only wiring: it needs no gates at all, which is why processors can offer it as a one-cycle instruction.

## Reductions

- **To the bit-reversal permutation.** One call for each index, or a reversed increment, gives the order of an FFT input.
- **To byte swap.** $\operatorname{rev}_w(x) = \operatorname{bswap}(r_8(x))$, where $r_8$ reverses the bits inside each byte; the swap stages compute $r_8$ in $\lg 8 = 3$ stages.
- **To [bit matrix transposition](/bit-matrix-transposition/).** Both are fixed permutations of bit positions, and both are done by a sequence of masked swaps of bit fields. Knuth treats these swaps, and general bit permutations, in Section 7.1.3.

## Applications

- **The FFT.** The iterative Cooley-Tukey FFT first puts the input in bit-reversed order (BIT-REVERSE-COPY in CLRS), or produces its output in that order. See [iterative FFT](/iterative-fft/).
- **Cyclic redundancy checks.** Many CRC standards process the bits of each byte from the least significant bit, so code that works from the most significant bit reverses the polynomial or the data. See [table-driven CRC](/table-driven-crc/).
- **Bitboards.** In board games, reversing a [bitboard](/bitboard/) mirrors the position, which lets one routine handle moves in two opposite directions.
- **Van der Corput sequence.** The reversals $\operatorname{rev}_k(i) / 2^k$ for $i = 0, 1, 2, \ldots$ spread points evenly over $[0, 1)$, a base-2 low-discrepancy sequence.

## References
