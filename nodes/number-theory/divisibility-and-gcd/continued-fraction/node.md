---
tag: YA71YH
kind: concept
slug: continued-fraction
name: Continued fraction
aliases:
- Continued fractions
area: number-theory/divisibility-and-gcd
level: core
summary: Represents a real number as a sequence of integer partial quotients, a nested fraction that gives rational approximations.
prereqs: [euclidean-algorithm]
see_also: [continued-fraction-convergents, stern-brocot-tree, farey-sequence, pell-equation, rational-approximation, extended-euclidean-algorithm, wiener-attack, continued-fraction-factorization]
sources:
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 10, Continued fractions (finite and infinite expansions, uniqueness, periodic expansions of quadratic irrationals), and Chapter 11 (approximation of irrationals by rationals)
  - book: isbn:9780486696300
    title: A. Ya. Khinchin, Continued Fractions, Dover edition
    locator: Chapter I (properties of the apparatus), Chapter II (representation of numbers by continued fractions), Chapter III (the measure theory of continued fractions)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.5.3, Analysis of Euclid's algorithm (continued fractions, continuants, and the Gauss-Kuzmin distribution of partial quotients)
---

A continued fraction writes a number as an integer plus the reciprocal of a number that is again written the same way:

$$x = a_0 + \cfrac{1}{a_1 + \cfrac{1}{a_2 + \cfrac{1}{a_3 + \cdots}}},$$

shortened to $x = [a_0; a_1, a_2, a_3, \ldots]$. The integers $a_i$ are the *partial quotients*, with $a_0 \in \mathbb{Z}$ and $a_i \ge 1$ for $i \ge 1$. Each real number has such an expansion; it is finite exactly when the number is rational, and then the partial quotients are the quotients of the [Euclidean algorithm](/euclidean-algorithm/). Cutting the expansion short gives the [convergents](/continued-fraction-convergents/), fractions that approximate $x$ better than any other fraction with a denominator as small. This makes continued fractions the tool for [rational approximation](/rational-approximation/), for the [Pell equation](/pell-equation/), and for the analysis of the Euclidean algorithm itself.

## In plain words

Take a number and split off its whole part. What is left is less than one, so turn it upside down to get a number larger than one, and split off its whole part again. Repeat. The list of whole parts is the continued fraction of the number.

For a fraction of two whole numbers this is the same as dividing with remainder again and again, so the list is short and ends. For a number like the square root of two, the list goes on forever, and it repeats.

The list is useful because stopping early gives a simple fraction that is very close to the number. A large whole part in the list means the fraction just before it is especially good. This is how people found that three hundred fifty-five over one hundred thirteen is a very good value for pi.

## The idea

**The expansion.** For a real $x$, set $x_0 = x$ and, for $k \ge 0$,

$$a_k = \lfloor x_k \rfloor, \qquad x_{k+1} = \frac{1}{x_k - a_k} \quad \text{if } x_k \ne a_k.$$

The process stops if some $x_k$ is an integer. Each $x_{k+1} > 1$, so $a_{k+1} \ge 1$. The value $x_k$ is the *complete quotient*, and $x = [a_0; a_1, \ldots, a_{k-1}, x_k]$ holds exactly at every step.

**Rational numbers and the Euclidean algorithm.** If $x = p/q$ with $q > 0$, then $x_k$ is a ratio $r_{k-1}/r_k$ of consecutive remainders of the Euclidean algorithm on $(p, q)$, and $a_k$ is the quotient of that division step. The remainders reach zero, so the expansion of a rational number is finite, with as many terms as the Euclidean algorithm has division steps. Conversely a finite expansion is a rational number. So a number is rational if and only if its continued fraction is finite.

**Uniqueness.** A rational number has exactly two expansions, because the last term can be split: $[a_0; \ldots, a_n] = [a_0; \ldots, a_n - 1, 1]$ when $a_n \ge 2$. The *canonical* expansion is the one whose last term is at least $2$ (or that has the single term $a_0$). An irrational number has exactly one expansion, and it is infinite. Two different canonical expansions give different numbers, so the expansion is a code for the real numbers.

**Infinite expansions converge.** For any integers $a_0$ and $a_1, a_2, \ldots \ge 1$, the finite values $[a_0; a_1, \ldots, a_n]$ tend to a limit, and that limit is irrational with exactly this expansion. The finite values are the convergents $p_n / q_n$, computed by

$$p_n = a_n p_{n-1} + p_{n-2}, \qquad q_n = a_n q_{n-1} + q_{n-2},$$

from $p_{-1} = 1, p_{-2} = 0, q_{-1} = 0, q_{-2} = 1$. They lie alternately below and above $x$, and $|x - p_n/q_n| < 1/(q_n q_{n+1})$. The [convergents](/continued-fraction-convergents/) page proves these facts.

**Matrix form.** In terms of $2 \times 2$ integer matrices,

$$\begin{pmatrix} a_0 & 1 \\ 1 & 0 \end{pmatrix} \begin{pmatrix} a_1 & 1 \\ 1 & 0 \end{pmatrix} \cdots \begin{pmatrix} a_n & 1 \\ 1 & 0 \end{pmatrix} = \begin{pmatrix} p_n & p_{n-1} \\ q_n & q_{n-1} \end{pmatrix}.$$

Each factor has determinant $-1$, so $p_n q_{n-1} - p_{n-1} q_n = (-1)^{n+1}$. This form underlies the [extended Euclidean algorithm](/extended-euclidean-algorithm/), [Lehmer's GCD](/lehmers-gcd/) and the [half-GCD](/half-gcd/).

**Periodic expansions.** An expansion is *eventually periodic* if from some point on the partial quotients repeat with a fixed period. Euler showed that a periodic expansion is a quadratic irrational, a root of an integer quadratic equation that is not rational, and Lagrange proved the converse: each quadratic irrational has an eventually periodic expansion. For a positive integer $N$ that is not a square,

$$\sqrt N = [a_0; \overline{a_1, a_2, \ldots, a_2, a_1, 2a_0}],$$

with $a_0 = \lfloor \sqrt N \rfloor$, a period that ends in $2a_0$, and a symmetric part before it. The convergents at the end of each period solve the [Pell equation](/pell-equation/) $x^2 - N y^2 = \pm 1$.

**Typical numbers.** For almost every real number in the sense of measure, the partial quotients follow the *Gauss-Kuzmin distribution*: the proportion of $k$ with $a_k = j$ tends to $\log_2 (1 + 1/(j(j + 2)))$. So about $41.5\%$ of the partial quotients are $1$ and about $17\%$ are $2$. Khinchin proved that the geometric mean of $a_1, \ldots, a_n$ tends to a constant $K \approx 2.6855$ for almost every $x$, and Lévy that $q_n^{1/n}$ tends to $e^{\pi^2 / (12 \ln 2)} \approx 3.2758$. The same distribution describes the quotients of the Euclidean algorithm on random inputs, which is how its average number of steps is found.

**Generalized continued fractions.** Allowing numerators other than $1$, as in $b_0 + a_1/(b_1 + a_2/(b_2 + \cdots))$, gives expansions of functions such as $\tan x$ and $\arctan x$, used in numerical analysis ([Padé approximation](/pade-approximation/), [Thiele interpolation](/thiele-continued-fraction-interpolation/)). This page is about the simple form with all numerators $1$.

## Examples

**A fraction.** $415/93$: the Euclidean algorithm gives $415 = 4 \cdot 93 + 43$, $93 = 2 \cdot 43 + 7$, $43 = 6 \cdot 7 + 1$, $7 = 7 \cdot 1$. So

$$\frac{415}{93} = [4; 2, 6, 7] = 4 + \cfrac{1}{2 + \cfrac{1}{6 + \cfrac{1}{7}}}.$$

The other expansion is $[4; 2, 6, 6, 1]$. The convergents are $4$, $9/2$, $58/13$ and $415/93$.

**The square root of 2.** Since $\sqrt 2 - 1 = 1/(\sqrt 2 + 1)$ and $\sqrt 2 + 1 = 2 + (\sqrt 2 - 1)$, each complete quotient after the first is $\sqrt 2 + 1$, and

$$\sqrt 2 = [1; 2, 2, 2, \ldots] = [1; \overline{2}].$$

The convergents $1, 3/2, 7/5, 17/12, 41/29, \ldots$ alternate around $\sqrt 2 \approx 1.41421$.

**Other quadratic irrationals.** The golden ratio is $\varphi = (1 + \sqrt 5)/2 = [1; \overline{1}]$, the expansion with the smallest possible partial quotients, so it is the hardest number to approximate by fractions; its convergents are ratios of consecutive [Fibonacci numbers](/fibonacci-numbers/). Further, $\sqrt 3 = [1; \overline{1, 2}]$, $\sqrt{13} = [3; \overline{1, 1, 1, 1, 6}]$ and $\sqrt{14} = [3; \overline{1, 2, 1, 6}]$. For $N = 13$ the period has odd length $5$, and the convergent at the end of the second period, $649/180$, gives $649^2 - 13 \cdot 180^2 = 1$.

**$\pi$ and $e$.**

$$\pi = [3; 7, 15, 1, 292, 1, 1, 1, 2, 1, 3, 1, 14, 2, 1, \ldots], \qquad e = [2; 1, 2, 1, 1, 4, 1, 1, 6, 1, 1, 8, \ldots].$$

No pattern is known for $\pi$. The convergents of $\pi$ are $3$, $22/7$, $333/106$, $355/113$, $103993/33102$, and so on. The large partial quotient $292$ comes right after $355/113$, which is why this fraction is so good: $|\pi - 355/113| < 3 \cdot 10^{-7}$. The expansion of $e$ has the regular pattern $1, 2k, 1$, found by Euler.

**A calendar.** The tropical year is about $365.24219$ days. The fractional part is $0.24219 = [0; 4, 7, 1, 3, \ldots]$, with convergents $1/4$, $7/29$, $8/33$ and $31/128$. The first gives the Julian calendar, one leap day every four years, and $8/33$ gives a cycle of eight leap days in 33 years, used in some Persian calendars.

**Musical scales.** The perfect fifth has frequency ratio $3/2$, and $\log_2(3/2) = [0; 1, 1, 2, 2, 3, 1, \ldots]$, with convergents $1/2$, $3/5$, $7/12$, $24/41$, $31/53$. The convergent $7/12$ says that seven steps of a scale of twelve equal steps make a good fifth, which is the scale of Western music; $31/53$ explains the 53-step scale.

| number | expansion | first convergents |
|---|---|---|
| $415/93$ | $[4; 2, 6, 7]$ | $4, 9/2, 58/13, 415/93$ |
| $\sqrt 2$ | $[1; \overline{2}]$ | $1, 3/2, 7/5, 17/12$ |
| $\varphi$ | $[1; \overline{1}]$ | $1, 2, 3/2, 5/3, 8/5$ |
| $\sqrt{14}$ | $[3; \overline{1, 2, 1, 6}]$ | $3, 4, 11/3, 15/4$ |
| $\pi$ | $[3; 7, 15, 1, 292, \ldots]$ | $3, 22/7, 333/106, 355/113$ |
| $e$ | $[2; 1, 2, 1, 1, 4, \ldots]$ | $2, 3, 8/3, 11/4, 19/7$ |

**Computing in floating point.** The steps $x_{k+1} = 1/(x_k - a_k)$ magnify rounding errors at each step. Starting from the double-precision value of $\pi$, the expansion is correct only for its first 13 terms; the fourteenth comes out as $3$ instead of $2$. To expand a real number reliably, use exact rational or high-precision arithmetic, or bound the error with two rational endpoints and stop when their expansions disagree.

## Where it is used

- **Best rational approximation.** The convergents are the best approximations of $x$ for their size of denominator, and fractions with $|x - p/q| < 1/(2q^2)$ are always convergents. See [rational approximation](/rational-approximation/) and [convergents](/continued-fraction-convergents/).
- **Analysis of the Euclidean algorithm.** The number of steps of the [Euclidean algorithm](/euclidean-algorithm/) is the length of a continued fraction, the worst case comes from $[1; 1, \ldots, 1]$ (Fibonacci numbers, [Lamé's theorem](/lames-theorem/)), and the average comes from the Gauss-Kuzmin distribution.
- **The Pell equation.** The periodic expansion of $\sqrt N$ gives the smallest solution of $x^2 - N y^2 = 1$; see [Pell equation](/pell-equation/).
- **Factoring.** The [continued fraction factorization](/continued-fraction-factorization/) method (CFRAC) uses the convergents of $\sqrt N$ to find small squares modulo $N$.
- **Cryptanalysis.** [Wiener's attack](/wiener-attack/) on RSA recovers a small private exponent $d$ as the denominator of a convergent of $e/N$.
- **Quantum period finding.** In [Shor's algorithm](/shor-algorithm/), the measured value is turned into a period by the [continued fraction post-processing](/continued-fraction-post-processing/) step.
- **Trees of fractions.** The path to a fraction in the [Stern-Brocot tree](/stern-brocot-tree/) and in the [Calkin-Wilf tree](/calkin-wilf-tree/) is its continued fraction written as runs of left and right moves; neighbours in the [Farey sequence](/farey-sequence/) are linked to the same expansions.
- **Words and geometry.** The digitized straight lines of slope $\alpha$, the [Sturmian words](/sturmian-word/), are built from the continued fraction of $\alpha$; so are gear ratios, calendars and the tuning of musical scales.

## References
