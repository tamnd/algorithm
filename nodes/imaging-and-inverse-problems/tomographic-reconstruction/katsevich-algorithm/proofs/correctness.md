---
title: Correctness of Katsevich's algorithm
proves: [correctness]
status: partial
---

We use the conventions of the page. The source is on the helix $y(s) = (R\cos s, R\sin s, hs)$ with $h = P/(2\pi)$. The vectors $e_u(s) = (-\sin s, \cos s, 0)$, $e_v = (0, 0, 1)$ and $e_w(s) = (\cos s, \sin s, 0)$ are orthonormal, and the flat detector point $(u, v)$ is $y(s) + u\,e_u + v\,e_v - D\,e_w$. The cone-beam data is $D_f(y, \theta) = \int_0^\infty f(y + t\theta)\,dt$ for a unit vector $\theta$, and $g(s, u, v) = D_f(y(s), \theta(s, u, v))$ with $\theta = (u e_u + v e_v - D e_w)/\sqrt{u^2 + v^2 + D^2}$. The object $f$ is smooth with support in the cylinder $x_1^2 + x_2^2 < r^2$, $r < R$.

**What is proved here and what is cited.** The main theorem, Katsevich's inversion formula, is cited from Katsevich (2002), and the flat-detector form that the code uses is the form of Noo, Pack and Heuscher (2003). This file proves the facts that connect the cited formula to the code: the PI-line exists, the kappa-line formula, the derivative at a fixed ray direction, the change from the angle form to the detector form with its constant, and the discretization. It also explains, without a full proof, why the formula is exact. The numbers on the page check the whole chain, including the constant $1/(2\pi)$ and the sign.

## Part 1. The PI-line

**Lemma 1 (existence).** For every $x$ with $x_1^2 + x_2^2 < R^2$ there are $s_b < s_t < s_b + 2\pi$ such that $x$ lies on the open segment from $y(s_b)$ to $y(s_t)$.

*Proof.* For $s_b \in \mathbb{R}$, the line in the plane through $(R\cos s_b, R\sin s_b)$ and $(x_1, x_2)$ meets the circle of radius $R$ at a second point, since $(x_1, x_2)$ is inside. Let $s_t(s_b)$ be its angle in $(s_b, s_b + 2\pi)$, and let $\lambda(s_b) \in (0, 1)$ be the position of $(x_1, x_2)$ on the chord. Both depend continuously on $s_b$. The point of the 3D segment from $y(s_b)$ to $y(s_t)$ over $(x_1, x_2)$ has the height $F(s_b) = h((1 - \lambda)s_b + \lambda s_t)$. It lies between $h s_b$ and $h s_t$. At $s_b = x_3/h$ we have $F > h s_b = x_3$. At $s_b = x_3/h - 2\pi$ we have $F < h s_t < h(s_b + 2\pi) = x_3$. By the intermediate value theorem $F(s_b) = x_3$ for some $s_b$ in between, and then $x$ is on the segment. $\square$

The PI-line is also unique for points inside the helix cylinder. This is a known result that Katsevich's paper relies on. We do not prove it here. The code finds $s_b$ by bisection on $F(s_b) - x_3$ in the range of the proof, and the test checks that $x$ lies on the computed segment. The interval $I_{PI}(x) = [s_b, s_t]$ is the PI-interval.

For a point on the axis, $(x_1, x_2) = 0$, every chord is a diameter, $s_t = s_b + \pi$ and $\lambda = \frac{1}{2}$, so $F = h(s_b + \pi/2)$ and $I_{PI}(x) = [x_3/h - \pi/2, x_3/h + \pi/2]$.

## Part 2. Projections and kappa-lines

**Lemma 2.** The ray from $y(s)$ through $x$ meets the detector at
$$u^* = \frac{D\,x\cdot e_u}{R - x\cdot e_w}, \qquad v^* = \frac{D\,(x_3 - hs)}{R - x\cdot e_w}.$$

*Proof.* $x - y(s) = (x\cdot e_u)e_u + (x_3 - hs)e_v - (R - x\cdot e_w)e_w$, because $y(s)\cdot e_u = 0$ and $y(s)\cdot e_w = R$. The detector point $(u, v)$ is $y + u e_u + v e_v - D e_w$. The two vectors are parallel when $u/D = x\cdot e_u/(R - x\cdot e_w)$ and $v/D = (x_3 - hs)/(R - x\cdot e_w)$. $\square$

**Lemma 3.** For $0 < |\psi| < \pi$, the line in the detector of view $s$
$$v = v_\kappa(u, \psi) = \frac{DP}{2\pi R}\left(\psi + \frac{\psi}{\tan\psi}\,\frac{u}{D}\right)$$
passes through the projections of $y(s + \psi)$ and $y(s + 2\psi)$.

*Proof.* Put $t \in \{\psi, 2\psi\}$. Here $y(s + t)\cdot e_u(s) = R\sin t$, $y(s + t)\cdot e_w(s) = R\cos t$ and the height difference is $ht$. Lemma 2 gives $u = D\sin t/(1 - \cos t) = D\cot(t/2)$ and $v = Dht/(R(1 - \cos t))$. For $t = \psi$: $\frac{\psi}{\tan\psi}\cot\frac{\psi}{2} = \frac{\cos\psi}{1 - \cos\psi}$, so $v_\kappa = \frac{DP}{2\pi R}\,\frac{\psi}{1 - \cos\psi}$, and $\frac{Dh\psi}{R(1 - \cos\psi)}$ is the same since $h = P/(2\pi)$. For $t = 2\psi$: $u = D\cot\psi$, so $v_\kappa = \frac{DP}{2\pi R}\,\psi(1 + \cot^2\psi) = \frac{DP}{2\pi R}\,\frac{\psi}{\sin^2\psi}$, and $\frac{2Dh\psi}{R(1 - \cos 2\psi)} = \frac{Dh\psi}{R\sin^2\psi}$ is the same. $\square$

So $v_\kappa(\cdot, \psi)$ is the projection of Katsevich's kappa-plane through $y(s)$, $y(s + \psi)$ and $y(s + 2\psi)$. The limit $\psi \to 0$ is the line $v = \frac{P}{2\pi R}u$. For $|u|$ in the range of the detector of the page, $v_\kappa$ increases with $\psi$, so bisection on $\psi \in (-\pi/2, \pi/2)$ finds the kappa-line through $(u^*, v^*)$. The test checks Lemma 3 and the inverse.

## Part 3. The derivative at a fixed direction

**Lemma 4.** For a fixed unit vector $\theta$,
$$\frac{\partial}{\partial q} D_f(y(q), \theta)\Big|_{q = s} = \left(\partial_s + \frac{u^2 + D^2}{D}\,\partial_u + \frac{uv}{D}\,\partial_v\right) g(s, u, v),$$
where $(u, v)$ is the detector point of $\theta$ at the view $s$.

*Proof.* Let $(u(q), v(q))$ be the detector point of the fixed $\theta$ at the view $q$. Then $D_f(y(q), \theta) = g(q, u(q), v(q))$, and the chain rule gives $\partial_s g + u'\,\partial_u g + v'\,\partial_v g$. The vector $W(q) = u e_u + v e_v - D e_w$ must stay parallel to $\theta$, so $W' = cW$ for some $c$. Since $e_u' = -e_w$ and $e_w' = e_u$, $W' = (u' - D)e_u + v' e_v - u\,e_w$. Comparing with $cW = cu\,e_u + cv\,e_v - cD\,e_w$ gives $c = u/D$, $u' = D + u^2/D$ and $v' = uv/D$. $\square$

Lines L1 and L2 compute this with central differences of step $\Delta s$, $\Delta u$ and $\Delta v$, which have the error $O(\Delta s^2 + \Delta u^2 + \Delta v^2)$ for smooth data. Line L3 multiplies by $D/\sqrt{u^2 + v^2 + D^2}$, which gives $g_2$. The test compares $g_2$ with the derivative computed along the source path for a fixed direction.

## Part 4. The formula

**Theorem (Katsevich 2002, cited).** For $f$ as above and $x$ in the cylinder of radius $r$,
$$f(x) = -\frac{1}{2\pi^2}\int_{I_{PI}(x)} \frac{1}{|x - y(s)|}\int_0^{2\pi} \frac{\partial}{\partial q} D_f\big(y(q), \cos\gamma\,\beta + \sin\gamma\,e\big)\Big|_{q = s}\,\frac{d\gamma}{\sin\gamma}\,ds,$$
where $\beta = (x - y(s))/|x - y(s)|$, $e$ is a unit vector orthogonal to $\beta$ in the kappa-plane of $x$ at $s$ (the plane through $y(s)$ whose detector line is the kappa-line through $(u^*, v^*)$), and the inner integral is a principal value. The orientation of $e$ and the sign go together, so we do not rely on the sign in this form. The code uses the detector form below, whose constant and sign the page confirms numerically.

**Proposition 1 (detector form).** The theorem is equivalent to
$$f(x) = \frac{1}{2\pi}\int_{I_{PI}(x)} \frac{1}{R - x\cdot e_w(s)}\,\mathrm{p.v.}\!\int \frac{1}{\pi(u^* - u)}\,g_2\big(s, u, v_\kappa(u, \psi^*)\big)\,du\,ds$$
up to the sign convention of $e$, where $\psi^*$ is the angle of the kappa-line through $(u^*, v^*)$.

*Proof of the change of variables.* Fix $s$. The directions $\cos\gamma\,\beta + \sin\gamma\,e$ for $\gamma \in (-\pi/2, \pi/2)$ point to the detector, and they meet it on the kappa-line. The directions of the other half have $\theta\cdot e_w(s) > 0$. For such a $\theta$ and for $q$ near $s$, $\theta\cdot e_w(q) > 0$, so every point $y(q) + t\theta$ with $t > 0$ has $(y(q) + t\theta)\cdot e_w(q) > R$ and lies outside the cylinder of radius $r$. So $D_f(y(q), \theta) = 0$ for $q$ near $s$, and its derivative in $q$ vanishes. Let $\ell$ be the arc length on the kappa-line and $p$ the distance from $y(s)$ to that line in the kappa-plane. A direction with the angle $\phi$ from the foot of the perpendicular hits the point $\ell = p\tan\phi$, and $\beta$ hits $\ell^* = p\tan\phi^*$ with $\gamma = \phi - \phi^*$. Then $d\ell = p\,d\phi/\cos^2\phi$ and $\ell - \ell^* = p\sin(\phi - \phi^*)/(\cos\phi\cos\phi^*)$, so
$$\frac{d\gamma}{\sin\gamma} = \frac{\cos\phi}{\cos\phi^*}\,\frac{d\ell}{\ell - \ell^*}.$$
Here $\cos\phi = p/|P - y|$ for the detector point $P$, so $\cos\phi/\cos\phi^* = |P^* - y|/|P - y|$. The kappa-line has a constant slope in the $(u, v)$ plane, so $d\ell/(\ell - \ell^*) = du/(u - u^*)$. The point $x$ lies on the ray to $P^*$ at the depth $R - x\cdot e_w$ along $-e_w$, and $P^*$ at the depth $D$, so $|P^* - y|/|x - y| = D/(R - x\cdot e_w)$. Finally $|P - y| = \sqrt{u^2 + v^2 + D^2}$. Putting these together, with Lemma 4 for the derivative,
$$\frac{1}{|x - y|}\int \frac{\partial_q D_f}{\sin\gamma}\,d\gamma = \frac{1}{R - x\cdot e_w}\,\mathrm{p.v.}\!\int \frac{D}{\sqrt{u^2 + v^2 + D^2}}\,\frac{g_1(s, u, v_\kappa(u))}{u - u^*}\,du = \frac{-\pi}{R - x\cdot e_w}\,\mathrm{p.v.}\!\int \frac{g_2}{\pi(u^* - u)}\,du.$$
Multiplying by $-1/(2\pi^2)$ gives the factor $\frac{1}{2\pi}$ of the proposition. $\square$

The detector form does not depend on $D$. If $D$ changes to $cD$, then $u$, $v$ and $u^*$ scale by $c$, $g_2$ does not change at corresponding points, and $du/(u^* - u)$ does not change. The prototype for this page checked this with $D = R$ and $D = 2R$ and got the same values.

**Why the formula is exact (sketch, not a full proof).** The 3D Radon inversion formula writes $f(x)$ as an integral over all planes through $x$ of the second derivative of the plane integrals of $f$ (see [Grangeat's formula](/grangeat-formula/)). Grangeat's identity gives the first derivative from the cone-beam data of one source point in the plane, and the derivative along the helix at a fixed direction gives the second. Every plane through $x$ meets the PI-segment of the helix, $y(I_{PI}(x))$, in one or three points. If one assigns to each meeting point a weight so that the weights of each plane add to 1, the inversion formula becomes an integral over $s \in I_{PI}(x)$. Katsevich chose the weights so that they jump only where the plane contains a kappa-line, and then the integral over the planes through $x$ and $y(s)$ becomes a single Hilbert transform along one line in the detector. The proof that the weights add to 1 for almost every plane is the main geometric step of Katsevich's paper. We do not reproduce it.

## Part 5. The discrete algorithm

Line L4 finds $I_{PI}(x)$ (Part 1). For each view $s_k$ with $s_k \in [s_b - \Delta s, s_t + \Delta s]$, line L5 computes $(u^*, v^*)$ and the depth $R - x\cdot e_w$ (Lemma 2). Line L6 reads $g_2$ along the kappa-line through $(u^*, v^*)$ at the detector columns $u_j$, by linear interpolation in $v$. Line L7 applies the discrete Hilbert kernel $\frac{2}{\pi n}$ for odd $n$ and 0 for even $n$, which is $\Delta u$ times the band-limited kernel $\frac{1 - \cos(\pi(u^* - u)/\Delta u)}{\pi(u^* - u)}$ at the sample points, at the two columns next to $u^*$. Line L8 interpolates linearly to $u^*$ and divides by the depth. Line L9 integrates the piecewise linear interpolant of these values over $[s_b, s_t]$ exactly and multiplies by $\frac{1}{2\pi}$. Each step has an error that goes to 0 with the steps for smooth data, so the output converges to the right side of Proposition 1. The page measures the error on a Gaussian blob: it is 0.031 at the peak with 41 columns and 0.011 with 81 columns.

**Locality in $v$ (exact).** For a point $x$, line L6 reads $g_2$ only at the heights $v_\kappa(u_j, \psi)$ with $|\psi| < \pi/2$, and with the detector columns $|u_j| \le u_{\max}$ these heights satisfy $|v_\kappa| \le \frac{DP}{2\pi R}(\pi/2 + u_{\max}/D)$, because $|\psi/\tan\psi| \le 1$. Linear interpolation uses the two rows next to that height, and the central difference in $v$ uses one more row on each side. So the output does not depend on the data in rows more than $2\Delta v$ away from this band. The test changes these rows at random and gets the same output. This is the reason why a helical detector needs only a few rows: the data outside the band around the kappa-lines, which lie near the Tam-Danielsson window, is never read.
