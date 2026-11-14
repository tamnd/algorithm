---
title: The boundary integral equation on a circle, its degenerate scale, and the consistency of IGABEM collocation
proves: [correctness]
status: full
---

We use the notation of the page: $u^*(x, y) = -\frac{1}{2\pi} \ln |y - x|$, $q^* = \partial u^* / \partial n_y$, $(V q)(x) = \int_\Gamma u^*(x, y) q(y) \, ds_y$ and $(K u)(x) = \int_\Gamma q^*(x, y) u(y) \, ds_y$. The boundary integral equation is $\tfrac12 u + K u = V q$ on a smooth closed curve $\Gamma$. We take it as known from Green's second identity, as derived on the page.

**Lemma 1 (the double layer of a constant).** For a smooth closed curve $\Gamma$ and $x \in \Gamma$, $\int_\Gamma q^*(x, y) \, ds_y = -\tfrac12$.

*Proof.* The function $u = 1$ is harmonic with $q = 0$. The boundary integral equation gives $\tfrac12 \cdot 1 + \int_\Gamma q^*(x, y) \, ds_y = 0$. $\square$

**Lemma 2 (the circle).** Let $\Gamma$ be the circle of radius $R$ about the origin, with $x = R e^{i\theta}$ and $y = R e^{i\varphi}$. Then

1. $q^*(x, y) = -\dfrac{1}{4\pi R}$ for $y \ne x$, so $(K u)(x) = -\tfrac12 \bar u$, where $\bar u$ is the mean of $u$ over $\Gamma$;
2. $V 1 = -R \ln R$, and $V e^{ik\varphi} = \dfrac{R}{2|k|} e^{ik\theta}$ for each integer $k \ne 0$.

*Proof.* (1) The outward normal at $y$ is $n_y = y / R$, and $|x| = |y| = R$, so $(y - x) \cdot n_y = (R^2 - x \cdot y)/R$ and $|y - x|^2 = 2R^2 - 2 x \cdot y$. So $(y - x) \cdot n_y = |y - x|^2 / (2R)$, and $q^* = -\frac{1}{2\pi} \cdot \frac{1}{2R}$. With $ds_y = R \, d\varphi$, $(K u)(x) = -\frac{1}{4\pi R} \int_0^{2\pi} u \, R \, d\varphi = -\tfrac12 \bar u$.

(2) $|y - x| = R \, |1 - e^{i(\varphi - \theta)}|$, and for $\alpha \notin 2\pi\mathbb{Z}$ the Fourier series $\ln |1 - e^{i\alpha}| = -\sum_{m \ge 1} \frac{\cos m\alpha}{m}$ holds, as the real part of $\ln(1 - z) = -\sum_m z^m / m$ on $|z| = 1$, $z \ne 1$, with convergence in $L^2(0, 2\pi)$. So

$$ \ln |y - x| = \ln R - \sum_{m \ge 1} \frac{\cos m(\varphi - \theta)}{m}. $$

Multiply by $-\frac{1}{2\pi} e^{ik\varphi} R$ and integrate over $\varphi \in (0, 2\pi)$; the $L^2$ convergence allows term by term integration against the bounded function $e^{ik\varphi}$. For $k = 0$ only the constant term remains, and it gives $-\frac{1}{2\pi} \cdot 2\pi R \ln R = -R \ln R$. For $k \ne 0$ only the term $m = |k|$ remains, with $\int_0^{2\pi} \cos(|k|(\varphi - \theta)) e^{ik\varphi} \, d\varphi = \pi e^{ik\theta}$, which gives $\frac{1}{2\pi} \cdot \frac{R}{|k|} \cdot \pi e^{ik\theta} = \frac{R}{2|k|} e^{ik\theta}$. $\square$

**Theorem 1 (solvability on the circle and the degenerate scale).** On the circle of radius $R$, $V$ is injective on $L^2(\Gamma)$ if and only if $R \ne 1$. For $R \ne 1$ and the Dirichlet data $g$, the equation $V q = \tfrac12 g + K g$ has the unique solution with the Fourier coefficients $\hat q_0 = 0$ and $\hat q_k = \frac{|k|}{R} \hat g_k$ for $k \ne 0$, which is the exact flux $\partial u / \partial n$.

*Proof.* By Lemma 2, $V$ multiplies the Fourier coefficient of index $k$ by $\frac{R}{2|k|} > 0$ for $k \ne 0$ and by $-R \ln R$ for $k = 0$. A multiplier operator is injective if and only if no multiplier is zero, and $-R \ln R = 0$ exactly for $R = 1$. For the right side, Lemma 2 gives $\tfrac12 g + K g = \tfrac12 (g - \bar g)$, whose coefficients are $0$ for $k = 0$ and $\tfrac12 \hat g_k$ for $k \ne 0$. Dividing by the multipliers gives the stated $\hat q$. The harmonic function with boundary values $g$ is $u = \sum_k \hat g_k (r/R)^{|k|} e^{ik\theta}$, and $\partial u / \partial r$ at $r = R$ has the coefficients $\frac{|k|}{R} \hat g_k$, so the solution is the exact flux. $\square$

For $g = x^2 - y^2 = R^2 \cos 2\theta$ this gives $q = \frac{2}{R} R^2 \cos 2\theta = 2R \cos 2\theta$, the value used in the test. For $R = 1$, $V 1 = 0$, so the constant density is in the kernel and the Dirichlet problem cannot be solved through $V$ alone. This is the degenerate scale of the Pitfalls.

**Theorem 2 (consistency of the collocation).** Let $\Gamma$ be a smooth closed NURBS curve and let the collocation points $x_i$ be smooth points of $\Gamma$. Suppose the exact solution has $u|_\Gamma = \sum_j R_j \tilde u_j$ and $q = \sum_j R_j \tilde q_j$ in the merged basis. If the matrix $C = (R_j(\tau_i))$ of line L8 and the matrix $G$ of line L9 are non-singular, and the integrals of lines L3 to L7 are exact, then IGABEM-DIRICHLET returns $q = \tilde q$.

*Proof.* Line L8 solves $C u = (g(x_i))_i$. The vector $\tilde u$ satisfies it, because $g(x_i) = u(x_i) = \sum_j R_j(\tau_i) \tilde u_j$, and $C$ is non-singular, so $u = \tilde u$. With exact integrals, row $i$ of $H \tilde u$ is $\tfrac12 u(x_i) + (K u)(x_i)$ and row $i$ of $G \tilde q$ is $(V q)(x_i)$, by linearity of the integrals in the coefficients. The boundary integral equation holds at every smooth point of $\Gamma$, so $G \tilde q = H \tilde u = H u$. $G$ is non-singular, so line L9 returns $\tilde q$. $\square$

On the circle, $x = \sum_j R_j(t) X_j$ and $y = \sum_j R_j(t) Y_j$ for the control points $(X_j, Y_j)$, because a NURBS curve is the weighted sum of its control points. The function $u = a x + b y$ is harmonic, and its flux is $q = (a x + b y)/R$ by $n = (x, y)/R$. Both lie in the space, so Theorem 2 applies: the method returns the control values $(a X_j + b Y_j)/R$ of $q$. The test checks this with $a = 1$, $b = 2$, $R = 2$, where the only error left is that of the quadrature.

**Corollary (constant data).** For $g = 1$ on any smooth closed curve, $u = (1, \ldots, 1)$ by the partition of unity, and with exact integrals $(H u)_i = \tfrac12 + \int_\Gamma q^*(x_i, y) \, ds_y = 0$ by Lemma 1. So if $G$ is non-singular, $q = 0$. $\blacksquare$

**What is not proved here.** The non-singularity of the discrete $G$ for $R \ne 1$ and the rate of convergence when $q$ is not in the spline space are not proved. The page measures an order of about 3 for the largest flux error and about 4 at an interior point, for quadratic NURBS on the circle.
