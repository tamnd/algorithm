---
title: The bisection finds the optimal H-infinity level and the Riccati step returns the stabilizing solution
proves: [correctness]
status: full
---

Notation is that of the page. The plant satisfies assumptions 1 to 5. We use the DGKF theorem as a cited result: for $\gamma > 0$, FEASIBLE$(\gamma)$ in exact arithmetic returns true if and only if some internally stabilizing controller gives $\|T_{zw}\|_\infty < \gamma$ (Doyle, Glover, Khargonekar and Francis 1989; Zhou, Doyle and Glover 1996, chapter 16). Let $\gamma_{\rm opt}$ be the infimum of $\|T_{zw}\|_\infty$ over all internally stabilizing controllers.

## Claim 1: the feasible levels form the interval above the optimum

*FEASIBLE$(\gamma)$ is true if and only if $\gamma > \gamma_{\rm opt}$.*

*Proof.* If $\gamma > \gamma_{\rm opt}$, the definition of the infimum gives a controller with $\|T_{zw}\|_\infty < \gamma$, so FEASIBLE$(\gamma)$ is true. If FEASIBLE$(\gamma)$ is true, some controller has norm $\nu < \gamma$, so $\gamma_{\rm opt} \le \nu < \gamma$. $\square$

## Claim 2: the bisection brackets the optimum

*After line L2, `lo` is 0 or infeasible and `hi` is feasible. After the loop of lines L3 to L5, $\text{lo} \le \gamma_{\rm opt} \le \text{hi}$ and $\text{hi} - \text{lo} \le \text{tol} \cdot \text{hi}$.*

*Proof.* Line L1 sets lo $= 0 \le \gamma_{\rm opt}$. Line L2 doubles hi and moves the old hi into lo only when the old hi is infeasible, so by Claim 1 each value of lo is at most $\gamma_{\rm opt}$. The loop of L2 ends: assumptions 1 and 2 give a stabilizing controller, its norm is finite, and every larger level is feasible. At the end of L2, hi is feasible, so $\gamma_{\rm opt} < \text{hi}$. Inside L3 to L5 the midpoint $g$ replaces hi only if it is feasible ($\gamma_{\rm opt} < g$) and replaces lo only if it is infeasible ($g \le \gamma_{\rm opt}$). So the invariant $\text{lo} \le \gamma_{\rm opt} < \text{hi}$ holds after each step. Each step halves $\text{hi} - \text{lo}$, and hi does not drop below $\gamma_{\rm opt}$, so the loop ends after at most $\lceil \log_2(\text{hi}_0/(\text{tol}\,\gamma_{\rm opt})) \rceil$ steps when $\gamma_{\rm opt} > 0$. $\square$

Line L6 takes $g = (1 + \delta)\,\text{hi} > \gamma_{\rm opt}$, so FEASIBLE$(g)$ is true and the theorem gives that the central controller of lines L8 to L10 is internally stabilizing with $\|T_{zw}\|_\infty < g \le (1 + \delta)(1 + \text{tol}')\gamma_{\rm opt}$, where $\text{tol}' = \text{tol}/(1 - \text{tol})$.

## Claim 3: a stabilizing Riccati solution is unique

*Let $R$ and $Q$ be symmetric. If $X_1$ and $X_2$ are symmetric, both solve $A^T X + X A + X R X + Q = 0$, and both $A + R X_1$ and $A + R X_2$ are Hurwitz, then $X_1 = X_2$.*

*Proof.* Let $D = X_1 - X_2$. Subtract the two equations and use $X_1 R X_1 - X_2 R X_2 = X_1 R D + D R X_2$:

$$(A + R X_1)^T D + D (A + R X_2) = 0.$$

This is a Sylvester equation $M^T D + D N = 0$ with $M$ and $N$ Hurwitz. It has a unique solution when $M^T$ and $-N$ have no common eigenvalue. The eigenvalues of $M^T$ are in the open left half plane and those of $-N$ in the open right half plane, so $D = 0$ is the only solution. $\square$

The routine `riccati` returns a matrix only after it checks the residual and that $A + R X$ is Hurwitz. By Claim 3, in exact arithmetic that matrix is $\mathrm{Ric}(H)$. In floating point the checks hold with the stated tolerances.

## Claim 4: the sign function gives the stable subspace

*Assume $H = \begin{bmatrix} A & R \\ -Q & -A^T \end{bmatrix}$ has no eigenvalue on the imaginary axis and $W = \mathrm{sign}(H)$. If the stable invariant subspace of $H$ is the range of $\begin{bmatrix} I \\ X \end{bmatrix}$, then $X$ is the unique solution of the linear system $\begin{bmatrix} W_{12} \\ W_{22} + I \end{bmatrix} X = -\begin{bmatrix} W_{11} + I \\ W_{21} \end{bmatrix}$, and $X$ solves the Riccati equation with $A + R X$ Hurwitz.*

*Proof.* Write $H = V \,\mathrm{diag}(J_-, J_+)\, V^{-1}$ with the eigenvalues of $J_-$ in the open left half plane and those of $J_+$ in the open right half plane. Then $W = V \,\mathrm{diag}(-I, I)\, V^{-1}$, so $W + I = V\,\mathrm{diag}(0, 2I)\,V^{-1}$, whose kernel is the span of the first block of columns of $V$, the stable invariant subspace. Since that subspace is the range of $\begin{bmatrix} I \\ X \end{bmatrix}$, we have $(W + I)\begin{bmatrix} I \\ X \end{bmatrix} = 0$. The block rows of this identity are the stated system. The solution is unique: if $\begin{bmatrix} W_{12} \\ W_{22} + I \end{bmatrix} v = 0$, then $\begin{bmatrix} 0 \\ v \end{bmatrix}$ is in the kernel of $W + I$, so it equals $\begin{bmatrix} u \\ X u \end{bmatrix}$ for some $u$, which gives $u = 0$ and $v = 0$. So the matrix has full column rank and the normal equations have the same unique solution.

The subspace is invariant, so $H\begin{bmatrix} I \\ X \end{bmatrix} = \begin{bmatrix} I \\ X \end{bmatrix} \Lambda$ for some $\Lambda$ whose eigenvalues are the stable eigenvalues of $H$. The first block row gives $\Lambda = A + R X$, so $A + R X$ is Hurwitz. The second block row gives $-Q - A^T X = X(A + R X)$, which is the Riccati equation. $\square$

The scaled Newton iteration $W \leftarrow \frac12(\mu W + \mu^{-1} W^{-1})$ with $\mu > 0$ converges to $\mathrm{sign}(H)$ when $H$ has no eigenvalue on the imaginary axis (Higham 2008, chapter 5). The code stops when the change is below $10^{-13}$ relative and then checks $\|W^2 - I\| \le 10^{-8}$.

## Claim 5: the scalar example has optimum a + sqrt(a^2 + 2)

*For $A = a$, $B_1 = [1, 0]$, $B_2 = 1$, $C_1 = [1; 0]$, $D_{12} = [0; 1]$, $C_2 = 1$ and $D_{21} = [0, 1]$, the optimal level is $\gamma_{\rm opt} = a + \sqrt{a^2 + 2}$.*

*Proof.* Let $c = 1 - \gamma^{-2}$. Both Hamiltonians equal $\begin{bmatrix} a & -c \\ -1 & -a \end{bmatrix}$, with eigenvalues $\pm\sqrt{a^2 + c}$. So condition 1 needs $a^2 + c > 0$, and then $X = Y$ is the root of $-cX^2 + 2aX + 1 = 0$ with $a - cX = -\sqrt{a^2 + c}$, that is $X = (a + \sqrt{a^2 + c})/c$ for $c \ne 0$ and $X = -1/(2a)$ for $c = 0$. Condition 3 is $X < \gamma$, since $X \ge 0$ is needed anyway.

Write $f_\gamma(t) = -c t^2 + 2a t + 1$, so $X(\gamma)$ is the root of $f_\gamma$ with $f_\gamma'(X) = 2(a - cX) < 0$. The key identity is

$$f_\gamma(\gamma) = -(1 - \gamma^{-2})\gamma^2 + 2a\gamma + 1 = -(\gamma^2 - 2a\gamma - 2),$$

which is negative for $\gamma > \gamma^*$ and positive for $0 < \gamma < \gamma^*$, where $\gamma^* = a + \sqrt{a^2 + 2}$ is the positive root of $\gamma^2 - 2a\gamma - 2$.

At $\gamma = \gamma^*$ the value $t = \gamma^*$ is a root of $f_{\gamma^*}$, and $a = (\gamma^* - 2/\gamma^*)/2$ gives $a - c^*\gamma^* = a - \gamma^* + 1/\gamma^* = -\gamma^*/2 < 0$. So $\gamma^*$ is the stabilizing root: $X(\gamma^*) = \gamma^*$, and $a^2 + c^* = (\gamma^*/2)^2 > 0$. By continuity there is a neighborhood $U$ of $\gamma^*$ and an interval $I$ around $\gamma^*$ such that, for $\gamma \in U$, the Hamiltonian has no imaginary eigenvalue, $X(\gamma) \in I$, $\gamma \in I$, $X(\gamma) > 0$, and $f_\gamma' < 0$ on all of $I$. On $I$ the function $f_\gamma$ is strictly decreasing and is 0 at $X(\gamma)$. So for $\gamma \in U$: $X(\gamma) < \gamma$ if and only if $f_\gamma(\gamma) < 0$, that is, if and only if $\gamma > \gamma^*$. Conditions 1 and 2 hold in $U$, so levels just above $\gamma^*$ are feasible and levels just below are not. By Claim 1 the feasible set is $(\gamma_{\rm opt}, \infty)$, so $\gamma_{\rm opt} = \gamma^*$. For $a = 1$ this is $1 + \sqrt 3 = 2.73205$, and the table on the page shows the change of sign of $\gamma^2 - X^2$ between $\gamma = 2.7$ and $2.75$. $\square$

The test checks Claim 5 for $a = -1, 0, 1, 2$ against the bisection, with relative error at most $10^{-6}$.

## What the tests check

- The Riccati residual is below $10^{-9}$, $X$ is symmetric and positive definite, and $A + R X$ is Hurwitz, on a plant with two states.
- The three conditions fail at $0.99\,\gamma_{\rm opt}$ and hold at $1.01\,\gamma_{\rm opt}$.
- The central controller gives a Hurwitz closed loop matrix and a frequency sweep peak below $\gamma$ and at least $\gamma_{\rm opt}(1 - 10^{-4})$.
- Brute force: 150 random first-order controllers $K(s) = (k_1 s + k_0)/(s + p)$ for each of two scalar plants. Every one that stabilizes has a sweep peak of at least $\gamma_{\rm opt}(1 - 10^{-3})$.
