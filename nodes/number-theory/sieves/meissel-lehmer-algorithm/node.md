---
tag: 2SPPAE
kind: algorithm
slug: meissel-lehmer-algorithm
name: Meissel-Lehmer algorithm
aliases:
- Meissel-Lehmer method
- Lehmer prime counting
- LMO algorithm
area: number-theory/sieves
level: advanced
summary: Computes pi(x) as phi(x, a) + a - 1 - P2(x, a) with a = pi(x^(1/3)), splitting phi into ordinary and special leaves. This form takes O(x^(2/3) log x) time and O(x^(2/3)) memory.
solves: [prime-counting-function]
model: word-ram
complexity:
  vars: {x: the input, y: the cube root x^(1/3), z: the bound x / y}
  time: {worst: "O(x^(2/3) log x)"}
  space: {extra: "O(x^(2/3))"}
properties: {deterministic: true, recursive: false}
prereqs: [legendre-phi-function]
see_also: [legendre-phi-function, prime-counting-function, lucy-hedgehog-prime-counting, sieve-of-eratosthenes, segmented-sieve, fenwick-tree, linear-sieve, mobius-function]
sources:
  - paper: doi:10.1090/S0025-5718-1985-0777285-5
    title: J. C. Lagarias, V. S. Miller and A. M. Odlyzko, Computing pi(x), the Meissel-Lehmer method, Mathematics of Computation 44(170), 1985
    locator: pages 537 to 560 (the leaf decomposition of phi(x, a), the O(x^(2/3) / log x) time bound, and the sieving of the special leaves)
  - paper: doi:10.1090/S0025-5718-96-00674-6
    title: M. Deléglise and J. Rivat, Computing pi(x), the Meissel, Lehmer, Lagarias, Miller, Odlyzko method, Mathematics of Computation 65(213), 1996
    locator: Section 3, formula (4); Section 4 (P2); Section 5, Truncation Rule 2 and Lemma 5.2 (ordinary and special leaves)
  - paper: doi:10.1215/ijm/1255455259
    title: D. H. Lehmer, On the exact number of primes less than a given limit, Illinois Journal of Mathematics 3(3), 1959
    locator: the formula with P2 and P3 and the computation of pi(10^10)
  - paper: doi:10.1007/BF01444045
    title: E. D. F. Meissel, Ueber die Bestimmung der Primzahlenmenge innerhalb gegebener Grenzen, Mathematische Annalen 2, 1870
    locator: pages 636 to 642 (the formula with the P2 correction)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 3.7.1, Combinatorial method
---

The Meissel-Lehmer algorithm computes the [prime-counting function](/prime-counting-function/) $\pi(x)$ without listing the primes up to $x$. With $y = \lfloor x^{1/3} \rfloor$ and $a = \pi(y)$ it uses $\pi(x) = \phi(x, a) + a - 1 - P_2(x, a)$, where $\phi$ is [Legendre's phi function](/legendre-phi-function/) and $P_2(x, a)$ counts the $n \le x$ that are products of two primes larger than $y$. The recursion for $\phi$ is cut off as soon as the divisor passes $y$, which leaves about $x^{2/3}$ terms, and these are answered with a sieve up to $x^{2/3}$. The form on this page, due in essence to Lagarias, Miller and Odlyzko, takes $O(x^{2/3} \log x)$ word operations and $O(x^{2/3})$ memory.

## In plain words

Counting the primes up to a trillion by listing them all is slow. This method counts them in a smarter way.

It first counts the numbers up to the bound that have no small prime factor. Such a number is 1, a large prime, or a product of two large primes, because three large primes already multiply to more than the bound. So the method subtracts the products of two large primes, which is easy with a table of prime counts for smaller bounds.

The count of numbers without small factors breaks into many smaller counts of the same kind. The method breaks them down only until they become cheap, and then answers all the small counts together with one sieve.

## The problem

The input is an integer $x$. The output is $\pi(x)$, the number of primes $p \le x$. The cost model is the [word RAM](/word-ram/) with words of $\Theta(\log x)$ binary digits: arithmetic, comparisons and array access on numbers up to $x$ cost one step. Memory is counted in words.

Write $p_1 = 2 < p_2 = 3 < \cdots$ for the primes, $\phi(t, b)$ for the number of $1 \le n \le t$ with no prime factor among $p_1, \ldots, p_b$, and $\mathrm{lpf}(m)$ for the least prime factor of $m \ge 2$.

## The algorithm

The steps rest on three identities, proved under Correctness. With $y = \lfloor x^{1/3} \rfloor$, $a = \pi(y)$ and $z = \lfloor x / y \rfloor$:

1. $\pi(x) = \phi(x, a) + a - 1 - P_2(x, a)$ with $P_2(x, a) = \sum_{y < p \le \sqrt x} \left( \pi(\lfloor x/p \rfloor) - \pi(p) + 1 \right)$.
2. $\phi(x, a) = S_0 + S$, with the ordinary leaves $S_0 = \sum_{m \le y} \mu(m) \lfloor x/m \rfloor$ and the special leaves $S = -\sum_{b=0}^{a-1} \sum \mu(m)\, \phi(\lfloor x / (m p_{b+1}) \rfloor, b)$, the inner sum over squarefree $m$ with $y / p_{b+1} < m \le y$ and $\mathrm{lpf}(m) > p_{b+1}$.
3. Every argument $\lfloor x / (m p_{b+1}) \rfloor$ of a special leaf and every $\lfloor x/p \rfloor$ in $P_2$ is at most $z$.

So one sieve over $[1, z]$ answers everything. The values $\phi(n, b)$ for $n \le z$ are prefix counts of the numbers that survive the first $b$ rounds of the [sieve of Eratosthenes](/sieve-of-eratosthenes/), kept in a [Fenwick tree](/fenwick-tree/) $F$ so that a round can delete numbers and a query can count a prefix, each in $O(\log z)$ steps.

```pseudo id=main
MEISSEL-LEHMER(x)                           ▷ returns π(x)
L1  if x < 2 then return 0
L2  y ← ⌊x^(1/3)⌋, z ← ⌊x / y⌋
L3  sieve [1 .. z]: lpf, the primes p1 < p2 < ⋯, the table π, and μ on [1 .. y]; a ← π(y)
L4  φ ← Σ_{m ≤ y} μ(m) · ⌊x / m⌋             ▷ the ordinary leaves S0
L5  F ← Fenwick tree with F[n] = 1 for 1 ≤ n ≤ z
L6  for b ← 0 to a − 1 do                     ▷ F marks the n ≤ z free of p1, …, pb
L7      for each squarefree m with ⌊y / p_{b+1}⌋ < m ≤ y and lpf(m) > p_{b+1} do
L8          φ ← φ − μ(m) · F.prefix(⌊x / (m · p_{b+1})⌋)   ▷ a special leaf, φ(x / (m p_{b+1}), b)
L9      set F[k] ← 0 for each multiple k of p_{b+1} in [1 .. z] with F[k] = 1
L10 P2 ← Σ over primes y < p ≤ ⌊√x⌋ of (π(⌊x / p⌋) − π(p) + 1)
L11 return φ + a − 1 − P2
```

Lines L7 and L8 run before line L9 in each round, so the queries of round $b$ see the numbers free of $p_1, \ldots, p_b$ exactly. Line L9 deletes each number at most once over the whole run, which is what keeps the sieve cost near $z \log z$. Nothing here is recursive: the recursion for $\phi$ appears only in the proof.

## Example

Take $x = 1000$. Then $y = 10$, $a = \pi(10) = 4$ with primes 2, 3, 5, 7, and $z = 100$.

**Ordinary leaves.** $S_0 = \sum_{m \le 10} \mu(m) \lfloor 1000/m \rfloor = 1000 - 500 - 333 - 200 + 166 - 142 + 100 = 91$.

**Special leaves.** The pairs $(b, m)$ of line L7 and their terms are:

| $b$ | $p_{b+1}$ | $m$ | $\mu(m)$ | $n = \lfloor 1000 / (m p_{b+1}) \rfloor$ | $-\mu(m)\,\phi(n, b)$ |
|---|---|---|---|---|---|
| 0 | 2 | 7 | $-1$ | 71 | $\phi(71, 0) = 71$ |
| 1 | 3 | 5 | $-1$ | 66 | $\phi(66, 1) = 33$ |
| 1 | 3 | 7 | $-1$ | 47 | $\phi(47, 1) = 24$ |
| 2 | 5 | 7 | $-1$ | 28 | $\phi(28, 2) = 9$ |

For $b = 3$ there is no $m \le 10$ with $\mathrm{lpf}(m) > 7$ and $m > 10/7$, since 11 is already too big. So $S = 137$ and $\phi(1000, 4) = 91 + 137 = 228$.

**The correction.** The primes $10 < p \le 31$ are 11, 13, 17, 19, 23, 29, 31, and the terms $\pi(\lfloor 1000/p \rfloor) - \pi(p) + 1$ are $20, 16, 10, 8, 6, 2, 1$; for instance $p = 11$ gives $\pi(90) - \pi(11) + 1 = 24 - 5 + 1 = 20$. So $P_2 = 63$, and $\pi(1000) = 228 + 4 - 1 - 63 = 168$.

## Correctness

**Identity 1.** Every $n$ counted by $\phi(x, a)$ is 1, a prime $p > y$, or a product $pq$ of primes $y < p \le q$, because $p_{a+1} > x^{1/3}$ makes a product of three such primes exceed $x$. The primes give $\pi(x) - a$, and for each prime $y < p \le \sqrt x$ the partners $q$ are the primes in $[p, x/p]$, which number $\pi(\lfloor x/p \rfloor) - \pi(p) + 1$.

**Identity 2.** Expand $\phi(x, a) = \sum_{d \mid p_1 \cdots p_a} \mu(d) \lfloor x/d \rfloor$. The terms with $d \le y$ are $S_0$, since every squarefree $m \le y$ has all its prime factors at most $p_a$. For $d > y$, list the prime factors of $d$ in decreasing order and stop at the first prefix product that exceeds $y$: this writes $d = m \cdot p_{b+1} \cdot r$ in exactly one way, with $m \le y < m p_{b+1}$, $\mathrm{lpf}(m) > p_{b+1}$, and $r$ a squarefree product of primes below $p_{b+1}$. Summing over $r$ with the same inclusion-exclusion gives $\mu(m p_{b+1}) \phi(\lfloor x/(m p_{b+1}) \rfloor, b) = -\mu(m) \phi(\ldots, b)$.

**Identity 3 and the sieve.** $m p_{b+1} > y$ gives $\lfloor x / (m p_{b+1}) \rfloor \le \lfloor x/y \rfloor = z$, and $p > y$ gives $\lfloor x/p \rfloor \le z$. At the start of round $b$ the tree holds 1 exactly at the $n \le z$ free of $p_1, \ldots, p_b$, so its prefix sum up to $n$ is $\phi(n, b)$. The full proof is below.

## Complexity

**Sieve.** Line L3 is a [linear sieve](/linear-sieve/) up to $z = O(x^{2/3})$: $O(x^{2/3})$ steps and words.

**Ordinary leaves.** Line L4 costs $O(y) = O(x^{1/3})$.

**Special leaves.** For each of the $a$ rounds, line L7 scans at most $y$ values of $m$, so there are at most $a y \le x^{2/3}$ queries, each $O(\log z)$ steps.

**Deletions.** Line L9 visits $z / p$ multiples of $p$ per round, $O(z \log \log z)$ in all by Mertens' theorem, and deletes each $n \le z$ at most once, at $O(\log z)$ steps per deletion.

**Correction.** Line L10 costs $O(\sqrt x)$.

**Total.** $O(x^{2/3} \log x)$ word operations and $O(x^{2/3})$ words of memory. These bounds are proved; they use no conjecture. Using $a = \pi(y) = O(y / \log y)$ (Chebyshev's bound) the query count improves to $O(x^{2/3} / \log x)$, but the deletions still cost $O(x^{2/3} \log x)$ in this simple form.

## Properties

- **Exact.** The answer is an exact count, not an estimate, and no conjecture is used.
- **Sublinear.** The work is about $x^{2/3}$ instead of the $x \log \log x$ of a full sieve.
- **Deterministic and iterative.** No randomness, no recursion, no floating point except for an initial guess of the cube root that is then corrected in integers.
- **Offline.** The special leaves are answered in order of $b$, interleaved with the sieve, not one at a time.

## Variants and improvements

- **Meissel (1870).** Meissel used $a = \pi(x^{1/3})$ and the $P_2$ correction, and evaluated $\phi$ by hand with tables, reaching $\pi(10^9)$, with a small error.
- **Lehmer (1959).** Lehmer took $a = \pi(x^{1/4})$, which needs a $P_3$ term as well, and computed $\pi(10^{10})$ on a computer.
- **Lagarias, Miller and Odlyzko (1985).** They introduced the truncation into ordinary and special leaves and the segmented sieve for the special leaves: $O(x^{2/3} / \log x)$ time and $O(x^{1/3} \log^2 x \log \log x)$ space, with $y$ a little above $x^{1/3}$.
- **Deléglise and Rivat (1996).** They split the special leaves further and answered many at once: $O(x^{2/3} / \log^2 x)$ time and $O(x^{1/3} \log^3 x \log \log x)$ space, and computed $\pi(10^{18})$. Later work by Gourdon, and the primecount program of Kim Walisch, refined and parallelized this method; it is used for the largest exact values of $\pi(x)$ known.
- **Segmentation.** Sieving $[1, z]$ in blocks of length about $y$, as in the [segmented sieve](/segmented-sieve/), cuts the memory to about $x^{1/3}$ words.
- **Analytic methods.** Lagarias and Odlyzko gave a method with $O(x^{1/2 + \varepsilon})$ time based on the Riemann zeta function; it is asymptotically faster but harder to implement exactly.
- **Simpler sublinear methods.** The [Lucy_Hedgehog method](/lucy-hedgehog-prime-counting/) takes $O(x^{3/4} / \log x)$ time and $O(\sqrt x)$ memory with a few lines of code.

## When to use it

Use it to compute one value of $\pi(x)$ for $x$ from about $10^{10}$ up to about $10^{14}$ in this simple form, and well beyond with the Deléglise-Rivat refinements and segmentation. For $x$ up to $10^9$ or so, a [segmented sieve](/segmented-sieve/) that counts is simpler; for programming contest bounds near $10^{11}$ the [Lucy_Hedgehog method](/lucy-hedgehog-prime-counting/) is often enough. To list the primes, or to count them in many short ranges, use a sieve.

## Pitfalls

- **The integer cube root.** $x^{1/3}$ in floating point can be off by one near perfect cubes. The proof needs $p_{a+1} > x^{1/3}$ and $y^3 \le x$, so correct the guess in integers.
- **Counting 1.** $\phi(x, a)$ counts $n = 1$; that is the $-1$ in the formula.
- **The order of a round.** Answer the special leaves of round $b$ before deleting the multiples of $p_{b+1}$; the other order gives $\phi(n, b + 1)$.
- **Deep recursion.** Coding the recursion for $\phi$ directly makes an exponential call tree and overflows the stack in languages with small stacks; the leaf sum avoids both.
- **Overflow.** $m \cdot p_{b+1}$ and the sums $S_0$ and $S$ fit in a word, but intermediate values in $S_0$ can be negative; use signed integers of the full width.

## Implementations

## History

Legendre's formula of 1808 counts primes through $\phi(x, \pi(\sqrt x))$ but needs about $2^{\pi(\sqrt x)}$ terms. In 1870 the astronomer Ernst Meissel added the $P_2$ correction, which allows $a = \pi(x^{1/3})$, and computed $\pi(10^8)$ by hand, and later $\pi(10^9)$, a value that turned out slightly too small. In 1959 D. H. Lehmer simplified and extended the method and computed $\pi(10^{10})$ on an IBM 701, a value later found to be too large by one. In 1985 Lagarias, Miller and Odlyzko turned the method into an algorithm with a proved bound of $O(x^{2/3} / \log x)$ time, and in 1996 Deléglise and Rivat improved it by a further logarithmic factor.

## References
