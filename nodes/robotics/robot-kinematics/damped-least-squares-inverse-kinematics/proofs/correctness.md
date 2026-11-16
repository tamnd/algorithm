---
title: The damped least squares step is the bounded minimizer of the damped objective, and the iteration converges linearly near a regular solution
proves: [correctness]
status: full
---

We use the notation of the page, in exact arithmetic, with $\lambda > 0$.
$J$ is an $m \times n$ real matrix, $e \in \mathbb R^m$, and norms are Euclidean norms or the matching operator norms.

**Claim 1.** $JJ^{\mathsf T} + \lambda^2I$ and $J^{\mathsf T}J + \lambda^2I$ are symmetric positive definite, and
$$J^{\mathsf T}(JJ^{\mathsf T} + \lambda^2I)^{-1} = (J^{\mathsf T}J + \lambda^2I)^{-1}J^{\mathsf T}.$$

*Proof.*
For every $y \ne 0$, $y^{\mathsf T}(JJ^{\mathsf T} + \lambda^2I)y = |J^{\mathsf T}y|^2 + \lambda^2|y|^2 > 0$, and the same holds for the other matrix.
The identity $(J^{\mathsf T}J + \lambda^2I)J^{\mathsf T} = J^{\mathsf T}(JJ^{\mathsf T} + \lambda^2I)$ holds by expanding both sides.
Multiply it on the left by $(J^{\mathsf T}J + \lambda^2I)^{-1}$ and on the right by $(JJ^{\mathsf T} + \lambda^2I)^{-1}$.
$\square$

So line L6 always has exactly one solution, and the two forms of the step on the page are equal.

**Claim 2.** The step $\Delta\theta = (J^{\mathsf T}J + \lambda^2I)^{-1}J^{\mathsf T}e$ is the unique minimizer of $\phi(x) = |Jx - e|^2 + \lambda^2|x|^2$.

*Proof.*
$\phi(x) = x^{\mathsf T}(J^{\mathsf T}J + \lambda^2I)x - 2e^{\mathsf T}Jx + |e|^2$ is a quadratic function with a positive definite Hessian $2(J^{\mathsf T}J + \lambda^2I)$, so it is strictly convex.
Its gradient $2(J^{\mathsf T}J + \lambda^2I)x - 2J^{\mathsf T}e$ is zero exactly at $\Delta\theta$.
$\square$

**Claim 3.** Let $J = \sum_{i=1}^r \sigma_iu_iv_i^{\mathsf T}$ be a singular value decomposition with $\sigma_i > 0$, orthonormal $u_i$ and orthonormal $v_i$.
Then $\Delta\theta = \sum_i \frac{\sigma_i}{\sigma_i^2 + \lambda^2}(u_i^{\mathsf T}e)v_i$ and $|\Delta\theta| \le |e|/(2\lambda)$.

*Proof.*
Complete the $v_i$ to an orthonormal basis of $\mathbb R^n$.
In this basis $J^{\mathsf T}J + \lambda^2I$ is diagonal, with $\sigma_i^2 + \lambda^2$ on $v_i$ and $\lambda^2$ on the other basis vectors.
Since $J^{\mathsf T}e = \sum_i \sigma_i(u_i^{\mathsf T}e)v_i$, applying the inverse gives the formula.
By the inequality of the arithmetic and geometric means, $\sigma^2 + \lambda^2 \ge 2\sigma\lambda$, so each factor is at most $1/(2\lambda)$, with equality at $\sigma = \lambda$.
Then $|\Delta\theta|^2 = \sum_i \bigl(\frac{\sigma_i}{\sigma_i^2 + \lambda^2}\bigr)^2(u_i^{\mathsf T}e)^2 \le \frac{1}{4\lambda^2}\sum_i(u_i^{\mathsf T}e)^2 \le \frac{|e|^2}{4\lambda^2}$.
$\square$

The bound does not depend on $J$, so it holds at singular configurations too.
It is reached when $J$ has a singular value equal to $\lambda$ and $e$ is along the matching $u_i$.

**Claim 4.** As $\lambda \to 0$, $\Delta\theta \to J^{+}e = \sum_i \frac{1}{\sigma_i}(u_i^{\mathsf T}e)v_i$, for every $J$.

*Proof.*
There are finitely many terms, and each factor $\sigma_i/(\sigma_i^2 + \lambda^2)$ tends to $1/\sigma_i$ since $\sigma_i > 0$.
$\square$

**Claim 5.** $e - J\Delta\theta = \lambda^2(JJ^{\mathsf T} + \lambda^2I)^{-1}e$.
In particular the residual is zero only when $e = 0$.

*Proof.*
With $y = (JJ^{\mathsf T} + \lambda^2I)^{-1}e$, $J\Delta\theta = JJ^{\mathsf T}y = (JJ^{\mathsf T} + \lambda^2I)y - \lambda^2y = e - \lambda^2y$.
$\square$

**Claim 6.** If $J$ has full row rank, then $\Delta\theta = 0$ only if $e = 0$.

*Proof.*
$\Delta\theta = J^{\mathsf T}y$, and $J^{\mathsf T}$ is injective when $J$ has full row rank, so $\Delta\theta = 0$ gives $y = 0$ and $e = (JJ^{\mathsf T} + \lambda^2I)y = 0$.
$\square$

So a fixed point of the iteration at a configuration with full row rank is a solution.
At a singular configuration, a fixed point with $e \ne 0$ can exist, such as the stretched arm with a target out of reach on the page, where $e$ is orthogonal to the range of $J$.

## Local convergence

**Claim 7.** Let $m = n$, let $f$ be twice continuously differentiable, and let $\theta^*$ be a solution, $f(\theta^*) = x_d$, with $J(\theta^*)$ invertible and least singular value $\sigma_{\min}$.
Let $\rho = \lambda^2/(\sigma_{\min}^2 + \lambda^2) < 1$.
For every $\rho' \in (\rho, 1)$ there is $r > 0$ such that every start with $|\theta^0 - \theta^*| \le r$ gives iterates with $|\theta^{k+1} - \theta^*| \le \rho'|\theta^k - \theta^*|$, so the iteration converges to $\theta^*$.

*Proof.*
The iteration is $\theta^{k+1} = \Phi(\theta^k)$ with $\Phi(\theta) = \theta + J(\theta)^{\mathsf T}(J(\theta)J(\theta)^{\mathsf T} + \lambda^2I)^{-1}(x_d - f(\theta))$.
$\Phi$ is continuously differentiable, since the inverse exists everywhere by Claim 1, and $\Phi(\theta^*) = \theta^*$.
At $\theta^*$ the term with $x_d - f$ vanishes, so only the derivative of $x_d - f$, which is $-J$, contributes:
$$D\Phi(\theta^*) = I - (J^{\mathsf T}J + \lambda^2I)^{-1}J^{\mathsf T}J = \lambda^2(J^{\mathsf T}J + \lambda^2I)^{-1},$$
with $J = J(\theta^*)$, using Claim 1.
This matrix is symmetric with the eigenvalues $\lambda^2/(\sigma_i^2 + \lambda^2)$, all in $(0, 1)$, and the largest is $\rho$.
So $|D\Phi(\theta^*)| = \rho$.
By continuity of $D\Phi$, there is $r > 0$ with $|D\Phi(\theta)| \le \rho'$ on the ball of radius $r$ around $\theta^*$.
On this convex ball, the mean value inequality gives $|\Phi(\theta) - \theta^*| = |\Phi(\theta) - \Phi(\theta^*)| \le \rho'|\theta - \theta^*|$, so each iterate stays in the ball and the distance falls by at least the factor $\rho'$.
$\square$

For the 2R arm of the page at $(0, \pi/2)$, $J^{\mathsf T}J = [[2, 1], [1, 1]]$ has the eigenvalues $(3 \pm \sqrt 5)/2$, so $\rho = 0.0255$ for $\lambda = 0.1$ and $\rho = 0.396$ for $\lambda = 0.5$.
For a generic start the error along the eigenvector of $\rho$ dominates, and the measured ratios of the errors approach $\rho$, as the tests check.

For $m < n$ the solutions form a manifold, and $D\Phi$ has the eigenvalue 1 along its tangent space, so the claim does not apply as stated, and we do not prove a result for that case here.
The result is local, and nothing is claimed for far starts or for targets out of reach.
