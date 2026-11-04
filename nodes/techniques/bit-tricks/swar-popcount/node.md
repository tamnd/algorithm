---
tag: W1VS75
kind: algorithm
slug: swar-popcount
name: SWAR population count
aliases:
- parallel bit count
- Hacker's Delight popcount
- SIMD within a register popcount
area: techniques/bit-tricks
level: core
summary: Computes popcount by summing bits in parallel fields of a word using masks and shifts, in a fixed number of operations.
solves: [population-count]
model: word-ram
complexity:
  vars: {w: the word size in bits, a power of two}
  time: {worst: Θ(log w), average: Θ(log w), best: Θ(log w)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false}
prereqs: [population-count, bitwise-operations, simd-within-a-register]
see_also: [kernighan-popcount, bit-parity, table-lookup, bit-parallelism, hamming-distance, rank-select-dictionary]
sources:
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition, Addison-Wesley (2013)
    locator: Chapter 5, Section 5-1 (Counting 1-Bits)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley (2011)
    locator: Section 7.1.3 (Bitwise tricks and techniques), the part on sideways addition with broadword operations
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Springer (2011)
    locator: Chapter 1, Section 1.8 (Counting the bits and blocks of a word)
  - url: https://graphics.stanford.edu/~seander/bithacks.html
    title: Sean Eron Anderson, Bit Twiddling Hacks
    locator: section Counting bits set, in parallel
---

The SWAR population count computes the number of 1-bits of a $w$-bit word by treating the word as many small counters and adding neighbouring counters in parallel: first 2-bit fields, then 4-bit fields, then bytes, and last all bytes at once with one multiplication. For $w = 32$ or $w = 64$ it takes 12 word operations and no branch and no table. It is the standard software [population count](/population-count/), given in Hacker's Delight Section 5-1, and an example of [SIMD within a register](/simd-within-a-register/). The masks keep each field small enough that no carry crosses into the next field.

## In plain words

Think of the word as a row of tiny counters, one per bit, each holding 0 or 1. Pair them up and add each pair; now you have half as many counters, each holding 0, 1 or 2. Pair those up and add again; now each counter covers four bits and holds at most 4. One more round gives one counter per byte.

The trick is that one subtraction, one addition or one shift acts on all counters of the word at the same time. A mask clears the bits that belong to the neighbour, so the counters never spill into each other. At the end, one multiplication adds all byte counters into the top byte, and a shift moves that sum down.

## The problem

The input is an unsigned $w$-bit word $x$, $0 \le x < 2^w$, where $w$ is a power of two with $8 \le w \le 128$. The output is $\nu(x)$, the number of 1-bits of $x$. All arithmetic is modulo $2^w$, as with an unsigned integer type in C. This is the [population count](/population-count/) problem.

## The algorithm

The masks repeat a pattern over the whole word: $M_1 = (01)^{w/2}_2$, which is `0x5555...5`; $M_2 = (0011)^{w/4}_2$, which is `0x3333...3`; $M_4 = (00001111)^{w/8}_2$, which is `0x0F0F...0F`; and $H = (00000001)^{w/8}_2$, which is `0x0101...01`.

```pseudo id=main
SWAR-POPCOUNT(x)                       ▷ x unsigned, w ∈ {8, 16, 32, 64, 128}, arithmetic mod 2^w
L1  x ← x − ((x ≫ 1) ∧ M₁)             ▷ each 2-bit field holds the count of its 2 bits
L2  x ← (x ∧ M₂) + ((x ≫ 2) ∧ M₂)      ▷ each 4-bit field holds the count of its 4 bits
L3  x ← (x + (x ≫ 4)) ∧ M₄             ▷ each byte holds the count of its 8 bits
L4  return (x · H) ≫ (w − 8)           ▷ the top byte of x · H is the sum of all bytes
```

Line L1 works on each 2-bit field $(b_1 b_0)$, whose value is $2b_1 + b_0$. The term $(x \gg 1) \wedge M_1$ puts $b_1$ in the low bit of the field, and $2b_1 + b_0 - b_1 = b_1 + b_0$, the count of the field. The subtraction never borrows from the next field, because $2b_1 + b_0 \ge b_1$. Line L2 adds the two 2-bit counts of each 4-bit field. Both are masked first, and their sum is at most 4, so it fits. Line L3 adds the two 4-bit counts of each byte. Their sum is at most 8, which fits in 4 bits, so the mask can come after the addition. Line L4 multiplies by $H = \sum_i 2^{8i}$, which adds shifted copies of $x$; the top byte receives the sum of all byte counts.

## Example

Take $w = 16$ and $x = $ `0xB4E7` $= 1011\,0100\,1110\,0111_2$, with $\nu(x) = 10$. Then $M_1 = $ `0x5555`, $M_2 = $ `0x3333`, $M_4 = $ `0x0F0F`, $H = $ `0x0101`.

| after line | $x$ in binary, grouped by fields | hex | the fields as numbers |
|---|---|---|---|
| start | 10 11 01 00 11 10 01 11 | `0xB4E7` | bits |
| L1 | 01 10 01 00 10 01 01 10 | `0x6496` | 1, 2, 1, 0, 2, 1, 1, 2 |
| L2 | 0011 0001 0011 0011 | `0x3133` | 3, 1, 3, 3 |
| L3 | 00000100 00000110 | `0x0406` | 4, 6 |
| L4 | `0x0406` $\cdot$ `0x0101` $\bmod 2^{16}$ $=$ `0x0A06`, shifted right by 8 | `0x000A` | 10 |

The multiplication gives `0x0406` $+$ `0x0406` $\cdot 2^8 = $ `0x40A06`, and the reduction modulo $2^{16}$ drops the byte `0x4`. The top byte `0x0A` is $4 + 6$.

## Correctness

The proof shows by induction over the lines that after line L1, L2 or L3, each field of width $f = 2, 4, 8$ holds the number of 1-bits of the input in that field, written as an ordinary binary number in the field. The base case is line L1, by the computation $2b_1 + b_0 - b_1 = b_1 + b_0$ for each field, with no borrow. Each later line adds two neighbouring fields; the masks make sure each addend lies inside its field, and the sum is at most $f$, which is less than $2^f$, so no carry leaves the field. For line L4, the product $x \cdot H$ is $\sum_i c_i 2^{8i} \cdot \sum_k 2^{8k}$; byte $j$ of the product receives $\sum_{i \le j} c_i \le w \le 128 < 256$, so no carry crosses a byte, and byte $w/8 - 1$ receives $\sum_i c_i = \nu(x)$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

For each fixed $w$ from 8 to 128, the pseudocode does 3 operations in line L1 (shift, AND, subtract), 4 in line L2 (two ANDs, a shift, an add), 3 in line L3 (shift, add, AND) and 2 in line L4 (multiply, shift): 12 operations, with no branch, on every input. On the [word RAM](/word-ram/) each costs one step.

For a general power of two $w$, the same doubling runs until the fields are wide enough to hold the answer $w$.

- **Without multiplication.** Double the field width $\lg w$ times, from 1 to $w$. Each step costs $O(1)$ operations, so the time is $\Theta(\log w)$ in every case. This is the bound in the front matter.
- **With one multiplication.** Double only until the field width $f$ satisfies $2^f > w$; this takes $\lceil \lg \lg (w + 1) \rceil$ steps. Then one multiplication by $\sum_i 2^{fi}$ and one shift by $w - f$ finish. For $w = 8$ to 128 this is $f = 8$ (or $f = 4$ for $w = 8$); for $w = 256$ to 1024 it is $f = 16$.

The extra space is $\Theta(1)$: the masks are constants.

## Properties

- **Branch-free and constant-time.** The same operations run for every input, so the time does not leak $\nu(x)$.
- **No table.** It needs no memory besides a few constants, unlike a [table lookup](/table-lookup/).
- **Fixed width.** The masks depend on $w$, and the final shift is $w - 8$. Code written for 32 bits gives wrong answers on 64-bit inputs.
- **Middle results.** After line L3, each byte holds its own count. Some uses need only these, for example the rank inside a word with a prefix sum by the same multiplication.

## Variants and improvements

- **Without multiplication.** Replace line L4 by $x \gets x + (x \gg 8)$, $x \gets x + (x \gg 16)$, and for $w = 64$ also $x \gets x + (x \gg 32)$, then return $x \wedge 127$. The low byte collects the sum, and the higher bytes hold garbage that the mask removes. For $w = 32$ the mask $63$ is enough, as in Hacker's Delight.
- **A first step with masks on both sides.** Line L1 can be written as $(x \wedge M_1) + ((x \gg 1) \wedge M_1)$. It costs one more AND; the subtraction form saves it.
- **Prefix counts.** The product $x \cdot H$ after line L3 has in byte $j$ the count of bytes 0 to $j$. With a shift and a mask this gives the number of 1-bits below each byte boundary, which is the core of fast rank in [rank and select dictionaries](/rank-select-dictionary/).
- **Arrays of words.** For long arrays, carry-save adders (the Harley-Seal method) combine several words before one SWAR count, and vector registers apply the same idea to 256 or 512 bits at a time.
- **Parity.** Keep only the low bit of the final count, or use the cheaper XOR folding of [bit parity](/bit-parity/).

## When to use it

Use the hardware instruction when the compiler can emit it, for example with `std::popcount` in C++20 or `__builtin_popcountll` with a target that has `POPCNT`; without that target, the compiler falls back to a library routine or to an inline sequence like this one. Use the SWAR method for portable code, for dense words, and when the time must not depend on the data. For sparse words, [Kernighan's loop](/kernighan-popcount/) can be faster.

## Pitfalls

- **Signed type.** If `x` is a signed `int` in C, the right shifts in lines L1 to L3 copy the sign bit for negative values (implementation-defined, C11 Section 6.5.7), and the arithmetic can overflow. Use `uint32_t` or `uint64_t`.
- **Mask of the wrong width.** Writing line L1 with the 32-bit `0x55555555` on a 64-bit word leaves the top half unmasked. Each mask in lines L1 to L3 must fill all $w$ bits.
- **Final shift of the wrong size.** Line L4 must shift by $w - 8$: 24 for 32 bits, 56 for 64 bits. Shifting a 64-bit product by 24 returns the middle bytes.
- **Product in a wider type.** If $x \cdot H$ in line L4 is computed in a type wider than $w$ bits (for example `uint16_t` operands promoted to `int` in C), the high bytes are not dropped, and the shift by $w - 8$ returns the sum plus garbage. Reduce the product modulo $2^w$, for example with a cast, before the shift.
- **Mask after the addition in line L2.** The form $(x + (x \gg 2)) \wedge M_2$ is wrong: before the mask, the neighbour's bits are added in, and the 2-bit counts can carry into the wrong place. Line L3 can mask after the addition only because each 4-bit count is at most 4 and the sum of two is at most 8 < 16.

## Implementations

## History

The method of adding neighbouring fields is old; the sources here do not name an inventor. Hacker's Delight presents the version with the subtraction in the first step and the final multiplication in Section 5-1, and Knuth treats it in Section 7.1.3 under the name sideways addition with broadword operations.

## References
