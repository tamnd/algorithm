---
tag: ECN92E
kind: theorem
slug: descartes-rule-of-signs
name: Descartes' rule of signs
aliases:
- Descartes' rule
- Descartes' sign rule
- Descartes' law of signs
area: algebra/polynomial-arithmetic
level: core
summary: The number of positive real roots is at most the number of sign changes in the coefficients.
prereqs: [polynomial, factor-theorem]
see_also: [real-root-isolation, vincent-collins-akritas, vincent-theorem, sturm-theorem, multiplicity-of-roots, polynomial-root-finding, horner-rule, vieta-formulas]
sources:
  - book: doi:10.1007/3-540-33099-2
    title: Saugata Basu, Richard Pollack and Marie-Francoise Roy, Algorithms in Real Algebraic Geometry, second edition, Springer, 2006
    locator: Section 2.2.1, Descartes's Law of Signs and the Budan-Fourier Theorem
  - book: isbn:9780486600680
    title: Rene Descartes, The Geometry of Rene Descartes, translated by David Eugene Smith and Marcia L. Latham, Dover, 1954
    locator: Book III, the rule for the number of true (positive) and false (negative) roots
---

Descartes' rule of signs bounds the number of positive real roots of a real polynomial by the number of sign changes in its list of coefficients. The bound and the true count differ by an even number, so a list with no sign change means no positive root, and a list with exactly one sign change means exactly one positive root. The test needs only a scan of the coefficients, and it is the base of the Descartes method for [real root isolation](/real-root-isolation/).

## Statement

Let $f = \sum_{k=0}^{n} f_k x^k \in \mathbb{R}[x]$ be nonzero. Let $V(f)$ be the number of sign changes in the sequence $f_0, f_1, \ldots, f_n$ after the zero entries are removed: the number of pairs of consecutive nonzero entries with opposite signs. Let $Z(f)$ be the number of roots of $f$ in the open interval $(0, \infty)$, each counted with its [multiplicity](/multiplicity-of-roots/).

**Theorem (Descartes' rule of signs).** $Z(f) \le V(f)$, and $V(f) - Z(f)$ is even.

**Corollary (negative roots).** The number of roots of $f$ in $(-\infty, 0)$, counted with multiplicity, is at most $V(f(-x))$ and has the same parity. The sequence of $f(-x)$ is $f_0, -f_1, f_2, -f_3, \ldots$.

**Corollary (exact cases).** If $V(f) = 0$, $f$ has no positive root. If $V(f) = 1$, $f$ has exactly one positive root, and it is simple. If all roots of $f$ are real, then $Z(f) = V(f)$.

The proof uses only the intermediate value theorem and Rolle's theorem, so the statement holds over every real closed field.

## In plain words

Write down the coefficients of a polynomial from the constant term up, skip the zeros, and count how often the sign flips from plus to minus or from minus to plus. The polynomial cannot have more positive roots than that count. The true number of positive roots is the count, or the count minus two, or minus four, and so on. So no flips means no positive roots, and one flip means exactly one positive root. To bound the negative roots, flip the sign of every odd coefficient and count again. When every root is real, the count is exact.

## Proof

Two reductions first. If $f = x^m g$ with $g(0) \ne 0$, then $f$ and $g$ have the same positive roots with the same multiplicities, and the same nonzero coefficients in the same order, so $V(f) = V(g)$ and $Z(f) = Z(g)$. Multiplying $f$ by a nonzero constant changes neither number. So we may assume $f_0 \ne 0$ whenever we need it.

*Parity.* Assume $f_0 \ne 0$, and let $f_n \ne 0$ be the leading coefficient. The nonzero coefficients start with $f_0$ and end with $f_n$. Each sign change flips the sign, so $V(f)$ is even exactly when $f_0 f_n > 0$. Now factor $f$ over the positive roots. If $r_1, \ldots, r_s$ are the distinct positive roots with multiplicities $m_1, \ldots, m_s$, the [factor theorem](/factor-theorem/) gives $f = (x - r_1)^{m_1} \cdots (x - r_s)^{m_s}\, g$ with $g$ real and $g(t) \ne 0$ for $t > 0$. By the intermediate value theorem $g$ has a constant sign on $(0, \infty)$, and by continuity also at $0$, where $g(0) \ne 0$ because $f(0) = f_0 \ne 0$. The leading coefficient of $g$ is $f_n$, and $g(t)$ has the sign of $f_n$ for large $t$, so $g(0) f_n > 0$. Then

$$f_0 = f(0) = \prod_{i} (-r_i)^{m_i}\, g(0), \qquad \operatorname{sign}(f_0 f_n) = (-1)^{Z(f)} \operatorname{sign}(g(0) f_n) = (-1)^{Z(f)}.$$

So $Z(f)$ is even exactly when $f_0 f_n > 0$, which is exactly when $V(f)$ is even. Hence $V(f) - Z(f)$ is even.

*Bound.* Induction on $n = \deg f$. For $n = 0$, $f$ is a nonzero constant and $Z(f) = V(f) = 0$. Let $n \ge 1$ and assume the bound for all degrees below $n$. By the reductions we may assume $f_0 \ne 0$. The derivative $f' = \sum_{k=1}^{n} k f_k x^{k-1}$ is nonzero of degree $n - 1$. Its coefficient sequence is $f_1, f_2, \ldots, f_n$ with each entry multiplied by the positive number $k$, so its signs are those of $f$ with the first entry $f_0$ removed. Removing the first nonzero entry removes at most one sign change, so $V(f') \le V(f)$.

Now compare the roots. Let $r_1 < \cdots < r_s$ be the distinct positive roots of $f$ with multiplicities $m_1, \ldots, m_s$. A root of multiplicity $m$ of $f$ is a root of multiplicity at least $m - 1$ of $f'$: if $f = (x - r)^m h$, then $f' = (x - r)^{m-1}(m h + (x - r) h')$. By Rolle's theorem, $f'$ has a root strictly between $r_i$ and $r_{i+1}$ for each $i < s$, and these roots are different from all $r_j$. So, if $s \ge 1$,

$$Z(f') \ge \sum_{i=1}^{s} (m_i - 1) + (s - 1) = Z(f) - 1,$$

and if $s = 0$ the bound $Z(f) \le V(f)$ is trivial. By the induction hypothesis, $Z(f') \le V(f')$. So $Z(f) \le Z(f') + 1 \le V(f') + 1 \le V(f) + 1$. By the parity part, $Z(f) \ne V(f) + 1$. Hence $Z(f) \le V(f)$.

*Negative roots.* The roots of $f(-x)$ in $(0, \infty)$ are the negatives of the roots of $f$ in $(-\infty, 0)$, with the same multiplicities. Apply the theorem to $f(-x)$.

*Exact cases.* If $V(f) = 0$ then $Z(f) = 0$. If $V(f) = 1$ then $Z(f) \le 1$ and $Z(f)$ is odd, so $Z(f) = 1$, and the root is simple because it is counted with multiplicity. For the all-real case, divide off the root $0$, so that $f_0 \ne 0$ and every root is a nonzero real number. Let $Z^-$ and $V^-$ be the count and the bound for negative roots. Then $Z(f) + Z^- = n$. We show $V(f) + V^- \le n$. Take two nonzero coefficients $f_i$ and $f_j$, $i < j$, with only zeros between them. In $f(-x)$ they become $(-1)^i f_i$ and $(-1)^j f_j$, so the pair gives a sign change in exactly one of the two sequences if $j - i$ is odd, and in the same number of sequences, $0$ or $2$, if $j - i$ is even. In both cases the pair adds at most $j - i$ to $V(f) + V^-$. Summing over the consecutive pairs from index $0$ to index $n$ gives $V(f) + V^- \le n$. Then $n = Z(f) + Z^- \le V(f) + V^- \le n$, and since $Z(f) \le V(f)$ and $Z^- \le V^-$, both are equalities. $\blacksquare$

## Consequences

- **Real root isolation.** The [Vincent-Collins-Akritas method](/vincent-collins-akritas/) maps an interval $(a, b)$ to $(0, \infty)$ by $x = (a + b y)/(1 + y)$, clears denominators, and counts sign changes. A count of $0$ discards the interval and a count of $1$ certifies one root in it. Otherwise it bisects. [Vincent's theorem](/vincent-theorem/) says that, for a square-free polynomial, the subdivision ends with counts of $0$ or $1$. The change of variable is a Taylor shift, which [Horner's rule](/horner-rule/) computes.
- **Cheap exclusion tests.** A polynomial with all coefficients of one sign has no positive root, and $f(-x)$ gives the same test for negative roots. For example $x^4 + 3x^2 + 1$ has no real root at all, because both sequences have no sign change.
- **Fewnomial bounds.** A real polynomial with $t$ nonzero terms has at most $t - 1$ sign changes, so at most $t - 1$ positive roots and at most $2t - 1$ real roots, whatever its degree. The bound does not depend on the degree, which matters for [sparse polynomials](/sparse-polynomial-representation/).
- **Budan-Fourier.** The coefficients of $f(x + a)$ are $f^{(k)}(a)/k!$, so $V(f(x + a))$ is the number of sign changes in $f(a), f'(a), \ldots, f^{(n)}(a)$. The Budan-Fourier theorem says that the number of roots in $(a, b]$, counted with multiplicity, is at most $V(f(x + a)) - V(f(x + b))$, with an even gap. Descartes' rule is the case $a = 0$ with $b$ large, where the count at $b$ is $0$. See Basu, Pollack and Roy, Section 2.2.1. The exact count needs a [Sturm sequence](/sturm-theorem/).

**Worked examples.** These counts were checked by an exact script.

| $f$ | factored | $V(f)$ | positive roots | $V(f(-x))$ | negative roots |
| --- | --- | --- | --- | --- | --- |
| $x^3 - 7x + 6$ | $(x - 1)(x - 2)(x + 3)$ | 2 | 2 | 1 | 1 |
| $x^2 - x + 1$ | no real roots | 2 | 0 | 0 | 0 |
| $x^2 - 2x + 1$ | $(x - 1)^2$ | 2 | 2 (one double root) | 0 | 0 |
| $x^4 + x^3 - x - 1$ | $(x - 1)(x + 1)(x^2 + x + 1)$ | 1 | 1 | 3 | 1 |
| $x^5 - 5x^4 - 9x^3 + 49x^2 - 8x - 60$ | $(x + 3)(x + 1)(x - 2)^2 (x - 5)$ | 3 | 3 | 2 | 2 |

In the fourth row, the sequence of $f$ from the constant term is $-1, -1, 0, 1, 1$; the zero is skipped and the only change is from $-1$ to $1$. The sequence of $f(-x)$ is $-1, 1, 0, -1, 1$, with three changes, and $f$ has one negative root, $3 - 1 = 2$ below the bound. The last row has only real roots, and both counts are exact.

## Tightness

- **The bound can be strict.** $x^2 - x + 1$ has $V = 2$ and no real roots. The gap is always even, and it can be as large as the degree: $1 - x + x^2 - \cdots + x^{2k} = (x^{2k+1} + 1)/(x + 1)$ has $V = 2k$ and no positive root, because $x^{2k+1} + 1 > 0$ for $x > 0$.
- **Multiplicity is needed.** $(x - 1)^2$ has $V = 2$ but one distinct positive root. The statement is false if roots are counted without multiplicity, since then the parity can fail.
- **The bound is attained.** By the exact case, any polynomial with only real roots, such as $\prod_i (x - r_i)$ with $r_i > 0$, has $Z = V$.
- **The real numbers are needed.** Sign changes make no sense over $\mathbb{C}$. Over an ordered field that is not real closed, the parity part can fail: $x^2 - 2$ has $V = 1$ and no positive root in $\mathbb{Q}$. The proof uses the intermediate value theorem and Rolle's theorem, which hold in every real closed field and fail in $\mathbb{Q}$.

## History

Descartes stated the rule in Book III of La Geometrie (1637), without proof, as a rule for the number of true (positive) and false (negative) roots. Proofs followed in the 18th century, and Gauss showed in 1828 that, when roots are counted with multiplicity, the gap between the bound and the true count is even. Budan and Fourier extended the rule to arbitrary intervals in the early 19th century, and Vincent's theorem of 1836 showed how continued fraction transformations reduce every sign count to $0$ or $1$. Collins and Akritas turned this into the Descartes method for real root isolation in 1976, which is still one of the fastest exact methods in practice.

## References
