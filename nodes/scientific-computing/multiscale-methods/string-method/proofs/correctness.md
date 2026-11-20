---
title: What the simplified string method computes
proves: [correctness]
status: full
---

We assume exact arithmetic and a potential $V$ with a Lipschitz continuous gradient. The string is $\varphi_0, \ldots, \varphi_N$; one iteration is the evolution step of line L3 and the reparametrization of lines L4 and L5.

**Lemma 1 (the reparametrization).** Let $P$ be the polygon through the points $\varphi_0^*, \ldots, \varphi_N^*$, with total length $L > 0$. Lines L4 and L5 return the points $\psi_i = P(iL/N)$, where $P(s)$ is the point at arc length $s$ along $P$. So $\psi_0 = \varphi_0^*$, $\psi_N = \varphi_N^*$, every $\psi_i$ lies on $P$, and the arc length along $P$ between $\psi_{i-1}$ and $\psi_i$ is $L/N$ for every $i$.

*Proof.* Line L4 computes the arc length $s_j$ of $P$ at its vertex $\varphi_j^*$ and $\alpha_j = s_j / L$, an increasing sequence from 0 to 1 (strictly increasing when consecutive points differ). For a target $\alpha = i/N$, line L5 finds $j$ with $\alpha_{j-1} \le \alpha \le \alpha_j$ and returns $(1 - w)\varphi_{j-1}^* + w \varphi_j^*$ with $w = (\alpha - \alpha_{j-1}) / (\alpha_j - \alpha_{j-1})$. On the segment from $\varphi_{j-1}^*$ to $\varphi_j^*$, arc length is linear in $w$, so this point has arc length $s_{j-1} + w (s_j - s_{j-1}) = \alpha L = iL/N$. $\square$

**Lemma 2 (the ends).** The ends never change in line L5, so $\varphi_0$ and $\varphi_N$ each follow steepest descent $\varphi \leftarrow \varphi - h \nabla V(\varphi)$ on their own. If an end starts in the basin of a nondegenerate minimum $m$ and $0 < h < 2/\lambda_{\max}$, where $\lambda_{\max}$ is the largest eigenvalue of the Hessian at $m$, it converges to $m$ when it starts close enough to $m$.

*Proof.* Near $m$, the map is $\varphi - m \mapsto (I - h \nabla^2 V(m))(\varphi - m) + o(|\varphi - m|)$, and the eigenvalues of $I - h \nabla^2 V(m)$ lie in $(-1, 1)$. $\square$

**The motion along the string does nothing.** If the evolution step moves every image along $P$ only, the polygon does not change as a set, and by Lemma 1 the reparametrization returns the same equally spaced points. So, to first order in $h$, only the part of $-h \nabla V$ perpendicular to the string changes the string. This is why the simplified method needs no projection of the force: the original string method of 2002 writes the motion as

$$\partial_t \varphi = -\nabla V(\varphi)^{\perp} + \lambda \hat\tau, \qquad \nabla V^{\perp} = \nabla V - (\nabla V \cdot \hat\tau)\hat\tau,$$

with the unit tangent $\hat\tau$ and a multiplier $\lambda$ that keeps the parametrization by normalized arc length. The simplified method replaces $-\nabla V^{\perp}$ by $-\nabla V$, because the difference is a tangential term that the reparametrization absorbs into $\lambda$. One iteration is a splitting step of this equation: an Euler step of $\partial_t \varphi = -\nabla V(\varphi)$, then the constraint.

**Theorem (the stationary curves).** Let $\varphi(\alpha)$, $\alpha \in [0, 1]$, be a smooth curve parametrized by normalized arc length with $|\varphi'| = L > 0$. It is a stationary solution of the equation above if and only if $\nabla V(\varphi(\alpha))^{\perp} = 0$ for all $\alpha$, that is, the gradient is parallel to the tangent at every point. This is the definition of a minimum energy path (MEP).

*Proof.* If $\partial_t \varphi = 0$, then $-\nabla V^{\perp} + \lambda \hat\tau = 0$. The first term is perpendicular to $\hat\tau$ and the second is parallel, so both are zero, and $\nabla V^{\perp} = 0$. Conversely, if $\nabla V^{\perp} = 0$, the choice $\lambda = 0$ gives $\partial_t \varphi = 0$, and the arc length constraint holds because the curve does not move. $\blacksquare$

On an MEP, $V$ along the curve has $\frac{d}{d\alpha} V(\varphi(\alpha)) = \nabla V \cdot \varphi' = \pm |\nabla V| L$, so $V$ changes monotonically between the stationary points on the curve; the highest point of an MEP between two minima is a stationary point of $V$, a saddle.

**The discrete string.** The converged string of the algorithm is a fixed point of the discrete map, not an exact MEP. Its error has two sources: the points lie on chords of the curve, and the evolution step moves points along the string, which the linear interpolation turns into a small shift towards the inside of a bend. On the test potential $4(r - 1)^2 + \sin^2\theta$, whose MEP is the unit circle, the largest distance from the circle is $0.0213$, $0.0095$ and $0.0036$ for $N = 8, 16, 32$ with $h = 0.02$: the error falls roughly like $1/N$. Interpolation with a cubic spline reduces it.

**What is not proved.** The theorem is about stationary curves. It does not show that the iteration converges, that it converges to the MEP closest to the start, or that the MEP has a single barrier. If an MEP passes through an intermediate minimum, the string passes through it as well.
