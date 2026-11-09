---
title: ADMM has a nonincreasing Lyapunov function and an O(1/K) ergodic rate for the objective and the residual
proves: [correctness, convergence-rate]
status: full
---

The problem is $\min f(x) + g(z)$ subject to $Ax + Bz = c$. Write $p(x, z) = f(x) + g(z)$ and $L_0(x, z, y) = p(x, z) + y^\top(Ax + Bz - c)$. The method, in the unscaled form with $y_k = \rho u_k$, is

$$x_{k+1} \in \operatorname{argmin}_x f(x) + \tfrac\rho2\|Ax + Bz_k - c + y_k/\rho\|^2,\quad z_{k+1} \in \operatorname{argmin}_z g(z) + \tfrac\rho2\|Ax_{k+1} + Bz - c + y_k/\rho\|^2,$$

$$r_{k+1} = Ax_{k+1} + Bz_{k+1} - c, \qquad y_{k+1} = y_k + \rho r_{k+1}.$$

We assume:

- (A1) $f$ and $g$ are closed, proper and convex, and $\rho > 0$;
- (A2) $L_0$ has a saddle point $(x^*, z^*, y^*)$: $L_0(x^*, z^*, y) \le L_0(x^*, z^*, y^*) \le L_0(x, z, y^*)$ for all $x, z, y$. Then $(x^*, z^*)$ is optimal with value $p^* = p(x^*, z^*)$, and $Ax^* + Bz^* = c$;
- (A3) both subproblems have minimizers at each step.

**Lemma 1 (optimality of the two steps).** For each $k \ge 0$,

$$-A^\top\big(y_{k+1} - \rho B(z_{k+1} - z_k)\big) \in \partial f(x_{k+1}), \qquad -B^\top y_{k+1} \in \partial g(z_{k+1}).$$

*Proof.* The $x$-step gives $0 \in \partial f(x_{k+1}) + \rho A^\top(Ax_{k+1} + Bz_k - c + y_k/\rho)$, and $Ax_{k+1} + Bz_k - c + y_k/\rho = y_{k+1}/\rho - B(z_{k+1} - z_k)$. The $z$-step gives $0 \in \partial g(z_{k+1}) + \rho B^\top(r_{k+1} + y_k/\rho) = \partial g(z_{k+1}) + B^\top y_{k+1}$. $\square$

So $z_{k+1}$ minimizes $L_0(x_{k+1}, \cdot, y_{k+1})$ exactly, and $x_{k+1}$ minimizes $L_0(\cdot, z_{k+1}, y_{k+1})$ up to the dual residual $s_{k+1} = \rho A^\top B(z_{k+1} - z_k)$.

**Lemma 2 (one step).** For each $(x, z)$ with $Ax + Bz = c$, each $\lambda$ and each $k \ge 0$,

$$p(x_{k+1}, z_{k+1}) - p(x, z) + \lambda^\top r_{k+1} \le \frac{\|\lambda - y_k\|^2 - \|\lambda - y_{k+1}\|^2}{2\rho} + \frac\rho2\big(\|B(z_k - z)\|^2 - \|B(z_{k+1} - z)\|^2\big) - \frac\rho2\|r_{k+1} - B(z_{k+1} - z_k)\|^2.$$

*Proof.* Write $\Delta = B(z_{k+1} - z_k)$ and $r = r_{k+1}$. The subgradient inequalities for the two subgradients of Lemma 1 give

$$f(x_{k+1}) \le f(x) + (y_{k+1} - \rho\Delta)^\top A(x - x_{k+1}), \qquad g(z_{k+1}) \le g(z) + y_{k+1}^\top B(z - z_{k+1}).$$

Since $Ax + Bz = c$, we have $A(x - x_{k+1}) + B(z - z_{k+1}) = -r$ and $A(x - x_{k+1}) = -r + B(z_{k+1} - z)$. Add the two inequalities and $\lambda^\top r$:

$$p(x_{k+1}, z_{k+1}) - p(x, z) + \lambda^\top r \le (\lambda - y_{k+1})^\top r + \rho\Delta^\top r - \rho\Delta^\top B(z_{k+1} - z).$$

Now use $r = (y_{k+1} - y_k)/\rho$ and the identity $2(a - b)^\top(b - e) = \|a - e\|^2 - \|a - b\|^2 - \|b - e\|^2$ twice:

$$(\lambda - y_{k+1})^\top r = \tfrac{1}{2\rho}\big(\|\lambda - y_k\|^2 - \|\lambda - y_{k+1}\|^2\big) - \tfrac\rho2\|r\|^2,$$

$$-\rho\Delta^\top B(z_{k+1} - z) = \tfrac\rho2\big(\|B(z_k - z)\|^2 - \|B(z_{k+1} - z)\|^2\big) - \tfrac\rho2\|\Delta\|^2.$$

Finally $-\tfrac\rho2\|r\|^2 + \rho\Delta^\top r - \tfrac\rho2\|\Delta\|^2 = -\tfrac\rho2\|r - \Delta\|^2$. $\square$

**Theorem 1 (ergodic rate).** Let $\bar x_K = \frac1K\sum_{k=1}^K x_k$, $\bar z_K = \frac1K\sum_{k=1}^K z_k$ and $\bar r_K = A\bar x_K + B\bar z_K - c$. For each feasible $(x, z)$ and each $\lambda$,

$$p(\bar x_K, \bar z_K) - p(x, z) + \lambda^\top\bar r_K \le \frac{C(\lambda, z)}{K}, \qquad C(\lambda, z) = \frac{\|\lambda - y_0\|^2}{2\rho} + \frac\rho2\|B(z_0 - z)\|^2.$$

In particular, with $D = \tfrac{1}{2\rho}(\|y_0 - y^*\| + 1)^2 + \tfrac\rho2\|B(z_0 - z^*)\|^2$:

$$-\|y^*\|\,\|\bar r_K\| \le p(\bar x_K, \bar z_K) - p^* \le \frac{C(0, z^*)}{K}, \qquad \|\bar r_K\| \le \frac{D}{K}.$$

*Proof.* Add Lemma 2 for $k = 0, \ldots, K - 1$, drop the last term, which is not positive, and let the sums telescope. The left side becomes $\sum_{k=1}^K\big(p(x_k, z_k) - p(x, z) + \lambda^\top r_k\big)$. Since $p$ is convex and $r$ is affine in $(x, z)$, Jensen's inequality bounds $K$ times the left side of the claim by this sum. For the particular bounds take $(x, z) = (x^*, z^*)$. The upper bound on $p - p^*$ is the case $\lambda = 0$. The lower bound is the saddle point inequality $p^* = L_0(x^*, z^*, y^*) \le L_0(\bar x_K, \bar z_K, y^*) = p(\bar x_K, \bar z_K) + y^{*\top}\bar r_K$. For the residual, assume $\bar r_K \ne 0$ and take $\lambda = y^* + \bar r_K/\|\bar r_K\|$. The left side is $\big(p(\bar x_K, \bar z_K) - p^* + y^{*\top}\bar r_K\big) + \|\bar r_K\|$, and the bracket is at least $0$ by the saddle point inequality. Also $\|\lambda - y_0\| \le \|y^* - y_0\| + 1$. $\square$

**Theorem 2 (Lyapunov function).** Let $V_k = \tfrac1\rho\|y_k - y^*\|^2 + \rho\|B(z_k - z^*)\|^2$. Then $V_1 \le V_0$, and for each $k \ge 1$,

$$V_{k+1} \le V_k - \rho\|r_{k+1}\|^2 - \rho\|B(z_{k+1} - z_k)\|^2.$$

So $\sum_{k \ge 2}\|r_k\|^2 \le V_0/\rho$, the residual $r_k$ and the change $B(z_{k+1} - z_k)$ go to $0$, and $\min_{2 \le j \le K+1}\|r_j\|^2 \le V_0/(\rho K)$.

*Proof.* Take $(x, z, \lambda) = (x^*, z^*, y^*)$ in Lemma 2. The left side is $L_0(x_{k+1}, z_{k+1}, y^*) - L_0(x^*, z^*, y^*) \ge 0$. The first two terms on the right are $\tfrac12(V_k - V_{k+1})$. So $V_{k+1} \le V_k - \rho\|r_{k+1} - \Delta\|^2$ with $\Delta = B(z_{k+1} - z_k)$, which gives $V_1 \le V_0$. For $k \ge 1$, Lemma 1 at steps $k$ and $k + 1$ gives $-B^\top y_k \in \partial g(z_k)$ and $-B^\top y_{k+1} \in \partial g(z_{k+1})$. The subdifferential of a convex function is monotone, so $-(y_{k+1} - y_k)^\top B(z_{k+1} - z_k) \ge 0$, that is, $\rho r_{k+1}^\top\Delta \le 0$. Then $\|r_{k+1} - \Delta\|^2 = \|r_{k+1}\|^2 - 2r_{k+1}^\top\Delta + \|\Delta\|^2 \ge \|r_{k+1}\|^2 + \|\Delta\|^2$. Adding the inequalities for $k = 1, \ldots, K$ gives the sum bound, and the smallest term is at most the mean. $\blacksquare$
