---
title: The levelled system is solvable, every iterate brackets E_n(f), and the stopping test certifies near-optimality
proves: [correctness, termination]
status: full
---

**Setting.** $f$ is continuous on $[a, b]$, $\mathcal{P}_n$ is the space of real polynomials of degree at most $n$, $E_n(f) = \min_{q \in \mathcal{P}_n} \|f - q\|_\infty$, and a reference is $x_0 < \cdots < x_{n+1}$ in $[a, b]$. The basis $T_0, \ldots, T_n$ of line L3 is any basis of $\mathcal{P}_n$; the arguments below do not depend on it. We use one fact about $\mathcal{P}_n$: a nonzero element has at most $n$ zeros (the Haar property).

**Lemma 1 (sign changes).** No $g \in \mathcal{P}_n$ satisfies $(-1)^i \sigma\, g(x_i) > 0$ for $i = 0, \ldots, n + 1$ and a fixed sign $\sigma \in \{-1, 1\}$.

*Proof.* Such a $g$ changes sign between consecutive reference points, so by the intermediate value theorem a zero lies in each of the $n + 1$ intervals $(x_i, x_{i+1})$, and these are disjoint. A nonzero $g \in \mathcal{P}_n$ has at most $n$ zeros, and $g \ne 0$ since $g(x_0) \ne 0$. $\square$

**Lemma 2 (the levelled system is nonsingular).** For every reference and every $f$ there are unique $p \in \mathcal{P}_n$ and $h \in \mathbb{R}$ with $f(x_i) - p(x_i) = (-1)^i h$ for $i = 0, \ldots, n + 1$.

*Proof.* The system is square: $n + 2$ equations in the $n + 1$ coefficients of $p$ and $h$. It suffices that the homogeneous system $p(x_i) + (-1)^i h = 0$ has only the trivial solution. If $h \ne 0$, then $(-1)^i \sigma\, p(x_i) = |h| > 0$ with $\sigma = -\operatorname{sign} h$, which Lemma 1 forbids. So $h = 0$, and then $p$ vanishes at $n + 2$ distinct points, so $p = 0$. $\square$

**Lemma 3 (de la Vallée Poussin).** Let $p \in \mathcal{P}_n$ and suppose $(-1)^i \sigma (f(x_i) - p(x_i)) > 0$ for all $i$, for a fixed sign $\sigma$. Then
$$\min_i |f(x_i) - p(x_i)| \le E_n(f) \le \|f - p\|_\infty.$$

*Proof.* The right inequality is the definition of $E_n$. For the left, suppose $q \in \mathcal{P}_n$ has $\|f - q\|_\infty < \delta := \min_i |f(x_i) - p(x_i)|$. Put $g = q - p = (f - p) - (f - q)$. At each $x_i$, $|f(x_i) - q(x_i)| < \delta \le |f(x_i) - p(x_i)|$, so $g(x_i)$ is nonzero and has the sign of $f(x_i) - p(x_i)$, that is $(-1)^i \sigma g(x_i) > 0$. Lemma 1 forbids this. So every $q$ has $\|f - q\|_\infty \ge \delta$, and $E_n(f) \ge \delta$. $\square$

**Corollary 4 (the bracket).** For the solution $(p, h)$ of line L3, $|h| \le E_n(f) \le \|f - p\|_\infty$.

*Proof.* If $h = 0$ the left inequality is trivial. Otherwise $f(x_i) - p(x_i) = (-1)^i h$ alternates strictly in sign with $|f(x_i) - p(x_i)| = |h|$, and Lemma 3 applies. $\square$

**Theorem 5 (correctness of the output).** Suppose line L6 succeeds with $M = \max|e|$ and $0 \le \text{tol} < 1$, and suppose $M = \|f - p\|_\infty$ (the search of line L5 found the true maximum). Then
$$E_n(f) \le \|f - p\|_\infty \le \frac{E_n(f)}{1 - \text{tol}}.$$

*Proof.* The test gives $M(1 - \text{tol}) \le |h|$, and Corollary 4 gives $|h| \le E_n(f)$. So $M \le E_n(f)/(1 - \text{tol})$; the left inequality is the definition of $E_n$. $\square$

If the search returns $M < \|f - p\|_\infty$, the lower bound $|h| \le E_n(f)$ remains valid, but the upper bound holds only for the searched maximum. This is the limit of any implementation that locates extrema numerically.

**Theorem 6 (exact cases).** (a) If $f \in \mathcal{P}_n$, the first iteration returns $p = f$. (b) If the reference is the alternation set of the best approximation $p^*$, then line L3 returns $p = p^*$ and $|h| = E_n(f)$.

*Proof.* (a) $p = f$, $h = 0$ solves the system, which is unique by Lemma 2; then $e = 0$ and line L6 succeeds. (b) $p^*$ and $h = \pm E_n(f)$ solve the system, by the equioscillation property of $p^*$, and the solution is unique by Lemma 2. $\square$

**Termination.** The implementation performs at most a fixed number of iterations. Each iteration is finite: the linear solve, a scan of $m$ grid points, and a fixed number of golden-section steps per extremum. Convergence of the iterates to $p^*$ is a further property, proved for the single-exchange rule for every continuous $f$ (Powell, Chapters 8 and 9) and, with a quadratic rate near the solution, for the multiple exchange under smoothness and nondegeneracy assumptions (Veidinger 1960). It is not claimed here for the window rule of line L8 in every degenerate case.
