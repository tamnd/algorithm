---
tag: DT65XZ
kind: algorithm
slug: lehman-factorization
name: Lehman's factorization method
aliases:
- Lehman's method
area: number-theory/factorization
level: advanced
summary: Trial division to N^(1/3), then Fermat's method on 4kN for every multiplier k up to N^(1/3), each over a short range of x. It factors N or proves it prime in O(N^(1/3)) operations.
solves: [integer-factorization]
model: word-ram
complexity:
  vars: {N: the integer to factor, n: the number of binary digits of N}
  time: {worst: O(N^(1/3))}
  space: {extra: O(1)}
  bit_operations: {worst: O(N^(1/3) n^2)}
properties: {deterministic: true, recursive: false}
prereqs: [fermat-factorization, trial-division, integer-square-root, greatest-common-divisor]
see_also: [hart-one-line-factorization, shanks-squfof, pollard-rho, congruence-of-squares, knuth-schroeppel-multiplier, continued-fraction, integer-factorization]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 5.1.2, Lehman method, pages 227 to 228 (Algorithm 5.1.2, the cost O(n^(1/3) ln ln n), and Theorem 5.1.3 with its proof); Section 5.1.1 for the multiplier example n = 2581
  - paper: "R. Sherman Lehman, Factoring large integers, Mathematics of Computation 28(126), 1974"
    locator: pages 637 to 646
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Theorem 36 (Dirichlet's theorem on approximation by fractions with bounded denominator), used in the proof
---

Lehman's method factors an integer $N$ in $O(N^{1/3})$ arithmetic operations in the worst case, with a proof that needs no unproved hypothesis. It first runs [trial division](/trial-division/) up to $N^{1/3}$. If that finds nothing, $N$ is a prime or a product $pq$ of two primes above $N^{1/3}$, and the method runs [Fermat's method](/fermat-factorization/) on $4kN$ for each multiplier $k \le N^{1/3}$, each time over a range of only about $N^{1/6}/(4\sqrt k)$ values. A theorem on rational approximation shows that some $k$ makes $4kN$ a product of two very close numbers, so one of these short searches succeeds.

## In plain words

Fermat's method is fast when the two factors of a number are close, and slow otherwise. A trick can fix this: multiply the number by a small $k$. If the factors are $p$ and $q$ and $p/q$ is close to a fraction $v/u$, then $uq$ and $vp$ are close, and $kN = (uq)(vp)$ with $k = uv$ is easy for Fermat.

You do not know the right $k$, so try them all, up to the cube root of the number, and for each one walk only a short distance. A classical result says that every ratio $p/q$ has a good enough fraction with small numerator and denominator, so one of the walks will hit a square.

The small factors, below the cube root, would spoil this argument, so remove them first with trial division. If nothing works, the number is prime.

## The problem

**Input.** An integer $N \ge 22$.

**Output.** A divisor $d$ of $N$ with $1 < d < N$, or $N$ itself if $N$ is a [prime](/prime-number/). So the method is also a deterministic primality test. Applied again to $d$ and $N/d$, it gives the full [integer factorization](/integer-factorization/).

**Cost model.** On the [word RAM](/word-ram/) with $N < 2^w$ (and $4N^{4/3} < 2^w$ for the products $4kN$), a division, a multiplication and an [integer square root](/integer-square-root/) cost $O(1)$. For an arbitrary-precision $N$ with $n$ binary digits, each of these costs $O(n^2)$ bit operations with schoolbook arithmetic. Crandall and Pomerance count $O(\ln \ln N)$ operations per perfect-square test with their square root routine, which gives their bound $O(N^{1/3} \ln \ln N)$.

## The algorithm

The tests are written with integers only. The condition $(a^2 - 4kN)^3 < N^2$ means $a^2 - 4kN < N^{2/3}$, which is the range in which the proof finds the solution.

```pseudo id=main
LEHMAN(N)                                 ▷ N ≥ 22; returns d with 1 < d < N and d | N, or N if N is prime
L1  for d = 2, 3, …, ⌊N^(1/3)⌋: if d divides N then return d
L2  for k = 1, 2, …, ⌊N^(1/3)⌋ + 1 do
L3      a ← ⌈√(4kN)⌉
L4      while (a² − 4kN)³ < N² do
L5          if a² − 4kN = b² for an integer b ≥ 0 then return gcd(a + b, N)
L6          a ← a + 1
L7  return N
```

Line L1 removes the small factors. For each multiplier $k$, lines L3 to L6 are Fermat's method on $4kN$: they look for $a^2 - b^2 = 4kN$, starting at the smallest $a$ with $a^2 \ge 4kN$. The loop of line L4 stops when $a^2 - 4kN$ reaches $N^{2/3}$, which happens after at most about $N^{1/6}/(4\sqrt k) + 1$ values of $a$. Line L5 does not return $a - b$ or $a + b$ directly, because the factors of $4kN$ include those of $4k$; the gcd with $N$ removes them.

## Example

Let $N = 2581$. Here $N^{1/3} \approx 13.7$, and no $d \le 13$ divides $2581$, so line L1 finds nothing. The bound of line L4 is $N^2 = 6{,}661{,}561$.

| $k$ | $4kN$ | $a$ | $a^2 - 4kN$ | $(a^2 - 4kN)^3 < N^2$? | square? |
|---|---|---|---|---|---|
| 1 | 10324 | 102 | 80 | yes | no |
| 1 | 10324 | 103 | 285 | no ($23{,}149{,}125$) | |
| 2 | 20648 | 144 | 88 | yes | no |
| 2 | 20648 | 145 | 377 | no | |
| 3 | 30972 | 176 | 4 | yes | yes, $b = 2$ |

Line L5 returns $\gcd(176 + 2, 2581) = \gcd(178, 2581) = 89$, and $2581 = 29 \cdot 89$. The multiplier $k = 3$ works because $29/89$ is close to $1/3$: with $u = 1$, $v = 3$, the numbers $uq = 89$ and $vp = 87$ are close, and $12N = 4 \cdot 87 \cdot 89 = 176^2 - 2^2$. Plain Fermat on $2581$ needs nine values of $x$ (Crandall and Pomerance, Section 5.1.1).

## Correctness

If line L5 returns, then $a^2 - b^2 = 4kN$ with $b < N^{1/3}$ and $k \le N^{1/3} + 1$, so $N$ divides $(a + b)(a - b)$ with $0 < a - b < a + b < N$ (this uses $N \ge 22$), and $\gcd(a + b, N)$ is a proper factor. If $N$ is composite and line L1 finds no factor, then $N = pq$ with primes $N^{1/3} < p \le q$. Dirichlet's approximation theorem gives $u, v \ge 1$ with $v \le B = N^{1/6}\sqrt{q/p}$ and $|u/v - p/q| < 1/(vB)$. Then $k = uv < N^{1/3} + 1$, and $a = uq + vp$, $b = |uq - vp| < N^{1/3}$ satisfy $a^2 - b^2 = 4kN$ with $a \ge 2\sqrt{kN}$, so line L5 finds a square for this $k$ or earlier. So the method returns $N$ only for a prime $N$. The full proof is below.

## Complexity

- **Trial division.** Line L1 makes at most $N^{1/3}$ divisions.
- **The Fermat searches.** For multiplier $k$, the values of $a$ lie in $[\sqrt{4kN}, \sqrt{4kN + N^{2/3}})$, an interval of length at most $N^{2/3} / (2\sqrt{4kN}) = N^{1/6}/(4\sqrt k)$. Summed over $k \le N^{1/3} + 1$, with $\sum_{k \le K} k^{-1/2} \le 2\sqrt K$, this gives at most $\frac{1}{2} N^{1/6} \sqrt{N^{1/3} + 1} + N^{1/3} + 1 = O(N^{1/3})$ square tests.
- **Time.** $O(N^{1/3})$ on the word RAM, worst case, for both the factorization and the primality proof. For an arbitrary-precision $N$, each operation costs $O(n^2)$ bit operations, so the total is $O(N^{1/3} n^2)$.
- **Space.** $O(1)$ numbers.

This is proved, with no heuristic. Faster methods exist: [Pollard's rho](/pollard-rho/) and [SQUFOF](/shanks-squfof/) need about $N^{1/4}$ steps heuristically, and the deterministic [Pollard-Strassen method](/pollard-strassen/) needs $N^{1/4 + o(1)}$ provably, but with large memory.

## Properties

- **Deterministic and proved.** The bound holds for every $N$, and the output is always right.
- **A primality test.** For prime $N$ it runs to the end and returns $N$, a proof of primality in $O(N^{1/3})$ steps.
- **A prime factor.** The result of line L1 is the smallest prime factor. Line L5 is reached only when $N = pq$ with two primes above $N^{1/3}$, so its gcd is $p$ or $q$. So the output is always prime when $N$ is composite.
- **Fast on easy cases.** If $N$ has a small factor, line L1 finds it; if $p/q$ is close to a fraction with small terms, an early $k$ succeeds.

## Variants and improvements

- **Order of the multipliers.** Try first the values of $k$ with many divisors, because each factorization $k = uv$ gives a chance for a close pair $uq, vp$. Crandall and Pomerance mention this speedup and refer to Lehman's paper for the details.
- **Residue filters.** As in [Fermat's method](/fermat-factorization/), tables of the squares modulo small numbers reject most $a$ before any square root.
- **[Hart's one line factoring](/hart-one-line-factorization/).** It tries only $a = \lceil \sqrt{kN} \rceil$ for each $k = 1, 2, \dots$, and asks whether $a^2 \bmod N$ is a square. It is simpler and fast in practice, with a heuristic bound of about $N^{1/3}$.

## When to use it

Use Lehman's method when you need a proved bound and a primality certificate for numbers of moderate size, for example up to $10^{15}$, where $N^{1/3}$ is $10^5$. As a general factoring tool it is outclassed by [Pollard's rho](/pollard-rho/) and [SQUFOF](/shanks-squfof/) for 64-bit numbers, and by the [elliptic curve method](/elliptic-curve-factorization/) and the [quadratic sieve](/quadratic-sieve/) beyond.

## Pitfalls

- **Skipping the trial division.** The proof needs both prime factors above $N^{1/3}$. Without line L1, a number such as $N = 3q$ with a large prime $q$ needs a multiplier near $q/3$, far beyond $N^{1/3}$, and the method would wrongly report $N$ as prime.
- **The upper end of $k$.** The proof gives $k < N^{1/3} + 1$, not $k \le N^{1/3}$; the loop of line L2 includes $\lfloor N^{1/3} \rfloor + 1$ to be safe.
- **Returning $a - b$ instead of a gcd.** For $N = 2581$ and $k = 3$, $a - b = 174 = 2 \cdot 87 = 2 \cdot 3 \cdot 29$, which is not a divisor of $N$. Take $\gcd(a \pm b, N)$.
- **Floating-point bounds.** The bound $2\sqrt{kN} + N^{1/6}/(4\sqrt k)$ computed with doubles can be off by one for large $N$. The integer test $(a^2 - 4kN)^3 < N^2$ of line L4 is exact.
- **Small $N$.** The inequality $a + b < N$ in the proof needs $N > 20.4$. For $N \le 21$ use trial division.

## Implementations

## History

R. Sherman Lehman published the method in 1974. Its proved running time of $O(N^{1/3})$ is below the $N^{1/2}$ of trial division and Fermat's method. In the same year Pollard gave a deterministic $N^{1/4 + o(1)}$ algorithm based on fast polynomial arithmetic, and Strassen gave a similar one, but these need large memory. In 2012 William Hart published his "one line" method, a simplified heuristic form of Lehman's search.

## References
