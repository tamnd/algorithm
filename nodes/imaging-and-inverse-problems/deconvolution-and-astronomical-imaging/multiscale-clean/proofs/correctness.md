---
title: "Multiscale CLEAN keeps every smoothed residual exact, lowers the misfit at each step, and fits the data in the limit"
proves: [correctness]
status: full
---

**Setting.** As on the [Hogbom CLEAN](/hogbom-clean/) page: a periodic grid of $n$ pixels (read indices as 2D for an image), the DFT $\hat y_k = \sum_q y_q e^{-2\pi i kq/n}$, a real sky $x$ with $V = \hat x$, weights $w_k \ge 0$ with $w_{-k} = w_k$ and $W = \sum_k w_k > 0$, the dirty beam $B_q = \frac1W \sum_k w_k e^{2\pi i kq/n}$ (real, $B_0 = 1$), and the dirty image $D = B \ast x$. The misfit is $Q(M) = \frac1W \sum_k w_k |V_k - \hat M_k|^2$. The scale functions $\phi_0 = \delta, \phi_1, \ldots, \phi_{s-1}$ are real and symmetric, $\phi_u(-q) = \phi_u(q)$. Write $R = D - B \ast M$, $I_t = \phi_t \ast R$ and $B_{ut} = \phi_u \ast \phi_t \ast B$. The loop is lines L1 to L9 with $\tau = 0$.

From the Hogbom page (Claim 1 there), for every model $M$,

$$R_q = \frac1W \sum_k w_k (V_k - \hat M_k) e^{2\pi i kq/n}. \tag{1}$$

**Claim 1 (the smoothed residuals stay exact).** After every step, $I_t = \phi_t \ast (D - B \ast M)$ for every scale $t$. In particular $I_0 = R$.

*Proof.* Line L1 makes it true with $M = 0$. A step adds $c\,\phi_u(\cdot - p) = c\,\phi_u \ast \delta_p$ to $M$, which changes $\phi_t \ast (D - B \ast M)$ by $-c\,\phi_t \ast B \ast \phi_u \ast \delta_p = -c\,B_{ut}(\cdot - p)$, since periodic convolution is commutative and associative. Line L8 makes exactly this change to $I_t$. $\square$

**Claim 2 (the cost of a step).** Let $\psi = \phi_u(\cdot - p)$. For every real $c$,

$$Q(M + c\,\psi) = Q(M) - 2c\, I_u(p) + c^2 B_{uu}(0).$$

*Proof.* $\hat\psi_k = \hat\phi_u(k) e^{-2\pi i kp/n}$, and $\hat\phi_u(k)$ is real because $\phi_u$ is real and symmetric. Expanding the square as on the Hogbom page,

$$Q(M + c\psi) = Q(M) - \frac{2c}{W} \mathrm{Re} \sum_k w_k (V_k - \hat M_k)\, \hat\phi_u(k)\, e^{2\pi i kp/n} + \frac{c^2}{W} \sum_k w_k\, \hat\phi_u(k)^2 .$$

By (1) and the convolution theorem, $\frac1W \sum_k w_k (V_k - \hat M_k) \hat\phi_u(k) e^{2\pi i kq/n} = (\phi_u \ast R)_q = I_u(q)$, which is real; take $q = p$. The DFT of $B$ is $\hat B_k = n w_k / W$, so $B_{uu}(0) = \frac1n \sum_k \hat\phi_u(k)^2 \hat B_k = \frac1W \sum_k w_k \hat\phi_u(k)^2$. $\square$

$B_{uu}(0) \ge 0$, and the code requires $B_{uu}(0) > 0$: the scale must have some weight on the measured frequencies. For $u = 0$, $B_{00}(0) = B_0 = 1$.

**Claim 3 (the drop).** With $c = g\, I_u(p) / B_{uu}(0)$ (line L6),

$$Q(M) - Q(M + c\psi) = (2g - g^2)\, \frac{I_u(p)^2}{B_{uu}(0)} = \frac{2 - g}{g}\, c^2 B_{uu}(0).$$

*Proof.* Substitute $c$ in Claim 2. $\square$

So for $0 < g < 2$ every step lowers $Q$ unless $I_u(p) = 0$, and line L4 (with no bias) picks the pair $(u, p)$ with the largest drop.

**Claim 4 (convergence).** Let $0 < g < 2$, $\tau = 0$, and let line L4 maximize $\beta_u |I_u(p)| / \sqrt{B_{uu}(0)}$ with fixed weights $\beta_u > 0$ (no bias is $\beta_u = 1$). Then $\max_q |R_q| \to 0$, $Q(M) \to 0$, and $\hat M_k \to V_k$ at every measured frequency.

*Proof.* Let $\beta_{\max} = \max_u \beta_u$ and $b = \max_u B_{uu}(0)$. At the step that picks $(u, p)$, the choice of line L4 gives, for every pixel $q$ and using the point scale,

$$\beta_u \frac{|I_u(p)|}{\sqrt{B_{uu}(0)}} \ge \beta_0 \frac{|I_0(q)|}{\sqrt{B_{00}(0)}} = \beta_0 |R_q|,$$

so $I_u(p)^2 / B_{uu}(0) \ge (\beta_0 / \beta_{\max})^2 \max_q R_q^2$. By Claim 3, each step lowers $Q$ by at least $(2g - g^2)(\beta_0 / \beta_{\max})^2 \max_q R_q^2$. Since $Q \ge 0$ these amounts have a finite sum, so $\max_q |R_q| \to 0$ along the iterations. By (1), $R$ is a fixed invertible linear map of the vector $(w_k (V_k - \hat M_k))_k$, so each $w_k (V_k - \hat M_k) \to 0$, and $Q \to 0$ as on the Hogbom page. $\square$

**Claim 5 (one scale is Hogbom CLEAN).** If the only scale is $\phi_0 = \delta$, then $I_0 = R$, $B_{00} = B$, the score in line L4 is $|R_p|$, and lines L6 to L8 are lines L5 to L7 of Hogbom CLEAN.

*Proof.* $\delta \ast \delta \ast B = B$ and $\delta \ast R = R$. $\square$

**What is not claimed.** The set of models with $Q = 0$ is the sky plus every image whose DFT vanishes on the measured frequencies, and the iteration may approach any of them; the proof does not say that $M$ converges, nor that a larger scale set gives a model closer to the sky. The example on the page shows a closer model in one case; that is a measurement, not a theorem. If some $\phi_u$ is not symmetric, $\hat\phi_u(k)$ is complex and $I_u(p)$ is no longer the inner product of the blob with the residual, so Claim 2 fails.
