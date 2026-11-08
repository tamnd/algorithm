---
tag: S7DSDC
kind: algorithm
slug: multiple-recursive-generator
name: Multiple recursive generator
aliases:
- MRG
- multiple recursive congruential generator
- linear recurrence modulo a prime
area: numerical/random-number-generation
level: advanced
summary: A generalization of the LCG where each output depends linearly on several previous outputs modulo m.
model: word-ram
complexity:
  vars: {k: "the order of the recurrence", m: "the prime modulus"}
  time: {worst: Θ(k)}
  space: {extra: Θ(k)}
properties: {deterministic: true, in_place: true, recursive: false}
prereqs: [linear-congruential-generator, primitive-polynomial, generator-period]
see_also: [mrg32k3a, lecuyer-combined-generator, lagged-fibonacci-generator, spectral-test, jump-ahead, matrix-power, park-miller-minimal-standard, multiply-with-carry]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.2.2, the linear recurrence x_n = (a_1 x_(n-1) + ... + a_k x_(n-k)) mod p, the maximal period p^k - 1 when the polynomial is primitive, and the three conditions for a primitive polynomial modulo p
  - paper: doi:10.1145/169702.169698
    title: Pierre L'Ecuyer, François Blouin and Raymond Couture, A search for good multiple recursive random number generators, ACM Transactions on Modeling and Computer Simulation 3(2), 1993, pages 87 to 98
    locator: the maximal period condition, the search with r = (m^k - 1)/(m - 1) prime, the spectral test for MRGs and the tables of good parameters
  - paper: doi:10.1287/opre.47.1.159
    title: Pierre L'Ecuyer, Good parameters and implementations for combined multiple recursive random number generators, Operations Research 47(1), 1999, pages 159 to 164
    locator: the components of MRG32k3a and the requirement that (m^k - 1)/(m - 1) be prime
  - paper: doi:10.1287/ijoc.9.1.57
    title: Pierre L'Ecuyer, Bad lattice structures for vectors of non-successive values produced by some linear recurrences, INFORMS Journal on Computing 9(1), 1997, pages 57 to 60
    locator: the hyperplane bound in terms of the sum of squares of the coefficients, which rules out recurrences with few small non-zero coefficients
---

A multiple recursive generator (MRG) of order $k$ computes $x_n = (a_1 x_{n-1} + a_2 x_{n-2} + \cdots + a_k x_{n-k}) \bmod m$ for a prime $m$ and outputs $u_n = x_n / m$. It is the [linear congruential generator](/linear-congruential-generator/) with $c = 0$ extended from one previous value to $k$. If the characteristic polynomial $z^k - a_1 z^{k-1} - \cdots - a_k$ is a [primitive polynomial](/primitive-polynomial/) modulo $m$, every non-zero seed gives the maximal period $m^k - 1$, so a modulus near $2^{31}$ or $2^{32}$ gives periods near $2^{32k}$ while the arithmetic stays in machine words. MRGs and their combinations, such as [MRG32k3a](/mrg32k3a/), are standard generators for stochastic simulation.

## In plain words

A linear congruential generator makes each number from the previous one: multiply, take the remainder. A multiple recursive generator makes each number from the last few numbers: multiply each of them by its own constant, add, and take the remainder after division by a prime.

Because the generator remembers several numbers, it can go through far more combinations before it repeats. With three remembered numbers below about four billion, the sequence can run for about $10^{28}$ steps. The constants must be chosen so that this maximum is reached, which a test from number theory decides, and so that the outputs do not fall on a few planes.

## The problem

We use the notation of the [pseudorandom number generator](/pseudorandom-number-generator/) page. The modulus $m$ is a prime, and the multipliers $a_1, \ldots, a_k$ lie in $\{0, \ldots, m - 1\}$ with $a_k \ne 0$. The state is the vector $s_n = (x_{n-1}, \ldots, x_{n-k})$, in $S = \mathbb{Z}_m^k \setminus \{0\}$. The transition $f$ is the linear map with the companion matrix

$$M = \begin{pmatrix} a_1 & a_2 & \cdots & a_{k-1} & a_k \\ 1 & 0 & \cdots & 0 & 0 \\ & \ddots & & & \vdots \\ 0 & \cdots & & 1 & 0 \end{pmatrix},$$

and the output is $u_n = x_n / m$ in $[0, 1)$, or $(x_n + 1)/(m + 1)$ to avoid 0. The tasks are to choose $a_j$ for the maximal period $\rho = m^k - 1$ and a good lattice structure, and to compute a step cheaply without overflow.

## The algorithm

The state $x[1..k]$ holds the last $k$ values, newest first.

```pseudo id=main
MRG-NEXT(x[1..k], a[1..k], m)              ▷ x not all zero, m prime
L1  s ← 0
L2  for j ← 1 to k do s ← (s + a_j · x_j) mod m
L3  for j ← k down to 2 do x_j ← x_(j−1)
L4  x_1 ← s
L5  return s                               ▷ the output is u = s / m
```

In practice most $a_j$ are 0, and the shift of line L3 is a circular buffer index, so a step costs a few multiplications. MRG32k3a, for example, has $k = 3$ and two non-zero multipliers in each component. To compute $a_j x_j \bmod m$ without overflow, implementations use 64-bit integers, double-precision floating point with $a_j (m - 1) < 2^{53}$, or Schrage's decomposition as in the [Park-Miller generator](/park-miller-minimal-standard/).

**Choosing the multipliers.** Knuth (Section 3.2.2) gives a test for primitivity of $P(z) = z^k - a_1 z^{k-1} - \cdots - a_k$ modulo $p$, with $r = (p^k - 1)/(p - 1)$:

1. $(-1)^{k-1} a_k$ is a [primitive root](/primitive-root/) modulo $p$;
2. $z^r \bmod P(z)$ is the constant $(-1)^{k-1} a_k$;
3. for each prime $q$ dividing $r$, $z^{r/q} \bmod P(z)$ is not a constant.

The test needs the prime factors of $p - 1$ and of $r$. L'Ecuyer chooses moduli for which $r$ is itself prime, so the factorization is trivial. Among primitive candidates, he keeps those with the best [spectral test](/spectral-test/) values.

**Jumping ahead.** $s_{n+J} = M^J s_n \bmod m$, and $M^J$ costs $O(k^3 \log J)$ operations by [matrix powering](/matrix-power/). This splits the period into streams, as on the [jump-ahead](/jump-ahead/) page.

## Example

Take $m = 7$, $k = 2$ and $x_n = (x_{n-1} + 4 x_{n-2}) \bmod 7$. Then $P(z) = z^2 - z - 4$, and $(-1)^{1} \cdot 4 \equiv 3$ is a primitive root modulo 7 (its powers are 3, 2, 6, 4, 5, 1). From $x_{-1} = 0$ and $x_0 = 1$:

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $x_n$ | 1 | 5 | 2 | 1 | 2 | 6 | 0 | 3 | 3 | 1 | 6 | 3 |

For instance $x_2 = 1 + 4 \cdot 1 = 5$ and $x_3 = 5 + 4 \cdot 1 = 9 \equiv 2$. The sequence has period $48 = 7^2 - 1$: every non-zero pair $(x_n, x_{n-1})$ appears once per period. Over a period, each non-zero residue appears 7 times and 0 appears 6 times. A single output can be 0 even though the state is never zero. With $a_2 = 3$ instead, $-3 \equiv 4$ has order 3 modulo 7, condition 1 fails, and the period is only 24.

## Correctness

Correctness means: if $P$ is primitive modulo the prime $m$, every non-zero seed has period exactly $m^k - 1$, and the $k$-tuples $(x_n, \ldots, x_{n-k+1})$ run through all non-zero vectors once per period. The proof, below, follows the same plan as for [xorshift](/xorshift/) over $\mathrm{GF}(2)$:

1. The characteristic polynomial of the companion matrix $M$ is $P$, and $M$ is invertible because $a_k \ne 0$.
2. $P$ is primitive if and only if $M$ has order $m^k - 1$, because then $\mathbb{Z}_m[M]$ is the field with $m^k$ elements and $M$ generates its multiplicative group.
3. If $M$ has order $m^k - 1$, then for $s \ne 0$, $M^\rho s = s$ forces $M^\rho = I$, since $M^\rho - I$ is either 0 or invertible in that field. So every non-zero state has period $m^k - 1$, and its orbit is all of $S$.

The tests of the implementation enumerate all coefficient vectors for small $p$ and $k$ and check that the period from a non-zero seed is $p^k - 1$ exactly when Knuth's three conditions hold. They also verify the two components of MRG32k3a, with the primes $m$ and $r = m^2 + m + 1$.

## Complexity

A step costs $k$ multiplications, $k$ additions and one reduction modulo $m$, or as many as there are non-zero $a_j$: $\Theta(k)$ word operations in general and $\Theta(1)$ for a fixed sparse recurrence. The state is $k$ words. A jump of $J$ steps costs $O(k^3 \log J)$ with the matrix, or $O(k^2 \log J)$ with polynomials modulo $P$.

## Properties

- **Maximal period** $m^k - 1$ when $P$ is primitive (proved). The all-zero state is a fixed point.
- **Equidistribution.** Over a period every non-zero $k$-tuple of successive values appears once, so the output is equidistributed in dimensions up to $k$, up to the missing zero tuple.
- **Lattice structure.** For $t > k$, the vectors $(u_n, \ldots, u_{n+t-1})$, over all states, form the points of a lattice intersected with the unit cube, and the [spectral test](/spectral-test/) measures the distance between its hyperplanes.
- **Small coefficients are bad.** For every vector of $k + 1$ successive outputs, $u_n - a_1 u_{n-1} - \cdots - a_k u_{n-k}$ is an integer. So all such points lie on hyperplanes at distance $(1 + a_1^2 + \cdots + a_k^2)^{-1/2}$ from each other (proved; L'Ecuyer 1997). A [lagged Fibonacci generator](/lagged-fibonacci-generator/) with $a_j \in \{0, \pm 1\}$ puts its points on planes $1/\sqrt{3}$ apart in that dimension.
- **Not secure.** The recurrence is linear; $2k$ outputs determine it, and $k$ consecutive outputs give the state.

## Variants and improvements

- **Combined MRGs.** Adding the outputs of two or more MRGs with different prime moduli gives a generator whose period is the least common multiple of the periods and whose structure is that of one MRG with a huge modulus, but with small, fast components. [MRG32k3a](/mrg32k3a/) combines two MRGs of order 3. The [L'Ecuyer combined generator](/lecuyer-combined-generator/) of 1988 is the case $k = 1$.
- **Fast MRGs (DX generators).** Deng and Lin, and later Deng and Xu, use MRGs with very large order $k$, such as several thousand, and only one or two non-zero coefficients of special form, for very long periods at the cost of one or two multiplications.
- **MRGs modulo 2.** With $m = 2$ the recurrence is a [linear feedback shift register](/linear-feedback-shift-register/), the basis of the [Mersenne Twister](/mersenne-twister/) and [WELL](/well-rng/).
- **Multiply-with-carry.** [Multiply-with-carry](/multiply-with-carry/) and add-with-carry generators emulate an MRG or an LCG with a huge modulus by keeping a carry.

## When to use it

Use a well-chosen combined MRG, in practice [MRG32k3a](/mrg32k3a/) or MRG31k3p, for discrete-event simulation where streams and substreams are needed and the theory of the generator must be documented. Use a single MRG with tested parameters when you need a prime modulus and a long period with simple arithmetic. Avoid MRGs with few small coefficients, such as the additive lagged Fibonacci generators, when the lattice structure matters. For speed with 64-bit integers, [xoshiro256**](/xoshiro-xoroshiro/) or [PCG](/pcg-random/) are faster.

## Pitfalls

- **Overflow.** $a_j x_j$ needs up to $2 \lceil \log_2 m \rceil$ bits. In 32-bit or floating-point code, check that every product is exact, or use Schrage's method.
- **Non-primitive polynomials.** A random choice of $a_j$ almost never gives the maximal period. Test primitivity with the factorizations of $m - 1$ and $(m^k - 1)/(m - 1)$.
- **All-zero seeds.** A seed of $k$ zeros, or of $k$ multiples of $m$, stays at zero. Reject it.
- **Negative coefficients.** Implementations often use $a_j < 0$, as in MRG32k3a, and then compute a signed sum. Reduce the result into $[0, m)$ before the next step, because the remainder operator of many languages returns negative values for negative operands.
- **Output 0.** $x_n = 0$ can occur even with a non-zero state, so $u_n = x_n / m$ can be 0. Use $(x_n + 1)/(m + 1)$ or a combination that avoids 0 when the next step takes a logarithm.

## Implementations

## History

Linear recurrences modulo a prime as generators are discussed by Knuth, who gives the primitivity criterion in Section 3.2.2, and earlier by Alanen and Knuth in 1964. Pierre L'Ecuyer and coauthors developed the theory and tables of good parameters in the 1990s, combining primitivity with the spectral test, and introduced combined MRGs. MRG32k3a (1999) became the generator of many simulation packages. Lih-Yuan Deng and coauthors proposed very high order MRGs with sparse coefficients from 2000 onwards.

## References
