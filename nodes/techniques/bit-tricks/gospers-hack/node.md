---
tag: EEBZ0F
kind: algorithm
slug: gospers-hack
name: Gosper's hack
aliases:
- Gosper's hack for combinations
- next bit permutation with same popcount
- snoob
area: techniques/bit-tricks
level: core
summary: Compute the next integer with the same number of set bits in a few arithmetic operations.
solves: [next-same-popcount]
model: word-ram
complexity:
  vars: {w: the word size in bits, n: the size of the ground set, k: the size of each subset}
  time: {worst: O(1), average: O(1), best: O(1)}
  space: {extra: O(1)}
history:
  year: 1972
  people: [Bill Gosper]
  note: Item 175 of HAKMEM, MIT AI Memo 239, February 1972.
prereqs: [twos-complement, lowest-set-bit, bitmask]
see_also: [next-same-popcount, colexicographic-order, k-subset-enumeration, lexicographic-combinations, submask-enumeration, population-count]
sources:
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition
    locator: Section 2-1, Manipulating Rightmost Bits, subsection A Novel Application and Figure 2-1 (the function snoob)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.1.3, Bitwise Tricks and Techniques; Section 7.2.1.3, Generating all combinations
  - url: "https://dspace.mit.edu/handle/1721.1/6086"
    title: Michael Beeler, R. William Gosper and Richard Schroeppel, HAKMEM, MIT Artificial Intelligence Laboratory, AI Memo 239, February 1972
    locator: Item 175 (Gosper)
---

Gosper's hack computes, from a nonzero word $x$, the smallest integer larger than $x$ with the same number of 1-bits, using one negation, one AND, one addition, one XOR, one shift, one division and one OR. It solves the [next number with same popcount](/next-same-popcount/) problem in $O(1)$ time on the [word RAM](/word-ram/). When the word is read as a [bitmask](/bitmask/) of a set, repeated calls list all $k$-element subsets of $\{0, \ldots, n-1\}$ in increasing numeric order, which is [colexicographic order](/colexicographic-order/). Bill Gosper published it in 1972 as item 175 of HAKMEM, and Warren gives it under the name snoob ("same number of one bits").

## In plain words

Write the number in binary. Find the lowest group of 1-bits that stand side by side. Move the top bit of that group one place to the left. Then move the other bits of the group down to the very bottom of the number.

For example, 1011100 becomes 1100011. The lowest group was 111. Its top bit moved one place up, and the two other bits went to the bottom.

The number of 1-bits does not change. The result is the next larger number with that many 1-bits, because the change happens as low in the number as it can, and the bits below it are as small as they can be. The trick does this with a few arithmetic steps and no loop.

## The problem

The input is a word $x$ of $w$ bits, read as an unsigned integer with $0 < x < 2^w$. Let $k$ be the number of 1-bits of $x$, its [population count](/population-count/). The output is the least integer $y > x$ with exactly $k$ 1-bits. If $y \ge 2^w$, so that no such word exists, the output is not defined, and the caller must stop before it reaches this case. This is the [next number with same popcount](/next-same-popcount/) problem.

## The algorithm

All operations are on unsigned $w$-bit words, modulo $2^w$. The operation $-x$ is the [two's complement](/twos-complement/) negation, so $x \mathbin{\&} (-x)$ is the [lowest set bit](/lowest-set-bit/) of $x$.

```pseudo id=main
GOSPER-NEXT(x)                     ▷ x ≠ 0, a w-bit unsigned word
L1  smallest ← x AND (−x)          ▷ the lowest 1-bit of x, as a power of 2
L2  ripple ← x + smallest          ▷ the carry clears the lowest block of 1s and sets the 0 above it
L3  ones ← x XOR ripple            ▷ the block of 1s and the bit above it
L4  ones ← (ones >> 2) / smallest  ▷ move the block to the bottom, two bits shorter
L5  return ripple OR ones
```

Write $x$ as $x = a \cdot 2^{t+m+1} + (2^m - 1) \cdot 2^t$ with $m \ge 1$ and $t \ge 0$: there are $t$ trailing zeros, then the lowest block of $m$ ones, then a 0 at bit $t + m$, then the high part $a$. Line L1 gives $2^t$. Line L2 adds $2^t$ at the bottom of the block, so the carry runs through the $m$ ones, clears them, and sets bit $t + m$. Line L3 marks every bit that line L2 changed: the $m$ ones and bit $t + m$, which is $m + 1$ ones starting at bit $t$. Line L4 divides this by $2^{t+2}$, which drops the $t$ low zeros and two of the $m + 1$ ones and leaves $m - 1$ ones at the bottom. Line L5 puts these $m - 1$ ones under the new high part. Unsigned division by $2^t$ is a right shift by $t$, so line L4 is the same as `ones >> (t + 2)`.

## Example

Take $x = 92 = 1011100_2$. Here $t = 2$, $m = 3$ and the high part is $a = 1$.

| line | value | binary |
| --- | --- | --- |
| L1 smallest | 4 | 0000100 |
| L2 ripple = 92 + 4 | 96 | 1100000 |
| L3 ones = 92 XOR 96 | 60 | 0111100 |
| L4 ones >> 2 | 15 | 0001111 |
| L4 15 / 4 | 3 | 0000011 |
| L5 96 OR 3 | 99 | 1100011 |

Both 92 and 99 have four 1-bits, and no integer from 93 to 98 has four 1-bits.

Start from $x = 7 = 111_2$ and call GOSPER-NEXT while the result is below $2^5 = 32$. The calls give 7, 11, 13, 14, 19, 21, 22, 25, 26 and 28, in binary 00111, 01011, 01101, 01110, 10011, 10101, 10110, 11001, 11010 and 11100. These are the $\binom{5}{3} = 10$ subsets of size 3 of $\{0, 1, 2, 3, 4\}$, in increasing order. The next call returns 35, which is at least 32, and the loop stops.

## Correctness

Let $x = a \cdot 2^{t+m+1} + (2^m - 1) \cdot 2^t$ as above, and assume that bit $t + m$ is inside the word, that is $t + m < w$. Then GOSPER-NEXT returns
$$ z = (a \cdot 2 + 1) \cdot 2^{t+m} + (2^{m-1} - 1). $$
The value $z$ has $\operatorname{pop}(a) + 1 + (m - 1) = \operatorname{pop}(x)$ ones and $z > x$, because the highest bit where $z$ and $x$ differ is bit $t + m$, and $z$ has a 1 there. It is the least such integer. Let $y > x$ have the same number of ones and let $p$ be the highest bit where $y$ and $x$ differ, so that $y$ has a 1 and $x$ a 0 at bit $p$. If $p < t$, then $y$ keeps all ones of $x$ and adds one more, a contradiction. The bits $t$ to $t + m - 1$ of $x$ are ones, so $p \ge t + m$. If $p > t + m$, then $z$ agrees with $x$ above bit $t + m$, has a 0 at bit $p$ and so is less than $y$. If $p = t + m$, then $y$ agrees with $z$ at bit $t + m$ and above, and its low $t + m$ bits must hold $m - 1$ ones; the least such value is $2^{m-1} - 1$, which is the low part of $z$. So $z \le y$. The full proof, with each line of the pseudocode, is below.

## Complexity

- **Time.** Five lines, each a fixed number of word operations: one negation, one AND, one addition, one XOR, one shift, one division and one OR. On the [word RAM](/word-ram/), with unit-cost division, the time is $O(1)$ in each case.
- **Space.** Three extra words.
- **Listing all subsets of size $k$.** Starting at $2^k - 1$ and stopping at the first result $\ge 2^n$ takes $\binom{n}{k}$ calls, so $\Theta(\binom{n}{k})$ time for all of them, which is $O(1)$ for each subset produced. This needs $n < w$, so that the last call does not overflow; see the pitfalls.

The division is the slow step on most processors. A version with a count of [trailing zeros](/trailing-zero-count/) replaces line L4 with `ones ← ones >> (ctz(x) + 2)`, which is one instruction on most current machines.

## Properties

- **Branch-free.** The five lines have no test and no loop. The time does not depend on the value of $x$.
- **Colexicographic.** For subsets of a fixed size, increasing numeric order of the masks is [colexicographic order](/colexicographic-order/) of the sets, so the calls list the subsets in that order.
- **Unsigned arithmetic.** The method needs wrap-around addition and a logical right shift. With signed words, line L4 can shift in copies of the sign bit.
- **Deterministic and in place.** It uses three words of state and no table.

## Variants and improvements

- **Shift instead of divide.** Replace line L4 with `ones ← (x XOR ripple) >> (ctz(x) + 2)`, where ctz is the [trailing zero count](/trailing-zero-count/). In C, this shift can reach $w + 1$ positions when the block reaches the top of the word, and a shift by $w$ or more is undefined; the loop bound must stop before that call.
- **Variant of de Kloet.** Warren gives in Section 2-1 a second version of the same idea, due to David de Kloet, that also uses one division.
- **Previous number with the same popcount.** Apply GOSPER-NEXT to the complement: if $y = \text{GOSPER-NEXT}(\lnot x)$ in $w$ bits, then $\lnot y$ is the largest number below $x$ with the same number of ones. Complementing reverses the order and keeps the number of zeros fixed.
- **Other orders.** Lexicographic order, [revolving-door Gray order](/combination-gray-code-generation/) and loopless methods such as [Ehrlich's](/ehrlich-loopless-combinations/) list the same subsets in other orders. See [k-subset enumeration](/k-subset-enumeration/).

## When to use it

Use Gosper's hack to loop over all subsets of size $k$ of a set with fewer than $w$ elements, as in a [bitmask DP](/bitmask-dp/) that works layer by layer on the size of the set, or in a brute force over all ways to choose $k$ items. It costs a few cycles for each subset and needs no array. For sets larger than one word, or when each successor must differ from the last in only two elements, use a [Gray code for combinations](/combination-gray-code-generation/) instead. To loop over all subsets of a given set, not of a given size, use [submask enumeration](/submask-enumeration/).

## Pitfalls

- **Zero input.** For $x = 0$, line L1 gives smallest $= 0$ and line L4 divides by zero. Handle $k = 0$ apart: the only subset of size 0 is the empty set.
- **The last combination.** When the lowest block of ones reaches bit $w - 1$, line L2 overflows to 0 and the result has $k - 2$ ones when $k \ge 2$ (for example, with $w = 8$, $x = 11100000_2$ gives $1$). Loop with `while x < (1 << n)` and $n < w$, or check the result, never test only the number of calls.
- **Signed types.** In C or Java, a signed `x` makes `x >> 2` an arithmetic shift, and `x + smallest` can overflow, which is undefined in C. Use unsigned types (`>>>` in Java).
- **Shift by the word size.** In the ctz variant, a shift by $w$ or more is undefined in C and is taken modulo $w$ on x86, so the bad last call can return a wrong value without any error.
- **Wrong loop bound.** The loop `for (x = (1 << k) - 1; x < (1 << n); x = next(x))` needs `1 << n` to fit in the type. With $n = 32$ and 32-bit words, `1 << n` is undefined.

## Implementations

## History

Bill Gosper gave the method as item 175 of HAKMEM, a memo of the MIT Artificial Intelligence Laboratory written by Beeler, Gosper and Schroeppel in February 1972, as a short machine-language program. Warren put it in Section 2-1 of Hacker's Delight under the name snoob, with C code. Knuth treats the operations on the rightmost bits that it uses in Section 7.1.3 of Volume 4A, and the colexicographic order of $k$-subsets in Section 7.2.1.3.

## References
