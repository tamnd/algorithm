---
title: The SVD formula computes the GCV function, the search terminates, and the expected GCV function is the predictive risk plus the noise variance up to a relative error bounded by the trace of the influence matrix
proves: [correctness, termination]
status: full
---

**Setting.** $A$ is a real $m \times n$ matrix with thin SVD $A = \sum_{i=1}^r s_iu_iv_i^T$, $s_1 \ge \dots \ge s_r > 0$. For $\alpha > 0$ the Tikhonov solution is $x_\alpha = (A^TA + \alpha I)^{-1}A^Ty$ and the influence matrix is $H_\alpha = A(A^TA + \alpha I)^{-1}A^T$, so $Ax_\alpha = H_\alpha y$. Line L1 computes $b_i = \langle u_i, y\rangle$ and $p^2 = \lVert y\rVert^2 - \sum_i b_i^2$. Write $f_i = s_i^2/(s_i^2 + \alpha) \in (0, 1)$.

**Claim 1 (the influence matrix).** $H_\alpha = \sum_i f_iu_iu_i^T$. Hence $\mathrm{trace}(H_\alpha) = \sum_i f_i$, $\mathrm{trace}(I - H_\alpha) = m - \sum_i f_i > 0$ whenever $m > r$ or $\alpha > 0$, and

$$\lVert(I - H_\alpha)y\rVert^2 = \sum_i (1 - f_i)^2b_i^2 + p^2.$$

*Proof.* $A^TA + \alpha I = \sum_i (s_i^2 + \alpha)v_iv_i^T + \alpha P_N$ with $P_N$ the projector on the null space of $A$, and $A^T = \sum_i s_iv_iu_i^T$ maps into the span of the $v_i$. So $(A^TA + \alpha I)^{-1}A^T = \sum_i s_i/(s_i^2 + \alpha)\,v_iu_i^T$ and $H_\alpha = \sum_i s_i^2/(s_i^2 + \alpha)\,u_iu_i^T$. The trace of $u_iu_i^T$ is $1$. Each $f_i < 1$, so $m - \sum_i f_i > m - r \ge 0$. Write $y = \sum_i b_iu_i + y_\perp$ with $\lVert y_\perp\rVert = p$; then $(I - H_\alpha)y = \sum_i (1 - f_i)b_iu_i + y_\perp$, and Pythagoras gives the norm. $\square$

**Claim 2 (line L2 computes V).** For $t = \log\alpha$, the function $G$ of line L2 equals $V(\alpha) = \frac1m\lVert(I - H_\alpha)y\rVert^2/[\frac1m\mathrm{trace}(I - H_\alpha)]^2$.

*Proof.* By Claim 1, $V = \frac1m R/(\frac1m T_r)^2 = mR/T_r^2$ with $R = \sum_i (1 - f_i)^2b_i^2 + p^2$ and $T_r = m - \sum_i f_i$. That is $G$. $\square$

**Claim 3 (termination and the grid guarantee).** The loop of lines L6 to L8 stops after $\lceil\log(w/\varepsilon)/\log(1/\varphi)\rceil$ steps, with $w$ the width of the bracket of line L5 and $\varphi = (\sqrt5 - 1)/2$. The returned value of $G$ is at most $\min_j G(t_j)$, and it is the value at the returned $\alpha$.

*Proof.* Each golden-section step replaces $[a, c]$ by $[a, t_2]$ or $[t_1, c]$, where $t_1 = c - \varphi(c - a)$ and $t_2 = a + \varphi(c - a)$, so the width is multiplied by $\varphi$; since $\varphi^2 = 1 - \varphi$ the kept interior point is at a golden position of the new bracket. After $K$ steps the width is $w\varphi^K$, which is at most $\varepsilon$ for the stated $K$. Line L8 starts from the best grid point $(t_{j^\ast}, G(t_{j^\ast}))$ and only replaces it by a point with a smaller value, and lines L9 and L10 return that point and its value. $\square$

**Claim 4 (output).** Line L10 returns $x_\alpha = \sum_i s_ib_i/(s_i^2 + \alpha)\,v_i$, the Tikhonov solution, by the formula in the proof of Claim 1.

**Claim 5 (expected GCV function; Golub, Heath and Wahba 1979, Theorem 1).** Let $y = g + e$ with $g = Ax^\dagger$ and $e \sim N(0, \sigma^2I_m)$, or more generally $Ee = 0$ and $E\,ee^T = \sigma^2I_m$. Fix $\alpha$ with $\mu_1 = \frac1m\mathrm{trace}(H_\alpha) < 1$, and let $\mu_2 = \frac1m\mathrm{trace}(H_\alpha^2)$ and $T = \frac1mE\lVert H_\alpha y - g\rVert^2$. Then

$$E\,V(\alpha) = \frac{\beta^2 + \sigma^2(1 - 2\mu_1 + \mu_2)}{(1 - \mu_1)^2}, \qquad \beta^2 = \tfrac1m\lVert(I - H_\alpha)g\rVert^2,$$

and

$$\frac{|E\,V(\alpha) - \sigma^2 - T|}{T} \le \frac{2\mu_1 + \mu_1^2/\mu_2}{(1 - \mu_1)^2}.$$

*Proof.* Write $H = H_\alpha$, which is symmetric and does not depend on $y$. The denominator of $V$ is the constant $(1 - \mu_1)^2$, so $E\,V$ is $\frac1mE\lVert(I - H)y\rVert^2$ divided by it. For any fixed matrix $M$, $E\lVert M(g + e)\rVert^2 = \lVert Mg\rVert^2 + 2\langle Mg, M\,Ee\rangle + E\,e^TM^TMe = \lVert Mg\rVert^2 + \sigma^2\mathrm{trace}(M^TM)$. With $M = I - H$, $\mathrm{trace}((I - H)^2) = m(1 - 2\mu_1 + \mu_2)$, which gives the formula for $E\,V$. With $M = H$ applied to $y$ and $g$ subtracted, $H y - g = -(I - H)g + He$, so the same computation gives $T = \beta^2 + \sigma^2\mu_2$.

Now compute the numerator of $E\,V - \sigma^2 - T$ over the common denominator $(1 - \mu_1)^2$:

$$\beta^2 + \sigma^2(1 - 2\mu_1 + \mu_2) - (\sigma^2 + T)(1 - 2\mu_1 + \mu_1^2).$$

Substitute $\beta^2 = T - \sigma^2\mu_2$. The terms $\sigma^2\mu_2$ cancel, the terms $\sigma^2(1 - 2\mu_1)$ cancel, and what is left is

$$T - \sigma^2\mu_1^2 - T(1 - 2\mu_1 + \mu_1^2) = T(2\mu_1 - \mu_1^2) - \sigma^2\mu_1^2.$$

Both $T(2\mu_1 - \mu_1^2)$ and $\sigma^2\mu_1^2$ are nonnegative because $0 \le \mu_1 < 1$, so the absolute value is at most their sum. Since $T = \beta^2 + \sigma^2\mu_2 \ge \sigma^2\mu_2$, we have $\sigma^2 \le T/\mu_2$, so the sum is at most $T(2\mu_1 - \mu_1^2 + \mu_1^2/\mu_2) \le T(2\mu_1 + \mu_1^2/\mu_2)$. Divide by $T(1 - \mu_1)^2$. $\square$

**What Claim 5 means and does not mean.** If $\mu_1 \to 0$ and $\mu_1^2/\mu_2 \to 0$ along a family of problems, for example when the effective number of parameters $\mathrm{trace}(H_\alpha)$ grows more slowly than $m$, then $E\,V(\alpha) - \sigma^2 = T(\alpha)(1 + o(1))$, and the minimizer of the expected GCV function is close to the minimizer of the predictive risk. The claim is about the expectation of $V$ at a fixed $\alpha$. It does not bound the risk at the random minimizer of $V$ for one draw of the noise; results of that kind, such as Li (1987), need further conditions. The claim is about the predictive risk and not about $\lVert x_\alpha - x^\dagger\rVert$. And for a deterministic noise model it gives nothing: by the Bakushinskii veto, a rule that does not use the noise level cannot be convergent for all noise. The near-optimal errors in the example of the page and in the tests are measurements.
