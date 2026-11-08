---
tag: 288J76
kind: technique
slug: richardson-extrapolation
name: Richardson extrapolation
aliases:
- Richardson's extrapolation
- deferred approach to the limit
- extrapolation to the limit
- h-squared extrapolation
area: numerical/quadrature
level: advanced
summary: Combine approximations at different step sizes to cancel the leading error term.
prereqs: [quadrature-error, asymptotic-notation]
see_also: [romberg-integration, euler-maclaurin-formula, neville-algorithm, sequence-extrapolation, aitken-delta-squared, bulirsch-stoer-method, trapezoidal-rule, finite-differences]
sources:
  - paper: doi:10.1098/rsta.1927.0008
    title: Lewis Fry Richardson and J. Arthur Gaunt, The deferred approach to the limit, Philosophical Transactions of the Royal Society A 226, 1927, 299-361
    locator: Part I (Richardson), the method with h^2 and h^4 terms
  - paper: doi:10.1098/rsta.1911.0009
    title: Lewis Fry Richardson, The approximate arithmetical solution by finite differences of physical problems involving differential equations, Philosophical Transactions of the Royal Society A 210, 1911, 307-357
    locator: the first use of the h^2 extrapolation for finite difference solutions
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Section 1.15, Extrapolation and speed-up; Section 6.3, Romberg integration
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Chapter 5, Section 5.4, Asymptotic error formulas and their applications (Richardson extrapolation and Romberg integration)
  - book: "Claude Brezinski and Michela Redivo Zaglia, Extrapolation Methods, Theory and Practice, North-Holland, 1991"
    locator: Chapter 2, Section 2.2 (the Richardson process and its convergence)
---

Richardson extrapolation turns a sequence of approximations $A(h)$ with a known form of error, $A(h) = A + c_1 h^{p_1} + c_2 h^{p_2} + \cdots$, into a sequence that converges faster. Computing $A$ at two step sizes $h$ and $h/r$ and taking the combination $\big(r^{p_1} A(h/r) - A(h)\big)/(r^{p_1} - 1)$ cancels the term $c_1 h^{p_1}$, without knowing $c_1$. Repeating the step removes one term after another. Applied to the [trapezoidal rule](/trapezoidal-rule/), whose error has an expansion in even powers of $h$ by the [Euler-Maclaurin formula](/euler-maclaurin-formula/), it is [Romberg integration](/romberg-integration/); applied to difference quotients, finite difference solutions or ODE integrators, it raises their order in the same way.

## In plain words

Suppose a method gets closer to the right answer as a step size shrinks, and its mistake shrinks in a known pattern, for example four times smaller each time the step is halved. Then two runs with different steps tell you both the answer and the mistake: the change between the two runs is about three times the remaining mistake of the finer run. Add that correction and most of the mistake is gone.

The corrected values also follow a pattern, with a smaller mistake that shrinks faster, so you can repeat the trick on them. Each round costs only one more run at a smaller step and a few additions. The trick depends entirely on knowing the pattern of the mistake. If the pattern is wrong, the correction can make things worse.

## When it applies

The technique needs an approximation $A(h)$, computable for a decreasing sequence of steps, with an asymptotic error expansion of known exponents:

$$A(h) = A + c_1 h^{p_1} + c_2 h^{p_2} + \cdots + c_K h^{p_K} + O(h^{p_{K+1}}), \qquad 0 < p_1 < p_2 < \cdots < p_{K+1},$$

where the $c_k$ do not depend on $h$ and may be unknown. Typical sources of such expansions:

- The composite trapezoidal and midpoint rules for $f \in C^{2K+2}[a, b]$: $p_k = 2k$, by the Euler-Maclaurin formula.
- The central difference $\big(f(x + h) - f(x - h)\big)/(2h)$ for $f'(x)$: $p_k = 2k$, by Taylor's theorem; the one-sided difference has $p_k = k$.
- Symmetric one-step ODE methods, such as the modified midpoint method in the [Bulirsch-Stoer method](/bulirsch-stoer-method/): an expansion in $h^2$.
- Integrands with algebraic endpoint singularities, where the trapezoidal expansion contains known non-integer powers $h^{1 + \beta}$, $h^{2 + \beta}, \ldots$ besides the even powers (Navot's extension of Euler-Maclaurin).

## The template

```pseudo id=main
RICHARDSON(A, h_0, r, p_1..p_K)        ▷ A(h): the base approximation; r > 1: the step ratio
L1  for i ← 0 to K do
L2      T[i, 0] ← A(h_0 / r^i)
L3  for k ← 1 to K do
L4      for i ← k to K do
L5          T[i, k] ← T[i, k−1] + (T[i, k−1] − T[i−1, k−1]) / (r^(p_k) − 1)
L6  return T[K, K], with |T[K, K] − T[K, K−1]| as an error estimate
```

The holes are the base method $A$, the step ratio $r$ (usually 2) and the exponents $p_k$, which must come from an analysis of $A$.

**Why it works.** Line L5 is $T[i, k] = \big(r^{p_k} T[i, k-1] - T[i-1, k-1]\big)/(r^{p_k} - 1)$. With $h_i = h_0 r^{-i}$, so that $h_{i-1} = r h_i$, a term $c\,h^{p}$ present in column $k - 1$ becomes

$$\frac{r^{p_k} c\,h_i^{p} - c\,(r h_i)^{p}}{r^{p_k} - 1} = c\,\frac{r^{p_k} - r^{p}}{r^{p_k} - 1}\, h_i^{p},$$

which is 0 for $p = p_k$ and is a constant multiple of $h_i^p$ otherwise, while a constant $A$ is kept, since the coefficients $\frac{r^{p_k}}{r^{p_k} - 1}$ and $\frac{-1}{r^{p_k} - 1}$ add to 1. By induction on $k$:

**Theorem.** Under the expansion above, for $0 \le k \le K$ and $i \ge k$,

$$T[i, k] = A + \sum_{j = k+1}^{K} c_j^{(k)} h_i^{p_j} + O(h_i^{p_{K+1}}), \qquad c_j^{(k)} = c_j \prod_{l=1}^{k} \frac{r^{p_l} - r^{p_j}}{r^{p_l} - 1}.$$

In particular $T[i, k] - A = O(h_i^{p_{k+1}})$ as $i \to \infty$. *Proof.* For $k = 0$ it is the hypothesis. Assume it for $k - 1$. Apply the computation above to each term of $T[i, k-1]$ and $T[i-1, k-1]$: the $h^{p_k}$ term cancels, each $c_j^{(k-1)} h^{p_j}$ with $j > k$ is multiplied by $(r^{p_k} - r^{p_j})/(r^{p_k} - 1)$, and the two remainders $O(h_i^{p_{K+1}})$ and $O((r h_i)^{p_{K+1}})$ combine into $O(h_i^{p_{K+1}})$ with coefficients $\frac{r^{p_k}}{r^{p_k} - 1}$ and $\frac{1}{r^{p_k} - 1}$. $\square$

The result is asymptotic: it says how fast the error falls as $h_0 \to 0$, not how large it is for a given $h_0$. The error estimate of line L6 is also asymptotic. It is the difference of two values, the less accurate one with error $O(h_K^{p_K})$, so for small $h$ it overestimates the error of $T[K, K]$.

**Interpretation.** When $p_k = k\,p$, the value $T[i, k]$ is the value at $t = 0$ of the polynomial in $t = h^{p}$ of degree $k$ through the points $(h_{i-j}^p, A(h_{i-j}))$, $j = 0, \ldots, k$, and line L5 is [Neville's algorithm](/neville-algorithm/) for evaluating it at 0. Richardson extrapolation is polynomial extrapolation to $h = 0$ in the variable $h^p$.

**Stability.** $T[K, K] = \sum_i \gamma_i A(h_i)$ with $\sum_i \gamma_i = 1$. Errors in the $A(h_i)$, such as rounding, are amplified by at most $\sum_i |\gamma_i|$. For $r = 2$ and $p_k = 2k$ this sum is $1.667, 1.889, 1.949, 1.964$ for $K = 1, \ldots, 4$ and stays below $1.97$ for all $K$ computed up to 10, so Romberg is stable. For $p_k = k$ it grows: $3, 5, 6.43, 7.29$ for $K = 1, \ldots, 4$.

## Classic examples

- **[Romberg integration](/romberg-integration/).** The base method is the composite trapezoidal rule with $h_i = (b - a)/2^i$, $r = 2$, $p_k = 2k$. The first extrapolated column is the composite [Simpson's rule](/simpsons-rule/), the second is the composite Boole rule, and later columns are not [Newton-Cotes](/newton-cotes-formulas/) rules.
- **Numerical differentiation.** The central difference has an expansion in $h^2$, and extrapolating it removes the step-size dilemma between truncation and rounding; the worked table follows the list.
- **The Bulirsch-Stoer method.** The [Bulirsch-Stoer method](/bulirsch-stoer-method/) extrapolates the modified midpoint method for ODEs in $h^2$, with a sequence of steps $H/n_i$ and polynomial or rational extrapolation.
- **Finite difference solutions of PDEs.** Richardson (1911) solved a boundary value problem with the 5-point difference scheme at two mesh sizes and extrapolated in $h^2$; the same is done with the [finite difference method](/finite-difference-method/) today.
- **Archimedes and Huygens.** The perimeters of inscribed regular polygons with $n$ sides satisfy $P_n = 2\pi - c_1 n^{-2} + c_2 n^{-4} - \cdots$. Huygens (1654) combined $P_n$ and $P_{2n}$ in essentially Richardson's way to get far more digits of $\pi$ than Archimedes.

**Worked example.** For $f(x) = e^x$ at $x = 0$, $D(h) = \sinh(h)/h$ is the central difference, with exact value 1. With $h_0 = 0.4$, $r = 2$, $p_k = 2k$, the errors are:

| $h$ | $T[i,0] - 1$ | $T[i,1] - 1$ | $T[i,2] - 1$ | $T[i,3] - 1$ |
|---|---|---|---|---|
| 0.4 | $2.69 \times 10^{-2}$ | | | |
| 0.2 | $6.68 \times 10^{-3}$ | $-5.36 \times 10^{-5}$ | | |
| 0.1 | $1.67 \times 10^{-3}$ | $-3.34 \times 10^{-6}$ | $1.27 \times 10^{-8}$ | |
| 0.05 | $4.17 \times 10^{-4}$ | $-2.08 \times 10^{-7}$ | $1.99 \times 10^{-10}$ | $-4.4 \times 10^{-13}$ |
| 0.025 | $1.04 \times 10^{-4}$ | $-1.30 \times 10^{-8}$ | $3.10 \times 10^{-12}$ | $-1.1 \times 10^{-16}$ |

The columns fall by factors of about 4, 16 and 64 per row, as the theorem predicts. The plain central difference reaches its best error, about $10^{-11}$, near $h = 10^{-5}$, and gets worse for smaller $h$ because rounding in $f(x + h) - f(x - h)$ grows like $u/h$. Extrapolation from large steps avoids that floor.

## Variations

- **Unknown exponent.** If $p_1$ is unknown, three values give an estimate: $r^{p_1} \approx \frac{A(h) - A(h/r)}{A(h/r) - A(h/r^2)}$. Eliminating $p_1$ and $c_1$ together is [Aitken's delta-squared process](/aitken-delta-squared/), a [sequence extrapolation](/sequence-extrapolation/) method.
- **Non-geometric steps.** Steps $h_i$ in any decreasing sequence work with the Neville form; Bulirsch used $h/2, h/3, h/4, h/6, \ldots$ to reduce the number of evaluations.
- **Rational extrapolation.** Extrapolating by a rational function of $h^2$ instead of a polynomial (Bulirsch and Stoer, 1964) is sometimes more robust.
- **Repeated Richardson in one step.** With a single pair of steps and a known $p_1$, the correction $\big(A(h/r) - A(h)\big)/(r^{p_1} - 1)$ alone serves as an error estimate for $A(h/r)$, as in [adaptive quadrature](/adaptive-quadrature/), where the Simpson error estimate is $(S_{2m} - S_m)/15$.

## Pitfalls

- **The expansion does not exist.** For $\int_0^1 \sqrt{x}\,dx$ the trapezoidal error has a term in $h^{3/2}$, not $h^2$, and extrapolating with $p_1 = 2$ gains almost nothing. For non-smooth integrands, or functions with a kink inside the interval, the hypothesis fails and the columns do not improve.
- **A periodic integrand.** For a smooth periodic function over a period, the trapezoidal coefficients $c_k$ all vanish and the error is already exponentially small; extrapolation adds rounding and no accuracy.
- **Steps too large.** The theorem is about $h \to 0$. If $h_0$ is not in the asymptotic range, the terms dropped are not small and the extrapolated values can be worse than the base values. The ratios of successive differences in each column, which should approach $r^{p_k}$, are a cheap check.
- **Too many columns.** Each column needs $f$ to be smoother, and in floating point the later columns only add rounding. Stop when the estimate of line L6 stops falling.
- **Trusting the estimate as a bound.** $|T[K,K] - T[K, K-1]|$ is an asymptotic estimate. It can be fooled like any estimate computed from samples, as on the [quadrature error](/quadrature-error/) page.

## Exercises

1. For the trapezoidal rule $T(h)$ with $h_0 = b - a$, show that $T[1, 1] = (4 T(h/2) - T(h))/3$ is Simpson's rule on two subintervals.
2. Derive the extrapolation step for step ratio $r = 3$ and $p_1 = 2$, and check it on $D(h) = \sinh(h)/h$.
3. For $f(x) = \sqrt{x}$ on $[0, 1]$, compute the trapezoidal values for $h = 2^{-i}$ and estimate the leading exponent from three of them as in the variation above. Then extrapolate with that exponent.

## References
