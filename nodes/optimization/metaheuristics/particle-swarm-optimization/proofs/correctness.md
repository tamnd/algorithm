---
title: PSO keeps the best points it has visited, and under stagnation the mean of a particle converges exactly when |w| < 1 and 0 < c1 + c2 < 4(1 + w)
proves: [correctness]
status: full
---

We use the pseudocode of the page and minimize $f : \mathbb{R}^n \to \mathbb{R}$.

**Claim 1 (personal bests).** After each execution of line L8 for particle $i$, $f(p_i) = \min\{f(y) : y \text{ a point that particle } i \text{ has visited}\}$, and $p_i$ is one of these points.

*Proof.* By induction on the number of moves of particle $i$. Line L1 sets $p_i = x_i$, the only visited point. A move adds one visited point, the new $x_i$ of line L7. Line L8 replaces $p_i$ by it exactly when $f(x_i) < f(p_i)$, so $f(p_i)$ becomes the minimum of the old minimum and $f(x_i)$. $\square$

**Claim 2 (global best).** At all times $f(g) = \min_i f(p_i)$, and $g$ is one of the $p_i$ or a former value of one. So $f(g)$ is the smallest value of $f$ at all evaluated points, and it never increases.

*Proof.* Line L2 gives $f(g) = \min_i f(p_i)$. A personal best changes only in line L8, and only to a point $x_i$ with a smaller value. If $f(x_i) < f(g)$, line L9 sets $g = x_i$, and the minimum over the $p_i$ is now $f(x_i) = f(g)$. Otherwise $f(x_i) \ge f(g)$ and the minimum does not change. By Claim 1 the minimum over the $p_i$ is the minimum over all visited points. $\square$

**Lemma (roots in the unit disk).** Let $a, b \in \mathbb{R}$. Both roots of $z^2 - a z + b$ satisfy $|z| < 1$ if and only if $|b| < 1$ and $|a| < 1 + b$.

*Proof.* Let $q(z) = z^2 - a z + b$, with roots $z_1, z_2$, so $z_1 z_2 = b$.

If $a^2 < 4b$, the roots are complex conjugates with $|z_1|^2 = |z_2|^2 = b > 0$. If $|b| < 1$ and $|a| < 1 + b$, then $|z_j|^2 = b < 1$. Conversely, if $|z_j| < 1$, then $0 < b < 1$, and $|a| < 2\sqrt{b} \le 1 + b$ by the inequality of the arithmetic and geometric means.

If $a^2 \ge 4b$, the roots are real, $z_1 \le z_2$. Suppose both lie in $(-1, 1)$. Then $|b| = |z_1 z_2| < 1$, and since $q$ has a positive leading coefficient and $\pm 1$ lie outside $[z_1, z_2]$, $q(1) = 1 - a + b > 0$ and $q(-1) = 1 + a + b > 0$, that is $|a| < 1 + b$. Conversely, suppose $|b| < 1$ and $|a| < 1 + b$. Then $q(1) > 0$, $q(-1) > 0$, and the vertex $a/2$ satisfies $|a/2| < (1 + b)/2 < 1$. A parabola that opens upward, is positive at $-1$ and at $1$, and has its vertex between them, has both its roots strictly between $-1$ and $1$. $\square$

**Claim 3 (first-order stability).** Fix a particle and a coordinate, and suppose that $p = p_{i,d}$ and $q = g_d$ do not change from some time on (stagnation). Let $x_t$ be the coordinate after the particle's $t$th move and $m_t = \mathrm{E}[x_t]$. Then for every start $(m_0, m_1)$, $m_t$ converges if and only if $|w| < 1$ and $0 < c_1 + c_2 < 4(1 + w)$, and the limit is $(c_1 p + c_2 q)/(c_1 + c_2)$.

*Proof.* Lines L6 and L7 give $v_{t+1} = w v_t + \varphi_1 (p - x_t) + \varphi_2 (q - x_t)$ and $x_{t+1} = x_t + v_{t+1}$, where $\varphi_1 = c_1 r_1$ and $\varphi_2 = c_2 r_2$ with fresh uniform $r_1, r_2$. Since $v_t = x_t - x_{t-1}$,
$$x_{t+1} = (1 + w - \varphi_1 - \varphi_2) x_t - w x_{t-1} + \varphi_1 p + \varphi_2 q.$$
The factors $\varphi_1, \varphi_2$ are independent of $x_t$ and $x_{t-1}$, with means $c_1/2$ and $c_2/2$. Taking expectations, with $\bar c = (c_1 + c_2)/2$,
$$m_{t+1} = (1 + w - \bar c) m_t - w m_{t-1} + \tfrac{1}{2}(c_1 p + c_2 q).$$
If $c_1 + c_2 \ne 0$, the constant sequence $m^* = (c_1 p + c_2 q)/(c_1 + c_2)$ solves this recurrence, and $e_t = m_t - m^*$ satisfies $e_{t+1} = a e_t - b e_{t-1}$ with $a = 1 + w - \bar c$ and $b = w$. A linear recurrence of order 2 tends to 0 for every start if and only if both roots of $z^2 - a z + b$ have modulus less than 1. If a root $z$ has $|z| \ge 1$, the start $(e_0, e_1) = (1, z)$ gives $e_t = z^t$ (or its real part for complex $z$), which does not tend to 0. By the Lemma, the condition is $|w| < 1$ and $|1 + w - \bar c| < 1 + w$, that is $0 < \bar c < 2(1 + w)$, or $0 < c_1 + c_2 < 4(1 + w)$. If $c_1 + c_2 = 0$ the condition fails and $a = 1 + w$, $b = w$ give the root $z = 1$, so the mean does not converge for every start. $\square$

The same proof with fixed values $\varphi_1 + \varphi_2 = \varphi$ in place of random ones gives the deterministic model of Clerc and Kennedy: $x_t$ converges to $(\varphi_1 p + \varphi_2 q)/\varphi$ for every start if and only if $|w| < 1$ and $0 < \varphi < 2(1 + w)$.

**Claim 4 (second moments, for reference).** Under the same stagnation with $p = q$, let $y_t = x_t - p$. Then $y_{t+1} = A_t y_t - w y_{t-1}$ with $A_t = 1 + w - \varphi_1 - \varphi_2$ independent of the past, $\mathrm{E}[A_t] = \mu = 1 + w - \bar c$ and $\mathrm{E}[A_t^2] = s = \mu^2 + (c_1^2 + c_2^2)/12$. So the vector $(\mathrm{E}[y_t^2], \mathrm{E}[y_t y_{t-1}], \mathrm{E}[y_{t-1}^2])$ is multiplied in each step by
$$M = \begin{pmatrix} s & -2 w \mu & w^2 \\ \mu & -w & 0 \\ 1 & 0 & 0 \end{pmatrix}.$$
The second moments converge for every start if and only if the spectral radius of $M$ is less than 1. For $c_1 = c_2$, Poli (2009) showed that this holds if and only if $|w| < 1$ and $c_1 + c_2 < 24(1 - w^2)/(7 - 5w)$. The test of the implementation checks this region against iterations of $M$ on a grid of parameters. $\blacksquare$
