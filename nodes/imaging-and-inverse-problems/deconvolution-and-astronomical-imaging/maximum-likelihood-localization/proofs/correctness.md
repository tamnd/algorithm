---
title: The derivatives are exact, every step lowers the Poisson negative log likelihood, noise-free data give the true parameters, and the returned matrix is the Cramer-Rao bound
proves: [correctness]
status: full
---

**Setting.** Pixel $(v, u)$ covers $[u - \frac12, u + \frac12] \times [v - \frac12, v + \frac12]$. For $\theta = (x_0, y_0, N, b)$ the expected count is $\mu = N E_x(u) E_y(v) + b$ with

$$E_x(u) = \int_{u - 1/2}^{u + 1/2} g(\xi - x_0)\, d\xi = \tfrac12\Bigl[\operatorname{erf}\tfrac{u - x_0 + 1/2}{\sqrt2 s} - \operatorname{erf}\tfrac{u - x_0 - 1/2}{\sqrt2 s}\Bigr],$$

where $g(t) = e^{-t^2/(2s^2)}/(\sqrt{2\pi}s)$ is the normal density, and the same for $E_y$. The counts $c$ are independent Poisson with the means $\mu$. The negative log likelihood, without the constant $\sum \log c!$, is $L(\theta) = \sum (\mu - c\log\mu)$.

**Claim 1 (pixel derivatives).** With $t_1 = u - x_0 + \frac12$ and $t_2 = u - x_0 - \frac12$,

$$\frac{\partial E_x}{\partial x_0} = g(t_2) - g(t_1), \qquad \frac{\partial^2 E_x}{\partial x_0^2} = \frac{t_2}{s^2} g(t_2) - \frac{t_1}{s^2} g(t_1).$$

*Proof.* $E_x = G(t_1) - G(t_2)$ with $G$ the normal distribution function, $G' = g$, and $\partial t_i/\partial x_0 = -1$. So $\partial E_x/\partial x_0 = -g(t_1) + g(t_2)$. Then $g'(t) = -(t/s^2)g(t)$, so $\partial g(t_i)/\partial x_0 = (t_i/s^2)g(t_i)$. $\square$

**Claim 2 (gradient, Hessian, Fisher information).**

$$\nabla L = \sum \Bigl(1 - \frac c\mu\Bigr)\nabla\mu, \qquad \nabla^2 L = \sum \frac{c}{\mu^2}\nabla\mu\,\nabla\mu^T + \Bigl(1 - \frac c\mu\Bigr)\nabla^2\mu,$$

and the Fisher information is $I(\theta) = \mathbb E[\nabla^2 L] = \sum \nabla\mu\,\nabla\mu^T/\mu$. Here $\nabla\mu = (N E_x' E_y,\ N E_x E_y',\ E_x E_y,\ 1)$, and the nonzero entries of $\nabla^2\mu$ are $N E_x''E_y$, $N E_x E_y''$, $N E_x'E_y'$, $E_x'E_y$ and $E_xE_y'$ in the obvious places.

*Proof.* Differentiate $\mu - c\log\mu$ once and twice by the chain rule, and $\mu$ by the product rule with Claim 1. Taking the expectation with $\mathbb E[c] = \mu$ removes the second term of the Hessian. $\square$

The test compares the gradient and the Hessian with central differences, and checks that the Hessian at $c = \mu$ equals $I$.

**Claim 3 (descent).** Let $\mu > 0$ at all pixels. If $\nabla^2 L$ is positive definite, the Newton step $\delta = -(\nabla^2 L)^{-1}\nabla L$ satisfies $\nabla L^T\delta < 0$ unless $\nabla L = 0$. If not, and the four vectors $(\partial_i\mu)$ over the pixels are linearly independent, $I(\theta)$ is positive definite and the scoring step $\delta = -I^{-1}\nabla L$ has the same property. Then the backtracking of line L6 ends with a $t > 0$ for which $L(\theta + t\delta) \le L(\theta) + 10^{-4} t\,\nabla L^T\delta < L(\theta)$.

*Proof.* For a positive definite $A$, $\nabla L^T\delta = -\nabla L^T A^{-1}\nabla L < 0$ when $\nabla L \ne 0$. $z^T I z = \sum (z^T\nabla\mu)^2/\mu$ is $0$ only if $z^T\nabla\mu = 0$ at every pixel, which the linear independence excludes for $z \ne 0$. The set where $N > 0$, the center lies in the image and all $\mu > 0$ is open and contains $\theta$, and $L$ is differentiable there, so $L(\theta + t\delta) = L(\theta) + t\nabla L^T\delta + o(t)$; for small $t$ the point is in the set and the inequality holds because $10^{-4} < 1$. Halving $t$ reaches such a $t$. $\square$

So the sequence $L(\theta_k)$ never increases, which the test checks. The loop stops when a step is below the tolerance. With steps from matrices whose eigenvalues stay in a fixed positive range, the standard theory of line search methods gives $\nabla L(\theta_k) \to 0$; near a minimizer with a positive definite Hessian the full Newton step is accepted and the convergence is quadratic. These two facts are standard results and are not proved here. The limit on the move of the center (one pixel per step) only shortens steps, so it keeps the descent property.

**Claim 4 (noise-free data).** If $c = \mu(\theta^*)$, then $\theta^*$ is a global minimizer of $L$, and a strict local minimizer if $I(\theta^*)$ is positive definite.

*Proof.* With $\mu^* = \mu(\theta^*)$ and $r = \mu/\mu^*$ at each pixel, $L(\theta) - L(\theta^*) = \sum \mu^*(r - 1 - \log r) \ge 0$, since $r - 1 - \log r \ge 0$ for $r > 0$. At $\theta^*$ the gradient is $0$, since $1 - c/\mu = 0$ at every pixel, and the Hessian is $I(\theta^*)$ by Claim 2. A zero gradient and a positive definite Hessian give a strict local minimizer. $\square$

The test starts from the centroid guess and from three poor starts, and all four runs return $\theta^*$ to $10^{-6}$.

**Claim 5 (the bound).** For any unbiased estimator $\hat\theta$ of $\theta$ from the counts, $\operatorname{Cov}\hat\theta \succeq I(\theta)^{-1}$. The code returns $I(\hat\theta)^{-1}$.

*Proof.* This is the [Cramer-Rao bound](/cramer-rao-bound/) for the product of Poisson laws, whose Fisher information is the $I$ of Claim 2. $\square$

The maximum likelihood estimate reaches the bound only asymptotically, as the photon count grows and when the PSF model is correct; for small counts it can be biased and its variance can differ from the bound. The test measures the variance over $200$ Poisson images with about $500$ signal photons and finds it within $30$ percent of $I^{-1}$ (a measurement, not a theorem).

**Claim 6 (no pixels, no background).** If the pixels are infinitely small and $b = 0$, the information about $x_0$ is $N/s^2$, so the bound on the standard deviation is $s/\sqrt N$.

*Proof.* The photon positions then form a Poisson process with the intensity $N g(\xi - x_0)$ (times the same in $y$), and the information about $x_0$ is $N\int g'(t)^2/g(t)\,dt = N\,\mathbb E[(t/s^2)^2] = N/s^2$ for a normal $t$ with variance $s^2$. $\square$

With unit pixels of side $a$ the information is smaller. The test computes the bound for $s = a = 100$ nm, $N = 1000$ and a background of $10^{-6}$ on a $15 \times 15$ grid and finds $3.2914$ nm. This agrees to $10^{-3}$ nm with $\sqrt{(s^2 + a^2/12)/N}$, which is a numerical observation for this case, not an identity. $\blacksquare$
