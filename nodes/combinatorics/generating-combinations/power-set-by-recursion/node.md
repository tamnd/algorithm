---
tag: 198V88
kind: algorithm
slug: power-set-by-recursion
name: Power set by recursion and binary counting
aliases:
- subset enumeration by binary counter
- binary counting subsets
- include-exclude recursion for subsets
area: combinatorics/generating-combinations
level: intro
summary: Enumerate subsets by counting from 0 to 2^n-1 and reading each bit as membership.
solves: [power-set-enumeration]
model: word-ram
complexity:
  vars: {n: the size of the ground set}
  time: {worst: Θ(2^n), amortized: Θ(1)}
  space: {extra: Θ(n)}
properties: {in_place: true, deterministic: true, comparison: false, recursive: true}
prereqs: [power-set-enumeration, recursion]
see_also: [power-set-enumeration, binary-counter-increment, aggregate-method, binary-reflected-gray-code, loopless-gray-code-generation, submask-enumeration, recursive-combination-generation, constant-amortized-time-generation]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.1, Generating all n-tuples (Algorithm M, mixed-radix generation, with all radices equal to 2)
  - book: isbn:9780125192606
    title: Albert Nijenhuis and Herbert S. Wilf, Combinatorial Algorithms for Computers and Calculators, second edition, Academic Press, 1978
    locator: Chapter 1, Next subset of an n-set
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration, and Search, CRC Press, 1999
    locator: Chapter 2, Section 2.2, Subsets
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Section 16.1, Aggregate analysis (incrementing a binary counter)
---

This algorithm lists all $2^n$ subsets of $[n] = \{1, \ldots, n\}$ in binary counting order. It keeps the subset as a bit vector $x$, with $x_j = 1$ when element $j + 1$ is in the set, and adds $1$ to $x$ as a binary number at each step. A recursive form, "first the subsets without an element, then the subsets with it", gives the same list. It solves [power set enumeration](/power-set-enumeration/) in $\Theta(2^n)$ total time, so it takes $O(1)$ amortized time for each subset, but one step can take $\Theta(n)$ time.

## In plain words

Write a row of $n$ boxes, one for each item. A box holds $1$ if the item is in the set and $0$ if it is not. Start with all boxes at $0$: this is the empty set. Then count up in binary, as an odometer does. To add one, go from the right end: change each $1$ to $0$ until you find a $0$, and change that $0$ to $1$. When all boxes hold $1$, you have seen every set.

The recursive form asks one question for each item: "is this item in the set?" It first answers "no" and lists all sets for that answer, then answers "yes" and lists all sets again. With $n$ items it answers $n$ questions, so it finds $2^n$ sets.

## The problem

Given $n \ge 0$, visit each subset of $[n]$ exactly once. The current subset is a bit vector $x[0 \ldots n-1]$ that the algorithm changes in place, with $x[j] = 1$ if and only if $j + 1$ is in the subset. This is [power set enumeration](/power-set-enumeration/).

## The algorithm

SUBSETS-COUNTER is the iterative form. The extra entry $x[n] = 0$ is a sentinel: it stops the scan of line L5. SUBSETS-RECURSIVE is the recursive form. It fixes $x[n-1]$ first and $x[0]$ last.

```pseudo id=main
SUBSETS-COUNTER(n)                         ▷ x[0 .. n − 1] is the subset, x[n] is a sentinel
L1  x[j] ← 0 for 0 ≤ j ≤ n
L2  loop
L3      visit x[0 .. n − 1]
L4      j ← 0
L5      while x[j] = 1 do x[j] ← 0, j ← j + 1
L6      if j = n then return
L7      x[j] ← 1

SUBSETS-RECURSIVE(n)
L8  EXTEND(n)

EXTEND(i)                                  ▷ x[i .. n − 1] is fixed, choose x[0 .. i − 1]
L9  if i = 0 then visit x[0 .. n − 1], return
L10 x[i − 1] ← 0, EXTEND(i − 1)            ▷ the subsets without element i
L11 x[i − 1] ← 1, EXTEND(i − 1)            ▷ the subsets with element i
```

Lines L4 to L7 are the [binary counter increment](/binary-counter-increment/). The scan of line L5 clears the trailing ones, and line L7 sets the lowest zero. If $x$ holds only ones, the scan reaches the sentinel, and line L6 stops.

## Example

Take $n = 3$. The table writes $x$ as $x[2]\,x[1]\,x[0]$, so it reads as a binary number.

| visit | $x$ | subset | $j$ after L5 | writes in L5 and L7 |
| --- | --- | --- | --- | --- |
| 0 | $000$ | $\emptyset$ | 0 | 1 |
| 1 | $001$ | $\{1\}$ | 1 | 2 |
| 2 | $010$ | $\{2\}$ | 0 | 1 |
| 3 | $011$ | $\{1, 2\}$ | 2 | 3 |
| 4 | $100$ | $\{3\}$ | 0 | 1 |
| 5 | $101$ | $\{1, 3\}$ | 1 | 2 |
| 6 | $110$ | $\{2, 3\}$ | 0 | 1 |
| 7 | $111$ | $\{1, 2, 3\}$ | 3 | 3, then stop |

The seven increments write $1 + 2 + 1 + 3 + 1 + 2 + 1 = 11 = 2^4 - 3 - 2$ bits. The last scan clears three more bits and stops at the sentinel.

EXTEND$(3)$ gives the same list. Line L10 sets $x[2] = 0$ and lists the four subsets of $\{1, 2\}$. Then line L11 sets $x[2] = 1$ and lists them again, each with $3$ added.

## Correctness

The counter is correct by a [loop invariant](/loop-invariant/) of line L3: at the $v$-th visit, counted from $0$, the vector $x[0 \ldots n-1]$ is the binary form of $v$, and $x[n] = 0$. Lines L4 to L7 change the binary form of $v$ to the binary form of $v + 1$ when $v < 2^n - 1$, and they stop when $v = 2^n - 1$. So the visits are the binary forms of $0, 1, \ldots, 2^n - 1$, each once. The map from a bit vector to a subset is a bijection, so each subset appears once.

The recursion is correct by [induction](/induction/) on $i$: EXTEND$(i)$ visits the $2^i$ vectors that agree with the fixed part $x[i \ldots n-1]$, in increasing order of their value. The vectors with $x[i-1] = 0$ are all smaller than the vectors with $x[i-1] = 1$, so line L10 before line L11 keeps the order. The full proofs are in the proof file.

## Complexity

**Counter.** Line L7 runs $2^n - 1$ times. The scan of line L5 clears each one bit that line L7 set, plus nothing else, so it also runs $2^n - 1$ times in total, the last $n$ of them in the final step. The total time is $\Theta(2^n)$, which is less than $3$ steps of lines L4 to L7 for each subset on average. This is the [aggregate method](/aggregate-method/) of amortized analysis. Counted by bit writes, the $2^n - 1$ increments write $2^{n+1} - n - 2$ bits.

**Recursion.** EXTEND is called once at each node of a complete binary tree of height $n$, so there are $2^{n+1} - 1$ calls, and the total time is $\Theta(2^n)$.

**Delay.** Both forms are CAT, see [constant amortized time generation](/constant-amortized-time-generation/). They are not loopless. The counter takes $\Theta(n)$ time to go from $0111\cdots1$ to $1000\cdots0$. The recursion returns $n - 1$ levels at the same point.

**Space.** The counter uses $n + 1$ bits and one index. The recursion uses a stack of depth $n$. If each subset is copied as a list, the copies cost $n 2^{n-1}$ elements in total, so the time becomes $\Theta(n 2^n)$.

## Properties

- **In place.** The algorithm changes one vector and does not copy it.
- **Order.** Binary counting order: the subset visited at step $v$ has rank $v = \sum_{j \in S} 2^{j-1}$. So rank and unrank are trivial.
- **Not a Gray code.** One step can change all $n$ bits.
- **The same list.** The counter and the recursion visit the same subsets in the same order.
- **Element order in a step.** At each step, the elements that leave the set are the smallest elements, and one element enters.

## Variants and improvements

- **Loop over integers.** When $n \le w$, run $v$ from $0$ to $2^n - 1$ and test bit $j$ of $v$ with a shift and a mask. The increment is one machine instruction, but a scan over all $n$ bits costs $\Theta(n)$ for each subset. Iterate only over the set bits with the [lowest set bit](/lowest-set-bit/) trick to pay for the size of the subset.
- **Gray code.** Flip only bit $\rho(v)$, the number of trailing zeros of $v$, at step $v$. This gives the [binary reflected Gray code](/binary-reflected-gray-code/), with one change for each step. Focus pointers make it loopless, see [loopless Gray code generation](/loopless-gray-code-generation/).
- **Submasks.** To list the subsets of a set $M$, use $s \leftarrow (s - 1) \wedge M$. See [submask enumeration](/submask-enumeration/).
- **Mixed radix.** With radix $m_j$ in place of $2$ for each position, the same counter lists all tuples $(a_1, \ldots, a_n)$ with $0 \le a_j < m_j$. This is Knuth's Algorithm M.
- **Pruning.** In the recursion, skip a branch when no subset in it can be useful. This is [backtracking](/generic-backtracking-algorithm/), and with a size limit it becomes [recursive combination generation](/recursive-combination-generation/).

## When to use it

Use it when $n$ is small, about $25$ or less, and the program must look at every subset. Use the integer loop when $n$ fits in a word and the subsets are used as bitmasks, as in [bitmask DP](/bitmask-dp/). Use the recursion when the work for each subset can be built up along the path, for example a running sum, or when branches can be cut. Use a Gray code when the work for each subset is an update with the one element that changed.

## Pitfalls

- **Overflow.** In a language with fixed-width integers, `1 << n` overflows when $n$ is the word size. Use a wider type or the bit vector form.
- **Hidden $\Theta(n)$ work.** A loop that tests all $n$ bits of each $v$, or a recursion that copies the current list at each call, costs $\Theta(n 2^n)$, not $\Theta(2^n)$.
- **Shared state.** The visit sees the vector that the algorithm will change. If the caller stores the subsets, it must copy each one.
- **The empty ground set.** For $n = 0$ there is exactly one subset, the empty set. The loop must visit once and stop.
- **Bit and element numbers.** Bit $j$ stands for element $j + 1$. Mixing $0$-based bits and $1$-based elements is a common error.

## Implementations

## History

Binary counting as a way to list subsets is old and has no single inventor. In the computer literature, the first chapter of Nijenhuis and Wilf (1975, second edition 1978) treats the listing of all subsets of an $n$-set. Knuth treats it in Section 7.2.1.1 as the case $m_j = 2$ of mixed-radix generation. The aggregate analysis of the binary counter, which shows the constant amortized cost, is a standard first example of amortized analysis.

## References
