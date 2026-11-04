---
tag: G8X0J3
kind: algorithm
slug: xor-swap
name: XOR swap
aliases:
- XOR swap algorithm
- exclusive-or swap
area: techniques/bit-tricks
level: intro
summary: Swapping x and y with three XORs, x ^= y, y ^= x, x ^= y, without a temporary; fails if x and y alias the same location.
solves: [swap-two-values]
model: word-ram
complexity:
  vars: {w: the word size in bits}
  time: {worst: Θ(1), average: Θ(1), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false}
prereqs: [bitwise-operations, swap-two-values]
see_also: [xor-linked-list, single-number, bit-manipulation, branchless-programming, in-place-algorithm]
sources:
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition, Addison-Wesley (2013)
    locator: Chapter 2, Section 2-20 (Exchanging Registers)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley (2011)
    locator: Section 7.1.3 (Bitwise tricks and techniques), the algebraic laws of the exclusive-or operation
  - url: https://graphics.stanford.edu/~seander/bithacks.html
    title: Sean Eron Anderson, Bit Twiddling Hacks
    locator: sections Swapping values with XOR, and Swapping individual bits with XOR
  - url: https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf
    title: ISO/IEC 9899:2011 committee draft N1570 (the C11 standard)
    locator: Section 6.5, paragraph 2 (unsequenced side effects on the same object are undefined)
---

The XOR swap exchanges the contents of two words $x$ and $y$ with three [exclusive-or](/bitwise-operations/) assignments, $x \gets x \oplus y$, $y \gets x \oplus y$, $x \gets x \oplus y$, and no temporary variable. It works for words of any width $w$, signed or unsigned, because it uses only the bit patterns and never does arithmetic, so no overflow can occur. It fails when $x$ and $y$ are the same memory location: the first step sets that location to zero. It is one solution of the [swap problem](/swap-two-values/), and on current processors it is seldom faster than a swap through a temporary.

## In plain words

Exclusive-or compares two bit patterns and gives a 1 in each position where they differ. If you combine a pattern with the same key twice, you get the pattern back. The XOR swap uses this. First it stores in the first variable the "difference" of the two values. Then it combines the second variable with that difference, which turns the second value into the first value. Last, it combines the first variable with the new second value, which turns the difference into the second value. No third variable holds anything during the swap.

The trick has one trap. If both names refer to the same place in memory, the first step combines a value with itself, which gives zero, and the value is lost.

## The problem

The input is two cells $A[i]$ and $A[j]$ of a memory, each holding a $w$-bit word. The output is the same memory with the two words exchanged and all other cells unchanged. This is the [swap problem](/swap-two-values/). The indices $i$ and $j$ may be equal; then the memory must not change.

## The algorithm

Here $\oplus$ is bitwise exclusive-or on $w$-bit words. The words may be read as unsigned or as signed in [two's complement](/twos-complement/): the operation only sees the bits.

```pseudo id=main
XOR-SWAP(A, i, j)                      ▷ exchange the words A[i] and A[j]
L1  if i = j then return               ▷ one cell: the XORs would set it to 0
L2  A[i] ← A[i] ⊕ A[j]                 ▷ A[i] holds x ⊕ y
L3  A[j] ← A[i] ⊕ A[j]                 ▷ A[j] holds (x ⊕ y) ⊕ y = x
L4  A[i] ← A[i] ⊕ A[j]                 ▷ A[i] holds (x ⊕ y) ⊕ x = y
```

Write $x$ and $y$ for the old values of $A[i]$ and $A[j]$. After line L2 the cell $A[i]$ holds $x \oplus y$, which records in which bit positions $x$ and $y$ differ. Line L3 flips the bits of $y$ at exactly those positions, so $y$ becomes $x$. Line L4 flips the bits of $x \oplus y$ at the positions where $x$ has a 1, which leaves $y$. The comments give the value after each line. With two plain variables $x$ and $y$ that are known to be distinct objects, line L1 is not needed, and the method is the three statements `x ^= y; y ^= x; x ^= y;`.

## Example

Take $w = 8$, $x = 180 = 10110100_2$ and $y = 105 = 01101001_2$, in two different cells.

| after line | $A[i]$ | $A[j]$ |
|---|---|---|
| start | 10110100 (180) | 01101001 (105) |
| L2 | 11011101 (221) | 01101001 (105) |
| L3 | 11011101 (221) | 10110100 (180) |
| L4 | 01101001 (105) | 10110100 (180) |

Now call it with $i = j$ and without line L1, on a cell that holds 180. Line L2 computes $180 \oplus 180 = 0$. Lines L3 and L4 compute $0 \oplus 0 = 0$. The cell ends with 0, not 180.

## Correctness

The proof uses four laws of $\oplus$ on $w$-bit words, each of which holds bit by bit: it is associative and commutative, $a \oplus 0 = a$, and $a \oplus a = 0$. So $(\{0,1\}^w, \oplus)$ is an abelian group in which each element is its own inverse. If $i \ne j$, then after line L3 the cell $A[j]$ holds $(x \oplus y) \oplus y = x \oplus (y \oplus y) = x \oplus 0 = x$, and after line L4 the cell $A[i]$ holds $(x \oplus y) \oplus x = y \oplus (x \oplus x) = y$. If $i = j$, line L1 returns and the memory does not change. The full proof, with the failure of the version without line L1, is in [the correctness proof](proofs/correctness.md).

## Complexity

The algorithm does one comparison and three XOR operations, each with two loads and one store when the words are in memory. On the [word RAM](/word-ram/) each of these costs one step, so the time is $\Theta(1)$ in every case. The extra space is $\Theta(1)$: no word besides the two cells is written. The three XORs form a chain: each one needs the result of the one before it. A swap through a temporary has two independent loads and two independent stores, and an optimizing compiler often removes a register-to-register swap by renaming, so the XOR form is usually not faster.

## Properties

- **Width and sign.** It works for each word size $w$, and for signed and unsigned words alike, because $\oplus$ acts on each bit position separately and has no carries and no overflow.
- **In place.** It needs no temporary cell. This was the reason to use it on machines with few registers.
- **Not alias-safe.** Without line L1 it sets a cell to zero when $i = j$.
- **Integers only, in practice.** In C, `^` is defined only on integer types. Swapping two floating-point values or two pointers by XOR needs a conversion to an integer type of the same width.

## Variants and improvements

- **Add and subtract.** $x \gets x + y$, $y \gets x - y$, $x \gets x - y$ also swaps, with arithmetic modulo $2^w$ on unsigned words. For $w = 8$, $x = 200$, $y = 100$: $x$ becomes $300 \bmod 256 = 44$, then $y = 44 - 100 \bmod 256 = 200$, then $x = 44 - 200 \bmod 256 = 100$. On signed C integers the first sum can overflow, which is undefined behaviour, so use an unsigned type. It has the same aliasing failure.
- **Conditional swap without a branch.** With a mask $m$ that is all zeros or all ones, $t \gets (x \oplus y) \wedge m$, $x \gets x \oplus t$, $y \gets y \oplus t$ swaps when $m$ is all ones and does nothing when $m = 0$. This form uses a temporary, but it has no branch, which matters in constant-time code and in [branchless programming](/branchless-programming/).
- **Swap of bit fields.** To exchange the $k$-bit fields at positions $p$ and $q$ of one word, set $t \gets ((x \gg p) \oplus (x \gg q)) \wedge (2^k - 1)$, then $x \gets x \oplus ((t \ll p) \vee (t \ll q))$, when the two fields do not overlap.
- **Swap of memory blocks.** Applying the three steps word by word swaps two blocks of equal length that do not overlap.
- **The same identity elsewhere.** The [XOR linked list](/xor-linked-list/) stores $prev \oplus next$ in one field and recovers one address from the other by the same cancellation. The [single number](/single-number/) problem uses $a \oplus a = 0$ in the same way.

## When to use it

Use a temporary in ordinary code: it is clearer, it has no aliasing trap, and compilers make it at least as fast. The XOR swap is useful when no spare register or cell exists, for example in hand-written assembly for a small microcontroller, in a puzzle, or as a teaching example of the group laws of XOR. The masked conditional form is useful when a swap must not depend on a branch.

## Pitfalls

- **Aliasing.** Omitting line L1 and calling the swap on the same cell, for example `swap(&a[i], &a[j])` with `i == j` inside a sorting loop, sets that element to zero. Keep the test of line L1, or use a temporary.
- **One expression in C.** The line `x ^= y ^= x ^= y;` modifies `x` twice between sequence points, which is undefined behaviour in C (C11 Section 6.5, paragraph 2). Write lines L2 to L4 as three statements.
- **Signed add and subtract.** The add-and-subtract variant on `int` overflows for large values, which is undefined in C. The XOR version has no such problem.
- **Assuming it is faster.** On processors with register renaming, the three dependent XORs of lines L2 to L4 take at least three cycles, while a swap through a temporary can cost no instruction at all after the compiler renames the registers.

## Implementations

## History

Warren gives the method, its variants with addition and subtraction, and the swap of fields within a register in Hacker's Delight, Section 2-20. The trick was known among assembly programmers long before; the sources here do not name an inventor.

## References
