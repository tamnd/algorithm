---
tag: ZB7C0A
kind: algorithm
slug: continued-fraction-factorization
name: Continued fraction factorization (CFRAC)
aliases:
- CFRAC
- Morrison-Brillhart method
area: number-theory/factorization
level: advanced
summary: Expands sqrt(kN) as a continued fraction, keeps the smooth residues A^2 mod N below 2 sqrt(kN), and combines them mod 2 into a congruence of squares. Heuristically L_N[1/2, 2^(1/2)].
solves: [integer-factorization]
model: word-ram
complexity:
  vars: {N: the integer to factor, n: the number of binary digits of N, k: the multiplier, K: the number of primes in the factor base, I: the step limit}
  time: {worst: O(I K + K^3), heuristic: exp((2^(1/2) + o(1)) (ln N ln ln N)^(1/2))}
  space: {extra: O(K^2)}
  bit_operations: {heuristic: exp((2^(1/2) + o(1)) (ln N ln ln N)^(1/2))}
properties: {deterministic: true, recursive: false}
prereqs: [continued-fraction-convergents, congruence-of-squares, relation-collection, quadratic-residue]
see_also: [shanks-squfof, dixon-random-squares, quadratic-sieve, knuth-schroeppel-multiplier, smooth-number, pell-equation, gaussian-elimination, integer-factorization]
sources:
  - paper: "Michael A. Morrison and John Brillhart, A method of factoring and the factorization of F7, Mathematics of Computation 29(129), 1975"
    locator: pages 183 to 205 (the method, the factor base of primes p with kN a quadratic residue, the multiplier k, and the factorization of the Fermat number F7)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: introduction to Chapter 6, page 261 (CFRAC as the first subexponential factoring algorithm); Exercise 6.4, pages 307 to 308 (the residues of size O(N^(1/2)) and why they cannot be sieved); Section 1.3.2, around page 29 (F7)
  - paper: "D. H. Lehmer and R. E. Powers, On factoring large numbers, Bulletin of the American Mathematical Society 37(10), 1931"
    locator: pages 770 to 776 (the use of the continued fraction of the square root of kN to find small quadratic residues)
  - paper: "Carl Pomerance, Analysis and comparison of some integer factoring algorithms, in Computational Methods in Number Theory, Part I, Mathematical Centre Tracts 154, Mathematisch Centrum, Amsterdam, 1982"
    locator: pages 89 to 139 (the heuristic analysis of the continued fraction method and the early abort strategy)
  - paper: "Carl Pomerance, A tale of two sieves, Notices of the American Mathematical Society 43(12), 1996"
    locator: pages 1473 to 1485 (the history of the continued fraction method and its place before the quadratic sieve)
---

The continued fraction factorization method, CFRAC, of Michael Morrison and John Brillhart was the first factoring algorithm with a subexponential running time, heuristically $L_N[1/2, \sqrt 2]$. It expands $\sqrt{kN}$ as a [continued fraction](/continued-fraction/) for a small multiplier $k$. The [convergents](/continued-fraction-convergents/) $A_{i-1}/B_{i-1}$ satisfy $A_{i-1}^2 \equiv (-1)^i Q_i \pmod N$ with $0 < Q_i < 2\sqrt{kN}$, so each step gives a square congruent to a small number. The steps where $(-1)^i Q_i$ is [smooth](/smooth-number/) are [relations](/relation-collection/), and linear algebra over the field with two elements combines them into a [congruence of squares](/congruence-of-squares/) that splits $N$.

## In plain words

Squares of whole numbers, reduced modulo the number to factor, are usually about as large as the number itself. The continued fraction of the square root of the number gives a stream of special whole numbers whose squares leave very small remainders, below twice the square root.

Small remainders break into small primes far more often than large ones. So compute the stream, and keep each number whose remainder breaks completely into primes from a short list. When there are more kept numbers than primes in the list, some group of them has a product of remainders that is a perfect square. Multiply that group together on both sides: two numbers with the same square appear, and one gcd usually shows a factor.

## The problem

**Input.** An odd integer $N \ge 3$ that is not a prime power, a multiplier $k \ge 1$ such that $kN$ is not a perfect square, a smoothness bound $B$, a count $E \ge 1$ of extra relations, and a step limit $I$.

**Output.** A proper factor $g$ of $N$ (with $1 < g < N$), or $1$ for a failure with these parameters.

**The continued fraction of $\sqrt D$.** Let $D = kN$ and $a = \lfloor \sqrt D \rfloor$. The complete quotients of $\sqrt D$ are $x_i = (P_i + \sqrt D)/Q_i$ for $i \ge 1$, with $P_1 = a$, $Q_0 = 1$, $Q_1 = D - a^2$, and
$$b_i = \lfloor (a + P_i)/Q_i \rfloor, \quad P_{i+1} = b_i Q_i - P_i, \quad Q_{i+1} = Q_{i-1} + b_i(P_i - P_{i+1}).$$
The numerators of the convergents are $A_{-1} = 1$, $A_0 = a$ and $A_i = b_i A_{i-1} + A_{i-2}$. The key identity, proved below, is
$$A_{i-1}^2 - D B_{i-1}^2 = (-1)^i Q_i, \qquad 0 < Q_i < 2\sqrt D,$$
and since $N \mid D$ it gives $A_{i-1}^2 \equiv (-1)^i Q_i \pmod N$. Only $A_i \bmod N$ is needed, so all numbers stay below $N$ or below $2\sqrt D$.

**The factor base.** An odd prime $p$ that divides some $Q_i$ but not $D$ must have $D$ as a [quadratic residue](/quadratic-residue/), since $A_{i-1}^2 \equiv D B_{i-1}^2 \pmod p$ and $\gcd(A_{i-1}, B_{i-1}) = 1$. So the [factor base](/factor-base/) $F$ holds $-1$, $2$, and the odd primes $p \le B$ with $p \mid D$ or [Legendre symbol](/legendre-symbol/) $(D/p) = 1$. Its size $K$ is about half the number of primes up to $B$.

**Cost model.** On the [word RAM](/word-ram/) with $N < 2^w$, a step costs $O(1)$ and the smoothness test by trial division costs $O(K)$. For an arbitrary-precision $N$ with $n$ binary digits, a step costs $O(n^2)$ bit operations and a trial division of a number below $2\sqrt D$ by a prime of the base costs $O(n)$. The time bound $O(IK + K^3)$ counts word operations for word-sized $N$. The subexponential bound is a heuristic.

## The algorithm

$R$ is the list of relations, each a pair of $A_{i-1} \bmod N$ and the exponent vector of $(-1)^i Q_i$ over $F$.

```pseudo id=main
CFRAC(N, k, B, E, I)              ▷ N odd, not a prime power; kN not a square; returns a proper factor or 1
L1  D ← kN, a ← ⌊√D⌋, F ← −1, 2 and the odd primes p ≤ B with p | D or (D/p) = 1
L2  (P, Q', Q) ← (a, 1, D − a²), (A', A) ← (1, a mod N), i ← 1, R ← empty
L3  while |R| < |F| + E and i < I do
L4      if (−1)^i Q factors completely over F then append (A, its exponent vector) to R
L5      b ← ⌊(a + P)/Q⌋, P⁺ ← bQ − P, (Q', Q) ← (Q, Q' + b(P − P⁺)), P ← P⁺, (A', A) ← (A, (bA + A') mod N), i ← i + 1
L6  for each nonempty subset T of R whose exponent vectors add to 0 mod 2, found by Gaussian elimination over GF(2) do
L7      X ← ∏ of the A in T mod N, e ← the sum of the exponent vectors in T, Y ← ∏ over odd p in F of p^(e_p/2) mod N
L8      g ← gcd(X − Y, N); if 1 < g < N then return g
L9  return 1
```

Line L1 builds the factor base. Line L2 starts the expansion at $i = 1$ with $A = A_0$. In the loop, line L4 tests the value $(-1)^i Q_i$ with $A = A_{i-1}$, and line L5 steps to $i + 1$. The loop stops when there are $|F| + E$ relations, which ensures at least $E$ dependencies, or after $I$ steps. Line L6 runs Gaussian elimination on the exponent vectors mod 2 with a record of which rows were added; each row that reduces to zero gives a subset $T$. Lines L7 and L8 turn a subset into $X^2 \equiv Y^2 \pmod N$ and try the gcd. The sign entry $e_{-1}$ is even in every subset, so it does not enter $Y$.

## Example

Let $N = 9073 = 43 \cdot 211$, $k = 1$, $B = 20$ and $E = 2$. Then $a = 95$, and $9073$ is a quadratic residue modulo $3, 7, 11, 13$ but not modulo $5, 17, 19$, so $F = \{-1, 2, 3, 7, 11, 13\}$ and $|F| = 6$. The expansion:

| $i$ | $P_i$ | $Q_i$ | $b_i$ | $A_{i-1} \bmod N$ | $(-1)^i Q_i$ | smooth? |
|---|---|---|---|---|---|---|
| 1 | 95 | 48 | 3 | 95 | $-48 = -2^4 \cdot 3$ | yes |
| 2 | 49 | 139 | 1 | 286 | $139$ | no |
| 3 | 90 | 7 | 26 | 381 | $-7$ | yes |
| 4 | 92 | 87 | 2 | 1119 | $87 = 3 \cdot 29$ | no |
| 5 | 82 | 27 | 6 | 2619 | $-27 = -3^3$ | yes |
| 6 | 80 | 99 | 1 | 7760 | $99 = 3^2 \cdot 11$ | yes |
| 7 | 19 | 88 | 1 | 1306 | $-88 = -2^3 \cdot 11$ | yes |
| 8 | 69 | 49 | 3 | 9066 | $49 = 7^2$ | yes |
| 9 | 78 | 61 | 2 | 1285 | $-61$ | no |
| 10 | 44 | 117 | 1 | 2563 | $117 = 3^2 \cdot 13$ | yes |
| 11 | 73 | 32 | 5 | 3848 | $-32 = -2^5$ | yes |

For instance $95^2 - 9073 = 9025 - 9073 = -48$. The loop stops after step 11 with $8 = |F| + E$ relations. Over $(-1, 2, 3, 7, 11, 13)$ the vectors mod 2 of steps 1 and 5 are both $(1, 0, 1, 0, 0, 0)$, so the elimination finds $T = \{1, 5\}$ first: $(-48)(-27) = 1296 = 36^2$. Then $X = 95 \cdot 2619 \bmod 9073 = 3834$, $Y = 2^2 \cdot 3^2 = 36$, and $\gcd(3834 - 36, 9073) = \gcd(3798, 9073) = 211$. So $9073 = 43 \cdot 211$.

**Dependencies that fail.** Step 8 alone is a dependency, since $49 = 7^2$. But $A_7 = 9066 \equiv -7$, so $X \equiv -Y$ and $\gcd(X - Y, N) = \gcd(-14, 9073) = 1$. The set $\{6, 7, 11\}$ gives $99 \cdot (-88) \cdot (-32) = 528^2$ and $X = 7760 \cdot 1306 \cdot 3848 \bmod 9073 = 528 = Y$, so the gcd is $N$. Each dependency is a fresh try, and for $N$ with two prime factors about half of them succeed.

## Correctness

Each complete quotient $x_i = (P_i + \sqrt D)/Q_i$ is reduced, that is $x_i > 1$ and $-1 < \bar x_i < 0$; this gives $Q_i > 0$, $Q_i < 2\sqrt D$, and $b_i = \lfloor x_i \rfloor$, so the recurrence of line L5 really computes the continued fraction of $\sqrt D$. The convergents then satisfy $\sqrt D = (A_{i-1} x_i + A_{i-2})/(B_{i-1} x_i + B_{i-2})$, and comparing this with $x_i = (P_i + \sqrt D)/Q_i$ gives $A_{i-1}^2 - DB_{i-1}^2 = (-1)^i Q_i$. Reduced modulo $N$, each relation is $A_{i-1}^2 \equiv (-1)^i Q_i \pmod N$. For a subset $T$ whose vectors add to $0$ mod 2, the product of the right sides is $\prod_{p \in F} p^{e_p}$ with all $e_p$ even, which is $Y^2$, while the product of the left sides is $X^2$. So $X^2 \equiv Y^2 \pmod N$, and $g = \gcd(X - Y, N)$ divides $N$. Line L8 returns $g$ only if $1 < g < N$, and the loops are bounded by $I$ and by $|R|$. So the output is a proper factor or $1$, and the algorithm stops. The full proof is below.

Why a dependency succeeds is a heuristic. If $N$ has $r \ge 2$ distinct prime factors and $X$ behaves like a random square root of $Y^2$ modulo $N$, then $X \equiv \pm Y$ holds with probability $2^{1-r}$, so a dependency splits $N$ with probability at least $1/2$. With $E$ dependencies, all fail with probability about $2^{-E}$.

## Complexity

- **Per step.** One division and a few multiplications of numbers below $2\sqrt D$, one multiplication modulo $N$, and a trial division by the $K$ primes of the base. The trial division dominates: $O(K)$ word operations per step for word-sized $N$.
- **With the limit $I$.** At most $I$ steps, so $O(IK)$ for the expansion, and $O(K^3)$ word operations for Gaussian elimination on a $(K + E) \times K$ matrix over GF(2), or $O(K^3/w)$ with rows packed in words. This is the proved bound for given parameters, and it says nothing about success.
- **Heuristic bound.** Treat the $Q_i$ as random numbers of size about $\sqrt N$. By the theory of [smooth numbers](/smooth-number/), a number of that size is $B$-smooth with probability about $u^{-u}$ for $u = \ln \sqrt N / \ln B$. Balancing the number of steps, about $K u^u$, against the cost per step and the matrix gives the best bound $B = L_N[1/2, 1/(2\sqrt 2)]$ and a total time of $L_N[1/2, \sqrt 2] = \exp((\sqrt 2 + o(1))\sqrt{\ln N \ln \ln N})$ with trial division (Pomerance 1982). This is a heuristic: the $Q_i$ are not proved to be smooth as often as random numbers of their size, and no proved subexponential bound for CFRAC is known.
- **Space.** $O(K^2)$ for the matrix, and $O(K)$ numbers modulo $N$ for the relations.

## Properties

- **Small residues.** The values $Q_i$ are below $2\sqrt{kN}$, smaller than the residues $x^2 - N$ of the [quadratic sieve](/quadratic-sieve/), which are about $2M\sqrt N$ for a sieve interval of length $2M$. This is the one point where CFRAC is better.
- **No sieve.** The $Q_i$ follow no polynomial in $i$, so a prime $p$ does not divide them at regular steps, and each $Q_i$ must be tested by trial division. This is why the quadratic sieve replaced CFRAC.
- **Deterministic.** For fixed parameters the output is fixed. A failure leads to more relations or another multiplier.
- **Independent of the size of the factors.** The run time depends on $N$, not on its smallest prime factor. Remove small factors first with [trial division](/trial-division/) or the [elliptic curve method](/elliptic-curve-factorization/).
- **Period.** The expansion of $\sqrt D$ is periodic. For small $N$ the period can be short and end before enough relations are found, and then a new multiplier is needed.

## Variants and improvements

- **The multiplier.** Morrison and Brillhart expanded $\sqrt{kN}$ for a small $k$ chosen so that many small primes have $kN$ as a quadratic residue, which makes more $Q_i$ smooth. The [Knuth-Schroeppel multiplier](/knuth-schroeppel-multiplier/) is a rule for this choice.
- **The large prime variation.** A $Q_i$ that is smooth except for one prime below $B^2$ is kept. Two such values with the same large prime multiply to a relation (Morrison and Brillhart). See [relation collection](/relation-collection/).
- **Early abort.** Trial divide by the small primes of the base first, and drop the $Q_i$ whose remaining cofactor is still large. Pomerance showed that this lowers the constant $\sqrt 2$ of the heuristic bound.
- **Faster smoothness tests.** Pollard's rho or [ECM](/elliptic-curve-factorization/) on the cofactors, or [batch gcd](/batch-gcd/) over many $Q_i$ at once, replace part of the trial division.
- **SQUFOF.** [Shanks' square forms factorization](/shanks-squfof/) uses the same expansion but waits for a single $Q_i$ at an even step that is a perfect square, and then needs no factor base and no linear algebra.

## When to use it

CFRAC is now mostly of historical and teaching value: it shows the whole plan of relations and linear algebra with very small residues. For all but small $N$, the [quadratic sieve](/quadratic-sieve/) and its [multiple polynomial](/multiple-polynomial-quadratic-sieve/) form are faster, because sieving replaces trial division. For $N$ above about 100 digits, use the [number field sieve](/general-number-field-sieve/). For small factors, use [Pollard's rho](/pollard-rho/) or [ECM](/elliptic-curve-factorization/) first.

## Pitfalls

- **The sign.** The residue at step $i$ is $(-1)^i Q_i$, not $Q_i$. Keep $-1$ in the factor base; a wrong sign gives $X^2 \equiv -Y^2$ and only trivial gcds.
- **Off by one.** The relation at step $i$ pairs $Q_i$ with $A_{i-1}$. Test $Q$ before the update of line L5, while $A$ still holds $A_{i-1}$.
- **Large numerators.** The $A_i$ grow without bound. Reduce them modulo $N$ at each step, since only $A_i \bmod N$ is used.
- **Squares and prime powers.** If $kN$ is a square, $Q_1 = 0$. If $N = p^j$, every square root of $Y^2$ that is a unit is $\pm Y$ modulo $p^j$ for odd $p$, so all gcds are trivial. Test for perfect powers first.
- **The wrong factor base.** An odd prime $p \nmid D$ with $(D/p) = -1$ never divides any $Q_i$; including it only slows the trial division.
- **Too few relations.** With exactly $|F|$ relations there may be no dependency. Collect $E \ge 10$ extra so that several dependencies give several tries.

## Implementations

## History

Derrick Lehmer and Ralph Powers proposed in 1931 to factor $N$ with the continued fraction of $\sqrt{kN}$ and combinations of the small residues $Q_i$, but the method was hard to carry out by hand. Michael Morrison and John Brillhart made it systematic in the early 1970s with a factor base and Gaussian elimination mod 2, and used it to factor the Fermat number $F_7 = 2^{128} + 1$, which has 39 digits. They published the method and the factorization in 1975. It was the first subexponential factoring algorithm and raised the limit of complete factorization from about 20 to about 50 digits (Crandall and Pomerance). Carl Pomerance analyzed it in 1982 in the paper that introduced the [quadratic sieve](/quadratic-sieve/), which soon replaced it.

## References
