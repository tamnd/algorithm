---
title: Kirkwood's identity, the concavity of A along a linear path, and the error of the estimator
proves: [correctness]
status: full
---

Let $U_\lambda(x)$, $\lambda \in [0, 1]$, be a family of potentials with $Z_\lambda = \int e^{-\beta U_\lambda(x)}\,dx$ finite and positive, and $A_\lambda = -\beta^{-1} \ln Z_\lambda$. Write $\langle f \rangle_\lambda = Z_\lambda^{-1} \int f\, e^{-\beta U_\lambda}\,dx$ and $U' = \partial U_\lambda / \partial \lambda$. Assume that $U_\lambda(x)$ is twice differentiable in $\lambda$ and that $e^{-\beta U_\lambda}$, $|U'| e^{-\beta U_\lambda}$, $(U')^2 e^{-\beta U_\lambda}$ and $|\partial^2 U_\lambda / \partial \lambda^2|\, e^{-\beta U_\lambda}$ are bounded, uniformly for $\lambda$ in a neighbourhood of each point, by integrable functions of $x$. Then derivatives in $\lambda$ may be taken under the integral sign (dominated convergence).

**Claim 1 (Kirkwood's identity).** $dA_\lambda / d\lambda = \langle U' \rangle_\lambda$, and therefore
$$A_1 - A_0 = \int_0^1 \langle U' \rangle_\lambda\, d\lambda.$$

*Proof.* $dZ_\lambda / d\lambda = \int -\beta U'\, e^{-\beta U_\lambda}\,dx = -\beta Z_\lambda \langle U' \rangle_\lambda$. So $dA_\lambda / d\lambda = -\beta^{-1} Z_\lambda^{-1}\, dZ_\lambda / d\lambda = \langle U' \rangle_\lambda$. The derivative is continuous in $\lambda$ under the same domination, so the fundamental theorem of calculus gives the integral. $\square$

**Claim 2 (curvature).**
$$\frac{d^2 A_\lambda}{d\lambda^2} = \Bigl\langle \frac{\partial^2 U_\lambda}{\partial \lambda^2} \Bigr\rangle_\lambda - \beta\, \mathrm{var}_\lambda(U').$$
On the linear path $U_\lambda = (1 - \lambda) U_0 + \lambda U_1$ the first term is 0, so $A_\lambda$ is concave in $\lambda$ and $g(\lambda) = \langle U_1 - U_0 \rangle_\lambda$ is non-increasing.

*Proof.* Differentiate $\langle U' \rangle_\lambda = Z_\lambda^{-1} \int U' e^{-\beta U_\lambda}\,dx$:
$$\frac{d}{d\lambda} \langle U' \rangle_\lambda = \Bigl\langle \frac{\partial^2 U_\lambda}{\partial \lambda^2} \Bigr\rangle_\lambda - \beta \langle (U')^2 \rangle_\lambda + \beta \langle U' \rangle_\lambda^2,$$
where the last term comes from $d Z_\lambda^{-1} / d\lambda = \beta Z_\lambda^{-1} \langle U' \rangle_\lambda$ by Claim 1. The last two terms are $-\beta\, \mathrm{var}_\lambda(U')$. On the linear path $\partial^2 U / \partial \lambda^2 = 0$ and the variance is at least 0. $\square$

**Claim 3 (the estimator).** Let the run at node $\lambda_j$ give $\bar g_j$, the mean of $U'(\lambda_j, x_i)$ over $N$ samples, with $E[\bar g_j] = g(\lambda_j)$ (exact draws, or a stationary chain started in equilibrium) and the runs independent. Then the output $T = \sum_j a_j \bar g_j$ has $E[T] = Q = \sum_j a_j g(\lambda_j)$ and $\mathrm{var}(T) = \sum_j a_j^2 \mathrm{var}(\bar g_j)$. With independent draws and $\mathrm{var}_\lambda(U') < \infty$ at the nodes, $T \to Q$ with probability 1 and $\mathrm{var}(T) = \sum_j a_j^2 \mathrm{var}_{\lambda_j}(U') / N$.

*Proof.* Linearity of expectation, independence of the runs for the variance of the sum, the law of large numbers at each node, and $\mathrm{var}(\bar g_j) = \mathrm{var}_{\lambda_j}(U') / N$ for independent draws. $\square$

Lines L4 and L5 estimate $\mathrm{var}(\bar g_j)$ by $s_j^2$ and add $a_j^2 s_j^2$, which is the plug-in form of this variance. With batch means, $s_j^2$ estimates the variance of a correlated mean instead.

**Claim 4 (total error).**
$$T - \Delta A = (Q - \Delta A) + (T - Q),$$
where $Q - \Delta A$ is the quadrature error of the rule on $g$, a fixed number, and $T - Q$ has mean 0 and standard deviation $\sqrt{\mathrm{var}(T)} = O(N^{-1/2})$. If $g$ is $C^2$ on $[0, 1]$, the composite trapezoidal rule with $K$ intervals has $|Q - \Delta A| \le \max|g''| / (12 K^2)$; if $g$ is $C^4$, the composite Simpson rule has $|Q - \Delta A| \le \max|g^{(4)}| / (180 K^4)$; the $n$-point Gauss-Legendre rule is exact when $g$ is a polynomial of degree at most $2n - 1$.

*Proof.* The split is an identity, $\Delta A = \int_0^1 g$ by Claim 1, and Claim 3 gives the mean and variance of $T - Q$. The quadrature bounds are the standard error bounds of these rules on an interval of length 1, proved on the pages of the [trapezoidal rule](/trapezoidal-rule/), the [Simpson rule](/simpsons-rule/) and [Gaussian quadrature](/gaussian-quadrature/). $\square$

**Claim 5 (the harmonic example).** For $U_\lambda = (1 + \lambda) x^2 / 2$ in one dimension, $g(\lambda) = 1 / (2\beta (1 + \lambda))$ and $\Delta A = (2\beta)^{-1} \ln 2$.

*Proof.* $U' = x^2/2$ and $x$ is normal with variance $1/(\beta(1 + \lambda))$ in state $\lambda$, so $g(\lambda) = 1/(2\beta(1+\lambda))$. Its integral over $[0, 1]$ is $(2\beta)^{-1} \ln 2$, which equals $-\beta^{-1} \ln \sqrt{k_0 / k_1}$ with $k_0 = 1$, $k_1 = 2$, the ratio of the Gaussian partition functions $\sqrt{2\pi / (\beta k)}$. $\square$

The integrand $g$ here is decreasing, as Claim 2 requires, since $U_\lambda = (1 - \lambda) U_0 + \lambda U_1$ with $U_0 = x^2/2$ and $U_1 = x^2$. It is also convex, so the trapezoidal rule overestimates the integral, as the example on the page shows.
