---
title: The Nessyahu-Tadmor scheme is conservative and consistent, and for linear advection with the minmod-theta slope it is TVD for Courant numbers up to one half
proves: [correctness]
status: full
---

**Setting.** The scheme stores cell averages $u_j$ on a uniform grid with width $\Delta x$ and cell centers $x_j$, with $\lambda = \Delta t/\Delta x$. Lines L2 to L4 of the page compute the slopes $u'_j = S(u_{j-1}, u_j, u_{j+1})$ and $f'_j = S(f(u_{j-1}), f(u_j), f(u_{j+1}))$ with

$$S(a, b, c) = \mathrm{minmod}\big(\theta(b - a), \tfrac12(c - a), \theta(c - b)\big), \qquad 1 \le \theta \le 2,$$

the midpoint values $u_j^{n+1/2} = u_j - \frac{\lambda}{2}f'_j$, and the averages over the staggered cells $[x_j, x_{j+1}]$:

$$w_{j+1/2} = \tfrac12(u_j + u_{j+1}) + \tfrac18(u'_j - u'_{j+1}) - \lambda\big(f(u_{j+1}^{n+1/2}) - f(u_j^{n+1/2})\big).$$

The next step applies the same formula to the $w$ values and gives averages over the original cells. For systems, every line acts componentwise.

**Where the formula comes from.** Integrate $u_t + f(u)_x = 0$ over $[x_j, x_{j+1}] \times [t^n, t^{n+1}]$ and divide by $\Delta x$. The average of the piecewise linear data $u_j + u'_j(x - x_j)/\Delta x$ over the right half of cell $j$ is $u_j + \frac14 u'_j$, and over the left half of cell $j + 1$ it is $u_{j+1} - \frac14 u'_{j+1}$. Their mean is the first two terms. The fluxes are needed only at $x_j$ and $x_{j+1}$, the centers of the old cells, where the data are smooth for a short time when $\lambda\max|f'| \le \frac12$, so no Riemann problem appears. The midpoint rule in time with the Taylor value $u_j^{n+1/2}$ gives the last term.

**Lemma 1 (conservation and consistency).** On a periodic grid $\sum_j w_{j+1/2} = \sum_j u_j$. If $u_{j-1} = \dots = u_{j+2} = \bar u$, then $w_{j+1/2} = \bar u$.

*Proof.* Each $u_j$ appears with the weight $\frac12$ in $w_{j-1/2}$ and in $w_{j+1/2}$. Each $u'_j$ appears with $+\frac18$ in $w_{j+1/2}$ and $-\frac18$ in $w_{j-1/2}$, and each $f(u_j^{n+1/2})$ with $+\lambda$ and $-\lambda$. So the sum is $\sum_j u_j$. For constant data all slopes are zero, both midpoint values are $\bar u$, and the flux difference is zero. $\square$

The test checks Lemma 1 exactly in `Fraction` arithmetic for Burgers' equation and three values of $\theta$. By the [Lax-Wendroff theorem](/lax-wendroff-theorem/), bounded $L^1_{loc}$ limits of the scheme are weak solutions.

**Lemma 2 (the slope).** $S$ is odd and positively homogeneous, so $S(ca, cb, cc) = c\,S(a, b, c)$ for every real $c$. If $u_j - u_{j-1}$ and $u_{j+1} - u_j$ do not have the same strict sign, $u'_j = 0$. Otherwise $u'_j$ has their sign and $|u'_j| \le \theta\min(|u_j - u_{j-1}|, |u_{j+1} - u_j|)$.

*Proof.* minmod is odd and positively homogeneous in its three arguments. It returns zero unless all three have one strict sign, and then it returns the one of least size, which is at most $\theta$ times each one-sided difference. $\square$

**Lemma 3 (the linear case).** Let $f(u) = cu$ and $\nu = \lambda c$. Then

$$w_{j+1/2} = \big(\tfrac12 + \nu\big)A_j + \big(\tfrac12 - \nu\big)B_{j+1}, \qquad A_j = u_j + \tfrac{1 - 2\nu}{4}u'_j, \quad B_j = u_j - \tfrac{1 + 2\nu}{4}u'_j.$$

*Proof.* By Lemma 2, $f'_j = c\,u'_j$, so $u_j^{n+1/2} = u_j - \frac{\nu}{2}u'_j$ and $f(u_j^{n+1/2}) = c u_j - \frac{c\nu}{2}u'_j$. Multiply the flux difference by $\lambda$; then

$$w_{j+1/2} = \big(\tfrac12 + \nu\big)u_j + \big(\tfrac12 - \nu\big)u_{j+1} + \kappa(u'_j - u'_{j+1}), \qquad \kappa = \tfrac18 - \tfrac{\nu^2}{2} = \tfrac{(1 - 2\nu)(1 + 2\nu)}{8}.$$

Now $\kappa = (\frac12 + \nu)\frac{1 - 2\nu}{4} = (\frac12 - \nu)\frac{1 + 2\nu}{4}$, which gives the split into $A_j$ and $B_{j+1}$. At $\nu = \frac12$, $\kappa = 0$, $A_j = u_j$ and the weights are $1$ and $0$, so $w_{j+1/2} = u_j$. $\square$

The test `test_hand_trace_against_the_linear_formula` checks the formula with $\kappa$ exactly in `Fraction` arithmetic, and `test_courant_one_half_is_an_exact_shift` checks the end point $\nu = \frac12$: the scheme moves the data exactly by half a cell.

**Theorem 1 (TVD for linear advection).** For $f(u) = cu$, $|\nu| \le \frac12$ and $1 \le \theta \le 2$, on a periodic grid, $TV(w) \le TV(u)$ and $\min_k u_k \le w_{j+1/2} \le \max_k u_k$, where $TV(u) = \sum_j |u_{j+1} - u_j|$. The same holds for the step from $w$ back to the original grid, so for every number of steps.

*Proof.* The factors $\frac{1 - 2\nu}{4}$ and $\frac{1 + 2\nu}{4}$ lie in $[0, \frac12]$, and by Lemma 2 $|u'_j| \le 2|u_{j+1} - u_j|$ with the same sign. So $A_j$ lies between $u_j$ and $u_{j+1}$. In the same way $B_j$ lies between $u_{j-1}$ and $u_j$. In the sequence $u_0, A_0, u_1, A_1, u_2, \dots$, each pair of neighbors $u_j, A_j, u_{j+1}$ is monotone, so the total variation of this sequence equals $TV(u)$. The sequence $(A_j)$ is a subsequence, so by the triangle inequality $TV(A) \le TV(u)$. In the same way $TV(B) \le TV(u)$. By Lemma 3 with weights $\frac12 \pm \nu \ge 0$ that add up to 1,

$$TV(w) = \sum_j \big|(\tfrac12 + \nu)(A_{j+1} - A_j) + (\tfrac12 - \nu)(B_{j+2} - B_{j+1})\big| \le (\tfrac12 + \nu)TV(A) + (\tfrac12 - \nu)TV(B) \le TV(u).$$

Each $w_{j+1/2}$ is a convex combination of $A_j$ and $B_{j+1}$, which lie between old values, so no new extrema appear. The step back is the same formula on the grid of the $w$ values. $\square$

The test `test_tvd_and_no_new_extrema_for_advection` checks Theorem 1 for $\theta = 1, 1.5, 2$ and $\nu = 0.2, 0.5, -0.4$.

**What is not proved here.** For nonlinear scalar laws this page does not prove TVD; the test checks it for Burgers' equation on one step problem, which is a measurement. For the Euler equations no TVD or positivity property is proved. Second order accuracy is measured: the $L^1$ orders are about 2 on a smooth advection wave and on a smooth Euler wave. The growth of the error at small Courant numbers is also measured, not proved: in Lemma 3 the coefficient $\kappa$ tends to $\frac18$ as $\nu \to 0$, so the scheme keeps the averaging $\frac12(u_j + u_{j+1})$ in every step, and the number of steps grows like $1/\Delta t$.
