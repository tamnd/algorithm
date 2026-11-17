---
title: Go-ICP returns a pose within eps of the global minimum over its domain, and stops
proves: [correctness, termination]
status: full
---

We use the notation of the page. The source is $P = (p_1, \ldots, p_n)$ and the target is $Q = \{q_1, \ldots, q_m\}$ in $\mathbb{R}^3$. For an angle-axis vector $r \in \mathbb{R}^3$, $R_r = \operatorname{Exp}(r)$ is the rotation by the angle $|r|$ about $r / |r|$. The residuals and the cost are

$$e_i(R, t) = \min_j |R p_i + t - q_j|, \qquad E(R, t) = \sum_{i=1}^n e_i(R, t)^2 .$$

The rotation domain is a cube $C_r$ of angle-axis vectors, and the translation domain is a cube $C_t$ with center $t_c$ and half side $\tau$. A cube of half side $\sigma$ is the set of points whose coordinates differ from those of its center by at most $\sigma$, so every point of it is within $\sqrt{3}\sigma$ of the center. Let $D = \{(r, t) : r \in C_r, |r| \le \pi, t \in C_t\}$ and $m^\star = \min_D E(R_r, t)$; the minimum exists because $D$ is compact and $E$ is continuous. We assume exact arithmetic and eps $> 0$.

**Claim.** GO-ICP stops after finitely many steps and returns $(R, t, E)$ with $E = E(R, t)$, $\det R = +1$ and $E < m^\star + \text{eps}$.

**Lemma 1 (rotation uncertainty).** Let $r, r_0$ lie in a cube of half side $\sigma$ with center $r_0$. Then for every $x \in \mathbb{R}^3$,

$$|R_r x - R_{r_0} x| \le \gamma(\sigma, x) := 2 \sin\big(\min(\sqrt{3}\sigma/2,\, \pi/2)\big)\, |x| .$$

*Proof.* Let $v(s) = r_0 + s (r - r_0)$ for $s \in [0, 1]$ and $y(s) = R_{v(s)} x$. The derivative of $s \mapsto \operatorname{Exp}(v(s))$ has the form $\dot R = [\omega]_\times R$ with $\omega = \mathcal{J}(v) \dot v$, where for $\theta = |v| > 0$

$$\mathcal{J}(v) = I + \frac{1 - \cos\theta}{\theta^2} [v]_\times + \frac{\theta - \sin\theta}{\theta^3} [v]_\times^2$$

is the left Jacobian of the exponential map of $SO(3)$, and $\mathcal{J}(0) = I$. $\mathcal{J}(v)$ maps $v$ to $v$, since $[v]_\times v = 0$. For a unit vector $u$ orthogonal to $v$, with $\hat v = v/\theta$ and $u' = \hat v \times u$, we get $[v]_\times u = \theta u'$ and $[v]_\times^2 u = -\theta^2 u$, so $\mathcal{J}(v) u = \frac{\sin\theta}{\theta} u + \frac{1 - \cos\theta}{\theta} u'$. This vector is orthogonal to $v$, and its length is $\sqrt{2 - 2\cos\theta}/\theta = 2\sin(\theta/2)/\theta \le 1$. So $\mathcal{J}(v)$ maps the line of $v$ and the plane orthogonal to it into themselves, it is the identity on the line, and it multiplies lengths in the plane by $2\sin(\theta/2)/\theta \le 1$. Write $z$ as the sum of its parts on the line and in the plane; the images of the parts are orthogonal, so $|\mathcal{J}(v) z| \le |z|$ for all $z$. Hence $|\omega(s)| \le |\dot v| = |r - r_0|$.

The point $y(s)$ stays on the sphere of radius $|x|$ about the origin, and $|\dot y| = |\omega \times y| \le |\omega|\,|x|$. So the length of the path $y$ is at most $|r - r_0|\,|x|$. The angle $\varphi \in [0, \pi]$ between $y(0)$ and $y(1)$ times $|x|$ is the length of the shortest path on the sphere between them, so $\varphi \le |r - r_0| \le \sqrt{3}\sigma$. Also $\varphi \le \pi$. The chord is $|y(1) - y(0)| = 2 \sin(\varphi / 2) |x|$, and $\sin$ increases on $[0, \pi/2]$, so the chord is at most $2 \sin(\min(\sqrt{3}\sigma, \pi)/2) |x| = \gamma(\sigma, x)$. $\square$

**Lemma 2 (residual bound).** Let $r$ lie in the rotation cube of half side $\sigma_r$ with center $r_0$, and $t$ in the translation cube of half side $\sigma_t$ with center $t_0$. Let $\gamma_i = \gamma(\sigma_r, p_i)$ and $\gamma_t = \sqrt{3}\sigma_t$. Then $e_i(R_r, t) \ge \max(e_i(R_{r_0}, t_0) - \gamma_i - \gamma_t,\, 0)$ and $e_i(R_r, t) \ge \max(e_i(R_{r_0}, t) - \gamma_i, 0)$.

*Proof.* For every $j$, the triangle inequality and Lemma 1 give $|R_r p_i + t - q_j| \ge |R_{r_0} p_i + t_0 - q_j| - |R_r p_i - R_{r_0} p_i| - |t - t_0| \ge e_i(R_{r_0}, t_0) - \gamma_i - \gamma_t$. Take the minimum over $j$, and use $e_i \ge 0$. The second bound is the case $t_0 = t$, $\gamma_t = 0$. $\square$

Fix a rotation cube with center $r_0$ and half side $h$, and let $\gamma_i = \gamma(h, p_i)$. Define $f(t) = \sum_i \max(e_i(R_{r_0}, t) - \gamma_i, 0)^2$. Squaring keeps the order of nonnegative numbers, so Lemma 2 gives $E(R_r, t) \ge f(t)$ for every $r$ in the cube, and, for a translation cube of half side $s$ and center $c$, $f(t) \ge \underline f(c, s) := \sum_i \max(e_i(R_{r_0}, c) - \gamma_i - \sqrt{3}s, 0)^2$ for every $t$ in it.

**Lemma 3 (the inner search).** INNER-BNB, called with the bound $E_b$, returns $(E_t, t_b, L)$ such that: $E_t \le E_b$; if $t_b$ is not None, $t_b \in C_t$ and $f(t_b) = E_t$; and $L \le \min(E_t, \min_{t \in C_t} f(t))$. It stops after finitely many steps.

*Proof.* The value $E_t$ starts at $E_b$ (line L9) and changes only to a value $f(c)$ at an evaluated center $c$ with $f(c) < E_t$ (line L12), and then $t_b = c$. Centers of sub-cubes of $C_t$ lie in $C_t$. This gives the first two parts.

For the third part, say that a cube was *not pushed* when its bound $\underline f$ was at least the value of $E_t$ at the time it was made. Invariant: every $t \in C_t$ lies in a cube in the queue, or in a cube that was not pushed. This holds at the start, because $C_t$ is pushed or not pushed in line L9, and a popped cube is the union of its 8 children, each pushed or not pushed in line L13. If $t$ lies in a cube that was not pushed, then $f(t) \ge \underline f \ge E_t^{\text{then}} \ge E_t$, since $E_t$ never increases. If $t$ lies in a cube in the queue, $f(t)$ is at least the bound of that cube, and so at least the least bound in the queue. Line L14 returns $L = \min(E_t, \text{least bound in the queue})$, or $E_t$ if the queue is empty, so $L \le f(t)$ for every $t \in C_t$, and $L \le E_t$.

Termination. Let $A$ bound $e_i(R_{r_0}, t)$ over $t \in C_t$ and all $i$; it exists since $C_t$ is bounded. For $a, g \ge 0$ and $\delta \ge 0$, $\max(a - g, 0)^2 - \max(a - g - \delta, 0)^2 \le 2\delta \max(a - g, 0) \le 2 \delta A$. So for a cube of half side $s$ and center $c$, $f(c) - \underline f(c, s) \le 2\sqrt{3}\, n A s$. When a cube is pushed, $E_t \le f(c)$ already holds (line L12 runs before line L13), and $E_t$ never increases. So when a cube of half side $s$ is at the top of the queue, $E_t - \text{lb} \le 2\sqrt{3}\, n A s$. Once $s < \delta / (2\sqrt{3}\, n A)$ this is below $\delta$, and line L10 stops. There are $8^k$ cubes of half side $\tau / 2^k$, so only finitely many cubes of half side at least that threshold can be popped. Hence the search stops. $\square$

**Lemma 4 (the outer lower bound).** When line L7 pushes a rotation cube with center $r_0$ and half side $h$ and bound $L$, then $E(R_r, t) \ge L$ for every $r$ in that cube and $t \in C_t$.

*Proof.* $E(R_r, t) \ge f(t) \ge \min_{C_t} f \ge L$ by the remark after Lemma 2 and Lemma 3. $\square$

*Proof of the claim: the returned value.* $E$ is set in line L1 to the cost of the pose that local ICP returns, and later only to $\text{Eu} = E(R_{r_0}, t_b)$, computed from the true residuals, or to the cost that local ICP returns, which it computes at the pose it returns. So $E = E(R, t)$ at the end. Every rotation is $R_{r_0}$, the identity, or a Kabsch rotation with the sign fix, so $\det R = +1$.

*Proof of the claim: the bound.* Invariant of the outer loop: every $(r, t) \in D$ has $r$ in a rotation cube in the queue, or $E(R_r, t) \ge E$ for the current $E$. At the start the queue holds $C_r$ with the bound 0, which is a valid lower bound. When a cube is popped, its 8 children cover it. A child that line L4 drops has $|r_0| - \sqrt{3}h > \pi$, so every $r$ in it has $|r| \ge |r_0| - |r - r_0| > \pi$, and it holds no point of $D$. A child that line L7 does not push has $L \ge E$ at that time, so by Lemma 4 every $(r, t)$ with $r$ in it has $E(R_r, t) \ge L \ge E$; and $E$ never increases later. A child that is pushed is in the queue, with a valid bound by Lemma 4. So the invariant holds. At the stop, either the queue is empty and $m^\star \ge E$, or the least bound lb in the queue has $E - \text{lb} < \text{eps}$, and $m^\star \ge \min(E, \text{lb}) > E - \text{eps}$. In both cases $E < m^\star + \text{eps}$.

*Proof of the claim: termination.* Each call of INNER-BNB stops by Lemma 3; it uses $\delta = \text{eps}/2$ and the extra stop rule $E_b - \text{lb} < \text{eps}$ with $E_b$ the current $E$. Let $A$ bound all residuals $e_i(R, t)$ over all rotations $R$ and $t \in C_t$. For a rotation cube of half side $h$, $\gamma_i \le \sqrt{3} h |p_i|$, and so for every $t$, $E(R_{r_0}, t) - f(t) \le \sum_i 2\gamma_i A \le 2\sqrt{3}\, h A \sum_i |p_i| =: \beta(h)$, by the inequality of Lemma 3 with $\delta = \gamma_i$. Consider a child cube whose inner search, called with $E_b$ equal to the current $E$, returns $(E_t, t_b, L)$ with $L = \min(E_t, \text{lb})$, or $L = E_t$ if the queue is empty. The search ends in one of three ways. If the queue is empty, $L = E_t$. If it breaks because $E_t - \text{lb} < \text{eps}/2$, then $E_t - L < \text{eps}/2$. If it breaks because $E_b - \text{lb} < \text{eps}$, then $L = E_t$ or $L = \text{lb} > E_b - \text{eps}$. So either (i) $L > E_b - \text{eps}$, or (ii) $E_t - L < \text{eps}/2$.

In case (i), the cube is pushed only if $L < E \le E_b$, and then $E - L < \text{eps}$. In case (ii) with $t_b$ not None, line L6 leaves $E \le \text{Eu} = E(R_{r_0}, t_b) \le f(t_b) + \beta(h) = E_t + \beta(h) < L + \text{eps}/2 + \beta(h)$. In case (ii) with $t_b$ None, $E_t = E_b = E$, so $E - L < \text{eps}/2$. So once $\beta(h) < \text{eps}/2$, a child of half side $h$ is either not pushed, or pushed with $E - L < \text{eps}$ for the $E$ of that moment. Later values of $E$ are not larger, so the gap stays below eps. When such a cube reaches the top of the queue, line L2 stops. Only finitely many cubes have $\beta(h) \ge \text{eps}/2$, since there are $8^k$ cubes at depth $k$ and $\beta(h) \to 0$ as $h \to 0$. Each pop takes finitely many steps. Hence GO-ICP stops. $\blacksquare$

**Remarks.** The returned pose need not lie in $D$, because the local ICP of line L6 can move outside the domain; the bound compares $E$ with the least cost over $D$, and a pose outside $D$ with a smaller cost only helps. In floating point the bounds are computed with rounding, so the guarantee holds up to the rounding error of the sums. The upper bound of line L6 replaces the second inner search of Yang et al. with $\gamma = 0$; the proof above shows that the guarantee does not need that search.
