---
tag: 3C5CRR
kind: algorithm
slug: aitken-delta-squared
name: Aitken's delta-squared process
aliases:
- Aitken acceleration
- Aitken extrapolation
- Aitken's Δ² process
area: numerical/interpolation-and-approximation
level: advanced
summary: Replace s_k by s_{k+2} - (Δs_{k+1})^2 / Δ²s_k. Exact when the error is geometric, and faster in the limit whenever s_{k+1} - s ≈ λ (s_k - s) with λ ≠ 1. Useless for logarithmic convergence.
solves: [sequence-extrapolation]
model: real-ram
complexity:
  vars: {N: "the index of the last term used, with N + 1 terms"}
  time: {total: Θ(N)}
  space: {extra: Θ(1)}
  flops: {per_output: "6"}
properties: {deterministic: true, recursive: false, nonlinear: true, exact_on: "s + c λ^k with c ≠ 0 and λ ≠ 0 or 1"}
history:
  year: 1926
  people: [Alexander C. Aitken, Seki Takakazu, Daniel Shanks, Peter Wynn, Peter Henrici]
  note: Aitken introduced the process in 1926 to accelerate Bernoulli's method for polynomial roots; Seki had used an equivalent step for π around 1680; Shanks (1955) and Wynn (1956) generalized it.
prereqs: [order-of-convergence, finite-differences]
see_also: [steffensen-method, fixed-point-iteration, richardson-extrapolation, sequence-extrapolation, pade-approximation, power-iteration, romberg-integration, catastrophic-cancellation]
sources:
  - paper: doi:10.1017/S0370164600022070
    title: "A. C. Aitken, On Bernoulli's numerical solution of algebraic equations, Proceedings of the Royal Society of Edinburgh 46 (1926) 289-305"
    locator: the δ² process applied to the ratios of Bernoulli's method
  - book: isbn:9780444888143
    title: Claude Brezinski and Michela Redivo Zaglia, Extrapolation Methods, Theory and Practice, North-Holland, 1991
    locator: Chapter 2, the Δ² process (acceleration theorems for linear convergence, the logarithmic case) and its relation to the Shanks transformation and the ε-algorithm
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Section 2.6, Aitken extrapolation for linearly convergent sequences
  - book: isbn:9780521450072
    title: George A. Baker Jr. and Peter Graves-Morris, Padé Approximants, second edition, Cambridge University Press, 1996
    locator: Chapter 3, the ε-algorithm and Shanks's transformation as Padé approximants of power series
  - paper: "Daniel Shanks, Non-linear transformations of divergent and slowly convergent sequences, Journal of Mathematics and Physics 34 (1955) 1-42"
    locator: the e_k transformations, of which Aitken's process is e_1
  - paper: "J. P. Delahaye and B. Germain-Bonnet, Résultats négatifs en accélération de la convergence, Numerische Mathematik 35 (1980) 443-457"
    locator: no algorithm accelerates all logarithmically convergent sequences
---

Aitken's $\Delta^2$ process turns a sequence $s_0, s_1, s_2, \ldots$ with limit $s$ into a new sequence
$$t_k = s_{k+2} - \frac{(\Delta s_{k+1})^2}{\Delta^2 s_k} = s_{k+2} - \frac{(s_{k+2} - s_{k+1})^2}{(s_{k+2} - s_{k+1}) - (s_{k+1} - s_k)},$$
which is the limit of the geometric sequence that matches $s_k, s_{k+1}, s_{k+2}$. If the error is exactly geometric, $s_k = s + c\lambda^k$, then $t_k = s$. If the error is geometric only in the limit, $s_{k+1} - s = (\lambda + o(1))(s_k - s)$ with $\lambda \ne 1$, then $(t_k - s)/(s_k - s) \to 0$: the new sequence converges faster. This covers linearly convergent iterations and alternating series. It does not help logarithmic convergence ($\lambda = 1$), where it gains only a constant factor. Each $t_k$ costs 6 arithmetic operations, but the second difference in the denominator suffers [cancellation](/catastrophic-cancellation/), so the formula must be written in a stable form and applied before the terms have converged to rounding level.

## In plain words

Many iterations creep toward their answer, closing the same fraction of the remaining gap at every step. If you see three consecutive values, you can work out that fraction and jump straight to where the creeping would end. That is all Aitken's process does: from three terms, it guesses the limit as if the errors shrank by exactly the same ratio each time.

When the errors really shrink by a nearly constant ratio, the guess is much better than the last term, and doing it again on the guesses improves things further. When the errors shrink more and more slowly, like $1/k$, the ratio tends to 1, the guess is poor, and the trick fails.

## The problem

The input is terms $s_0, \ldots, s_N$ of a sequence, numbers in a field (real, complex, or exact rationals), believed to converge to an unknown $s$. The output is a new sequence $t_0, \ldots, t_{N-2}$ that should approach $s$ faster, in the sense $(t_k - s)/(s_k - s) \to 0$. No transformation can do this for every convergent sequence, so each method is designed for a class of error behaviour; for Aitken's process the class is errors that are asymptotically geometric.

Notation on the interpolation and approximation pages: for sequence acceleration $s_k$ are the terms (often partial sums) with limit $s$, $e_k = s_k - s$ the errors, $\Delta s_k = s_{k+1} - s_k$ and $\Delta^2 s_k = \Delta s_{k+1} - \Delta s_k$. Costs are arithmetic operations on the [real RAM](/real-ram/).

## The algorithm

```pseudo id=main
AITKEN(s[0 .. N])
L1  for k ← 0 to N − 2
L2      a ← s[k+1] − s[k]
L3      b ← s[k+2] − s[k+1]
L4      d ← b − a                                ▷ the second difference Δ²s[k]
L5      if d = 0: t[k] ← s[k+2] if b = 0, else undefined
L6      else t[k] ← s[k+2] − b² / d
```

If $d = 0$ and $b = 0$, the three terms are equal and the sequence has locally converged. If $d = 0$ and $b \ne 0$, the terms are in arithmetic progression and the geometric model has ratio 1 and no finite limit. **Iterated Aitken** applies the process again to $t$, and so on, building a triangular table; each pass shortens the sequence by 2.

## Example

**Leibniz series.** The partial sums of $1 - \frac13 + \frac15 - \cdots = \frac{\pi}{4} \approx 0.785398$ start $s_0 = 1$, $s_1 = \frac23$, $s_2 = \frac{13}{15}$. Then $a = -\frac13$, $b = \frac15$, $d = \frac{8}{15}$, $b^2/d = \frac{3}{40}$, and
$$t_0 = \frac{13}{15} - \frac{3}{40} = \frac{19}{24} \approx 0.791667,$$
with error $6.3 \times 10^{-3}$, against $8.1 \times 10^{-2}$ for $s_2$. Applying the process repeatedly, with exact arithmetic and errors converted to double precision:

| $k$ | $s_k$ | $t_k$ (once) | twice | three times |
|---|---|---|---|---|
| 0 | 2.15e-1 | 6.27e-3 | 1.28e-4 | 1.68e-6 |
| 2 | 8.13e-2 | 9.11e-4 | 1.27e-5 | 1.44e-7 |
| 4 | 4.95e-2 | 2.80e-4 | 2.55e-6 | 2.25e-8 |

The row for $k$ uses the terms $s_k, \ldots, s_{k + 2j}$ for $j$ passes. With 7 terms, three passes give 6 correct digits where the plain partial sum has 1.

**Fixed-point iteration.** For $x_{k+1} = \cos x_k$ from $x_0 = 1$, the errors shrink by about $|\sin(0.739)| \approx 0.674$ per step with alternating sign. From $x_0, x_1, x_2 = 1, 0.5403, 0.8576$ the process gives $0.72801$, with error $1.1 \times 10^{-2}$ against $0.12$ for $x_2$. Restarting the iteration from each extrapolated value is [Steffensen's method](/steffensen-method/), which converges quadratically.

**A divergent series.** The partial sums $1, 3, 7, 15$ of $1 + 2 + 4 + \cdots$ give $t_0 = t_1 = -1$, the value of $1/(1 - 2)$: with $\lambda = 2$ the process returns the anti-limit of the geometric model.

**A logarithmic sequence.** For $s_k = s + a/k$ one gets exactly $t_k = s + \frac{a}{2(k+1)}$: the error is only halved. The partial sums of $\sum 1/j^2$ behave the same way; at 51 terms the ratio of the errors of $t$ and $s$ is about $0.49$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The steps are these.

1. *Equivalent forms.* Clearing the denominator, $t_k = \dfrac{s_k s_{k+2} - s_{k+1}^2}{s_{k+2} - 2s_{k+1} + s_k}$, and also $t_k = s_k - (\Delta s_k)^2/\Delta^2 s_k$; all are equal in exact arithmetic whenever $\Delta^2 s_k \ne 0$. The process commutes with affine maps: replacing $s_k$ by $\alpha s_k + \beta$ ($\alpha \ne 0$) replaces $t_k$ by $\alpha t_k + \beta$, so it can be applied to the errors $e_k$.
2. *Exactness on geometric errors (proved).* If $e_k = c\lambda^k$ with $c \ne 0$, $\lambda \ne 0, 1$, then $e_k e_{k+2} - e_{k+1}^2 = 0$ while the denominator is $c\lambda^k(\lambda - 1)^2 \ne 0$, so $t_k = s$. Conversely, $t_k = s$ for a given $k$ with $e_k \ne 0$ only if $e_k, e_{k+1}, e_{k+2}$ are in geometric progression.
3. *Acceleration theorem (proved; Henrici's form).* Suppose $e_k \ne 0$ for all $k$ and $e_{k+1} = (\lambda + \varepsilon_k) e_k$ with $\varepsilon_k \to 0$ and $\lambda \ne 1$. Then $t_k$ is defined for all large $k$ and
$$\frac{t_k - s}{e_k} = \frac{\rho_k(\rho_{k+1} - \rho_k)}{\rho_k\rho_{k+1} - 2\rho_k + 1} \to \frac{\lambda \cdot 0}{(\lambda - 1)^2} = 0, \qquad \rho_k = \lambda + \varepsilon_k.$$
If moreover $\lambda \ne 0$, the same holds with $e_{k+2}$ in place of $e_k$, since $e_{k+2}/e_k \to \lambda^2$. The theorem covers linear convergence $0 < |\lambda| < 1$, alternating series with $\lambda = -1$, and divergent sequences with $|\lambda| > 1$. The amount of acceleration depends on how fast $\varepsilon_k \to 0$: if $e_k = c_1\lambda_1^k + c_2\lambda_2^k + \cdots$ with $|\lambda_1| > |\lambda_2|$, then $t_k - s = O(\lambda_2^k)$ when $\lambda_2 \ne 0$ (asymptotic, proved by expanding the formula).
4. *Logarithmic convergence ($\lambda = 1$).* For $e_k = a/k$ the computation in the example is exact, so no theorem of the kind above can hold. More strongly, Delahaye and Germain-Bonnet (1980) proved that no sequence transformation accelerates every logarithmically convergent sequence.

## Complexity

Each $t_k$ costs 3 subtractions, one squaring, one division and one subtraction: 6 operations, so $6(N - 1)$ for the whole sequence. The process needs only the last three terms, so streaming use takes $O(1)$ extra space. Iterating the process $j$ times on $N + 1$ terms costs about $6jN$ operations and yields $N + 1 - 2j$ terms. The main cost in practice is producing the terms $s_k$ themselves (function evaluations or iterations); the process lets one stop with fewer of them.

**Rounding.** The denominator $d$ is a difference of nearly equal differences when $\lambda$ is close to 1 or when the terms have nearly converged. For geometric errors $e_k = c\lambda^k$, differentiating the symmetric form gives $\partial t_k/\partial s_k = \lambda^2/(\lambda - 1)^2$, $\partial t_k/\partial s_{k+1} = -2\lambda/(\lambda - 1)^2$ and $\partial t_k/\partial s_{k+2} = 1/(\lambda - 1)^2$. So absolute errors $\eta$ in the terms (from rounding, about $u|s|$) are amplified, to first order, by up to $\big((1 + |\lambda|)/(1 - \lambda)\big)^2$: a factor 9 for $\lambda = 1/2$, about $4 \times 10^4$ for $\lambda = 0.99$. This is a first-order condition number, proved by the differentiation, not a rigorous bound on the computed result. Two practical consequences:

- *Use the form $s_{k+2} - b^2/d$.* The symmetric form $(s_k s_{k+2} - s_{k+1}^2)/(s_{k+2} - 2s_{k+1} + s_k)$ subtracts two nearly equal products of size $s^2$ and loses everything when $|e_k| \ll |s|$. In a test on 3000 random geometric sequences in double precision, the total error of the stable form was below $10^{-6}$ and that of the symmetric form was more than $10^3$ times larger (observed; see the tests).
- *Stop before convergence.* Once $|e_k|$ is near rounding level, $a$, $b$ and $d$ are noise and $t_k$ is meaningless; a test $|d| \le$ a few units of $u|s_{k+2}|$ should end the extrapolation.

## Properties

- **Nonlinear and quasi-linear.** $t$ depends nonlinearly on $s$, but commutes with affine maps $s \mapsto \alpha s + \beta$.
- **Kernel.** The sequences with $t_k = s$ for all $k$ are exactly those with $s_k = s + c\lambda^k$, $c \ne 0$, $\lambda \ne 0, 1$ (and constant sequences, by the convention of L5).
- **Local.** $t_k$ uses only $s_k, s_{k+1}, s_{k+2}$.
- **Equal to Shanks's $e_1$** and to the column $\varepsilon_2^{(k)}$ of Wynn's ε-algorithm (see [sequence extrapolation](/sequence-extrapolation/)). For partial sums of a power series $\sum c_j z^j$, $t_k$ equals the [Padé approximant](/pade-approximation/) $[k+1/1]$ at $z$.
- **Accelerates linear convergence, not logarithmic convergence** (Correctness, steps 3 and 4).

## Variants and improvements

- **Iterated Aitken.** Apply the process to its own output. Each pass removes the next geometric component when the error is a sum of geometric terms; see the Leibniz table.
- **Shanks transformation and the ε-algorithm.** Shanks's $e_m$ fits $m$ geometric terms using $2m + 1$ terms of the sequence; Wynn's ε-algorithm computes all $e_m$ by a cheap recursion. Aitken's process is $e_1$.
- **Steffensen's method.** For a fixed-point iteration $x = g(x)$, compute $x, g(x), g(g(x))$, extrapolate, and restart from the result. This gives order 2 without derivatives ([Steffensen's method](/steffensen-method/)).
- **Power iteration.** The Rayleigh quotients or eigenvector components of [power iteration](/power-iteration/) converge linearly with ratio $\lambda_2/\lambda_1$, and Aitken's process accelerates them; this was Aitken's original setting in Bernoulli's method for the dominant root.
- **Richardson extrapolation** is the linear counterpart when the error expansion is in known powers of a step size $h$ ([Richardson extrapolation](/richardson-extrapolation/)).
- **Logarithmic sequences** need other transformations, such as Levin's $u$ transformation or the ρ-algorithm, which work for many but not all such sequences.

## When to use it

Use Aitken's process on a linearly convergent sequence whose ratio of successive errors settles to a constant: fixed-point iterations, power iteration, alternating series, or any iteration whose error is dominated by one geometric mode. It is the first thing to try because it costs almost nothing and needs no knowledge of the ratio. Do not use it on logarithmically convergent sequences (errors like $1/k$ or $1/k^2$), where it barely helps, nor on sequences whose error ratio oscillates without settling, such as those with two dominant modes of equal size. For power series, consider Padé approximants directly; for errors with known powers of $h$, use Richardson extrapolation.

## Pitfalls

- **Division by a tiny second difference.** Near convergence, or for $\lambda \approx 1$, $d$ is dominated by rounding. Guard the division and stop early.
- **The unstable textbook form.** $(s_k s_{k+2} - s_{k+1}^2)/\Delta^2 s_k$ is algebraically equal but numerically far worse.
- **Logarithmic convergence.** The process gains only a constant factor, and the output can look converged when it is not.
- **Spurious results from irregular sequences.** If the error ratio is not settling (for example two competing modes $\lambda$ and $-\lambda$), $t_k$ can be worse than $s_k$; compare successive $t_k$ before trusting them.
- **Anti-limits.** For divergent sequences the process returns a finite number, which is the limit of the geometric model, not of the sequence; it is meaningful only when that interpretation is (as with analytic continuation of a geometric series).

## Implementations

## History

The step appears in Seki Takakazu's computation of $\pi$ from inscribed polygons in the 1680s, according to historians of Japanese mathematics. Alexander Aitken introduced the process in 1926, in a paper on Bernoulli's method for the largest root of a polynomial, where the ratios of consecutive terms of a linear recurrence converge linearly; he wrote it with the operator $\delta^2$. Steffensen (1933) built it into a fixed-point iteration of order 2. Shanks (1955) generalized it to the $e_m$ transformations and Wynn (1956) found the ε-algorithm to compute them. Henrici's textbook (1964) gave the acceleration theorem in the form used above. Delahaye and Germain-Bonnet (1980) showed that the failure on logarithmic sequences is not specific to Aitken's process: no single transformation accelerates them all.

## References
