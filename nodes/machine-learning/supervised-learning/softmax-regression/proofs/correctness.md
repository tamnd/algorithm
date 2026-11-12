---
title: Gradient descent with step 1/L on the softmax cross-entropy stops at an approximate minimizer
proves: [correctness, termination]
status: full
---

Let $J(W) = \frac1n\sum_i[\operatorname{lse}(W^\top\tilde x_i) - \theta_{y_i}^\top\tilde x_i] + \frac\lambda2\|\bar W\|_F^2$, where $\operatorname{lse}(z) = \log\sum_k e^{z_k}$, $\theta_k$ is column $k$ of $W$ and $\bar W$ is $W$ with the bias row set to 0. Let $G(W) = \nabla J(W) = \frac1n\tilde X^\top(P - Y) + \lambda\bar W$ and $L = \|\tilde X\|_F^2/(2n) + \lambda$. Arithmetic is exact in this proof.

**Lemma 1 (line L3 computes $P$ and $G$).** For each $m \in \mathbb{R}$, $e^{z_k - m}/\sum_j e^{z_j - m} = e^{z_k}/\sum_j e^{z_j}$, so line L3 computes the softmax. The derivative of $\operatorname{lse}(z) - z_y$ in $z_k$ is $P_k - [k = y]$, and $\partial z_k/\partial\theta_k = \tilde x$, so the data part of $G$ is $\frac1n\sum_i\tilde x_i(P_i - Y_i)^\top = \frac1n\tilde X^\top(P - Y)$. The penalty part is $\lambda\bar W$. $\square$

**Lemma 2 (convexity and smoothness).** $J$ is convex and $\nabla J$ is $L$-Lipschitz.

*Proof.* The Hessian of $\operatorname{lse}$ at $z$ is $A = \operatorname{diag}(p) - pp^\top$ with $p = \operatorname{softmax}(z)$. For $u \in \mathbb{R}^K$, $u^\top Au = \sum_k p_k u_k^2 - (\sum_k p_k u_k)^2$, the variance of $u_k$ when $k$ has distribution $p$. It is $\ge 0$, and it is at most $(\max_k u_k - \min_k u_k)^2/4$ by Popoviciu's inequality, which is at most $\|u\|^2/2$ since $(a - b)^2 \le 2a^2 + 2b^2$. So $0 \preceq A \preceq \frac12 I$. The map $W \mapsto W^\top\tilde x_i$ is linear, and for a direction $V$ the second derivative of $\operatorname{lse}(W^\top\tilde x_i)$ is $(V^\top\tilde x_i)^\top A(V^\top\tilde x_i) \in [0, \frac12\|V^\top\tilde x_i\|^2] \subseteq [0, \frac12\|V\|_F^2\|\tilde x_i\|^2]$. The term $-\theta_{y_i}^\top\tilde x_i$ is linear. The penalty has second derivative $\lambda\|\bar V\|_F^2 \in [0, \lambda\|V\|_F^2]$. Averaging over $i$ gives $0 \le D^2J(W)[V, V] \le L\|V\|_F^2$, so $J$ is convex and $\nabla J$ is $L$-Lipschitz. $\square$

**Lemma 3 (descent).** If $W' = W - \frac1L G(W)$ (line L6), then $J(W') \le J(W) - \frac{1}{2L}\|G(W)\|_F^2$.

*Proof.* For a function with $L$-Lipschitz gradient, $J(W - \eta G) \le J(W) - \eta\|G\|^2 + \frac{L\eta^2}{2}\|G\|^2$. With $\eta = 1/L$ the right side is $J(W) - \frac{1}{2L}\|G\|^2$. $\square$

**Termination.** $J \ge 0$, because $\operatorname{lse}(z) \ge z_y$ for each $y$. Adding Lemma 3 over the steps gives $\frac{1}{2L}\sum_t\|G(W_t)\|_F^2 \le J(0) = \log K$. So $\|G(W_t)\|_F \to 0$, and for each tol $> 0$ line L5 returns after at most $2L\log K/\text{tol}^2$ iterations.

**Theorem.** The returned $W$ has $\|\nabla J(W)\|_F \le \text{tol}$. If $J$ has a minimizer $W^\star$, then $J(W_t) - J(W^\star) \le \frac{L\|W^\star\|_F^2}{2t}$ for every $t \ge 1$, and $J(W) - J(W^\star) \le \text{tol}\cdot\|W - W^\star\|_F$ at the returned $W$. A matrix with $\nabla J = 0$ is a global minimizer.

*Proof.* The first claim is the test of line L5. For a convex $J$, $J(W^\star) \ge J(W) + \langle G(W), W^\star - W\rangle$, which gives $J(W) - J(W^\star) \le \|G(W)\|_F\|W - W^\star\|_F$ and shows that $G = 0$ means a global minimum. The rate is the standard bound for gradient descent with step $1/L$ on a convex function with $L$-Lipschitz gradient: by Lemma 3 and convexity, $J(W_{t+1}) - J^\star \le \frac{L}{2}(\|W_t - W^\star\|^2 - \|W_{t+1} - W^\star\|^2)$, and adding over $t$ steps with $W_0 = 0$ and using that $J(W_t)$ decreases gives $J(W_t) - J^\star \le L\|W^\star\|^2/(2t)$ (Boyd and Vandenberghe, Section 9.3). $\blacksquare$

**Remark (the subspace).** Each row of $P - Y$ adds up to 0, so $\frac1n\tilde X^\top(P - Y)\mathbf{1} = 0$, and $G(W)\mathbf{1} = \lambda\bar W\mathbf{1}$. If $W\mathbf{1} = 0$, then $G(W)\mathbf{1} = 0$ and $W'\mathbf{1} = 0$. Since $W_0 = 0$, by induction every iterate has columns that add up to the zero vector, which is the condition that each minimizer satisfies when $\lambda > 0$.
