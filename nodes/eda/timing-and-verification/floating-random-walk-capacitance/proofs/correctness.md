---
title: The floating random walk gives an unbiased estimate of each capacitance coefficient, with finite variance
proves: [correctness, termination, complexity]
status: full
---

We prove the claims for the two-dimensional version of the page, with squares. The three-dimensional version with cubes is the same proof with a cube in place of the square.

**Setting.** The free space $\Omega$ is the open region inside the grounded box minus the closed conductor rectangles $D_1, \ldots, D_M$. The box is conductor $D_0$. The permittivity $\varepsilon$ is constant. For a conductor $j$, let $\phi_j$ be the potential that is harmonic in $\Omega$, continuous on $\overline{\Omega}$, equal to 1 on $D_j$ and 0 on every other conductor. The *capacitance coefficient* $C_{ij}$ is the charge on conductor $i$ when the potentials are $\phi_j$. Let $\Gamma$ be a closed curve in $\Omega$ that surrounds $D_i$ and no other conductor, with outward unit normal $n$ and length $L$. Gauss's law gives

$$C_{ij} = -\varepsilon \oint_\Gamma \nabla \phi_j \cdot n \, ds. \qquad (1)$$

In the code $\Gamma$ is the boundary of $D_i$ grown by the gap $g$, and $g$ is less than the distance from $D_i$ to every other conductor.

**Lemma 1 (the square kernel).** Let $Q$ be the closed square of half width $h$ centred at $p$, with $Q \subset \overline{\Omega}$. If $\phi$ is harmonic in $\Omega$ and continuous on $\overline{\Omega}$, then

$$\phi(p) = \oint_{\partial Q} K(q) \, \phi(q) \, dq, \qquad \nabla \phi(p) = \oint_{\partial Q} \nabla_p K(p, q) \, \phi(q) \, dq,$$

where $K(q) = K(p, q)$ is the Poisson kernel of $Q$ at its centre. After scaling $Q$ to $[0, \pi]^2$, the kernel on the bottom side at abscissa $u$ is

$$K(u) = \frac{1}{\pi} \sum_{n \text{ odd}} (-1)^{(n-1)/2} \frac{\sin n u}{\cosh(n \pi / 2)},$$

the same on the other sides by symmetry, and its derivatives with respect to the centre, toward the side and along it, are the series of the functions `normal_derivative` and `tangent_derivative`.

*Proof.* The interior of $Q$ is in $\Omega$, because $h$ is at most the distance from $p$ to every conductor in the $L^\infty$ norm. So $\phi$ is harmonic inside $Q$ and continuous on $Q$, and it is the Poisson integral of its boundary values. Separation of variables on $[0, \pi]^2$ gives the kernel of the bottom side at $(x, y)$ as $\frac{2}{\pi} \sum_{n \ge 1} \sin(n u) \sin(n x) \sinh(n(\pi - y)) / \sinh(n \pi)$. At $x = y = \pi/2$ the factor $\sin(n \pi / 2)$ is 0 for even $n$ and $(-1)^{(n-1)/2}$ for odd $n$, and $\sinh(n \pi / 2) / \sinh(n \pi) = 1 / (2 \cosh(n \pi / 2))$, which gives the formula. Differentiating the series term by term in $x$ and in $y$ at the centre gives the two derivative series. The series converge geometrically, as $e^{-n \pi / 2}$, so term-by-term differentiation is valid at the centre. The gradient formula is the derivative of the Poisson integral under the integral sign, which is valid at an interior point. $\square$

The tests check the series against a direct sum of the kernel and against central differences, and check by quadrature that the kernel reproduces harmonic polynomials and their gradients.

**Lemma 2 (each side has mass 1/4, and the weight is bounded).** $\int_0^\pi K(u) \, du = 1/4$, $K(u) > 0$ on $(0, \pi)$, and $|\nabla_p K / K| \le c / h$ on $\partial Q$ minus the corners for a constant $c$ that does not depend on $h$.

*Proof.* The kernel of a domain is positive on the smooth part of the boundary, and the four sides are symmetric, so each has mass $1/4$. Integration of the series term by term gives $\frac{4}{\pi} \sum_{n \text{ odd}} (-1)^{(n-1)/2} / (n \cosh(n \pi / 2)) = 1/4$, which the code checks. As functions of $q$, $K(p, q)$ and $\nabla_p K(p, q)$ are the normal derivatives of $G(p, q)$ and $\nabla_p G(p, q)$, where $G$ is the Green's function of $Q$. Near a corner both are harmonic in $q$ and zero on the two sides, and at a right angle such a function is $a r^2 \sin 2\theta + O(r^4)$ in polar coordinates at the corner. So both normal derivatives vanish to first order in $r$, with $a > 0$ for $G$ because $K > 0$ on the sides. So the quotient has a finite limit at each corner, and it is continuous on each side, hence bounded. The factor $1/h$ comes from the scaling. $\square$

**Lemma 3 (the walk stops, and its end value is unbiased).** Let $X_0 = q \in \Omega$ and let $X_{t+1}$ be drawn from $K$ on the largest empty square around $X_t$. Let $\tau$ be the first $t$ with $X_t$ within distance $\delta$ of a conductor, and let $k$ be that conductor. Then $\tau$ is finite with probability 1, and $|E[\phi(\text{the point of } D_k \text{ nearest } X_\tau)] - \phi(q)| \le \delta \cdot \max |\nabla \phi|$ over the $\delta$-layer, which tends to 0 with $\delta$.

*Proof.* By Lemma 1, $E[\phi(X_{t+1}) \mid X_t] = \phi(X_t)$, so $\phi(X_t)$ is a [martingale](/martingale/), bounded because $|\phi| \le 1$ by the maximum principle. Let $z$ be a conductor point at distance $h$ from $X_t$. It lies on $\partial Q$. The points of $\partial Q$ within distance $h/2$ of $z$ form one or two pieces of side of total length at least $h/2$, and each of them is within $h/2$ of the conductor. The kernel is positive and scales with $h$, so the next point falls there with probability at least a constant $\beta > 0$ that does not depend on $h$ or $t$. So the distance to the conductors halves with probability at least $\beta$ at every step. Let $R$ be the size of the box and $s = \lceil \log_2(R / \delta) \rceil$. From any point, $s$ halvings in a row reach the $\delta$-layer, so each block of $s$ steps stops the walk with probability at least $\beta^s$. Then $P(\tau > b s) \le (1 - \beta^s)^b$, so $\tau$ is finite with probability 1 and $E[\tau] \le s / \beta^s$. The [optional stopping theorem](/optional-stopping-theorem/) for a bounded martingale and an almost surely finite stopping time gives $E[\phi(X_\tau)] = \phi(q)$. Replacing $\phi(X_\tau)$ by its value at the nearest conductor point moves it by at most $\delta \max |\nabla \phi|$. $\square$

In the code the positions are integers and the walk stops when it stands on a conductor, so $\delta$ is one grid unit, $2^{-24}$ of a length unit in the tests, and the only other error is the rounding of each jump to the grid. The bound on the expected number of steps above is weak. The measured number is small, as the page shows.

**Theorem 4 (unbiased estimate of $C_{ij}$).** Let $Z = -\varepsilon L \, w \, [k = j]$, where $r$ is uniform on $\Gamma$, $Q$ is the largest empty square around $r$ with half width $h$, the first point $q$ is drawn from $K$ on $\partial Q$, $w = \nabla_r K(r, q) \cdot n / K(q)$, and $k$ is the conductor at the end of the walk from $q$. Then, in the limit $\delta \to 0$, $E[Z] = C_{ij}$, and $\operatorname{Var}(Z) < \infty$.

*Proof.* Condition on $r$ and $q$. By Lemma 3, $E[[k = j] \mid q] = \phi_j(q)$, since $\phi_j$ is the indicator of $j$ on the conductors. So

$$E[w \, [k = j] \mid r] = \oint_{\partial Q} K(q) \frac{\nabla_r K(r, q) \cdot n}{K(q)} \phi_j(q) \, dq = \nabla \phi_j(r) \cdot n$$

by Lemma 1, where the density of $q$ is $K$, with total mass 1 on the four sides by Lemma 2. Averaging over $r$, uniform on $\Gamma$ with density $1/L$, gives $E[Z] = -\varepsilon \oint_\Gamma \nabla \phi_j \cdot n \, ds = C_{ij}$ by (1). For the variance, $h$ is at least the distance from $\Gamma$ to the conductors, which is positive, so $|w| \le c / h$ is bounded by Lemma 2, $|Z|$ is bounded, and its variance is finite. $\square$

**Corollary 5 (the row sums to zero, and the error falls as $1/\sqrt{N}$).** The sum $\sum_j E[Z_j] = \sum_j C_{ij} = 0$, where $j$ runs over the box and all conductors, because $\sum_j \phi_j \equiv 1$ has zero gradient. The mean $\bar Z$ of $N$ independent samples has standard deviation $\sigma / \sqrt{N}$ with $\sigma^2 = \operatorname{Var}(Z)$. By the [Chebyshev inequality](/chebyshev-inequality/), $P(|\bar Z - C_{ij}| \ge a \sigma / \sqrt{N}) \le 1 / a^2$ for every $N$, and by the [central limit theorem](/central-limit-theorem/) the interval $\bar Z \pm 1.96 \, \hat\sigma / \sqrt{N}$, with the sample standard deviation $\hat\sigma$, holds $C_{ij}$ with probability that tends to 0.95. $\square$

**Complexity.** One step of a walk finds the nearest conductor, which costs $O(M)$ by a scan of the $M$ rectangles, and draws a side and a position, which costs $O(\log G)$ for a table of $G$ points. With $T$ the mean number of steps per walk, $N$ walks cost $O(N T (M + \log G))$ time and $O(M + G)$ space. With a spatial index the nearest conductor query is faster in practice. The expected number of steps $T$ is finite by Lemma 3, but this proof gives no useful bound on it in terms of the geometry. It is a measured quantity. For an error of $\eta$ with a fixed confidence, $N$ grows as $\sigma^2 / \eta^2$.
