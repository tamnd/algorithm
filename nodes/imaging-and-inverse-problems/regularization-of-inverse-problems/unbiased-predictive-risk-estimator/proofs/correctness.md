---
title: The SVD formula computes the UPRE function, the function is an unbiased estimate of the predictive risk, and the search terminates
proves: [correctness, termination]
status: full
---

**Setting.** $A$ is a real $m \times n$ matrix with thin SVD $A = \sum_{i=1}^r s_iu_iv_i^T$, $s_1 \ge \dots \ge s_r > 0$. For $\alpha > 0$, $x_\alpha = (A^TA + \alpha I)^{-1}A^Ty$ and $H_\alpha = A(A^TA + \alpha I)^{-1}A^T$, so $Ax_\alpha = H_\alpha y$. Line L1 computes $b_i = \langle u_i, y\rangle$ and $p^2 = \lVert y\rVert^2 - \sum_i b_i^2$. Write $f_i = s_i^2/(s_i^2 + \alpha)$.

**Claim 1 (the influence matrix).** $H_\alpha = \sum_i f_iu_iu_i^T$, so $\mathrm{trace}(H_\alpha) = \sum_i f_i$ and $\lVert(I - H_\alpha)y\rVert^2 = \sum_i (1 - f_i)^2b_i^2 + p^2$.

*Proof.* $(A^TA + \alpha I)^{-1}A^T = \sum_i s_i/(s_i^2 + \alpha)\,v_iu_i^T$, because $A^TA + \alpha I$ acts on $v_i$ as multiplication by $s_i^2 + \alpha$. Multiply by $A = \sum_i s_iu_iv_i^T$ on the left. For the norm, write $y = \sum_i b_iu_i + y_\perp$ with $\lVert y_\perp\rVert = p$; then $(I - H_\alpha)y = \sum_i (1 - f_i)b_iu_i + y_\perp$, and the terms are orthogonal. $\square$

**Claim 2 (line L2 computes U).** By Claim 1, the function $G$ of line L2 at $t = \log\alpha$ equals $U(\alpha) = \frac1m\lVert(I - H_\alpha)y\rVert^2 + \frac{2\sigma^2}{m}\mathrm{trace}(H_\alpha) - \sigma^2$. $\square$

**Claim 3 (unbiasedness).** Let $y = g + e$ with $g = Ax^\dagger$ fixed, $Ee = 0$ and $E\,ee^T = \sigma^2I_m$. For every fixed $\alpha > 0$,

$$E\,U(\alpha) = T(\alpha) := \tfrac1mE\lVert H_\alpha y - g\rVert^2.$$

*Proof.* For a fixed matrix $M$ and fixed vector $c$, $E\lVert c + Me\rVert^2 = \lVert c\rVert^2 + 2\langle c, M\,Ee\rangle + E\,\mathrm{trace}(M^TMee^T) = \lVert c\rVert^2 + \sigma^2\mathrm{trace}(M^TM)$. Write $H = H_\alpha$, which is symmetric. First, $(I - H)y = (I - H)g + (I - H)e$, so

$$E\lVert(I - H)y\rVert^2 = \lVert(I - H)g\rVert^2 + \sigma^2\,\mathrm{trace}((I - H)^2) = \lVert(I - H)g\rVert^2 + \sigma^2(m - 2\,\mathrm{trace}(H) + \mathrm{trace}(H^2)).$$

Second, $Hy - g = -(I - H)g + He$, so

$$mT = \lVert(I - H)g\rVert^2 + \sigma^2\,\mathrm{trace}(H^2).$$

Subtracting, $E\lVert(I - H)y\rVert^2 - mT = \sigma^2(m - 2\,\mathrm{trace}(H))$. Divide by $m$ and move the terms: $T = \frac1mE\lVert(I - H)y\rVert^2 + \frac{2\sigma^2}{m}\mathrm{trace}(H) - \sigma^2 = E\,U(\alpha)$, since $\mathrm{trace}(H)$ is not random. $\square$

**Link with Stein's lemma.** For Gaussian noise, Stein's unbiased risk estimate of $E\lVert h(y) - g\rVert^2$ for a weakly differentiable $h$ is $\lVert h(y) - y\rVert^2 + 2\sigma^2\,\mathrm{div}\,h(y) - m\sigma^2$. For $h(y) = H_\alpha y$ the divergence is $\sum_k \partial(H_\alpha y)_k/\partial y_k = \mathrm{trace}(H_\alpha)$, and dividing by $m$ gives $U$. Claim 3 shows that for linear $h$ Gaussianity is not needed.

**Claim 4 (termination and the grid guarantee).** The loop of lines L6 to L8 stops after $\lceil\log(w/\varepsilon)/\log(1/\varphi)\rceil$ steps, where $w$ is the width of the bracket of line L5 and $\varphi = (\sqrt5 - 1)/2$. The returned value of $G$ is at most $\min_j G(t_j)$, and it is the value at the returned $\alpha$.

*Proof.* Each golden-section step replaces $[a, c]$ by $[a, t_2]$ or $[t_1, c]$ with $t_1 = c - \varphi(c - a)$ and $t_2 = a + \varphi(c - a)$, so the width is multiplied by $\varphi$. After $K$ steps it is $w\varphi^K \le \varepsilon$ for the stated $K$, and the loop condition fails. Line L8 starts from the best grid point and only replaces it by a point with a smaller value; lines L9 and L10 return that point. $\square$

**Claim 5 (output).** Line L10 returns $x_\alpha = \sum_i s_ib_i/(s_i^2 + \alpha)\,v_i$, the Tikhonov solution for the returned $\alpha$, by the formula in the proof of Claim 1.

**What is not proved.** Claim 3 holds at each fixed $\alpha$. The returned $\hat\alpha$ depends on $e$, and in general $E\,U(\hat\alpha)$ is not the expected loss $\frac1mE\lVert H_{\hat\alpha}y - g\rVert^2$ at the data-dependent parameter. The closeness of the risk at the UPRE choice to the smallest risk, seen in the tests, is a measurement. Asymptotic results of this kind exist (Li 1987) under further conditions.
