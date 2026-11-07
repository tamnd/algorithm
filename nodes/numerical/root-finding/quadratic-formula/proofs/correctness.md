---
title: The stable quadratic formula returns the roots, each with relative error at most 7u/2 + O(u^2)
proves: [correctness, error-bound]
status: full
---

Write $h = b/2$, $D = h^2 - ac$ and $p(x) = a x^2 + b x + c$ with $a \ne 0$. In floating point, $\operatorname{fl}(x \circ y) = (x \circ y)(1 + \delta)$ and $\operatorname{fl}(\sqrt x) = \sqrt x\,(1 + \delta)$ with $|\delta| \le u$ when no underflow or overflow occurs (the standard model; see [floating-point arithmetic](/floating-point-arithmetic/)).

**Claim 1 (exact arithmetic).** QUADRATIC returns the two roots of $p$, with multiplicity.

*Proof.* Line L2 multiplies $a, b, c$ by the same nonzero number, which does not change the roots. Completing the square gives $p(x) = a\big((x + h/a)^2 - D/a^2\big)$, so the roots are $x = (-h \pm \sqrt D)/a$, real and distinct if $D > 0$, a double root $-h/a$ if $D = 0$, and the complex pair $(-h \pm i\sqrt{-D})/a$ if $D < 0$, which lines L5 and L6 return. Let $D \ge 0$ and $\sigma = 1$ if $h \ge 0$, $\sigma = -1$ otherwise. Line L7 sets $q = -(h + \sigma\sqrt D)$, so $x_1 = q/a$ is one of the two roots. The product of the roots is $c/a$ (expand $a(x - x_1)(x - x_2)$). If $q \ne 0$, the other root is $(c/a)/(q/a) = c/q$, which line L9 returns. If $q = 0$, then $h + \sigma\sqrt D = 0$; both terms have the sign $\sigma$ or are zero, so $h = 0$ and $D = 0$, hence $ac = 0$, so $c = 0$ and $p(x) = a x^2$ has the double root $0$ of line L8. $\square$

**Claim 2 (floating point).** Assume binary64 with round to nearest and that, after line L2, no operation underflows or overflows. Let $x_1, x_2$ be the exact roots of the stored scaled coefficients. Then the computed $D$ has the sign of $D$, the computed real roots are $x_i(1 + \theta_i)$, and the computed real and imaginary parts in the complex case are the exact ones times $1 + \theta$, with every $|\theta| \le \tfrac72 u + O(u^2)$.

*Proof.* Line L2 multiplies by a power of two, which is exact. In line L3, $h = b/2$ is exact, and $\hat D = D(1 + \delta_1)$ because $D$ is formed exactly and rounded once; in particular $\hat D$ and $D$ have the same sign, and $\hat D = 0$ only if $D = 0$.

*Real case.* $\hat s = \operatorname{fl}(\sqrt{\hat D}) = \sqrt D\,(1 + \delta_1)^{1/2}(1 + \delta_2) = \sqrt D\,(1 + \epsilon_s)$ with $|\epsilon_s| \le \tfrac32 u + O(u^2)$. Say $h \ge 0$ (the other case is the same with signs changed). Then $\hat q = -\operatorname{fl}(h + \hat s) = -(h + \sqrt D + \sqrt D\,\epsilon_s)(1 + \delta_3)$. Since $h \ge 0$ and $\sqrt D \ge 0$, $|\sqrt D\,\epsilon_s| \le |h + \sqrt D|\,|\epsilon_s|$, so $\hat q = q(1 + \epsilon_q)$ with $|\epsilon_q| \le \tfrac52 u + O(u^2)$. Then $\operatorname{fl}(\hat q/a) = (q/a)(1 + \epsilon_q)(1 + \delta_4)$ and $\operatorname{fl}(c/\hat q) = (c/q)(1 + \delta_5)/(1 + \epsilon_q)$, and both factors are $1 + \theta$ with $|\theta| \le \tfrac72 u + O(u^2)$. If $\hat q = 0$ then $q = 0$, and line L8 is exact.

*Complex case.* $\operatorname{fl}(-h/a) = (-h/a)(1 + \delta_6)$, and $\operatorname{fl}(\sqrt{-\hat D}/a) = (\sqrt{-D}/a)(1 + \delta_1)^{1/2}(1 + \delta_7)(1 + \delta_8)$, whose factor is $1 + \theta$ with $|\theta| \le \tfrac52 u + O(u^2)$. $\square$

**Remark (no cancellation is essential).** The step $|\sqrt D\,\epsilon_s| \le |h + \sqrt D|\,|\epsilon_s|$ uses that $h$ and $\sigma\sqrt D$ have the same sign. With the other sign, $|h - \sqrt D|$ can be much smaller than $\sqrt D$, and the same computation only gives an absolute error of about $u\sqrt D$; this is the failure of the textbook formula. $\blacksquare$
