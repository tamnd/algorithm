---
title: The first-order distance approximates the geometric distance to second order, the Taubin fit is the smallest eigenvector of the reduced generalized eigenproblem, it is exact on noise-free data, and it is invariant under similarities
proves: [correctness, termination]
status: full
---

**Setup.** The basis functions $\varphi_1, \dots, \varphi_n$ are polynomials on $\mathbb{R}^d$, linearly independent, and $f_a = \sum_j a_j \varphi_j$. The data are $x_1, \dots, x_m$. $J(x)$ is the $n \times d$ matrix with row $j$ equal to $\nabla \varphi_j(x)^{\mathsf T}$, so $\nabla f_a(x) = J(x)^{\mathsf T} a$. $M = \sum_i \varphi(x_i) \varphi(x_i)^{\mathsf T}$, $N = \sum_i J(x_i) J(x_i)^{\mathsf T}$, and $D$ is the $m \times n$ matrix with rows $\varphi(x_i)^{\mathsf T}$, so $M = D^{\mathsf T} D$. Termination is clear: the algorithm has one loop over the points, one Cholesky factorization and one eigen solve; the Jacobi solver of the code stops after a fixed maximum number of sweeps.

**Lemma 1 (first-order distance).** Let $Z = \{ f = 0 \}$ for a $C^2$ function $f$, let $x$ be a point, and let $y \in Z$ be a nearest point of $Z$ to $x$, at distance $\delta = \lvert x - y \rvert$. Let $g = \lvert \nabla f(y) \rvert > 0$, and let $K$ bound the operator norm of the Hessian of $f$ on the ball of radius $\delta$ about $y$. If $K \delta \le g/2$, then
$$ \left| \frac{\lvert f(x) \rvert}{\lvert \nabla f(x) \rvert} - \delta \right| \le \frac{3 K}{g}\, \delta^2 . $$

*Proof.* Since $\nabla f(y) \ne 0$, $Z$ is a smooth hypersurface near $y$, and $y$ minimizes $\lvert x - z \rvert^2$ over $z \in Z$. By a Lagrange multiplier, $x - y = \mu \nabla f(y)$ for some $\mu$, so $\nabla f(y) \cdot (x - y) = \pm g \delta$. By Taylor's theorem with the remainder bounded by $K$, $f(x) = f(y) + \nabla f(y) \cdot (x - y) + R$ with $f(y) = 0$ and $\lvert R \rvert \le K \delta^2 / 2$, so $\bigl| \lvert f(x) \rvert - g \delta \bigr| \le K \delta^2 / 2$. Also $\lvert \nabla f(x) - \nabla f(y) \rvert \le K \delta$, so $\bigl| \lvert \nabla f(x) \rvert - g \bigr| \le K \delta$, and $\lvert \nabla f(x) \rvert \ge g - K\delta \ge g/2$. Then
$$ \bigl| \lvert f(x) \rvert - \delta \lvert \nabla f(x) \rvert \bigr| \le \bigl| \lvert f(x) \rvert - g \delta \bigr| + \delta \bigl| g - \lvert \nabla f(x) \rvert \bigr| \le \tfrac{3}{2} K \delta^2 , $$
and division by $\lvert \nabla f(x) \rvert \ge g/2$ gives the claim. $\square$

So $\lvert f \rvert / \lvert \nabla f \rvert$ is the geometric distance up to an error of order $\delta^2$, and $\sum_i f(x_i)^2 / \lvert \nabla f(x_i) \rvert^2$ (the Sampson cost) is the sum of squared distances up to terms of order $\delta^3$. Taubin's cost replaces the sum of the ratios by the ratio of the sums. That step is an approximation and is not proved to be close here; when $\lvert \nabla f \rvert$ is the same at all data points the two agree up to the factor $m$.

**Lemma 2 (the cost as a quotient).** For every $a$ with $a^{\mathsf T} N a > 0$,
$$ q(a) = \frac{\sum_i f_a(x_i)^2}{\sum_i \lvert \nabla f_a(x_i) \rvert^2} = \frac{a^{\mathsf T} M a}{a^{\mathsf T} N a} . $$

*Proof.* $f_a(x_i) = \varphi(x_i)^{\mathsf T} a$, so $f_a(x_i)^2 = a^{\mathsf T} \varphi(x_i) \varphi(x_i)^{\mathsf T} a$. $\nabla f_a(x_i) = J(x_i)^{\mathsf T} a$, so $\lvert \nabla f_a(x_i) \rvert^2 = a^{\mathsf T} J(x_i) J(x_i)^{\mathsf T} a$. Sum over $i$. $\square$

**Lemma 3 (eliminating the constant).** Let $\varphi_n = \kappa \ne 0$ be constant and the others not, write $a = (b, c)$ with $c = a_n$, and let $M' = M_{bb} - M_{bc} M_{cb} / M_{cc}$ as in line L6. Then $M_{cc} = m \kappa^2 > 0$, $a^{\mathsf T} N a = b^{\mathsf T} N_{bb} b$, and for fixed $b$ the numerator $a^{\mathsf T} M a$ is smallest at $c = -M_{cb} b / M_{cc}$, where it equals $b^{\mathsf T} M' b \ge 0$. So $\min_a q(a) = \min_{b \ne 0} b^{\mathsf T} M' b / b^{\mathsf T} N_{bb} b$, and a minimizer $b$ of the right side gives the minimizer $(b, -M_{cb} b / M_{cc})$ of the left side.

*Proof.* $\nabla \varphi_n = 0$, so row and column $n$ of $N$ are zero, which gives the formula for $a^{\mathsf T} N a$; also $a^{\mathsf T} N a > 0$ forces $b \ne 0$. Next, $a^{\mathsf T} M a = b^{\mathsf T} M_{bb} b + 2 c\, M_{cb} b + c^2 M_{cc}$ is a quadratic in $c$ with positive leading coefficient; its minimum is at the stated $c$, with value $b^{\mathsf T} M_{bb} b - (M_{cb} b)^2 / M_{cc} = b^{\mathsf T} M' b$, which is at least $0$ because it is a value of $a^{\mathsf T} M a = \lVert D a \rVert^2$. The denominator does not depend on $c$, so minimizing $q$ over $c$ first and then over $b$ gives the claim. Without a constant basis function, take $M' = M$ and skip this step. $\square$

**Lemma 4 (the eigen step).** Let $N_{bb} = L L^{\mathsf T}$ with $L$ lower triangular and invertible (line L7, which fails exactly when $N_{bb}$ is not positive definite), and $C = L^{-1} M' L^{-\mathsf T}$. If $y$ is a unit eigenvector of the smallest eigenvalue $\lambda$ of $C$ and $b = L^{-\mathsf T} y$, then $b$ minimizes $b^{\mathsf T} M' b / b^{\mathsf T} N_{bb} b$, the minimum is $\lambda \ge 0$, and $M' b = \lambda N_{bb} b$.

*Proof.* The map $b \mapsto y = L^{\mathsf T} b$ is a bijection of the nonzero vectors, and $b^{\mathsf T} M' b / b^{\mathsf T} N_{bb} b = y^{\mathsf T} C y / y^{\mathsf T} y$. $C$ is symmetric, so by the spectral theorem this Rayleigh quotient has minimum $\lambda$, reached at $y$. $\lambda \ge 0$ because $M'$ is positive semidefinite by Lemma 3. Finally $M' b = L C L^{\mathsf T} b = L C y = \lambda L y = \lambda L L^{\mathsf T} b = \lambda N_{bb} b$. $\square$

**Theorem 1 (correctness).** If $N_{bb}$ is positive definite, the algorithm returns a unit vector $a$ that minimizes $q$ over all $a$ with $a^{\mathsf T} N a > 0$, and $\lambda = q(a)$.

*Proof.* Lemmas 3 and 4 give the minimizer $(b, c)$; line L10 only scales it, and $q$ does not change under scaling. $\square$

**Theorem 2 (exact on noise-free data).** Suppose every $x_i$ lies on $f_{a^*} = 0$, where $a^*$ has a nonconstant part $b^* \ne 0$, that $N_{bb}$ is positive definite, and that the null space of $D$ is spanned by $a^*$. Then $\lambda = 0$ and the algorithm returns $\pm a^* / \lvert a^* \rvert$.

*Proof.* $D a^* = 0$, so $q(a^*) = 0$; $b^* \ne 0$ gives $a^{*\mathsf T} N a^* > 0$. Since $q \ge 0$, the minimum is $0$, so $\lambda = 0$ by Theorem 1. The returned $a$ has $q(a) = 0$, so $\lVert D a \rVert^2 = a^{\mathsf T} M a = 0$, and $a$ is in the null space of $D$, which is the span of $a^*$. It is a unit vector, so it is $\pm a^* / \lvert a^* \rvert$. $\square$

**Theorem 3 (invariance).** Let $T(x) = s R x + t$ with $s > 0$, $R$ orthogonal, and suppose that $f \mapsto f \circ T^{-1}$ maps the span of the basis onto itself (true for all polynomials of degree at most $k$, and for the circle and sphere family $A \lvert x \rvert^2 + B \cdot x + C$). If $f$ minimizes Taubin's cost for the points $x_i$, then $f \circ T^{-1}$ minimizes it for the points $T(x_i)$, and its zero set is the image under $T$ of the zero set of $f$.

*Proof.* Let $g = f \circ T^{-1}$. Then $g(T x_i) = f(x_i)$, and by the chain rule $\nabla g(T x) = s^{-1} R\, \nabla f(x)$, so $\lvert \nabla g(T x_i) \rvert = \lvert \nabla f(x_i) \rvert / s$. Hence the cost of $g$ on the moved points is $s^2$ times the cost of $f$ on the old points. The map $f \mapsto f \circ T^{-1}$ is a linear bijection of the family, so it maps minimizers to minimizers. Finally $g(z) = 0$ exactly when $f(T^{-1} z) = 0$. $\square$

$\blacksquare$
