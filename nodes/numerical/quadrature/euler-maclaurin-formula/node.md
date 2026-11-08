---
tag: CGQKY5
kind: theorem
slug: euler-maclaurin-formula
name: Euler-Maclaurin formula
aliases:
- Euler-Maclaurin summation
- Euler-Maclaurin summation formula
- Euler's summation formula
- Euler-Maclaurin expansion of the trapezoidal rule
area: numerical/quadrature
level: advanced
summary: Relates a sum of a smooth function to its integral plus boundary and correction terms.
prereqs: [trapezoidal-rule, asymptotic-notation]
see_also: [romberg-integration, richardson-extrapolation, composite-quadrature, quadrature-error, peano-kernel-theorem, stirling-approximation, sequence-extrapolation, degree-of-precision]
sources:
  - paper: "Leonhard Euler, Methodus generalis summandi progressiones, Commentarii Academiae Scientiarum Petropolitanae 6 (1738) 68-97"
    locator: the summation formula with the coefficients later called Bernoulli numbers (Eneström index E25)
  - book: "Colin Maclaurin, A Treatise of Fluxions, Edinburgh, 1742"
    locator: Book 2, the independent derivation of the summation formula
  - paper: "Carl Gustav Jacob Jacobi, De usu legitimo formulae summatoriae Maclaurinianae, Journal für die reine und angewandte Mathematik 12 (1834) 263-272"
    locator: the remainder term and the conditions for its use
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Chapter 5, Section 5.4, asymptotic error formulas and the Euler-MacLaurin formula, with Romberg integration
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Chapter 2, the Euler-Maclaurin summation formula and its use for the trapezoidal rule and Romberg integration
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 7, Numerical integration I (the Euler-Maclaurin expansion and Richardson extrapolation)
  - paper: doi:10.1137/130932132
    title: "Lloyd N. Trefethen and J. A. C. Weideman, The exponentially convergent trapezoidal rule, SIAM Review 56(3) (2014) 385-458"
    locator: Sections 2 and 3, the trapezoidal rule for periodic functions and the role of the Euler-Maclaurin formula
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition, Addison-Wesley, 1994
    locator: Section 9.5, Euler's summation formula (the remainder and its use for sums and Stirling's formula)
---

The Euler-Maclaurin formula expresses the error of the [trapezoidal rule](/trapezoidal-rule/) as a series in even powers of the step $h$, whose coefficients are differences of odd derivatives of $f$ at the two endpoints, plus an explicit remainder. Read one way it is a quadrature result: it explains why the trapezoidal rule is $O(h^2)$, why [Richardson extrapolation](/richardson-extrapolation/) of it works ([Romberg integration](/romberg-integration/)), and why it is spectrally accurate for smooth periodic functions. Read the other way it is a summation formula: it turns $\sum_{k} f(k)$ into $\int f$ plus corrections, which gives closed forms for power sums and Stirling's formula for $\log n!$.

## Statement

**Notation.** As on all quadrature pages: $I(f) = \int_a^b f(x)\,dx$ (weight $w = 1$), a rule $Q$, and $E = I - Q$. The composite rule uses $m$ panels of width $h = \frac{b - a}{m}$ with nodes $x_i = a + ih$, and
$$T_h(f) = h\Bigl(\tfrac12 f(x_0) + f(x_1) + \cdots + f(x_{m-1}) + \tfrac12 f(x_m)\Bigr)$$
is the composite trapezoidal rule with $m + 1$ evaluations. The Bernoulli polynomials are defined by $B_0 = 1$, $B_k' = kB_{k-1}$ and $\int_0^1 B_k = 0$ for $k \ge 1$; the Bernoulli numbers are $b_k = B_k(0)$, so $b_1 = -\frac12$, $b_2 = \frac16$, $b_4 = -\frac{1}{30}$, $b_6 = \frac{1}{42}$, $b_8 = -\frac{1}{30}$, and $b_k = 0$ for odd $k \ge 3$. $\tilde B_k(x) = B_k(x - \lfloor x\rfloor)$ is the periodic extension.

**Hypotheses.** $a < b$, $m \ge 1$, $p \ge 1$, and $f \in C^{2p}[a, b]$.

**Theorem.**

1. (Expansion with remainder.)
$$T_h(f) - I(f) = \sum_{k=1}^{p}\frac{b_{2k}h^{2k}}{(2k)!}\bigl(f^{(2k-1)}(b) - f^{(2k-1)}(a)\bigr) + R_p,\qquad R_p = -\frac{h^{2p}}{(2p)!}\int_a^b\tilde B_{2p}\Bigl(\frac{x - a}{h}\Bigr)f^{(2p)}(x)\,dx.$$
2. (Mean value form.) There is $\xi \in [a, b]$ with
$$T_h(f) - I(f) = \sum_{k=1}^{p-1}\frac{b_{2k}h^{2k}}{(2k)!}\bigl(f^{(2k-1)}(b) - f^{(2k-1)}(a)\bigr) + \frac{b_{2p}h^{2p}}{(2p)!}(b - a)f^{(2p)}(\xi).$$
3. (Bound.) In particular $\bigl\lvert T_h(f) - I(f) - \sum_{k=1}^{p-1}\cdots\bigr\rvert \le \frac{\lvert b_{2p}\rvert h^{2p}}{(2p)!}(b - a)\max_{[a, b]}\lvert f^{(2p)}\rvert$.

With $a = 0$, $b = n$ and $h = 1$, part 1 is the summation form
$$\sum_{k=0}^{n}f(k) = \int_0^n f(x)\,dx + \frac{f(0) + f(n)}{2} + \sum_{k=1}^{p}\frac{b_{2k}}{(2k)!}\bigl(f^{(2k-1)}(n) - f^{(2k-1)}(0)\bigr) + R_p.$$

## In plain words

The trapezoidal rule estimates an area by cutting it into thin strips and treating each strip as a trapezoid. This theorem says exactly how wrong that estimate is. The mistake is a sum of terms that get smaller very quickly as the strips get thinner, and each term depends only on how the function bends at the two ends of the interval, not in the middle. That has three uses. You can subtract the first few terms to get a much better answer. You can combine answers from two strip widths so that the largest term cancels. And when the two ends behave in the same way, as for a function that repeats, all these terms vanish and the simple rule is astonishingly accurate. Read backwards, the same identity turns long sums into integrals.

## Proof

The full proof is in [the proof](proofs/main.md). On one panel, write $x = x_i + th$ and $g(t) = f(x_i + th)$, $t \in [0, 1]$. Integration by parts against $B_1(t) = t - \frac12$ gives
$$\frac{g(0) + g(1)}{2} - \int_0^1 g = \int_0^1 B_1g'.$$
Repeated integration by parts, using $B_k' = kB_{k-1}$, $B_k(0) = B_k(1) = b_k$ for $k \ge 2$ and $b_k = 0$ for odd $k \ge 3$, turns the right side into $\sum_{k=1}^{p}\frac{b_{2k}}{(2k)!}\bigl(g^{(2k-1)}(1) - g^{(2k-1)}(0)\bigr) - \frac{1}{(2p)!}\int_0^1B_{2p}g^{(2p)}$. Scaling by $h$, with $g^{(j)} = h^jf^{(j)}$, and summing over the $m$ panels, the interior derivative terms telescope and part 1 follows.

For part 2, move the $k = p$ boundary term into the remainder, which becomes $-\frac{h^{2p}}{(2p)!}\int_a^b\bigl(\tilde B_{2p} - b_{2p}\bigr)f^{(2p)}$. A Rolle argument with the symmetry $B_k(1 - t) = (-1)^kB_k(t)$ shows that $B_{2p}(t) - b_{2p}$ has no zero in $(0, 1)$. So the mean value theorem for integrals applies, and $\int_0^1(B_{2p} - b_{2p}) = -b_{2p}$ gives the factor $b_{2p}$. Part 3 follows from part 2. $\blacksquare$

## Consequences

- **The trapezoidal rule is $O(h^2)$, with a known constant.** With $p = 1$: $T_h(f) - I(f) = \frac{h^2}{12}(b - a)f''(\xi)$. With $p = 2$: $T_h(f) - I(f) = \frac{h^2}{12}\bigl(f'(b) - f'(a)\bigr) + O(h^4)$.
- **Endpoint corrections.** Subtracting the known boundary terms raises the order: by part 2 with $p = 2$, $T_h - \frac{h^2}{12}(f'(b) - f'(a)) - I(f) = -\frac{h^4}{720}(b - a)f^{(4)}(\xi)$. For $\int_0^1 e^x\,dx$ with $m = 4$, the plain rule errs by $8.9 \times 10^{-3}$, and subtracting one, two, three and four correction terms leaves $9.3 \times 10^{-6}$, $1.4 \times 10^{-8}$, $2.2 \times 10^{-11}$ and $3.4 \times 10^{-14}$ (measured). Gregory's formula does the same with finite differences instead of derivatives.
- **[Romberg integration](/romberg-integration/).** Because the error is $c_1h^2 + c_2h^4 + \cdots$ with $c_k$ independent of $h$, the combination $\frac{4T_{h/2} - T_h}{3}$ removes the $h^2$ term (it is Simpson's rule), and repeated [Richardson extrapolation](/richardson-extrapolation/) removes $h^4, h^6, \ldots$ in turn. Part 1 with $p$ terms justifies each step as long as $f \in C^{2p}$.
- **Periodic functions.** If $f$ is $(b - a)$-periodic and $C^{2p}$ on $\mathbb{R}$, every boundary term vanishes and $T_h(f) - I(f) = O(h^{2p})$. For $C^\infty$ periodic $f$ the rule converges faster than any power of $h$, and for analytic periodic $f$ it converges geometrically (Trefethen and Weideman 2014, cited). Measured: for $\int_0^{2\pi}e^{\cos x}\,dx = 2\pi I_0(1)$, $m = 4, 8, 16$ give errors $3.4 \times 10^{-2}$, $1.3 \times 10^{-6}$ and rounding level; the error matches $4\pi I_m(1)$. This is why the trapezoidal rule is the method of choice for periodic integrands and the basis of [tanh-sinh](/tanh-sinh-quadrature/) quadrature.
- **Power sums.** For $f(x) = x^r$, $f^{(2p)} = 0$ once $2p > r$, so the formula is exact and gives Faulhaber's closed forms, for example $\sum_{k=0}^{n}k^2 = \frac{n^3}{3} + \frac{n^2}{2} + \frac{n}{6}$.
- **Stirling's formula.** With $f = \log x$ on $[1, n]$, the formula gives $\log n! = n\log n - n + \frac12\log n + C + \frac{1}{12n} - \frac{1}{360n^3} + \cdots$, where Wallis's product identifies $C = \frac12\log 2\pi$. At $n = 10$, stopping after the $\frac{1}{360n^3}$ term leaves an error of $7.9 \times 10^{-9}$. See [Stirling's approximation](/stirling-approximation/).

## Tightness

- **The remainder is sharp.** For a polynomial of degree $2p$, $f^{(2p)}$ is constant and part 2 holds with any $\xi$. With $f = x^2$ on $[0, 1]$ and $m = 1$: $T_h - I = \frac12 - \frac13 = \frac16 = \frac{b_2}{2!}\cdot 2$. With $f = x^6$, $m = 3$ and $p = 3$, both sides equal $\frac{1639}{30618}$ (checked in rational arithmetic).
- **The series is asymptotic, not convergent.** $\lvert b_{2k}\rvert$ grows like $\frac{2(2k)!}{(2\pi)^{2k}}$, so for fixed $h$ the terms eventually grow unless the derivatives of $f$ grow slowly enough. For $f = \frac1x$ on $[1, 2]$ with $h = 1$, the terms have sizes $6.2 \times 10^{-2}$, $7.8 \times 10^{-3}$, $3.9 \times 10^{-3}$, $4.2 \times 10^{-3}$, $7.6 \times 10^{-3}$, $2.1 \times 10^{-2}$, then grow without bound. The theorem is a statement for each fixed $p$, as $h \to 0$.
- **Zero corrections do not mean zero error.** For periodic $f$ all boundary terms vanish, yet the error of $e^{\cos x}$ with $m = 4$ is $3.4 \times 10^{-2}$. The error is entirely in $R_p$, and the formula only says that $R_p = O(h^{2p})$ for every $p$.
- **Smoothness is needed.** For $f = \sqrt x$ on $[0, 1]$, $f'$ is unbounded at $0$, the hypotheses fail for every $p \ge 1$, and the error of the trapezoidal rule is $\Theta(h^{3/2})$, not $O(h^2)$. Expansions with fractional powers (Navot's extension) cover such endpoint singularities.

## History

Euler found the formula around 1732 and published it in 1738, and soon used it to evaluate slowly convergent series such as $\sum 1/k^2$ to many digits. Maclaurin derived it independently and published it in his *Treatise of Fluxions* in 1742. Neither gave a usable remainder; Poisson and then Jacobi (1834) supplied it, and Jacobi's paper made clear when the series may be used. The coefficients are the numbers Jacob Bernoulli had found in 1713 in his sums of powers. In numerical analysis the formula became central with Romberg's method (1955), which is Richardson extrapolation built on it, and with the modern understanding of the trapezoidal rule's exponential accuracy for periodic and decaying integrands.

## References
