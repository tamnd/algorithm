---
title: The method of multipliers is the proximal point method on the dual, with O(1/k) dual gap and O(1/k^(1/2)) residual
proves: [correctness, convergence-rate]
status: full
---

The problem is $\min f(x)$ subject to $Ax = b$, where $f$ is closed, proper and convex. The Lagrangian is $L(x, y) = f(x) + y^\top(Ax - b)$, the dual function is $d(y) = \inf_x L(x, y)$, and the augmented Lagrangian is $L_\rho(x, y) = L(x, y) + \tfrac{\rho}{2}\|Ax - b\|^2$ with $\rho > 0$. The method sets $x_{k+1} \in \operatorname{argmin}_x L_\rho(x, y_k)$, $r_{k+1} = Ax_{k+1} - b$ and $y_{k+1} = y_k + \rho r_{k+1}$. We assume:

- (A1) there is a primal optimal $x^*$ and a dual optimal $y^*$ with $f(x^*) = d(y^*)$, that is, strong duality holds and both optima are attained (for example, when $f$ is finite on $\mathbb{R}^n$ and the problem has a solution);
- (A2) for each $y$, the function $L_\rho(\cdot, y)$ has a minimizer (for example, when $f + \tfrac{\rho}{2}\|Ax\|^2$ is strongly convex).

**Lemma 1 (each step makes a dual point with a known value).** $x_{k+1}$ minimizes the ordinary Lagrangian $L(\cdot, y_{k+1})$. So $d(y_{k+1}) = f(x_{k+1}) + y_{k+1}^\top r_{k+1}$, and $r_{k+1}$ is a supergradient of $d$ at $y_{k+1}$: $d(y) \le d(y_{k+1}) + r_{k+1}^\top(y - y_{k+1})$ for all $y$.

*Proof.* The optimality condition of line L2 is $0 \in \partial f(x_{k+1}) + A^\top y_k + \rho A^\top r_{k+1} = \partial f(x_{k+1}) + A^\top y_{k+1}$. The right side is the subdifferential of the convex function $L(\cdot, y_{k+1})$ at $x_{k+1}$, so $x_{k+1}$ minimizes it, and $d(y_{k+1}) = L(x_{k+1}, y_{k+1})$. For any $y$, $d(y) \le L(x_{k+1}, y) = L(x_{k+1}, y_{k+1}) + (y - y_{k+1})^\top r_{k+1}$. $\square$

**Lemma 2 (the multiplier update is a proximal step).** Let $\varphi = -d$, a closed proper convex function. Then $y_{k+1} = \operatorname{prox}_{\rho\varphi}(y_k)$.

*Proof.* The point $\operatorname{prox}_{\rho\varphi}(y_k)$ is the unique $y$ with $0 \in \partial\varphi(y) + (y - y_k)/\rho$. At $y = y_{k+1}$ we have $(y_{k+1} - y_k)/\rho = r_{k+1}$, and by Lemma 1, $-r_{k+1} \in \partial\varphi(y_{k+1})$. So $0 \in \partial\varphi(y_{k+1}) + (y_{k+1} - y_k)/\rho$. $\square$

**Theorem 1 (dual rate).** For each $k \ge 1$, $d^* - d(y_k) \le \|y_0 - y^*\|^2/(2\rho k)$, where $d^* = d(y^*) = f(x^*)$.

*Proof.* By Lemma 2, $(y_k)$ is the proximal point sequence for $\varphi$ with parameter $\rho$, and $y^*$ minimizes $\varphi$. The theorem of the [proximal point method](/proximal-point-method/) gives $\varphi(y_k) - \varphi(y^*) \le \|y_0 - y^*\|^2/(2\rho k)$. $\square$

**Theorem 2 (residual rate).** For each $k \ge 1$, $\|r_k\| \le \|y_0 - y^*\|/(\rho\sqrt{k})$, and $\|r_k\|$ does not increase with $k$.

*Proof.* Write $P = \operatorname{prox}_{\rho\varphi}$. For two points $u, v$ with $p = P(u)$, $q = P(v)$, the vectors $(u - p)/\rho$ and $(v - q)/\rho$ are subgradients of $\varphi$ at $p$ and $q$, and monotonicity of $\partial\varphi$ gives $\big((u - p) - (v - q)\big)^\top(p - q) \ge 0$, that is,

$$\|p - q\|^2 \le (u - v)^\top(p - q). \tag{F}$$

By the Cauchy-Schwarz inequality, $\|p - q\| \le \|u - v\|$. With $u = y_k$ and $v = y_{k-1}$ this gives $\|y_{k+1} - y_k\| \le \|y_k - y_{k-1}\|$, so $\|r_{k+1}\| \le \|r_k\|$. With $v = y^*$, $q = y^*$ (a minimizer is a fixed point of $P$), (F) gives $\|y_{j+1} - y^*\|^2 \le (y_j - y^*)^\top(y_{j+1} - y^*)$, and with $\|a - c\|^2 = \|a\|^2 - 2a^\top c + \|c\|^2$ for $a = y_j - y^*$, $c = y_{j+1} - y^*$ this implies

$$\|y_{j+1} - y^*\|^2 + \|y_{j+1} - y_j\|^2 \le \|y_j - y^*\|^2.$$

Add these for $j = 0, \ldots, k - 1$: $\sum_{j=1}^k\|y_j - y_{j-1}\|^2 \le \|y_0 - y^*\|^2$. The terms do not increase, so the last one is at most the mean: $\|y_k - y_{k-1}\|^2 \le \|y_0 - y^*\|^2/k$. Since $y_k - y_{k-1} = \rho r_k$, the claim follows. $\square$

**Corollary (primal accuracy and the gap).** For each $k \ge 1$,

$$-\|y^*\|\,\|r_k\| \le f(x_k) - f^* \le f(x_k) - d(y_k) = -y_k^\top r_k \le \|y_k\|\,\|r_k\|.$$

*Proof.* The left inequality: $f^* = d(y^*) \le L(x_k, y^*) = f(x_k) + y^{*\top} r_k$. The middle: $d(y_k) \le f^*$ by weak duality. The equality is Lemma 1. So the primal value converges at the rate $O(1/\sqrt{k})$ of the residual, the gap $-y_k^\top r_k$ is computable at each step, and $\|y_k\| \le \|y^*\| + \|y_0 - y^*\|$ because $\|y_k - y^*\|$ does not increase. $\blacksquare$
