---
tag: 06CGXM
kind: theorem
slug: sturm-theorem
name: Sturm's theorem
aliases:
- Sturm's root-counting theorem
- Sturm theorem
area: algebra/polynomial-arithmetic
level: advanced
summary: The difference in sign changes of a Sturm sequence at two points counts the distinct real roots between them.
prereqs: [sturm-sequence, square-free-polynomial]
see_also: [sturm-sequence, descartes-rule-of-signs, budan-fourier-theorem, real-root-isolation, real-root-counting, vincent-theorem, real-closed-field, cauchy-root-bound]
sources:
  - book: doi:10.1007/3-540-33099-2
    title: Saugata Basu, Richard Pollack and Marie-Francoise Roy, Algorithms in Real Algebraic Geometry, second edition, Springer, 2006
    locator: Section 2.2.2, Sturm's Theorem and the Cauchy Index
  - book: isbn:9780195125160
    title: Chee K. Yap, Fundamental Problems of Algorithmic Algebra, Oxford University Press, 2000
    locator: Chapter VII, Sturm Theory
  - book: doi:10.1007/978-3-7643-7990-2_29
    title: Charles François Sturm, Mémoire sur la résolution des équations numériques, reprinted in Collected Works of Charles François Sturm, Birkhäuser, 2009
    locator: pp. 345 to 390
---

Sturm's theorem counts the distinct real roots of a real polynomial in an interval by exact arithmetic. Build the [Sturm sequence](/sturm-sequence/) of $f$, evaluate it at the two ends, and count sign changes: the difference of the two counts is the number of roots. Unlike [Descartes' rule of signs](/descartes-rule-of-signs/), the count is exact, and it holds for every polynomial, square-free or not.

## Statement

Let $f \in \mathbb{R}[x]$ have degree $n \ge 1$. Let $f_0 = f$, $f_1 = f'$ and $f_{i+1} = -\operatorname{rem}(f_{i-1}, f_i)$ for $i \ge 1$, where $k$ is the last index with $f_k \ne 0$. For $x \in \mathbb{R}$ let $V(x)$ be the number of sign changes in $f_0(x), f_1(x), \ldots, f_k(x)$ after the zeros are removed. Let $V(\pm\infty)$ be the number of sign changes in the signs of $f_i$ for $x \to \pm\infty$, that is, of $\operatorname{lc}(f_i)$ and of $(-1)^{\deg f_i}\operatorname{lc}(f_i)$.

**Theorem (Sturm).** For all real $a < b$ such that neither $a$ nor $b$ is a multiple root of $f$, the number of distinct roots of $f$ in the half-open interval $(a, b]$ is $V(a) - V(b)$. In particular:

1. if neither $a$ nor $b$ is a root of $f$, the number of distinct roots in $(a, b)$ is $V(a) - V(b)$;
2. the number of distinct real roots of $f$ is $V(-\infty) - V(+\infty)$.

If $f$ is [square-free](/square-free-polynomial/), it has no multiple roots and the condition on $a$ and $b$ is empty.

The theorem holds with $\mathbb{R}$ replaced by any [real closed field](/real-closed-field/), since the proof uses only the intermediate value property for polynomials and the sign of a polynomial near a point. It also holds for every sequence that starts with $f, f'$ and is built with positive multiples of the remainders, because the proof uses only properties (P1) to (P4) below.

## In plain words

Take a polynomial and build its chain of divisions with the sign flips. Put a number into every member of the chain, keep the signs, and count how often the sign flips from one member to the next. As the number moves from left to right along the real line, this count never goes up. It goes down by exactly one each time the number passes a root of the polynomial, and it stays the same everywhere else. So the count at the left end minus the count at the right end is the number of different roots in between. A root that appears twice or more is counted once. Large enough numbers on each side give the total number of real roots.

## Proof

Write $V_f$ for the count of the theorem. Euclid's relations are

$$f_{i-1} = q_i f_i - f_{i+1} \qquad (1 \le i \le k - 1), \qquad f_{k-1} = q_k f_k.$$

**Step 1: divide by the last term.** Let $g = f_k$. By the relations, $g$ divides $f_{k-1}$, then $f_{k-2} = q_{k-1} f_{k-1} - f_k$, and so on down to $f_1$ and $f_0$. Conversely every common divisor of $f_0$ and $f_1$ divides $f_2 = q_1 f_1 - f_0$, then $f_3$, and so on to $f_k$. So $g$ is a nonzero constant multiple of $\gcd(f, f')$. Let $h_i = f_i / g \in \mathbb{R}[x]$. Then $h_k = 1$ and

$$h_{i-1} = q_i h_i - h_{i+1} \qquad (1 \le i \le k - 1).$$

For $x$ with $g(x) \ne 0$, the list $f_0(x), \ldots, f_k(x)$ is the list $h_0(x), \ldots, h_k(x)$ multiplied by the nonzero number $g(x)$, so the two lists have the same number of sign changes. Write $W(x)$ for the number of sign changes in $h_0(x), \ldots, h_k(x)$. Then $V_f(x) = W(x)$ whenever $g(x) \ne 0$.

**Step 2: the roots of $h_0$.** Let $c$ be a root of $f$ of multiplicity $m \ge 1$, and write $f = (x - c)^m u$ with $u(c) \ne 0$. Then $f' = (x - c)^{m - 1}(m u + (x - c) u')$, and the second factor does not vanish at $c$ because $m u(c) \ne 0$. So $(x - c)^{m-1}$ is the exact power of $x - c$ in $\gcd(f, f')$, and $x - c$ divides $h_0 = f/g$ exactly once. Any root of $h_0$ is a root of $f$. Hence the real roots of $h_0$ are exactly the distinct real roots of $f$.

**Step 3: four properties of the $h_i$.**

(P1) $h_k = 1$ has no root.

(P2) Two consecutive terms have no common root. If $h_i(c) = h_{i+1}(c) = 0$ with $i + 1 \le k$, then $h_{i+2}(c) = q_{i+1}(c) h_{i+1}(c) - h_i(c) = 0$ by the relation for index $i + 1$, and so on up to $h_k(c) = 0$, which contradicts (P1).

(P3) If $0 < i < k$ and $h_i(c) = 0$, then $h_{i-1}(c) = -h_{i+1}(c)$, and both are nonzero by (P2). So they have opposite signs.

(P4) If $h_0(c) = 0$, then $h_1(c) \ne 0$ by (P2), and $h_0 h_1$ is negative just left of $c$ and positive just right of $c$. Indeed $h_0 h_1 = f f' / g^2$, and with the notation of step 2,

$$f f' = (x - c)^{2m - 1}\, u\,(m u + (x - c) u').$$

Near $c$ the factor $u (m u + (x - c) u')$ has the sign of $m u(c)^2 > 0$, so $f f'$ has the sign of $(x - c)^{2m-1}$, which is the sign of $x - c$. The positive factor $g^2$ does not change the sign at points near $c$ other than $c$.

**Step 4: a deletion rule.** In a list of reals, if an entry has two neighbours that are nonzero and of opposite signs, then removing that entry does not change the number of sign changes. Indeed the three entries $s, t, -s$ contribute exactly one sign change whatever the sign of $t$, and so do the two entries $s, -s$.

**Step 5: $W$ is a step function.** Let $c$ be a root of some $h_i$. Choose $\varepsilon > 0$ such that no $h_j$ has a root in $[c - \varepsilon, c + \varepsilon]$ other than possibly $c$. Then each $h_j$ with $h_j(c) \ne 0$ has a constant sign on the whole interval, by the intermediate value property. Let $Z = \{ j : h_j(c) = 0 \}$. By (P1) $k \notin Z$, and by (P2) $Z$ has no two consecutive indices.

Fix $x \in [c - \varepsilon, c + \varepsilon]$. For each $j \in Z$ with $j \ge 1$, the neighbours $h_{j-1}$ and $h_{j+1}$ are not in $Z$, so they are nonzero at $x$; they have opposite signs at $c$ by (P3), and so at $x$. By step 4 we can delete all entries with index in $Z \setminus \{0\}$, one at a time, without changing the count; the neighbours of each deleted entry are never deleted. Every entry that is left, except possibly the entry $h_0(x)$, has a sign that does not depend on $x$.

- If $0 \notin Z$, every entry left has a constant sign, so $W$ is constant on $[c - \varepsilon, c + \varepsilon]$.
- If $0 \in Z$, then $1 \notin Z$, so $h_1(x)$ is still the entry next to $h_0(x)$. By (P4), the pair $h_0(x), h_1(x)$ gives one sign change for $x < c$ and none for $x > c$. At $x = c$ the entry $h_0(c) = 0$ is dropped, so it gives none. Hence $W(x) = W(c) + 1$ for $x \in [c - \varepsilon, c)$ and $W(x) = W(c)$ for $x \in [c, c + \varepsilon]$.

Between two consecutive roots of the polynomials $h_j$, no entry changes sign, so $W$ is constant there. Combining, $W$ is constant except that it drops by exactly one at each root of $h_0$, and it takes its new value at the root itself. So for $a < b$, $W(a) - W(b)$ is the number of roots of $h_0$ in $(a, b]$. By step 2 this is the number of distinct roots of $f$ in $(a, b]$.

**Step 6: back to $f$.** The roots of $g$ are exactly the multiple roots of $f$, by step 2. So the hypothesis says $g(a) \ne 0$ and $g(b) \ne 0$, and step 1 gives $V_f(a) - V_f(b) = W(a) - W(b)$, which is the number of distinct roots of $f$ in $(a, b]$ by step 5. Part 1 follows because $b$ is then not in the set of roots. For part 2, every $f_i$ has the sign of its leading term for all $|x| \ge R$, for $R$ large, so $V(\pm\infty) = V(\pm R)$; take $R$ larger than the absolute value of every real root of $f$ and apply part 1 on $(-R, R)$. $\blacksquare$

## Consequences

- **Root counting and isolation.** With [Cauchy's root bound](/cauchy-root-bound/) $R$, $V(-R) - V(R)$ is the number of distinct real roots, and bisection with the count at each midpoint gives isolating intervals for all of them. This is the Sturm method of [real root isolation](/real-root-isolation/).
- **All roots real.** A polynomial of degree $n$ has $n$ distinct real roots if and only if $V(-\infty) - V(+\infty) = n$. Since $V(-\infty) \le k \le n$ and $V(+\infty) \ge 0$, this holds if and only if the sequence has $n + 1$ terms with degrees $n, n - 1, \ldots, 0$ and the leading coefficients all have the same sign.
- **Decision procedure.** Whether a polynomial with rational coefficients has a real root in a rational interval is decided by exact arithmetic over $\mathbb{Q}$. Generalizations with a second polynomial $g$ in place of $f'$ (signed remainder sequences of $f$ and $f' g$) count the roots of $f$ at which $g$ is positive minus those at which it is negative; Basu, Pollack and Roy develop this through the Cauchy index in Section 2.2.2, and it is a base of [quantifier elimination](/quantifier-elimination/) over the reals.
- **Integer arithmetic.** Since only properties (P1) to (P4) are used, the remainders may be replaced by positive multiples. This allows fraction-free computation with [pseudo-division](/pseudo-division/) and Sturm-Habicht sequences built from [subresultants](/subresultant-gcd/).

## Tightness

- **Distinct roots, not multiplicities.** For $f = x^2$ the sequence is $x^2, 2x$, and $V(-1) - V(1) = 1 - 0 = 1$. The double root at $0$ is counted once. Descartes' rule counts with multiplicity but only gives an upper bound.
- **Endpoints.** The interval is half-open. For $f = x$ the sequence is $x, 1$, with $V(-1) = 1$, $V(0) = 0$ and $V(1) = 0$. So the root $0$ is counted in $(-1, 0]$ and not in $(0, 1]$.
- **Multiple roots at an endpoint.** The hypothesis on $a$ and $b$ cannot be dropped. For $f = x^2(x - 1) = x^3 - x^2$ the sequence is $x^3 - x^2, 3x^2 - 2x, \tfrac{2}{9}x$, and every term vanishes at the double root $0$, so $V(0) = 0$. Also $V(2) = 0$, but $f$ has the root $1$ in $(0, 2]$. The fix is to evaluate the reduced sequence $f_i / f_k$ at such a point, or to move the point slightly.
- **The sign change is needed.** For $f = x^2 - 1$ the list $x^2 - 1, 2x, -1$ built with the remainder instead of its negative has one sign change at both $-\infty$ and $+\infty$, and so counts zero roots instead of two. Property (P3) fails for it.
- **The field must be real closed for the roots to exist.** Over $\mathbb{Q}$ the computation still runs, but for $f = x^2 - 2$ it gives $V(0) - V(2) = 1$ while $f$ has no rational root. The theorem counts roots in the real closure, here $\sqrt 2 \in \mathbb{R}$.

## History

Sturm stated the theorem in his memoir on the solution of numerical equations, read to the Paris Academy in 1829 and reprinted in his collected works, pp. 345 to 390. It answered the problem of counting the real roots of an equation in an interval exactly, where the earlier rules of Descartes and of [Budan and Fourier](/budan-fourier-theorem/) gave only upper bounds. Basu, Pollack and Roy, Chapter 2, and Yap, Chapter VII, give modern proofs and the generalizations to Cauchy indices and subresultant sequences.

## References
