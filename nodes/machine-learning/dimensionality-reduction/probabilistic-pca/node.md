---
tag: V9B0Y7
kind: model
slug: probabilistic-pca
name: Probabilistic PCA
aliases:
- PPCA
- probabilistic principal component analysis
area: machine-learning/dimensionality-reduction
level: advanced
summary: "The Gaussian latent model x = Wz + mu + eps with isotropic noise. Its maximum likelihood W spans the principal subspace, and sigma^2 is the mean of the discarded eigenvalues."
prereqs: [principal-component-analysis, maximum-likelihood-estimation, expectation-maximization]
see_also: [factor-analysis, gaussian-mixture-model, autoencoder, variational-autoencoder, explained-variance, reconstruction-error, scree-plot, whitening]
sources:
  - paper: doi:10.1111/1467-9868.00196
    title: Michael E. Tipping and Christopher M. Bishop, Probabilistic principal component analysis, Journal of the Royal Statistical Society, Series B 61(3), 611-622, 1999
    locator: the latent variable model, the closed-form maximum likelihood estimators of W and sigma^2, the maximum of the log likelihood, the posterior of the latent variables, and the EM algorithm
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: Section 12.2 (12.2.1 maximum likelihood PCA, 12.2.2 EM algorithm for PCA, 12.2.3 Bayesian PCA, 12.2.4 factor analysis)
  - paper: "Sam Roweis, EM algorithms for PCA and SPCA, Advances in Neural Information Processing Systems 10, 626-632, 1998"
    title: Roweis 1998
    locator: EM for PCA in the zero-noise limit and its cost per iteration without forming the covariance matrix
  - paper: doi:10.1162/089976699300016728
    title: Michael E. Tipping and Christopher M. Bishop, Mixtures of probabilistic principal component analyzers, Neural Computation 11(2), 443-482, 1999
    locator: mixtures of PPCA models fitted by EM
---

Probabilistic PCA (PPCA) is the Gaussian latent variable model $x = W z + \mu + \varepsilon$, with $z \sim \mathcal{N}(0, I_q)$ and isotropic noise $\varepsilon \sim \mathcal{N}(0, \sigma^2 I_d)$. Tipping and Bishop (1999) showed that its [maximum likelihood](/maximum-likelihood-estimation/) fit has a closed form: $W = U_q (\Lambda_q - \sigma^2 I)^{1/2} R$, where $U_q$ holds the top $q$ eigenvectors of the sample [covariance matrix](/covariance-matrix/), $\Lambda_q$ their eigenvalues and $R$ any rotation, and $\sigma^2$ is the mean of the $d - q$ discarded eigenvalues. So the fitted $W$ spans the subspace of [PCA](/principal-component-analysis/). The model adds a density, a likelihood, posterior scores and an [EM algorithm](/expectation-maximization/) to PCA.

## The machine

**Parameters.** A mean $\mu \in \mathbb{R}^d$, a $d \times q$ matrix $W$ with $q < d$, and a noise variance $\sigma^2 > 0$.

**Generation.** Draw $z \sim \mathcal{N}(0, I_q)$ and an independent $\varepsilon \sim \mathcal{N}(0, \sigma^2 I)$, and output $x = W z + \mu + \varepsilon$. Then

$$x \sim \mathcal{N}(\mu, C), \qquad C = W W^T + \sigma^2 I .$$

$C$ has the eigenvalue $\sigma^2$ with multiplicity at least $d - q$, and the larger eigenvalues $\sigma^2 + l_j^2$ in the directions of the left singular vectors of $W$ (with singular values $l_j$). So PPCA is a Gaussian whose covariance is "low rank plus a constant".

**Posterior.** With the $q \times q$ matrix $M = W^T W + \sigma^2 I$,

$$z \mid x \sim \mathcal{N}\big(M^{-1} W^T (x - \mu),\ \sigma^2 M^{-1}\big).$$

**Likelihood.** For $n$ independent points with sample mean $\bar x$ and covariance $S$ (divisor $n$), the fit of $\mu$ is $\bar x$ and

$$\ell(W, \sigma^2) = -\frac{n}{2}\Big(d \ln 2\pi + \ln\det C + \operatorname{tr}(C^{-1} S)\Big).$$

## What it counts

- **Log likelihood** of the data, and the density $\mathcal{N}(x \mid \mu, C)$ of a new point. Its Mahalanobis term splits into the distance within the principal subspace and the residual, the [reconstruction error](/reconstruction-error/) of the point, divided by $\sigma^2$. This makes PPCA a density model for anomaly detection and classification.
- **Posterior scores** $\mathbb{E}[z \mid x]$, the probabilistic analogue of the principal component scores.
- **Free parameters.** $W$ has $dq$ entries, but $W$ and $WR$ give the same $C$ for orthogonal $R$, so the model has $dq - q(q-1)/2 + 1$ free parameters besides $\mu$. This number is linear in $d$, against $d(d+1)/2$ for a full covariance, which is the reason to use PPCA in high dimension.
- **Cost.** $C^{-1}$ and $\ln\det C$ follow from $M$ by the [Woodbury identity](/woodbury-identity/) and the matrix determinant lemma: $C^{-1} = \sigma^{-2}(I - W M^{-1} W^T)$ and $\det C = \sigma^{2(d-q)} \det M$. So one density evaluation costs $O(d q)$ after an $O(d q^2)$ setup.

## Relation to other models

- **PCA.** As $\sigma^2 \to 0$ with $W$ fixed, the posterior mean $W M^{-1} W^T (x - \mu)$ of $W z$ tends to the orthogonal projection of $x - \mu$ on the column space of $W$, which is the PCA reconstruction. For $\sigma^2 > 0$ the posterior mean is shrunk toward $\mu$. In the maximum likelihood fit the column space of $W$ is the principal subspace, but the columns themselves are orthogonal eigenvectors only for $R = I$.
- **Factor analysis.** [Factor analysis](/factor-analysis/) is the same model with a diagonal noise covariance $\Psi$ in place of $\sigma^2 I$. It has no closed form, and it is equivariant under rescaling of the features, which PPCA is not.
- **Mixtures.** A mixture of PPCA models is a [Gaussian mixture model](/gaussian-mixture-model/) whose covariances are low rank plus isotropic; Tipping and Bishop (1999, Neural Computation) fit it by EM.
- **Bayesian PCA.** A prior on the columns of $W$ with one precision per column can switch off unneeded columns, which chooses $q$ (Bishop, Section 12.2.3).
- **Autoencoders.** A linear [autoencoder](/autoencoder/) with squared loss learns the same subspace without a noise model. A [variational autoencoder](/variational-autoencoder/) with a linear Gaussian decoder and isotropic noise is PPCA.

## Known results in the model

### The closed-form maximum

Let $S$ have the eigenvalues $\lambda_1 \ge \cdots \ge \lambda_d$ and orthonormal eigenvectors $u_1, \ldots, u_d$, and assume $\lambda_q > \lambda_{q+1}$. Tipping and Bishop (1999) proved that the global maximum of $\ell$ is at

$$\sigma^2_{\mathrm{ML}} = \frac{1}{d - q} \sum_{j = q+1}^{d} \lambda_j, \qquad W_{\mathrm{ML}} = U_q (\Lambda_q - \sigma^2_{\mathrm{ML}} I)^{1/2} R,$$

with $U_q = [u_1, \ldots, u_q]$, $\Lambda_q = \operatorname{diag}(\lambda_1, \ldots, \lambda_q)$ and $R$ any orthogonal $q \times q$ matrix, and that the maximum value is

$$\ell_{\max} = -\frac{n}{2}\Big(d \ln 2\pi + \sum_{j=1}^{q} \ln\lambda_j + (d - q)\ln\sigma^2_{\mathrm{ML}} + d\Big).$$

*Sketch.* The gradient $\partial \ell / \partial W = n(C^{-1} S C^{-1} W - C^{-1} W)$ vanishes when $S C^{-1} W = W$. Write $W = U L R^T$ with orthonormal columns in $U$ and $L$ diagonal positive. Then $C^{-1} U = U (L^2 + \sigma^2 I)^{-1}$, and the condition becomes $S u_j = (l_j^2 + \sigma^2) u_j$: each column of $U$ is an eigenvector of $S$ with $\lambda_j = l_j^2 + \sigma^2$. Putting this into $\ell$ and maximizing over $\sigma^2$ gives the mean of the eigenvalues not used, and the value

$$-\frac n2\Big(d\ln 2\pi + \sum_{j} \ln \lambda_j + (d - q)\big[\ln \overline{\lambda}_{\text{out}} - \overline{\ln \lambda}_{\text{out}}\big] + d\Big),$$

where the bracket is the log of the ratio of the arithmetic and geometric means of the discarded eigenvalues. Tipping and Bishop show that this is smallest, and the stationary point is a maximum rather than a saddle, exactly when the discarded eigenvalues are the $d - q$ smallest ones. $\square$

Two consequences: the principal subspace is the maximum likelihood subspace of a Gaussian model, and $\sigma^2_{\mathrm{ML}}$ is the [reconstruction error](/reconstruction-error/) of rank $q$ PCA divided by $d - q$.

### Fitting by EM

The closed form needs all eigenvalues, or at least the trace and the top $q$. EM avoids the eigendecomposition and handles missing values; each step uses only products with $S$ (Tipping and Bishop 1999; Bishop, Section 12.2.2):

```pseudo id=main
EM-PPCA(S, n, q, ε)
L1  W ← random d × q matrix; σ² ← tr(S)/d
L2  repeat
L3      M ← W^T W + σ² I
L4      W_new ← S W (σ² I + M^(−1) W^T S W)^(−1)
L5      σ² ← (1/d) tr(S − S W M^(−1) W_new^T)
L6      W ← W_new
L7  until ℓ(W, σ²) grew by less than ε (relative)
L8  return W, σ²
```

These are the E step (posterior means $M^{-1} W^T (x_i - \bar x)$ and second moments $\sigma^2 M^{-1} + \mathbb{E}[z]\mathbb{E}[z]^T$) and the M step, combined and written in terms of $S$. By the general argument on the [EM](/expectation-maximization/) page, $\ell$ never decreases. The only stable fixed points are the global maxima above; the other stationary points, built on other eigenvectors, are saddle points (Tipping and Bishop 1999). One step costs $O(d^2 q)$ with $S$ given, or $O(n d q)$ when the products $S W$ are formed from the data without $S$ (Roweis 1998), which is cheaper than an $O(n d^2)$ covariance when $q \ll d$.

### A worked example

The eight points of the [PCA](/principal-component-analysis/) page have $S$ with the eigenvalues $81, 36, 9$ and eigenvectors $u_1 = (1, 2, 2)/3$, $u_2 = (2, 1, -2)/3$, $u_3 = (2, -2, 1)/3$.

- $q = 1$: $\sigma^2 = (36 + 9)/2 = 22.5$ and $W = \sqrt{81 - 22.5}\, u_1 = \sqrt{58.5}\, u_1 \approx (2.5495, 5.0990, 5.0990)$. The maximum is $\ell = -4(3 \ln 2\pi + \ln 81 + 2 \ln 22.5 + 3) \approx -76.5404$ for $n = 8$. For the point $(13, 11, 9)$, with PCA score 9, the posterior mean is $\sqrt{58.5} \cdot 9 / 81 \approx 0.8498$.
- $q = 2$: $\sigma^2 = 9$ and $W = [\sqrt{72}\, u_1, \sqrt{27}\, u_2]$. Then $W W^T + 9 I = 81 u_1 u_1^T + 36 u_2 u_2^T + 9 u_3 u_3^T = S$: with $d - q = 1$ the model fits $S$ exactly, and $\ell = -4(3\ln 2\pi + \ln(81 \cdot 36 \cdot 9) + 3) \approx -74.7553$.

EM for $q = 1$ from a random start (`random.Random(3)`) gives $\ell \approx -82.2147, -79.1776, -78.4309, -77.6894, -77.0581, -76.7287, \ldots$ and stops after 31 steps at $-76.5404$ with $\sigma^2 \approx 22.50001$ and the same $W$ up to sign.

### Choosing q

$\ell_{\max}$ grows with $q$, so the likelihood alone does not choose $q$. Options are a penalty such as BIC with the parameter count above, held-out likelihood, Bayesian PCA, or the heuristics of the [scree plot](/scree-plot/) and the [explained variance](/explained-variance/).

## References
