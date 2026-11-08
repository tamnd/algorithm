---
title: RKF45 takes fourth-order steps, its estimate is asymptotically exact, and the loop terminates
proves: [correctness, termination]
status: full
---

**Setting.** $f : [t_0, T] \times \mathbb{R}^d \to \mathbb{R}^d$ is continuous and Lipschitz in $y$, so the problem has a unique solution $y$ ([Picard-Lindelöf theorem](/picard-lindelof-theorem/)). The tableau is the Fehlberg tableau of the page, with $c_i = \sum_j a_{ij}$. We write $y_4 = y + h\sum_i b_i k_i$ and $y_5 = y + h\sum_i \hat b_i k_i$ for the two results of one step from $(t, y)$, and $\mathrm{est} = y_5 - y_4 = h\sum_i (\hat b_i - b_i) k_i$.

**Lemma 1 (orders of the two formulas).** The weights $b$ satisfy the 8 order conditions of the rooted trees with at most 4 vertices, and not all 9 conditions of order 5. The weights $\hat b$ satisfy all 17 conditions of the trees with at most 5 vertices.

*Proof.* Each condition is an identity between rational numbers, $\sum_i b_i \Phi_i(\tau) = 1/\gamma(\tau)$. The test file evaluates all 17 conditions in exact rational arithmetic (`fractions.Fraction`) for both weight vectors. For $b$, the first failure is $\sum_i b_i c_i^4 \ne \frac15$. $\square$

By Butcher's theorem (HNW I, Section II.2), Lemma 1 gives local errors $\ell_4 = y(t + h) - y_4 = O(h^5)$ and $\ell_5 = y(t + h) - y_5 = O(h^6)$, for the exact start value $y = y(t)$ and $f \in C^5$.

**Theorem 1 (the estimate).** For $f \in C^5$ and a start on the exact solution, $\mathrm{est} = \ell_4 + O(h^6)$. If the principal error term of $\ell_4$, $h^5 \psi(t)$, has $\psi(t) \ne 0$, then $\|\mathrm{est}\| / \|\ell_4\| \to 1$ as $h \to 0$.

*Proof.* $\mathrm{est} = y_5 - y_4 = (y(t + h) - y_4) - (y(t + h) - y_5) = \ell_4 - \ell_5$, and $\ell_5 = O(h^6)$. With $\ell_4 = h^5\psi(t) + O(h^6)$ the ratio is $1 + O(h)$. $\square$

This is an asymptotic result. It says nothing for large $h$, and it is the reason why the controller works on smooth problems.

**Theorem 2 (what an accepted step does).** Each accepted step of length $h$ replaces $(t, y)$ by $(t + h, y_4)$, one step of an explicit Runge-Kutta method of order 4. So the computed values are the values of the fourth-order method on the grid of accepted points, and the convergence theory of [Runge-Kutta methods](/runge-kutta-methods/) applies to each fixed grid.

*Proof.* Line L7 sets $y \leftarrow y_4$ only when the test passes, and line L3 makes the last step end at $T$. A rejected step changes only $h$. $\square$

**Theorem 3 (termination).** Assume $\mathrm{atol} > 0$ and $\|f(t, u)\|_\infty \le K$ for all $t \in [t_0, T]$ and $u \in \mathbb{R}^d$. Let $\sigma = \sum_i |\hat b_i - b_i|$, $h^* = \mathrm{atol}/(\sigma K)$ and $\eta = \min(h_0, 0.2h^*)$, where $h_0$ is the first trial step. Then the loop of line L2 ends after finitely many iterations.

*Proof.* **(a) Small steps pass.** Each slope satisfies $\|k_i\|_\infty \le K$, so $|\mathrm{est}_m| \le h\sigma K$. Each scale factor $\mathrm{atol} + \mathrm{rtol}\max(|y_m|, |y_{4,m}|)$ is at least $\mathrm{atol}$. So the RMS error satisfies $\mathrm{err} \le h\sigma K/\mathrm{atol} = h/h^*$, and a trial with $h \le h^*$ is accepted.

**(b) The step never collapses.** Line L8 sets $h' = \varphi h$ with $\varphi = 5$ if $\mathrm{err} = 0$ and $\varphi = \min(5, \max(0.2, 0.9\,\mathrm{err}^{-1/5}))$ otherwise. The map $x \mapsto \min(5, \max(0.2, x))$ is non-decreasing, and $\mathrm{err} \le h/h^*$, so $h' \ge \min(5h, \max(0.2h, g(h)))$ with $g(h) = 0.9h^{4/5}h^{*1/5}$. If $h \ge h^*$, then $h' \ge \min(5h, 0.2h) \ge 0.2h^*$. If $h \le 0.9^5 h^*$, then $g(h) \ge h$, so $h' \ge h$. If $0.9^5 h^* < h < h^*$, then $g(h) \ge g(0.9^5h^*) = 0.9^5h^* > 0.2h^*$ and $5h > 0.2h^*$, so $h' \ge 0.2h^*$. In each case $h' \ge \min(h, 0.2h^*)$. By induction, each trial step that line L3 does not shorten has $h \ge \eta$, and a shortened trial has $h = T - t$. So each trial has length at least $\min(\eta, T - t)$.

**(c) Counting.** An accepted step that is not the last advances $t$ by at least $\eta$, so there are at most $\lceil (T - t_0)/\eta \rceil$ accepted steps. Between two accepted steps $t$ is fixed. A rejected trial has $\mathrm{err} > 1$, so $\varphi \le \max(0.2, 0.9) = 0.9$, and the step shrinks by a factor of at least $1/0.9$. It cannot shrink below $\min(\eta, T - t) > 0$ by (b), so each run of rejections is finite. Hence the loop ends. $\blacksquare$

Without the bound $K$ the loop can run until the guard on the number of steps or on the step size stops it. This happens, for example, when the solution blows up inside $[t_0, T]$, as for $y' = 1/(1 - t)$ on $[0, 2]$. The test file checks that the implementation then raises an error instead of looping.

**What is not proved.** The controller keeps each accepted local error estimate below the tolerance. It does not bound the global error by the tolerance. The global error is a sum of local errors, each carried forward by the problem (see [global error](/global-error/)). Tolerance proportionality, a global error roughly proportional to the tolerance, is an observation on smooth problems and an asymptotic result under extra assumptions on the controller, not a theorem for the code as written.
