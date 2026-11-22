---
title: The gradients of the cost, the exact result of MI-FACE on a binary logistic model, and global optimality of its fixed points on a softmax regression
proves: [correctness]
status: full
---

**Setting.** A model gives class confidences $p_1(x), \ldots, p_k(x) > 0$ on $x \in [0, 1]^d$, the cost of the class $\ell$ is $c(x) = 1 - p_\ell(x)$, and one step of line L3 is $T(x) = \operatorname{clip}(x - \lambda \nabla c(x))$, where clip maps each coordinate to the nearest point of $[0, 1]$. All arithmetic is exact.

**Claim 0 (what MI-FACE returns).** For any cost, MI-FACE stops after at most $\alpha$ steps and returns a point of $[0, 1]^d$ with the least cost among $x_0, \ldots, x_r$, the points it visited, and the first one on ties.

*Proof.* The loop of line L2 runs at most $\alpha$ times. $x_0 = 0$ is in the box, and each $x_i$ is a clip, so it is in the box. The code replaces the kept point only when the new cost is strictly lower, so it keeps the first point of least cost. $\square$

**Claim 1 (the gradients).** Write $\sigma(t) = 1/(1 + e^{-t})$, so $\sigma' = \sigma(1 - \sigma)$.

1. For $p_1(x) = \sigma(w \cdot x + b)$: $\nabla c(x) = -\sigma'(z) w$ with $z = w \cdot x + b$.
2. For $p = \operatorname{softmax}(z)$ with $z = W x + b$: $\nabla c(x) = -p_\ell(x)\big(W_\ell - \sum_j p_j(x) W_j\big)$, where $W_j$ is row $j$ of $W$.
3. For $p = \operatorname{softmax}(z(x))$ with any logits $z(x)$ differentiable at $x$: $\nabla c(x) = p_\ell(x) \nabla \text{CE}(x)$, where $\text{CE}(x) = -\ln p_\ell(x)$. A tiny ReLU network is differentiable at every $x$ where no hidden pre-activation is $0$, since there the pattern of active units is constant near $x$ and the logits are affine.

*Proof.* (1) is the chain rule. For (2), $\ln p_\ell = z_\ell - \ln \sum_j e^{z_j}$, so $\partial \ln p_\ell / \partial z_j = [j = \ell] - p_j$, and with $\partial z_j / \partial x = W_j$ we get $\nabla \ln p_\ell = W_\ell - \sum_j p_j W_j$. Then $\nabla c = -\nabla p_\ell = -p_\ell \nabla \ln p_\ell$. For (3), $p_\ell = e^{-\text{CE}}$, so $\nabla c = -\nabla p_\ell = p_\ell \nabla \text{CE}$. $\square$

**Claim 2 (binary logistic model).** Let $p_1(x) = \sigma(w \cdot x + b)$ with $w_j \ne 0$ for all $j$, let $\ell = 1$, $M = \lVert w \rVert_1 + |b|$, $s = \sigma'(M)$, $m = \min_j |w_j|$ and $N = \lceil 1/(\lambda s m) \rceil$. Let $x^*_j = 1$ if $w_j > 0$ and $x^*_j = 0$ if $w_j < 0$. Then $x^*$ is the unique minimizer of $c$ on the box. If $\gamma < c(x^*)$ and $\alpha \ge N$, MI-FACE returns $x^*$ and $c(x^*)$, and if $\alpha \ge N + \beta$, line L4 stops the run after at most $N + \beta$ steps.

*Proof.* *The minimizer.* $c = 1 - \sigma(w \cdot x + b)$ and $\sigma$ is strictly increasing, so $c$ is least where $w \cdot x = \sum_j w_j x_j$ is largest. Each term $w_j x_j$ with $x_j \in [0, 1]$ is largest only at $x_j = x^*_j$, since $w_j \ne 0$.

*A lower bound on the slope.* For $x$ in the box, $|z| = |w \cdot x + b| \le M$. The function $\sigma'$ is even and decreasing in $|t|$, so $\sigma'(z) \ge s > 0$.

*The iterates.* By Claim 1, coordinate $j$ of $x - \lambda \nabla c(x)$ is $x_j + \lambda \sigma'(z) w_j$. If $w_j < 0$, it is at most $x_j$; starting from $x_{0, j} = 0$, the clip keeps $x_{i, j} = 0$ for all $i$. If $w_j > 0$, it is at least $x_j + \lambda s m$, so $x_{i, j} \ge \min(1, x_{i-1, j} + \lambda s m)$: the coordinate grows by at least $\lambda s m$ per step until it equals $1$, and after that the clip keeps it at $1$. So all coordinates with $w_j > 0$ equal $1$ after at most $\lceil 1/(\lambda s m) \rceil = N$ steps. Let $i^* \le N$ be the first index with $x_{i^*} = x^*$; then $x_i = x^*$ for all $i \ge i^*$, because $T(x^*) = x^*$ by the same two cases.

*The costs.* For $1 \le i \le i^*$, $x_i \ne x_{i-1}$: some coordinate with $w_j > 0$ was below $1$ at step $i - 1$ and grows by a positive amount, and no coordinate moves the other way. So $w \cdot x_i > w \cdot x_{i-1}$ and $c(x_i) < c(x_{i-1}) \le \max(c(x_{i-1}), \ldots, c(x_{i - \beta}))$, and line L4 does not stop the run. Line L5 never stops it, because $c(x_i) \ge c(x^*) > \gamma$. So the run reaches step $i^*$ when $\alpha \ge N \ge i^*$. The costs $c(x_0) > c(x_1) > \cdots > c(x_{i^*}) = c(x^*)$ are strictly decreasing and every later cost equals $c(x^*)$, so the first visited point of least cost is $x_{i^*} = x^*$, and by Claim 0 MI-FACE returns it. Finally, at step $i = i^* + \beta$ the last $\beta$ costs are all $c(x^*)$ and $c(x_i) = c(x^*)$, so line L4 stops the run there, or earlier, when $\alpha \ge N + \beta$. $\square$

**Claim 3 (softmax regression).** Let $p = \operatorname{softmax}(W x + b)$ and $\varphi(x) = \ln p_\ell(x)$. Then $\varphi$ is concave. If $T(x) = x$, then $x$ minimizes $c$ on the box. For every $x$ in the box, with $g = \nabla \varphi(x)$,

$$\varphi(x^*) - \varphi(x) \le G(x) = \sum_{j=1}^{d} \max\big(-g_j x_j,\ g_j (1 - x_j)\big),$$

where $x^*$ is any maximizer of $\varphi$ on the box.

*Proof.* *Concavity.* $\varphi(x) = z_\ell - L(z)$ with $z = Wx + b$ and $L(z) = \ln \sum_j e^{z_j}$. The Hessian of $L$ is $\operatorname{diag}(p) - p p^\top$, and for every vector $v$, $v^\top(\operatorname{diag}(p) - pp^\top)v = \sum_j p_j v_j^2 - (\sum_j p_j v_j)^2 \ge 0$, the variance of $v$ under the distribution $p$. So $L$ is convex, $L(Wx + b)$ is convex in $x$ as a convex function of an affine map, and $\varphi$ is an affine function minus a convex one, so it is concave.

*The gap.* By concavity, $\varphi(u) \le \varphi(x) + g \cdot (u - x)$ for every $u$. Take $u = x^*$, and bound $g \cdot (x^* - x)$ by its maximum over the box. The maximum of the linear function $u \mapsto g \cdot (u - x)$ on the box splits over the coordinates, and in coordinate $j$ it is attained at $u_j = 0$ or $u_j = 1$, which gives $G(x)$.

*Fixed points.* By Claim 1, $\nabla c = -p_\ell g$ with $p_\ell > 0$. A coordinate of $T(x)$ equals $x_j$ exactly when $0 < x_j < 1$ and $g_j = 0$, or $x_j = 0$ and $g_j \le 0$, or $x_j = 1$ and $g_j \ge 0$. In each case both terms of the maximum in $G$ are at most $0$ and one of them is $0$, so $G(x) = 0$. Then $\varphi(x^*) \le \varphi(x)$, so $x$ maximizes $\varphi$, hence maximizes $p_\ell = e^{\varphi}$ and minimizes $c$. $\square$

**What the tests check.** The example and Claim 2 on $500$ random binary logistic models, with $\alpha = N + \beta + 1$ and a tolerance of $10^{-9}$ for rounding; Claim 1 against central differences; and $G(x) < 10^{-3}$ at the result on $500$ random softmax regressions, which by Claim 3 puts $\ln p_\ell$ within $10^{-3}$ of its largest value. Claim 3 does not say how many steps are needed to make $G$ small; that the tests reach it in at most $300$ steps of size $4$ is a measurement. For networks with a hidden layer $\varphi$ need not be concave, and nothing beyond Claims 0 and 1 is claimed. $\blacksquare$
