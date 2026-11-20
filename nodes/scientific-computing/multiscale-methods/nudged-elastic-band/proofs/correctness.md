---
title: The fixed points of the nudged elastic band
proves: [correctness]
status: full
---

We assume exact arithmetic and a potential $V$ that is continuously differentiable. The band is $R_0, \ldots, R_N$ with fixed ends, $g_i = \nabla V(R_i)$, $\tau_i$ is a unit vector (the tangent of line L4), $d_i = |R_i - R_{i-1}|$ for $i = 1, \ldots, N$, and $k > 0$. A converged band is one where every force of lines L6 and L7 is zero. The claim is about such a band. It is not a claim that the iteration converges.

**Lemma 1 (the climbing force is a reflection).** Let $P = I - 2 \tau \tau^{\mathsf T}$ for a unit vector $\tau$. Then the force of line L7 is $F_c = -P g_c$, and $|F_c| = |g_c|$.

*Proof.* $-g_c + 2 (g_c \cdot \tau_c) \tau_c = -(I - 2\tau_c\tau_c^{\mathsf T}) g_c$. The matrix $P$ is symmetric and $P^2 = I - 4\tau\tau^{\mathsf T} + 4 \tau (\tau^{\mathsf T}\tau) \tau^{\mathsf T} = I$, so $P$ is orthogonal and keeps lengths. $\square$

So the stop test of line L8 also bounds the gradient at the climbing image: $|g_c| < \mathrm{tol}$.

**Theorem (the fixed points).** Assume that all forces of lines L6 and L7 are zero, with the climbing image $c$ (if any).

1. For every image $i \ne c$, the gradient $g_i$ is parallel to $\tau_i$: the perpendicular part of the true force is zero.
2. For every image $i \ne c$, $d_{i+1} = d_i$. So the images are equally spaced on each side of the climbing image: $d_1 = \cdots = d_c$ and $d_{c+1} = \cdots = d_N$. Without a climbing image, all $N$ distances are equal.
3. The climbing image is a stationary point of $V$: $g_c = 0$.

*Proof.* Write $g = (g \cdot \tau)\tau + g^{\perp}$ with $g^{\perp} \cdot \tau = 0$. For $i \ne c$, line L6 gives

$$F_i = -g_i + (g_i \cdot \tau_i) \tau_i + k (d_{i+1} - d_i) \tau_i = -g_i^{\perp} + k (d_{i+1} - d_i) \tau_i.$$

The two terms are orthogonal, so $F_i = 0$ holds if and only if $g_i^{\perp} = 0$ and $k(d_{i+1} - d_i) = 0$. Since $k > 0$, this gives parts 1 and 2. For the climbing image, Lemma 1 gives $|g_c| = |F_c| = 0$, which is part 3. $\blacksquare$

**Why the projections are needed.** Without the projections, the force $-g_i + k(R_{i+1} - 2R_i + R_{i-1})$ of a plain elastic band has two faults that the theorem shows NEB does not have. The parallel part of $-g_i$ is not balanced by anything but the springs, so the images slide down from the barrier towards the minima and the region of the saddle has few images. The perpendicular part of the spring force is not zero where the path bends, so a converged plain band cuts the corner of a curved path and has $g_i^{\perp} \ne 0$. In NEB, the true force acts only across the path and the spring force acts only along it, so the two effects separate: part 1 holds whatever $k$ is, and $k$ affects only the spacing.

**The link to the minimum energy path.** A minimum energy path (MEP) is a curve $\varphi$ from one minimum to another on which $(\nabla V)^{\perp} = 0$: at every point, the gradient is parallel to the tangent. Part 1 is the discrete form of this condition at the images. If the images lie on a smooth curve and $\tau_i$ approximates its tangent, a converged band is a discrete approximation of an MEP, and part 3 places one image exactly at a stationary point on it. The tangent of Henkelman and Jonsson is chosen so that $\tau_i$ points to the neighbour with the higher energy, with a smooth switch at the extremes of the energy along the band. It approximates the tangent of the curve to first order in the spacing.

**What is not proved.** The NEB force is not the gradient of any function, because the projections depend on the band, so there is no energy that the iteration decreases, and the convergence of line L9 is not proved in general. Near a converged band, the iteration is a linear fixed point iteration, and it converges if $h$ is small enough compared with the largest curvature of $V$ and with $4k$. The theorem does not say that the stationary point of part 3 is a first-order saddle, that it is the lowest saddle between the two minima, or that the band finds the MEP of lowest barrier. In practice the climbing image is the highest point of a converged band and is a first-order saddle, and the band finds the MEP closest to its start.
