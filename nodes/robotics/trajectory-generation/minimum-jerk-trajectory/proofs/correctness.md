---
title: The quintic is the unique minimizer of the integral of squared jerk
proves: [correctness]
status: full
---

We use the notation of the page. Fix $T > 0$ and the six end values $x(0) = p_0$, $x'(0) = v_0$, $x''(0) = c_0$, $x(T) = p_1$, $x'(T) = v_1$, $x''(T) = c_1$ of one coordinate. Let $\mathcal X$ be the set of functions on $[0, T]$ with these end values whose third derivative is square integrable. The cost is

$$J(x) = \int_0^T x'''(t)^2\, dt.$$

Line L6 returns the coefficients of the quintic $x^*$ with these six end values. The page of the [quintic polynomial trajectory](/quintic-polynomial-trajectory/) proves that this quintic exists, is unique, and that the closed form of line L6 gives it.

## The quintic is the unique minimizer

**Theorem 1.** For every $x \in \mathcal X$, $J(x) = J(x^*) + J(x - x^*)$. So $J(x) \ge J(x^*)$, with equality only for $x = x^*$.

*Proof.* Let $\eta = x - x^*$. Then $\eta$, $\eta'$ and $\eta''$ vanish at $0$ and at $T$, and

$$J(x) = J(x^*) + 2\int_0^T x^{*\prime\prime\prime} \eta'''\, dt + J(\eta).$$

Integrate the middle integral by parts three times:

$$\int_0^T x^{*(3)} \eta^{(3)} = \big[x^{*(3)} \eta''\big]_0^T - \big[x^{*(4)} \eta'\big]_0^T + \big[x^{*(5)} \eta\big]_0^T - \int_0^T x^{*(6)} \eta\, dt.$$

The three brackets are zero because $\eta''$, $\eta'$ and $\eta$ vanish at both ends. The last integral is zero because $x^*$ has degree 5, so $x^{*(6)} = 0$. This proves the identity. If $J(\eta) = 0$, then $\eta''' = 0$ almost everywhere, so $\eta$ is a polynomial of degree at most 2. Then $\eta(0) = \eta'(0) = \eta''(0) = 0$ forces its three coefficients to be zero, so $\eta = 0$. $\square$

This is the Euler-Lagrange equation $x^{(6)} = 0$ of the cost, solved with its natural boundary data; the identity also shows that the stationary point is a minimum, with no extra argument.

## Several coordinates

The cost of a motion in $\mathbb R^d$ is the sum of the costs of the coordinates, and the end conditions do not couple them. So the minimizer is the quintic minimizer in each coordinate, and the theorem applies to each. For a rest-to-rest move all coordinates follow the same profile $s(\tau)$, scaled by their displacements, so the path is the straight segment from $x_0$ to $x_f$. This is lines L1 to L5.

## The rest-to-rest profile and its cost

With zero end velocities and accelerations, line L6 gives $s(\tau) = 10\tau^3 - 15\tau^4 + 6\tau^5$ with $\tau = t/T$, as on the quintic page. Its derivatives in $t$ are lines L3 and L4:

$$\dot x = \frac{D}{T}\, 30\tau^2(1 - \tau)^2, \qquad \ddot x = \frac{D}{T^2}\, 60\tau(1 - \tau)(1 - 2\tau),$$

for a displacement $D$. The jerk is $\frac{D}{T^3} 60(6\tau^2 - 6\tau + 1)$. The polynomial $6\tau^2 - 6\tau + 1$ is the shifted Legendre polynomial $P_2(2\tau - 1)$, whose square has the integral $1/5$ over $[0, 1]$. So

$$J(x^*) = \int_0^T \Big(\frac{60D}{T^3}\Big)^2 P_2(2t/T - 1)^2\, dt = \frac{3600 D^2}{T^6} \cdot \frac{T}{5} = \frac{720 D^2}{T^5}.$$
