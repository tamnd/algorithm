---
title: Mean value coordinates sum to 1 and reproduce linear functions, so the cage deformation is the identity at rest and reproduces affine maps
proves: [correctness]
status: full
---

We use the notation of the page.
The cage is a simple polygon $c_0, \dots, c_{n-1}$, and $p$ is a point inside it that is not on the boundary.
Let $r_i = |c_i - p|$, $e_i = (c_i - p)/r_i$, and let $\alpha_i \in (-\pi, \pi)$ be the signed angle at $p$ from $e_i$ to $e_{i+1}$, with indices modulo $n$.
The unnormalized weights are $\tilde w_i = (\tan(\alpha_{i-1}/2) + \tan(\alpha_i/2))/r_i$, and $W = \sum_i \tilde w_i$.

## The half-angle tangent

**Lemma 1.** With $\times$ the 2D cross product and $\cdot$ the dot product, $\tan(\alpha_i/2) = \dfrac{(c_i - p) \times (c_{i+1} - p)}{r_ir_{i+1} + (c_i - p) \cdot (c_{i+1} - p)}$, and the denominator is positive.

*Proof.*
The numerator is $r_ir_{i+1}\sin\alpha_i$ and the denominator is $r_ir_{i+1}(1 + \cos\alpha_i)$, which is positive because $\alpha_i \ne \pm\pi$, since $p$ is not on edge $i$. And $\sin\alpha/(1 + \cos\alpha) = \tan(\alpha/2)$. $\square$

This is the form the implementation uses. It stays accurate when $p$ is on the line of an edge but not on the edge, where $\alpha_i = 0$; the denominator is 0 only when $p$ is on the edge, where the implementation returns the linear weights along the edge.

## Linear precision

**Lemma 2.** For every angle $\alpha \in (-\pi, \pi)$ and the unit vector $u(\theta) = (\cos\theta, \sin\theta)$: $\int_\theta^{\theta + \alpha}u(t)\,dt = \tan(\alpha/2)\,(u(\theta) + u(\theta + \alpha))$.

*Proof.*
Rotate so that $\theta = 0$. The left side is $(\sin\alpha, 1 - \cos\alpha)$. The right side is $\tan(\alpha/2)(1 + \cos\alpha, \sin\alpha)$, and $\tan(\alpha/2) = \sin\alpha/(1 + \cos\alpha) = (1 - \cos\alpha)/\sin\alpha$, so the two agree (for $\alpha = 0$ both sides are 0). $\square$

**Theorem 1.** $\sum_i \tilde w_i(c_i - p) = 0$.

*Proof.*
Let $\theta_i$ be the angle of $e_i$, chosen continuously along the boundary, so that $\theta_{i+1} = \theta_i + \alpha_i$.
Because $p$ is inside the simple polygon, the boundary winds once around $p$, and $\sum_i\alpha_i = 2\pi$.
By Lemma 2, $\sum_i\tan(\alpha_i/2)(e_i + e_{i+1}) = \sum_i\int_{\theta_i}^{\theta_{i+1}}u(t)\,dt = \int_{\theta_0}^{\theta_0 + 2\pi}u(t)\,dt = 0$.
Collect the terms of each $e_i$: it appears with $\tan(\alpha_{i-1}/2)$ and with $\tan(\alpha_i/2)$. So $\sum_i(\tan(\alpha_{i-1}/2) + \tan(\alpha_i/2))e_i = \sum_i\tilde w_ir_ie_i = \sum_i\tilde w_i(c_i - p) = 0$. $\square$

**Theorem 2.** If $W \ne 0$, the coordinates $w_i = \tilde w_i/W$ satisfy $\sum_iw_i = 1$ and $\sum_iw_ic_i = p$.

*Proof.*
The first claim is the normalization. By Theorem 1, $\sum_iw_i(c_i - p) = 0$, so $\sum_iw_ic_i = p\sum_iw_i = p$. $\square$

If the cage is convex, or more generally if $p$ lies in the kernel of a star-shaped cage, every $\alpha_i$ is in $(0, \pi)$, so every $\tilde w_i > 0$, and $W > 0$: the coordinates are positive.
For an arbitrary simple polygon, Hormann and Floater (2006) show that $W > 0$ at every point that is not on the boundary; we quote this and do not prove it here.
The tests check the sum and the linear precision at random points of an L-shaped cage, and the positivity in a convex hexagon.

## The deformation

**Theorem 3.** With the coordinates of Theorem 2, line L3 returns $p$ for the rest cage $c' = c$, and $A(p)$ for the moved cage $c'_i = A(c_i)$ with an affine map $A(x) = Mx + t$.

*Proof.*
$\sum_iw_iA(c_i) = M\sum_iw_ic_i + t\sum_iw_i = Mp + t$. The rest cage is the case $M = I$, $t = 0$. $\square$

**Theorem 4.** The coordinates do not change when the cage and the point are moved together by a similarity $x \mapsto \lambda Qx + t$ with a rotation $Q$ and $\lambda > 0$.

*Proof.*
The signed angles $\alpha_i$ do not change, and every $r_i$ is multiplied by $\lambda$. So every $\tilde w_i$ is divided by $\lambda$, and the normalized $w_i$ do not change. $\square$

## The boundary cases

If $p = c_i$, the implementation returns the unit weight of vertex $i$, so $p' = c'_i$.
If $p$ is on edge $i$ at the fraction $s = r_i/(r_i + r_{i+1})$ from $c_i$, it returns the weights $1 - s$ and $s$, so $\sum_iw_ic_i = p$, and $p'$ is the point at the same fraction of the moved edge.
So points on the cage follow the cage boundary linearly.
That the coordinates of inside points tend to these boundary values is a known property of mean value coordinates; we quote it and do not prove it here.
