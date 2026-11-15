---
title: The Lyapunov adaptive laws keep all signals bounded and drive the tracking error to zero
proves: [correctness]
status: full
---

Notation is that of the page. The plant is $\dot x = A x + b u$, the model is $\dot x_m = A_m x_m + b_m r$ with $A_m$ Hurwitz, and $r$ is bounded and piecewise continuous. There are $k^*$, $l^* \ne 0$ with $A + b k^{*T} = A_m$ and $b l^* = b_m$. The error is $e = x - x_m$, $\tilde k = k - k^*$, $\tilde l = l - l^*$, $Q = Q^T \succ 0$, and $P$ solves $A_m^T P + P A_m = -Q$. The laws are $\dot k = -\gamma\,\mathrm{sgn}(l^*)\,x\,b_m^T P e$ and $\dot l = -\gamma\,\mathrm{sgn}(l^*)\,r\,b_m^T P e$ with $\gamma > 0$.

**Claim 0 (P exists).** Because $A_m$ is Hurwitz, $P = \int_0^\infty e^{A_m^T t} Q e^{A_m t}\,dt$ converges, is symmetric positive definite, and is the unique solution of the Lyapunov equation. This is the standard theorem on the [Lyapunov equation](/lyapunov-equation/). The Kronecker form solved in line L1 has the matrix $I \otimes A_m^T + A_m^T \otimes I$, whose eigenvalues are the sums $\lambda_i + \lambda_j$ of eigenvalues of $A_m$. They all have negative real part, so the matrix is invertible and line L1 returns this $P$.

**Claim 1 (error equation).** With $u = k^T x + l r$,
$$\dot e = A x + b(k^T x + l r) - A_m x_m - b_m r = (A + b k^{*T}) x + b \tilde k^T x + b l^* r + b \tilde l r - A_m x_m - b_m r.$$
By matching, $A + b k^{*T} = A_m$ and $b l^* = b_m$, so $\dot e = A_m e + b(\tilde k^T x + \tilde l r)$. Since $b = b_m / l^*$, this is $\dot e = A_m e + \frac{1}{l^*} b_m (\tilde k^T x + \tilde l r)$.

**Claim 2 (V does not increase).** Let $V = e^T P e + (\tilde k^T\tilde k + \tilde l^2)/(\gamma |l^*|)$. Since $k^*$, $l^*$ are constant, $\dot{\tilde k} = \dot k$ and $\dot{\tilde l} = \dot l$. With $s = b_m^T P e$, which equals $e^T P b_m$ because $P$ is symmetric,
$$\dot V = e^T(A_m^T P + P A_m) e + \frac{2}{l^*} s\,(\tilde k^T x + \tilde l r) + \frac{2}{\gamma|l^*|}\big(\tilde k^T \dot k + \tilde l \dot l\big).$$
The laws give $\tilde k^T \dot k + \tilde l \dot l = -\gamma\,\mathrm{sgn}(l^*)\, s\,(\tilde k^T x + \tilde l r)$, so the last term is $-\frac{2\,\mathrm{sgn}(l^*)}{|l^*|} s (\tilde k^T x + \tilde l r) = -\frac{2}{l^*} s (\tilde k^T x + \tilde l r)$, which cancels the middle term. Hence $\dot V = -e^T Q e \le -\lambda_{\min}(Q)\,|e|^2$.

**Claim 3 (bounded signals).** By Claim 2, $V(t) \le V(0)$ for all $t$ in the interval of existence. So $e^T P e \le V(0)$ gives $|e|^2 \le V(0)/\lambda_{\min}(P)$, and $|\tilde k|^2 + \tilde l^2 \le \gamma |l^*| V(0)$. The model state $x_m$ is bounded because $A_m$ is Hurwitz and $r$ is bounded. So $x = e + x_m$, $k$ and $l$ are bounded, and then $u$ is bounded. The right-hand side of the closed loop is locally Lipschitz in the state, and a bounded solution cannot escape in finite time, so the solution exists for all $t \ge 0$ and is bounded.

**Claim 4 (the error goes to zero).** Integrate $\dot V = -e^T Q e$ from $0$ to $T$: $\int_0^T e^T Q e\,dt = V(0) - V(T) \le V(0)$. So $e \in L_2$. By Claim 1 and Claim 3, $\dot e$ is bounded, so $e$ is uniformly continuous, and so is $e^T Q e$ (a product of bounded, uniformly continuous functions). Its integral over $[0, \infty)$ is finite, so by [Barbalat's lemma](/barbalat-lemma/) $e^T Q e \to 0$, and $e(t) \to 0$ because $Q \succ 0$. $\square$

**Remark (parameter convergence).** The proof above gives no convergence of $\tilde k$ and $\tilde l$. If the regressor $w = (x_m, r)$ of the model is persistently exciting, that is, $\int_t^{t + T_0} w w^T d\tau \succeq \alpha_0 T_0 I$ for some $\alpha_0, T_0 > 0$ and all $t$, then the equilibrium $(e, \tilde k, \tilde l) = 0$ is exponentially attractive (Ioannou and Sun, Chapter 4 and Section 6.2, theorem). Without excitation the gains can stop at any point with $\tilde k^T x + \tilde l r \equiv 0$ along the limit trajectory. For the scalar example of the page with $r = 1$, this set is the line $k + l = -0.5$; the tests check both cases.

**Numerical check.** The tests compute $V$ along the RK4 solution and check that $V(0) - V(T)$ equals the Simpson integral of $e^T Q e$ within $10^{-6}$, which is Claim 2 in integral form.
