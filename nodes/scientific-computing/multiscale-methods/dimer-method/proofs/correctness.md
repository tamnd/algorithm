---
title: The rotation and the translation of the dimer method
proves: [correctness]
status: full
---

We assume exact arithmetic and a potential $V$ that is three times continuously differentiable. $F = -\nabla V$ is the force, $H(R) = \nabla^2 V(R)$ the Hessian, the dimer has the centre $R$, the unit vector $N$ and the half length $\Delta R$, and $F_1 = F(R + \Delta R N)$, $F_2 = F(R - \Delta R N)$. The implementation computes $F_2$ as $2F(R) - F_1$, which is the same up to $O(\Delta R^2)$ and is exact when $V$ is quadratic.

**Lemma 1 (the curvature).** $C = (F_2 - F_1) \cdot N / (2\Delta R) = N^{\mathsf T} H(R) N + O(\Delta R^2)$, and $(F_1 - F_2) / (2\Delta R) = -H(R) N + O(\Delta R^2)$. Both are exact for a quadratic $V$.

*Proof.* By Taylor's theorem, $\nabla V(R \pm \Delta R N) = \nabla V(R) \pm \Delta R\, H N + \frac12 \Delta R^2 D^3V[N, N] + O(\Delta R^3)$. The difference of the two cancels the even terms: $F_1 - F_2 = -2\Delta R\, H N + O(\Delta R^3)$. Divide by $2\Delta R$ and take the dot product with $N$. For a quadratic $V$ the gradient is affine, so there are no remainder terms. $\square$

So with $\Delta R$ small the dimer measures $H N$ with two gradients and never forms $H$.

**Lemma 2 (the rotation is exact for a quadratic).** Let $V$ be quadratic with Hessian $H$, let $\Theta$ be the unit vector of the part of $F_1 - F_2$ that is perpendicular to $N$ (line L5), and let $N(\varphi) = \cos\varphi\, N + \sin\varphi\, \Theta$. Then the curvature along $N(\varphi)$ is

$$C(\varphi) = \tfrac12 a_0 + a_1 \cos 2\varphi + b_1 \sin 2\varphi,$$

with $a_0 = N^{\mathsf T} H N + \Theta^{\mathsf T} H \Theta$, $a_1 = \frac12 (N^{\mathsf T} H N - \Theta^{\mathsf T} H \Theta)$ and $b_1 = \Theta^{\mathsf T} H N$. The three numbers are fixed by $C(0)$, $C'(0) = 2 b_1$ and one value $C(\varphi_1)$ with $\cos 2\varphi_1 \ne 1$, and the angle of line L6 gives the minimum of $C$ over the plane of $N$ and $\Theta$, which is the smaller eigenvalue of $H$ restricted to this plane.

*Proof.* By Lemma 1, $C(\varphi) = N(\varphi)^{\mathsf T} H N(\varphi) = \cos^2\varphi\, N^{\mathsf T} H N + 2 \sin\varphi \cos\varphi\, \Theta^{\mathsf T} H N + \sin^2\varphi\, \Theta^{\mathsf T} H \Theta$, and the double angle formulas give the form above. Then $C(0) = \frac12 a_0 + a_1$ and $C'(0) = 2 b_1$. By Lemma 1, $\Theta^{\mathsf T} H N = -(F_1 - F_2) \cdot \Theta / (2\Delta R)$, which is the value of $b_1$ that the code uses. The value $C(\varphi_1)$ gives $a_1 (1 - \cos 2\varphi_1) = C(0) - C(\varphi_1) + b_1 \sin 2\varphi_1$, which is the formula of the code, and then $a_0 = 2(C(0) - a_1)$. Write $a_1 \cos 2\varphi + b_1 \sin 2\varphi = \rho \cos(2\varphi - 2\varphi^*)$ with $\rho = (a_1^2 + b_1^2)^{1/2}$ and $2\varphi^* = \operatorname{atan2}(b_1, a_1)$. The maximum of $C$ is at $\varphi^*$ and the minimum at $\varphi^* + \pi/2$, with the value $\frac12 a_0 - \rho$. The code computes $\varphi^*$, sees that $C(\varphi^*) > C(0)$ unless $\rho = 0$, and adds $\pi/2$. The minimum of a Rayleigh quotient over the unit vectors of a plane is the smaller eigenvalue of the restriction. $\square$

**Consequences for the rotation.** In two dimensions the plane is the whole space, so one rotation gives the lowest eigenvalue and its eigenvector exactly. In $n$ dimensions each rotation does not increase $C$, and the rotational force $F_1 - F_2$ minus its part along $N$ is zero exactly when $H N$ is parallel to $N$, so the fixed points of the rotation are the eigenvectors of $H$. The minimum of the Rayleigh quotient over all unit vectors is the smallest eigenvalue $\lambda_1$, and repeated rotations are a descent method for it. We do not prove that they converge to the eigenvector of $\lambda_1$ from every start; they do if $\lambda_1$ is simple and the start is not orthogonal to its eigenvector.

**Lemma 3 (the fixed points of the translation).** Let $P = I - 2NN^{\mathsf T}$. Where $C < 0$, the force of line L9 is $F^{\dagger} = P F$, and $F^{\dagger} = 0$ if and only if $F = 0$.

*Proof.* $F - 2(F \cdot N) N = P F$, and $P$ is orthogonal ($P^2 = I$, $P = P^{\mathsf T}$), so $|F^{\dagger}| = |F|$. $\square$

So the stop test $|\nabla V| < \mathrm{tol}$ of line L8 is a test on $|F^{\dagger}|$.

**Theorem (local convergence to a first-order saddle).** Let $R_s$ be a first-order saddle: $\nabla V(R_s) = 0$ and $H(R_s)$ has eigenvalues $\lambda_1 < 0 < \lambda_2 \le \cdots \le \lambda_n$. Assume that $N$ is the unit eigenvector of $\lambda_1$ at every step (exact rotation) and that $V$ is quadratic. Then the step $R \leftarrow R + h F^{\dagger}$ of line L10 converges to $R_s$ from every start with $C < 0$ if $0 < h < 2 / \max(|\lambda_1|, \lambda_n)$.

*Proof.* For a quadratic $V$, $F(R) = -H (R - R_s)$, so $R - R_s$ changes by the matrix $I - h P H$. With $N$ the eigenvector of $\lambda_1$, $P$ and $H$ have the same eigenvectors, and $P H$ has the eigenvalues $-\lambda_1 = |\lambda_1|, \lambda_2, \ldots, \lambda_n$, all positive. The matrix $I - h P H$ has the eigenvalues $1 - h|\lambda_1|, 1 - h\lambda_2, \ldots$, all in $(-1, 1)$ under the condition on $h$. So $R - R_s \to 0$ geometrically. $\blacksquare$

The inversion of the force along $N$ turns the saddle, which is not a minimum of $V$, into a minimum of the modified landscape seen by the translation: the step goes uphill along the lowest mode and downhill in all others. For a smooth $V$ that is not quadratic, the same argument holds near $R_s$ for the linearized step, so a first-order saddle is a locally attracting fixed point.

**What is not proved.** The theorem is local. Far from a saddle, where $C \ge 0$, the method moves along $N$ only, and nothing guarantees that it reaches a region with $C < 0$: on the Muller-Brown surface many searches from the minimum A run away to the region where $V$ grows without bound. The method does not say which saddle it finds, and a set of searches from one minimum gives a sample of nearby saddles, not a complete list.
