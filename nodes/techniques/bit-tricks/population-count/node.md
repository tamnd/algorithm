---
tag: TTEQ4K
kind: problem
slug: population-count
name: Population count
aliases:
- popcount
- Hamming weight
- bit count
- sideways sum
area: techniques/bit-tricks
level: intro
summary: Counting the number of 1-bits in the binary representation of an integer.
prereqs: [bitwise-operations, twos-complement]
see_also: [kernighan-popcount, swar-popcount, hamming-weight, hamming-distance, bit-parity, table-lookup, simd-within-a-register, rank-select-dictionary]
sources:
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition, Addison-Wesley (2013)
    locator: Chapter 5, Section 5-1 (Counting 1-Bits)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley (2011)
    locator: Section 7.1.3 (Bitwise tricks and techniques), the part on sideways addition
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Springer (2011)
    locator: Chapter 1, Section 1.8 (Counting the bits and blocks of a word)
  - paper: doi:10.1093/comjnl/bxx046
    title: Wojciech Muła, Nathan Kurz and Daniel Lemire, Faster population counts using AVX2 instructions, The Computer Journal 61(1), 2018
    locator: pp. 111 to 120 (population counts of long arrays, the Harley-Seal method)
  - paper: doi:10.1007/BF01744431
    title: Merrick Furst, James B. Saxe and Michael Sipser, Parity, circuits, and the polynomial-time hierarchy, Mathematical Systems Theory 17(1), 1984
    locator: the main theorem (parity is not computed by constant-depth polynomial-size circuits)
---

The population count of a word is the number of its bits that are 1. For $x = 180 = 10110100_2$ it is 4. Knuth calls it the *sideways sum* and writes $\nu x$; in coding theory it is the [Hamming weight](/hamming-weight/). Methods range from a loop over all $w$ bits, through [Kernighan's loop](/kernighan-popcount/) that runs once per 1-bit and the [SWAR method](/swar-popcount/) with $\Theta(\log w)$ word operations, to a single hardware instruction. It is the core step of the [Hamming distance](/hamming-distance/), of rank queries on [bit vectors](/rank-select-dictionary/), and of set sizes in a [bit set](/bit-set/).

## In plain words

Write a number in binary and count the ones. That count is the population count. The number 180 is 10110100 in binary, which has four ones.

The count says how many members a set has when the set is stored as a row of yes-or-no bits. It also says in how many places two rows differ, after you mark the places where they differ. The task is simple, but it comes up so often in search engines, databases, chess programs and compression that processors have a special instruction for it, and programmers have found many fast ways to compute it without that instruction.

## Definition

**Input.** A $w$-bit word $x = (x_{w-1} \ldots x_1 x_0)_2$, read as an unsigned integer $x = \sum_{i=0}^{w-1} x_i 2^i$ with $0 \le x < 2^w$.

**Output.** The integer
$$\nu(x) = \sum_{i=0}^{w-1} x_i, \qquad 0 \le \nu(x) \le w.$$

**Signed inputs.** A signed $w$-bit integer is counted through its [two's complement](/twos-complement/) bit pattern, so the answer depends on $w$: for $x = -1$ it is $w$. In mathematics, $\nu$ of a negative integer is often defined as $\nu$ of its absolute value, or as $\infty$; say which convention you use.

**Basic laws.** For unsigned words: $\nu(x) = 0$ if and only if $x = 0$; $\nu(2x) = \nu(x)$ when $2x < 2^w$; $\nu(x \wedge y) + \nu(x \vee y) = \nu(x) + \nu(y)$; $\nu(x \oplus y) = \nu(x) + \nu(y) - 2\nu(x \wedge y)$; $\nu(\lnot x) = w - \nu(x)$; and $\nu(x \wedge (x-1)) = \nu(x) - 1$ for $x \ne 0$. Each law holds bit by bit except the last, which holds because $x - 1$ changes exactly the lowest 1-bit of $x$ and the 0-bits below it (see [lowest set bit](/lowest-set-bit/)).

## Variants

- **Parity.** Only $\nu(x) \bmod 2$. It is a separate problem, [bit parity](/bit-parity/), with cheaper methods.
- **Hamming distance.** $d(x, y) = \nu(x \oplus y)$, the number of positions where two words differ.
- **Popcount of an array.** $\sum_j \nu(A[j])$ for a long array, as in the size of a [bit set](/bit-set/) or a bitmap index. Methods that combine several words before counting beat one count per word.
- **Rank.** $\nu(x \wedge (2^k - 1))$, the number of 1-bits below position $k$. A [rank and select dictionary](/rank-select-dictionary/) answers it on long bit vectors.
- **Count in fields.** The count of each byte or each $k$-bit field separately. The [SWAR method](/swar-popcount/) computes these as middle results.
- **Count of 0-bits.** $w - \nu(x)$.

## Examples

| $x$ | binary | $\nu(x)$ |
|---|---|---|
| 0 | 00000000 | 0 |
| 1 | 00000001 | 1 |
| 180 | 10110100 | 4 |
| 255 | 11111111 | 8 |
| 46311 (16-bit, `0xB4E7`) | 1011010011100111 | 10 |
| $2^{64} - 1$ | 64 ones | 64 |
| `0x5555555555555555` | 32 alternating pairs `01` | 32 |

**Distribution.** Among the 256 words of 8 bits, the number with $\nu(x) = k$ is $\binom{8}{k}$: 1, 8, 28, 56, 70, 56, 28, 8, 1 for $k = 0$ to 8. In general, $\sum_{x=0}^{2^w - 1} \nu(x) = w \, 2^{w-1}$, because each of the $w$ positions is 1 in half of the words. For $w = 8$ the sum is 1024, and for $w = 16$ it is 524288.

**Hamming distance.** For $x = $ `0xB4E7` and $y = $ `0x4D2C`, $x \oplus y = 1111100111001011_2$ and $d(x, y) = 11$.

**Signed pitfall.** As a 32-bit pattern, $-1$ has 32 one-bits. Python's `(-1).bit_count()` returns 1, because it counts the bits of the absolute value; `((-1) & 0xFFFFFFFF).bit_count()` returns 32.

## Known algorithms

All bounds count word operations on the [word RAM](/word-ram/) with $w$-bit words.

| method | operations on one word | notes |
|---|---|---|
| loop over all bits | $\Theta(w)$ | test $x \wedge 1$, shift right, repeat $w$ times |
| [Kernighan's loop](/kernighan-popcount/) | $\Theta(\nu(x))$ iterations, $w$ in the worst case | clears the lowest 1-bit each time with $x \wedge (x - 1)$ |
| [table lookup](/table-lookup/) | $w / 8$ lookups with a table of 256 entries | the table costs memory and cache space |
| [SWAR popcount](/swar-popcount/) | $\Theta(\log w)$; 12 operations for $w = 32$ with one multiplication | sums bits in 2-bit, 4-bit and 8-bit fields |
| hardware instruction | 1 | x86-64 `POPCNT`; ARMv8 counts per byte with the vector instruction `CNT` |
| Harley-Seal for arrays | fewer than one count per word | adds words with carry-save adders and counts the carries; Muła, Kurz and Lemire use it with AVX2 |

In C and C++, the portable calls are `__builtin_popcount` (GCC and Clang), `std::popcount` (C++20, unsigned types only) and `stdc_count_ones` (C23). In Java, `Integer.bitCount` and `Long.bitCount` count the two's complement pattern. In Python 3.10 and later, `int.bit_count` counts the bits of the absolute value.

## Bounds

**Upper bound.** $O(\log w)$ word operations with addition, shifts, AND and one multiplication, by the [SWAR method](/swar-popcount/). Without multiplication, $O(\log w)$ operations also suffice: replace the final multiply by $\lg w - 3$ shift-and-add steps. With an instruction for it, $O(1)$.

**Output size.** The answer is a number from 0 to $w$, so it has $\lfloor \lg w \rfloor + 1$ bits.

**Lower bound for constant-depth circuits.** The lowest bit of $\nu(x)$ is the parity of $x$. Parity of $w$ bits has no Boolean circuit of constant depth and polynomial size with unbounded fan-in AND, OR and NOT gates (the class [AC0](/ac0/)); this was proved by Furst, Saxe and Sipser and by Ajtai. A straight-line program of a constant number of AND, OR, NOT, shift and add operations on $w$-bit words is such a circuit, so it cannot compute $\nu$ for all large $w$. This is why the SWAR method needs a number of steps that grows with $w$, or a multiplication, which is not in AC0.

## Reductions

- **Parity reduces to popcount**: parity$(x) = \nu(x) \bmod 2$, with one AND.
- **Hamming distance reduces to popcount**: $d(x, y) = \nu(x \oplus y)$, with one XOR.
- **Popcount reduces to trailing zeros on the isolated suffix**: $\nu(\lnot x \wedge (x - 1)) = $ [ctz](/trailing-zero-count/)$(x)$ for $x \ne 0$. This runs the other way: a fast popcount gives a fast trailing zero count.
- **Popcount of $n$ bits** reduces to $\lceil n / w \rceil$ word popcounts and additions.

## Applications

- **Set sizes.** The size of a set stored as a [bit set](/bit-set/) or [bitmask](/bitmask/), and the size of an intersection $\nu(A \wedge B)$.
- **Similarity.** [Hamming distance](/hamming-distance/) between binary fingerprints, as in [SimHash](/simhash/), and the [Jaccard similarity](/jaccard-similarity/) of two bit sets as $\nu(A \wedge B) / \nu(A \vee B)$.
- **Succinct structures.** Rank on [bit vectors](/bit-vector/) and in [succinct data structures](/succinct-data-structures/).
- **Games.** Counting pieces or mobility on a [bitboard](/bitboard/).
- **Coding.** The weight of a code word and the [parity bit](/parity-bit/).
- **Enumeration.** [Gosper's hack](/gospers-hack/) walks all words with the same popcount.

## References
