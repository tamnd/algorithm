---
title: "Hogbom CLEAN is greedy coordinate descent on the visibility misfit, and its residual tends to zero for 0 < g < 2"
proves: [correctness]
status: full
---

**Setting.** The grid is periodic with $n$ pixels and a 1D index; for an image read every index as a 2D index and every DFT as the 2D DFT. The DFT is $\hat y_k = \sum_q y_q e^{-2\pi i kq/n}$. The sky $x$ is real and $V = \hat x$. The weights satisfy $w_k \ge 0$, $w_{-k} = w_k$ and $W = \sum_k w_k > 0$. The dirty beam and the dirty image are

$$B_q = \frac1W \sum_k w_k e^{2\pi i kq/n}, \qquad D_q = \frac1W \sum_k w_k V_k e^{2\pi i kq/n}.$$

$B$ is real because $w$ is symmetric, and $B_0 = \frac1W \sum_k w_k = 1$. The model $M$ is a real image, and the misfit is

$$Q(M) = \frac1W \sum_k w_k\, |V_k - \hat M_k|^2 \;\ge\; 0 .$$

The loop is lines L1 to L8 with $\tau = 0$, no window and no positive option, unless stated. Write $M^{(t)}$ and $R^{(t)}$ for the model and the residual after $t$ steps, and $p_t$, $c_t$ for the pixel and the flux of step $t$.

**Claim 1 (the invariant).** After each step, $R^{(t)} = D - B \ast M^{(t)}$, and

$$R^{(t)}_q = \frac1W \sum_k w_k \big(V_k - \hat M^{(t)}_k\big) e^{2\pi i kq/n}.$$

*Proof.* At $t = 0$, $R = D$ and $M = 0$. Step $t$ adds $c_t \delta_{p_t}$ to $M$ (line L6) and subtracts $c_t B_{q - p_t}$ from $R_q$ (line L7). Since $(B \ast \delta_p)_q = B_{q-p}$, the identity $R = D - B \ast M$ is kept. For the formula, $(B \ast M)_q = \sum_r B_{q-r} M_r = \frac1W \sum_k w_k \big(\sum_r M_r e^{-2\pi i kr/n}\big) e^{2\pi i kq/n} = \frac1W \sum_k w_k \hat M_k e^{2\pi i kq/n}$. Subtract this from $D_q$. $\square$

**Claim 2 (one step changes the misfit by an exact amount).** For every real $c$ and pixel $p$,

$$Q(M + c\,\delta_p) = Q(M) - 2c\,R_p + c^2 B_0, \qquad R = D - B \ast M .$$

*Proof.* The DFT of $c\,\delta_p$ is $c\, e^{-2\pi i kp/n}$. Expand $|a - b|^2 = |a|^2 - 2\,\mathrm{Re}(a \bar b) + |b|^2$ with $a = V_k - \hat M_k$ and $b = c\,e^{-2\pi i kp/n}$:

$$Q(M + c\delta_p) = Q(M) - \frac{2c}{W}\, \mathrm{Re} \sum_k w_k (V_k - \hat M_k) e^{2\pi i kp/n} + \frac{c^2}{W} \sum_k w_k .$$

By Claim 1 the middle sum is $W R_p$; it is real because $R$ is real. The last term is $c^2 B_0$. $\square$

So $Q$ is a convex quadratic in $M$ with $\partial Q / \partial M_p = -2 R_p$ and with second derivative $2B_0$ along each coordinate. The exact minimizer along the coordinate $p$ is $c = R_p / B_0$, and line L5 takes $g$ times it. Line L3 picks the coordinate with the largest $|\partial Q / \partial M_p|$. This is coordinate descent with the greedy (Gauss-Southwell) rule and a damped step.

**Claim 3 (the drop).** With $c = g R_p / B_0$,

$$Q(M) - Q(M + c\,\delta_p) = (2g - g^2)\, \frac{R_p^2}{B_0} .$$

For $0 < g < 2$ this is $\ge 0$, and $> 0$ when $R_p \ne 0$. For $g = 2$ it is $0$, and for $g > 2$ it is negative, so $Q$ rises.

*Proof.* Put $c = g R_p / B_0$ in Claim 2: $-2cR_p + c^2 B_0 = (-2g + g^2) R_p^2 / B_0$. $\square$

**Claim 4 (convergence).** Let $0 < g < 2$, $\tau = 0$ and no window. Then $\max_q |R^{(t)}_q| \to 0$ and $Q(M^{(t)}) \to 0$ as $t \to \infty$. In particular $\hat M^{(t)}_k \to V_k$ at every frequency with $w_k > 0$.

*Proof.* By Claim 3 and $Q \ge 0$,

$$(2g - g^2) \sum_{t \ge 0} \frac{\big(R^{(t)}_{p_{t+1}}\big)^2}{B_0} \le Q(0) < \infty,$$

so $R^{(t)}_{p_{t+1}} \to 0$. Line L3 picks the largest $|R_q|$, so $\max_q |R^{(t)}_q| = |R^{(t)}_{p_{t+1}}| \to 0$. By Claim 1, $R^{(t)}$ is the inverse DFT of $\frac{n}{W} w_k (V_k - \hat M^{(t)}_k)$. The inverse DFT is a fixed invertible linear map, so each $w_k (V_k - \hat M^{(t)}_k) \to 0$. Each term of $Q$ is $\frac1W w_k |V_k - \hat M_k|^2 = \frac{1}{W w_k} |w_k(V_k - \hat M_k)|^2$ when $w_k > 0$ and $0$ when $w_k = 0$, so $Q(M^{(t)}) \to 0$. $\square$

Claim 4 is about the data, not the sky. The set of models with $Q = 0$ is $x$ plus every image whose DFT is zero on the measured frequencies, and CLEAN may approach any point of it, or no single point (the theorem does not say that $M^{(t)}$ itself converges).

**Claim 5 (with a window).** Let the window be a set $S$ of pixels, and let line L3 pick the largest $|R_q|$ over $q \in S$. For $0 < g < 2$ and $\tau = 0$, $\max_{q \in S} |R^{(t)}_q| \to 0$, and $Q(M^{(t)})$ tends to the least value of $Q$ over the models that are zero outside $S$.

*Proof.* The first part is the proof of Claim 4 with the maximum over $S$. Restricted to the models $m$ that are zero outside $S$, $Q$ is a convex quadratic $f(m) = Q(0) - 2\langle d, m\rangle + \langle m, Hm\rangle$, with $H$ symmetric and positive semidefinite (the restriction of $B$ as a matrix $B_{q-r}$, $q, r \in S$, which is positive semidefinite because its eigenvalues on the full grid are $n w_k / W \ge 0$). Its gradient is $-2 R|_S$. A convex quadratic that is bounded below has $d$ in the range of $H$, and then $f(m) - \min f = \langle Hm - d, H^{+}(Hm - d)\rangle \le \|R|_S\|^2 / \lambda$, where $\lambda$ is the smallest nonzero eigenvalue of $H$. The right side tends to $0$. $\square$

**Claim 6 (full coverage).** If $w_k = 1$ for every $k$, then $B = \delta_0$ and $D = x$. With $g = 1$, CLEAN stops after as many steps as $x$ has nonzero pixels, with $M = x$ and $R = 0$ (with $\tau$ above round-off). With $g \ne 1$ each component is reached geometrically: the residual at $p$ is multiplied by $1 - g$ at each visit, which tends to $0$ exactly when $|1 - g| < 1$, that is $0 < g < 2$.

*Proof.* $B_q = \frac1n \sum_k e^{2\pi i kq/n} = \delta_{q,0}$, so $D = x$ and line L7 changes only $R_p$, to $R_p - g R_p = (1 - g)R_p$. With $g = 1$ each visited pixel becomes $0$ and is never visited again, and $M_p$ gets the full value $x_p$. $\square$

Claim 6 shows that the range $0 < g < 2$ of Claim 4 cannot be widened: for $g \ge 2$ a single point source with full coverage gives $|R_p| \ge |x_p|$ at every step.

**Restoring.** RESTORE (line L9) is a convolution and an addition, and makes no claim of optimality. With the invariant of Claim 1 the restored image is $C \ast M + D - B \ast M$, so it equals $D$ plus $(C - B) \ast M$: the components with the dirty beam replaced by the clean beam.
