---
tag: KXGSQH
kind: problem
slug: trailing-zero-count
name: Trailing zero count
aliases:
- count trailing zeros
- ctz
- find first set
- bit scan forward
area: techniques/bit-tricks
level: intro
summary: Counting the zero bits below the least significant 1-bit of an integer.
prereqs: [lowest-set-bit, bitwise-operations]
see_also: [leading-zero-count, de-bruijn-bit-scan, floor-log2, population-count, ruler-sequence, binary-gcd, bit-set, fenwick-tree]
sources:
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition, Addison-Wesley (2013)
    locator: Chapter 5, Section 5-4 (Counting Trailing 0's), and Chapter 2, Section 2-1 (Manipulating Rightmost Bits)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley (2011)
    locator: Section 7.1.3 (Bitwise tricks and techniques), the part on the ruler function
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Springer (2011)
    locator: Chapter 1, Section 1.3 (Operations on low bits or blocks of a word) and Section 1.5 (Computing the index of a single set bit)
  - paper: "Charles E. Leiserson, Harald Prokop and Keith H. Randall, Using de Bruijn Sequences to Index a 1 in a Computer Word, unpublished manuscript, MIT Laboratory for Computer Science, July 1998"
    locator: the whole note (the de Bruijn method for the index of the lowest 1-bit)
---

The trailing zero count $\operatorname{ctz}(x)$ of a nonzero $w$-bit word $x$ is the number of 0-bits below its lowest 1-bit, which is the index of that bit and the exponent of the largest power of two that divides $x$. Knuth calls it the *ruler function* and writes $\rho x$. Software computes it with a binary search in $\Theta(\log w)$ steps, with a [population count](/population-count/) of $\lnot x \wedge (x - 1)$, or in $O(1)$ steps with a multiplication and a small table by the [de Bruijn bit scan](/de-bruijn-bit-scan/); most processors have an instruction for it. The value for $x = 0$ needs a convention, and in C the built-in functions leave it undefined.

## In plain words

Write a number in binary and count the zeros at its right end, up to the first one. For 180, which is 10110100, there are two such zeros. This is also how many times you can halve the number and still get a whole number.

The count tells you where the lowest one sits. Programs use it to find the first free slot in a bitmap, to walk over the members of a set stored as bits, and to strip factors of two in the binary method for the greatest common divisor. Zero has no lowest one, so each program has to decide what the answer for zero is.

## Definition

**Input.** A $w$-bit word $x$, read as an unsigned integer $0 \le x < 2^w$.

**Output.** For $x \ne 0$,
$$\operatorname{ctz}(x) = \max\{\, k \ge 0 : 2^k \text{ divides } x \,\} = \min\{\, i : x_i = 1 \,\},$$
an integer from 0 to $w - 1$. The two forms agree: if the lowest 1-bit is at position $j$, then $x = 2^j \cdot (\text{an odd number})$.

**The zero input.** $\operatorname{ctz}(0)$ is not defined by the formula. The usual convention is $\operatorname{ctz}(0) = w$, which is what the x86 instruction `TZCNT`, C++20 `std::countr_zero` and C23 `stdc_trailing_zeros` return. GCC's `__builtin_ctz(0)` is undefined, and x86 `BSF` leaves its destination undefined for a zero source (it sets the zero flag).

**Signed words.** A signed value is read through its [two's complement](/twos-complement/) bit pattern. For $x \ne 0$ the answer does not depend on $w$ or on the sign: $\operatorname{ctz}(-x) = \operatorname{ctz}(x)$, because $-x = \lnot x + 1$ has the same lowest 1-bit as $x$.

**Find first set.** The function `ffs(x)` of POSIX returns $\operatorname{ctz}(x) + 1$, and 0 for $x = 0$.

## Variants

- **Index of a single set bit.** When $x$ is known to be a power of two, the problem is to compute $\lg x$; the [de Bruijn](/de-bruijn-bit-scan/) and the modulus-37 methods are designed for this case.
- **Trailing ones.** $\operatorname{cto}(x) = \operatorname{ctz}(\lnot x)$, the number of 1-bits at the low end.
- **Lowest set bit as a mask.** $x \wedge (-x) = 2^{\operatorname{ctz}(x)}$ gives the bit itself; see [lowest set bit](/lowest-set-bit/).
- **Opposite end.** The [leading zero count](/leading-zero-count/) counts zeros above the highest 1-bit.
- **2-adic valuation.** For a nonzero integer of any size, $\operatorname{ctz}$ is the 2-adic valuation $v_2(x)$.

## Examples

| $x$ | binary (8 bits) | $\operatorname{ctz}(x)$ | $x \wedge (-x)$ |
|---|---|---|---|
| 1 | 00000001 | 0 | 1 |
| 12 | 00001100 | 2 | 4 |
| 180 | 10110100 | 2 | 4 |
| 128 | 10000000 | 7 | 128 |
| 0 | 00000000 | 8 by convention | 0 |

**The ruler sequence.** For $x = 1, 2, 3, \ldots, 16$, $\operatorname{ctz}(x)$ is $0, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 0, 4$: the heights of the marks on a ruler. See [ruler sequence](/ruler-sequence/).

**Through the population count.** For $x = 180 = 10110100_2$: $x - 1 = 10110011_2$, $\lnot x = 01001011_2$, and $\lnot x \wedge (x - 1) = 00000011_2 = 3$, with two 1-bits. So $\operatorname{ctz}(180) = \nu(3) = 2$.

**The modulus-37 method.** For a 32-bit $x \ne 0$, the 32 values $2^k \bmod 37$ for $k = 0$ to 31 are distinct and nonzero, because 2 has order 36 modulo the prime 37. So a table $T$ of 37 entries with $T[2^k \bmod 37] = k$ gives $\operatorname{ctz}(x) = T[(x \wedge -x) \bmod 37]$. For $x = 180$, $x \wedge -x = 4$ and $4 \bmod 37 = 4$, and $T[4] = 2$. The entry $T[0]$ is free and can hold 32 for $x = 0$.

## Known algorithms

Costs are word operations on the [word RAM](/word-ram/), for $x \ne 0$.

| method | operations | notes |
|---|---|---|
| loop: shift right while the low bit is 0 | $\Theta(\operatorname{ctz}(x) + 1)$, up to $w$ | fast on odd inputs, which are half of all words |
| binary search | $\Theta(\log w)$ | test the low $w/2$ bits, then $w/4$, and so on; for $w = 32$, five tests |
| population count | 3 operations and one popcount | $\operatorname{ctz}(x) = \nu(\lnot x \wedge (x - 1))$; also gives $w$ for $x = 0$ |
| [de Bruijn bit scan](/de-bruijn-bit-scan/) | $O(1)$: negate, AND, multiply, shift, one lookup | a table of $w$ entries |
| modulus 37 (32-bit) | $O(1)$: negate, AND, remainder, one lookup | a table of 37 entries; the remainder is slow on many machines |
| through [floor of log2](/floor-log2/) | $\operatorname{ctz}(x) = \lfloor \lg(x \wedge -x) \rfloor$ | any method for the highest bit works on the isolated bit |
| hardware | 1 or 2 | x86 `BSF` and `TZCNT`; on ARM A64 cores without a count-trailing-zeros instruction, compilers emit `RBIT` then `CLZ` |

**Binary search for $w = 32$.** Set $n \gets 0$. If $x \wedge \texttt{0xFFFF} = 0$, then $n \gets n + 16$ and $x \gets x \gg 16$. Repeat with the masks `0xFF`, `0xF`, `0x3` and `0x1` and the steps 8, 4, 2 and 1. The result is $n$. Each test shows whether the lowest 1-bit lies in the lower half of the remaining window, so after five tests the window has one bit. For $x = 0$ this code returns 31, not 32, so it needs a separate test for zero.

## Bounds

**Upper bound.** $O(1)$ word operations with a multiplication and a table of $w$ words, by the de Bruijn method; $O(\log w)$ without multiplication and without tables, by binary search.

**Relation to popcount.** The identity $\operatorname{ctz}(x) = \nu(\lnot x \wedge (x - 1))$ makes ctz at most as hard as popcount plus three operations. The word $\lnot x \wedge (x - 1)$ has exactly the $\operatorname{ctz}(x)$ low bits set: subtracting 1 turns the trailing zeros into ones and the lowest 1-bit into 0, and the AND with $\lnot x$ clears every bit at or above the old lowest 1-bit.

## Reductions

- **To the index of a power of two.** $\operatorname{ctz}(x) = \lg(x \wedge -x)$ for $x \ne 0$. The word $x \wedge -x$ has one 1-bit, so any method for the position of a single 1-bit solves ctz with two more operations.
- **To the leading zero count.** For $x \ne 0$, $\operatorname{ctz}(x) = w - 1 - \operatorname{clz}(x \wedge -x)$.
- **To bit reversal.** $\operatorname{ctz}(x) = \operatorname{clz}(\operatorname{rev}(x))$, where rev reverses the order of the $w$ bits; this is the ARM route.

## Applications

- **Iterating over a set.** Visit $\operatorname{ctz}(x)$, then clear that bit with $x \gets x \wedge (x - 1)$, until $x = 0$. This lists the members of a [bit set](/bit-set/) or [bitmask](/bitmask/) in increasing order, at one step per member.
- **Binary GCD.** The [binary GCD](/binary-gcd/) algorithm removes all factors of two at once with a shift by ctz.
- **Fenwick trees.** The step $i \gets i + (i \wedge -i)$ of a [Fenwick tree](/fenwick-tree/) moves by the lowest set bit, whose index is ctz.
- **Allocators and schedulers.** Finding the first free block in a bitmap, or the highest-priority ready queue in a priority bitmap.
- **Gray codes.** In the step from $x - 1$ to $x$, the [binary reflected Gray code](/binary-reflected-gray-code/) flips bit $\operatorname{ctz}(x)$.

## References
