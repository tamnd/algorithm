---
title: The KLT selection is a greedy maximal spaced set, each tracking step is the inverse compositional Gauss-Newton step for a translation, an exact translation is a superlinearly attracting fixed point, and the pyramid sums the level results
proves: [correctness]
status: full
---

We use the notation of the page: the window of a point $q$ is the set of points $q + (i, j)$ with integers $|i|, |j| \le r$, the gradient matrix is $G(q) = \sum_x \nabla I(x) \nabla I(x)^{\mathsf T}$ over the window, and $\lambda(q)$ is its smaller eigenvalue.

## 1. The selection

**Claim 1.** Let $C$ be the list of line L10, sorted by decreasing $\lambda$, and let $P$ be the output of line L11. Then (a) every $p \in P$ has $\lambda(p) \ge q \max \lambda$; (b) any two points of $P$ are at least $\delta$ apart; (c) every $c \in C \setminus P$ has a point $p \in P$ with $|c - p| < \delta$ and $\lambda(p) \ge \lambda(c)$.

*Proof.* (a) $P \subseteq C$, and line L10 puts in $C$ only pixels that pass the threshold. (b) A point is added only when its distance to every point already in $P$ is at least $\delta$, and points are never removed; so for two points of $P$, the later one was tested against the earlier one. (c) Let $c \in C$ be rejected. When the loop reached $c$, the test failed, so some $p$ already in $P$ had $|c - p| < \delta$. That $p$ came earlier in $C$, so $\lambda(p) \ge \lambda(c)$ by the order of $C$, and $p$ stays in $P$ until the end. $\square$

Property (c) says that $P$ is a maximal set of spaced points: no rejected candidate can be added without breaking (b). It does not say that $P$ is the largest such set; that problem is a maximum independent set problem in a disk graph, and the greedy order by strength is a design choice.

## 2. The step at one level

Fix a level, drop the index $\ell$, and fix the guess $g$ and the current correction $\nu$. Write $J_\nu(x) = J(x + g + \nu)$ and $e(x) = I(x) - J_\nu(x)$. Consider the inverse compositional problem for a translation: find $\eta$ that minimizes

$$
\psi(\eta) = \sum_{x} \big( I(x - \eta) - J_\nu(x) \big)^2 ,
$$

which asks which shift of the first window matches the current sample of $J$. If $\eta$ solves it, then $I(x - \eta) \approx J(x + g + \nu)$, that is $I(y) \approx J(y + g + \nu + \eta)$ with $y = x - \eta$, so the new correction is $\nu + \eta$, as in line L20.

**Claim 2.** The Gauss-Newton step for $\psi$ from $\eta = 0$ is $\eta = G^{-1} b$ with $b = \sum_x \nabla I(x)\, e(x)$, which is line L19 and line L20. It is unique when $G$ is nonsingular, and $G$ does not depend on $\nu$.

*Proof.* The first-order expansion $I(x - \eta) = I(x) - \nabla I(x)^{\mathsf T} \eta + o(|\eta|)$ turns $\psi$ into the linear least-squares function

$$
\phi(\eta) = \sum_x \big( e(x) - \nabla I(x)^{\mathsf T} \eta \big)^2 = \eta^{\mathsf T} G \eta - 2 b^{\mathsf T} \eta + \sum_x e(x)^2 .
$$

For any $\eta$ and $h$, $\phi(\eta + h) - \phi(\eta) = 2 h^{\mathsf T}(G \eta - b) + h^{\mathsf T} G h$. $G$ is a sum of matrices $a a^{\mathsf T}$, so $h^{\mathsf T} G h = \sum_x (\nabla I(x)^{\mathsf T} h)^2 \ge 0$. If $G \eta = b$, the difference is $\ge 0$ for every $h$, so $\eta$ is a minimizer. If $G$ is nonsingular it is positive definite (its smaller eigenvalue is positive by line L16), so $h^{\mathsf T} G h > 0$ for $h \ne 0$ and the minimizer is unique. Conversely, at a minimizer the gradient $2(G\eta - b)$ is zero. The gradient $\nabla I$ is taken on the fixed window of $I$, so $G$ depends only on $I$, $q$ and $r$: line L15 computes it once per level. $\square$

## 3. Fixed point and local convergence

Here we use a smooth image model: $I$ and $J$ are continuously differentiable functions on the plane (for example the continuous image before sampling, or an interpolation with continuous derivatives). Define the map of one iteration

$$
\Phi(\nu) = \nu + G^{-1} \sum_x \nabla I(x) \big( I(x) - J(x + g + \nu) \big).
$$

**Claim 3.** Suppose that $J(y + g + \nu^*) = I(y)$ for all $y$ in an open set that contains the window, and that $G$ is nonsingular. Then $\nu^*$ is a fixed point of $\Phi$, the Jacobian of $\Phi$ at $\nu^*$ is zero, and there is a $\rho > 0$ such that for every start with $|\nu_0 - \nu^*| \le \rho$ the iterates $\nu_{j+1} = \Phi(\nu_j)$ converge to $\nu^*$ with $|\nu_{j+1} - \nu^*| / |\nu_j - \nu^*| \to 0$.

*Proof.* At $\nu^*$ every term $I(x) - J(x + g + \nu^*)$ is zero, so $\Phi(\nu^*) = \nu^*$. The Jacobian is

$$
D\Phi(\nu) = \mathrm{Id} - G^{-1} \sum_x \nabla I(x)\, \nabla J(x + g + \nu)^{\mathsf T} .
$$

The identity $J(y + g + \nu^*) = I(y)$ holds on an open set, so its derivatives agree there: $\nabla J(x + g + \nu^*) = \nabla I(x)$ for each window point $x$. Then the sum is $G$ and $D\Phi(\nu^*) = \mathrm{Id} - G^{-1} G = 0$. $D\Phi$ is continuous because $\nabla J$ is, so for each $c \in (0, 1)$ there is a $\rho_c > 0$ with $\|D\Phi(\nu)\| \le c$ on the closed ball $B$ of radius $\rho_c$ around $\nu^*$. Take $\rho = \rho_{1/2}$. For $\nu \in B$, the mean value inequality on the segment from $\nu^*$ to $\nu$ (which lies in the convex set $B$) gives $|\Phi(\nu) - \nu^*| = |\Phi(\nu) - \Phi(\nu^*)| \le \frac{1}{2} |\nu - \nu^*|$. So $\Phi$ maps $B$ into $B$, and by induction $|\nu_j - \nu^*| \le 2^{-j} |\nu_0 - \nu^*| \to 0$. For the rate, fix $c \in (0, 1/2]$. Once $\nu_j$ is in the ball of radius $\rho_c$, which happens for all large $j$, the same inequality gives $|\nu_{j+1} - \nu^*| \le c |\nu_j - \nu^*|$. As $c$ is arbitrary, the ratio tends to 0. $\square$

The claim needs the identity on an open set, not only on the window points: the step uses the gradients. Bilinear interpolation has kinks on the grid lines, so on sampled images the claim holds only approximately; this is why the subpixel example on the page ends at about 0.01 to 0.05 pixel and not at zero. The claim says nothing about starts far from $\nu^*$. The size of $\rho$ depends on the image, which is the reason for the pyramid.

## 4. The pyramid

**Claim 4.** Let $\nu_\ell$ be the correction that level $\ell$ returns in lines L17 to L21. Then PYR-LK returns $d = \sum_{\ell = 0}^{L} 2^\ell \nu_\ell$.

*Proof.* Let $g_\ell$ be the guess on entry to level $\ell$, so $g_L = 0$ and, by line L22, $g_{\ell - 1} = 2(g_\ell + \nu_\ell)$ for $\ell \ge 1$. We show by induction on $j = L - \ell$ that $g_\ell = \sum_{i = \ell + 1}^{L} 2^{i - \ell} \nu_i$. For $\ell = L$ the sum is empty and $g_L = 0$. If it holds for $\ell$, then $g_{\ell - 1} = 2 \nu_\ell + \sum_{i = \ell + 1}^{L} 2^{i - \ell + 1} \nu_i = \sum_{i = \ell}^{L} 2^{i - (\ell - 1)} \nu_i$. At level 0, line L22 returns $g_0 + \nu_0 = \sum_{i = 1}^{L} 2^i \nu_i + \nu_0$. $\square$

**Claim 5.** In the continuous model, let level $\ell$ of an image $E$ be $E_\ell(x) = (k_\ell * E)(2^\ell x)$ for a blur kernel $k_\ell$. If $J(y + d) = I(y)$ for all $y$, then $J_\ell(x + d / 2^\ell) = I_\ell(x)$ for all $x$.

*Proof.* Convolution commutes with translation: $(k_\ell * J)(z + d) = \int k_\ell(w) J(z + d - w)\, dw = \int k_\ell(w) I(z - w)\, dw = (k_\ell * I)(z)$. Put $z = 2^\ell x$: $J_\ell(x + d / 2^\ell) = (k_\ell * J)(2^\ell x + d) = (k_\ell * I)(2^\ell x) = I_\ell(x)$. $\square$

So, with Claim 3 at each level, if the guess from level $\ell + 1$ is within the attraction radius of level $\ell$, the level converges to the right correction, and by Claim 4 the corrections add up to $d$. The sampled pyramid of the page (binomial blur, then every second pixel) satisfies Claim 5 exactly only for shifts by multiples of $2^\ell$; for other shifts it holds up to the sampling error of the blur.

## 5. What is not proved

The backward check of lines L5 and L6 is a heuristic. A wrong track can return to its start (the page shows a point that is 0.395 pixel wrong with a backward error of 0.11), and a right track can fail the check when the backward solve starts outside its attraction radius. The tracker has no global convergence result: for a start outside the radius $\rho$ of Claim 3, the iteration can converge to another fixed point.
