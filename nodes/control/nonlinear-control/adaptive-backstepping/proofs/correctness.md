---
title: Adaptive backstepping with tuning functions gives V' = -sum c_i z_i^2, bounded signals and regulation of the state to zero
proves: [correctness, termination]
status: full
---

The system is in parametric strict feedback form:

$$\dot x_i = x_{i+1} + \varphi_i(\bar x_i)^T \theta \quad (1 \le i \le n - 1), \qquad \dot x_n = \beta(x)\, u + \varphi_n(x)^T \theta,$$

where $\bar x_i = (x_1, \dots, x_i)$, $\theta \in \mathbb{R}^p$ is constant and unknown, the maps $\varphi_i : \mathbb{R}^i \to \mathbb{R}^p$ and $\beta : \mathbb{R}^n \to \mathbb{R}$ are smooth ($C^\infty$), $\beta(x) \neq 0$ for every $x$, and $\varphi_i(0) = 0$. The gains $c_1, \dots, c_n$ are positive and $\Gamma$ is a symmetric positive definite $p \times p$ matrix. The estimate is $\hat\theta$ and the error is $\tilde\theta = \theta - \hat\theta$.

Put $\alpha_0 = 0$, $z_0 = 0$, $\tau_0 = 0$ (line L1). For $i = 1, \dots, n$ (line L2) define, as functions of $(\bar x_i, \hat\theta)$,

$$z_i = x_i - \alpha_{i-1}(\bar x_{i-1}, \hat\theta), \qquad w_i = \varphi_i - \sum_{k=1}^{i-1} \frac{\partial \alpha_{i-1}}{\partial x_k} \varphi_k, \qquad \tau_i = \tau_{i-1} + w_i z_i,$$

$$\alpha_i = -z_{i-1} - c_i z_i - w_i^T \hat\theta + \sum_{k=1}^{i-1} \frac{\partial \alpha_{i-1}}{\partial x_k} x_{k+1} + \frac{\partial \alpha_{i-1}}{\partial \hat\theta} \Gamma \tau_i + \sum_{k=2}^{i-1} z_k \frac{\partial \alpha_{k-1}}{\partial \hat\theta} \Gamma w_i.$$

These are lines L3 to L6. Here $\partial \alpha_{k-1} / \partial \hat\theta$ is a row vector. The controller is $u = \alpha_n / \beta$ and the update law is $\dot{\hat\theta} = \Gamma \tau_n$ (line L7). Let

$$V = \frac12 \sum_{i=1}^n z_i^2 + \frac12 \tilde\theta^T \Gamma^{-1} \tilde\theta.$$

## Termination

The algorithm defines $\alpha_1, \dots, \alpha_n$ once each. The implementation does this by a recursion on $i$ that stops at $i = 0$. Each call at level $i \ge 2$ makes $i + p$ calls at level $i - 1$ and no other recursive calls, so the recursion tree is finite and the computation ends.

## Lemma 1: each alpha_i is smooth and vanishes at x = 0

Each $\alpha_i$ is a smooth function of $(\bar x_i, \hat\theta)$, and $\alpha_i(0, \hat\theta) = 0$ for every $\hat\theta$. Also $z_i$, $w_i$ and $\tau_i$ are smooth, and they vanish at $\bar x_i = 0$.

*Proof.* By induction on $i$. For $i = 0$ all four are zero. Suppose the claim holds for $i - 1$. Then $z_i$, $w_i$, $\tau_i$ and $\alpha_i$ are built from smooth functions by sums, products and first partial derivatives of the smooth $\alpha_k$, $k < i$, so they are smooth. At $\bar x_i = 0$: $z_i = 0 - \alpha_{i-1}(0, \hat\theta) = 0$; $w_i = 0$ because every $\varphi_k(0) = 0$; $\tau_i = \tau_{i-1} + 0 = 0$; and every term of $\alpha_i$ is zero: $z_{i-1}$, $z_i$, $w_i$, $x_{k+1}$, $\tau_i$ and $w_i$ again. $\square$

## Lemma 2: the error dynamics

Along every solution of the closed loop, for $i = 1, \dots, n$, with $z_{n+1} = 0$,

$$\dot z_i = -c_i z_i + z_{i+1} - z_{i-1} + w_i^T \tilde\theta - \sum_{j=i+1}^{n} \sigma_{ij} z_j + \sum_{k=2}^{i-1} \sigma_{ki} z_k, \qquad \sigma_{ij} = \frac{\partial \alpha_{i-1}}{\partial \hat\theta} \Gamma w_j.$$

*Proof.* By the chain rule and the equations of the system for $k \le i - 1 \le n - 1$,

$$\frac{d}{dt} \alpha_{i-1} = \sum_{k=1}^{i-1} \frac{\partial \alpha_{i-1}}{\partial x_k} \bigl(x_{k+1} + \varphi_k^T \theta\bigr) + \frac{\partial \alpha_{i-1}}{\partial \hat\theta} \Gamma \tau_n.$$

For $i \le n - 1$, $\dot x_i = x_{i+1} + \varphi_i^T \theta = z_{i+1} + \alpha_i + \varphi_i^T \theta$. For $i = n$, $\dot x_n = \beta u + \varphi_n^T \theta = \alpha_n + \varphi_n^T \theta$, which is the same with $z_{n+1} = 0$. So

$$\dot z_i = z_{i+1} + \alpha_i + w_i^T \theta - \sum_{k=1}^{i-1} \frac{\partial \alpha_{i-1}}{\partial x_k} x_{k+1} - \frac{\partial \alpha_{i-1}}{\partial \hat\theta} \Gamma \tau_n,$$

where the terms with $\theta$ were collected with the definition of $w_i$. Put in $\alpha_i$. The sum over $x_{k+1}$ cancels, $w_i^T \theta - w_i^T \hat\theta = w_i^T \tilde\theta$, and

$$\frac{\partial \alpha_{i-1}}{\partial \hat\theta} \Gamma (\tau_i - \tau_n) = -\sum_{j=i+1}^{n} \frac{\partial \alpha_{i-1}}{\partial \hat\theta} \Gamma w_j z_j = -\sum_{j=i+1}^{n} \sigma_{ij} z_j,$$

because $\tau_n - \tau_i = \sum_{j = i+1}^n w_j z_j$ by line L5. The last sum of $\alpha_i$ is $\sum_{k=2}^{i-1} \sigma_{ki} z_k$. This is the claim. $\square$

## Lemma 3: the derivative of V

Along the closed loop, $\dot V = -\sum_{i=1}^n c_i z_i^2$.

*Proof.* Multiply Lemma 2 by $z_i$ and add over $i$.

- The terms $z_i z_{i+1}$ and $-z_{i-1} z_i$ give $\sum_{i=1}^{n-1} z_i z_{i+1} - \sum_{i=2}^{n} z_{i-1} z_i = 0$, because $z_0 = z_{n+1} = 0$.
- Note that $\sigma_{1j} = 0$, because $\alpha_0 = 0$. The terms with $\sigma$ give $-\sum_{2 \le i < j \le n} \sigma_{ij} z_i z_j + \sum_{2 \le k < i \le n} \sigma_{ki} z_k z_i$. Rename $(k, i)$ to $(i, j)$ in the second sum: it is the first sum with the opposite sign, so they cancel. This is the reason for the last sum in line L6.
- The terms with $\tilde\theta$ give $\tilde\theta^T \sum_i w_i z_i = \tilde\theta^T \tau_n$.

So $\sum_i z_i \dot z_i = -\sum_i c_i z_i^2 + \tilde\theta^T \tau_n$. Since $\theta$ is constant, $\dot{\tilde\theta} = -\dot{\hat\theta} = -\Gamma \tau_n$, and the derivative of the second part of $V$ is $\tilde\theta^T \Gamma^{-1} (-\Gamma \tau_n) = -\tilde\theta^T \tau_n$, with $\Gamma$ symmetric. The two terms with $\tau_n$ cancel. $\square$

## Lemma 4: the change of coordinates

For each fixed $\hat\theta$, the map $x \mapsto z$ is a bijection of $\mathbb{R}^n$, and $x$ is a continuous function of $(z, \hat\theta)$ with $x = 0$ when $z = 0$.

*Proof.* Given $(z, \hat\theta)$, the equations $x_i = z_i + \alpha_{i-1}(\bar x_{i-1}, \hat\theta)$ for $i = 1, \dots, n$ give $x_1 = z_1$, then $x_2$, and so on, in a unique way, and each step is continuous. If $z = 0$, then $x_1 = 0$, and by Lemma 1 every later $x_i = \alpha_{i-1}(0, \hat\theta) = 0$. $\square$

## Theorem: boundedness and regulation

For every initial state $x(0)$ and estimate $\hat\theta(0)$, the solution of the closed loop exists for all $t \ge 0$, $x$ and $\hat\theta$ are bounded, $V$ is nonincreasing, and $x(t) \to 0$ as $t \to \infty$.

*Proof.* The closed loop in $(x, \hat\theta)$ is smooth by Lemma 1 and because $\beta \neq 0$, so it is locally Lipschitz and solutions are unique on their maximal interval $[0, t_f)$ (Picard-Lindelöf). On this interval $V$ is nonincreasing by Lemma 3, so $|z(t)|^2 \le 2 V(0)$ and $\tilde\theta(t)^T \Gamma^{-1} \tilde\theta(t) \le 2 V(0)$. The second bound and $\Gamma^{-1} > 0$ bound $\hat\theta$. Then $(z, \hat\theta)$ stays in a compact set $K$, and $x$, a continuous function of $(z, \hat\theta)$ by Lemma 4, stays in the compact image of $K$. A solution that stays in a compact set cannot have a finite escape time, so $t_f = \infty$.

The right side of the closed loop is continuous, so it is bounded on this compact set, and so is $\dot z$, which is a continuous function of $(x, \hat\theta)$ by Lemma 2. So $z$ is uniformly continuous. Integrating Lemma 3, $\int_0^\infty \sum_i c_i z_i^2\, dt \le V(0)$. By Barbalat's lemma, $z(t) \to 0$.

Last, $x \to 0$. The map $(z, \hat\theta) \mapsto x$ of Lemma 4 is uniformly continuous on $K$ and is zero on $\{z = 0\} \cap K$. Given $\epsilon > 0$, there is $\delta > 0$ such that $|z| < \delta$ implies $|x| < \epsilon$ on $K$. Since $z(t) \to 0$, $|x(t)| < \epsilon$ for all large $t$. $\square$

The theorem does not say that $\hat\theta(t) \to \theta$. The proof only gives that $\tilde\theta$ is bounded.

## Lemma 5: the implementation computes the partial derivatives exactly

The implementation evaluates step $i - 1$ at $(\bar x, \hat\theta)$ with one coordinate replaced by $x_k + \varepsilon$ or $\hat\theta_l + \varepsilon$, where $\varepsilon^2 = 0$ and the tag of $\varepsilon$ is new. By the dual number lemma of the [backstepping proof](/backstepping/) (sum, product, quotient and power rules hold in $R[\varepsilon]$ for any commutative ring $R$, so also when $R$ holds dual numbers with smaller tags), the coefficient of $\varepsilon$ in each returned $\alpha_k$, $k \le i - 1$, is $\partial \alpha_k / \partial x_k$ or $\partial \alpha_k / \partial \hat\theta_l$ at the point. Every tag made inside the call is removed before the call returns, so the split by the new tag is unambiguous. The rest of step $i$ is lines L3 to L6 as written, and line L7 divides by $\beta$ and multiplies by $\Gamma$. So the code returns $u$, $\dot{\hat\theta}$ and $z$ exactly when the inputs are exact rationals and $\varphi_i$, $\beta$ are rational functions, and up to floating point rounding otherwise. $\blacksquare$
