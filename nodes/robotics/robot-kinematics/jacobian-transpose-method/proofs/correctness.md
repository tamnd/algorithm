---
title: The Jacobian transpose step is a descent step, the iteration reaches a stationary point for a small fixed gain, and it converges linearly near a regular solution
proves: [correctness]
status: full
---

We use the notation of the page, in exact arithmetic.
The task is a position task $f : \mathbb R^n \to \mathbb R^m$, twice continuously differentiable, with $e(\theta) = x_d - f(\theta)$, $J = Df$ and $E(\theta) = \tfrac12|e(\theta)|^2$.

**Claim 1 (gradient).** $\nabla E(\theta) = -J(\theta)^{\mathsf T}e(\theta)$.

*Proof.*
$DE(\theta)h = e^{\mathsf T}De(\theta)h = -e^{\mathsf T}Jh$ for every $h$, so the gradient is $-J^{\mathsf T}e$.
$\square$

**Claim 2 (descent).** If $g = J^{\mathsf T}e \ne 0$, there is $\bar\alpha > 0$ with $E(\theta + \alpha g) < E(\theta)$ for all $0 < \alpha \le \bar\alpha$.

*Proof.*
$\frac{d}{d\alpha}E(\theta + \alpha g)$ at $\alpha = 0$ is $\nabla E^{\mathsf T}g = -|g|^2 < 0$, and the derivative is continuous.
$\square$

**Claim 3 (the gain of Buss and Kim).** Let $g = J^{\mathsf T}e \ne 0$.
Then $Jg \ne 0$, the gain $\alpha_B = \langle e, Jg\rangle/|Jg|^2$ is positive, and it is the unique minimizer of $r(\alpha) = |e - \alpha Jg|^2$.

*Proof.*
$\langle e, Jg\rangle = \langle J^{\mathsf T}e, g\rangle = |g|^2 > 0$, so $Jg \ne 0$ and $\alpha_B > 0$.
$r$ is a quadratic in $\alpha$ with the positive leading coefficient $|Jg|^2$, and $r'(\alpha) = -2\langle e, Jg\rangle + 2\alpha|Jg|^2$ is zero exactly at $\alpha_B$.
$\square$

So the gain of L7 is defined whenever the step is not zero, and the code returns the zero step when $Jg = 0$, which by the same identity means $g = 0$.

## A global result for a fixed gain

**Claim 4.** Suppose $\nabla E$ is Lipschitz with constant $\Lambda$ on $\mathbb R^n$, and let $0 < \alpha < 2/\Lambda$.
Then the iterates $\theta^{k+1} = \theta^k + \alpha J^{\mathsf T}e$ satisfy $E(\theta^{k+1}) \le E(\theta^k) - \alpha(1 - \alpha\Lambda/2)|\nabla E(\theta^k)|^2$.
So $E(\theta^k)$ never increases, $\sum_k|\nabla E(\theta^k)|^2 < \infty$, $J^{\mathsf T}e \to 0$, and every limit point of the iterates is a stationary point of $E$.

*Proof.*
With $d = -\alpha\nabla E(\theta^k)$, the standard bound for a function with a Lipschitz gradient gives $E(\theta^k + d) \le E(\theta^k) + \nabla E(\theta^k)^{\mathsf T}d + \tfrac{\Lambda}{2}|d|^2$.
By Claim 1 the step is $d$, and substituting gives the inequality.
Since $1 - \alpha\Lambda/2 > 0$, $E$ decreases at each step, and summing over $k$ gives $\alpha(1 - \alpha\Lambda/2)\sum_k|\nabla E(\theta^k)|^2 \le E(\theta^0)$.
So $\nabla E(\theta^k) \to 0$, and by continuity $\nabla E = 0$ at every limit point.
$\square$

**The hypothesis holds for revolute arms.** If all joints are revolute, $f$ is $2\pi$-periodic in each $\theta_i$.
Then the Hessian of $E$ is continuous and periodic, so it is bounded on $\mathbb R^n$ by its maximum over one period box, and $\nabla E$ is Lipschitz with that bound as $\Lambda$.

**What the result does not give.** A stationary point need not be a solution.
For the 2R arm with the target $(2.5, 0)$, the stretched pose $\theta = (0, 0)$ has $J = [[0, 0], [2, 1]]$ and $e = (0.5, 0)$, so $J^{\mathsf T}e = 0$ with $|e| = 0.5$.

## Local rate

**Claim 5.** Let $m = n$, let $\theta^*$ be a solution with $J(\theta^*)$ invertible and singular values $\sigma_i$, and let $0 < \alpha < 2/\sigma_{\max}^2$.
Let $\rho = \max_i|1 - \alpha\sigma_i^2| < 1$.
For every $\rho' \in (\rho, 1)$ there is $r > 0$ such that every start with $|\theta^0 - \theta^*| \le r$ gives $|\theta^{k+1} - \theta^*| \le \rho'|\theta^k - \theta^*|$ for all $k$.

*Proof.*
The iteration is $\theta^{k+1} = \Phi(\theta^k)$ with $\Phi(\theta) = \theta + \alpha J(\theta)^{\mathsf T}(x_d - f(\theta))$, which is continuously differentiable, and $\Phi(\theta^*) = \theta^*$.
At $\theta^*$, the factor $x_d - f$ is zero, so $D\Phi(\theta^*) = I - \alpha J^{\mathsf T}J$ with $J = J(\theta^*)$.
This matrix is symmetric with the eigenvalues $1 - \alpha\sigma_i^2$, so its norm is $\rho$.
Since $\sigma_i > 0$ and $\alpha\sigma_i^2 < 2$, every eigenvalue is in $(-1, 1)$ and $\rho < 1$.
By continuity there is $r > 0$ with $|D\Phi(\theta)| \le \rho'$ on the closed ball of radius $r$ around $\theta^*$.
The mean value inequality on this convex ball gives $|\Phi(\theta) - \theta^*| \le \rho'|\theta - \theta^*|$, so every iterate stays in the ball and the distance falls by the factor $\rho'$.
$\square$

For the 2R arm at $(0, \pi/2)$, $J^{\mathsf T}J = [[2, 1], [1, 1]]$ has the eigenvalues $(3 \pm \sqrt 5)/2$.
The claim gives $\rho = 0.962$, $0.809$ and $0.745$ for $\alpha = 0.1$, $0.5$ and $2/3$, and the tests check that the measured error ratios approach these values.
The value $\alpha = 2/(\sigma_1^2 + \sigma_2^2)$ makes $\rho$ smallest, with $\rho = (\sigma_1^2 - \sigma_2^2)/(\sigma_1^2 + \sigma_2^2)$.
For $\alpha > 2/\sigma_{\max}^2$ the claim does not apply; the page shows by measurement that the iteration then fails on the 2R arm.
The gain of Buss and Kim changes from step to step, and we prove no rate for it.
