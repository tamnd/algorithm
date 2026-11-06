---
tag: 6FBZTF
kind: algorithm
slug: dirichlet-hyperbola-method
name: Dirichlet hyperbola method
aliases:
- Dirichlet's hyperbola method
- divisor-pair symmetry method
area: number-theory/divisibility-and-gcd
level: advanced
summary: Evaluates the divisor summatory function in O(sqrt n) by counting lattice points under a hyperbola.
solves: [divisor-summatory-function]
model: word-ram
complexity:
  vars: {n: the input value, the bound on the product ab}
  time: {worst: Θ(n^(1/2)), best: Θ(n^(1/2))}
  space: {extra: Θ(1)}
  bit_operations: {worst: O(n^(1/2) log(n)^2)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1849
  people: [Peter Gustav Lejeune Dirichlet]
  note: Dirichlet's proof that the average number of divisors is ln n + 2 gamma - 1 with error O(n^(-1/2)).
prereqs: [divisor-summatory-function, dirichlet-convolution, floor-division, loop-invariant]
see_also: [dirichlets-divisor-problem, lattice-point-counting, divisor-count-sieve, lucy-hedgehog-prime-counting, meissel-lehmer-algorithm, counting-coprime-pairs, mobius-inversion-formula, multiplicative-function]
sources:
  - book: isbn:9780387901633
    title: Tom M. Apostol, Introduction to Analytic Number Theory
    locator: Chapter 3, Section 3.5, The average order of d(n) (Theorem 3.3 and the lattice points under the hyperbola qd = x)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 18, Section 18.2, The average order of d(n) (Theorem 320, proved by the symmetry of the hyperbola)
  - paper: "Richard Sladkey, A successive approximation algorithm for computing the divisor summatory function, arXiv:1206.3369, 2012"
    locator: abstract and introduction (the O(n^(1/2)) hyperbola method as the baseline, and the O(n^(1/3)) improvement)
  - url: "https://en.wikipedia.org/wiki/Divisor_summatory_function"
    locator: Wikipedia, Divisor summatory function (the hyperbola formula and Dirichlet's asymptotic)
---

The Dirichlet hyperbola method computes the [divisor summatory function](/divisor-summatory-function/) $D(n) = \sum_{k \le n} d(k)$ exactly with $\lfloor \sqrt n \rfloor$ divisions. $D(n)$ is the number of pairs $(a, b)$ of positive integers with $ab \le n$, the lattice points under the hyperbola $xy = n$. Every such pair has $a \le \sqrt n$ or $b \le \sqrt n$, and the region is symmetric, so with $s = \lfloor \sqrt n \rfloor$

$$D(n) = 2 \sum_{a=1}^{s} \left\lfloor \frac{n}{a} \right\rfloor - s^2.$$

The same split works for any sum $\sum_{ab \le n} f(a) g(b)$, the prefix sum of a [Dirichlet convolution](/dirichlet-convolution/), when prefix sums of $f$ and $g$ are cheap. Dirichlet used it in 1849 to prove $D(n) = n \ln n + (2\gamma - 1)n + O(\sqrt n)$; in computation it is the standard $O(\sqrt n)$ method and the starting point of faster ones.

## In plain words

Picture a grid of points, one for each pair of whole numbers whose product is at most the limit. The points fill a region under a curved line, and the answer is how many points there are. Counting column by column needs one division per column, but there are as many columns as the limit itself.

The region is the same when you swap the two numbers. Every point lies in one of the first few columns or one of the first few rows, where "few" means up to the square root of the limit, because two numbers both larger than the square root multiply to more than the limit. So count the first few columns, double that to cover the first few rows, and subtract the small square in the corner, which was counted twice.

## The problem

The input is an integer $n$. The output is $D(n) = \sum_{k=1}^{n} d(k)$, where $d(k)$ is the number of positive divisors of $k$; for $n \le 0$ the sum is empty and the output is $0$. Negative $n$ is not an error; it gives $0$.

**Cost model.** On the [word RAM](/word-ram/), $n$ fits in a word, and each [floor division](/floor-division/), addition and multiplication costs one step. The answer is below $n(\ln n + 1)$, so it needs about $\lg n + \lg \ln n$ binary digits, a little more than one word; see the pitfalls. The square root $s = \lfloor \sqrt n \rfloor$ is computed by Newton's method on integers in $O(\log n)$ steps, which is negligible. For [arbitrary-precision](/arbitrary-precision-arithmetic/) $n$ of $\beta$ binary digits, each division of $n$ by $a \le \sqrt n$ costs $O(\beta^2)$ bit operations with schoolbook arithmetic. In both models the $\Theta(\sqrt n)$ loop limits $n$ to about $10^{18}$ in practice.

**General form.** Given arithmetic functions $f, g$ with prefix sums $F(x) = \sum_{a \le x} f(a)$ and $G(x) = \sum_{b \le x} g(b)$, compute $\sum_{ab \le n} f(a) g(b) = \sum_{k \le n} (f * g)(k)$. The divisor case is $f = g = 1$, $F(x) = G(x) = \lfloor x \rfloor$.

## The algorithm

```pseudo id=main
HYPERBOLA-D(n)
L1  if n ≤ 0 then return 0              ▷ empty sum
L2  s ← ⌊√n⌋                            ▷ integer square root, s² ≤ n < (s + 1)²
L3  t ← 0
L4  for a ← 1 to s
L5      t ← t + ⌊n / a⌋                 ▷ points (a, b) with b ≤ n / a
L6  return 2t − s²                      ▷ columns plus rows minus the corner square
```

Line L5 adds the number of points in column $a$, the $b$ with $1 \le b \le n/a$. After the loop, $t$ counts the points with $a \le s$. By symmetry, $t$ also counts the points with $b \le s$. The corner square $a, b \le s$ has $s^2$ points, all under the hyperbola since $ab \le s^2 \le n$, and it was counted in both, so line L6 subtracts it once.

For the general sum, the same three parts give

$$\sum_{ab \le n} f(a) g(b) = \sum_{a \le s} f(a) \, G\!\left(\left\lfloor \frac{n}{a} \right\rfloor\right) + \sum_{b \le s} g(b) \, F\!\left(\left\lfloor \frac{n}{b} \right\rfloor\right) - F(s) \, G(s),$$

with $2s$ evaluations each of $f$, $g$, $F$ and $G$. When $f \ne g$ the two sums must both be computed; only the divisor case can double one of them.

## Example

Compute $D(100)$. Here $s = 10$ and the column counts $\lfloor 100/a \rfloor$ for $a = 1, \ldots, 10$ are

| $a$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| $\lfloor 100/a \rfloor$ | 100 | 50 | 33 | 25 | 20 | 16 | 14 | 12 | 11 | 10 |

Their sum is $t = 291$, and line L6 returns $2 \cdot 291 - 100 = 482$. Adding $d(1) + \cdots + d(100)$ directly gives the same $482$, and the column count $\sum_{a \le 100} \lfloor 100/a \rfloor$ needs $100$ divisions instead of $10$. For $n = 10^{12}$ the loop runs $10^6$ times and returns $D(10^{12}) = 27785452449086$.

**General form.** The sum of divisors, $\sum_{k \le 10} \sigma(k)$, is the case $f(a) = a$, $g = 1$, $F(x) = x(x + 1)/2$, $G(x) = x$, with $s = 3$:

$$\underbrace{1 \cdot 10 + 2 \cdot 5 + 3 \cdot 3}_{29} + \underbrace{F(10) + F(5) + F(3)}_{55 + 15 + 6 = 76} - F(3) G(3) = 29 + 76 - 18 = 87,$$

which equals $1 + 3 + 4 + 7 + 6 + 12 + 8 + 15 + 13 + 18$.

## Correctness

Let $P = \{ (a, b) \in \mathbb{Z}_{\ge 1}^2 : ab \le n \}$. Grouping $P$ by the product $k = ab$ gives $|P| = \sum_{k \le n} d(k) = D(n)$, since each divisor $a$ of $k$ gives one pair $(a, k/a)$. Let $A = \{ (a, b) \in P : a \le s \}$ and $B = \{ (a, b) \in P : b \le s \}$.

- $P = A \cup B$: if $a > s$ and $b > s$, then $ab \ge (s + 1)^2 > n$.
- $|A| = \sum_{a \le s} \lfloor n/a \rfloor$, the [loop invariant](/loop-invariant/) of lines L4 and L5 being $t = \sum_{a' < a} \lfloor n/a' \rfloor$.
- $|B| = |A|$, because $(a, b) \mapsto (b, a)$ maps $A$ onto $B$.
- $A \cap B = \{1, \ldots, s\}^2$, because $ab \le s^2 \le n$ for all such pairs.

By inclusion and exclusion, $D(n) = |A| + |B| - |A \cap B| = 2t - s^2$. The general form follows in the same way, with each point $(a, b)$ weighted by $f(a) g(b)$: the weight of $A$ is $\sum_{a \le s} f(a) G(\lfloor n/a \rfloor)$, that of $B$ is the mirror sum, and that of the square is $F(s) G(s)$. The full proof is in the proofs.

## Complexity

The loop runs exactly $s = \lfloor \sqrt n \rfloor$ times with one division and one addition each, so the time is $\Theta(\sqrt n)$ word operations in the worst and the best case, and the extra space is $\Theta(1)$ words. Computing $s$ by Newton's method adds $O(\log n)$ steps. With $n$ of $\beta = \Theta(\log n)$ binary digits in arbitrary precision, each division costs $O(\beta^2)$, so the total is $O(\sqrt n \log^2 n)$ bit operations.

| method for $D(n)$ | divisions | extra space |
|---|---|---|
| sieve $d(k)$ for $k \le n$, then add | about $n \ln n$ additions | $\Theta(n)$ |
| column count $\sum_{a \le n} \lfloor n/a \rfloor$ | $n$ | $\Theta(1)$ |
| hyperbola method | $\lfloor \sqrt n \rfloor$ | $\Theta(1)$ |
| convex-hull walk (Sladkey) | $O(n^{1/3})$ steps | $O(\log n)$ |

The general form makes $2s$ calls of each function, so it costs $\Theta(\sqrt n)$ calls; its total time depends on the cost of $F$ and $G$ at the points $\lfloor n/a \rfloor$.

## Properties

- **Exact.** Integer arithmetic only; no rounding, unlike the asymptotic formula it was invented to prove.
- **Deterministic, iterative, constant space.** One loop and three integers.
- **Symmetric split.** The cut at $\sqrt n$ balances the two halves; the general form allows any cut $a \le u$, $b \le n/u$, which matters when $F$ and $G$ have different costs.
- **Also an analytic tool.** Replacing $\lfloor n/a \rfloor$ by $n/a - \{n/a\}$ in the formula gives Dirichlet's theorem $D(n) = n \ln n + (2\gamma - 1)n + O(\sqrt n)$ in a few lines.

## Variants and improvements

- **Unbalanced cut.** With $u v = n$, $\sum_{ab \le n} f(a) g(b) = \sum_{a \le u} f(a) G(n/a) + \sum_{b \le v} g(b) F(n/b) - F(u) G(v)$. Choosing $u$ to balance a cheap $F$ against a costly $G$ is the core of many sublinear prefix-sum algorithms for [multiplicative functions](/multiplicative-function/).
- **Block decomposition.** The quotient $\lfloor n/a \rfloor$ takes fewer than $2\sqrt n$ values. Summing over blocks of equal quotient gives another $O(\sqrt n)$ method for $\sum_{a \le n} h(a) \lfloor n/a \rfloor$ when $h$ has fast prefix sums; it is used in [Lucy Hedgehog prime counting](/lucy-hedgehog-prime-counting/) and the [Meissel-Lehmer algorithm](/meissel-lehmer-algorithm/).
- **Piltz divisor functions.** $D_3(n) = \#\{ abc \le n \}$ splits by the smallest of $a, b, c$, which is at most $n^{1/3}$, and costs $O(n^{2/3})$ divisions.
- **Convex-hull walk.** Sladkey (2012) counts the points between $x = n^{1/3}$ and $x = \sqrt n$ by following the hyperbola with lattice segments, reaching $O(n^{1/3})$ time and $O(\log n)$ space.
- **Coprime pairs and squarefree weights.** $\sum_{k \le n} 2^{\omega(k)} = \sum_{m \le \sqrt n} \mu(m) D(\lfloor n/m^2 \rfloor)$, a [Möbius inversion](/mobius-inversion-formula/) that calls the hyperbola method $O(\sqrt n)$ times; see [counting coprime pairs](/counting-coprime-pairs/).

## When to use it

Use it to compute one value $D(n)$, or a sum $\sum_{k \le n} (f * g)(k)$ with fast prefix sums of $f$ and $g$, for $n$ up to about $10^{16}$ to $10^{18}$, where an $O(n)$ sieve is too slow or needs too much memory. When all of $D(1), \ldots, D(n)$ are needed, a [divisor count sieve](/divisor-count-sieve/) with prefix sums is better. For single values with $n$ much beyond $10^{18}$, the $O(n^{1/3})$ convex-hull method is faster.

## Pitfalls

- **Floating-point square root.** Computing $s$ as `int(sqrt(n))` in double precision is wrong for large $n$: for $n = 10^{16} + 2 \cdot 10^8 = (10^8 + 1)^2 - 1$ it gives $10^8 + 1$ instead of $10^8$, and the answer is off by $2\lfloor n/(s + 1) \rfloor - 2s - 1$, here $-1$. Use an integer square root, or correct the float result so that $s^2 \le n < (s + 1)^2$.
- **Overflow of the result.** $D(n) \approx n \ln n$ passes $2^{64}$ for $n$ near $4.5 \cdot 10^{17}$, and $2t$ overflows before the subtraction; $D(10^{18}) \approx 4.2 \cdot 10^{19}$. Use 128-bit or arbitrary-precision accumulators.
- **Overflow of $s^2$.** With signed 64-bit integers and $n$ near $2^{63}$, $s^2$ fits but $(s + 1)^2$ in a correction step may not.
- **Forgetting the square.** Returning $2t$ counts the $s^2$ corner points twice; for $n = 10$ it gives $36$ instead of $27$.
- **Doubling in the general form.** $2 \sum_{a \le s} f(a) G(n/a)$ is correct only when $f = g$; otherwise compute both sums.

## Implementations

## History

Dirichlet introduced the method in 1849, in his memoir on mean values in number theory, to show that the average of $d(k)$ for $k \le n$ is $\ln n + 2\gamma - 1$ with error $O(n^{-1/2})$, improving the error $O(1)$ that the plain column count gives. The question of the true error term became the [Dirichlet divisor problem](/dirichlets-divisor-problem/), and the split at $\sqrt n$ became a standard tool for sums of [Dirichlet convolutions](/dirichlet-convolution/), described in Apostol and in Hardy and Wright. As an algorithm, it is the baseline that Sladkey's 2012 $O(n^{1/3})$ method improves.

## References
