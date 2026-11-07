---
tag: DAGHKF
kind: theorem
slug: budan-fourier-theorem
name: Budan-Fourier theorem
aliases:
- Budan's theorem
- Fourier-Budan theorem
- Fourier's theorem on real roots
area: numerical/root-finding
level: advanced
summary: For a real polynomial, the drop V(a) - V(b) in sign changes of p, p', ..., p^(n) bounds the number of roots in (a, b], counted with multiplicity, and exceeds it by an even number.
prereqs: [descartes-rule-of-signs, multiplicity-of-roots]
see_also: [real-root-counting, sturm-theorem, vincent-theorem, vincent-collins-akritas, cauchy-root-bound, gauss-lucas-theorem, bisection-method, polynomial-root-finding]
sources:
  - book: "François Budan de Boislaurent, Nouvelle méthode pour la résolution des équations numériques d'un degré quelconque, Paris, 1807"
    locator: the count of sign changes in the coefficients of p(x + a) and p(x + b)
  - paper: "Joseph Fourier, Sur l'usage du théorème de Descartes dans la recherche des limites des racines, Bulletin des Sciences par la Société Philomatique de Paris, 1820"
    locator: the theorem stated with the sequence of derivatives
  - book: "Saugata Basu, Richard Pollack and Marie-Françoise Roy, Algorithms in Real Algebraic Geometry, second edition, Springer, 2006"
    locator: Chapter 2, Real Closed Fields (the Budan-Fourier theorem with its proof and Descartes's law of signs as a corollary)
  - book: "Morris Marden, Geometry of Polynomials, second edition, Mathematical Surveys 3, American Mathematical Society, 1966"
    locator: the chapter on the number of real zeros (the theorems of Descartes, Budan-Fourier and Sturm)
---

The Budan-Fourier theorem bounds the number of real roots of a real polynomial in an interval by counting sign changes in the sequence $p, p', p'', \dots, p^{(n)}$ at the two ends. If $V(x)$ is the number of sign changes of that sequence at $x$, then $V(a) - V(b)$ is at least the number of roots in $(a, b]$, counted with multiplicity, and the two differ by an even number. When the drop is 0 there is no root in $(a, b]$, and when it is 1 there is exactly one, which gives a bracket for [bisection](/bisection-method/). [Descartes' rule of signs](/descartes-rule-of-signs/) is the case $a = 0$, $b = \infty$. Unlike [Sturm's theorem](/sturm-theorem/), the count is only an upper bound.

## Statement

Let $p$ be a real polynomial of degree $n \ge 1$. For real $x$ let $V(x)$ be the number of sign changes in the sequence
$$p(x), p'(x), p''(x), \dots, p^{(n)}(x)$$
after deleting the zeros. ($p^{(n)} = n!\,a_0$ is a nonzero constant, so the sequence is never all zero.) For $a < b$ let $N(a, b)$ be the number of roots of $p$ in $(a, b]$, counted with [multiplicity](/multiplicity-of-roots/).

**Theorem (Budan 1807, Fourier 1820).** For all real $a < b$,
$$V(a) - V(b) = N(a, b) + 2k \qquad\text{for some integer } k \ge 0 .$$
In particular $N(a, b) \le V(a) - V(b)$, and $N(a, b) = V(a) - V(b)$ when the right side is 0 or 1.

**Budan's form.** By Taylor's formula, $p^{(j)}(a) = j!\,c_j$ where $p(x + a) = \sum_j c_jx^j$, so $V(a)$ is the number of sign changes in the coefficients of $p(x + a)$.

**Descartes' rule.** For $x$ large, every $p^{(j)}(x)$ has the sign of $a_0$, so $V(+\infty) = 0$; and $V(0)$ is the number of sign changes in the coefficients of $p$. So the number of positive roots is the number of sign changes in the coefficients minus an even number $\ge 0$. (Use $(0, b]$ with $b$ above the [Cauchy bound](/cauchy-root-bound/), and note that $V(0)$ counts no root at 0 because $(0, b]$ is open at 0.)

## In plain words

Write down the signs of the polynomial and all its derivatives at a point, and count how often the sign flips along the list. Move the point to the right. Every time it passes a root of the polynomial, the count drops by the multiplicity of the root. Every time it passes a point where only some derivative vanishes, the count either stays the same or drops by an even number. So the total drop between two points counts the roots in between, plus an even overcount that can come from pairs of complex roots. A drop of zero or one is exact.

## Proof

Fix $c$ and choose $\varepsilon > 0$ so small that no $p^{(j)}$, $0 \le j \le n$, has a root in $[c - \varepsilon, c) \cup (c, c + \varepsilon]$; this is possible since each nonzero polynomial has finitely many roots. Then $V$ is constant on $[c - \varepsilon, c)$ and on $(c, c + \varepsilon]$; write $V(c^-)$ and $V(c^+)$ for these values.

*Lemma (a block of zeros).* Let $g$ be a real polynomial with a root of multiplicity $\mu \ge 1$ at $c$, so $g(c) = \cdots = g^{(\mu-1)}(c) = 0 \ne g^{(\mu)}(c) =: \gamma$. For $0 < x - c < \varepsilon$, $g^{(i)}(x)$ has the sign of $\gamma$ for $0 \le i \le \mu$. For $0 < c - x < \varepsilon$, $g^{(i)}(x)$ has the sign of $(-1)^{\mu - i}\gamma$.

*Proof of the lemma.* By Taylor's formula, $g^{(i)}(x) = \gamma\,(x - c)^{\mu - i}/(\mu - i)! \cdot (1 + O(x - c))$ for $i \le \mu$, and the factor $1 + O(x - c)$ is positive for $x$ close to $c$; within $\varepsilon$ none of these functions changes sign, so the sign is that of $\gamma(x - c)^{\mu - i}$. $\square$

*The drop at $c$.* Split the indices $0, \dots, n$ at $c$ into maximal runs of consecutive $j$ with $p^{(j)}(c) = 0$. A pair $(i, i+1)$ with both values nonzero at $c$ keeps its signs on $[c - \varepsilon, c + \varepsilon]$, so it contributes the same to $V(c^-)$ and $V(c^+)$. Consider a run $j, \dots, j + \mu - 1$; then $p^{(j + \mu)}(c) \ne 0$, and $g = p^{(j)}$ has a root of multiplicity $\mu$ at $c$. Let $s$ be the sign of $p^{(j+\mu)}(c)$. By the lemma, on the right of $c$ the entries $j, \dots, j + \mu$ all have sign $s$, with no change among them; on the left they alternate and end with $s$, giving $\mu$ changes.

- If $j = 0$ (the run starts at $p$, so $c$ is a root of $p$ of multiplicity $m = \mu$), the run has no left neighbour and the drop is exactly $\mu = m$.
- If $j \ge 1$, the left neighbour $p^{(j-1)}$ is nonzero at $c$, with a fixed sign $\sigma$ near $c$. After $c$ the pair $(j - 1, j)$ contributes $[\sigma \ne s]$; before $c$ it contributes $[\sigma \ne (-1)^\mu s]$. The drop from this run is $\mu + [\sigma \ne (-1)^\mu s] - [\sigma \ne s]$. For even $\mu$ this is $\mu$; for odd $\mu$ it is $\mu \pm 1$. Either way it is even and $\ge 0$.

So $V(c^-) - V(c^+) = m(c) + 2k_c$ with $k_c \ge 0$, where $m(c)$ is the multiplicity of $c$ as a root of $p$ (0 if $p(c) \ne 0$).

*Right continuity.* At $x = c$ itself the zeros are deleted, so each run disappears and its right neighbour $p^{(j+\mu)}(c)$, of sign $s$, follows $p^{(j-1)}(c)$, of sign $\sigma$: the count is $[\sigma \ne s]$, as on the right of $c$. A run at $j = 0$ leaves the sequence starting at sign $s$, again as on the right. Hence $V(c) = V(c^+)$.

*Conclusion.* $V$ is a step function, constant except at the finitely many roots of the $p^{(j)}$, and right continuous. For $a < b$, $V(a) - V(b)$ is the sum of the drops $V(c^-) - V(c^+)$ over the points $c \in (a, b]$ where some $p^{(j)}$ vanishes. Each drop is $m(c)$ plus an even number $\ge 0$, and $\sum_{c \in (a, b]} m(c) = N(a, b)$. $\square$

## Consequences

- **Example, exact.** For $p = (x - 1)(x - 2)(x - 3) = x^3 - 6x^2 + 11x - 6$: $p' = 3x^2 - 12x + 11$, $p'' = 6x - 12$, $p''' = 6$. At $x = 0$ the signs are $(-, +, -, +)$, $V(0) = 3$; at $x = 4$ they are $(+, +, +, +)$, $V(4) = 0$. So there are 3 roots in $(0, 4]$, all of them.
- **Example, with a zero entry.** For $p = x^3 - x - 2$ at $x = 0$ the values are $(-2, -1, 0, 6)$; deleting the zero leaves $(-, -, +)$, $V(0) = 1$. At $x = 2$: $(4, 11, 12, 6)$, $V(2) = 0$. So exactly one root lies in $(0, 2]$, the root $1.5214$.
- **Root isolation.** A drop of 1 certifies one simple root, and a drop of 0 certifies none. Subdivision alone does not always get there: for $x^2 + 1$ every interval that contains 0 has drop 2. [Vincent's theorem](/vincent-theorem/) shows that after enough continued fraction substitutions $x \mapsto q + 1/x$ the coefficient sign count of a square-free polynomial becomes 0 or 1, and the [Vincent-Collins-Akritas](/vincent-collins-akritas/) method turns this into an isolation algorithm with Budan's form on the intervals.
- **Brackets for iterative methods.** An interval with drop 1 and a sign change of $p$ is a valid bracket for [bisection](/bisection-method/) or [Brent's method](/brent-method/) with exactly one root inside.
- **Real-root counting.** For an exact count, use Sturm sequences ([Sturm's theorem](/sturm-theorem/)); Budan-Fourier is cheaper since the derivatives need no division, but only bounds. See [real-root counting](/real-root-counting/).

## Tightness

- **The excess is real.** For $p = x^2 + 1$ on $(-1, 1]$: at $-1$ the signs are $(+, -, +)$, $V(-1) = 2$; at $1$, $(+, +, +)$, $V(1) = 0$. The drop is 2 but there is no real root; the pair $\pm i$ causes it, through the root of $p' = 2x$ at 0 where the drop is 2.
- **The excess can be large.** For $p = x^{2r} + 1$, every derivative up to order $2r - 1$ vanishes at 0 and $V(-1) - V(1) = 2r$ with no real root, so the bound can be off by the full degree.
- **Multiplicities are counted.** For $p = (x - 1)^2$ on $(0, 2]$: $V(0) = 2$ from $(+, -, +)$, $V(2) = 0$, and $N = 2$ counts the double root twice.
- **Half-open interval.** The count is for $(a, b]$, a consequence of the right continuity. For $p = x - 1$: $V(1) = 0$ from $(0, 1)$ with the zero deleted, and $V(0) = 1$, so the root 1 is counted in $(0, 1]$ but not in $(1, 2]$.

## History

François Budan de Boislaurent published his form, in terms of the coefficients of $p(x + a)$, in 1807. Joseph Fourier stated the form with derivatives in an 1820 paper, and the theorem carries both names. Sturm's 1829 theorem, which gives the exact count, was inspired by Fourier's work on the same question. Vincent's 1836 theorem used Budan's form after continued fraction substitutions, and became the basis of modern real root isolation through the work of Collins and Akritas in the 1970s.

## References
