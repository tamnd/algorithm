---
tag: VRP0NH
kind: technique
slug: mobius-inversion
name: Möbius inversion
aliases:
- Möbius inversion formula
- Mobius inversion
- inversion over divisors
area: combinatorics/counting-algorithms
level: core
summary: Inverts a sum over divisors or posets to recover the original counts.
prereqs: [mobius-function, inclusion-exclusion-principle]
see_also: [mobius-function, mobius-inversion-formula, dirichlet-convolution, counting-coprime-pairs, euler-totient, necklace-counting, linear-sieve, inclusion-exclusion-principle]
sources:
  - book: isbn:9780387901633
    title: Tom M. Apostol, Introduction to Analytic Number Theory, Springer, 1976
    locator: Chapter 2, Arithmetical Functions and Dirichlet Multiplication (Section 2.2, the Möbius function; Section 2.7, the Möbius inversion formula)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter XVI, Arithmetical functions (Sections 16.3 and 16.4, the Möbius function and the Möbius inversion formula)
  - paper: doi:10.1007/BF00531932
    title: Gian-Carlo Rota, On the foundations of combinatorial theory I, Theory of Möbius functions, Zeitschrift für Wahrscheinlichkeitstheorie und verwandte Gebiete 2, 340 to 368 (1964)
    locator: the Möbius function of a locally finite poset and the general inversion formula
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Chapter 3, Partially Ordered Sets (Section 3.7, The Möbius inversion formula)
---

Möbius inversion recovers a function $g$ from its sums $f(n) = \sum_{d \mid n} g(d)$ over divisors: $g(n) = \sum_{d \mid n} \mu(d) f(n/d)$, where $\mu$ is the [Möbius function](/mobius-function/). As a counting technique it says: when the objects counted "exactly" by $g$ are hard to count, but the objects counted "up to a divisor" by $f$ are easy, count $f$ and invert. It gives the number of [coprime pairs](/counting-coprime-pairs/), [Euler's totient](/euler-totient/), the number of aperiodic strings and [necklaces](/necklace-counting/), and the number of irreducible polynomials over a finite field. On a general partial order, the same idea is Rota's Möbius inversion, and on the subsets of a set it is the [inclusion-exclusion principle](/inclusion-exclusion-principle/).

## In plain words

Sometimes the number you want is hidden inside a total that is easy to count. For example, it is easy to count the pairs of numbers that are both even, or both multiples of three, but harder to count the pairs that share no factor at all. The easy totals mix together the cases with each common factor.

Möbius inversion undoes the mixing. It takes the easy totals and adds and subtracts them with fixed signs, so that each case with a common factor cancels out and only the wanted case is left. The signs come from a fixed table that depends only on the factors, not on the problem, and a sieve computes it fast.

## When it applies

- The objects you want are those with an "exact" parameter, such as $\gcd = 1$, a primitive period, or an exact set of properties, and the objects whose parameter is a *multiple* (or a divisor) of a given value are easy to count.
- The relation between the easy and the exact counts is a sum over divisors or over multiples, or more generally over the elements below a given element in a partial order.
- The range is $1 \le d \le N$ with $N$ up to about $10^7$ for a sieve of $\mu$, or the sum can be grouped by the values of $\lfloor N/d \rfloor$.

## The template

Notation: $d \mid n$ means that $d$ divides $n$; $\mu(n) = (-1)^r$ if $n$ is a product of $r$ distinct primes (so $\mu(1) = 1$), and $\mu(n) = 0$ if $p^2 \mid n$ for some prime $p$. $N$ is the upper end of the range. Arithmetic is on exact integers, or modulo a prime $p$ when the counts are large; $\mu$ takes only the values $-1, 0, 1$.

**Lemma.** $\sum_{d \mid n} \mu(d) = 1$ if $n = 1$, and $0$ if $n > 1$.

*Proof.* For $n = 1$ the sum is $\mu(1) = 1$. For $n > 1$ with $r \ge 1$ distinct prime factors, only the squarefree divisors contribute, and they correspond to the subsets of the $r$ primes, so the sum is $\sum_{j=0}^{r}\binom{r}{j}(-1)^j = (1 - 1)^r = 0$ by the [binomial theorem](/binomial-theorem/). $\square$

**Theorem (Möbius inversion, divisor form).** For functions $f, g$ on the positive integers, $f(n) = \sum_{d \mid n} g(d)$ for all $n \ge 1$ if and only if $g(n) = \sum_{d \mid n} \mu(d) f(n/d)$ for all $n \ge 1$.

*Proof.* Assume the first relation. Then
$$\sum_{d \mid n} \mu(d) f(n/d) = \sum_{d \mid n} \mu(d) \sum_{e \mid n/d} g(e) = \sum_{e \mid n} g(e) \sum_{d \mid n/e} \mu(d) = g(n),$$
because the pairs $(d, e)$ with $d \mid n$ and $e \mid n/d$ are the pairs with $e \mid n$ and $d \mid n/e$, and by the lemma the inner sum is $1$ for $e = n$ and $0$ otherwise. The converse is the same computation with the roles exchanged: $\sum_{d \mid n} \sum_{e \mid d} \mu(e) f(d/e) = \sum_{m \mid n} f(m) \sum_{e \mid n/m} \mu(e) = f(n)$. $\square$

**Theorem (multiples form).** Let $N \ge 1$ and let $F, G$ be functions on $[N]$. Then $F(d) = \sum_{d \mid m,\ m \le N} G(m)$ for all $d \in [N]$ if and only if $G(d) = \sum_{d \mid m,\ m \le N} \mu(m/d) F(m)$ for all $d \in [N]$. The proof is the same, with $m = d e$.

The multiples form is the one used for counting: $F(d)$ counts the objects whose parameter is a multiple of $d$, which is often a simple product, and $G(1)$ is the number of objects whose parameter is exactly $1$.

```pseudo id=main
MOBIUS-COUNT(N)
L1  compute μ(1), ..., μ(N) with a linear sieve
L2  for d ← 1 to N do
L3      F[d] ← the number of objects whose parameter is a multiple of d   ▷ hole: the easy count
L4  G ← 0
L5  for d ← 1 to N do
L6      if μ(d) ≠ 0 then G ← G + μ(d) · F[d]
L7  return G                                     ▷ the number with parameter exactly 1
```

Line L3 is the problem-specific step. Line L1 takes $O(N)$ time with a [linear sieve](/linear-sieve/), or the [Möbius sieve](/mobius-sieve/). To get $G(d)$ for every $d$ instead of only $G(1)$, loop over the multiples of each $d$; the total work is $\sum_{d \le N} N/d = O(N \log N)$ by the [harmonic series](/harmonic-series/).

## Classic examples

**1. Coprime pairs.** Count the pairs $(a, b) \in [N]^2$ with $\gcd(a, b) = 1$. The pairs with $d \mid \gcd(a, b)$ are the pairs of multiples of $d$, so $F(d) = \lfloor N/d \rfloor^2$, and the answer is $\sum_{d=1}^{N} \mu(d)\lfloor N/d \rfloor^2$. For $N = 10$, with $\mu(1), \ldots, \mu(10) = 1, -1, -1, 0, -1, 1, -1, 0, 0, 1$: $100 - 25 - 9 - 4 + 1 - 1 + 1 = 63$. For $N = 1000$ the count is $608383$, close to $(6/\pi^2) N^2 \approx 607927$. See [counting coprime pairs](/counting-coprime-pairs/).

**2. Euler's totient.** Each $k \in [n]$ has $\gcd(k, n) = d$ for exactly one divisor $d$, and the $k$ with $\gcd(k, n) = d$ correspond to the $j \in [n/d]$ coprime to $n/d$. So $n = \sum_{d \mid n} \varphi(d)$ ([totient divisor sum](/totient-divisor-sum/)), and inversion gives $\varphi(n) = \sum_{d \mid n} \mu(d)\, n/d$. For $n = 12$: $12 - 6 - 4 + 2 = 4$.

**3. Aperiodic strings and necklaces.** Each string of length $n$ over $k$ letters is a power $w^{n/d}$ of a unique primitive (aperiodic) string $w$ of length $d \mid n$. So $k^n = \sum_{d \mid n} M(d)$, with $M(d)$ the number of primitive strings of length $d$, and $M(n) = \sum_{d \mid n} \mu(d) k^{n/d}$. For $n = 6$, $k = 2$: $64 - 8 - 4 + 2 = 54$. Each primitive necklace (Lyndon word) has $n$ distinct rotations, so there are $54/6 = 9$ binary Lyndon words of length 6, which is also the number of monic irreducible polynomials of degree 6 over the field with two elements. See [necklace counting](/necklace-counting/).

**4. Squarefree numbers.** The number of squarefree integers in $[N]$ is $\sum_{d \le \sqrt N} \mu(d)\lfloor N/d^2 \rfloor$, by inversion over the largest square divisor. For $N = 100$ it is $100 - 25 - 11 - 4 + 2 - 2 + 1 = 61$.

**5. Inclusion-exclusion.** On the lattice of subsets of $[m]$, ordered by inclusion, the Möbius function is $\mu(S, T) = (-1)^{|T| - |S|}$ for $S \subseteq T$, and Rota's inversion formula is the function form of inclusion-exclusion.

## Variations

- **Dirichlet convolution.** With $(f * g)(n) = \sum_{d \mid n} f(d) g(n/d)$ and $\mathbf{1}(n) = 1$, the lemma says $\mu * \mathbf{1} = \varepsilon$, the identity for $*$, and inversion is $f = g * \mathbf{1} \iff g = f * \mu$. See [Dirichlet convolution](/dirichlet-convolution/) and the [Möbius inversion formula](/mobius-inversion-formula/).
- **Without $\mu$.** In the multiples form, $G(d) = F(d) - \sum_{k \ge 2,\ kd \le N} G(kd)$, computed for $d = N, N - 1, \ldots, 1$. This also takes $O(N \log N)$ and needs no sieve; it is the same inversion, unrolled.
- **Grouping by quotients.** In example 1, $\lfloor N/d \rfloor$ takes only $O(\sqrt N)$ distinct values. With prefix sums of $\mu$ (the Mertens function), the sum is computed in $O(\sqrt N)$ steps once those prefix sums are known; see [floor division](/floor-division/).
- **Posets (Rota).** For a locally finite partial order, define $\mu(x, x) = 1$ and $\mu(x, y) = -\sum_{x \le z < y} \mu(x, z)$ for $x < y$. Then $f(y) = \sum_{x \le y} g(x)$ for all $y$ if and only if $g(y) = \sum_{x \le y} \mu(x, y) f(x)$ (Rota, 1964; Stanley, Section 3.7). The divisor form is the case of the order "divides", where $\mu(d, n) = \mu(n/d)$.
- **Multiplicative functions.** If $f$ is multiplicative, so is $g = f * \mu$, and $g$ can be computed from prime powers with a sieve.

## Pitfalls

- **Divisors or multiples.** The divisor form sums over $d \mid n$, the multiples form over $d \mid m \le N$. Using the wrong one inverts the wrong relation. Write the easy relation down first.
- **The easy count must be over all multiples.** $F(d)$ must count every object whose parameter is a multiple of $d$, including those with parameter $2d$, $3d$, and so on. Counting "exactly $d$" in line L3 makes the inversion meaningless.
- **$\mu$ of non-squarefree numbers.** $\mu(4) = \mu(8) = \mu(9) = 0$, not $\pm 1$. A sieve that only flips signs at each prime gets these wrong.
- **Quadratic loops.** Summing over all pairs $(d, m)$ with $d, m \le N$ costs $O(N^2)$; loop over multiples only, for $O(N \log N)$.
- **Overflow.** $\lfloor N/d \rfloor^2$ and the partial sums can exceed 64 bits for large $N$, and the partial sums can be negative. Reduce modulo $p$ with care, or use big integers.

## Exercises

1. Count the pairs $(a, b) \in [N] \times [M]$ with $\gcd(a, b) = g$, and check it for $N = M = 10$, $g = 2$ by listing.
2. Show that the number of monic irreducible polynomials of degree $n$ over a field with $q$ elements is $\frac1n\sum_{d \mid n}\mu(d) q^{n/d}$, given that $x^{q^n} - x$ is the product of all monic irreducibles of degree dividing $n$.
3. Compute $\sum_{i=1}^{N}\sum_{j=1}^{N} \gcd(i, j)$ using $\gcd(i, j) = \sum_{d \mid \gcd(i,j)} \varphi(d)$, in $O(N)$ time after a sieve.

## References
