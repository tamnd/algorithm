---
tag: GPR00G
kind: algorithm
slug: sieve-of-atkin
name: Sieve of Atkin
aliases:
- Atkin sieve
- Atkin-Bernstein sieve
area: number-theory/sieves
level: advanced
summary: Finds the primes up to n by counting, modulo 2, the representations of each number by 4x^2 + y^2, 3x^2 + y^2 or 3x^2 - y^2, then removing non-squarefree numbers. The basic form takes Θ(n) time.
solves: [primes-up-to-n]
model: word-ram
complexity:
  vars: {n: the bound}
  time: {worst: "Θ(n)"}
  space: {extra: "Θ(n)"}
properties: {deterministic: true, recursive: false}
prereqs: [sieve-of-eratosthenes]
see_also: [sieve-of-eratosthenes, primes-up-to-n, segmented-sieve, linear-sieve, wheel-factorization, sieve-of-sundaram, quadratic-residue, integer-square-root]
sources:
  - paper: doi:10.1090/S0025-5718-03-01501-1
    title: A. O. L. Atkin and D. J. Bernstein, Prime sieves using binary quadratic forms, Mathematics of Computation 73(246), 2004
    locator: pages 1023 to 1030; Section 3 (Algorithms 3.1 to 3.3), Section 5 (the O(N / log log N) bound), Section 6 (Theorems 6.1 to 6.3)
  - url: https://cr.yp.to/primegen.html
    title: D. J. Bernstein, primegen
    locator: the description of the library, which uses the sieve of Atkin
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 3.2, Sieving (the sieve of Eratosthenes and its refinements, for comparison)
---

The sieve of Atkin lists the primes up to $n$ by using quadratic forms instead of multiples. For a squarefree number $m$ coprime to 6, Atkin and Bernstein proved that $m$ is prime exactly when it has an odd number of representations $m = 4x^2 + y^2$ (if $m \equiv 1, 5 \pmod{12}$), $m = 3x^2 + y^2$ (if $m \equiv 7$), or $m = 3x^2 - y^2$ with $x > y$ (if $m \equiv 11$), in positive integers. So the sieve flips a flag once for each pair $(x, y)$ with a value up to $n$, and then clears the multiples of $p^2$ for each prime $p \ge 5$ to remove the numbers that are not squarefree. The basic form takes $\Theta(n)$ word operations; with a wheel modulo 60 and segmentation, Atkin and Bernstein got $O(n / \log \log n)$ operations and $n^{1/2 + o(1)}$ memory.

## In plain words

The sieve of Eratosthenes crosses out the multiples of each prime. The sieve of Atkin uses a different test. It looks at certain sums of squares, such as four times a square plus another square, and for each number counts how many ways it can be written that way. A prime, of the right kind, can be written in an odd number of ways; a product of two or more different primes always in an even number of ways.

So the sieve walks through all small pairs of numbers, computes the sum for each pair, and flips a switch at that sum. Numbers whose switch ends up on are prime, except for those divisible by the square of a prime, which a short second pass removes. Then 2 and 3 are added by hand.

## The problem

The input is an integer $n$; the output is the increasing list of the primes $p \le n$, the problem of [listing the primes up to n](/primes-up-to-n/). The cost model is the [word RAM](/word-ram/) with words of $\Theta(\log n)$ binary digits: arithmetic, comparisons and array access on numbers up to $n$ cost one step. Memory is counted in words and flags; the output list is not counted.

## The algorithm

The sieve rests on three theorems of Atkin and Bernstein (Theorems 6.1, 6.2 and 6.3 of their paper). Let $m$ be a squarefree positive integer.

1. If $m \equiv 1 \pmod 4$, then $m$ is prime if and only if $\#\{(x, y) : x > 0, y > 0, 4x^2 + y^2 = m\}$ is odd.
2. If $m \equiv 1 \pmod 6$, then $m$ is prime if and only if $\#\{(x, y) : x > 0, y > 0, 3x^2 + y^2 = m\}$ is odd.
3. If $m \equiv 11 \pmod{12}$, then $m$ is prime if and only if $\#\{(x, y) : x > y > 0, 3x^2 - y^2 = m\}$ is odd.

Every $m$ coprime to 6 lies in one of the classes $1, 5, 7, 11 \pmod{12}$; the classes 1 and 5 are covered by the first theorem, 7 by the second and 11 by the third. Array $F[0 \ldots n]$ holds one flag per number.

```pseudo id=main
SIEVE-OF-ATKIN(n)                           ▷ returns the primes p ≤ n
L1  if n < 2 then return the empty list
L2  F[0 .. n] ← false
L3  for each x ≥ 1, y ≥ 1 with m = 4x² + y² ≤ n do if m mod 12 ∈ {1, 5} then flip F[m]
L4  for each x ≥ 1, y ≥ 1 with m = 3x² + y² ≤ n do if m mod 12 = 7 then flip F[m]
L5  for each x > y ≥ 1 with m = 3x² − y² ≤ n do if m mod 12 = 11 then flip F[m]
L6  for r ← 5 to ⌊√n⌋ do
L7      if F[r] then set F[k] ← false for each multiple k of r² with k ≤ n   ▷ r is prime here
L8  return the primes 2 and 3 that are ≤ n, then each m in [5, n] with F[m]
```

After lines L3 to L5, $F[m]$ is the parity of the number of representations of $m$ by its form, so it is right for every squarefree $m$ coprime to 6. Lines L6 and L7 then clear every $m$ divisible by $p^2$ for a prime $p \ge 5$; numbers divisible by 4 or 9 are never flipped, because they are not coprime to 6. In line L5, $3x^2 - y^2$ grows as $y$ falls, so for each $x$ the loop runs $y = x - 1, x - 2, \ldots$ until the value exceeds $n$, and $x$ needs to go only while $3x^2 - (x-1)^2 = 2x^2 + 2x - 1 \le n$.

## Example

Take $n = 50$. The numbers in $[5, 50]$ coprime to 6, with their representations:

| $m$ | $m \bmod 12$ | form | pairs $(x, y)$ | parity | after L7 |
|---|---|---|---|---|---|
| 5, 13, 17, 29, 37, 41 | 1 or 5 | $4x^2 + y^2$ | one each, such as $(1, 1)$, $(1, 3)$, $(2, 1)$ | odd | prime |
| 25 | 1 | $4x^2 + y^2$ | $(2, 3)$ | odd | cleared, $25 = 5^2$ |
| 49 | 1 | $4x^2 + y^2$ | none | even | not prime |
| 7, 19, 31, 43 | 7 | $3x^2 + y^2$ | $(1, 2)$, $(1, 4)$, $(3, 2)$, $(3, 4)$ | odd | prime |
| 11, 23, 47 | 11 | $3x^2 - y^2$ | $(2, 1)$, $(3, 2)$, $(4, 1)$ | odd | prime |
| 35 | 11 | $3x^2 - y^2$ | none | even | not prime |

So the output is 2, 3 and the 13 primes above, 15 in all, which is $\pi(50)$. The number 25 shows why line L7 is needed: it is not squarefree, and its one representation would make it look prime. A squarefree composite such as $65 = 5 \cdot 13 \equiv 5 \pmod{12}$ has the two representations $4 \cdot 2^2 + 7^2$ and $4 \cdot 4^2 + 1^2$, an even number, so it is never marked.

## Correctness

After lines L3 to L5, for $5 \le m \le n$ coprime to 6, $F[m]$ is true exactly when the number of representations of $m$ by the form of its class is odd; every other flag is false. Line L7 handles $r$ in increasing order. When it reaches $r$, every non-squarefree $m \le n$ coprime to 6 with a prime square factor $q^2$, $q < r$, is already cleared, so $F[r]$ is true only for primes $r$ by the three theorems. Hence lines L6 and L7 clear exactly the non-squarefree numbers coprime to 6, and by the theorems the remaining flags mark exactly the primes in $[5, n]$. The full proof is below.

## Complexity

**Pairs.** The pairs of line L3 lie in the quarter ellipse $4x^2 + y^2 \le n$, of area $\pi n / 8$, so there are at most about $0.39 n$ of them, each costing $O(1)$; line L4 has at most about $\pi n / (4\sqrt 3) \approx 0.45 n$ pairs. For line L5, each $y < \sqrt{n/2}$ allows the $x$ in $(y, \sqrt{(n + y^2)/3}\,]$, at most $\sqrt{n}$ values, and the region has area less than $0.3 n$; so line L5 makes $O(n)$ steps, including the one failed test that ends each $y$ loop and the outer loop over $x \le \sqrt{n/2} + 1$.

**Squares.** Lines L6 and L7 cost $O(\sqrt n + \sum_{r \ge 5} n / r^2) = O(n)$.

**Total.** $\Theta(n)$ word operations and $n + 1$ flags of memory. These bounds are proved and use no conjecture; the three theorems are proved by Atkin and Bernstein from the arithmetic of $\mathbb{Z}[i]$, $\mathbb{Z}[\omega]$ and $\mathbb{Z}[\sqrt 3]$. The basic form is no better asymptotically than the [sieve of Eratosthenes](/sieve-of-eratosthenes/), whose $\Theta(n \log \log n)$ grows extremely slowly; the gain comes only with the wheel below.

## Properties

- **One flip per pair.** Each pair $(x, y)$ is handled once, with no inner loop over primes; the only prime-dependent pass is the cheap square removal.
- **Few composites touched.** Composites with an even number of representations, and numbers divisible by 2 or 3, are never written at all.
- **Deterministic and iterative.** No randomness and no recursion.
- **Segmentable.** For a fixed $x$, the values $4x^2 + y^2$ in a range of $m$ form a contiguous range of $y$, so the pairs can be enumerated block by block, as in the [segmented sieve](/segmented-sieve/).

## Variants and improvements

- **The wheel modulo 60.** Atkin and Bernstein work with the 16 classes $d$ modulo 60 coprime to 60 ($1, 13, 17, 29, 37, 41, 49, 53$ for $4x^2 + y^2$; $7, 19, 31, 43$ for $3x^2 + y^2$; $11, 23, 47, 59$ for $3x^2 - y^2$), and trace only the pairs $(x \bmod 60, y \bmod 60)$ that can hit each class, so multiples of 5 are skipped too.
- **The asymptotic version.** With a wheel $W$ equal to 12 times the primes from 5 up to about $\sqrt{\log n}$, the fraction of useful pairs drops to $O(1 / \log \log n)$, which gives $O(n / \log \log n)$ operations and $n^{1/2 + o(1)}$ memory: the first sieve to reach both bounds at once.
- **Less memory.** Galway replaced the pair enumeration with methods from the circle problem to get $n^{1/3 + o(1)}$ memory at a small cost in time.
- **Other forms.** Other choices work too, such as $x^2 + y^2$ with $x > y > 0$ for $m \equiv 1 \pmod 4$ or $2x^2 + y^2$ for $m \equiv 3 \pmod 8$.
- **Primegen.** Bernstein's primegen library is the reference implementation; in the paper, the mod 60 sieve found the primes up to $10^9$ in about $2.5 \cdot 10^9$ cycles against $3.3 \cdot 10^9$ for a tuned sieve of Eratosthenes on the same machine.

## When to use it

Use it when you want a fast, carefully tuned prime generator and are willing to write the mod 60 tracing code, or when you use an existing implementation such as primegen. For most uses, a [segmented](/segmented-sieve/) [sieve of Eratosthenes](/sieve-of-eratosthenes/) with a wheel is simpler and, in modern well tuned code, about as fast or faster. The basic mod 12 version on this page is mainly of teaching value: it is $\Theta(n)$ but usually slower in practice than a plain sieve of Eratosthenes.

## Pitfalls

- **Forgetting the squares.** The parity test is only valid for squarefree numbers; without lines L6 and L7, numbers like 25, 121 or $5 \cdot 7^2$ come out as primes when their count is odd.
- **The condition $x > y$.** Line L5 must use $x > y > 0$; counting all $x, y > 0$ with $3x^2 - y^2 = m$ gives the wrong parity.
- **The residue tests.** Each form must flip only the numbers in its own classes; $4x^2 + y^2$ also hits multiples of 3 and numbers $\equiv 9 \pmod{12}$, which must be skipped.
- **2 and 3.** They are never flagged and must be added by hand, but only when they are at most $n$.
- **Loop bounds.** The $y$ loop of line L5 has to run downward from $x - 1$ and stop when the value exceeds $n$; running $y$ upward and stopping at the first value below 1 misses pairs.

## Implementations

## History

A. O. L. Atkin and Daniel J. Bernstein developed the sieve around the turn of the millennium; their paper appeared in Mathematics of Computation in 2004. It answered a question of Paul Pritchard, who had asked whether the primes up to $n$ can be listed with $o(n)$ operations and $O(n^\alpha)$ memory for some $\alpha < 1$. Bernstein's primegen library implements it.

## References
