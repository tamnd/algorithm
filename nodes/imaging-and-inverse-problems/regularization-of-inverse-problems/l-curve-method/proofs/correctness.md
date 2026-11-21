---
title: The L-curve is monotone, the closed-form curvature is its signed curvature, and the corner search terminates with a point at least as curved as the best grid point
proves: [correctness, termination]
status: full
---

**Setting.** $A$ is a real $m \times n$ matrix with thin SVD $A = \sum_{i=1}^r s_iu_iv_i^T$ and $s_1 \ge \dots \ge s_r > 0$. For data $y$, line L1 computes $b_i = \langle u_i, y\rangle$ and $p^2 = \lVert y\rVert^2 - \sum_i b_i^2 \ge 0$, the squared norm of the part of $y$ outside the range of $A$. For $\alpha > 0$ the Tikhonov solution is $x_\alpha = (A^TA + \alpha I)^{-1}A^Ty$. Assume some $s_ib_i \ne 0$; otherwise $x_\alpha = 0$ for every $\alpha$ and there is no curve.

**Claim 1 (the two norms).** With $q_i = s_i^2 + \alpha$,

$$x_\alpha = \sum_i \frac{s_ib_i}{q_i}v_i, \qquad \eta = \lVert x_\alpha\rVert^2 = \sum_i \frac{s_i^2b_i^2}{q_i^2}, \qquad \rho = \lVert Ax_\alpha - y\rVert^2 = \sum_i \frac{\alpha^2b_i^2}{q_i^2} + p^2.$$

*Proof.* In the basis $v_i$ the normal equations $(A^TA + \alpha I)x = A^Ty$ are diagonal, with $q_i\xi_i = s_ib_i$ for $i \le r$ and $\alpha\xi = 0$ on the null space of $A$. Then $Ax_\alpha - y = \sum_i (s_i^2/q_i - 1)b_iu_i - P^\perp y$ with $s_i^2/q_i - 1 = -\alpha/q_i$, and Pythagoras gives both norms. $\square$

**Claim 2 (monotonicity).** $\eta' = -2\sum_i s_i^2b_i^2/q_i^3 < 0$ and $\rho' = -\alpha\eta' > 0$. So as $\alpha$ grows, the curve $(X, Y) = (\frac12\log\rho, \frac12\log\eta)$ moves strictly right and strictly down.

*Proof.* Differentiate term by term: $\frac{d}{d\alpha}(s_i^2b_i^2q_i^{-2}) = -2s_i^2b_i^2q_i^{-3}$, and $\frac{d}{d\alpha}(\alpha^2b_i^2q_i^{-2}) = 2\alpha b_i^2q_i^{-2} - 2\alpha^2b_i^2q_i^{-3} = 2\alpha b_i^2s_i^2q_i^{-3}$. The second is $-\alpha$ times the first. Some $s_ib_i \ne 0$, so $\eta' < 0$. $\square$

**Claim 3 (the curvature formula).** The signed curvature $\kappa = (X'Y'' - X''Y')/(X'^2 + Y'^2)^{3/2}$ of the curve, with $'$ the derivative in $\alpha$, equals

$$\kappa = -\frac{2\eta\rho\,(\alpha\eta'\rho + \alpha^2\eta'\eta + \eta\rho)}{\eta'\,(\alpha^2\eta^2 + \rho^2)^{3/2}}.$$

*Proof.* We have $X' = \rho'/(2\rho)$, $Y' = \eta'/(2\eta)$, $X'' = \rho''/(2\rho) - \rho'^2/(2\rho^2)$ and $Y'' = \eta''/(2\eta) - \eta'^2/(2\eta^2)$. By Claim 2, $\rho' = -\alpha\eta'$ and so $\rho'' = -\eta' - \alpha\eta''$. Substitute:

$$4(X'Y'' - X''Y') = \frac{\rho'}{\rho}\Big(\frac{\eta''}{\eta} - \frac{\eta'^2}{\eta^2}\Big) - \frac{\eta'}{\eta}\Big(\frac{\rho''}{\rho} - \frac{\rho'^2}{\rho^2}\Big) = \frac{-\alpha\eta'\eta''}{\rho\eta} + \frac{\alpha\eta'^3}{\rho\eta^2} + \frac{\eta'^2 + \alpha\eta'\eta''}{\eta\rho} + \frac{\alpha^2\eta'^3}{\eta\rho^2}.$$

The two terms with $\eta''$ cancel. Over the common denominator $\eta^2\rho^2$ the rest is $\eta'^2(\alpha\eta'\rho + \eta\rho + \alpha^2\eta'\eta)/(\eta^2\rho^2)$. Also

$$4(X'^2 + Y'^2) = \frac{\alpha^2\eta'^2}{\rho^2} + \frac{\eta'^2}{\eta^2} = \frac{\eta'^2(\alpha^2\eta^2 + \rho^2)}{\eta^2\rho^2}.$$

So

$$\kappa = \frac{\eta'^2(\alpha\eta'\rho + \alpha^2\eta'\eta + \eta\rho)/(4\eta^2\rho^2)}{|\eta'|^3(\alpha^2\eta^2 + \rho^2)^{3/2}/(8\eta^3\rho^3)} = \frac{2\eta\rho(\alpha\eta'\rho + \alpha^2\eta'\eta + \eta\rho)}{|\eta'|(\alpha^2\eta^2 + \rho^2)^{3/2}},$$

and $|\eta'| = -\eta'$ by Claim 2. $\square$

The sign convention: the curve runs right and down as $\alpha$ grows, and $\kappa > 0$ means that it turns counterclockwise, from steep to flat, which is the turn at the corner of an L.

**Claim 4 (invariance).** The value of $\kappa$ at a point of the curve does not depend on the parameter. In particular, $\kappa$ computed in $\alpha$ equals $\kappa$ computed in $t = \log\alpha$.

*Proof.* Let $\alpha = g(t)$ with $g' > 0$. Then $\dot X = X'g'$ and $\ddot X = X''g'^2 + X'g''$, and the same for $Y$. So $\dot X\ddot Y - \ddot X\dot Y = g'^3(X'Y'' - X''Y')$, because the $g''$ terms cancel, and $(\dot X^2 + \dot Y^2)^{3/2} = g'^3(X'^2 + Y'^2)^{3/2}$. The factors $g'^3$ cancel. $\square$

**Claim 5 (scaling).** Replacing $A$ and $y$ by $cA$ and $cy$ with $c > 0$ maps the curvature at $\alpha$ to the curvature at $c^2\alpha$ of the new problem, and the solution is unchanged.

*Proof.* The new singular values are $cs_i$ and the new coefficients $cb_i$. At $c^2\alpha$ each term of $\eta$ is unchanged and each term of $\rho$ is multiplied by $c^2$. So the new curve is the old one shifted by $(\log c, 0)$, a rigid motion, and the curvature is unchanged. The solution $\sum_i cs_icb_iv_i/(c^2q_i)$ is the old one. $\square$

**Claim 6 (termination and the guarantee of the search).** Let $w = t_{j^\ast+1} - t_{j^\ast-1}$ be the width of the bracket from line L5 (at most $2(\log s_1^2 - \log s_r^2)/(P - 1)$). The loop of lines L6 to L8 stops after $K = \lceil\log(w/\varepsilon)/\log(1/\varphi)\rceil$ steps, with $\varphi = (\sqrt5 - 1)/2$. The returned $\alpha$ satisfies $\kappa(\alpha) \ge \max_j k_j$. If $\kappa(e^t)$ is unimodal on the bracket, the returned $t$ is within $\varepsilon$ of the maximizer on the bracket.

*Proof.* The search keeps two interior points $t_1 < t_2$ of $[a, c]$ at the golden ratio positions $t_1 = c - \varphi(c - a)$ and $t_2 = a + \varphi(c - a)$. If $\kappa(t_1) \ge \kappa(t_2)$ it replaces $c$ by $t_2$, otherwise $a$ by $t_1$. Since $\varphi^2 = 1 - \varphi$, the kept interior point is at a golden position of the new bracket, so one new evaluation per step suffices, and the width is multiplied by $\varphi$ in every step. After $K$ steps it is $w\varphi^K \le \varepsilon$, so the loop stops. Line L8 starts from the best grid point $(t_{j^\ast}, k_{j^\ast})$ and replaces it only by a point with a larger value, so the returned value is at least $k_{j^\ast} = \max_j k_j$, and line L9 returns the $\alpha$ where it was attained. If the function is unimodal on $[a, c]$, each step discards a part of the bracket that contains no point larger than the kept interior point, so the maximizer stays in $[a, c]$. The returned $t$ was evaluated inside the final bracket or is at least as good as all points evaluated in it, so it lies within the final width of the maximizer when the function is unimodal. $\square$

**Claim 7 (the output).** Line L10 returns $x_\alpha = \sum_i s_ib_i/(s_i^2 + \alpha)\,v_i$, the Tikhonov solution for the chosen $\alpha$, by Claim 1.

**What is not proved.** The claims above make the algorithm a correct and terminating maximizer of the curvature. They do not say that the corner gives a small error. By the Bakushinskii veto, no rule that does not use the noise level can make $x_\alpha \to x^\dagger$ for all $x^\dagger$ and all noise as the noise goes to zero, and Hanke (1996) and Vogel (1996) give explicit model problems where the L-curve choice fails to converge. The good behaviour in the example of the page is a measurement.
