---
title: The identities behind INLA, and its exactness for a Gaussian likelihood
proves: [correctness]
status: full
---

**Setting.** A latent Gaussian model with hyperparameter $\theta$:

$$\theta \sim \pi(\theta), \qquad x \mid \theta \sim N(0, Q(\theta)^{-1}), \qquad y_j \mid x, \theta \sim p(y_j \mid x_j) \text{ independently}, \quad j = 1, \ldots, n.$$

$Q(\theta)$ is symmetric positive definite. Write $g_j(v) = \log p(y_j \mid x_j = v)$, and assume each $g_j$ is twice differentiable and concave. All densities are with respect to Lebesgue measure on $x \in \mathbb{R}^n$ (and on $\theta$). Write

$$F_\theta(x) = -\tfrac12 x^\top Q(\theta) x + \sum_j g_j(x_j),$$

so that $\pi(x, \theta, y) = \pi(\theta)\,(2\pi)^{-n/2}\det Q(\theta)^{1/2}\, e^{F_\theta(x)}$.

## Claim 1: the basic identity

For every $\theta$ and every $x$,

$$\pi(\theta \mid y) = \frac{\pi(x, \theta, y)}{\pi(x \mid \theta, y)\, \pi(y)}.$$

*Proof.* By the definition of conditional densities, $\pi(x, \theta, y) = \pi(x \mid \theta, y)\, \pi(\theta \mid y)\, \pi(y)$. Divide by $\pi(x \mid \theta, y)\pi(y)$, which is positive because $e^{F_\theta(x)} > 0$. $\square$

So the right-hand side does not depend on $x$. L4 replaces the unknown $\pi(x \mid \theta, y)$ by the Gaussian approximation $\pi_G(x \mid \theta, y) = N(x^*, P^{-1})$ and evaluates at $x = x^*$, where $\pi_G(x^* \mid \theta, y) = (2\pi)^{-n/2}\det P^{1/2}$. The factors $(2\pi)^{-n/2}$ cancel, which gives

$$\log\tilde\pi(\theta \mid y) = \log\pi(\theta) + \tfrac12\log\det Q(\theta) + F_\theta(x^*) - \tfrac12\log\det P + \text{const},$$

the formula of L4. It is the [Laplace approximation](/laplace-approximation/) of $\int e^{F_\theta(x)}\, dx$, times $\pi(\theta)\det Q(\theta)^{1/2}$.

## Claim 2: the inner step is Newton's method, and its fixed point is the mode

$F_\theta$ is strictly concave and has a unique maximizer $x^*$. With $c_j(v) = -g_j''(v) \ge 0$, $D(x) = \operatorname{diag}(c_j(x_j))$ and $b(x) = D(x)x + g'(x)$, where $g'(x) = (g_j'(x_j))_j$, the Newton step for $F_\theta$ from $x$ is the solution $x_+$ of

$$(Q + D(x))\, x_+ = b(x),$$

and $x$ is a fixed point of this map if and only if $x = x^*$.

*Proof.* The Hessian of $F_\theta$ is $-(Q + D(x))$, which is negative definite because $Q$ is positive definite and $D(x)$ is non-negative. So $F_\theta$ is strictly concave and has at most one maximizer. It has one: concavity gives $g_j(v) \le g_j(0) + g_j'(0)v$, so $F_\theta(x) \le C + a^\top x - \tfrac12\lambda_{\min}\|x\|^2 \to -\infty$ as $\|x\| \to \infty$, and a continuous function that tends to $-\infty$ attains its maximum. The gradient is $\nabla F_\theta(x) = -Qx + g'(x)$, and the Newton step is

$$x_+ = x + (Q + D)^{-1}(-Qx + g') = (Q + D)^{-1}\big((Q + D)x - Qx + g'\big) = (Q + D)^{-1}(Dx + g').$$

If $x_+ = x$, then $(Q + D)x = Dx + g'$, so $Qx = g'(x)$, so $\nabla F_\theta(x) = 0$, and by strict concavity $x = x^*$. Conversely, $\nabla F_\theta(x^*) = 0$ gives $x_+ = x^*$. $\square$

The direction $x_+ - x = (Q + D)^{-1}\nabla F_\theta(x)$ is an ascent direction, since $\nabla F_\theta^\top (Q + D)^{-1}\nabla F_\theta > 0$ when $\nabla F_\theta \ne 0$. The implementation halves the step until $F_\theta$ does not decrease. That damped Newton methods converge for smooth strictly concave functions, and quadratically near $x^*$, is a standard result of numerical optimization; it is used here, not proved, and the tests check that the gradient vanishes at the returned point.

## Claim 3: the same identity gives the marginals of L5 and L6

For fixed $\theta$, index $i$ and value $z$, let $x_{-i}$ be the other coordinates. For every $x_{-i}$,

$$\pi(x_i = z \mid \theta, y) = \frac{\pi((z, x_{-i}), \theta, y)}{\pi(x_{-i} \mid x_i = z, \theta, y)\, \pi(\theta, y)}.$$

*Proof.* Claim 1 with the pair $(x_{-i}, x_i)$ in place of $(x, \theta)$. $\square$

L6 replaces $\pi(x_{-i} \mid x_i = z, \theta, y)$ by a Gaussian approximation with mode $x'_{-i}$, the maximizer of $F_\theta$ with $x_i = z$ held (it exists and is unique by Claim 2 applied to the free coordinates, with the linear term $-Q_{-i,i}z$ added), and precision $P_{-i}(x') = Q_{-i,-i} + D_{-i}(x')$. At $x_{-i} = x'_{-i}$ the approximation equals $(2\pi)^{-(n-1)/2}\det P_{-i}^{1/2}$, which gives

$$\tilde\pi(x_i = z \mid \theta, y) \propto \exp\big(F_\theta(x') - \tfrac12\log\det P_{-i}(x')\big),$$

with a constant independent of $z$; L7 removes it by normalizing over $z$.

## Claim 4: with a Gaussian likelihood every step is exact

Let $g_j(v) = -\frac{(y_j - v)^2}{2s_j^2} + \text{const}$. Then:

(a) $\pi(x \mid \theta, y) = N(x^*, P^{-1})$ with $P = Q(\theta) + \operatorname{diag}(1/s_j^2)$ and $x^* = P^{-1}(y_j/s_j^2)_j$, and L2 reaches $x^*$ in one Newton step from any start.

(b) $\tilde\pi(\theta \mid y)$ of L4 equals $\pi(\theta \mid y)$ up to a constant factor.

(c) The marginal of the Gaussian approximation and the full Laplace marginal of L6 both equal $\pi(x_i \mid \theta, y)$.

(d) The output of L9 is $\sum_k w_k \pi(x_i \mid \theta_k, y)$ with $w_k \propto \pi(\theta_k \mid y)$: the only error left is that of the numerical integration over $\theta$.

*Proof.* (a) $F_\theta(x) = -\tfrac12 x^\top P x + x^\top (y_j/s_j^2)_j + \text{const}$ is a quadratic with Hessian $-P$, so $e^{F_\theta}$ is proportional to the $N(x^*, P^{-1})$ density. $D = \operatorname{diag}(1/s_j^2)$ does not depend on $x$, and Newton's method maximizes a concave quadratic in one step. (b) $\pi_G$ is the exact conditional, so by Claim 1 the ratio in L4 is $\pi(\theta \mid y)\pi(y)$, and $\pi(y)$ does not depend on $\theta$. (c) The marginal of $N(x^*, P^{-1})$ is $N(x^*_i, (P^{-1})_{ii})$, which is exact by (a). For L6, the law of $x_{-i}$ given $x_i = z$ under a Gaussian is Gaussian with precision $P_{-i,-i}$ and mean equal to its mode $x'_{-i}$, so the approximation in Claim 3 is exact, and $\tilde\pi(x_i \mid \theta, y) = \pi(x_i \mid \theta, y)$ after normalization. (d) L8 normalizes the exact $\pi(\theta_k \mid y)$ over the grid, and L9 mixes the exact conditionals. $\square$

The tests confirm (b) to $10^{-9}$ in $\log\tilde\pi(\theta \mid y)$ and (d) to $10^{-6}$ in the density, for $n = 4$ and $17$ grid values.

## Claim 5: L9 is a quadrature rule for the marginal

$\pi(x_i \mid y) = \int \pi(x_i \mid \theta, y)\, \pi(\theta \mid y)\, d\theta$, and with equally spaced $\theta_k$ and $w_k = \tilde\pi(\theta_k \mid y)/\sum_m \tilde\pi(\theta_m \mid y)$, L9 is this integral by the rectangle rule, divided by the same rule applied to $\int \pi(\theta \mid y)\, d\theta = 1$.

*Proof.* $\sum_k w_k f_k = \frac{\Delta\sum_k \tilde\pi(\theta_k \mid y) f_k}{\Delta\sum_m \tilde\pi(\theta_m \mid y)}$, which is the ratio of the two rectangle sums with spacing $\Delta$. $\square$

The same sum gives the [marginal likelihood](/marginal-likelihood/): by Claim 1 with all constants kept, $\pi(y) = \int \pi(x^*, \theta, y)/\pi(x^* \mid \theta, y)\, d\theta$, which the code estimates by $\Delta\sum_k e^{\ell_k}$.

## What is proved and what is cited

Claims 1 to 5 are exact identities. When the likelihood is not Gaussian, the error of INLA comes from the Gaussian approximations in L4 and L6. For a fixed number of latent variables and growing data, a Laplace approximation of a ratio of integrals, as in L4 after normalization, has a small relative error that shrinks with the amount of data (Tierney and Kadane 1986; Kass, Tierney and Kadane 1990). In latent Gaussian models the dimension usually grows with the data, and Rue, Martino and Chopin (2009) discuss when the approximations stay accurate. Fong, Rue and Wakefield (2010) report that the approximation can be poor for binary data with few observations per latent variable. These error results are cited, not proved. The errors in the examples of the page are measured against brute-force numerical integration only.
