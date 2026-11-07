---
tag: NR3ZMR
kind: concept
slug: sturm-sequence
name: Sturm sequence
aliases:
- Sturm chain
- Sturm's algorithm
- signed remainder sequence
area: algebra/polynomial-arithmetic
level: advanced
summary: Sequence of polynomials from f and f' by negated remainders; sign changes at two points count real roots between them.
prereqs: [polynomial-euclidean-algorithm, polynomial-gcd]
see_also: [sturm-theorem, real-root-isolation, real-root-counting, descartes-rule-of-signs, polynomial-euclidean-algorithm, subresultant-gcd, pseudo-division, square-free-polynomial]
sources:
  - book: doi:10.1007/3-540-33099-2
    title: Saugata Basu, Richard Pollack and Marie-Francoise Roy, Algorithms in Real Algebraic Geometry, second edition, Springer, 2006
    locator: Section 2.2.2, Sturm's Theorem and the Cauchy Index (signed remainder sequences)
  - book: isbn:9780195125160
    title: Chee K. Yap, Fundamental Problems of Algorithmic Algebra, Oxford University Press, 2000
    locator: Chapter VII, Sturm Theory
  - book: doi:10.1007/978-3-7643-7990-2_29
    title: Charles François Sturm, Mémoire sur la résolution des équations numériques, reprinted in Collected Works of Charles François Sturm, Birkhäuser, 2009
    locator: pp. 345 to 390
---

The Sturm sequence of a real polynomial $f$ is the list $f_0 = f$, $f_1 = f'$, $f_{i+1} = -(f_{i-1} \bmod f_i)$, that is, the [Euclidean algorithm](/polynomial-euclidean-algorithm/) on $f$ and its derivative with every remainder negated. The sign changes in the values of this list at a point $x$ give a number $V(x)$, and [Sturm's theorem](/sturm-theorem/) says that $V(a) - V(b)$ is the number of distinct real roots of $f$ in $(a, b]$ when $a$ and $b$ are not multiple roots. The sequence turns root counting into exact arithmetic on polynomials, and it is one of the two classic tests behind [real root isolation](/real-root-isolation/).

## In plain words

Start with a polynomial and its derivative. Divide the first by the second, keep the remainder, and flip its sign. Then divide the second by this new polynomial, flip the sign of the remainder again, and continue until the remainder is zero. This is the same chain of divisions that finds a greatest common divisor, with one sign change added at each step.

To use the list at a number, put the number into every polynomial in it and write down only the signs. Count how often the sign flips as you read from left to right. Do this at two numbers. The drop in the count from the smaller number to the larger one is how many different real roots lie between them. No root has to be computed, and exact fractions give a sure answer.

## The idea

Let $f \in \mathbb{R}[x]$ have degree $n \ge 1$. All statements hold with $\mathbb{R}$ replaced by any [real closed field](/real-closed-field/), and the computation needs only the ordered subfield that contains the coefficients, for example $\mathbb{Q}$.

**Definition.** The *Sturm sequence* of $f$ is $f_0, f_1, \ldots, f_k$ with

$$f_0 = f, \qquad f_1 = f', \qquad f_{i+1} = -\operatorname{rem}(f_{i-1}, f_i) \quad (i \ge 1),$$

where $\operatorname{rem}$ is the remainder of [polynomial division](/polynomial-division/), and $k$ is the last index with $f_k \ne 0$. Thus $f_{i-1} = q_i f_i - f_{i+1}$ with $\deg f_{i+1} < \deg f_i$, so $k \le n$.

**Sign variations.** For a list of real numbers, the number of *sign variations* is the number of sign changes after the zeros are removed. For $x \in \mathbb{R}$ let $V(x)$ be the number of sign variations of $f_0(x), \ldots, f_k(x)$. Let $V(+\infty)$ and $V(-\infty)$ be the numbers of sign variations of the leading coefficients $\operatorname{lc}(f_i)$ and of $(-1)^{\deg f_i} \operatorname{lc}(f_i)$; these are the values of $V(x)$ for all $x$ of large absolute value.

**The last term is the gcd.** The sequence differs from the remainder sequence of the Euclidean algorithm only in signs, so $f_k$ is a nonzero constant multiple of $\gcd(f, f')$. Hence $f_k$ is a constant if and only if $f$ is [square-free](/square-free-polynomial/). If $f$ is not square-free, every $f_i$ is divisible by $g = f_k$, and $f_0/g, \ldots, f_k/g$ has the same sign variations as $f_0, \ldots, f_k$ at every point where $g \ne 0$.

**Why the signs work.** Three facts make $V(x)$ count roots. Write $h_i = f_i / f_k$.

1. Two consecutive terms $h_i, h_{i+1}$ have no common root, because a common root would pass down the relation $h_{i-1} = q_i h_i - h_{i+1}$ to every term and reach the constant $h_k = 1$.
2. Where a middle term $h_i$ vanishes, $h_{i-1} = -h_{i+1}$ there, so its neighbours have opposite signs and $V$ does not change as $x$ crosses that root.
3. Near a root $c$ of $f$, the product $f f'$ has the sign of $x - c$, so $h_0 h_1$ goes from negative to positive and one sign variation is lost as $x$ crosses $c$.

So $V(x)$ is a step function that drops by one at each distinct real root of $f$ and is constant elsewhere. The full proof is on the page for [Sturm's theorem](/sturm-theorem/).

**Generalized Sturm sequences.** Facts 1 to 3 are all the proof uses. Any sequence that starts with $f, f'$ and satisfies $c_i f_{i-1} = q_i f_i - d_i f_{i+1}$ with $c_i d_i > 0$ works as well. In particular a positive multiple of each remainder may be used. This lets the computation stay in $\mathbb{Z}[x]$ with [pseudo-division](/pseudo-division/), as long as the multiplier is positive: use $|\operatorname{lc}(f_i)|^{\delta + 1}$ or an even power of $\operatorname{lc}(f_i)$, not $\operatorname{lc}(f_i)^{\delta+1}$ with $\operatorname{lc}(f_i) < 0$ and $\delta$ even. The Sturm-Habicht sequence, based on [subresultants](/subresultant-gcd/), is a sequence of this kind with coefficients of controlled size.

## Examples

**A cubic with three real roots.** Let $f = x^3 - 3x + 1$. Then $f_1 = 3x^2 - 3$, and $f = \tfrac{x}{3} f_1 + (-2x + 1)$ gives $f_2 = 2x - 1$. Next $3x^2 - 3 = (\tfrac{3}{2}x + \tfrac{3}{4})(2x - 1) - \tfrac{9}{4}$ gives $f_3 = \tfrac{9}{4}$, a constant, so $f$ is square-free. The signs are:

| $x$ | $f_0$ | $f_1$ | $f_2$ | $f_3$ | $V(x)$ |
|---|---|---|---|---|---|
| $-\infty$ | $-$ | $+$ | $-$ | $+$ | 3 |
| $-2$ | $-$ | $+$ | $-$ | $+$ | 3 |
| $0$ | $+$ | $-$ | $-$ | $+$ | 2 |
| $1$ | $-$ | $0$ | $+$ | $+$ | 1 |
| $2$ | $+$ | $+$ | $+$ | $+$ | 0 |
| $+\infty$ | $+$ | $+$ | $+$ | $+$ | 0 |

So $f$ has $3 - 0 = 3$ real roots, one in $(-2, 0)$, one in $(0, 1)$ and one in $(1, 2)$. They are $2\cos(8\pi/9) \approx -1.879$, $2\cos(4\pi/9) \approx 0.347$ and $2\cos(2\pi/9) \approx 1.532$. At $x = 1$ the middle term $f_1$ is zero, and its neighbours $-1$ and $1$ have opposite signs, as fact 2 says.

**A repeated root.** Let $f = (x - 1)^2 (x + 1) = x^3 - x^2 - x + 1$. Then $f_1 = 3x^2 - 2x - 1$ and $f_2 = \tfrac{8}{9}(x - 1)$, and the next remainder is zero. The last term is a multiple of $\gcd(f, f') = x - 1$. The signs at $-\infty$ are $-, +, -$ and at $+\infty$ are $+, +, +$, so $V(-\infty) - V(+\infty) = 2$: the sequence counts the two distinct roots $-1$ and $1$, not the three roots with multiplicity.

**The sign matters.** For $f = x^2 - 1$ the Sturm sequence is $x^2 - 1, 2x, 1$, with $V(-\infty) = 2$ and $V(+\infty) = 0$, which is correct. If the remainder $-1$ is kept without the sign change, the list $x^2 - 1, 2x, -1$ gives $V(-\infty) = V(+\infty) = 1$ and a count of zero roots, which is wrong.

**Over $\mathbb{Q}$.** For $f = x^2 - 2$ the sequence is $x^2 - 2, 2x, 2$, and $V(0) - V(2) = 1 - 0 = 1$. The count is the number of roots in $\mathbb{R}$, here $\sqrt 2$, even though $f$ has no root in $\mathbb{Q}$.

## Where it is used

- [Sturm's theorem](/sturm-theorem/): the root count $V(a) - V(b)$ for the distinct real roots in $(a, b]$, for $a$ and $b$ that are not multiple roots.
- [Real root counting](/real-root-counting/) and [real root isolation](/real-root-isolation/): bisection with Sturm counts gives isolating intervals with an exact count at each step.
- [Real root isolation](/real-root-isolation/) by the [Vincent-Collins-Akritas](/vincent-collins-akritas/) method is the main alternative: it replaces the Sturm count by [Descartes' rule of signs](/descartes-rule-of-signs/), which needs no remainder sequence but only bounds the count.
- [Cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/) and [quantifier elimination](/quantifier-elimination/) over the reals: signed remainder and Sturm-Habicht sequences decide the signs of polynomials at real algebraic numbers.
- [Polynomial gcd](/polynomial-gcd/): the last term of the sequence is a multiple of $\gcd(f, f')$, so the same computation tests for repeated roots.

## References
