---
title: Every PISO corrector ends divergence free, and the correctors converge geometrically to the coupled implicit step, with a splitting error of order Δt^(m+1) after m of them
proves: [correctness, termination]
status: full
---

**Setting.** The grid is the periodic MAC grid of the main page with $M$ cells. $D$ is the divergence at the cell centers and $G$ the gradient at the faces. Summation by parts gives $G^T = -D$, and $-DG$ is the periodic 5-point matrix, symmetric positive semidefinite with the constants as its null space (proved on the [Chorin projection method](/chorin-projection-method/) page). One time step has the coefficients $a_P = 1/\Delta t + 2\nu/\Delta x^2 + 2\nu/\Delta y^2$, the same on every face, and the neighbor coefficients $a_{nb}$ of central differences, computed from $\mathbf{u}^n$. Write $N$ for the matrix of the $a_{nb}$ and $\mathbf{b} = \mathbf{u}^n/\Delta t + \mathbf{f}$. The coupled implicit step that PISO approximates is

$$a_P\mathbf{u} - N\mathbf{u} = \mathbf{b} - Gp, \qquad D\mathbf{u} = 0. \tag{C}$$

PISO computes the predictor $\mathbf{u}^{(0)} = \mathbf{u}^*$ from $(a_P - N)\mathbf{u}^* = \mathbf{b} - Gp^n$ (line L2) and then, for $k = 1, \dots, m$, $\mathbf{h} = (\mathbf{b} + N\mathbf{u}^{(k-1)})/a_P$, $p^{(k)}$ from $-DGp^{(k)} = -a_P D\mathbf{h}$, and $\mathbf{u}^{(k)} = \mathbf{h} - Gp^{(k)}/a_P$ (lines L4 to L6). The first corrector is Issa's form with $p' = p^{(1)} - p^n$: from the predictor equation $\mathbf{h} = \mathbf{u}^* + Gp^n/a_P$, so $\mathbf{u}^{(1)} = \mathbf{u}^* - G(p^{(1)} - p^n)/a_P$.

Let $U = \max|u^n|$, $V = \max|v^n|$, $S = 2\nu/\Delta x^2 + 2\nu/\Delta y^2 + U/\Delta x + V/\Delta y$, $q = S/a_P$, and the Courant number $C = \Delta t(U/\Delta x + V/\Delta y)$. Norms are Euclidean.

**Lemma 1 (the corrector is an orthogonal projection).** Let $P$ be the orthogonal projection onto the face vectors with $D\mathbf{w} = 0$. Each corrector gives $\mathbf{u}^{(k)} = P\mathbf{h}$.

*Proof.* The equation $-DGp = -a_P D\mathbf{h}$ is solvable because $\sum_c (D\mathbf{h})_c = 0$ on the periodic grid, so the right side is in the range of $-DG$. Then $D\mathbf{u}^{(k)} = D\mathbf{h} - DGp/a_P = 0$. Also $\mathbf{u}^{(k)} - \mathbf{h} = -Gp/a_P$ is in the range of $G$, and for every $\mathbf{w}$ with $D\mathbf{w} = 0$, $\mathbf{w}^TGp = (G^T\mathbf{w})^Tp = -(D\mathbf{w})^Tp = 0$. So $\mathbf{u}^{(k)}$ is divergence free and $\mathbf{h} - \mathbf{u}^{(k)}$ is orthogonal to the divergence-free vectors, which is the definition of $P\mathbf{h}$. $\square$

**Theorem 1 (mass conservation after every corrector).** $D\mathbf{u}^{(k)} = 0$ for every $k \ge 1$, whatever the predictor and $\Delta t$ are.

*Proof.* This is the first part of the proof of Lemma 1. $\square$

The test file checks $\max|D\mathbf{u}^{(k)}| < 10^{-10}$ after each of three correctors, from a start that is not divergence free.

**Lemma 2 (size of the neighbor matrix).** $\|N\| \le S$.

*Proof.* A row of $N$ has the four entries $\nu/\Delta x^2 \mp \bar u/(2\Delta x)$ and $\nu/\Delta y^2 \mp \bar v/(2\Delta y)$, where $\bar u$ and $\bar v$ are values or averages of $\mathbf{u}^n$, so $|\bar u| \le U$ and $|\bar v| \le V$. So every row has absolute sum at most $S$. A column receives one entry from each of four rows, the east, west, north and south neighbors, and the same bound on each entry gives column sums at most $S$. Then $\|N\|^2 \le \|N\|_1\|N\|_\infty \le S^2$. $\square$

Note that $q < 1$ is the same as $a_P > S$, which is $1/\Delta t > U/\Delta x + V/\Delta y$, that is $C < 1$. Also $a_P \ge 1/\Delta t$, so $q \le \Delta t\,S$, and $a_P - S \ge (1 - C)/\Delta t$.

**Theorem 2 (convergence of the correctors).** Let $C < 1$. Then (C) has exactly one velocity solution $\mathbf{u}$, with a pressure $p$ unique up to a constant, and for every $k \ge 1$

$$\|\mathbf{u}^{(k)} - \mathbf{u}\| \le q\,\|\mathbf{u}^{(k-1)} - \mathbf{u}\|, \qquad \|\mathbf{u}^* - \mathbf{u}\| \le \frac{\Delta t}{1 - C}\,\|G(p - p^n)\|.$$

So $\|\mathbf{u}^{(m)} - \mathbf{u}\| \le q^m\frac{\Delta t}{1 - C}\|G(p - p^n)\| \le \frac{(\Delta t\,S)^m\,\Delta t}{1 - C}\|G(p - p^n)\|$.

*Proof.* Let $T(\mathbf{w}) = P((\mathbf{b} + N\mathbf{w})/a_P)$, so that $\mathbf{u}^{(k)} = T(\mathbf{u}^{(k-1)})$ by Lemma 1. Since $\|P\| \le 1$ and by Lemma 2, $\|T(\mathbf{w}) - T(\mathbf{w}')\| \le \|N\|\|\mathbf{w} - \mathbf{w}'\|/a_P \le q\|\mathbf{w} - \mathbf{w}'\|$, so $T$ is a contraction and has exactly one fixed point $\mathbf{u}$. The fixed point solves (C): $\mathbf{u} = P\mathbf{h}$ with $\mathbf{h} = (\mathbf{b} + N\mathbf{u})/a_P$ gives $D\mathbf{u} = 0$ and $\mathbf{h} - \mathbf{u} = G\varphi$ for some $\varphi$ (the orthogonal complement of the divergence-free vectors is the range of $G$, because $G^T = -D$). With $p = a_P\varphi$ this is $a_P\mathbf{u} - N\mathbf{u} = \mathbf{b} - Gp$. Conversely every velocity solution of (C) is a fixed point of $T$ by Lemma 1, so it is $\mathbf{u}$; $Gp$ is then fixed by (C), and $p$ is fixed up to the null space of $G$, the constants.

For the first inequality, $\mathbf{u}^{(k)} - \mathbf{u} = T(\mathbf{u}^{(k-1)}) - T(\mathbf{u})$. For the second, subtract (C) from the predictor equation: $(a_P - N)(\mathbf{u}^* - \mathbf{u}) = G(p - p^n)$. For any $\mathbf{w}$, $\|(a_P - N)\mathbf{w}\| \ge (a_P - S)\|\mathbf{w}\| \ge (1 - C)\|\mathbf{w}\|/\Delta t$, which gives the bound. $\square$

**Corollary (splitting error).** On a fixed grid, as $\Delta t \to 0$, the difference between $m$ correctors and the coupled step is $O(\Delta t^{m+1})$ in general, and $O(\Delta t^{m+2})$ when $p^n$ comes from the previous step of a smooth solution, so that $p - p^n = O(\Delta t)$. The coupled backward Euler step has a local error of order $\Delta t^2$. So already one corrector with a consistent pressure, and two in general, keep the splitting error below the local time error, and PISO is first order in time like backward Euler.

The test file confirms the contraction with the proved factor ($q = 0.53$ on its $8 \times 8$ case, where the observed ratios are about 0.08, so the bound is far from tight), measures splitting error orders of about 2.9 and 3.9 for $m = 1$ and $m = 2$ with a consistent pressure, and measures first order in time over many steps.

**Termination.** Line L2 runs at most a fixed number of Gauss-Seidel sweeps (it stops earlier when the update is below $10^{-13}$; the sweeps converge when $C < 1$, because then $a_P > S$ makes the momentum matrix strictly diagonally dominant). The loop of line L3 runs exactly $m$ times, and each conjugate gradient solve stops after at most its iteration limit. So a PISO step always ends, after a fixed amount of work bounded in advance. There is no outer iteration.

**What is not proved.** The bounds are for one step with the coefficients frozen at $\mathbf{u}^n$. Stability over many steps and the effect of the frozen advection coefficients are not proved here; the condition $C < 1$ is sufficient for the bounds, not necessary for the method to work.
