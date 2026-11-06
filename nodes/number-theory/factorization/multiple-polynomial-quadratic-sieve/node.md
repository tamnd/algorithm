---
tag: CEZR0P
kind: algorithm
slug: multiple-polynomial-quadratic-sieve
name: Multiple-polynomial quadratic sieve
aliases:
- MPQS
area: number-theory/factorization
level: advanced
summary: The quadratic sieve with many polynomials (ax + b)^2 - N, each sieved over a short interval, so that the values stay near M N^(1/2) instead of growing. Heuristically L_N[1/2, 1].
solves: [integer-factorization]
model: word-ram
complexity:
  vars: {N: the integer to factor, n: the number of binary digits of N, B: the smoothness bound, K: the size of the factor base, M: half the length of the sieve interval, P: the number of polynomials}
  time: {worst: O(P (M K + K n^2) + K^3), heuristic: exp((1 + o(1)) (ln N ln ln N)^(1/2))}
  space: {extra: O(K^2 + M)}
  sieve_operations: {heuristic: O(P M log log B)}
properties: {deterministic: true, recursive: false}
prereqs: [quadratic-sieve, hensel-lifting, tonelli-shanks]
see_also: [quadratic-sieve, relation-collection, continued-fraction-factorization, general-number-field-sieve, knuth-schroeppel-multiplier, block-lanczos-algorithm, smooth-number, integer-factorization]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 6.1.5, Multiple polynomials, pages 273 to 274 (Montgomery's polynomials, a about (2n)^(1/2)/M, the bound (M/2^(1/2)) n^(1/2) on the values, a = p^2, and the speedup); Section 6.1.6, Self initialization, pages 274 to 276
  - paper: "Robert D. Silverman, The multiple polynomial quadratic sieve, Mathematics of Computation 48(177), 1987"
    locator: pages 329 to 339 (an implementation with Montgomery's polynomials and the choice of parameters)
  - paper: "Carl Pomerance, The quadratic sieve factoring algorithm, Advances in Cryptology, EUROCRYPT '84, Lecture Notes in Computer Science 209, 1985"
    locator: pages 169 to 182 (the multiple polynomial versions of Davis and Holdridge and of Montgomery)
---

The multiple polynomial quadratic sieve, MPQS, is the form of the [quadratic sieve](/quadratic-sieve/) used in practice. Instead of the one polynomial $x^2 - N$, whose values grow steadily as $x$ moves away from $\sqrt N$, it sieves many polynomials $f(x) = ax^2 + 2bx + c$ with $b^2 - ac = N$, each over a short interval $[-M, M]$. Since $af(x) = (ax + b)^2 - N$, each smooth value of $f$ gives a [relation](/relation-collection/), and with $a \approx \sqrt{2N}/M$ all values stay below about $M\sqrt{N/2}$. Peter Montgomery's choice $a = q^2$ for a prime $q$ makes the relation $\big((ax + b)/q\big)^2 \equiv f(x) \pmod N$ as simple as in the basic sieve. The heuristic running time is still $L_N[1/2, 1]$, but the values are smaller by a factor of about $B$, which makes the method much faster in practice.

## In plain words

The basic quadratic sieve looks at numbers that start small but grow as it moves on, so it finds fewer and fewer useful ones. The fix is to stop early and start again with a fresh formula whose numbers are small again.

Each formula comes from a prime chosen near a fixed size. Its numbers, multiplied by the square of that prime, are again squares minus the number to factor, so they serve just as well. All formulas use the same list of small primes, so their results all go into one table.

Sieve each formula over a short stretch, keep the results that break into small primes, then move on to the next prime and the next formula. When the table has more rows than primes, combine the rows as before to get two numbers with the same square, and take one gcd.

## The problem

**Input.** An odd integer $N \ge 3$ that is not a perfect square, a smoothness bound $B$, a half length $M$ of the sieve interval, a count $E \ge 1$ of extra relations, and a limit $P$ on the number of polynomials.

**Output.** A proper factor $g$ of $N$ (with $1 < g < N$), or $1$ for a failure with these parameters. A prime $N$ always gives $1$.

**Montgomery's polynomials.** Let $q$ be an odd prime with $q \nmid N$ and [Legendre symbol](/legendre-symbol/) $(N/q) = 1$, and let $a = q^2$. A square root $b_0$ of $N$ modulo $q$ lifts by [Hensel lifting](/hensel-lifting/) to $b$ with $b^2 \equiv N \pmod{q^2}$; replace $b$ by $a - b$ if needed so that $0 < b \le a/2$. Then $c = (b^2 - N)/a$ is an integer, and
$$a f(x) = a^2x^2 + 2abx + ac = (ax + b)^2 - N, \qquad \text{so} \qquad \big((ax + b) q^{-1}\big)^2 \equiv f(x) \pmod N.$$
On $[-M, M]$ the values satisfy $f(0) \approx -N/a$ and $f(\pm M) \approx (a^2M^2 - N)/a$. Making these equal in size gives $a \approx \sqrt{2N}/M$, so $q \approx (2N)^{1/4}/M^{1/2}$, and then $|f(x)| \lesssim M\sqrt{N/2}$ on the whole interval (Crandall and Pomerance).

**The factor base.** As in the basic sieve, $F$ is $-1$, $2$, and the odd primes $p \le B$ with $(N/p) = 1$, with $t_p^2 \equiv N \pmod p$. For $p \in F$ odd and $p \ne q$, $p \mid f(x)$ exactly when $ax + b \equiv \pm t_p \pmod p$, that is, $x \equiv (\pm t_p - b)a^{-1} \pmod p$. Since $a$ is odd, $f(x) \equiv x + c \pmod 2$. The factor base does not depend on the polynomial, so all relations go into one matrix. Choosing $q > B$ keeps $q$ out of $F$.

**Cost model.** On the [word RAM](/word-ram/) with $N < 2^w$, a sieve step costs $O(1)$. For an arbitrary-precision $N$ with $n$ binary digits, sieve steps are still word operations, and the setup of a polynomial (a Hensel lift, an inverse of $q$ modulo $N$, and the inverses $a^{-1} \bmod p$) costs $O(K n^2)$ bit operations or less. The worst-case bound is for fixed parameters; the subexponential bound is a heuristic.

## The algorithm

$R$ is the list of relations, each a pair of $(ax + b)q^{-1} \bmod N$ and the exponent vector of $f(x)$ over $F$.

```pseudo id=main
MPQS(N, B, M, E, P)              ▷ N odd, not a square; returns a proper factor of N or 1
L1  F ← −1, 2 and the odd p ≤ B with (N/p) = 1, with t_p² ≡ N (mod p); q ← max(B, ⌊((2N)^(1/2)/M)^(1/2)⌋), R ← empty
L2  while |R| < |F| + E and fewer than P polynomials were used do
L3      q ← the next prime above q with (N/q) = 1; a ← q², b ← a root of b² ≡ N (mod a) with 0 < b ≤ a/2, c ← (b² − N)/a
L4      root classes: x ≡ c (mod 2) for p = 2, and x ≡ (±t_p − b)a⁻¹ (mod p) for each odd p in F
L5      S[x] ← 0 for x in [−M, M); for each p and each root class, add log p to S[x] at every x of the class
L6      for each x with S[x] ≥ log |f(x)| − τ: if f(x) = ax² + 2bx + c factors over F then append ((ax + b)q⁻¹ mod N, its exponent vector) to R
L7  for each nonempty subset T of R whose exponent vectors add to 0 mod 2 do: X ← ∏ of the first entries, Y ← ∏ over p > 0 in F of p^(e_p/2), g ← gcd(X − Y, N); if 1 < g < N then return g
L8  return 1
```

Line L1 sets up the factor base once, and the first $q$ near the optimal size $(2N)^{1/4}/M^{1/2}$, but above $B$. Line L3 makes a new polynomial from the next suitable prime. Line L4 computes where each prime of the base divides $f$; this is the initialization, and it is the only work that depends on the polynomial. Lines L5 and L6 sieve $[-M, M)$ and confirm the candidates by trial division, exactly as in the basic sieve. A relation stores $(ax + b)q^{-1} \bmod N$, whose square is $f(x)$ modulo $N$. Line L7 is the same linear algebra as in the basic sieve, with $e$ the sum of the exponent vectors of $T$.

## Example

Let $N = 1000019999371 = 999983 \cdot 1000037$, $B = 50$, $M = 100$ and $E = 2$. The factor base is $F = \{-1, 2, 3, 5, 7, 13, 19, 29, 31, 37, 41, 43\}$, with $12$ entries, so $14$ relations are needed. The target size of $q$ is $\lfloor (\lfloor \sqrt{2N} \rfloor / 100)^{1/2} \rfloor = \lfloor 14142^{1/2} \rfloor = 118$, and the primes $q > 118$ with $(N/q) = 1$ are $127, 131, 149, 151, 157, 163, 181, 199, 227, \dots$ The first polynomial is $q = 127$, $a = 16129$, $b = 5508$, $c = -61999483$, and indeed $b^2 - ac = N$.

The nine polynomials from $q = 127$ to $q = 227$ give $1, 1, 0, 2, 3, 2, 0, 3, 2$ smooth values, $14$ in all. For $q = 127$ the values are below $9.9 \cdot 10^7$ in absolute value, close to the bound $M\sqrt{N/2} \approx 7.1 \cdot 10^7$. As $q$ moves above the best size $118$, $a$ grows and so do the values at the ends of the interval, up to $5.0 \cdot 10^8$ for $q = 227$. The basic sieve with one polynomial, over the same number $1800$ of values around $\sqrt N$, reaches $1.8 \cdot 10^9$. The elimination finds, among others, this dependency of four relations from four different polynomials:

| $q$ | $x$ | $ax + b$ | $f(x)$ |
|---|---|---|---|
| 151 | $-87$ | $-1981511$ | $2 \cdot 3 \cdot 5^6 \cdot 37^2$ |
| 157 | $-54$ | $-1328879$ | $2 \cdot 3^2 \cdot 5 \cdot 7 \cdot 31 \cdot 37 \cdot 43$ |
| 163 | $-19$ | $-501029$ | $-2 \cdot 3 \cdot 5 \cdot 13 \cdot 41^2 \cdot 43$ |
| 227 | $-7$ | $-358765$ | $-2 \cdot 3^4 \cdot 7 \cdot 13 \cdot 31 \cdot 37$ |

For the first row, $a = 22801$, $b = 2176$, and $(22801 \cdot (-87) + 2176)^2 - N = 22801 \cdot 128343750$. The product of the four values is $2^4 \cdot 3^8 \cdot 5^8 \cdot 7^2 \cdot 13^2 \cdot 31^2 \cdot 37^4 \cdot 41^2 \cdot 43^2$, a square. So $Y = 2^2 \cdot 3^4 \cdot 5^4 \cdot 7 \cdot 13 \cdot 31 \cdot 37^2 \cdot 41 \cdot 43 \bmod N = 717198484262$, and $X = \prod (ax + b) q^{-1} \bmod N = 48625850190$. Then $\gcd(X - Y, N) = 999983$, and $N = 999983 \cdot 1000037$.

## Correctness

The polynomial identity $af(x) = (ax + b)^2 - N$ follows from $b^2 - ac = N$, and $b^2 \equiv N \pmod{q^2}$ holds by the Hensel step, so $c$ is an integer. Since $(N/q) = 1$, $q \nmid N$ and $q$ is invertible modulo $N$, so each relation satisfies $\big((ax + b)q^{-1}\big)^2 \equiv a f(x) q^{-2} = f(x) \pmod N$. For an odd $p \in F$, $p \nmid a$, and $p \mid f(x)$ if and only if $(ax + b)^2 \equiv N \equiv t_p^2 \pmod p$, so the sieve hits exactly the $x$ where $p$ divides $f(x)$; for $p = 2$ the class $x \equiv c$ is exact as $a$ is odd. Line L6 confirms every relation by trial division. For a subset whose vectors add to $0$ mod 2, the product of the values is $Y^2$, so $X^2 \equiv Y^2 \pmod N$, and line L7 returns only a proper factor. The loops are bounded by $P$ polynomials of $2M$ values. The full proof is below.

Why a dependency splits $N$ is the same heuristic as for the basic sieve: with $N$ having two or more distinct prime factors, about half of the dependencies should succeed.

## Complexity

- **Per polynomial.** The initialization of line L4 costs $O(K)$ modular inverses and multiplications modulo small primes, plus a Hensel lift and one inverse modulo $N$. The sieve costs $O(M \ln \ln B + K)$ additions, and each candidate $O(K)$ divisions.
- **Proved bound for fixed parameters.** At most $P$ polynomials of $2M$ values, so $O(P(MK + Kn^2) + K^3)$ word operations even if every value is a candidate, with $O(K^3)$ for Gaussian elimination.
- **Heuristic bound.** The values are about $M\sqrt N$ instead of the $2M'\sqrt N$ of the basic sieve, where the basic sieve needs a total interval of $M' \approx B^2 = L_N[1/2, 1]$ but MPQS can take $M \approx B = L_N[1/2, 1/2]$ per polynomial. The total time is still $L_N[1/2, 1] = \exp((1 + o(1))\sqrt{\ln N \ln \ln N})$, heuristically, but the gain is a factor of roughly $\frac12\sqrt{\ln N \ln \ln N}$, about $17$ for $N$ of $100$ digits (Crandall and Pomerance, who note that this estimate has not been checked by experiment).
- **Space.** $O(M)$ for the sieve array, $O(K)$ for the roots and inverses, and $O(K^2)$ bits for the matrix.

## Properties

- **Values that do not grow.** Every polynomial has values below about $M\sqrt{N/2}$ on its interval, so the yield of smooth values stays the same throughout the run.
- **One factor base.** All polynomials use the same primes, the odd $p$ with $(N/p) = 1$, so the matrix does not grow with the number of polynomials.
- **Parallel.** Different polynomials are independent, so separate machines can sieve different ranges of $q$ and send their relations to one place. Large factorizations with MPQS were run this way over networks of workstations.
- **Deterministic.** For fixed parameters the output is fixed.
- **Independent of the size of the factors.** As for the basic sieve, small factors give no advantage; remove them first.

## Variants and improvements

- **Self initialization (SIQS).** Take $a$ as a product $q_1 \cdots q_k$ of $k$ primes with $(N/q_i) = 1$. Then $b^2 \equiv N \pmod a$ has $2^{k-1}$ essentially different solutions $B_1 \pm B_2 \pm \dots \pm B_k$, by the Chinese remainder theorem, and stepping through them in a Gray code order makes the next set of root classes cheap to compute. This about halves the time of MPQS (Crandall and Pomerance, Section 6.1.6, citing Contini).
- **Large primes.** Keep values that are smooth except for one or two primes a little above $B$, and match them in cycles; see [relation collection](/relation-collection/).
- **A multiplier.** Factor $kN$ for a small $k$ chosen by the [Knuth-Schroeppel](/knuth-schroeppel-multiplier/) rule.
- **Other polynomial families.** James Davis and Diane Holdridge proposed a different way to use many polynomials, independently of Montgomery; Montgomery's is slightly better and is the one used now (Crandall and Pomerance).

## When to use it

MPQS, usually in its self initializing form, is the standard method for general $N$ of moderate size, up to around 100 decimal digits, with no small factors and no special form. It is simpler to program and has a smaller matrix than the [general number field sieve](/general-number-field-sieve/), which is faster for larger $N$. Remove small factors first with [trial division](/trial-division/), [Pollard's rho](/pollard-rho/) or [ECM](/elliptic-curve-factorization/). For $N$ below about $2^{64}$, [SQUFOF](/shanks-squfof/) or rho is simpler.

## Pitfalls

- **A prime $q$ in the factor base.** If $q \le B$, then $q \in F$ and $q \mid a$, so the two root classes of $q$ collapse to one and the formula with $a^{-1} \bmod q$ fails. Take $q > B$.
- **A wrong root modulo $q^2$.** The square root modulo $q$ must be lifted to a root modulo $q^2$; otherwise $c = (b^2 - N)/a$ is not an integer.
- **Forgetting $q^{-1}$.** The relation is $\big((ax + b)q^{-1}\big)^2 \equiv f(x)$. Storing $ax + b$ with $f(x)$ gives a congruence that is off by the square $q^2$, and products of such relations no longer give $X^2 \equiv Y^2$ with the computed $Y$.
- **Duplicate relations.** Two polynomials can produce the same square modulo $N$. Two equal relations form a dependency with $X \equiv \pm Y$, a wasted try. Keep one of each value $\pm(ax + b)q^{-1} \bmod N$.
- **The interval.** If $M$ is much smaller than $B$, the cost of initialization per polynomial dominates. If $M$ is much larger, the values at the ends grow and the advantage is lost.

## Implementations

## History

The basic quadratic sieve of Carl Pomerance (1982) loses speed because its values grow along the interval. In the early 1980s James Davis and Diane Holdridge, and independently Peter Montgomery, proposed sieving many polynomials instead; Pomerance described these versions in 1985, and Robert Silverman published an implementation of Montgomery's version in 1987. Self initialization was sketched by Pomerance, Smith and Tuler in 1988 and described in full by Red Alford and Pomerance and by René Peralta in the 1990s (Crandall and Pomerance). MPQS with the double large prime variation of Arjen Lenstra and Mark Manasse factored the 129-digit RSA challenge number in 1994.

## References
