---
tag: 8SEBVH
kind: definition
slug: unimodal-function
name: Unimodal function
aliases:
- single-peaked function
- single-valleyed function
- unimodal sequence
area: searching/search-on-answers
level: intro
summary: A function that strictly increases up to a single maximum and then strictly decreases, or the reverse for minima.
prereqs: [monotone-predicate]
see_also: [unimodal-optimization, ternary-search, golden-section-search, fibonacci-search-unimodal, unimodal-maximum, peak-finding, bitonic-sequence, quasiconvex-function]
sources:
  - paper: doi:10.1090/S0002-9939-1953-0055639-3
    title: "J. Kiefer, Sequential minimax search for a maximum, Proceedings of the American Mathematical Society 4(3) (1953), 502-506"
    locator: the definition of a unimodal function on an interval and the search problem for its maximum
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 3.4, Quasiconvex functions
  - book: isbn:9783319725468
    title: Antti Laaksonen, Guide to Competitive Programming, first edition, Springer, 2017
    locator: Section 8.3, Finding Minimum Values (8.3.1 Ternary Search, 8.3.2 Convex Functions)
---

A unimodal function is a real function on an ordered domain that strictly increases up to one point and strictly decreases after it, so it has exactly one local maximum, which is also its global maximum. The mirror form strictly decreases and then strictly increases, and has one minimum. Unimodality is the condition under which a comparison of two function values throws away part of the domain, which is what [ternary search](/ternary-search/), [golden-section search](/golden-section-search/) and [Fibonacci search](/fibonacci-search-unimodal/) need. A unimodal sequence on the integers is also called a [bitonic sequence](/bitonic-sequence/) when its two parts are sorted.

## Definition

Let $D$ be a totally ordered set, in practice a real interval $[a, b]$ or an integer range $\{0, 1, \ldots, n-1\}$, and let $f : D \to \mathbb{R}$.

**Unimodal for a maximum.** $f$ is (strictly) unimodal if there is a point $m \in D$ such that

$$x < y \le m \implies f(x) < f(y) \qquad\text{and}\qquad m \le x < y \implies f(x) > f(y),$$

for all $x, y \in D$. The point $m$ is the **mode**. It is unique, and $f(m) > f(x)$ for all $x \ne m$. Either side may be empty: an increasing function is unimodal with $m = b$.

**Unimodal for a minimum.** $f$ is unimodal for a minimum if $-f$ is unimodal for a maximum: it strictly decreases up to $m$ and strictly increases after it. The search pages state their results for one of the two forms; the other follows by a change of sign.

**Weakly unimodal.** $f$ is weakly unimodal if there is an $m$ with $f$ non-decreasing on $\{x \le m\}$ and non-increasing on $\{x \ge m\}$. This allows flat parts. Combinatorics usually uses this weak form for sequences: the row $1, 5, 10, 10, 5, 1$ of binomial coefficients $\binom{5}{k}$ is weakly unimodal.

**The comparison lemma.** Let $f$ be unimodal for a maximum on $D$ with mode $m$, and let $x_1 < x_2$ be in $D$. Then

1. if $f(x_1) < f(x_2)$, then $m > x_1$;
2. if $f(x_1) > f(x_2)$, then $m < x_2$;
3. if $f(x_1) = f(x_2)$, then $x_1 < m < x_2$.

*Proof.* (1) Suppose $m \le x_1$. Then $m \le x_1 < x_2$, and $f$ strictly decreases on $\{x \ge m\}$, so $f(x_1) > f(x_2)$, a contradiction. (2) Suppose $m \ge x_2$. Then $x_1 < x_2 \le m$, so $f(x_1) < f(x_2)$, a contradiction. (3) By the two cases just shown, $m \le x_1$ gives $f(x_1) > f(x_2)$ and $m \ge x_2$ gives $f(x_1) < f(x_2)$. Neither is possible when the values are equal, so $x_1 < m < x_2$. $\square$

So after one comparison of two values, the mode is in $\{x > x_1\}$ or in $\{x < x_2\}$, and a search may drop the other end of the domain. This is the whole basis of [unimodal optimization](/unimodal-optimization/). The lemma fails for weakly unimodal functions, as the second non-example below shows.

**The integer form.** On $\{0, 1, \ldots, n-1\}$, $f$ is unimodal for a maximum if and only if there is an $m$ with $f(i) < f(i+1)$ for all $i < m$ and $f(i) > f(i+1)$ for all $i \ge m$ with $i + 1 < n$. *Proof.* The definition gives these inequalities for adjacent points; conversely, chains of adjacent strict inequalities give the strict inequalities for all pairs on each side. $\square$ So the test $P(i) = (f(i) > f(i+1))$ is a [monotone predicate](/monotone-predicate/) on $\{0, \ldots, n-2\}$ whose threshold is $m$, and a [binary search](/binary-search/) on it finds the mode with $\lceil \lg n \rceil$ evaluations of $P$.

## Examples and non-examples

- **A parabola.** $f(x) = -(x - 2)^2$ on $[0, 5]$ is unimodal for a maximum with $m = 2$. With $x_1 = 1$ and $x_2 = 4$, $f(1) = -1 > f(4) = -4$, and by case 2 of the lemma $m < 4$.
- **A sequence.** $1, 3, 8, 12, 4, 2$ is unimodal with mode at index 3. It is a bitonic sequence.
- **The absolute value.** $f(x) = |x - c|$ on $[a, b]$ with $a \le c \le b$ is unimodal for a minimum with $m = c$. It has no derivative at $c$; unimodality does not need one.
- **A convex function.** If $f$ is continuous and strictly convex on $[a, b]$, it is unimodal for a minimum. *Proof.* By continuity, $f$ has a minimum point $m$ on the compact interval. It is the only one: two minimum points $m_1 < m_2$ would give $f((m_1 + m_2)/2) < f(m_1)$. Let $x < y \le m$. If $y = m$, then $f(x) > f(m)$ by uniqueness. If $y < m$, then $y = \lambda x + (1 - \lambda) m$ with $0 < \lambda < 1$, and $f(y) < \lambda f(x) + (1 - \lambda) f(m) \le f(x)$. The right side of $m$ is symmetric. $\square$ The converse is false: $f(x) = \sqrt{|x|}$ on $[-1, 1]$ is unimodal for a minimum and not convex.
- **Non-example: two peaks.** $\sin x$ on $[0, 3\pi]$ has maxima at $\pi/2$ and $5\pi/2$. With $x_1 = \pi/2$ and $x_2 = 5\pi/2$ the values are equal, and case 3 of the lemma would place the mode strictly between them, where $\sin$ is smaller. The sequence $1, 4, 2, 5, 3$ fails in the same way.
- **Non-example: a plateau.** The sequence $f = (1, 2, 2, 2, 2, 2, 3, 1)$ on indices $0$ to $7$ is weakly unimodal with its maximum at index 6. With $x_1 = 2$ and $x_2 = 4$, $f(x_1) = f(x_2) = 2$, but the maximum is not between them. A ternary search that drops the right part on a tie loses the maximum. Strictness is the part of the definition that makes ties safe.
- **Non-example: a constant.** A constant function is weakly unimodal for every $m$, and not strictly unimodal. Every point is a maximum, so a search returns a correct value but no single mode exists.

## Related definitions

- **Quasiconcave and quasiconvex functions.** $f$ is quasiconcave if each upper level set $\{x : f(x) \ge t\}$ is convex (an interval, on the line), and quasiconvex if $-f$ is quasiconcave; see the page on [quasiconvex functions](/quasiconvex-function/). A unimodal function on an interval is quasiconcave: for $x < z < y$, $z$ is on the rising side of $x$ or on the falling side of $y$, so $f(z) > \min(f(x), f(y))$. Quasiconcavity alone allows flat parts and an unattained supremum, so it is closer to weak unimodality.
- **[Convex function](/convex-function/).** Every continuous strictly convex function on a closed interval is unimodal for a minimum (proved above). For a convex function that is not strictly convex, the set of minimum points is an interval and the function is only weakly unimodal.
- **[Bitonic sequence](/bitonic-sequence/).** A sequence that first increases and then decreases, or a cyclic shift of one. Sorting networks use the cyclic form, which is not unimodal in the sense of this page.
- **[Monotone predicate](/monotone-predicate/).** The integer form above turns a unimodal sequence into a monotone predicate on its differences.
- **Peak.** An index whose value is at least that of its neighbours. A unimodal sequence has exactly one; a general array has at least one, which [peak finding](/peak-finding/) finds without unimodality.

## References
