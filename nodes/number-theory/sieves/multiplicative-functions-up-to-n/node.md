---
tag: BJ1R7T
kind: problem
slug: multiplicative-functions-up-to-n
name: Multiplicative function values up to n
aliases:
- multiplicative function sieve problem
- sieving a multiplicative function
area: number-theory/sieves
level: core
summary: Given n and a multiplicative function f, known on prime powers, compute f(m) for every m up to n. The linear sieve does it in Θ(n) steps, which matches the size of the output.
model: word-ram
complexity:
  vars: {n: the bound}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
prereqs: [multiplicative-function]
see_also: [linear-sieve, mobius-sieve, euler-phi-sieve, divisor-count-sieve, totient-values-up-to-n, divisor-function-up-to-n, smallest-prime-factor-table, dirichlet-convolution]
sources:
  - book: isbn:9780387901633
    title: Tom M. Apostol, Introduction to Analytic Number Theory, Springer, 1976
    locator: Chapter 2 (multiplicative functions, their values on prime powers, and Dirichlet multiplication)
  - url: https://cp-algorithms.com/algebra/prime-sieve-linear.html
    title: Linear Sieve, cp-algorithms
    locator: Sections Algorithm and Correctness proof (the unique form m = lp(m) times i used to extend f)
  - paper: doi:10.1145/359657.359660
    title: David Gries and Jayadev Misra, A linear sieve algorithm for finding prime numbers, Communications of the ACM 21(12), 1978
    locator: pages 999 to 1003 (the linear sieve)
---

The problem of multiplicative function values up to $n$ asks, for a [multiplicative function](/multiplicative-function/) $f$ given by its values on prime powers, for the whole table $f(1), f(2), \ldots, f(n)$. A function is multiplicative when $f(1) = 1$ and $f(ab) = f(a) f(b)$ for all [coprime](/coprime-integers/) $a$ and $b$, so it is fixed by its values $f(p^a)$. Euler's $\varphi$, the [Möbius function](/mobius-function/) $\mu$ and the [divisor functions](/divisor-function/) $d$ and $\sigma$ are the main examples. The [linear sieve](/linear-sieve/) solves the problem in $\Theta(n)$ steps, which is optimal, and simpler sieves take $O(n \log \log n)$ or $O(n \log n)$.

## In plain words

Some functions on whole numbers are built from their values on prime powers: to get the value at a number, split it into powers of distinct primes, look up the value at each power, and multiply. The count of divisors works this way, and so does the count of numbers below that share no factor.

The task is to fill in a table of such a function for all numbers up to a bound. Splitting each number into primes from scratch is slow. A sieve builds the numbers in order, each as a smaller number times one more prime, and gets each value from a value it already has.

## Definition

**Input.** An integer $n \ge 0$, and a rule that returns $f(p^a)$ for a prime $p$ and $a \ge 1$ in $O(1)$ steps.

**Output.** The array $f[1 \ldots n]$, where for $m = p_1^{a_1} \cdots p_r^{a_r}$ with distinct primes,

$$f(m) = \prod_{i=1}^{r} f(p_i^{a_i}), \qquad f(1) = 1.$$

**Cost model.** The [word RAM](/word-ram/): arithmetic, comparisons and array access on numbers up to $n$, and on the values of $f$, cost one step each. Memory is counted in words.

## Variants

- **Completely multiplicative functions.** If $f(ab) = f(a) f(b)$ for all $a$ and $b$, such as $f(m) = m^k$ or the Liouville function $\lambda(m) = (-1)^{\Omega(m)}$, then $f(p i) = f(p) f(i)$ in every case, and no prime powers need tracking.
- **Additive functions.** Functions with $g(ab) = g(a) + g(b)$ for coprime $a, b$, such as $\omega(m)$, the number of distinct prime factors, work the same way with sums in place of products.
- **Summatory form.** Return only $F(n) = \sum_{m \le n} f(m)$. For many functions this takes $o(n)$ time: the [Dirichlet hyperbola method](/dirichlet-hyperbola-method/) gives $\sum d(m)$ in $O(\sqrt n)$, and methods in the style of [Lucy's prime counting](/lucy-hedgehog-prime-counting/) give sums over primes in about $n^{3/4}$ steps.
- **An interval.** Compute $f(m)$ for $m$ in $[L, R]$ with the [segmented sieve](/segmented-sieve/): divide out each prime $p \le \sqrt R$ from the numbers in the block, and treat a cofactor larger than 1 at the end as one more prime.

## Examples

| $m$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $\varphi(m)$ | 1 | 1 | 2 | 2 | 4 | 2 | 6 | 4 | 6 | 4 | 10 | 4 |
| $\mu(m)$ | 1 | $-1$ | $-1$ | 0 | $-1$ | 1 | $-1$ | 0 | 0 | 1 | $-1$ | 0 |
| $d(m)$ | 1 | 2 | 2 | 3 | 2 | 4 | 2 | 4 | 3 | 4 | 2 | 6 |
| $\sigma(m)$ | 1 | 3 | 4 | 7 | 6 | 12 | 8 | 15 | 13 | 18 | 12 | 28 |
| $\lambda(m)$ | 1 | $-1$ | $-1$ | 1 | $-1$ | 1 | $-1$ | $-1$ | 1 | 1 | $-1$ | $-1$ |

The prime power rules are $\varphi(p^a) = p^a - p^{a-1}$, $\mu(p) = -1$ and $\mu(p^a) = 0$ for $a \ge 2$, $d(p^a) = a + 1$, $\sigma(p^a) = (p^{a+1} - 1)/(p - 1)$, and $\lambda(p^a) = (-1)^a$. For $m = 12 = 4 \cdot 3$: $\sigma(12) = \sigma(4) \sigma(3) = 7 \cdot 4 = 28$.

**Non-examples.** The function $f(m) = m + 1$ is not multiplicative, since $f(1) = 2$. The number of prime factors $\Omega(m)$ is additive, not multiplicative. The function $\Lambda$ of von Mangoldt is neither.

## Known algorithms

| algorithm | time (word operations) | memory |
|---|---|---|
| factor each $m$ by [trial division](/trial-division/) | $O(n^{3/2})$ | the output |
| factor each $m$ with a [smallest prime factor table](/smallest-prime-factor-table/) | $O(n \log \log n)$ after the table | the output and the table |
| sieve over prime powers: for each $p^a \le n$, update its multiples | $O(n \log \log n)$ | the output and one array of cofactors |
| [linear sieve](/linear-sieve/) with the power of the least prime factor | $\Theta(n)$ | the output, two arrays of $n + 1$ words, the primes |
| Dirichlet convolution of two known tables, such as $\sigma = \mathrm{id} * 1$ | $\Theta(n \log n)$ | the output |

**The linear scheme.** Keep $\mathrm{lp}[m]$, the least prime factor, and $q[m]$, the largest power of $\mathrm{lp}(m)$ that divides $m$. When the linear sieve writes $m = p \cdot i$ with $p = \mathrm{lp}(m)$:

- if $p < \mathrm{lp}(i)$, then $\gcd(p, i) = 1$, so $q[m] = p$ and $f(m) = f(p) f(i)$;
- if $p = \mathrm{lp}(i)$, then $q[m] = p \cdot q[i]$, and either $m = q[m]$ is a prime power, whose value comes from the rule, or $f(m) = f(q[m]) \cdot f(m / q[m])$, two values that are already known.

The [Möbius sieve](/mobius-sieve/) and the linear version of the [Euler totient sieve](/euler-phi-sieve/) are special cases in which the second case simplifies.

## Bounds

The output has $n$ values, so $\Omega(n)$ steps are needed, and the linear scheme takes $O(n)$ steps when $f(p^a)$ costs $O(1)$. So the problem takes $\Theta(n)$ time in this model. The bound is proved and depends on no conjecture. If evaluating $f(p^a)$ is expensive, note that only $\pi(n) + O(\sqrt n)$ prime powers up to $n$ exist, so the rule is called $O(n / \log n)$ times.

## Reductions

- **From a factor table.** Given the [smallest prime factor table](/smallest-prime-factor-table/), the table of $f$ follows in one pass, in increasing $m$, from $f(m) = f(q) f(m/q)$ with $q$ the full power of $\mathrm{lp}(m)$ in $m$; if the cofactor $c(m) = m/q$ is stored too, each step costs $O(1)$, because $c(m) = c(m/p)$ when $p = \mathrm{lp}(m)$ divides $m/p$, and $c(m) = m/p$ otherwise.
- **To Dirichlet convolution.** The Dirichlet convolution of two multiplicative functions is multiplicative. So $f * g$ up to $n$ can be computed by sieving its prime power values, in $\Theta(n)$, instead of the $\Theta(n \log n)$ direct sum; see [Dirichlet convolution](/dirichlet-convolution/).
- **Special cases.** [Totient values up to n](/totient-values-up-to-n/) and [divisor function values up to n](/divisor-function-up-to-n/) are the cases $f = \varphi$ and $f = \sigma_k$.

## Applications

- Tables of $\mu$ for [Möbius inversion](/mobius-inversion-formula/) and counting with inclusion and exclusion.
- Tables of $\varphi$ for counting fractions and [coprime pairs](/counting-coprime-pairs/).
- The small values needed by sublinear methods for summatory functions, which combine a sieve up to about $n^{2/3}$ with a recursion for the large arguments.

## References
