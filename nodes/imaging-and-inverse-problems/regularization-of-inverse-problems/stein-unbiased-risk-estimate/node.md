---
tag: PFPHX9
kind: theorem
slug: stein-unbiased-risk-estimate
name: Stein's unbiased risk estimate
aliases:
- SURE
- Stein unbiased risk estimator
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: advanced
summary: For Gaussian noise the mean squared error of a weakly differentiable estimator has an unbiased estimate from the data and the divergence of the estimator.
prereqs: [mean-squared-error]
see_also: [unbiased-predictive-risk-estimator, james-stein-estimator, generalized-cross-validation, regularization-parameter-choice, admissible-estimator, signal-denoising, image-denoising, bilevel-learning-of-regularizers]
sources:
  - paper: doi:10.1214/aos/1176345632
    title: Charles M. Stein, Estimation of the mean of a multivariate normal distribution, Annals of Statistics 9(6), 1981
    locator: pages 1135 to 1151
  - paper: doi:10.1080/00401706.1973.10489103
    title: C. L. Mallows, Some comments on C_p, Technometrics 15(4), 1973
    locator: pages 661 to 675
  - paper: doi:10.1080/01621459.1995.10476626
    title: David L. Donoho and Iain M. Johnstone, Adapting to unknown smoothness via wavelet shrinkage, Journal of the American Statistical Association 90(432), 1995
    locator: pages 1200 to 1224
  - paper: doi:10.1109/TIP.2008.2001404
    title: Sathish Ramani, Thierry Blu and Michael Unser, Monte-Carlo SURE, a black-box optimization of regularization parameters for general denoising algorithms, IEEE Transactions on Image Processing 17(9), 2008
    locator: pages 1540 to 1554
---

Stein's unbiased risk estimate (SURE) is a formula for the mean squared error of an estimator that can be computed without knowing the truth. Observe $y = \mu + \varepsilon$ with $\varepsilon \sim N(0, \sigma^2I_m)$ and a known $\sigma$, and estimate $\mu$ by $g(y)$. The error $E\lVert g(y) - \mu\rVert^2$ depends on the unknown $\mu$. Stein (1981) proved that, for every weakly differentiable $g$,

$$E\lVert g(y) - \mu\rVert^2 = E\Big[\lVert g(y) - y\rVert^2 + 2\sigma^2\,\mathrm{div}\,g(y)\Big] - m\sigma^2,$$

so the quantity in brackets, minus $m\sigma^2$, is an unbiased estimate of the risk. The residual $\lVert g(y) - y\rVert^2$ alone is too optimistic, because $g$ follows the noise; the divergence $\sum_k \partial g_k/\partial y_k$ measures how strongly it follows, and corrects for it. For a linear estimator $g(y) = Hy$ the divergence is $\mathrm{trace}(H)$, and SURE becomes Mallows' $C_L$, the [unbiased predictive risk estimator](/unbiased-predictive-risk-estimator/) of regularization theory. For nonlinear estimators, such as soft thresholding of wavelet coefficients, it is the basis of SureShrink (Donoho and Johnstone 1995). Stein used it to explain why the [James-Stein estimator](/james-stein-estimator/) beats the observation itself in three or more dimensions.

## Statement

**Setting.** $y = \mu + \varepsilon$ in $\mathbb{R}^m$ with $\mu$ fixed and unknown, $\varepsilon \sim N(0, \sigma^2I_m)$ and $\sigma > 0$ known. A map $h: \mathbb{R} \to \mathbb{R}$ is called absolutely continuous if $h(b) - h(a) = \int_a^b h'(t)\,dt$ for a locally integrable $h'$. A map $g: \mathbb{R}^m \to \mathbb{R}^m$ is weakly differentiable in Stein's sense if, for each $k$ and for almost every value of the other coordinates, the function $t \mapsto g_k(y_1, \dots, t, \dots, y_m)$ in coordinate $k$ is absolutely continuous. Its divergence is $\mathrm{div}\,g = \sum_k \partial g_k/\partial y_k$.

**Lemma (Stein).** Let $Y \sim N(\mu, \sigma^2)$ and let $h$ be absolutely continuous with $E|h'(Y)| < \infty$. Then $E[(Y - \mu)h(Y)] = \sigma^2E[h'(Y)]$.

**Theorem (Stein 1981).** Let $g$ be weakly differentiable with $E\lVert g(y)\rVert^2 < \infty$ and $E|\partial g_k(y)/\partial y_k| < \infty$ for every $k$. Then

$$E\lVert g(y) - \mu\rVert^2 = E\big[\mathrm{SURE}(y)\big], \qquad \mathrm{SURE}(y) = \lVert g(y) - y\rVert^2 + 2\sigma^2\,\mathrm{div}\,g(y) - m\sigma^2.$$

For a linear map $g(y) = Hy$, the identity $E\lVert Hy - \mu\rVert^2 = E\lVert Hy - y\rVert^2 + 2\sigma^2\mathrm{trace}(H) - m\sigma^2$ holds for any noise with mean zero and covariance $\sigma^2I_m$, Gaussian or not.

## In plain words

You want to know how far your cleaned-up signal is from the true signal, but you do not know the true signal. Comparing the cleaned signal with the noisy data is not enough: a cleaner that changes nothing would look perfect. Stein's result gives a fair score. Take the distance to the data, add a penalty for how sensitive the cleaner is to small changes in the data, and subtract a constant that depends only on the noise level. On average this score equals the true error. Because it uses only the data, you can compute it for each setting of a cleaner and pick the setting with the best score.

## Proof

*Proof of the lemma.* Write $Y = \mu + \sigma Z$ with $Z$ standard normal, density $\phi(z) = e^{-z^2/2}/\sqrt{2\pi}$, and $u(z) = h(\mu + \sigma z)$, so $u'(z) = \sigma h'(\mu + \sigma z)$. Since $\phi'(t) = -t\phi(t)$ and $\phi(t) \to 0$ as $|t| \to \infty$,

$$\phi(z) = \int_z^\infty t\phi(t)\,dt \ \text{ for all } z, \qquad \phi(z) = -\int_{-\infty}^z t\phi(t)\,dt \ \text{ for all } z.$$

Use the first form for $z \ge 0$ and the second for $z < 0$:

$$E[u'(Z)] = \int_0^\infty u'(z)\int_z^\infty t\phi(t)\,dt\,dz - \int_{-\infty}^0 u'(z)\int_{-\infty}^z t\phi(t)\,dt\,dz.$$

The integrands $|u'(z)|\,|t|\phi(t)$ over the regions $0 \le z \le t$ and $t \le z < 0$ have total integral $\int|u'(z)|\phi(z)\,dz = \sigma E|h'(Y)| < \infty$, so Fubini's theorem allows swapping the order:

$$E[u'(Z)] = \int_0^\infty t\phi(t)\big(u(t) - u(0)\big)\,dt + \int_{-\infty}^0 t\phi(t)\big(u(t) - u(0)\big)\,dt = E[Z\,u(Z)] - u(0)E[Z] = E[Z\,u(Z)].$$

The middle step uses absolute continuity: $\int_0^t u' = u(t) - u(0)$, and $-\int_t^0 u' = u(t) - u(0)$. The same Fubini bound shows that $E|Z\,u(Z)| < \infty$. Now $E[Z\,u(Z)] = E[(Y - \mu)h(Y)]/\sigma$ and $E[u'(Z)] = \sigma E[h'(Y)]$, which gives the lemma. $\square$

*Proof of the theorem.* First expand the square around $y$:

$$\lVert g(y) - \mu\rVert^2 = \lVert g(y) - y\rVert^2 + 2\langle g(y) - y, y - \mu\rangle + \lVert y - \mu\rVert^2 = \lVert g(y) - y\rVert^2 + 2\langle g(y), y - \mu\rangle - \lVert y - \mu\rVert^2.$$

All terms have finite expectation: $E\lVert g\rVert^2 < \infty$ and $E\lVert y\rVert^2 < \infty$, so $E|\langle g, y - \mu\rangle| < \infty$ by the Cauchy-Schwarz inequality. Take expectations. $E\lVert y - \mu\rVert^2 = m\sigma^2$. For the middle term, fix $k$ and condition on the other coordinates $y_{-k}$, which are independent of $y_k$. For almost every $y_{-k}$, the function $h(t) = g_k(y_1, \dots, t, \dots, y_m)$ is absolutely continuous, and $E[|h'(y_k)| \mid y_{-k}] < \infty$ for almost every $y_{-k}$ because its expectation over $y_{-k}$ is finite. The lemma applied to $y_k \sim N(\mu_k, \sigma^2)$ gives

$$E[(y_k - \mu_k)g_k(y) \mid y_{-k}] = \sigma^2E\Big[\frac{\partial g_k}{\partial y_k}(y) \,\Big|\, y_{-k}\Big].$$

Take the expectation over $y_{-k}$ and sum over $k$: $E\langle g(y), y - \mu\rangle = \sigma^2E[\mathrm{div}\,g(y)]$. Inserting the three expectations gives the theorem.

For the linear case, $\langle Hy, y - \mu\rangle = \langle H\mu, \varepsilon\rangle + \langle H\varepsilon, \varepsilon\rangle$, whose expectation is $E[\varepsilon^TH\varepsilon] = \mathrm{trace}(H\,E[\varepsilon\varepsilon^T]) = \sigma^2\mathrm{trace}(H)$. This uses only the mean and covariance of $\varepsilon$, and the divergence of $y \mapsto Hy$ is $\mathrm{trace}(H)$. $\square$

## Consequences

- **Shrinkage in one dimension.** For $m = 1$, $\sigma = 1$ and $g(y) = y/2$: $\mathrm{SURE}(y) = y^2/4 + 2\cdot\frac12 - 1 = y^2/4$, and $E[y^2/4] = (\mu^2 + 1)/4$, which is the true risk $E(y/2 - \mu)^2 = \mu^2/4 + 1/4$.
- **Linear regularization.** For Tikhonov regularization with $g(y) = H_\alpha y$ and $H_\alpha = A(A^TA + \alpha I)^{-1}A^T$, dividing SURE by $m$ gives the [UPRE](/unbiased-predictive-risk-estimator/) function $U(\alpha)$, an unbiased estimate of the predictive risk $\frac1mE\lVert Ax_\alpha - Ax^\dagger\rVert^2$. For least squares on $k$ columns, $\mathrm{trace}(H) = k$ and SURE is Mallows' $C_p$ times $\sigma^2$.
- **James-Stein.** For $m \ge 3$ and $g(y) = (1 - (m - 2)\sigma^2/\lVert y\rVert^2)y$, $\mathrm{div}\,g = m - (m - 2)^2\sigma^2/\lVert y\rVert^2$, and SURE gives the risk $m\sigma^2 - (m - 2)^2\sigma^4E[1/\lVert y\rVert^2]$, which is below $m\sigma^2$, the risk of $g(y) = y$, for every $\mu$. This is Stein's explanation of the [James-Stein estimator](/james-stein-estimator/) and of the inadmissibility of $y$; see [admissible estimator](/admissible-estimator/).
- **Soft thresholding.** For $g_k(y) = \mathrm{sign}(y_k)\max(|y_k| - \lambda, 0)$, which is Lipschitz and so weakly differentiable, $\partial g_k/\partial y_k = 1$ where $|y_k| > \lambda$ and $0$ where $|y_k| < \lambda$. So $\mathrm{SURE}(y) = \sum_k \min(y_k^2, \lambda^2) + 2\sigma^2\#\{k : |y_k| > \lambda\} - m\sigma^2$, which can be minimized over $\lambda$ after sorting the $|y_k|$. Donoho and Johnstone (1995) used this, applied to each level of a wavelet transform, to build SureShrink for [signal denoising](/signal-denoising/).
- **Black-box estimators.** If $g$ is an algorithm without a formula for its divergence, estimate $\mathrm{div}\,g(y) \approx b^T(g(y + \epsilon b) - g(y))/\epsilon$ with a random vector $b \sim N(0, I)$ and a small $\epsilon$. This is Monte Carlo SURE (Ramani, Blu and Unser 2008), used to tune [image denoising](/image-denoising/) methods and learned regularizers.

## Tightness

- **Gaussian noise is needed for nonlinear $g$.** The lemma characterizes the normal distribution: if $E[(Y - \mu)h(Y)] = \sigma^2E[h'(Y)]$ for all bounded smooth $h$ with bounded derivative, then $Y$ is $N(\mu, \sigma^2)$. For other noise, SURE is biased for nonlinear estimators. Only the linear case survives with general noise.
- **Weak differentiability is needed.** Hard thresholding $g(y) = y\,\mathbf 1\{|y| > \lambda\}$ jumps at $|y| = \lambda$. Its pointwise derivative is $1$ or $0$ almost everywhere, but the formula with that derivative misses the jumps: the true risk has an extra term $2\sigma^2\lambda(\phi_\sigma(\lambda - \mu) + \phi_\sigma(\lambda + \mu))$, with $\phi_\sigma$ the $N(0, \sigma^2)$ density, which the naive estimate leaves out.
- **Known variance.** The estimate uses $\sigma^2$. With an estimated $\sigma^2$ it is no longer unbiased, and a too small $\sigma^2$ makes the divergence penalty too weak, so the minimizing parameter fits the noise.
- **Unbiased, not exact.** The variance of SURE can be large, especially for small $m$. Minimizing SURE over a parameter picks a data-dependent parameter, and the risk at that parameter is not what SURE estimates; guarantees for the minimizer need extra arguments.
- **Error in $\mu$, not in a preimage.** SURE estimates the error in the space of the data. For an inverse problem $y = Ax + \varepsilon$ it estimates $E\lVert Ax_\alpha - Ax\rVert^2$, not $E\lVert x_\alpha - x\rVert^2$, which has no unbiased estimate when $A$ is not invertible.

## History

Mallows (1973) gave $C_p$ and $C_L$, the unbiased risk estimates for linear estimators. Stein (1981) proved the lemma and the identity for weakly differentiable estimators of a normal mean, in the paper that also explained the James-Stein phenomenon, and the estimate took his name. Donoho and Johnstone (1995) made it a practical tool for adaptive wavelet denoising. Later work extended it to exponential families, to estimators without a closed form via Monte Carlo divergence (Ramani, Blu and Unser 2008), and to the training of denoisers and regularizers without clean data.

## References
