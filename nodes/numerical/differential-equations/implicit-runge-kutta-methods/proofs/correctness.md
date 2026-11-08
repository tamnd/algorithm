---
title: The stage equations of an implicit Runge-Kutta method are solvable, simplified Newton finds them, and the method converges with its classical order on nonstiff problems
proves: [correctness, termination, convergence]
status: full
---

**Setting.** We use a norm $\|\cdot\|$ on $\mathbb{R}^d$ and, for $Z = (Z_1, \dots, Z_s) \in \mathbb{R}^{sd}$, the norm $\|Z\|_* = \max_i \|Z_i\|$. The function $f : [t_0, T] \times \mathbb{R}^d \to \mathbb{R}^d$ is continuous and Lipschitz in $y$ with constant $L$. The tableau $(A, b, c)$ has $s$ stages, $\|A\|_\infty = \max_i \sum_j |a_{ij}|$ and $\|b\|_1 = \sum_i |b_i|$. For a step from $(t, u)$ with step $k$ write $F_i(Z) = f(t + c_i k, u + Z_i)$ and

$$G(Z) = Z - k (A \otimes I) F(Z), \qquad \text{that is} \quad G_i(Z) = Z_i - k \sum_j a_{ij} F_j(Z).$$

The stage equations are $G(Z) = 0$, and the step map is $\Phi_k(t, u) = u + k \sum_i b_i F_i(Z)$ at the solution $Z$.

**Lemma 1 (the loop).** Let $N$ be the value of line L1. After iteration $n$ of lines L3 to L15, if no failure is reported, $t = t_{n+1}$ and $y = y_{n+1}$, where $t_m = t_0 + mh$ for $m < N$, $t_N = T$, and $y_{m+1}$ is $y_m$ plus the update of line L14 computed from the last iterate $Z$.

*Proof.* Induction on $n$, as for Euler's method: lines L4 and L5 set the grid point and the step, lines L6 to L13 compute $Z$, line L14 the new value and line L15 the new time. $\square$

**Termination.** The outer loop runs $N = \lceil (T - t_0)/h \rceil$ times. The inner loop of lines L9 to L13 runs at most $m_{\max}$ times per step; if the test of line L13 never holds, the algorithm stops with a failure report. So the algorithm always terminates, after at most $N m_{\max}$ Newton iterations.

**Lemma 2 (existence and uniqueness of the stages).** If $k L \|A\|_\infty < 1$, the stage equations $G(Z) = 0$ have exactly one solution.

*Proof.* $G(Z) = 0$ means $Z = \Psi(Z)$ with $\Psi(Z) = k (A \otimes I) F(Z)$. For $Z, W \in \mathbb{R}^{sd}$,

$$\|\Psi_i(Z) - \Psi_i(W)\| \le k \sum_j |a_{ij}|\, L\, \|Z_j - W_j\| \le k L \|A\|_\infty \|Z - W\|_*.$$

So $\Psi$ is a contraction on the complete space $(\mathbb{R}^{sd}, \|\cdot\|_*)$, and Banach's fixed point theorem gives one fixed point. $\square$

**Lemma 3 (the limit of the Newton iteration).** Let $M = I - k (A \otimes J_n)$ be invertible. If the iterates of line L11, $Z^{(\ell+1)} = Z^{(\ell)} - M^{-1} G(Z^{(\ell)})$, converge to some $Z^*$, then $G(Z^*) = 0$. If $f$ is $C^1$ and $\|M^{-1}\|\, k \|A\|_\infty \sup \|f_y(t + c_j k, u + W_j) - J_n\| \le \theta < 1$ on a closed ball around $0$ that the iteration does not leave, the iterates converge to the unique solution with $\|Z^{(\ell)} - Z^*\|_* \le \theta^\ell \|Z^*\|_*$.

*Proof.* Since $G$ is continuous, $G(Z^*) = \lim G(Z^{(\ell)}) = \lim M (Z^{(\ell)} - Z^{(\ell+1)}) = 0$. For the second claim, the iteration map $\Gamma(Z) = Z - M^{-1} G(Z)$ has the derivative

$$\Gamma'(W) = I - M^{-1}\bigl(I - k (A \otimes I) \operatorname{diag}_j f_y(t + c_j k, u + W_j)\bigr) = k\, M^{-1}\bigl((A \otimes I) \operatorname{diag}_j (f_y(\cdot) - J_n)\bigr),$$

because $M - I = -k (A \otimes J_n)$. By the mean value inequality $\Gamma$ is a contraction with factor $\theta$ on the ball, and $Z^* = \Gamma(Z^*)$ gives the rate. $\square$

**Corollary (linear problems).** If $f(t, y) = \Lambda y + g(t)$ with a constant matrix $\Lambda$ and $J_n = \Lambda$, then $\Gamma' = 0$, so $Z^{(1)} = Z^*$ exactly, and in exact arithmetic the second iteration gives $\Delta Z = 0$ and stops the loop. This is why the stiff example of the page needs exactly two iterations per step.

**Lemma 4 (the update with $d$).** If $G(Z) = 0$ and $A$ is nonsingular, then $k \sum_i b_i F_i(Z) = \sum_i d_i Z_i$ with $d^{T} = b^{T}A^{-1}$.

*Proof.* $G(Z) = 0$ says $Z = k (A \otimes I) F$, so $k F = (A^{-1} \otimes I) Z$, and $k (b^{T} \otimes I) F = (b^{T}A^{-1} \otimes I) Z = \sum_i d_i Z_i$. $\square$

So, when the Newton iteration has converged, line L14 computes $\Phi_k(t, y)$ in both of its branches.

**Lemma 5 (stability of one step).** If $k L \|A\|_\infty \le q < 1$, then $\|\Phi_k(t, u) - \Phi_k(t, v)\| \le (1 + k\Lambda) \|u - v\|$ with $\Lambda = L \|b\|_1 / (1 - q)$.

*Proof.* Let $Z$ and $W$ be the stage solutions for $u$ and $v$, and $Y_i = u + Z_i$, $V_i = v + W_i$. Then $Y_i - V_i = u - v + k \sum_j a_{ij} (f(\cdot, Y_j) - f(\cdot, V_j))$, so $\max_i \|Y_i - V_i\| \le \|u - v\| + q \max_j \|Y_j - V_j\|$ and $\max_i \|Y_i - V_i\| \le \|u - v\|/(1 - q)$. Hence

$$\|\Phi_k(t, u) - \Phi_k(t, v)\| \le \|u - v\| + k L \|b\|_1 \max_i \|Y_i - V_i\| \le \Bigl(1 + \frac{k L \|b\|_1}{1 - q}\Bigr) \|u - v\|. \qquad \square$$

**Theorem (convergence of order $p$, nonstiff case).** Assume $h L \|A\|_\infty \le q < 1$, that the tableau satisfies the Butcher order conditions up to order $p$, and that $f$ is $C^p$, so that the local error satisfies $\|\delta(t, k)\| = \|y(t + k) - \Phi_k(t, y(t))\| \le C k^{p+1}$ for $0 < k \le h$ (Butcher's theorem, HNW I, Section II.2; the constant $C$ depends on bounds of the derivatives of $f$ near the solution). If the stage equations are solved exactly, then for $n = 0, \dots, N$

$$\|y(t_n) - y_n\| \le C h^p\, \frac{e^{\Lambda (t_n - t_0)} - 1}{\Lambda}, \qquad \Lambda = \frac{L \|b\|_1}{1 - q}.$$

*Proof.* With $E_n = \|y(t_n) - y_n\|$, Lemma 5 gives $E_{n+1} \le (1 + h_n \Lambda) E_n + C h_n^{p+1} \le e^{h_n\Lambda} E_n + C h^p h_n$, and the same induction as for Euler's and Heun's methods, which is the discrete [Gronwall inequality](/gronwall-inequality/), gives the bound. $\blacksquare$

**What is proved and what is not.** Lemmas 1 to 5 and the theorem are proved above, except Butcher's theorem on the local error, which is cited. The theorem needs $hL\|A\|_\infty < 1$, so it is useless for stiff problems, where $hL \gg 1$. For those, existence of the stage solution and error bounds independent of the stiffness are proved under a one-sided Lipschitz condition $\langle f(t, u) - f(t, v), u - v \rangle \le \nu \|u - v\|^2$ for algebraically stable methods, with orders tied to the stage order (B-convergence, HW II, Sections IV.14 and IV.15). The observed order 2 of the two-stage Radau IIA method on the stiff example of the page is a measurement consistent with that theory. In floating point the iteration stops at a tolerance, and the stopped iterate differs from $Z^*$ by about $\text{tol}\cdot\theta/(1 - \theta)$ times the scale of $y$.

**Remark (the test equation).** For $f(t, y) = \lambda y$, the stage equations read $(I - zA) Y = y_n \mathbb{1}$ with $z = k\lambda$, so $y_{n+1} = (1 + z\, b^{T}(I - zA)^{-1}\mathbb{1})\, y_n = R(z) y_n$ whenever $I - zA$ is invertible. By the corollary the implementation produces exactly this value after one Newton iteration, in exact arithmetic; the tests check it with fractions.
