---
tag: TVK2SZ
kind: algorithm
slug: kernighan-popcount
name: Kernighan's bit count
aliases:
- Brian Kernighan's method
- clear lowest set bit loop
area: techniques/bit-tricks
level: intro
summary: Repeatedly clears the lowest set bit with x &= x-1, so it runs in time proportional to the number of 1-bits.
solves: [population-count]
model: word-ram
complexity:
  vars: {w: the word size in bits, k: the number of 1-bits of the input}
  time: {worst: Θ(w), best: Θ(1), average: Θ(w)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false}
prereqs: [lowest-set-bit, bitwise-operations, population-count]
see_also: [swar-popcount, bit-parity, power-of-two-test, table-lookup, hamming-weight]
sources:
  - paper: doi:10.1145/367236.367286
    title: Peter Wegner, A technique for counting ones in a binary computer, Communications of the ACM 3(5), 1960
    locator: p. 322 (the whole note)
  - book: isbn:9780131103627
    title: Brian W. Kernighan and Dennis M. Ritchie, The C Programming Language, second edition, Prentice Hall (1988)
    locator: Section 2.10 (Assignment Operators and Expressions), the function bitcount and Exercise 2-9
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition, Addison-Wesley (2013)
    locator: Chapter 2, Section 2-1 (Manipulating Rightmost Bits), and Chapter 5, Section 5-1 (Counting 1-Bits)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley (2011)
    locator: Section 7.1.3 (Bitwise tricks and techniques), the part on sideways addition
---

Kernighan's bit count computes the [population count](/population-count/) $\nu(x)$ of a $w$-bit word by clearing the [lowest set bit](/lowest-set-bit/) with $x \gets x \wedge (x - 1)$ until $x = 0$, and counting the steps. The loop runs exactly $\nu(x)$ times, so it is fast on sparse words and costs $\Theta(w)$ only when most bits are 1. Peter Wegner published the method in 1960, and Kernighan and Ritchie made it widely known through Exercise 2-9 of their C book. It needs an unsigned word: in C, the step on a negative `int` can overflow.

## In plain words

Subtracting one from a binary number turns its last 1 into a 0 and turns all the 0s after it into 1s. The bits before that last 1 do not change. If you now keep only the bits that are 1 in both the old and the new number, the last 1 is gone and everything else is as before.

So each such step removes exactly one 1 from the number. Repeat it until nothing is left, and count the steps. The count is the number of ones. A number with three ones takes three steps, even if the word has 64 bits.

## The problem

The input is an unsigned $w$-bit word $x$, $0 \le x < 2^w$. The output is $\nu(x) = \sum_i x_i$, the number of 1-bits of $x$. This is the [population count](/population-count/) problem. Subtraction is modulo $2^w$, but the algorithm subtracts 1 only from a nonzero word, so no wrap-around occurs.

## The algorithm

```pseudo id=main
KERNIGHAN-POPCOUNT(x)                  ▷ x is an unsigned w-bit word
L1  c ← 0
L2  while x ≠ 0 do
L3      x ← x ∧ (x − 1)                ▷ clear the lowest 1-bit of x
L4      c ← c + 1
L5  return c
```

Write a nonzero $x$ as $x = (\alpha\, 1\, 0^j)_2$: a prefix $\alpha$, the lowest 1-bit at position $j$, and $j$ zeros below it. Then $x - 1 = (\alpha\, 0\, 1^j)_2$, and the AND of the two is $(\alpha\, 0\, 0^j)_2$. Line L3 therefore removes exactly one 1-bit and keeps all the others. Line L4 counts the removals. The loop stops when no 1-bit is left.

## Example

Take $w = 8$ and $x = 180 = 10110100_2$, with $\nu(x) = 4$.

| iteration | $x$ before L3 | $x - 1$ | $x$ after L3 | $c$ after L4 |
|---|---|---|---|---|
| 1 | 10110100 (180) | 10110011 | 10110000 (176) | 1 |
| 2 | 10110000 (176) | 10101111 | 10100000 (160) | 2 |
| 3 | 10100000 (160) | 10011111 | 10000000 (128) | 3 |
| 4 | 10000000 (128) | 01111111 | 00000000 (0) | 4 |

The test of line L2 fails, and line L5 returns 4. A loop over all bits would take 8 iterations for this word.

## Correctness

The loop of line L2 keeps the [invariant](/loop-invariant/) $c + \nu(x) = \nu(x_0)$, where $x_0$ is the input. It holds at the start with $c = 0$. Line L3 lowers $\nu(x)$ by exactly 1, because of the identity $\nu(x \wedge (x - 1)) = \nu(x) - 1$ for $x \ne 0$, and line L4 raises $c$ by 1. When the loop stops, $x = 0$, so $c = \nu(x_0)$. Since $\nu(x)$ drops by exactly 1 in each iteration and starts at $\nu(x_0) \le w$, the loop runs exactly $\nu(x_0)$ times. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $k = \nu(x)$. The loop runs exactly $k$ times, and each iteration does one subtraction, one AND, one addition and one test, each one step on the [word RAM](/word-ram/). So the time is $\Theta(k + 1)$.

- **Worst case.** $x = 2^w - 1$ has $k = w$, so the time is $\Theta(w)$.
- **Best case.** $x = 0$ has $k = 0$, and the time is $\Theta(1)$.
- **Average case.** For $x$ uniform on the $2^w$ words, $\mathbb{E}[k] = w/2$, because each bit is 1 with probability $1/2$. So the expected time is $\Theta(w)$, half the cost of a loop over all bits.
- **Space.** $\Theta(1)$ extra: the counter $c$.

The method wins when the words are known to be sparse, for example the bits of a sparse set. For random words, the [SWAR method](/swar-popcount/) with $\Theta(\log w)$ steps is faster.

## Properties

- **Output-sensitive.** The number of iterations equals the answer.
- **Branchy.** The loop has a data-dependent number of iterations, so its time leaks $\nu(x)$, and the exit branch is hard to predict for random words.
- **Width-free.** The code does not mention $w$ and works for any unsigned width, including arbitrary-precision integers that are not negative.
- **Byproduct.** The value $x \oplus (x \wedge (x - 1))$ in each iteration is the isolated lowest bit, so the same loop enumerates the 1-bits of $x$ in increasing order of position.

## Variants and improvements

- **Clear the lowest 0-bit instead.** The loop $x \gets x \vee (x + 1)$ until $x = 2^w - 1$ runs once per 0-bit, so it computes $w - \nu(x)$ in $\Theta(w - \nu(x))$ iterations. Use it when most bits are 1.
- **Enumerate the members of a set.** Replace line L4 by "visit the index of the bit $x \wedge (-x)$", with a [trailing zero count](/trailing-zero-count/) for the index. This is how one iterates over a [bit set](/bit-set/) or a [bitmask](/bitmask/).
- **Parity.** Replace line L4 by $c \gets 1 - c$ to compute [bit parity](/bit-parity/) in $\nu(x)$ iterations.
- **Power-of-two test.** One step of line L3 tells if $\nu(x) \le 1$: $x \wedge (x - 1) = 0$. See [power-of-two test](/power-of-two-test/).

## When to use it

Use the hardware instruction (`POPCNT`, `__builtin_popcount`, `std::popcount`) when it exists. Use Kernighan's loop when there is no such instruction and the words are sparse, or when the loop also needs the positions of the 1-bits. Use the [SWAR popcount](/swar-popcount/) for dense or random words, and a [table lookup](/table-lookup/) when memory is cheap and the table stays in cache.

## Pitfalls

- **Signed operand in C.** With `int x`, line L3 computes `x - 1`, which overflows when `x == INT_MIN`; signed overflow is undefined behaviour. Declare `x` as `unsigned` or `uint64_t`.
- **Negative numbers in Python.** Python integers have no fixed width, and a negative integer has infinitely many 1-bits in its two's complement form. Line L2 never becomes false: for $x = -1$ the values are $-2, -4, -8, \ldots$. Mask first with `x &= (1 << w) - 1`.
- **Wrong operator in line L3.** Writing `x = x - 1` or `x &= x + 1` does not clear the lowest 1-bit; the right step is `x &= x - 1`.
- **Precedence in C.** In a test such as `if (x & (x - 1) == 0)`, the comparison binds first, so it computes `x & ((x - 1) == 0)`. Write `if ((x & (x - 1)) == 0)`.

## Implementations

## History

Peter Wegner described the method in a short note in Communications of the ACM in 1960, for a machine with the IBM 704 instruction code. Kernighan and Ritchie state the fact that `x &= (x-1)` deletes the rightmost 1-bit in Exercise 2-9 of The C Programming Language and ask for a faster `bitcount`, which is why the loop carries Kernighan's name.

## References
