---
title: Unbiasedness of light tracing
proves: [correctness]
status: full
---

**Setting.** Surfaces have the area measure $A$. For points $x, y$ write $G(x, y) = V(x, y) \cos\theta_x \cos\theta_y / |x - y|^2$, where the cosines are taken with the normals at $x$ and $y$ toward the other point and are set to $0$ when negative. A direction $\omega$ at $x$ with the solid angle density $p(\omega)$ hits the point $y = h(x, \omega)$; the induced area density of $y$ is $p(\omega)\, \cos\theta_y / |x - y|^2$ (the change of variables $d\omega = \cos\theta_y\, dA(y) / |x - y|^2$), on the set of points visible from $x$.

The path integral form of the pixel value of a pinhole camera at $c$ is

$$I_j = \sum_{m \ge 0} \int_{A^{m+1}} F_m(x_0, \dots, x_m)\, dA(x_0) \cdots dA(x_m),$$

$$F_m = L_e(x_0 \to x_1) \Big[\prod_{i=1}^{m} G(x_{i-1}, x_i)\, f(x_{i-1} \to x_i \to x_{i+1})\Big] C_j(x_m),$$

with $x_{m+1} = c$ in the last BSDF factor, $L_e(x_0 \to x_1)$ read as $L_e(x_0 \to c)$ when $m = 0$, and the camera factor $C_j(x) = V(x, c)\, W_j(x \to c) \cos\theta_x / |x - c|^2$. This is the Neumann series of the rendering equation written with $d\omega = \cos\theta\, dA / |x - y|^2$ at each step: the term $m$ holds the light that leaves the emitter $x_0$ and reaches the camera after $m$ reflections.

**Claim.** Assume that $p_A(x_0) > 0$ wherever $L_e(x_0, \cdot) \ne 0$, that each direction density $p$ is positive wherever the factor it samples ($L_e \cos\theta$ at line L4, $f \cos\theta$ at line L7) is positive, and that $q > 0$ wherever a later vertex can still contribute. Let $S_j$ be the sum of the values that one run of the loop of lines L2 to L9 adds to pixel $j$. Then $E[S_j] = I_j$, and the value $I_j$ of line L10 is the mean of $N$ independent copies, so it is unbiased.

**The density of a path.** Let $x_0 = y$ be the light point of line L2 and $x_1, x_2, \dots$ the hits of line L5. Let $\omega_0$ be the direction of line L4 and $\omega_i$ the direction of line L7 at $x_i$. The probability that the path reaches $x_m$, together with the density of its vertices, is

$$P_m(x_0, \dots, x_m) = p_A(x_0) \cdot p_0(\omega_0) \frac{\cos\theta_{x_1}}{|x_1 - x_0|^2} \cdot \prod_{i=1}^{m-1} q_i\, p_i(\omega_i) \frac{\cos\theta_{x_{i+1}}}{|x_{i+1} - x_i|^2},$$

on the set of paths where each $x_{i+1}$ is visible from $x_i$, which is where $V(x_i, x_{i+1}) = 1$.

**The weight.** By lines L2, L4, L7 and L8, the weight at line L6 of vertex $x_m$, for $m \ge 1$, is

$$\beta_m = \frac{1}{p_A(x_0)} \cdot \frac{L_e(x_0 \to x_1) \cos\theta_{x_0}}{p_0(\omega_0)} \cdot \prod_{i=1}^{m-1} \frac{f(x_{i-1} \to x_i \to x_{i+1}) \cos\theta_{x_i}}{p_i(\omega_i)\, q_i},$$

where $\cos\theta_{x_i}$ in the factor of step $i$ is the cosine of the outgoing direction $\omega_i$ at $x_i$. Line L6 adds $\beta_m\, f(x_{m-1} \to x_m \to c)\, C_j(x_m)$. Multiply and divide by $P_m$: the cosines at the hit points of $P_m$ and the outgoing cosines of $\beta_m$ pair up as $\cos\theta_{x_i} \cos\theta_{x_{i+1}} / |x_{i+1} - x_i|^2 = G(x_i, x_{i+1})$ on the visible set, and the survival probabilities cancel. So the value added at vertex $x_m$ is exactly $F_m(x_0, \dots, x_m) / P_m(x_0, \dots, x_m)$, on the event that the path reaches $x_m$.

For $m = 0$, line L3 adds $L_e(x_0 \to c)\, C_j(x_0) / p_A(x_0) = F_0(x_0) / P_0(x_0)$.

**The mean.** The value added at vertex $m$ has the expected value

$$\int_{\{P_m > 0\}} \frac{F_m}{P_m}\, P_m\, dA(x_0) \cdots dA(x_m) = \int_{A^{m+1}} F_m\, dA(x_0) \cdots dA(x_m),$$

because the assumptions on the densities make $P_m > 0$ wherever $F_m > 0$: each factor of $F_m$ that is positive forces the matching factor of $P_m$ to be positive, and $V = 1$ on the support of $F_m$. All values are not negative, so by monotone convergence $E[S_j] = \sum_{m \ge 0} \int F_m = I_j$. $\square$

**The camera vertex.** The point $c$ never appears as a sampled vertex: a pinhole has area $0$, so no random ray hits it, and the integrand would be a point mass there. The deterministic connection replaces the integral over the camera vertex by its value. This is what makes the factor $C_j(x_m)$ appear in the estimator, and why every vertex needs a shadow ray.

**The weights of the implementation.** For a Lambertian emitter of radiance $E$ sampled with $p_A = E / \Phi$, $1 / p_A$ times $E$ is $\Phi$. With cosine sampling of $\omega_0$, $L_e \cos\theta / p_0 = E \pi$, and with $f = \rho / \pi$ and cosine sampling at $x_i$, each factor of the product is $\rho_i / q_i$. So $\beta_m f(x_{m-1} \to x_m \to c) = \Phi\, \rho_1 \cdots \rho_m / (q_1 \cdots q_{m-1})$, the form that the code uses.
