---
tag: BDHX6K
kind: problem
slug: totient-values-up-to-n
name: Totient values up to n
aliases:
- phi values for a range
- totient table
area: number-theory/sieves
level: intro
summary: Given n, compute Euler's totient phi(m) for every m from 1 to n. Sieves do it in O(n log log n) or Θ(n) word operations, and the output alone has n numbers.
model: word-ram
complexity:
  vars: {n: the bound}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
prereqs: [euler-totient]
see_also: [euler-phi-sieve, linear-sieve, multiplicative-functions-up-to-n, smallest-prime-factor-table, counting-coprime-pairs, farey-sequence, euler-theorem, divisor-function-up-to-n]
sources:
  - book: isbn:9780387901633
    title: Tom M. Apostol, Introduction to Analytic Number Theory, Springer, 1976
    locator: Chapter 2 (the totient and its product formula) and Chapter 3 (the average order of phi(n))
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition, Oxford University Press, 2008
    locator: Section 5.5 (the function phi(m)) and Section 18.5 (the average order of phi(n))
  - url: https://cp-algorithms.com/algebra/phi-function.html
    title: Euler's totient function, cp-algorithms
    locator: Section Euler totient function from 1 to n in O(n log log n)
---

The problem of totient values up to $n$ asks for the table $\varphi(1), \varphi(2), \ldots, \varphi(n)$ of [Euler's totient](/euler-totient/), where $\varphi(m)$ counts the integers $1 \le j \le m$ that are [coprime](/coprime-integers/) to $m$. The [Euler totient sieve](/euler-phi-sieve/) solves it in $\Theta(n \log \log n)$ word operations and the [linear sieve](/linear-sieve/) in $\Theta(n)$, which is optimal because the output has $n$ numbers. The table is the base of many counting programs, such as counting the fractions with small denominators or the coprime pairs in a square.

## In plain words

For each number up to the bound, count how many numbers from one up to it share no common factor with it. For a prime, every smaller number counts, so the answer is one less than the prime. For twelve, only one, five, seven and eleven count, so the answer is four.

Counting each answer from scratch is slow. A sieve gets all answers at once: start each entry at its own number, and for each prime, remove the right share from every multiple of that prime.

## Definition

**Input.** An integer $n \ge 0$.

**Output.** The array $\varphi[1 \ldots n]$ with

$$\varphi(m) = \#\{ 1 \le j \le m : \gcd(j, m) = 1 \} = m \prod_{p \mid m} \left( 1 - \frac{1}{p} \right),$$

where the product runs over the primes $p$ that divide $m$. So $\varphi(1) = 1$. For $n = 0$ the output is empty.

**Cost model.** The [word RAM](/word-ram/): arithmetic, comparisons and array access on numbers up to $n$ cost one step each. The output is $n$ words.

## Variants

- **Summatory totient.** Return only $\Phi(n) = \sum_{m \le n} \varphi(m)$. The identity $\sum_{d \le n} \Phi(\lfloor n/d \rfloor) = n(n+1)/2$, with the [Dirichlet hyperbola method](/dirichlet-hyperbola-method/) and a table of small values, gives it in $O(n^{2/3})$ time.
- **An interval.** Compute $\varphi(m)$ for $m$ in $[L, R]$, with the [segmented sieve](/segmented-sieve/) and the primes up to $\sqrt R$.
- **Other multiplicative functions.** The same methods give $\mu$, $\sigma$, $d$ and every other [multiplicative function](/multiplicative-function/); see [multiplicative functions up to n](/multiplicative-functions-up-to-n/).

## Examples

| $m$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $\varphi(m)$ | 1 | 1 | 2 | 2 | 4 | 2 | 6 | 4 | 6 | 4 | 10 | 4 | 12 | 6 | 8 | 8 | 16 | 6 | 18 | 8 |

For $m = 12 = 2^2 \cdot 3$, the formula gives $12 \cdot \frac12 \cdot \frac23 = 4$, and the coprime $j$ are 1, 5, 7 and 11.

**The size of the sums.** Mertens proved $\sum_{m \le n} \varphi(m) = \frac{3}{\pi^2} n^2 + O(n \log n)$. For $n = 1000$ the sum is 304192, and $3 \cdot 10^6 / \pi^2 \approx 303963.6$.

**Non-example.** The value $\varphi(1) = 0$, which some programs return by counting $1 \le j < m$, is wrong: the definition counts $j = 1$ for $m = 1$.

## Known algorithms

| algorithm | time (word operations) | memory |
|---|---|---|
| count $\gcd(j, m) = 1$ for each pair | $O(n^2 \log n)$ | $O(1)$ besides the output |
| factor each $m$ by [trial division](/trial-division/), then use the product | $O(n^{3/2})$ | $O(1)$ besides the output |
| [Euler totient sieve](/euler-phi-sieve/) | $\Theta(n \log \log n)$ | the output only |
| [linear sieve](/linear-sieve/) | $\Theta(n)$ | the output, a factor table and the primes |

The totient sieve starts with $\varphi[m] = m$, and for each prime $p$ subtracts $\varphi[m]/p$ from each multiple $m$ of $p$. The linear sieve sets each composite $m = p \cdot i$ once, with $p$ the smallest prime factor of $m$, by the rule $\varphi(p i) = p \varphi(i)$ if $p \mid i$ and $\varphi(p i) = (p - 1) \varphi(i)$ otherwise.

## Bounds

Every algorithm writes $n$ values, so it needs $\Omega(n)$ steps, and the linear sieve takes $O(n)$. So the problem takes $\Theta(n)$ time on the word RAM, a proved bound with no conjecture involved.

## Reductions

- **From a factor table.** Given the [smallest prime factor table](/smallest-prime-factor-table/), the whole table of $\varphi$ follows in $O(n)$ steps, from $\varphi(m) = \varphi(m/p)$ times $p$ or $p - 1$, where $p = \mathrm{spf}(m)$.
- **To counting coprime pairs.** The number of pairs $1 \le a, b \le n$ with $\gcd(a, b) = 1$ is $2 \Phi(n) - 1$. See [counting coprime pairs](/counting-coprime-pairs/).
- **To Farey sequences.** The [Farey sequence](/farey-sequence/) of order $n$ has $1 + \Phi(n)$ terms. For $n = 5$ this is $1 + 10 = 11$.

## Applications

- Counting reduced fractions, lattice points visible from the origin, and coprime pairs.
- Reducing exponents with [Euler's theorem](/euler-theorem/) for many moduli at once.
- Counting the primitive roots and the generators of cyclic groups: a cyclic group of order $m$ has $\varphi(m)$ generators.

## References
