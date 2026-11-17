---
title: The splicing model has an exact solution, steady states lie on a line, and the steady-state velocity has the right sign
proves: [correctness]
status: full
---

We prove what the steady-state model computes, for one gene. The splicing model has a closed-form solution (Theorem 1). Its steady states lie on the line $u = (\gamma/\beta)s$ (Lemma 2). With the true ratio, the velocity $u - (\gamma/\beta)s$ is $\frac{1}{\beta}\frac{ds}{dt}$, it is positive while the gene is switched on from zero and negative while it is switched off from its on state (Theorem 3). The fit of lines L1 and L2 is exact when the chosen cells lie on the steady-state line (Theorem 5), and the step of line L4 has an error of order $\Delta^2$ (Lemma 6). Real cells are not all at steady state at the extremes, counts are noisy, and genes do not all follow one switch; so the quality of the estimate on data is measured, not proved.

**Setting.** One gene in one cell, with unspliced count $u$ and spliced count $s$, and rates $\alpha \ge 0$ (transcription), $\beta > 0$ (splicing) and $\gamma > 0$ (degradation):
$$\frac{du}{dt} = \alpha - \beta u, \qquad \frac{ds}{dt} = \beta u - \gamma s.$$
The steady-state model takes $\beta$ to be the same for all genes and measures time in units of $1/\beta$, so its ratio is $\gamma' = \gamma/\beta$. Line L1 chooses the cells whose $s$ is among the $m = \lceil qn\rceil$ smallest or the $m$ largest. Line L2 sets $\hat\gamma = \sum u_is_i/\sum s_i^2$ over the chosen cells. Line L3 sets $v_i = u_i - \hat\gamma s_i$, and line L4 sets $\hat s_i = s_i + \Delta v_i$.

**Theorem 1 (solution).** With a constant $\alpha$ and start $(u_0, s_0)$, $u(t) = u_0e^{-\beta t} + \frac{\alpha}{\beta}(1 - e^{-\beta t})$ and, for $\beta \ne \gamma$,
$$s(t) = s_0e^{-\gamma t} + \frac{\alpha}{\gamma}(1 - e^{-\gamma t}) + \frac{\alpha - \beta u_0}{\gamma - \beta}\left(e^{-\gamma t} - e^{-\beta t}\right),$$
and for $\beta = \gamma$, $s(t) = s_0e^{-\gamma t} + \frac{\alpha}{\gamma}(1 - e^{-\gamma t}) + (\beta u_0 - \alpha)te^{-\gamma t}$.

*Proof.* Both formulas give $u(0) = u_0$ and $s(0) = s_0$. For $u$: $u' = -\beta u_0e^{-\beta t} + \alpha e^{-\beta t} = \alpha - \beta u$. For $s$ write $u = \frac{\alpha}{\beta} + (u_0 - \frac{\alpha}{\beta})e^{-\beta t}$, so that $s' + \gamma s = \alpha + (\beta u_0 - \alpha)e^{-\beta t}$. The terms $s_0e^{-\gamma t}$ and $\frac{\alpha}{\gamma}(1 - e^{-\gamma t})$ contribute $0$ and $\alpha$ to $s' + \gamma s$. When $\beta \ne \gamma$, $\frac{d}{dt}(e^{-\gamma t} - e^{-\beta t}) + \gamma(e^{-\gamma t} - e^{-\beta t}) = (\beta - \gamma)e^{-\beta t}$, so the last term, with $c = \frac{\alpha - \beta u_0}{\gamma - \beta}$, contributes $c(\beta - \gamma)e^{-\beta t} = (\beta u_0 - \alpha)e^{-\beta t}$, as needed. When $\beta = \gamma$, $\frac{d}{dt}(te^{-\gamma t}) + \gamma te^{-\gamma t} = e^{-\gamma t}$, so the last term contributes $(\beta u_0 - \alpha)e^{-\beta t}$. A linear equation with a given start has only one solution. $\square$

**Lemma 2 (steady state).** The only fixed point is $(\alpha/\beta, \alpha/\gamma)$, which lies on the line $u = (\gamma/\beta)s$, and every solution tends to it.

*Proof.* Setting both derivatives to 0 gives $u = \alpha/\beta$ and $s = \beta u/\gamma = \alpha/\gamma$. All exponentials in Theorem 1 tend to 0, and so does $te^{-\gamma t}$. $\square$

So a cell whose gene has been on for a long time sits at the upper end of the line, and a cell whose gene has been off for a long time sits near the origin, which is also on the line.

**Theorem 3 (sign).** Let $w = \beta u - \gamma s = \frac{ds}{dt}$. If the gene starts at $(0, 0)$ with $\alpha > 0$, then $w(t) > 0$ for all $t > 0$. If it starts at the on state $(\alpha_1/\beta, \alpha_1/\gamma)$ with $\alpha_1 > 0$ and is switched off ($\alpha = 0$), then $w(t) < 0$ for all $t > 0$. The velocity of line L3 with $\hat\gamma = \gamma/\beta$ is $w/\beta$, with the same sign.

*Proof.* In both cases $w(0) = 0$, and $w' = \beta u' - \gamma s' = \beta(\alpha - \beta u) - \gamma w$, so $w(t) = \int_0^te^{-\gamma(t - x)}\beta(\alpha - \beta u(x))\,dx$. In the first case $u(x) < \alpha/\beta$ for every $x$ by Theorem 1, so the integrand is positive. In the second case $\alpha = 0$ and $u(x) > 0$, so the integrand is negative. Finally $u - \frac{\gamma}{\beta}s = w/\beta$. $\square$

**Lemma 4 (mirror).** With $\beta, \gamma$ fixed, the path switched off from the on state of $\alpha_1$ is the on state minus the path switched on from $(0, 0)$ with $\alpha_1$, at the same times. So their velocities are opposite.

*Proof.* Let $(u, s)$ solve the on path. Then $(\alpha_1/\beta - u, \alpha_1/\gamma - s)$ starts at the on state, and its derivatives are $-(\alpha_1 - \beta u) = 0 - \beta(\alpha_1/\beta - u)$ and $-(\beta u - \gamma s) = \beta(\alpha_1/\beta - u) - \gamma(\alpha_1/\gamma - s)$, which is the off model with $\alpha = 0$. Its $w$ is $\beta(\alpha_1/\beta - u) - \gamma(\alpha_1/\gamma - s) = -(\beta u - \gamma s) = -w$. $\square$

**Theorem 5 (fit).** $\hat\gamma$ of line L2 minimizes $\sum(u_i - c\,s_i)^2$ over $c$, for the chosen cells. If every chosen cell lies on the line $u = \gamma' s$ and not every chosen $s_i$ is 0, then $\hat\gamma = \gamma'$.

*Proof.* The sum is a quadratic in $c$ with second derivative $2\sum s_i^2 > 0$ and derivative $-2\sum s_i(u_i - cs_i)$, which is 0 only at $c = \sum u_is_i/\sum s_i^2$. If $u_i = \gamma's_i$ for all chosen cells, the sum is 0 at $c = \gamma'$, so that is the minimum. $\square$

When some chosen cells are still on their way to a steady state, the fit is biased. Cells being switched on lie above the line and cells being switched off lie below it (Theorem 3), and the fit weights each cell by $s_i^2$. In the page example the fit over all cells gives 0.413 for a true 0.5.

**Lemma 6 (extrapolation).** If $\hat\gamma = \gamma'$ and $\beta = 1$, then $s(t + \Delta) - (s(t) + \Delta v(t)) = \frac{\Delta^2}{2}s''(\xi)$ for some $\xi$ between $t$ and $t + \Delta$.

*Proof.* $v = s'$ by Theorem 3, and this is Taylor's theorem with the Lagrange remainder; $s$ is smooth by Theorem 1. $\square$

**What the lines compute.** Line L1 picks the cells taken to be near the off and on steady states. Line L2 is Theorem 5. Line L3 is the velocity of Theorem 3, in units of $\beta$. Line L4 is Lemma 6. This page does not pool counts over neighbor cells, fit the rates of each gene by the dynamical model of Bergen and co-authors (2020), or project the velocities onto an embedding; Theorems 1 and 3 are the model that the dynamical fit uses, but the fit itself is not here.

**Complexity.** For $n$ cells and $g$ genes, line L1 sorts each gene in $O(n\log n)$ time and lines L2 to L4 take $O(n)$ per gene, so the total time is $O(gn\log n)$ and the space is $O(gn)$ for the velocities.

**What the tests check.** The test file checks the page example, Theorem 1 against a fourth-order Runge-Kutta solution in both cases of $\beta$ and $\gamma$, Lemma 2, Theorem 3 on random rates, Lemma 4, Theorem 5 with steady cells at the extremes, and the order $\Delta^2$ of Lemma 6. One simulation is a measurement, not a theorem: 20 genes and 300 cells over an on and an off phase with Gaussian noise, where the test checks the median error of $\hat\gamma$ and the share of cells with a clear velocity whose sign is right.
