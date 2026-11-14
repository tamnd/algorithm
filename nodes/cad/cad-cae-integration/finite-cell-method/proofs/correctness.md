---
title: The finite cell method for a bar, exactness of the continuous problem, well posedness for alpha = 0 and the error as alpha goes to 0
proves: [correctness]
status: full
---

We use the notation of the page. The physical bar is $(0, a)$ with $-(E u')' = f$, $u(0) = 0$ and $E u'(a) = P$, where $E > 0$ is constant and $f \in L^2(0, a)$. The embedding domain is $(0, L)$ with $L > a$, the stiffness is $k_\alpha = E$ on $(0, a)$ and $\alpha E$ on $(a, L)$, the load is $f$ on $(0, a)$ only, and the end $L$ is free. All integrals are exact. The exact split of line L2 makes this true for polynomial $f$, and the bisection only approximates it.

**Theorem 1 (the continuous problem).** Let $\alpha > 0$ and let $H = \{v \in H^1(0, L) : v(0) = 0\}$. The problem: find $w \in H$ with $\int_0^L k_\alpha w' v' \, dx = \int_0^a f v \, dx + P v(a)$ for all $v \in H$, has a unique solution, and $w = u$ on $(0, a)$ and $w = u(a)$ on $(a, L)$.

*Proof.* The bilinear form is bounded and, since $k_\alpha \ge \alpha E > 0$ and $v(0) = 0$, coercive on $H$ by the Poincaré inequality $\int_0^L v^2 \le L^2 \int_0^L v'^2$. The right side is a bounded functional, because $|v(a)| \le \sqrt{L} \, \|v'\|_{L^2}$. So the Lax-Milgram lemma gives a unique solution. Let $w$ be the function of the statement. It is in $H$, because $u$ is in $H^1(0, a)$ and $w$ is continuous at $a$. For $v \in H$, $w' = 0$ on $(a, L)$, so $\int_0^L k_\alpha w' v' = \int_0^a E u' v'$. Integration by parts on $(0, a)$ with $-(E u')' = f$, $v(0) = 0$ and $E u'(a) = P$ gives $\int_0^a E u' v' = \int_0^a f v + P v(a)$. So $w$ solves the problem, and by uniqueness it is the solution. $\square$

So for every $\alpha > 0$ the continuous FCM problem gives the exact solution on the physical part. The error of the discrete method comes from the discrete space, which ties the values on $(0, a)$ to those on $(a, L)$ through the polynomials of the cut cell, and from the quadrature.

**The discrete problem.** Let $V_h$ be the space of the page: continuous on the union of the active cells, a polynomial of degree $p \ge 1$ on each active cell, and $v(0) = 0$. With a basis of $V_h$, the matrix of line L8 is $K = K_0 + \alpha K_1$, where

$$ v^T K_0 w = \int_0^a E v' w' \, dx, \qquad v^T K_1 w = \int_a^{b} E v' w' \, dx, $$

$b$ is the right end of the last active cell, and $F$ does not depend on $\alpha$. We write $\|v\|_0 = (v^T K_0 v)^{1/2}$ and $\|v\|_1 = (v^T K_1 v)^{1/2}$. $K_1$ is symmetric and positive semi-definite.

**Lemma 1 ($K_0$ is positive definite).** If only active cells are kept, $K_0$ is symmetric positive definite.

*Proof.* Symmetry is clear. Let $v \in V_h$ with $v^T K_0 v = 0$. Then $v' = 0$ on $(0, a)$, and since $v$ is continuous with $v(0) = 0$, $v = 0$ on $[0, a]$. Each active cell $[x_c, x_{c+1}]$ has $x_c < a$, so it meets $(0, a)$ in an interval of positive length. On that interval the polynomial $v$ has infinitely many zeros, so $v = 0$ on the whole cell. So $v = 0$. $\square$

If a cell with $x_c \ge a$ were kept, its inner modes would have no stiffness for $\alpha = 0$, and $K_0$ would be singular. This is line L1.

**Corollary (the case alpha = 0).** For $\alpha = 0$ the system $K_0 u_0 = F$ has a unique solution, and $u_0$ restricted to $(0, a)$ is the Galerkin solution of the physical bar in the space of continuous piecewise polynomials on the mesh $\{x_0, \ldots, x_c, a\}$, with the cut part $(x_c, a)$ as the last element. By Galerkin orthogonality it is the best approximation of $u$ in the energy norm of $(0, a)$ from that space.

*Proof.* The restriction to $(0, a)$ is a bijection from $V_h$ onto that space, because a polynomial on a cut cell is fixed by its values on the part inside, and every piecewise polynomial on the truncated mesh extends to the full cut cell by the same polynomial. Both $K_0$ and $F$ only see $(0, a)$. So the system is the Galerkin system of the physical bar. Galerkin orthogonality, $\int_0^a E (u - u_0)' v' = 0$ for all $v$, gives the best approximation property. $\square$

**Theorem 2 (the error as alpha goes to 0).** Let $u_\alpha$ solve $(K_0 + \alpha K_1) u_\alpha = F$ for $\alpha \ge 0$, and let $C_{\text{ext}}$ be the largest eigenvalue of $K_0^{-1} K_1$, that is the largest value of $\|v\|_1^2 / \|v\|_0^2$ over $v \ne 0$. Then

$$ \|u_\alpha - u_0\|_0 \le \alpha \, C_{\text{ext}} \, \|u_0\|_0 \qquad \text{and} \qquad \|u_\alpha - u_0\|_0 \le \tfrac12 \sqrt{\alpha} \, \|u_0\|_1 . $$

*Proof.* $K_0 + \alpha K_1$ is positive definite by Lemma 1, so $u_\alpha$ exists. Let $e = u_\alpha - u_0$. Then $(K_0 + \alpha K_1) e = F - (K_0 + \alpha K_1) u_0 = -\alpha K_1 u_0$. Multiply by $e^T$:

$$ \|e\|_0^2 + \alpha \|e\|_1^2 = -\alpha \, e^T K_1 u_0 \le \alpha \, \|e\|_1 \, \|u_0\|_1 , $$

by the Cauchy-Schwarz inequality for the semi-definite form $K_1$.

For the first bound, drop $\alpha \|e\|_1^2 \ge 0$ and use $\|v\|_1 \le \sqrt{C_{\text{ext}}} \, \|v\|_0$ twice: $\|e\|_0^2 \le \alpha \, C_{\text{ext}} \, \|e\|_0 \, \|u_0\|_0$. Divide by $\|e\|_0$ if it is not zero.

For the second bound, use $\|e\|_1 \|u_0\|_1 \le \|e\|_1^2 + \tfrac14 \|u_0\|_1^2$. Then $\|e\|_0^2 + \alpha \|e\|_1^2 \le \alpha \|e\|_1^2 + \tfrac14 \alpha \|u_0\|_1^2$, so $\|e\|_0^2 \le \tfrac14 \alpha \|u_0\|_1^2$. $\square$

**Corollary (the total error).** By the triangle inequality and the first corollary, the energy error on $(0, a)$ satisfies

$$ \|u - u_\alpha\|_{E, (0, a)} \le \min_{v \in V_h} \|u - v\|_{E, (0, a)} + \min\left( \alpha C_{\text{ext}} \|u_0\|_0, \ \tfrac12 \sqrt{\alpha} \|u_0\|_1 \right), $$

and the second term tends to $0$ as $\alpha \to 0$. If $u$ is in the restricted space, the first term is $0$, $u_0 = u$, and the error is $O(\alpha)$. $\square$

**Proposition (one cell).** Let $L = 1$ with one cell, $p = 2$, $a = \tfrac12$, $E = 1$, $f = 1$ and $P = 0$. Then $u_\alpha(a) - u(a) = \dfrac{\alpha (1 - \alpha)}{8 (1 + 14 \alpha + \alpha^2)}$.

*Proof.* $V_h$ is the space of quadratics with $v(0) = 0$, with the basis $x$ and $x^2$. With $k_\alpha = 1$ on $(0, \tfrac12)$ and $\alpha$ on $(\tfrac12, 1)$:

$$ K = \begin{pmatrix} \tfrac{1 + \alpha}{2} & \tfrac{1 + 3\alpha}{4} \\ \tfrac{1 + 3\alpha}{4} & \tfrac{1 + 7\alpha}{6} \end{pmatrix}, \qquad F = \begin{pmatrix} \tfrac18 \\ \tfrac1{24} \end{pmatrix}, $$

from $\int_0^{1/2} 1 = \int_{1/2}^1 1 = \tfrac12$, $\int_0^{1/2} 2x = \tfrac14$, $\int_{1/2}^1 2x = \tfrac34$, $\int_0^{1/2} 4x^2 = \tfrac16$, $\int_{1/2}^1 4x^2 = \tfrac76$, $\int_0^{1/2} x = \tfrac18$ and $\int_0^{1/2} x^2 = \tfrac1{24}$. The determinant is $\frac{(1 + \alpha)(1 + 7\alpha)}{12} - \frac{(1 + 3\alpha)^2}{16} = \frac{D}{48}$ with $D = 1 + 14\alpha + \alpha^2$. Cramer's rule gives $c_1 = \frac{1 + 11\alpha}{2D}$ and $c_2 = -\frac{1 + 7\alpha}{2D}$, so $u_\alpha(\tfrac12) = \frac{c_1}{2} + \frac{c_2}{4} = \frac{1 + 15\alpha}{8D}$. The exact value is $u(\tfrac12) = \tfrac12 \cdot \tfrac12 - \tfrac18 = \tfrac18 = \frac{D}{8D}$, and the difference is $\frac{\alpha - \alpha^2}{8D}$. $\blacksquare$

**What is not proved here.** The exponential rate in $p$ of the best approximation for an analytic $u$ is the known rate of the p-version of the finite element method and is only measured on the page. The growth of $C_{\text{ext}}$ with $p$ and with a small cut, the condition numbers, and the error of the bisection quadrature are measured, not proved.
