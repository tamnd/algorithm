---
tag: QBJ183
kind: algorithm
slug: shanks-squfof
name: Shanks' square forms factorization
aliases:
- SQUFOF
area: number-theory/factorization
level: advanced
summary: Walks the continued fraction of sqrt(kN) until a denominator at an even step is a square, then walks a second cycle to a symmetric point that shows a factor. Heuristically O(N^(1/4)) steps.
solves: [integer-factorization]
model: word-ram
complexity:
  vars: {N: the integer to factor, n: the number of binary digits of N, k: the multiplier}
  time: {heuristic: O(N^(1/4))}
  space: {extra: O(1)}
  bit_operations: {heuristic: O(N^(1/4) n^2)}
properties: {deterministic: true, recursive: false}
prereqs: [continued-fraction, fermat-factorization, congruence-of-squares, integer-square-root]
see_also: [continued-fraction-factorization, lehman-factorization, pollard-rho, brent-pollard-rho, hart-one-line-factorization, ideal-class-group, pell-equation, integer-factorization]
sources:
  - paper: doi:10.1090/S0025-5718-07-02010-8
    title: Jason E. Gower and Samuel S. Wagstaff, Jr., Square form factorization, Mathematics of Computation 77(261) (2008)
    locator: pages 551 to 588 (the algorithm in terms of continued fractions and of binary quadratic forms, the multipliers, the heuristic analysis of the running time, and the history)
  - book: isbn:9781470410483
    title: Samuel S. Wagstaff, Jr., The Joy of Factoring, American Mathematical Society, 2013
    locator: the section on SQUFOF, about pages 163 to 168
  - paper: doi:10.1112/S1461157013000065
    title: "Franz Lemmermeyer, Václav Šimerka: quadratic forms and factorization, LMS Journal of Computation and Mathematics 16 (2013)"
    locator: pages 118 to 129 (Šimerka's 1858 factorization with a similar method)
---

Shanks' square forms factorization, SQUFOF, factors an odd integer $N$ in a heuristic $O(N^{1/4})$ steps, and every number it touches is below $2\sqrt{kN}$, so for $N < 2^{62}$ it runs in single-word arithmetic. It walks the [continued fraction](/continued-fraction/) of $\sqrt{kN}$ for a small multiplier $k$ and watches the denominators $Q_i$. When some $Q_i$ at an even step is a perfect square $r^2$, a second walk, started from $r$, reaches a point where two successive numerators are equal, and then the denominator there, or $\gcd(N, P)$, is usually a proper factor. In the language of binary quadratic forms, the first walk finds a square form in the principal cycle, and the second walk reaches an ambiguous form in the cycle of its square root.

## In plain words

Expand the square root of the number as a continued fraction. Each step gives a small whole number $Q$ below twice that square root, and each $Q$ at an even step is a remainder of a square modulo the number. Walk forward until one of these $Q$ is itself a perfect square.

A square remainder alone often gives only a trivial result. So instead, start a second walk of the same kind from the square root of that $Q$. This walk is designed to come to a point where it turns back on itself: two numbers in a row are equal. There the symmetry shows a factor of the number, found with one gcd.

If a square leads nowhere, walk on to the next square. If nothing works within the step limit, multiply the number by a small factor and start again.

## The problem

**Input.** An odd integer $N \ge 3$ that is not a perfect square, a squarefree multiplier $k \ge 1$ such that $kN$ is not a perfect square, and a step limit $I$.

**Output.** A proper factor $g$ of $N$ (with $1 < g < N$), or $1$ for a failure with this $k$ and $I$. A prime $N$ always gives $1$.

**The continued fraction of $\sqrt D$.** For $D = kN$ and $a = \lfloor \sqrt D \rfloor$, the complete quotients of $\sqrt D$ have the form $x_i = (P_i + \sqrt D)/Q_i$ with integers $P_i, Q_i$, starting with $P_1 = a$, $Q_0 = 1$, $Q_1 = D - a^2$, and
$$b_i = \lfloor (a + P_i)/Q_i \rfloor, \quad P_{i+1} = b_i Q_i - P_i, \quad Q_{i+1} = Q_{i-1} + b_i(P_i - P_{i+1}).$$
They satisfy $P_{i+1}^2 + Q_i Q_{i+1} = D$, and $0 < P_i < \sqrt D$, $0 < Q_i < 2\sqrt D$ for $i \ge 1$ (proved below). The convergents $A_i/B_i$ of $\sqrt D$ satisfy $A_{i-1}^2 - D B_{i-1}^2 = (-1)^i Q_i$, so at even $i$, $Q_i \equiv A_{i-1}^2 \pmod N$ is a quadratic residue; this is the link with [CFRAC](/continued-fraction-factorization/). SQUFOF never computes the large numbers $A_i$.

**Cost model.** On the [word RAM](/word-ram/) with $kN < 2^w$, each step is one division and a few multiplications of numbers below $2\sqrt{kN}$, and the perfect-square test is an [integer square root](/integer-square-root/); all cost $O(1)$. For an arbitrary-precision $N$ with $n$ binary digits, a step costs $O(n^2)$ bit operations.

## The algorithm

$P, Q$ and $Q'$ hold $P_i$, $Q_i$ and $Q_{i-1}$. The second walk uses $R, S, S'$ in the same way.

```pseudo id=main
SQUFOF(N, k, I)                     ▷ N odd, not a square; kN not a square; returns a proper factor or 1
L1  D ← kN, a ← ⌊√D⌋
L2  (P, Q', Q) ← (a, 1, D − a²), i ← 1
L3  while i < I do: b ← ⌊(a + P)/Q⌋, P⁺ ← bQ − P, (Q', Q) ← (Q, Q' + b(P − P⁺)), P ← P⁺, i ← i + 1
L4      if i is odd or Q is not a perfect square then go to the next pass of L3
L5      r ← √Q, b ← ⌊(a − P)/r⌋, R ← br + P, (S', S) ← (r, (D − R²)/r)
L6      repeat at most I times
L7          b ← ⌊(a + R)/S⌋, R⁺ ← bS − R
L8          if R⁺ = R then leave the repeat, else (S', S) ← (S, S' + b(R − R⁺)), R ← R⁺
L9      if the repeat ended at line L8 then g ← gcd(N, R) else go to the next pass of L3
L10     if 1 < g < N then return g
L11 return 1
```

Lines L3 and L4 are the forward walk. Line L5 starts the second walk with $S' = r$ and with the largest $R \le a$ that is congruent to $P$ modulo $r$; this is the reduced form of the square root of the square form, reversed. Lines L6 to L8 step this walk with the same rule until two successive numerators are equal. At that point $S$ divides $2R$, and line L9 takes the gcd. If the gcd is trivial, the forward walk goes on from where it was and looks for the next square.

## Example

Let $N = 11111$ and $k = 1$, so $D = 11111$ and $a = 105$. The forward walk:

| $i$ | $b$ | $P_i$ | $Q_i$ | even and square? |
|---|---|---|---|---|
| 1 | | 105 | 86 | |
| 2 | 2 | 67 | 77 | no |
| 3 | 2 | 87 | 46 | |
| 4 | 4 | 97 | 37 | no |
| 5 | 5 | 88 | 91 | |
| 6 | 2 | 94 | 25 | yes, $r = 5$ |

For example $b = \lfloor (105 + 105)/86 \rfloor = 2$, $P_2 = 2 \cdot 86 - 105 = 67$ and $Q_2 = 1 + 2(105 - 67) = 77$; and $67^2 + 86 \cdot 77 = 4489 + 6622 = 11111$.

Line L5: $b = \lfloor (105 - 94)/5 \rfloor = 2$, $R = 2 \cdot 5 + 94 = 104$, $S' = 5$ and $S = (11111 - 104^2)/5 = 295/5 = 59$. The second walk:

| step | $b$ | $R$ | $S$ |
|---|---|---|---|
| start | 2 | 104 | 59 |
| 1 | 3 | 73 | 98 |
| 2 | 1 | 25 | 107 |
| 3 | 1 | 82 | 41 |
| 4 | 4 | 82 | stop |

At step 4, $R^+ = 4 \cdot 41 - 82 = 82 = R$. Here $S = 41$ divides $2R = 164$, and $\gcd(11111, 82) = 41$. So $11111 = 41 \cdot 271$.

**A square that fails.** For $N = 13231 = 101 \cdot 131$, the forward walk gives $Q_4 = 9$. Line L5 gives $R = 115 = a$ and $S = 2$, and the second walk stops at once with $R = 115$ and $\gcd(13231, 115) = 1$. The walk goes on, $Q_6 = 25$ gives a second walk that ends at $R = 101$, $S = 101$, and $\gcd(13231, 101) = 101$.

## Correctness

For $i \ge 1$ the complete quotient $x_i = (P_i + \sqrt D)/Q_i$ is reduced: $x_i > 1$ and $-1 < \bar x_i < 0$, where the bar replaces $\sqrt D$ by $-\sqrt D$. This follows by induction from $x_{i+1} = 1/(x_i - b_i)$ with $b_i = \lfloor x_i \rfloor$, and it gives $Q_i > 0$, $0 < P_i < \sqrt D$ and $Q_i < 2\sqrt D$; so every division is by a positive number and every value is small. The identity $P_{i+1}^2 + Q_i Q_{i+1} = D$ makes $Q_{i+1}$ an integer, and at the square $Q_i = r^2$ it shows that $r$ divides $D - R^2$, so the start of the second walk is integral and again reduced. When the second walk stops, $R^+ = R$ gives $2R = bS$, and $S S' = D - R^2$; so $S \mid 2R$ and $S \mid D - R^2$, and the odd part of $S$ divides $D = kN$. Line L10 returns $g$ only if $1 < g < N$, and $g = \gcd(N, R)$ divides $N$; both loops are bounded by $I$. So the output is always a proper factor or $1$, and the algorithm stops. The full proof is below.

Why the gcd is so often proper is the theory of binary quadratic forms. The pairs $(Q_{i-1}, P_i, Q_i)$ are the reduced forms of discriminant $4D$ in the principal cycle, and $Q_i = r^2$ at an even step means that the form $F$ there is the square of a form $G$ with first coefficient $r$ in the class group. The second walk runs through the cycle of $G^{-1}$, which is symmetric, and its point of symmetry is an ambiguous form, whose coefficients give a factor of $D$. The factor is trivial when $G$ is itself in the principal class, as for $N = 13231$ and $Q_4 = 9$. Gower and Wagstaff give this argument in full.

## Complexity

- **Per step.** $O(1)$ operations on numbers below $2\sqrt{kN}$ on the word RAM, so $O(n^2)$ bit operations for an arbitrary-precision $N$, or less since the numbers have about $n/2$ binary digits.
- **With the limit $I$.** At most $I$ forward steps and, for each square found, at most $I$ backward steps.
- **Heuristic bound.** A square $Q_i$ at an even step appears after about $O(\sqrt[4]{kN})$ steps on average, because the $Q_i$ are below $2\sqrt{kN}$ and a number of that size is a square with probability about $(kN)^{-1/4}$. The expected total time is then $O(N^{1/4})$ for a fixed $k$, which is the bound of Shanks and of the analysis of Gower and Wagstaff. This is a heuristic, not a theorem. There is no proved bound of this form; the length of the period of the continued fraction of $\sqrt{kN}$ can be much larger than $N^{1/4}$, and a run may need several multipliers.
- **Space.** $O(1)$ numbers.

## Properties

- **Small numbers.** All values are below $2\sqrt{kN}$. For $kN < 2^{62}$, they are below $2^{32}$, and their products fit in 64 bits. This is the main practical merit of SQUFOF.
- **Deterministic.** For fixed $N$, $k$ and $I$ the output is fixed. A failure leads to the next multiplier.
- **Independent of the size of the factors.** Unlike [Pollard's rho](/pollard-rho/) or [trial division](/trial-division/), the run time depends on $N$, not on its smallest factor, so it does not find small factors faster.
- **Cheap test.** The perfect-square test runs only at even steps, and a test of $Q \bmod 64$, $63$ and $65$ against tables of squares rejects most $Q$ before any square root.

## Variants and improvements

- **Multipliers.** Running SQUFOF on $kN$ for squarefree $k$ such as $1, 3, 5, 7, 11, 15, 21, \dots, 1155$ (the products of the primes $3, 5, 7, 11$) changes the cycle, and the multiplier that succeeds first can be much faster. Programs try them in turn, or run several of them step by step in parallel.
- **The queue.** Shanks kept a short list of the small $Q_j$ seen before the square; if the root $r$ of a square is in it, the square leads to a trivial factor and is skipped without the second walk. This removes most failures like the one for $N = 13231$.
- **Forms instead of fractions.** The same walk can be written as reduction of indefinite binary quadratic forms, which is the original view of Shanks and the setting of the proof that the second walk finds an ambiguous form.
- **Šimerka's method.** In 1858 Václav Šimerka factored numbers with a related use of quadratic forms and their composition (Lemmermeyer).

## When to use it

SQUFOF is a good choice for $N$ up to about $2^{62}$, where its 32-bit arithmetic makes each step very cheap, for example as the routine that splits the cofactors of two large primes in the [quadratic sieve](/quadratic-sieve/) or the [number field sieve](/general-number-field-sieve/). [Brent's rho](/brent-pollard-rho/) with [Montgomery multiplication](/montgomery-multiplication/) is a competitor in the same range and is faster when the smallest factor is small. For larger $N$, use the [elliptic curve method](/elliptic-curve-factorization/) or the [quadratic sieve](/quadratic-sieve/).

## Pitfalls

- **Odd steps.** Only $Q_i$ at even $i$ are squares modulo $N$ (since $A_{i-1}^2 - DB_{i-1}^2 = (-1)^i Q_i$). A square at an odd step does not give a square form, and the second walk from it is useless.
- **Perfect squares.** If $kN$ is a square, $a^2 = D$ and $Q_1 = 0$. Test for a square $N$ first, and skip the multipliers that make $kN$ a square or share a factor with $N$.
- **Trivial factors.** A square can lead to $\gcd(N, R) = 1$, as above; then go on with the forward walk, do not stop.
- **A missing limit.** Without the limit $I$ the forward walk can run for the whole period of the continued fraction, which can be much longer than $N^{1/4}$, and on a prime $N$ it never stops looking. With $I$ about $4\sqrt{2\sqrt{kN}}$, a run is bounded.
- **Large $N$.** For $N$ beyond about $2^{80}$, the $N^{1/4}$ steps are too many. SQUFOF is a method for small numbers.
- **Small factors.** SQUFOF is no faster on $N = 3q$ than on a product of two equal-sized primes. Run [trial division](/trial-division/) first.

## Implementations

## History

Daniel Shanks developed SQUFOF in the 1970s as a refinement of the continued fraction and quadratic form methods, and he is reported to have programmed it on an HP-65 pocket calculator. He did not publish it in a journal. Samuel Wagstaff and Jason Gower gave the first full description and analysis in 2008, from Shanks' notes and Gower's 2004 thesis. Franz Lemmermeyer showed in 2013 that Václav Šimerka had used a related method in 1858.

## References
