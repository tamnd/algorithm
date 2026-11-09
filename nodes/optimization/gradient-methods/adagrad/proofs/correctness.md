---
title: Diagonal AdaGrad on a box has regret at most (D²/(2η) + η) times the sum of the per-coordinate gradient norms
proves: [correctness, convergence-rate]
status: full
---

**Setting.** Online convex optimization on a box $X = \prod_{i=1}^d[l_i, h_i]$ with $D_i = h_i - l_i$ and $D_\infty = \max_iD_i$. In round $t = 1, \dots, T$ the method plays $x_t \in X$, a convex loss $f_t$ is revealed, and the method receives $g_t \in \partial f_t(x_t)$. Diagonal AdaGrad with $\eta > 0$ sets, for each coordinate $i$,

$$G_{t,i} = \Big(\sum_{s=1}^tg_{s,i}^2\Big)^{1/2}, \qquad x_{t+1,i} = \operatorname{clip}_{[l_i, h_i]}\Big(x_{t,i} - \eta\frac{g_{t,i}}{G_{t,i}}\Big),$$

with $x_{t+1,i} = x_{t,i}$ when $G_{t,i} = 0$. Write $g_{1:T,i} = (g_{1,i}, \dots, g_{T,i})$, so $G_{T,i} = \lVert g_{1:T,i}\rVert_2$. The regret against $u \in X$ is $R_T(u) = \sum_{t=1}^T(f_t(x_t) - f_t(u))$.

The clipping is the projection onto $X$ in the norm $\lVert z\rVert_{H_t}^2 = \sum_iG_{t,i}z_i^2$, because both the box and the norm are separable. So this is the diagonal method of Duchi, Hazan and Singer (2011) with $\delta = 0$.

**Lemma 1.** For $a_1, \dots, a_T \ge 0$ and $S_t = \sum_{s\le t}a_s$, $\sum_{t: S_t > 0}a_t/\sqrt{S_t} \le 2\sqrt{S_T}$.

*Proof.* If $S_t > 0$, then $a_t = S_t - S_{t-1} = (\sqrt{S_t} - \sqrt{S_{t-1}})(\sqrt{S_t} + \sqrt{S_{t-1}}) \le 2\sqrt{S_t}(\sqrt{S_t} - \sqrt{S_{t-1}})$. Divide by $\sqrt{S_t}$ and sum; the right side telescopes to $2\sqrt{S_T}$. $\square$

**Lemma 2 (one coordinate).** Fix $i$ and drop it from the notation. For every $u \in [l, h]$,

$$\sum_{t=1}^Tg_t(x_t - u) \le \Big(\frac{D^2}{2\eta} + \eta\Big)G_T.$$

*Proof.* Rounds with $G_t = 0$ have $g_t = 0$ and contribute $0$; ignore them. Otherwise, clipping does not increase the distance to $u \in [l, h]$, so

$$(x_{t+1} - u)^2 \le \Big(x_t - u - \eta\frac{g_t}{G_t}\Big)^2 = (x_t - u)^2 - \frac{2\eta}{G_t}g_t(x_t - u) + \eta^2\frac{g_t^2}{G_t^2}.$$

Rearranged, $g_t(x_t - u) \le \frac{G_t}{2\eta}\big((x_t - u)^2 - (x_{t+1} - u)^2\big) + \frac{\eta}{2}\frac{g_t^2}{G_t}$. Sum over the rounds with $G_t > 0$. Summation by parts on the first part, with $G$ nondecreasing, gives

$$\sum_t\frac{G_t}{2\eta}\big((x_t - u)^2 - (x_{t+1} - u)^2\big) \le \frac{1}{2\eta}\Big(G_{t_0}(x_{t_0} - u)^2 + \sum_{t > t_0}(G_t - G_{t-1})(x_t - u)^2\Big) \le \frac{D^2}{2\eta}G_T,$$

where $t_0$ is the first round with $G_t > 0$, because each $(x_t - u)^2 \le D^2$ and the weights are nonnegative and add up to $G_T$; the dropped term $-G_T(x_{T+1} - u)^2/(2\eta)$ is nonpositive. Lemma 1 with $a_t = g_t^2$ bounds the second part by $\frac{\eta}{2}\cdot2G_T$. $\square$

**Theorem (regret).** For every $u \in X$,

$$R_T(u) \le \sum_{i=1}^d\Big(\frac{D_i^2}{2\eta} + \eta\Big)\lVert g_{1:T,i}\rVert_2 \le \Big(\frac{D_\infty^2}{2\eta} + \eta\Big)\sum_{i=1}^d\lVert g_{1:T,i}\rVert_2.$$

With $\eta = D_\infty/\sqrt{2}$ the bound is $\sqrt{2}\,D_\infty\sum_i\lVert g_{1:T,i}\rVert_2$.

*Proof.* Convexity gives $f_t(x_t) - f_t(u) \le \langle g_t, x_t - u\rangle = \sum_ig_{t,i}(x_{t,i} - u_i)$. Sum over $t$ and apply Lemma 2 to each coordinate. The minimum of $D_\infty^2/(2\eta) + \eta$ over $\eta > 0$ is $\sqrt{2}D_\infty$, at $\eta = D_\infty/\sqrt{2}$. $\blacksquare$

**Corollary 1 (comparison).** If $\lVert g_t\rVert_\infty \le G_\infty$, then $\sum_i\lVert g_{1:T,i}\rVert_2 \le d\,G_\infty\sqrt{T}$, so $R_T = O(dD_\infty G_\infty\sqrt{T})$. If coordinate $i$ is nonzero in only $T_i$ rounds, the sum is at most $G_\infty\sum_i\sqrt{T_i}$, which can be much smaller. By Cauchy-Schwarz, $\sum_i\lVert g_{1:T,i}\rVert_2 \le \sqrt{d}\big(\sum_t\lVert g_t\rVert_2^2\big)^{1/2}$, so the bound with $\eta = D_\infty/\sqrt{2}$ is at most $\sqrt{2}\,D_\infty\sqrt{d}\,(\sum_t\lVert g_t\rVert_2^2)^{1/2}$. This is the order of the bound of projected online gradient descent with the best fixed step chosen in hindsight, on a box of Euclidean diameter up to $D_\infty\sqrt{d}$. So AdaGrad loses at most a constant factor against that bound and gains when the gradients are sparse or uneven across coordinates. $\square$

**Corollary 2 (stochastic convex optimization).** Let $f_t = f(\cdot, \xi_t)$ with independent $\xi_t$ and $F = \mathbb{E}f(\cdot, \xi)$ convex with minimizer $x^* \in X$. Then $\bar{x}_T = \frac{1}{T}\sum_{t\le T}x_t$ satisfies $\mathbb{E}F(\bar{x}_T) - F(x^*) \le \frac{1}{T}\mathbb{E}\Big[\big(\frac{D_\infty^2}{2\eta} + \eta\big)\sum_i\lVert g_{1:T,i}\rVert_2\Big]$.

*Proof.* $x_t$ depends only on $\xi_1, \dots, \xi_{t-1}$, so $\mathbb{E}f(x_t, \xi_t) = \mathbb{E}F(x_t)$ and $\mathbb{E}f(x^*, \xi_t) = F(x^*)$. Hence $\mathbb{E}R_T(x^*) = \sum_t\mathbb{E}(F(x_t) - F(x^*)) \ge T(\mathbb{E}F(\bar{x}_T) - F(x^*))$ by Jensen's inequality. Apply the Theorem with $u = x^*$. $\blacksquare$

**Remarks.** The bound needs no knowledge of the gradient sizes: the step $\eta/G_{t,i}$ adapts to them. It is a worst-case bound over all loss sequences, so the tests check it at every round on random sequences of linear and quadratic losses, where the best comparator is known in closed form. The full-matrix version, with $G_t = (\sum_sg_sg_s^\top)^{1/2}$, has a similar bound with $\operatorname{tr}(G_T)$ in place of $\sum_i\lVert g_{1:T,i}\rVert_2$ (Duchi, Hazan and Singer 2011); it is not proved here.
