---
tag: R02AQ4
kind: problem
slug: gcd-of-array
name: GCD of an array
aliases:
- gcd of many integers
- multi-set GCD
area: number-theory/divisibility-and-gcd
level: core
summary: Compute the gcd of n given integers by folding a two-argument gcd.
prereqs: [greatest-common-divisor, gcd-of-two-integers, euclidean-algorithm]
see_also: [lcm-of-integers, range-gcd-query, extended-euclidean-algorithm, linear-diophantine-equation, polynomial-gcd, gcd-recursion-theorem, binary-gcd, bezouts-identity]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.5.2, The Greatest Common Divisor (the gcd of more than two numbers, computed by repeated two-number gcds)
  - book: isbn:9780387901633
    title: Tom M. Apostol, Introduction to Analytic Number Theory
    locator: Chapter 1, Section 1.8, The greatest common divisor of more than two numbers
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.2, Greatest common divisor (the bound on the number of recursive calls of EUCLID)
---

The GCD of an array is the problem of computing the [greatest common divisor](/greatest-common-divisor/) $\gcd(a_1, \ldots, a_k)$ of a list of integers. The standard method folds the [two-integer gcd](/gcd-of-two-integers/) over the list: $g \leftarrow \gcd(g, a_i)$ for each $i$, starting from $g = 0$, and it may stop as soon as $g = 1$. Because $g$ only shrinks and each step is a run of the [Euclidean algorithm](/euclidean-algorithm/), the total number of division steps telescopes to $O(k + \log \max |a_i|)$, which is no more than reading the input plus one gcd of two numbers.

## In plain words

You have a list of whole numbers and want the largest number that divides all of them. Take the largest common divisor of the first two numbers. Then take the largest common divisor of that answer and the third number, and go on to the end of the list. A number divides everything seen so far exactly when it divides the running answer, so the last running answer is the result. The running answer can only get smaller, and once it reaches one it stays at one, so you can stop early.

## Definition

**Input.** Integers $a_1, \ldots, a_k$ with $k \ge 1$.

**Output.** $G = \gcd(a_1, \ldots, a_k)$: the nonnegative integer that divides each $a_i$ and is divisible by every common divisor of the $a_i$. If not all $a_i$ are 0, $G$ is the largest common divisor; if all are 0, $G = 0$. Signs and zeros do not change the answer: $G = \gcd(|a_1|, \ldots, |a_k|)$, and terms equal to 0 can be dropped.

**Cost models.** On the [word RAM](/word-ram/) the $a_i$ fit in $w$-bit words and each arithmetic operation costs one unit; the answer always fits, since $G \le \min_{a_i \ne 0} |a_i|$. With arbitrary precision, let $n_i$ be the bit length of $a_i$, $B = \sum_i n_i$ the input size, and count bit operations.

## Variants

- **Bézout coefficients.** Find $x_1, \ldots, x_k$ with $\sum_i a_i x_i = G$. Fold the [extended Euclidean algorithm](/extended-euclidean-algorithm/): if $g = \sum_{j < i} a_j x_j$ and $g s + a_i t = \gcd(g, a_i)$, multiply the old coefficients by $s$ and set $x_i = t$. The coefficients grow along the fold, so practical code reduces them as it goes.
- **Range queries.** Answer $\gcd(a_l, \ldots, a_r)$ for many ranges. Since $\gcd(x, x) = x$, overlapping ranges are harmless, so a sparse table answers each query with one gcd after $O(k \log k)$ preprocessing; with updates, use a segment tree. See [range GCD query](/range-gcd-query/).
- **Leave one out.** For each $i$, the gcd of all elements except $a_i$: compute the prefix gcds and the suffix gcds, then combine them, in $O(k)$ gcd calls.
- **Gcd of differences.** $\gcd(a_2 - a_1, \ldots, a_k - a_1)$ is the largest $m$ with all $a_i$ congruent modulo $m$. It equals the gcd of all pairwise differences.
- **Subarrays.** Counting the subarrays with gcd 1, or listing all distinct subarray gcds, uses the fact that the gcds of the subarrays ending at a fixed position take at most $1 + \log_2 \max |a_i|$ distinct values, since each change at least halves the value.

## Examples

| array | gcd | note |
| --- | --- | --- |
| 12, 18, 30 | 6 | |
| 6, 10, 15 | 1 | every pair has gcd greater than 1 |
| 0, -8, 12 | 4 | zeros and signs are ignored |
| 0, 0, 0 | 0 | the convention $\gcd(0, \ldots, 0) = 0$ |
| $3 \cdot 2^{40}$, $9 \cdot 2^{35}$, $5 \cdot 2^{50}$ | $2^{35}$ | |
| 84, 126, 210, 315 | 21 | |

A trace of the fold on $(84, 126, 210, 315)$, starting from $g = 0$:

| $i$ | $a_i$ | $g$ before | $g$ after |
| --- | --- | --- | --- |
| 1 | 84 | 0 | 84 |
| 2 | 126 | 84 | 42 |
| 3 | 210 | 42 | 42 |
| 4 | 315 | 42 | 21 |

The array $(6, 10, 15)$ shows that pairwise information is not enough: $\gcd(6, 10) = 2$, $\gcd(10, 15) = 5$ and $\gcd(6, 15) = 3$, but the gcd of all three is 1.

## Known algorithms

**Fold.** Set $g \leftarrow 0$. For $i = 1, \ldots, k$: set $g \leftarrow \gcd(g, |a_i|)$, and stop if $g = 1$. Return $g$.

*Correctness.* By induction on $i$, $g = \gcd(a_1, \ldots, a_i)$ after step $i$. The base case is $\gcd(0, a_1) = |a_1|$. For the step, $d$ divides $a_1, \ldots, a_i$ exactly when $d$ divides $a_1, \ldots, a_{i-1}$ and $a_i$, which (by the divisibility form of the definition) is exactly when $d$ divides $\gcd(a_1, \ldots, a_{i-1})$ and $a_i$, that is, when $d \mid \gcd(g, a_i)$. The early stop is correct because $\gcd(1, x) = 1$ for every $x$.

*Word RAM cost.* Compute each $\gcd(g, a_i)$ with $g > 0$ as one division $r = a_i \bmod g$ followed by the Euclidean algorithm on $(g, r)$. The Euclidean algorithm on a pair performs the same quotients as on the pair divided by its gcd, so on $(g, r)$ with result $g'$ it takes at most $\log_\varphi(g/g') + 2$ steps, by [Lamé's theorem](/lames-theorem/), where $\varphi$ is the golden ratio. Summed over $i$, the terms $\log_\varphi(g/g')$ telescope to at most $\log_\varphi |a_1|$, with $a_1$ the first nonzero element. So the fold takes at most $\log_\varphi |a_1| + 3k$ division steps, which is $O(k + w)$ time. This is a factor of $w$ better than the naive bound of $k$ separate gcds of $O(w)$ steps each.

*Bit cost.* With schoolbook arithmetic, dividing $x$ by $y$ with quotient $q$ costs $O((\log q + 1) \log y)$ bit operations. In the Euclidean algorithm on $(x, y)$ with result $g$, the product of the quotients is at most $x/g$, so the total cost is $O(\log y \cdot (\log(x/g) + 1))$ plus the number of steps times $\log y$, which is $O(\log y \cdot (\log(x/g) + 1))$ again. Start the fold with an element of smallest nonzero absolute value, of $m$ bits. Then $g$ has at most $m$ bits throughout, each reduction $a_i \bmod g$ costs $O(n_i m)$, and the Euclidean parts telescope to $O(m (m + k))$. The total is $O(m B)$ bit operations, which is $O(B^2)$ in the worst case and nearly linear when one element is short.

**Balanced tree.** Combine the elements in pairs, then the results in pairs, and so on. This takes the same number of gcd calls but has depth $\lceil \log_2 k \rceil$, which suits parallel machines and, with a subquadratic gcd such as the [half-GCD](/half-gcd/), keeps the operands balanced.

**Other gcd kernels.** The fold works with any two-integer gcd: the [binary GCD](/binary-gcd/), [Lehmer's GCD](/lehmers-gcd/) or the half-GCD for long integers.

## Bounds

- **Lower bound.** Every element must be read in the worst case: on the input $(2, 2, \ldots, 2)$ the answer is 2, and changing any one unread element to 3 makes it 1. So $\Omega(k)$ word operations, or $\Omega(B)$ bit operations, are needed.
- **Upper bound.** $O(k + \log \max |a_i|)$ word operations on the word RAM by the fold, which matches the lower bound up to the cost of one gcd of two words.
- **Size.** The answer satisfies $0 \le G \le \min_{a_i \ne 0} |a_i|$, so it never overflows a word.

## Reductions

- **To the gcd of two integers.** The fold uses $k - 1$ two-integer gcds, and the gcd of two integers is the case $k = 2$.
- **Dual of the lcm.** In terms of prime exponents, $v_p(G) = \min_i v_p(a_i)$, while the [LCM of integers](/lcm-of-integers/) takes the maximum. The lcm fold has the same shape, but its intermediate values grow instead of shrink.
- **Primitive vectors.** Dividing an integer vector by the gcd of its entries gives the unique primitive vector, with entries of gcd 1, on the same ray from the origin.

## Applications

- **Linear Diophantine equations.** $a_1 x_1 + \cdots + a_k x_k = c$ has an integer solution if and only if $\gcd(a_1, \ldots, a_k) \mid c$, by [Bézout's identity](/bezouts-identity/) for several numbers; see [linear Diophantine equation](/linear-diophantine-equation/).
- **Content of a polynomial.** The content of an integer polynomial is the gcd of its coefficients. Removing it gives the primitive part, a step of [polynomial GCD](/polynomial-gcd/) algorithms over the integers.
- **Normalizing directions and ratios.** Lattice directions, reaction coefficients and resource ratios are divided by the gcd of their entries to get a canonical form.
- **Coin problems.** Coins of values $a_1, \ldots, a_k$ can pay every large enough amount if and only if $\gcd(a_1, \ldots, a_k) = 1$.

## References
