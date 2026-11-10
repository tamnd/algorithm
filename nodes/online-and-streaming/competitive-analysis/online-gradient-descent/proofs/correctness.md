---
title: Online gradient descent has regret at most D²/(2η_T) + Σ η_t‖g_t‖²/2, so (3/2)GD√T with η_t = D/(G√t), and (G²/(2λ))(1 + ln T) for λ-strongly convex losses with η_t = 1/(λt)
proves: [regret-bound, strongly-convex-regret]
status: full
---

Let $K \subset \mathbb{R}^d$ be nonempty, closed and convex, with diameter $D = \sup_{x, y \in K}\|x - y\|$, where $\|\cdot\|$ is the Euclidean norm. The losses $f_1, \ldots, f_T$ are convex on $K$ and may depend on the earlier points. The algorithm starts at $x_1 \in K$ (line L1), plays $x_t$, receives $g_t \in \partial f_t(x_t)$ (line L5), and sets $x_{t+1} = \Pi_K(x_t - \eta_t g_t)$ (lines L6 and L7), where $\Pi_K(y)$ is the point of $K$ nearest to $y$. Fix any comparator $x^* \in K$ and write $a_t = \|x_t - x^*\|^2$, so $0 \le a_t \le D^2$. The regret against $x^*$ is $R_T(x^*) = \sum_t (f_t(x_t) - f_t(x^*))$, and the regret $R_T$ is its maximum over $x^* \in K$.

**Lemma 1 (projection moves closer to every point of $K$).** For every $y \in \mathbb{R}^d$ and $u \in K$, $\|\Pi_K(y) - u\| \le \|y - u\|$.

*Proof.* Let $p = \Pi_K(y)$. For $s \in (0, 1]$ the point $p + s(u - p)$ lies in $K$ by convexity, so $\|y - p - s(u - p)\|^2 \ge \|y - p\|^2$. Expand: $-2s\langle y - p, u - p\rangle + s^2\|u - p\|^2 \ge 0$. Divide by $s$ and let $s \to 0$: $\langle y - p, u - p\rangle \le 0$. Then

$$\|y - u\|^2 = \|y - p\|^2 + \|p - u\|^2 - 2\langle y - p, u - p\rangle \ge \|p - u\|^2. \qquad \square$$

**Lemma 2 (one step).** For every $t$, $\langle g_t, x_t - x^*\rangle \le \dfrac{a_t - a_{t+1}}{2\eta_t} + \dfrac{\eta_t}{2}\|g_t\|^2$.

*Proof.* By Lemma 1 with $y = x_t - \eta_t g_t$ and $u = x^*$,

$$a_{t+1} \le \|x_t - \eta_t g_t - x^*\|^2 = a_t - 2\eta_t\langle g_t, x_t - x^*\rangle + \eta_t^2\|g_t\|^2.$$

Rearrange and divide by $2\eta_t > 0$. $\square$

**Theorem 1 (regret for convex losses).** If $\eta_1 \ge \eta_2 \ge \cdots \ge \eta_T > 0$, then

$$R_T \le \frac{D^2}{2\eta_T} + \frac12\sum_{t=1}^{T}\eta_t\|g_t\|^2.$$

If $\|g_t\| \le G$ for all $t$ and $\eta_t = D/(G\sqrt t)$, then $R_T \le \frac32 GD\sqrt T - \frac12 GD$. If $T$ is known and $\eta_t = D/(G\sqrt T)$ for all $t$, then $R_T \le GD\sqrt T$.

*Proof.* Convexity gives $f_t(x^*) \ge f_t(x_t) + \langle g_t, x^* - x_t\rangle$, so $f_t(x_t) - f_t(x^*) \le \langle g_t, x_t - x^*\rangle$. Sum Lemma 2 over $t$. The first part is

$$\sum_{t=1}^{T}\frac{a_t - a_{t+1}}{2\eta_t} = \frac{a_1}{2\eta_1} + \sum_{t=2}^{T} a_t\left(\frac{1}{2\eta_t} - \frac{1}{2\eta_{t-1}}\right) - \frac{a_{T+1}}{2\eta_T}.$$

The brackets are $\ge 0$ since the steps do not increase, and $a_t \le D^2$ and $a_{T+1} \ge 0$, so the sum is at most $D^2\bigl(\frac{1}{2\eta_1} + \sum_{t=2}^{T}(\frac{1}{2\eta_t} - \frac{1}{2\eta_{t-1}})\bigr) = \frac{D^2}{2\eta_T}$. This gives the first bound for every $x^*$, so for $R_T$.

With $\eta_t = D/(G\sqrt t)$, the first term is $\frac{D^2 G\sqrt T}{2D} = \frac12 GD\sqrt T$, and the second is at most $\frac{G^2}{2}\cdot\frac{D}{G}\sum_t \frac{1}{\sqrt t} = \frac{GD}{2}\sum_t\frac{1}{\sqrt t}$. For $t \ge 2$, $\frac{1}{\sqrt t} \le \frac{2}{\sqrt t + \sqrt{t-1}} = 2(\sqrt t - \sqrt{t-1})$, so $\sum_{t=1}^{T} \frac{1}{\sqrt t} \le 1 + 2(\sqrt T - 1) = 2\sqrt T - 1$. Together, $R_T \le \frac12 GD\sqrt T + GD\sqrt T - \frac12 GD$.

With the fixed step $\eta = D/(G\sqrt T)$, the two terms are $\frac12 GD\sqrt T$ and $\frac{G^2}{2}\cdot T\cdot\frac{D}{G\sqrt T} = \frac12 GD\sqrt T$. $\square$

A function $f$ is $\lambda$-strongly convex on $K$, for $\lambda > 0$, if $f(y) \ge f(x) + \langle g, y - x\rangle + \frac{\lambda}{2}\|y - x\|^2$ for all $x, y \in K$ and all $g \in \partial f(x)$.

**Theorem 2 (strongly convex losses; Hazan, Agarwal and Kale 2007).** If every $f_t$ is $\lambda$-strongly convex and $\eta_t = 1/(\lambda t)$, then

$$R_T \le \sum_{t=1}^{T}\frac{\|g_t\|^2}{2\lambda t} \le \frac{G^2}{2\lambda}H_T \le \frac{G^2}{2\lambda}(1 + \ln T),$$

where $G = \max_t\|g_t\|$ and $H_T = \sum_{t=1}^{T} 1/t$.

*Proof.* Strong convexity at $x_t$ with $y = x^*$ gives $f_t(x_t) - f_t(x^*) \le \langle g_t, x_t - x^*\rangle - \frac{\lambda}{2}a_t$. With Lemma 2 and $1/\eta_t = \lambda t$,

$$2\bigl(f_t(x_t) - f_t(x^*)\bigr) \le \lambda t\,a_t - \lambda t\,a_{t+1} - \lambda a_t + \eta_t\|g_t\|^2 = \lambda(t-1)a_t - \lambda t\,a_{t+1} + \frac{\|g_t\|^2}{\lambda t}.$$

Sum over $t = 1, \ldots, T$. The terms $\lambda(t-1)a_t - \lambda t\,a_{t+1}$ telescope to $0\cdot a_1 - \lambda T a_{T+1} \le 0$. So $2R_T(x^*) \le \sum_t \|g_t\|^2/(\lambda t)$ for every $x^*$. Finally $\|g_t\| \le G$, and $H_T \le 1 + \int_1^T \frac{dx}{x} = 1 + \ln T$. $\square$

**Corollary 1 (OGD and follow the leader for squared loss).** Let $K = [0, 1]$, $f_t(x) = (x - z_t)^2$ with $z_t \in [0, 1]$, which is $2$-strongly convex, and $\eta_t = 1/(2t)$. Then $x_{t+1} = \frac1t\sum_{s \le t} z_s$ for every $t \ge 1$, which is the point of follow the leader, and $R_T \le H_T$.

*Proof.* The update is $x_t - \frac{1}{2t}\cdot 2(x_t - z_t) = \frac{(t-1)x_t + z_t}{t}$. For $t = 1$ this is $z_1$. If $x_t$ is the mean of $z_1, \ldots, z_{t-1}$, it is the mean of $z_1, \ldots, z_t$, which lies in $[0, 1]$, so the projection does nothing. Here $|g_t| = 2|x_t - z_t| \le 2$, and Theorem 2 gives $R_T \le \frac{4}{4}H_T$. $\square$
