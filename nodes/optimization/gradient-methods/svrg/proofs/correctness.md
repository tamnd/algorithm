---
title: SVRG with a random snapshot converges linearly in expectation for strongly convex finite sums of smooth convex functions
proves: [correctness, convergence-rate]
status: full
---

**Setting.** $F(x) = \frac{1}{n}\sum_{i=1}^nf_i(x)$ on $\mathbb{R}^d$. Each $f_i$ is convex and differentiable with an $L$-Lipschitz gradient, and $F$ is $\mu$-strongly convex with minimizer $x^*$ and $F^* = F(x^*)$. In epoch $s$ the method fixes the snapshot $\tilde{x} = \tilde{x}_{s-1}$ and $\tilde{\mu} = \nabla F(\tilde{x})$, sets $x_0 = \tilde{x}$, and for $t = 0, \dots, m - 1$ draws $i_t$ uniformly from $\{1, \dots, n\}$, independently of the past, and sets

$$v_t = \nabla f_{i_t}(x_t) - \nabla f_{i_t}(\tilde{x}) + \tilde{\mu}, \qquad x_{t+1} = x_t - \eta v_t.$$

The new snapshot $\tilde{x}_s$ is $x_t$ for $t$ drawn uniformly from $\{0, \dots, m - 1\}$ (Option II of Johnson and Zhang). $\mathbb{E}_t$ is the expectation over $i_t$ given the past.

**Lemma 1 (unbiased).** $\mathbb{E}_tv_t = \nabla F(x_t)$.

*Proof.* $\mathbb{E}_t\nabla f_{i_t}(x_t) = \nabla F(x_t)$ and $\mathbb{E}_t\nabla f_{i_t}(\tilde{x}) = \nabla F(\tilde{x}) = \tilde{\mu}$. $\square$

**Lemma 2.** For every $x$, $\frac{1}{n}\sum_i\lVert\nabla f_i(x) - \nabla f_i(x^*)\rVert^2 \le 2L(F(x) - F^*)$.

*Proof.* Let $\phi_i(x) = f_i(x) - f_i(x^*) - \langle\nabla f_i(x^*), x - x^*\rangle$. It is convex with an $L$-Lipschitz gradient $\nabla f_i(x) - \nabla f_i(x^*)$, and its minimum is $\phi_i(x^*) = 0$, since $\nabla\phi_i(x^*) = 0$. The descent lemma at $x$ with the step $1/L$ gives $0 \le \phi_i(x - \nabla\phi_i(x)/L) \le \phi_i(x) - \frac{1}{2L}\lVert\nabla\phi_i(x)\rVert^2$. Average over $i$ and use $\frac{1}{n}\sum_i\nabla f_i(x^*) = \nabla F(x^*) = 0$, so $\frac{1}{n}\sum_i\phi_i(x) = F(x) - F^*$. $\square$

**Lemma 3 (variance).** $\mathbb{E}_t\lVert v_t\rVert^2 \le 4L(F(x_t) - F^*) + 4L(F(\tilde{x}) - F^*)$.

*Proof.* Write $v_t = u + w$ with $u = \nabla f_{i_t}(x_t) - \nabla f_{i_t}(x^*)$ and $w = -(\nabla f_{i_t}(\tilde{x}) - \nabla f_{i_t}(x^*) - \tilde{\mu})$. Then $\lVert v_t\rVert^2 \le 2\lVert u\rVert^2 + 2\lVert w\rVert^2$. The random vector $z = \nabla f_{i_t}(\tilde{x}) - \nabla f_{i_t}(x^*)$ has mean $\nabla F(\tilde{x}) - 0 = \tilde{\mu}$, so $\mathbb{E}_t\lVert w\rVert^2 = \mathbb{E}_t\lVert z - \mathbb{E}_tz\rVert^2 \le \mathbb{E}_t\lVert z\rVert^2$. Apply Lemma 2 at $x_t$ to $\mathbb{E}_t\lVert u\rVert^2$ and at $\tilde{x}$ to $\mathbb{E}_t\lVert z\rVert^2$. $\square$

At $x_t = \tilde{x} = x^*$ the bound is $0$: unlike the plain stochastic gradient, the estimator has no variance at the solution.

**Lemma 4 (one inner step).**

$$\mathbb{E}_t\lVert x_{t+1} - x^*\rVert^2 \le \lVert x_t - x^*\rVert^2 - 2\eta(1 - 2L\eta)(F(x_t) - F^*) + 4L\eta^2(F(\tilde{x}) - F^*).$$

*Proof.* Expand: $\mathbb{E}_t\lVert x_{t+1} - x^*\rVert^2 = \lVert x_t - x^*\rVert^2 - 2\eta\langle\mathbb{E}_tv_t, x_t - x^*\rangle + \eta^2\mathbb{E}_t\lVert v_t\rVert^2$. By Lemma 1 and convexity of $F$, $\langle\nabla F(x_t), x_t - x^*\rangle \ge F(x_t) - F^*$. Use Lemma 3 for the last term. $\square$

**Theorem.** If $0 < \eta < \frac{1}{2L}$ and $m$ is large enough that

$$\alpha = \frac{1}{\mu\eta(1 - 2L\eta)m} + \frac{2L\eta}{1 - 2L\eta} < 1,$$

then $\mathbb{E}F(\tilde{x}_s) - F^* \le \alpha^s(F(\tilde{x}_0) - F^*)$ for every $s \ge 0$. For $\eta = \frac{1}{10L}$ and $m \ge 50L/\mu$, $\alpha \le \frac{1}{2}$.

*Proof.* Fix an epoch and condition on its snapshot $\tilde{x}$. Take full expectations in Lemma 4 and sum over $t = 0, \dots, m - 1$. The distance terms telescope:

$$\mathbb{E}\lVert x_m - x^*\rVert^2 + 2\eta(1 - 2L\eta)\sum_{t=0}^{m-1}\mathbb{E}(F(x_t) - F^*) \le \lVert x_0 - x^*\rVert^2 + 4Lm\eta^2(F(\tilde{x}) - F^*).$$

Drop the first term, which is nonnegative. Since $x_0 = \tilde{x}$, strong convexity and $\nabla F(x^*) = 0$ give $\lVert\tilde{x} - x^*\rVert^2 \le \frac{2}{\mu}(F(\tilde{x}) - F^*)$. With Option II, $\mathbb{E}F(\tilde{x}_s) = \frac{1}{m}\sum_{t<m}\mathbb{E}F(x_t)$. Therefore

$$2\eta(1 - 2L\eta)m\,(\mathbb{E}F(\tilde{x}_s) - F^*) \le \Big(\frac{2}{\mu} + 4Lm\eta^2\Big)(F(\tilde{x}) - F^*),$$

and dividing gives $\mathbb{E}[F(\tilde{x}_s) - F^* \mid \tilde{x}_{s-1}] \le \alpha(F(\tilde{x}_{s-1}) - F^*)$. Take the expectation and apply induction on $s$. For the numbers: $2L\eta = 0.2$, so the second term of $\alpha$ is $0.2/0.8 = 0.25$, and $\mu\eta(1 - 2L\eta)m \ge \frac{\mu}{10L}\cdot0.8\cdot\frac{50L}{\mu} = 4$, so the first term is at most $0.25$. $\blacksquare$

**Corollary (cost).** With $\eta = \frac{1}{10L}$, $m = \lceil50\kappa\rceil$ and $\kappa = L/\mu$, an epoch costs $n + 2m$ component gradients, and $\lceil\log_2(\delta/\varepsilon)\rceil$ epochs give $\mathbb{E}F(\tilde{x}_s) - F^* \le \varepsilon$ from an initial gap $\delta$. The total is $O((n + \kappa)\log(\delta/\varepsilon))$.

**Remarks.** The proof needs each $f_i$ to be convex (Lemma 2) but only $F$ to be strongly convex. Option I, which keeps the last inner iterate, is what most codes use; Johnson and Zhang did not prove a rate for it, and this proof does not cover it. The tests check Lemma 1 as an exact identity, Lemmas 2 and 3 and Lemma 4 by enumeration over all $i$ on a ridge regression problem with a solution from the normal equations, and the Theorem by Monte Carlo over 60 seeds.
