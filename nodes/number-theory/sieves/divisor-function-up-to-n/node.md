---
tag: DA9EQ7
kind: problem
slug: divisor-function-up-to-n
name: Divisor function values up to n
aliases:
- divisor counts up to n
- sigma values up to n
- divisor sums up to n
area: number-theory/sieves
level: intro
summary: Given n, compute the number of divisors d(m), or the sum of divisors sigma(m), for every m from 1 to n. The harmonic sieve takes Θ(n log n) steps and the linear sieve Θ(n).
model: word-ram
complexity:
  vars: {n: the bound}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
prereqs: [divisor-function]
see_also: [divisor-count-sieve, linear-sieve, multiplicative-functions-up-to-n, divisor-summatory-function, dirichlets-divisor-problem, totient-values-up-to-n, enumerating-divisors, smallest-prime-factor-table]
sources:
  - book: isbn:9780387901633
    title: Tom M. Apostol, Introduction to Analytic Number Theory, Springer, 1976
    locator: Chapter 2 (the divisor functions sigma_k as multiplicative functions) and Chapter 3 (the average order of d(n) and sigma(n))
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition, Oxford University Press, 2008
    locator: Section 16.7 (the functions d(n) and sigma_k(n)), Section 18.1 (the order of d(n)) and Section 18.2 (the average order of d(n))
  - url: https://cp-algorithms.com/algebra/divisors.html
    title: Number of divisors / sum of divisors, cp-algorithms
    locator: Sections Number of divisors and Sum of divisors (the multiplicative formulas)
---

The problem of divisor function values up to $n$ asks for the table of $d(m)$, the number of divisors of $m$, or of $\sigma(m)$, the sum of the divisors of $m$, for every $1 \le m \le n$. More generally it asks for $\sigma_k(m) = \sum_{e \mid m} e^k$, the [divisor function](/divisor-function/) of order $k$, so that $d = \sigma_0$ and $\sigma = \sigma_1$. The [divisor count sieve](/divisor-count-sieve/) solves it in $\Theta(n \log n)$ word operations by adding each $e$ to its multiples, and the [linear sieve](/linear-sieve/) solves it in $\Theta(n)$, which matches the size of the output.

## In plain words

For each number up to the bound, count its divisors, or add them up. Twelve has the six divisors one, two, three, four, six and twelve, whose sum is twenty-eight.

Checking every smaller number for each number is far too slow. It is better to turn the work around: for each possible divisor, walk through its multiples and record it there. Each number then collects all its divisors.

## Definition

**Input.** An integer $n \ge 0$, and the order $k \ge 0$ (most often $k = 0$ or $k = 1$).

**Output.** The array $\sigma_k[1 \ldots n]$ with $\sigma_k(m) = \sum_{e \mid m} e^k$, the sum over the positive divisors $e$ of $m$. For $k = 0$ this is $d(m)$, also written $\tau(m)$. For $n = 0$ the output is empty.

**Multiplicativity.** If $m = p_1^{a_1} \cdots p_r^{a_r}$, then

$$d(m) = \prod_{i=1}^{r} (a_i + 1), \qquad \sigma(m) = \prod_{i=1}^{r} \frac{p_i^{a_i + 1} - 1}{p_i - 1}.$$

So $\sigma_k$ is a [multiplicative function](/multiplicative-function/), and the general methods for [multiplicative functions up to n](/multiplicative-functions-up-to-n/) apply.

**Cost model.** The [word RAM](/word-ram/): arithmetic, comparisons and array access on numbers of $O(\log n)$ binary digits cost one step. Since $\sigma(m) \le m^2$, every value of $\sigma$ fits in two words; for $\sigma_k$ with $k \ge 2$ the values grow like $m^k$, and the model must allow that size.

## Variants

- **Divisor counts only**, $k = 0$. The values are small: $d(m) \le 2 \sqrt m$, and in fact $d(m) = m^{O(1 / \log \log m)}$.
- **Divisor sums**, $k = 1$. The table of $\sigma$ finds perfect numbers ($\sigma(m) = 2m$) and amicable pairs ($\sigma(a) = \sigma(b) = a + b$).
- **Summatory form.** Return only $D(n) = \sum_{m \le n} d(m)$. The [Dirichlet hyperbola method](/dirichlet-hyperbola-method/) gives it in $O(\sqrt n)$ time; see the [divisor summatory function](/divisor-summatory-function/).
- **Divisor lists.** Return the list of divisors of each $m$. The output then has $D(n) \approx n \ln n$ numbers, so $\Theta(n \log n)$ is optimal for this variant.

## Examples

| $m$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $d(m)$ | 1 | 2 | 2 | 3 | 2 | 4 | 2 | 4 | 3 | 4 | 2 | 6 |
| $\sigma(m)$ | 1 | 3 | 4 | 7 | 6 | 12 | 8 | 15 | 13 | 18 | 12 | 28 |

For $m = 12 = 2^2 \cdot 3$, the formulas give $d(12) = 3 \cdot 2 = 6$ and $\sigma(12) = 7 \cdot 4 = 28$. The number 6 is perfect, since $\sigma(6) = 12$.

**Sizes.** Dirichlet proved $\sum_{m \le n} d(m) = n \ln n + (2 \gamma - 1) n + O(\sqrt n)$, where $\gamma \approx 0.5772$ is Euler's constant. For $n = 10^6$ the sum is 13970034, and the first two terms give 13969941.9. The sum of $\sigma(m)$ is $\frac{\pi^2}{12} n^2 + O(n \log n)$; for $n = 1000$ it is 823081, against 822467.0. The largest value of $d(m)$ for $m \le 1000$ is $d(840) = 32$.

**Non-example.** Counting the divisors $e < m$ only gives the aliquot sum $s(m) = \sigma(m) - m$ when summed, and $d(m) - 1$ when counted. Both are related functions, not $d$ or $\sigma$.

## Known algorithms

| algorithm | time (word operations) | memory |
|---|---|---|
| test each $e \le \sqrt m$ for each $m$ | $\Theta(n^{3/2})$ | the output |
| [divisor count sieve](/divisor-count-sieve/): add $e$ to each multiple of $e$ | $\Theta(n \log n)$ | the output |
| [linear sieve](/linear-sieve/), keeping the exponent of the least prime factor | $\Theta(n)$ | the output, the primes, and one extra array |
| factor each $m$ with a [smallest prime factor table](/smallest-prime-factor-table/) | $O(n \log \log n)$ | the output and the table |

The linear sieve uses the rule $d(p^{a+1} r) = d(p^a r) \cdot (a + 2) / (a + 1)$ for $p$ the least prime factor and $p \nmid r$, or, to avoid division, keeps $d(r)$ and $a$ for each $m$. Factoring with the table costs $\Omega(m) + 1$ lookups for $m$, and $\sum_{m \le n} \Omega(m) = n \ln \ln n + O(n)$. The page on [multiplicative functions up to n](/multiplicative-functions-up-to-n/) gives the scheme.

## Bounds

The output has $n$ numbers, so every algorithm takes $\Omega(n)$ steps, and the linear sieve takes $O(n)$. So the problem takes $\Theta(n)$ time, for each fixed $k$, on the word RAM. This is proved and does not depend on any conjecture. The harmonic sieve is slower by a factor of $\ln n$, which is often acceptable because its inner loop is so simple.

## Reductions

- **From a factor table.** With the [smallest prime factor table](/smallest-prime-factor-table/), each $\sigma_k(m)$ follows from the value at $m / p^a$, where $p^a$ is the full power of the least prime factor, in $O(1)$ steps once the exponent and $p^a$ are tracked.
- **To the summatory function.** Summing the table gives $D(n)$ or $\sum \sigma(m)$ in $O(n)$ more steps, although the [Dirichlet hyperbola method](/dirichlet-hyperbola-method/) does better for the sum alone.
- **As a Dirichlet convolution.** $d = 1 * 1$ and $\sigma = \mathrm{id} * 1$ in the sense of [Dirichlet convolution](/dirichlet-convolution/). The harmonic sieve is the direct computation of a convolution $f * g$ up to $n$, in $\Theta(n \log n)$ steps.

## Applications

- Searching for perfect, abundant and amicable numbers, and for numbers with many divisors.
- Counting problems in which the number of solutions of $ab = m$ is $d(m)$, such as counting rectangles of a given area.
- Tables for checking conjectures and for [Dirichlet's divisor problem](/dirichlets-divisor-problem/).

## References
