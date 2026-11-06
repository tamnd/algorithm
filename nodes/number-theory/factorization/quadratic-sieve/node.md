---
tag: 5TWHZJ
kind: algorithm
slug: quadratic-sieve
name: Quadratic sieve
aliases:
- QS
- Pomerance's quadratic sieve
area: number-theory/factorization
level: advanced
summary: Finds the smooth values of f(x) = x^2 - N near sqrt(N) with a sieve, as for primes, and combines them mod 2 into a congruence of squares. Heuristically L_N[1/2, 1].
solves: [integer-factorization]
model: word-ram
complexity:
  vars: {N: the integer to factor, n: the number of binary digits of N, B: the smoothness bound, K: the size of the factor base, M: the block length, V: the number of values sieved}
  time: {worst: O(V K + K^3), heuristic: exp((1 + o(1)) (ln N ln ln N)^(1/2))}
  space: {extra: O(K^2 + M)}
  sieve_operations: {heuristic: O(V log log B)}
properties: {deterministic: true, recursive: false}
prereqs: [relation-collection, congruence-of-squares, smooth-number, sieve-of-eratosthenes, tonelli-shanks]
see_also: [multiple-polynomial-quadratic-sieve, continued-fraction-factorization, dixon-random-squares, general-number-field-sieve, knuth-schroeppel-multiplier, block-lanczos-algorithm, structured-gaussian-elimination, integer-factorization]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 6.1.1, Basic QS, pages 261 to 266 (the example 1649, exponent vectors, the choice of B and the heuristic L(n)^(1+o(1))); Section 6.1.2, Algorithm 6.1.1 and its remarks, pages 266 to 268 (sieving by logarithms, negative values); Section 6.1.3, pages 268 to 270; Section 6.1.4, Large prime variations, pages 270 to 273; Section 6.1.5, page 274 (the values grow along the interval)
  - paper: "Carl Pomerance, Analysis and comparison of some integer factoring algorithms, in Computational Methods in Number Theory, Part I, Mathematical Centre Tracts 154, Mathematisch Centrum, Amsterdam, 1982"
    locator: pages 89 to 139 (the quadratic sieve and its heuristic analysis)
  - paper: "Carl Pomerance, The quadratic sieve factoring algorithm, Advances in Cryptology, EUROCRYPT '84, Lecture Notes in Computer Science 209, 1985"
    locator: pages 169 to 182 (a survey of the method and its variants)
  - paper: "Carl Pomerance, A tale of two sieves, Notices of the American Mathematical Society 43(12), 1996"
    locator: pages 1473 to 1485 (the history of the quadratic sieve, from Fermat and Kraitchik to Schroeppel's linear sieve)
---

The quadratic sieve, QS, factors an integer $N$ by collecting values of $f(x) = x^2 - N$ for $x$ near $\sqrt N$ that are [smooth](/smooth-number/) over a [factor base](/factor-base/) of small primes, and by combining them with linear algebra over the field with two elements into a [congruence of squares](/congruence-of-squares/). Its key step is that the values of a polynomial can be tested for smoothness all at once by a sieve, like the [sieve of Eratosthenes](/sieve-of-eratosthenes/): a prime $p$ divides $f(x)$ exactly when $x$ lies in one of two residue classes modulo $p$. This cuts the cost per value from about $K$ trial divisions to about $\ln \ln B$ additions, and gives the heuristic running time $L_N[1/2, 1]$. Carl Pomerance introduced it in 1982, and it was the fastest general method until the [number field sieve](/general-number-field-sieve/).

## In plain words

Square the whole numbers near the square root of the number to factor, and subtract the number. The results are fairly small. Keep those that break completely into small primes from a fixed list. When there are more kept results than primes in the list, some group of them multiplies to a perfect square, and this gives two numbers with the same square modulo the number to factor, so one gcd usually shows a factor.

The trick is how to find the results that break into small primes. A small prime divides these results in a fixed pattern: every so many steps, starting from two known places. So write the results in a row, walk along it with each prime at its step, and mark where it divides. The places with many marks are the ones to keep. This is much faster than dividing every result by every prime.

## The problem

**Input.** An odd integer $N \ge 3$ that is not a perfect square, a smoothness bound $B$, a block length $M$, a count $E \ge 1$ of extra relations, and a limit $J$ on the number of blocks.

**Output.** A proper factor $g$ of $N$ (with $1 < g < N$), or $1$ for a failure with these parameters. A prime $N$ always gives $1$.

**The polynomial and the factor base.** Let $s = \lfloor \sqrt N \rfloor$ and $f(t) = (s + t)^2 - N$. Then $(s + t)^2 \equiv f(t) \pmod N$, and for $|t|$ much smaller than $\sqrt N$, $|f(t)| \approx 2|t|\sqrt N$. An odd prime $p \nmid N$ divides some $f(t)$ only if $N$ is a [quadratic residue](/quadratic-residue/) modulo $p$; then $p \mid f(t)$ exactly when $s + t \equiv \pm r_p \pmod p$, where $r_p^2 \equiv N \pmod p$ is found by [Tonelli-Shanks](/tonelli-shanks/). So the factor base $F$ is $-1$, $2$, and the odd primes $p \le B$ with [Legendre symbol](/legendre-symbol/) $(N/p) = 1$; its size $K$ is about $\pi(B)/2$. Since $N$ is odd, $2 \mid f(t)$ exactly when $s + t$ is odd.

**Cost model.** On the [word RAM](/word-ram/) with $N < 2^w$, a sieve step (an addition of an approximate logarithm to an array entry) costs $O(1)$, and a trial division of a candidate by the $K$ primes costs $O(K)$. For an arbitrary-precision $N$ with $n$ binary digits, the sieve steps are still word operations, because they touch only small logarithms, while the evaluation and trial division of a candidate cost $O(K n^2)$ bit operations or less. The time $O(VK + K^3)$ for $V$ values sieved is a proved bound for fixed parameters; the subexponential bound is a heuristic.

## The algorithm

$R$ is the list of relations, each a pair of $s + t$ and the exponent vector of $f(t)$ over $F$. $S$ is the sieve array for one block.

```pseudo id=main
QS(N, B, M, E, J)                ▷ N odd, not a square; returns a proper factor of N or 1
L1  s ← ⌊√N⌋, F ← −1, 2 and the odd p ≤ B with (N/p) = 1; for each odd p in F, find r_p with r_p² ≡ N (mod p)
L2  R ← empty, j ← 0; while |R| < |F| + E and j < J do
L3      for each block W of M values of t, first [jM, (j + 1)M), then [−(j + 1)M, −jM), keeping s + t ≥ 1 do
L4          S[t] ← 0 for t in W; for each p in F, p > 0, and each root class c of p: for each t in W with s + t ≡ c (mod p): S[t] ← S[t] + log p
L5          for each t in W with S[t] ≥ log |f(t)| − τ do
L6              if f(t) factors completely over F then append (s + t, its exponent vector) to R
L7      j ← j + 1
L8  for each nonempty subset T of R whose exponent vectors add to 0 mod 2 do: X ← ∏ x over T mod N, Y ← ∏ over p > 0 in F of p^(e_p/2) mod N, g ← gcd(X − Y, N); if 1 < g < N then return g
L9  return 1
```

Line L1 builds the factor base and the two root classes $\pm r_p$ of each odd prime; for $p = 2$ the one class is $1$. Lines L2 and L3 walk outward from $t = 0$ in blocks, so that the values $|f(t)|$ stay as small as possible. Line L4 is the sieve: for each root class it adds $\log p$ to every $p$-th entry, starting at the first $t$ in the block with $s + t$ in that class. At an entry where $f(t)$ is smooth, the sum is close to $\log |f(t)|$, falling short only by the logarithms of repeated prime factors. Line L5 keeps the entries within a tolerance $\tau$ of that, and line L6 confirms each candidate by trial division. Line L8 runs [Gaussian elimination](/gaussian-elimination/) over GF(2) on the exponent vectors, as in [relation collection](/relation-collection/), and tries each dependency. Here $e$ is the sum of the exponent vectors of $T$.

## Example

Let $N = 9073 = 43 \cdot 211$ and $B = 20$. Then $s = 95$, and $N$ is a quadratic residue modulo $3, 7, 11, 13$ but not modulo $5, 17, 19$, so $F = \{-1, 2, 3, 7, 11, 13\}$. The roots are $r_3 = 1$, $r_7 = 1$, $r_{11} = 3$ and $r_{13} = 5$, so the root classes are $x \equiv 1, 2 \pmod 3$, $x \equiv 1, 6 \pmod 7$, $x \equiv 3, 8 \pmod{11}$, $x \equiv 5, 8 \pmod{13}$, and $x$ odd for $p = 2$. Sieve $x = s + t$ for $t \in [-10, 10)$:

| $x$ | $f = x^2 - N$ | primes that hit $x$ | left after dividing them out | smooth? |
|---|---|---|---|---|
| 85 | $-1848$ | 2, 3, 7, 11 | 1 | yes |
| 86 | $-1677$ | 3, 13 | 43 | no |
| 87 | $-1504$ | 2 | 47 | no |
| 88 | $-1329$ | 3 | 443 | no |
| 89 | $-1152$ | 2, 3 | 1 | yes |
| 90 | $-973$ | 7 | 139 | no |
| 91 | $-792$ | 2, 3, 11 | 1 | yes |
| 92 | $-609$ | 3, 7 | 29 | no |
| 93 | $-424$ | 2 | 53 | no |
| 94 | $-237$ | 3 | 79 | no |
| 95 | $-48$ | 2, 3 | 1 | yes |
| 96 | $143$ | 11, 13 | 1 | yes |
| 97 | $336$ | 2, 3, 7 | 1 | yes |
| 98 | $531$ | 3 | 59 | no |
| 99 | $728$ | 2, 7, 13 | 1 | yes |
| 100 | $927$ | 3 | 103 | no |
| 101 | $1128$ | 2, 3 | 47 | no |
| 102 | $1331$ | 11 | 1 | yes |
| 103 | $1536$ | 2, 3 | 1 | yes |
| 104 | $1743$ | 3, 7 | 83 | no |

The sieve finds $9$ smooth values among $20$, more than $|F| = 6$. Three of them have a product that is a square: $f(85) f(91) f(97) = (-2^3 \cdot 3 \cdot 7 \cdot 11)(-2^3 \cdot 3^2 \cdot 11)(2^4 \cdot 3 \cdot 7) = 2^{10} \cdot 3^4 \cdot 7^2 \cdot 11^2$. So $X = 85 \cdot 91 \cdot 97 \bmod 9073 = 6309$ and $Y = 2^5 \cdot 3^2 \cdot 7 \cdot 11 \bmod 9073 = 4030$, and $\gcd(6309 - 4030, 9073) = \gcd(2279, 9073) = 43$. So $9073 = 43 \cdot 211$.

## Correctness

The sieve is exact about which primes divide which values: for an odd $p \in F$, $p \mid f(t)$ if and only if $(s + t)^2 \equiv N \pmod p$, that is, $s + t \equiv \pm r_p$; for $p = 2$, if and only if $s + t$ is odd. So line L4 adds $\log p$ to $S[t]$ once for each distinct odd prime of $F$ that divides $f(t)$, and $\log 2$ when $2 \mid f(t)$. Whatever the threshold, line L6 appends a relation only after trial division shows $f(t) = \pm \prod_{p \in F} p^{v_p}$, and then $(s + t)^2 \equiv f(t) \pmod N$. For a subset $T$ whose vectors add to $0$ mod 2, every exponent of $e$ is even, including that of $-1$, so $\prod f = Y^2$ and $X^2 \equiv Y^2 \pmod N$. Line L8 returns $g = \gcd(X - Y, N)$ only if $1 < g < N$, and the loops are bounded by $J$ blocks of $M$ values and by $|R|$ subsets. So the output is a proper factor or $1$, and the algorithm stops. The full proof is below.

The threshold affects only how many smooth values are found, not correctness. Why a dependency splits $N$ is a heuristic, as for [CFRAC](/continued-fraction-factorization/): QS is not randomized, but if $X$ behaves like a random square root of $Y^2$, a dependency splits an $N$ with two or more distinct prime factors with probability at least $1/2$ (Crandall and Pomerance).

## Complexity

- **Sieve.** For a block of $M$ values, each root class of $p$ gives about $M/p + 1$ steps, so the sieve costs $O(M \sum_{p \le B} 1/p + K) = O(M \ln \ln B + K)$ additions, by Mertens' theorem. For $M \ge B$ this is $O(\ln \ln B)$ per value, against $K$ divisions per value for trial division.
- **Candidates and matrix.** Each candidate costs $O(K)$ divisions. Gaussian elimination on $K + E$ vectors of length $K + 1$ costs $O(K^3)$, or $O(K^3/w)$ with rows packed in words, and [block Lanczos](/block-lanczos-algorithm/) or [Wiedemann](/wiedemann-algorithm/) methods reduce it to about $O(K^2)$ times the number of nonzero entries per row.
- **Proved bound for fixed parameters.** At most $V = 2JM$ values, so $O(VK + K^3)$ word operations, even if every value is a candidate.
- **Heuristic bound.** Assume that the values $f(t)$ are as often smooth as random numbers of their size, about $N^{1/2 + o(1)}$. With $u = \ln N/(2\ln B)$, a value is smooth with probability about $u^{-u}$, so $K u^u$ values are needed, each at cost $\ln \ln B$. The minimum is at $B = \exp((\frac12 + o(1))\sqrt{\ln N \ln \ln N}) = L_N[1/2, 1/2]$, and the time is $B^{2 + o(1)} = L_N[1/2, 1] = \exp((1 + o(1))\sqrt{\ln N \ln \ln N})$, with the matrix step of the same order with sparse methods (Crandall and Pomerance, Section 6.1.1 and 6.1.3). This is a heuristic: no proof that the values of $x^2 - N$ are smooth this often is known.
- **Space.** $O(M)$ for the sieve array, $O(K)$ for the roots, and $O(K^2)$ bits for the matrix.

## Properties

- **A sieve on a polynomial.** The divisibility of $f(t)$ by $p$ depends only on $t \bmod p$. This is what CFRAC and Dixon's method lack, and it is the source of the speed of QS.
- **Approximate logarithms.** The sieve can add rounded values of $\log_2 p$ in one byte per entry, and it can skip the smallest primes and the prime powers; the tolerance $\tau$ makes up for these errors (Crandall and Pomerance).
- **Growing values.** $|f(t)| \approx 2|t|\sqrt N$ grows along the interval, so the yield of smooth values falls as the sieve moves away from $\sqrt N$. With one polynomial the interval must have length about $B^2 = L_N[1/2, 1]$. The [multiple polynomial](/multiple-polynomial-quadratic-sieve/) variant removes this loss.
- **Deterministic.** For fixed parameters the output is fixed. A failure leads to more relations, a larger $B$, or a multiplier.
- **Independent of the size of the factors.** The run time depends on $N$, not on its smallest prime factor. Remove small factors first with [trial division](/trial-division/), [Pollard's rho](/pollard-rho/) or [ECM](/elliptic-curve-factorization/).

## Variants and improvements

- **Multiple polynomials.** Sieve many polynomials $(ax + b)^2 - N$ over short intervals, so that all values stay small. See the [multiple polynomial quadratic sieve](/multiple-polynomial-quadratic-sieve/) and its self initializing form.
- **Large primes.** Keep values that are smooth except for one prime between $B$ and about $100B$, or two such primes, and match them in cycles. The double large prime variation of Lenstra and Manasse was used for the factorization of RSA-129 (Crandall and Pomerance, Section 6.1.4). See [relation collection](/relation-collection/).
- **A multiplier.** Factor $kN$ for a small $k$ chosen so that many small primes are in the factor base. The [Knuth-Schroeppel multiplier](/knuth-schroeppel-multiplier/) rule makes this choice.
- **Fast linear algebra.** [Structured Gaussian elimination](/structured-gaussian-elimination/), [block Lanczos](/block-lanczos-algorithm/) and [block Wiedemann](/block-wiedemann-algorithm/) handle the large sparse matrices of big factorizations.
- **Small prime variation.** Do not sieve with the primes below about $30$ and their powers, and lower the threshold to match. This saves much of the sieve time.

## When to use it

QS, in its multiple polynomial form, is the method of choice for general $N$ of moderate size, up to around 100 decimal digits, with no special form and no small factors. For larger $N$ the [general number field sieve](/general-number-field-sieve/) is faster, as its heuristic bound $L_N[1/3, (64/9)^{1/3}]$ suggests. For small factors of any $N$, use [Pollard's rho](/pollard-rho/) or the [elliptic curve method](/elliptic-curve-factorization/) first, since QS gains nothing from a small factor. For $N$ below about $2^{64}$, [SQUFOF](/shanks-squfof/) or rho is simpler.

## Pitfalls

- **Primes outside the factor base.** An odd prime $p \nmid N$ with $(N/p) = -1$ never divides $f(t)$. Sieving with it is wasted work, and putting it in the vectors adds empty columns.
- **Primes that divide $N$.** If $p \le B$ divides $N$, a factor is already found. Test this while building the factor base.
- **The sign.** Values with $t < 0$ are negative. Keep $-1$ as a coordinate of the vectors, or the products are squares only up to sign.
- **The threshold.** A tolerance $\tau$ that is too small loses smooth values with repeated prime factors. One that is too large makes many false candidates and wastes trial divisions. Every candidate must be confirmed by trial division.
- **Small $N$.** For small $N$ there may be few primes with $(N/p) = 1$ below $B$, and smooth values become rare. Make sure the factor base has some minimum size.
- **Perfect squares and prime powers.** For $N = s^2$, $f(0) = 0$. For $N = p^j$ every dependency is trivial. Test for perfect powers first.
- **Duplicate values of $x$.** If the blocks overlap or reach $s + t \le 0$, the same $x^2$ appears twice and gives a trivial dependency. Keep $s + t \ge 1$ and the blocks disjoint.

## Implementations

## History

The idea of combining several congruences $x^2 \equiv a \pmod N$ goes back to Maurice Kraitchik in the 1920s, who extended Fermat's method this way, and the systematic use of a factor base and linear algebra mod 2 to Morrison and Brillhart's [continued fraction method](/continued-fraction-factorization/). Richard Schroeppel's linear sieve of the late 1970s first used sieving to find smooth values. Carl Pomerance introduced the quadratic sieve in 1982 together with a heuristic analysis of several methods. With the multiple polynomial variant of Peter Montgomery and the large prime variations it set the factoring records of the 1980s and early 1990s, up to RSA-129 in 1994, before the number field sieve overtook it.

## References
