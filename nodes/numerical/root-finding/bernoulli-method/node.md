---
tag: QQR2VY
kind: algorithm
slug: bernoulli-method
name: Bernoulli's method
aliases:
- Bernoulli's method for dominant root
- Bernoulli's iteration
area: numerical/root-finding
level: advanced
summary: Runs the linear recurrence whose characteristic polynomial is p and takes the ratio of consecutive terms. It converges linearly, with rate |r2/r1|, to a root of p of strictly largest modulus.
solves: [polynomial-root-finding]
model: real-ram
complexity:
  vars: {n: "the degree", λ: "the ratio |r2|/|r1| of the two largest root moduli", δ: "the tolerance", K: "the cap on the steps"}
  time: {worst: "O(n K)", average: "O(n log(1/δ) / log(1/λ))"}
  space: {extra: Θ(n)}
  evaluations: {worst: "K", step: "1"}
properties: {deterministic: true, recursive: false, bracketing: false, derivative_free: true, global: true}
prereqs: [polynomial-root-finding, order-of-convergence]
see_also: [graeffe-method, companion-matrix-method, polynomial-deflation, cauchy-root-bound, durand-kerner-method, jenkins-traub-algorithm, stopping-criteria, aitken-delta-squared]
sources:
  - paper: "Daniel Bernoulli, Observationes de seriebus quae formantur ex additione vel subtractione quacunque terminorum se mutuo consequentium, Commentarii Academiae Scientiarum Imperialis Petropolitanae 3 (for 1728), 85-100, 1732"
    locator: the ratio of consecutive terms of a recurrent series as an approximation of the largest root
  - paper: "A. C. Aitken, On Bernoulli's numerical solution of algebraic equations, Proceedings of the Royal Society of Edinburgh 46, 289-305, 1926"
    locator: the analysis of the method, the extension to complex and further roots, and the delta-squared acceleration
  - book: "Peter Henrici, Elements of Numerical Analysis, Wiley, 1964"
    locator: the chapter on Bernoulli's method (the power sum start, the dominant root, the complex pair and the convergence rate)
  - book: "Alston S. Householder, The Numerical Treatment of a Single Nonlinear Equation, McGraw-Hill, 1970"
    locator: the chapter on methods of Bernoulli type and their relation to the power method and the QD algorithm
---

Bernoulli's method finds the root of largest modulus of a polynomial $p(x) = a_0x^n + \cdots + a_n$ without any starting guess. It runs the linear recurrence $a_0y_{k} + a_1y_{k-1} + \cdots + a_ny_{k-n} = 0$, whose solutions are combinations $\sum_i c_ir_i^k$ of the powers of the roots $r_i$, and watches the ratio $y_{k+1}/y_k$. When one root $r_1$ is strictly larger in modulus than all others, its powers win and the ratio tends to $r_1$, with linear rate $\lambda = |r_2|/|r_1|$, where $r_2$ is the next largest. It is global and simple, one recurrence step of $n$ multiplications per iteration, but slow when $\lambda$ is near 1 and useless as it stands when two roots tie for the largest modulus, as a complex conjugate pair does. It is the power method for the [companion matrix](/companion-matrix-method/) in disguise.

## In plain words

Raise every root to a high power, and the biggest root's power swamps the rest. A linear recurrence with the right coefficients does exactly that without knowing the roots: each new term is a fixed mix of the last $n$ terms, and after many steps the sequence grows like the powers of the biggest root. Divide each term by the one before and you read off that root. How fast this works depends on how much bigger the biggest root is than the second biggest.

## The problem

Notation on the root-finding pages: $f$ is the function, $x^*$ a root, $x_k$ the iterates and $e_k = x_k - x^*$ the error. A method has [order](/order-of-convergence/) $q$ and rate constant $C$ when $|e_{k+1}| \approx C |e_k|^q$, with $0 < C < 1$ when $q = 1$. A root has [multiplicity](/multiplicity-of-roots/) $m$ when $f(x^*) = \cdots = f^{(m-1)}(x^*) = 0 \ne f^{(m)}(x^*)$. The cost is the number of evaluations of $f$ (and of $f'$ where a method uses it). A method of order $q$ that needs $w$ evaluations in each step has efficiency index $q^{1/w}$.

Here $f = p$ has real coefficients and degree $n \ge 1$, with distinct roots $r_1, \dots, r_s$ of multiplicities $m_1, \dots, m_s$, ordered so that $|r_1| \ge |r_2| \ge \cdots$. The target is $x^* = r_1$ under the hypothesis that it is the only distinct root of largest modulus (it is then real, since its conjugate is also a root). The iterates are the ratios $\rho_k = y_{k+1}/y_k$, and one evaluation is one step of the recurrence. The stopping rule is $|\rho_k - \rho_{k-1}| \le \delta(1 + |\rho_k|)$ or $K$ steps.

## The algorithm

```pseudo id=main
BERNOULLI(a, delta, K):
L1   y <- (s_0, ..., s_{n-1}), the power sums of the roots, from Newton's identities
L2   for k = 1, 2, ..., K:
L3       t <- -(a_1 y_{last} + a_2 y_{last-1} + ... + a_n y_{last-n+1}) / a_0;  shift t into the window y
L4       divide the window by its largest absolute value (stop with root 0 if the window is all zero)
L5       if the previous term was 0 then skip the ratio this step
L6       rho_k <- t / (previous term)
L7       if |rho_k - rho_{k-1}| <= delta (1 + |rho_k|) then return rho_k, "converged"
L8   return rho_K, "max-iter"
```

Line L1 starts with the power sums $s_k = \sum_i m_ir_i^k$, which Newton's identities give from the coefficients: $s_0 = n$ and $a_0s_k + a_1s_{k-1} + \cdots + a_{k-1}s_1 + ka_k = 0$ for $1 \le k < n$. With this start every later term is again a power sum, $y_k = s_k$, so the coefficient of $r_1^k$ is $m_1 \ne 0$; an arbitrary start could make it 0. Line L4 rescales the last $n$ terms by one common factor. The ratio and the recurrence are unchanged, but the terms grow like $|r_1|^k$ and would overflow within a few hundred steps otherwise. Line L5 skips a ratio with a zero denominator, which happens for instance when the roots are $\pm 1$.

## Example

Take $p(x) = x^3 - 6x^2 + 11x - 6 = (x - 1)(x - 2)(x - 3)$. The power sums are $s_k = 1 + 2^k + 3^k$: 3, 6, 14, 36, 98, 276, 794, 2316, ... Line L1 produces $3, 6, 14$ from Newton's identities, and the recurrence $s_k = 6s_{k-1} - 11s_{k-2} + 6s_{k-3}$ continues the list. The ratios and their errors are

| $j$ | $s_{j+1}/s_j$ | error | error ratio |
|---|---|---|---|
| 2 | 2.571429 | $-0.428571$ | |
| 3 | 2.722222 | $-0.277778$ | 0.648 |
| 4 | 2.816327 | $-0.183673$ | 0.661 |
| 5 | 2.876812 | $-0.123188$ | 0.671 |
| 6 | 2.916877 | $-0.083123$ | 0.675 |
| 7 | 2.943869 | $-0.056131$ | 0.675 |

In closed form the error is $(s_{j+1} - 3s_j)/s_j = -(2 + 2^j)/(1 + 2^j + 3^j)$, and the error ratio tends to $\lambda = 2/3$. With $\delta = 10^{-12}$ the run stops after 63 steps with $\rho = 2.9999999999946$, an error of $5.4 \times 10^{-12}$. The error is about five times the last change in $\rho$, which is the price of a linear rate: see the pitfalls.

## Correctness

With the power sum start, $y_k = \sum_i m_ir_i^k$ exactly. If $r_1$ is the only distinct root of largest modulus and $\lambda = \max_{i \ge 2}|r_i|/|r_1| < 1$, then $y_k \ne 0$ for all large $k$ and
$$\rho_k - r_1 = \sum_{i \ge 2}\frac{m_i}{m_1}(r_i - r_1)\Bigl(\frac{r_i}{r_1}\Bigr)^k + O(\lambda^{2k}),$$
so $\rho_k \to r_1$ linearly, with $|\rho_k - r_1| = O(\lambda^k)$, and with error ratio exactly $r_2/r_1$ in the limit when $r_2$ is the only root of the second largest modulus. This holds for any multiplicity $m_1$ of the dominant root. If two or more distinct roots share the largest modulus, the ratios do not converge in general. The loop stops after at most $K$ steps, and the rescaling does not change any ratio. The proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

Each step costs $n$ multiplications and additions for the recurrence and $n$ divisions for the rescaling, so $O(n)$, and $O(n^2)$ for the start. To reach error $\delta$ the method needs about $\log(1/\delta)/\log(1/\lambda)$ steps, which is about 68 for the example ($\lambda = 2/3$, $\delta = 10^{-12}$) and about 540 for the degree-20 [Wilkinson polynomial](/wilkinson-polynomial/) ($\lambda = 19/20$). That last figure holds only in exact arithmetic: in double precision the ratios for the Wilkinson polynomial reach an error near $10^{-5}$ after about 300 steps and then fluctuate at that level, because of the rounding in its large coefficients and in the recurrence.

## Properties

- Global: no starting guess and no failure for lack of one, as long as the dominant root is unique in modulus.
- Linear convergence with rate $\lambda = |r_2/r_1|$ (proved); no derivatives and no division by $p'$.
- The result for a dominant root of multiplicity $m_1 > 1$ is still linear with rate $\lambda$, because the power sums carry no polynomial factors in $k$.
- Equivalent to the power method applied to the companion matrix of $p$, with the vector $(y_{k-n+1}, \dots, y_k)$.
- Fails without warning on ties: on $x^2 - 1$ and on a dominant complex pair the ratios oscillate until $K$.

## Variants and improvements

- **Complex pair.** If the dominant roots are a conjugate pair $r, \bar r$, then $y_{k+1} \approx Sy_k - Py_{k-1}$ with $S = r + \bar r$ and $P = |r|^2$. Fitting $S$ and $P$ to four consecutive terms gives the real quadratic factor $x^2 - Sx + P$. The reference code includes this as bernoulli_pair; on $x^4 + 3x^2 + 6x + 10$ it returns $S = 2$, $P = 5$, the factor of the roots $1 \pm 2i$.
- **Smallest root.** Applied to the reversed polynomial $x^np(1/x)$, the method finds the root of smallest modulus, which is the one wanted for [deflation](/polynomial-deflation/) with small errors.
- **Acceleration.** [Aitken's delta-squared process](/aitken-delta-squared/) applied to the ratios removes the leading geometric error term, which Aitken introduced for this method in 1926.
- **Shifts.** Running the method on $p(x + \sigma)$ changes which root dominates and how strongly.
- **All roots.** Rutishauser's quotient-difference algorithm extends the ratios to a table whose columns converge to every root of distinct modulus; [Graeffe's method](/graeffe-method/) squares the roots instead, separating their moduli quadratically.

## When to use it

Use it as a quick, guess-free estimate of the largest root, as a teaching example of the power method, or as a source of starting values for a fast local method such as [Newton's](/newton-raphson-method/) or [Laguerre's](/laguerre-method/). For production root finding of whole polynomials, prefer the [companion matrix method](/companion-matrix-method/), [Jenkins-Traub](/jenkins-traub-algorithm/) or [Aberth's method](/aberth-ehrlich-method/).

## Pitfalls

- L1: starting from an arbitrary window such as $(0, \dots, 0, 1)$ works when the roots are distinct, but the coefficient of $r_1^k$ can vanish for special starts; then the method converges to the wrong root. The power sum start excludes this.
- L4: without rescaling the terms overflow. With roots 2 and 1.999 the unscaled terms pass $10^{308}$ after about 1000 steps.
- L5: a zero term makes the ratio undefined; skip it, and do not count it as convergence.
- L7: with a linear rate, the error is about $|\rho_k - \rho_{k-1}|\,\lambda/(1 - \lambda)$, which is large when $\lambda$ is near 1, so the step test can stop too early; use a tighter $\delta$ or an error estimate from the observed error ratio. Once rounding noise dominates, the test can also fire by chance: on the Wilkinson polynomial of degree 20 with $\delta = 10^{-12}$ it fired after 63916 steps, when two noisy ratios happened to agree, with error $1.1 \times 10^{-5}$.
- L8: when roots tie for the largest modulus the ratio never settles and only the cap $K$ stops the loop; the status "max-iter" is the signal, not a root.

## Implementations

## History

Daniel Bernoulli described the method around 1728, in a paper on recurrent series published by the Saint Petersburg Academy, observing that the ratio of consecutive terms of such a series approaches the largest root of its scale equation. Euler treated it in his Introductio of 1748. A. C. Aitken's 1926 paper analysed it in detail, extended it to complex and subdominant roots, and introduced his delta-squared acceleration for it. Rutishauser's quotient-difference algorithm of 1954 grew out of the same idea, and the link with the power method made it one of the ancestors of matrix eigenvalue methods for polynomial roots.

## References
