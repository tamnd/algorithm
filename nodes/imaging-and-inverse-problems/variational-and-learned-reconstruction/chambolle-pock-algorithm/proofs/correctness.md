---
title: The Chambolle-Pock iterates converge to a saddle point for tau sigma ||K||^2 < 1, and their averages have a primal-dual gap of O(1/N)
proves: [correctness, convergence-rate]
status: full
---

**Setting.** $X = \mathbb{R}^n$ and $Y = \mathbb{R}^m$ with the Euclidean inner product, $K : X \to Y$ linear with $L = \|K\|$, and $F$, $G$ closed, proper and convex. The saddle function is $\mathcal{L}(x, y) = \langle Kx, y\rangle + G(x) - F^*(y)$, and we assume a saddle point $(x^*, y^*)$ exists: $\mathcal{L}(x^*, y) \le \mathcal{L}(x^*, y^*) \le \mathcal{L}(x, y^*)$ for all $x, y$. The algorithm with $\theta = 1$ is, for $n \ge 0$, with $\bar x^0 = x^0$:

$$y^{n+1} = \operatorname{prox}_{\sigma F^*}(y^n + \sigma K\bar x^n),\qquad x^{n+1} = \operatorname{prox}_{\tau G}(x^n - \tau K^*y^{n+1}),\qquad \bar x^{n+1} = 2x^{n+1} - x^n.$$

Set $x^{-1} = x^0$, so that $\bar x^n = 2x^n - x^{n-1}$ for all $n \ge 0$. Let $c = L\sqrt{\tau\sigma}$ and, for $(x, y) \in X \times Y$, $\Delta(x, y) = \|x - x^0\|^2/(2\tau) + \|y - y^0\|^2/(2\sigma)$.

**Facts used.** (P) For a closed proper convex $h$ and $t > 0$, $u = \operatorname{prox}_{th}(v)$ if and only if $(v - u)/t \in \partial h(u)$, and $\operatorname{prox}_{th}$ is continuous (it is nonexpansive). (T) For all vectors $a, b, c$: $2\langle a - b, c - b\rangle = \|a - b\|^2 + \|c - b\|^2 - \|a - c\|^2$. (Y) For all $a \in X$ and $b \in Y$: $|\langle Ka, b\rangle| \le L\|a\|\,\|b\| \le c\big(\|a\|^2/(2\tau) + \|b\|^2/(2\sigma)\big)$, because $L\|a\|\|b\| = c\,(\|a\|/\sqrt\tau)(\|b\|/\sqrt\sigma)$ and $2st \le s^2 + t^2$ for real $s, t$.

**Lemma 1 (one step).** For every $(x, y)$ and $n \ge 0$,

$$\mathcal{L}(x^{n+1}, y) - \mathcal{L}(x, y^{n+1}) \le \frac{\|x - x^n\|^2 - \|x - x^{n+1}\|^2 - \|x^{n+1} - x^n\|^2}{2\tau} + \frac{\|y - y^n\|^2 - \|y - y^{n+1}\|^2 - \|y^{n+1} - y^n\|^2}{2\sigma} + \langle K(x^{n+1} - \bar x^n), y - y^{n+1}\rangle.$$

*Proof.* By (P), $(y^n - y^{n+1})/\sigma + K\bar x^n \in \partial F^*(y^{n+1})$ and $(x^n - x^{n+1})/\tau - K^*y^{n+1} \in \partial G(x^{n+1})$. The subgradient inequalities at $y$ and $x$ read

$$F^*(y^{n+1}) - F^*(y) \le -\tfrac1\sigma\langle y^n - y^{n+1}, y - y^{n+1}\rangle - \langle K\bar x^n, y - y^{n+1}\rangle,$$

$$G(x^{n+1}) - G(x) \le -\tfrac1\tau\langle x^n - x^{n+1}, x - x^{n+1}\rangle + \langle K(x - x^{n+1}), y^{n+1}\rangle.$$

Now $\mathcal{L}(x^{n+1}, y) - \mathcal{L}(x, y^{n+1}) = \langle Kx^{n+1}, y\rangle - \langle Kx, y^{n+1}\rangle + G(x^{n+1}) - G(x) + F^*(y^{n+1}) - F^*(y)$. Insert the two inequalities. The bilinear terms add up to $\langle Kx^{n+1}, y\rangle - \langle Kx^{n+1}, y^{n+1}\rangle - \langle K\bar x^n, y - y^{n+1}\rangle = \langle K(x^{n+1} - \bar x^n), y - y^{n+1}\rangle$. By (T), $-2\langle x^n - x^{n+1}, x - x^{n+1}\rangle = \|x - x^n\|^2 - \|x - x^{n+1}\|^2 - \|x^n - x^{n+1}\|^2$, and the same for $y$. $\square$

**Lemma 2 (summed bound).** Let $\tau\sigma L^2 \le 1$, so $c \le 1$. For every $(x, y)$, every $0 \le M < N$,

$$\sum_{n=M}^{N-1}\big(\mathcal{L}(x^{n+1}, y) - \mathcal{L}(x, y^{n+1})\big) + \frac{\|x - x^N\|^2}{2\tau} + (1 - c)\frac{\|y - y^N\|^2}{2\sigma} + (1 - c)\sum_{n=M}^{N-1}\Big(\frac{\|x^{n+1} - x^n\|^2}{2\tau} + \frac{\|y^{n+1} - y^n\|^2}{2\sigma}\Big)$$

$$\le \frac{\|x - x^M\|^2}{2\tau} + \frac{\|y - y^M\|^2}{2\sigma} + R_M,\qquad R_M = c\,\frac{\|x^M - x^{M-1}\|^2}{2\tau} - \langle K(x^M - x^{M-1}), y - y^M\rangle.$$

In particular $R_0 = 0$ because $x^{-1} = x^0$.

*Proof.* Write $d^n = x^n - x^{n-1}$. Then $x^{n+1} - \bar x^n = d^{n+1} - d^n$ and

$$\langle K(d^{n+1} - d^n), y - y^{n+1}\rangle = \langle Kd^{n+1}, y - y^{n+1}\rangle - \langle Kd^n, y - y^n\rangle - \langle Kd^n, y^n - y^{n+1}\rangle.$$

The first two terms telescope over $n = M, \dots, N-1$ to $\langle Kd^N, y - y^N\rangle - \langle Kd^M, y - y^M\rangle$. By (Y), $|\langle Kd^n, y^n - y^{n+1}\rangle| \le c\,(\|d^n\|^2/(2\tau) + \|y^{n+1} - y^n\|^2/(2\sigma))$ and $|\langle Kd^N, y - y^N\rangle| \le c\,(\|d^N\|^2/(2\tau) + \|y - y^N\|^2/(2\sigma))$. Sum Lemma 1 over $n = M, \dots, N-1$. The distance terms telescope to $\|x - x^M\|^2/(2\tau) + \|y - y^M\|^2/(2\sigma) - \|x - x^N\|^2/(2\tau) - \|y - y^N\|^2/(2\sigma)$. The negative step terms are $\sum_{n=M+1}^{N}\|d^n\|^2/(2\tau) + \sum_{n=M}^{N-1}\|y^{n+1} - y^n\|^2/(2\sigma)$, and the positive terms from (Y) are $c\sum_{n=M}^{N}\|d^n\|^2/(2\tau) + c\sum_{n=M}^{N-1}\|y^{n+1} - y^n\|^2/(2\sigma) + c\|y - y^N\|^2/(2\sigma)$. Collect terms: the $x$ steps with index $M+1$ to $N$ keep the factor $1 - c$, the term $c\|d^M\|^2/(2\tau)$ and $-\langle Kd^M, y - y^M\rangle$ form $R_M$, and the rest is as stated. $\square$

**Theorem 1 (ergodic rate).** Let $\tau\sigma L^2 \le 1$, $X_N = \frac1N\sum_{n=1}^N x^n$ and $Y_N = \frac1N\sum_{n=1}^N y^n$. For every $(x, y)$,

$$\mathcal{L}(X_N, y) - \mathcal{L}(x, Y_N) \le \frac{\Delta(x, y)}{N}.$$

*Proof.* Lemma 2 with $M = 0$ and nonnegative extra terms gives $\sum_{n=0}^{N-1}\big(\mathcal{L}(x^{n+1}, y) - \mathcal{L}(x, y^{n+1})\big) \le \Delta(x, y)$. The map $x' \mapsto \mathcal{L}(x', y)$ is convex and $y' \mapsto \mathcal{L}(x, y')$ is concave, so by Jensen's inequality $\mathcal{L}(X_N, y) \le \frac1N\sum\mathcal{L}(x^{n}, y)$ and $\mathcal{L}(x, Y_N) \ge \frac1N\sum\mathcal{L}(x, y^n)$. Divide by $N$. $\square$

If $B_1 \times B_2$ is a bounded set that contains a saddle point, the partial gap $\sup_{(x,y) \in B_1 \times B_2}\mathcal{L}(X_N, y) - \mathcal{L}(x, Y_N)$ is therefore at most $\sup\Delta/N$. For total variation denoising the domain of $F^*$ is bounded, so this is the true primal-dual gap with a bounded $B_2$.

**Lemma 3 (boundedness).** Let $\tau\sigma L^2 < 1$, so $c < 1$. Then the iterates are bounded and $\sum_n\big(\|x^{n+1} - x^n\|^2 + \|y^{n+1} - y^n\|^2\big) < \infty$.

*Proof.* Take $(x, y) = (x^*, y^*)$ in Lemma 2 with $M = 0$. Each summand $\mathcal{L}(x^{n+1}, y^*) - \mathcal{L}(x^*, y^{n+1}) = \big(\mathcal{L}(x^{n+1}, y^*) - \mathcal{L}(x^*, y^*)\big) + \big(\mathcal{L}(x^*, y^*) - \mathcal{L}(x^*, y^{n+1})\big)$ is at least 0 by the saddle point property. So for every $N$, $\|x^* - x^N\|^2/(2\tau) + (1 - c)\|y^* - y^N\|^2/(2\sigma) \le \Delta(x^*, y^*)$ and $(1 - c)\sum_{n<N}(\dots) \le \Delta(x^*, y^*)$. $\square$

**Theorem 2 (convergence).** Let $\tau\sigma L^2 < 1$. Then $(x^n, y^n)$ converges to a saddle point of $\mathcal{L}$.

*Proof.* By Lemma 3 there is a subsequence with $(x^{n_k}, y^{n_k}) \to (\hat x, \hat y)$, and the step lengths tend to 0. So also $x^{n_k - 1} \to \hat x$, $x^{n_k + 1} \to \hat x$, $y^{n_k + 1} \to \hat y$ and $\bar x^{n_k} = 2x^{n_k} - x^{n_k - 1} \to \hat x$. The prox maps are continuous by (P), so passing to the limit in the two update equations gives

$$\hat y = \operatorname{prox}_{\sigma F^*}(\hat y + \sigma K\hat x),\qquad \hat x = \operatorname{prox}_{\tau G}(\hat x - \tau K^*\hat y).$$

By (P) these say $K\hat x \in \partial F^*(\hat y)$ and $-K^*\hat y \in \partial G(\hat x)$. The first means $\hat y$ maximizes the concave function $\mathcal{L}(\hat x, \cdot)$, and the second means $\hat x$ minimizes the convex function $\mathcal{L}(\cdot, \hat y)$. So $(\hat x, \hat y)$ is a saddle point.

Now apply Lemma 2 with $(x, y) = (\hat x, \hat y)$, $M = n_k$ and any $N > n_k$. The sum is at least 0 as in Lemma 3, so

$$\frac{\|\hat x - x^N\|^2}{2\tau} + (1 - c)\frac{\|\hat y - y^N\|^2}{2\sigma} \le \frac{\|\hat x - x^{n_k}\|^2}{2\tau} + \frac{\|\hat y - y^{n_k}\|^2}{2\sigma} + c\,\frac{\|x^{n_k} - x^{n_k - 1}\|^2}{2\tau} + L\|x^{n_k} - x^{n_k - 1}\|\,\|\hat y - y^{n_k}\|.$$

The right side tends to 0 as $k \to \infty$ and does not depend on $N$. So $x^N \to \hat x$ and $y^N \to \hat y$. $\square$

**Remarks.** The averages $X_N, Y_N$ then converge to the same limit. The bound of Theorem 1 holds with $\tau\sigma L^2 \le 1$, but the convergence of the iterates uses the strict inequality through the factor $1 - c$. The accelerated rates for strongly convex $G$ (Theorem 2 of Chambolle and Pock 2011) are not proved here.
