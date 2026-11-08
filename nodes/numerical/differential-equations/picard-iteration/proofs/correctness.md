---
title: Picard iteration converges for Lipschitz f, and its trapezoidal grid version converges to the trapezoidal solution when L times the grid spacing is below 2
proves: [correctness, termination, convergence]
status: full
---

**Setting.** $f : [t_0, T] \times \mathbb{R}^d \to \mathbb{R}^d$ is continuous and satisfies $\|f(t, u) - f(t, v)\| \le L\|u - v\|$ with $L > 0$. Let $M = \max_{t_0 \le t \le T}\|f(t, y_0)\|$.

## The continuous iteration

**Theorem 1.** The iterates $y^{(0)} = y_0$, $y^{(k+1)}(t) = y_0 + \int_{t_0}^t f(s, y^{(k)}(s))\,ds$ are continuous on $[t_0, T]$ and converge uniformly to a solution $y$ of the initial value problem, and for $t \in [t_0, T]$

$$\|y(t) - y^{(k)}(t)\| \le \frac{M}{L}\,\frac{(L(t - t_0))^{k+1}}{(k+1)!}\,e^{L(t - t_0)}.$$

*Proof.* Each iterate is continuous, since it is an integral of a continuous function. Let $d_k(t) = \|y^{(k+1)}(t) - y^{(k)}(t)\|$. Then $d_0(t) = \|\int_{t_0}^t f(s, y_0)\,ds\| \le M(t - t_0)$, and

$$d_{k}(t) \le \int_{t_0}^t \|f(s, y^{(k)}(s)) - f(s, y^{(k-1)}(s))\|\,ds \le L\int_{t_0}^t d_{k-1}(s)\,ds.$$

By induction $d_k(t) \le \frac{M}{L}\frac{(L(t - t_0))^{k+1}}{(k+1)!}$. The series $\sum_k d_k$ converges uniformly, so $y^{(k)} = y_0 + \sum_{j < k}(y^{(j+1)} - y^{(j)})$ converges uniformly to a continuous $y$. Passing to the limit in the recursion (the integrand converges uniformly by the Lipschitz condition) gives $y(t) = y_0 + \int_{t_0}^t f(s, y(s))\,ds$, so $y$ is $C^1$ and solves the problem. Finally, with $x = L(t - t_0)$,

$$\|y(t) - y^{(k)}(t)\| \le \sum_{j \ge k} d_j(t) \le \frac{M}{L}\sum_{j \ge k}\frac{x^{j+1}}{(j+1)!} \le \frac{M}{L}\frac{x^{k+1}}{(k+1)!}\sum_{i \ge 0}\frac{x^i}{i!},$$

using $(k + 1 + i)! \ge (k+1)!\,i!$. $\square$

The solution is unique by the [Gronwall inequality](/gronwall-inequality/): two solutions $y, z$ satisfy $\|y(t) - z(t)\| \le L\int_{t_0}^t\|y - z\|$, so $y = z$.

## The discrete iteration

Fix one window $[a, b]$ with nodes $\tau_i = a + i\Delta\tau$, $i = 0, \dots, m$, and start value $y_s$. For $Y = (Y_0, \dots, Y_m)$ define $\Phi(Y) = Z$ by line L6:

$$Z_0 = y_s, \qquad Z_i = y_s + \sum_{j=0}^{i} w_{ij} f(\tau_j, Y_j), \quad w_{i0} = w_{ii} = \frac{\Delta\tau}{2}, \; w_{ij} = \Delta\tau \;(0 < j < i).$$

(Unrolling the recursion $Z_i = Z_{i-1} + \frac{\Delta\tau}{2}(F_{i-1} + F_i)$ gives these weights.)

**Lemma 2 (the loop).** After sweep $k$ of lines L4 to L9, $Y = \Phi^k(Y^{(0)})$ with $Y^{(0)} = (y_s, \dots, y_s)$. Line L10 passes $Y_m$ as the start value of the next window.

*Proof.* Lines L5 and L6 compute $Z = \Phi(Y)$ from the old $Y$ only, and line L8 replaces $Y$ by $Z$. $\square$

**Termination.** Each window runs at most $K$ sweeps, and there are $W$ windows, so at most $WK$ sweeps of $m + 1$ evaluations each are made.

**Lemma 3 (fixed points are trapezoidal solutions).** $Y = \Phi(Y)$ holds exactly when $Y_0 = y_s$ and $Y_i = Y_{i-1} + \frac{\Delta\tau}{2}\bigl(f(\tau_{i-1}, Y_{i-1}) + f(\tau_i, Y_i)\bigr)$ for $i = 1, \dots, m$, that is, when $Y$ is the solution of the implicit trapezoidal method with step $\Delta\tau$.

*Proof.* Subtract the formulas for $Z_i$ and $Z_{i-1}$. $\square$

**Theorem 4 (contraction).** If $q_0 = L\Delta\tau/2 < 1$, then for every $q \in (q_0, 1)$ there is $r \in (0, 1)$ such that $\Phi$ is a contraction with factor $q$ in the norm $\|E\|_r = \max_i r^i\|E_i\|$. Hence $\Phi$ has a unique fixed point $Y^*$ (the trapezoidal solution of Lemma 3), and

$$\max_i\|Y^{(k)}_i - Y^*_i\| \le r^{-m}q^k\max_i\|Y^{(0)}_i - Y^*_i\|.$$

*Proof.* Let $E = Y - V$ and $\|E\|_r = \rho$, so that $\|E_j\| \le r^{-j}\rho$. Then

$$r^i\|\Phi(Y)_i - \Phi(V)_i\| \le r^i\sum_{j=0}^{i} w_{ij}L\|E_j\| \le L\rho\sum_{j=0}^i w_{ij}r^{i-j} \le L\Delta\tau\,\rho\Bigl(\frac12 + \sum_{l=1}^{\infty}r^l\Bigr) = L\Delta\tau\,\rho\Bigl(\frac12 + \frac{r}{1 - r}\Bigr),$$

where the term $j = i$ contributes $\frac12$ and the others at most $r^{i-j}$ (the term $j = 0$ only $\frac12 r^i$). The factor $L\Delta\tau(\frac12 + \frac{r}{1 - r})$ tends to $q_0$ as $r \to 0$, so it is at most $q$ for small $r > 0$. Banach's fixed point theorem on the complete space $(\mathbb{R}^{d(m+1)}, \|\cdot\|_r)$ gives the fixed point and $\|Y^{(k)} - Y^*\|_r \le q^k\|Y^{(0)} - Y^*\|_r$. The norms satisfy $r^m\max_i\|E_i\| \le \|E\|_r \le \max_i\|E_i\|$, which gives the bound in the max norm. $\square$

The factor $r^{-m}$ can be very large: it is the price of a long window, and it shows up as the transient growth of the iterates before they converge. For the linear problem $f = \lambda y$ the error propagates by the matrix $\lambda Q$, $Q$ lower triangular with diagonal $(0, \frac{\Delta\tau}{2}, \dots, \frac{\Delta\tau}{2})$, whose spectral radius is $|\lambda|\Delta\tau/2$; so $L\Delta\tau/2 < 1$ is also necessary for convergence from all starting guesses in that case.

**Corollary 5 (convergence of the method).** If $L\Delta\tau/2 < 1$, the stopping test holds after finitely many sweeps in exact arithmetic (the differences $\|Y^{(k+1)} - Y^{(k)}\|$ tend to 0), and the limit is the trapezoidal solution, whose global error at the grid points is $O(\Delta\tau^2)$ for a $C^3$ solution (the trapezoidal method is A-stable and of order 2; HNW I, Section II.3 for the convergence argument of one-step methods, and Section II.7 for implicit methods). Over $W$ windows the start value of each window is the trapezoidal value of the previous one, so the whole result is the trapezoidal solution on $[t_0, T]$ up to the stopping tolerance. $\blacksquare$

**What is proved and what is observed.** Theorem 1, Lemmas 2 and 3, Theorem 4 and the termination bound are proved above; the order of the trapezoidal method is cited. In floating point the sweeps stall at a rounding level proportional to $(b - a)\max\|f\|$, which is why line L9 uses a relative test; the iteration counts and the stall level on the page are observations.
