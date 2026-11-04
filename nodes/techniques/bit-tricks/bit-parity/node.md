---
tag: 5ZBQV5
kind: problem
slug: bit-parity
name: Bit parity
aliases:
- parity of a word
- parity bit
area: techniques/bit-tricks
level: intro
summary: Computing whether a word has an odd or even number of 1-bits, by XOR-folding or table lookup.
prereqs: [bitwise-operations, population-count]
see_also: [parity-bit, parity-problem, kernighan-popcount, swar-popcount, table-lookup, gray-code, ac0, error-detection]
sources:
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition, Addison-Wesley (2013)
    locator: Chapter 5, Section 5-2 (Parity)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley (2011)
    locator: Section 7.1.3 (Bitwise tricks and techniques), the parts on sideways addition and on the parity function
  - url: https://graphics.stanford.edu/~seander/bithacks.html
    title: Sean Eron Anderson, Bit Twiddling Hacks
    locator: sections Computing parity (naive, by lookup table, by multiply, in parallel)
  - paper: doi:10.1007/BF01744431
    title: Merrick Furst, James B. Saxe and Michael Sipser, Parity, circuits, and the polynomial-time hierarchy, Mathematical Systems Theory 17(1), 1984
    locator: the main theorem (parity is not computed by constant-depth polynomial-size circuits)
---

The parity of a $w$-bit word $x$ is $\nu(x) \bmod 2$: 1 if $x$ has an odd number of 1-bits, and 0 if the number is even. Equivalently, it is the exclusive-or of all bits of $x$. The standard method folds the word in half with XOR and shift, $\lg w$ times, which costs $\Theta(\log w)$ word operations; a [lookup table](/table-lookup/), one multiplication, or a hardware flag can make it cheaper. Parity is the basis of the [parity bit](/parity-bit/) for [error detection](/error-detection/), and a classic example of a function that constant-depth circuits cannot compute.

## In plain words

Count the ones in the binary form of a number and ask only whether the count is odd or even. For 180, which is 10110100, there are four ones, so the parity is even.

You do not need the full count. Exclusive-or of two bits tells you whether the pair has an odd number of ones. So you can cut the word in half, combine the two halves with exclusive-or, and the shorter result has the same parity as the whole word. Do this again and again until one bit is left. That bit is the answer.

## Definition

**Input.** A $w$-bit word $x = (x_{w-1} \ldots x_0)_2$. Signed words are read through their [two's complement](/twos-complement/) bit pattern, so the answer depends on $w$ for negative values.

**Output.**
$$\operatorname{parity}(x) = x_0 \oplus x_1 \oplus \cdots \oplus x_{w-1} = \nu(x) \bmod 2,$$
where $\nu$ is the [population count](/population-count/).

**Laws.** For words $x$ and $y$: $\operatorname{parity}(x \oplus y) = \operatorname{parity}(x) \oplus \operatorname{parity}(y)$, so parity is a linear map from $\{0,1\}^w$ to $\{0,1\}$ over the field of two elements. Shifts that drop no 1-bits keep the parity. For $1 \le s \le w/2$, the low $s$ bits of $x \oplus (x \gg s)$ have the same parity as the low $2s$ bits of $x$, because bit $i < s$ of the result is $x_i \oplus x_{i+s}$; this is the folding step. The bits of the result above position $s - 1$ do not matter for the later steps.

**Even and odd parity bits.** An *even parity bit* for $x$ is $\operatorname{parity}(x)$, so that $x$ with this bit appended has an even number of 1-bits. An *odd parity bit* is $1 - \operatorname{parity}(x)$.

## Variants

- **Parity of a long bit string.** XOR all words together, then take the parity of the one word that remains, by the linearity law.
- **Parity of each byte.** A [SWAR](/simd-within-a-register/) version folds inside each byte, for example with shifts of 4, 2 and 1 and a mask.
- **Prefix parity.** Compute, for each position $i$, the parity of the bits at positions $i$ and above. The doubling steps $x \gets x \oplus (x \gg 1)$, $x \gets x \oplus (x \gg 2)$, $x \gets x \oplus (x \gg 4)$, and so on up to $w/2$, compute all of them at once. This is the conversion from [Gray code](/gray-code/) to binary; see [Gray to binary conversion](/gray-to-binary-conversion/).
- **Parity of a set of chosen bits.** $\operatorname{parity}(x \wedge m)$ for a mask $m$. This is one row of a [parity-check matrix](/parity-check-matrix/) applied to $x$, and one output bit of an [LFSR](/lfsr/) or a CRC.

## Examples

**Folding, 8 bits.** $x = 180 = 10110100_2$, with four 1-bits.

| step | $x$ after the step |
|---|---|
| start | 10110100 |
| $x \gets x \oplus (x \gg 4)$ | 10111111 |
| $x \gets x \oplus (x \gg 2)$ | 10010000 |
| $x \gets x \oplus (x \gg 1)$ | 11011000 |

The low bit is 0, so the parity is even. The high bits are garbage and are masked off with $x \wedge 1$.

**The nibble table in a constant.** The 16-bit constant `0x6996` $= 0110\,1001\,1001\,0110_2$ has as its bit $k$ the parity of $k$, for $0 \le k < 16$. So after the word is folded to 4 bits, $(\texttt{0x6996} \gg x) \wedge 1$ is the parity. For the 16-bit $x = $ `0xB4E7`: $x \oplus (x \gg 8)$ has low byte `0x53`, a second fold by 4 gives the low nibble $6 = 0110_2$, and bit 6 of `0x6996` is 0. So the parity is even, which agrees with $\nu(x) = 10$.

**Negative values.** As a 32-bit pattern, $-1$ has parity 0 (32 ones); as an 8-bit pattern it also has parity 0 (8 ones); as a 7-bit pattern it would have parity 1.

## Known algorithms

Costs are word operations on the [word RAM](/word-ram/) with $w$-bit unsigned words.

| method | operations | notes |
|---|---|---|
| loop over all bits | $\Theta(w)$ | XOR each bit into an accumulator |
| [Kernighan's loop](/kernighan-popcount/) with a toggle | $\Theta(\nu(x))$ iterations | $p \gets 1 - p$ each time $x \gets x \wedge (x - 1)$ |
| XOR folding | $2 \lg w + 1$ | shifts $w/2, w/4, \ldots, 1$, then $\wedge 1$ |
| folding to 4 bits, then `0x6996` | $2 \lg w - 1$ | the last two folds are replaced by one shift of a constant |
| byte table | $w/8$ lookups, or $\lg w - 3$ folds and one lookup | a table of 256 bits or bytes |
| one multiplication | 8 for $w = 32$ or $w = 64$ | $x \gets x \oplus (x \gg 1)$; $x \gets x \oplus (x \gg 2)$; $x \gets (x \wedge \texttt{0x11111111}) \cdot \texttt{0x11111111}$; return $(x \gg 28) \wedge 1$; for $w = 64$ use the 64-bit constant and shift by 60 |
| [population count](/population-count/) | 1 popcount and one AND | fast when the machine has `POPCNT` |
| hardware | 1 | GCC and Clang `__builtin_parity`; on x86 the parity flag covers only the low 8 bits of a result |

**Why the multiplication works.** After the two folds, bit $4j$ of $x$ is the parity of the original bits $4j$ to $4j + 3$. The mask keeps these bits, so $x$ has the digit $p_j \in \{0, 1\}$ in each 4-bit field $j$. Multiplying by `0x11111111` $= \sum_{k=0}^{7} 2^{4k}$ puts $\sum_{j \le 7} p_j \le 8$ in the top nibble without carries between nibbles (each partial sum is at most 8 < 16). The low bit of that sum, bit 28 of the product, is the parity of all 32 bits. For $w = 64$ the top nibble can reach 16 and wrap, but the nibbles below it still hold sums of at most 15, so no carry reaches bit 60, and the low bit of the top nibble is still the parity.

## Bounds

**Upper bound.** $\Theta(\log w)$ operations with XOR and shifts only, by folding. With one multiplication, 8 operations for $w = 32$ and $w = 64$. With a table of $2^{w/c}$ entries, $O(c)$ lookups for a constant $c$.

**Lower bound for constant-depth circuits.** Parity of $w$ bits has no circuit of constant depth and polynomial size with unbounded fan-in AND, OR and NOT gates; this is the theorem of Furst, Saxe and Sipser (also proved by Ajtai), and puts parity outside [AC0](/ac0/). A fixed number of AND, OR, NOT, add and shift instructions forms such a circuit, so without multiplication, tables or a parity instruction, the number of operations must grow with $w$.

**Lower bound for queries.** Each of the $w$ bits can flip the answer, so any method that reads single bits must read all $w$ of them. See the [parity problem](/parity-problem/).

## Reductions

- **Parity reduces to popcount**: $\operatorname{parity}(x) = \nu(x) \wedge 1$.
- **Parity of $n$ bits reduces to parity of one word**: XOR the $\lceil n / w \rceil$ words, then take the parity of the result.
- **Gray to binary contains parity**: the low bit of the Gray-to-binary conversion of $g$ is $\operatorname{parity}(g)$.

## Applications

- **Error detection.** A [parity bit](/parity-bit/) detects each error that flips an odd number of bits, for example in memory words and serial links. A [Hamming code](/hamming-code/) uses several parities of masked bits.
- **CRCs and LFSRs.** Each feedback bit of an [LFSR](/lfsr/) is the parity of the bits selected by its taps.
- **Gray codes.** The parity of the current word tells which bit the [binary reflected Gray code](/binary-reflected-gray-code/) flips next: the lowest bit when the parity is even, and the bit just left of the lowest 1-bit when it is odd.
- **Linear algebra over two elements.** A dot product of two bit vectors modulo 2 is $\operatorname{parity}(x \wedge y)$, used in [Gaussian elimination over XOR](/xor-gaussian-elimination/).
- **Permutations.** The parity of a permutation is a different notion; see [permutation parity](/permutation-parity/).

## References
