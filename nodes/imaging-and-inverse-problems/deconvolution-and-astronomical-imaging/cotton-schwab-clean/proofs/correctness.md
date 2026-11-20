---
title: "Each major cycle of Cotton-Schwab CLEAN restores the exact residual, and the drift of a minor cycle is bounded by the sidelobes outside the patch"
proves: [correctness]
status: full
---

**Setting.** The image has $n$ pixels at directions $(l_q, m_q)$. The data are visibilities $V_j$ at $(u_j, v_j)$ with weights $w_j > 0$, $W = \sum_j w_j$. For a real model $M$, $(AM)_j = \sum_q M_q a_{jq}$ with $a_{jq} = e^{-2\pi i (u_j l_q + v_j m_q)}$, and for complex values $X$ the image is

$$\mathcal I(X)_q = \frac1W \sum_j w_j\, \mathrm{Re}\big(X_j\, \overline{a_{jq}}\big).$$

The beam is $B(q - r) = \frac1W \sum_j w_j \cos 2\pi\big(u_j (l_q - l_r) + v_j (m_q - m_r)\big)$, which depends only on the offset between two pixels of a regular grid; $B(0) = 1$. The misfit is $Q(M) = \frac1W \sum_j w_j |V_j - (AM)_j|^2$. For a patch half-width $P$, let $B_P(\Delta) = B(\Delta)$ when $|\Delta| \le P$ in each coordinate and $0$ otherwise, and $\beta_P = \max_\Delta |B(\Delta) - B_P(\Delta)|$, the largest beam value outside the patch.

**Claim 1 (the dirty image is a convolution).** For every real image $x$, $\mathcal I(Ax)_q = \sum_r B(q - r)\, x_r$.

*Proof.* $\mathcal I(Ax)_q = \frac1W \sum_j w_j \mathrm{Re} \sum_r x_r a_{jr} \overline{a_{jq}} = \sum_r x_r \frac1W \sum_j w_j \mathrm{Re}\, e^{2\pi i (u_j (l_q - l_r) + v_j (m_q - m_r))}$, and the inner sum is $B(q - r)$. $\square$

**Claim 2 (each major cycle starts from the exact residual).** After line L7, $V_r = V - AM$, so line L3 gives $R = \mathcal I(V - AM) = D - B \star M$, with $D = \mathcal I(V)$ and $\star$ the convolution of Claim 1. The same holds for the image returned by line L8.

*Proof.* $\mathcal I$ is linear over real scalars, and Claim 1 gives $\mathcal I(AM) = B \star M$. Lines L1 and L7 are the only lines that set $V_r$, and both make $V_r = V - AM$ for the current $M$. $\square$

So the state that a major cycle passes on is the model $M$ alone; whatever error the minor cycle made in its image is dropped.

**Claim 3 (the drift of a minor cycle).** Let a minor cycle start from the exact residual $R^{\mathrm{start}}$ and add the components $\Delta M$ (the sum of its steps). Let $\tilde R$ be the image it keeps and $R = \mathcal I(V - A(M + \Delta M))$ the exact residual. Then at every pixel

$$|\tilde R_q - R_q| \le \beta_P\, \|\Delta M\|_1 .$$

*Proof.* Each step at pixel $p$ with flux $c$ subtracts $c\,B_P(\cdot - p)$ from $\tilde R$, so $\tilde R = R^{\mathrm{start}} - B_P \star \Delta M$. By Claims 1 and 2, $R = R^{\mathrm{start}} - B \star \Delta M$. Hence $\tilde R_q - R_q = \sum_r (B - B_P)(q - r)\, \Delta M_r$, and each term is at most $\beta_P |\Delta M_r|$. $\square$

**Claim 4 (the cost of one component).** For every pixel $p$ and real $c$, with $R = \mathcal I(V - AM)$,

$$Q(M + c\,\delta_p) = Q(M) - 2c\, R_p + c^2 .$$

*Proof.* With $X = V - AM$, $Q(M + c\delta_p) = \frac1W \sum_j w_j |X_j - c\, a_{jp}|^2$. Since $|a_{jp}| = 1$, this is $Q(M) - \frac{2c}{W} \sum_j w_j \mathrm{Re}(X_j \overline{a_{jp}}) + \frac{c^2}{W} \sum_j w_j = Q(M) - 2cR_p + c^2$. $\square$

**Claim 5 (when a minor step lowers the true misfit).** Suppose a minor step sees the value $\tilde R_p$ at its chosen pixel, takes $c = g \tilde R_p$ with $0 < g < 2$, and the drift there is $|\tilde R_p - R_p| \le e$. Then

$$Q(M) - Q(M + c\,\delta_p) \ge g\, |\tilde R_p|\, \big((2 - g)|\tilde R_p| - 2e\big),$$

which is positive when $|\tilde R_p| > 2e / (2 - g)$.

*Proof.* By Claim 4 the drop is $2cR_p - c^2 = g \tilde R_p (2R_p - g \tilde R_p)$. Write $R_p = \tilde R_p + \epsilon$ with $|\epsilon| \le e$. Then $\tilde R_p R_p = \tilde R_p^2 + \tilde R_p \epsilon \ge \tilde R_p^2 - |\tilde R_p| e$, so the drop is at least $g(2\tilde R_p^2 - 2|\tilde R_p| e - g \tilde R_p^2)$. $\square$

Combined with Claim 3, a minor step is safe while its peak exceeds $2\beta_P \|\Delta M\|_1 / (2 - g)$. This is the reason to stop a minor cycle early. Clark's rule, which stops at $\beta_P$ times the starting peak, follows the same idea but does not bound $\|\Delta M\|_1$, so it is not a proof of descent.

**Claim 6 (the full patch).** If the patch holds the whole beam ($\beta_P = 0$), the minor cycle is Hogbom CLEAN on the exact non-periodic convolution, every step lowers $Q$ by $(2g - g^2) R_p^2$, and for $0 < g < 2$ and $\tau = 0$, $\max_q |R_q| \to 0$ and $Q(M)$ tends to its least value.

*Proof.* By Claim 3 the kept image is exact, so Claim 4 with $c = gR_p$ gives the drop. As on the Hogbom page, the drops have a finite sum and line L3 of the minor cycle takes the largest $|R_q|$, so $\max_q |R_q| \to 0$. Now $Q(M) = Q(0) - 2\langle D, M\rangle + \langle M, HM\rangle$ with $H_{qr} = B(q - r)$, and $\langle M, HM \rangle = \frac1W \sum_j w_j |(AM)_j|^2 \ge 0$, so $H$ is positive semidefinite, and $R = D - HM$ is minus half the gradient. A convex quadratic that is bounded below satisfies $Q(M) - \min Q = \langle R, H^{+} R\rangle \le \|R\|^2 / \lambda$, with $\lambda$ the smallest nonzero eigenvalue of $H$, and the right side tends to $0$. $\square$

**What is not claimed.** For $\beta_P > 0$ the method can raise $Q$ when the minor cycles go too far, and the page shows a run where it does. No convergence theorem is given for a cut beam with Clark's rule.
