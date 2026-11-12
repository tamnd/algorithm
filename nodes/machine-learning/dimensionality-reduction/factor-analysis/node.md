---
tag: 7FPPGW
kind: model
slug: factor-analysis
name: Factor analysis
aliases:
- common factor model
- linear factor model
area: machine-learning/dimensionality-reduction
level: core
summary: "A latent Gaussian model x = mu + Lambda z + eps with a diagonal noise covariance Psi. Fitted by maximum likelihood with EM; the loadings are only defined up to a rotation."
prereqs: [covariance-matrix, maximum-likelihood-estimation, expectation-maximization]
see_also: [probabilistic-pca, principal-component-analysis, independent-component-analysis, gaussian-mixture-model, explained-variance, scree-plot, variational-autoencoder, state-space-model]
sources:
  - paper: doi:10.2307/1412107
    title: C. Spearman, General intelligence, objectively determined and measured, The American Journal of Psychology 15(2), 201-292, 1904
    locator: the one-factor model of test scores, a general factor plus a specific part for each test
  - paper: doi:10.1007/BF02293851
    title: Donald B. Rubin and Dorothy T. Thayer, EM algorithms for ML factor analysis, Psychometrika 47(1), 69-76, 1982
    locator: the EM algorithm for maximum likelihood factor analysis, with the E step on the factor scores and the closed-form M step for the loadings and the unique variances
  - paper: doi:10.1007/BF02289233
    title: Henry F. Kaiser, The varimax criterion for analytic rotation in factor analysis, Psychometrika 23(3), 187-200, 1958
    locator: the varimax criterion, its row normalization by the communalities, and the rotation of pairs of factors by the angle with tan 4 phi given in closed form
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: Section 12.2.4 (factor analysis, the marginal covariance W W^T + Psi, and the EM updates of W and Psi)
  - book: isbn:9780471360919
    title: T. W. Anderson, An Introduction to Multivariate Statistical Analysis, third edition, Wiley, 2003
    locator: Chapter 14 (factor analysis, identification, maximum likelihood estimators and rotation)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 14.7.1 (latent variables and factor analysis, the rotation problem, and the comparison with PCA)
---

Factor analysis models each observed vector $x \in \mathbb{R}^d$ as a linear function of $k < d$ hidden *factors* plus noise: $x = \mu + \Lambda z + \varepsilon$, with $z \sim \mathcal{N}(0, I_k)$ and $\varepsilon \sim \mathcal{N}(0, \Psi)$, where $\Psi$ is **diagonal**. The factors explain all the correlation between the features, and each feature has its own noise variance. With $\Psi = \sigma^2 I$ the model becomes [probabilistic PCA](/probabilistic-pca/), which has a closed-form fit; general factor analysis has none and is fitted by [maximum likelihood](/maximum-likelihood-estimation/) with the [EM algorithm](/expectation-maximization/) of Rubin and Thayer (1982). The loadings $\Lambda$ are only defined up to an orthogonal rotation, and rotations such as varimax (Kaiser 1958) choose one that is easy to read.

## The machine

**Parameters.** A mean $\mu \in \mathbb{R}^d$, a $d \times k$ loading matrix $\Lambda$, and the unique variances $\Psi = \operatorname{diag}(\psi_1, \ldots, \psi_d)$ with $\psi_i > 0$.

**Generation.** Draw $z \sim \mathcal{N}(0, I_k)$ and an independent $\varepsilon \sim \mathcal{N}(0, \Psi)$, and output $x = \mu + \Lambda z + \varepsilon$. So $x$ is Gaussian with

$$x \sim \mathcal{N}(\mu, \Sigma), \qquad \Sigma = \Lambda \Lambda^T + \Psi .$$

The diagonal of $\Lambda \Lambda^T$ holds the *communalities* $h_i^2 = \sum_j \lambda_{ij}^2$, the part of the variance of feature $i$ that the factors share; $\psi_i$ is the part that belongs to feature $i$ alone. Since $\Psi$ is diagonal, the features are independent given $z$, and all covariance between two different features comes from $\Lambda \Lambda^T$.

**Posterior of the factors.** Given $x$, the factors are Gaussian with

$$\mathbb{E}[z \mid x] = \beta (x - \mu), \qquad \operatorname{Cov}[z \mid x] = I - \beta \Lambda, \qquad \beta = \Lambda^T \Sigma^{-1} = (I + \Lambda^T \Psi^{-1} \Lambda)^{-1} \Lambda^T \Psi^{-1}.$$

The two forms of $\beta$ are equal by the [Woodbury identity](/woodbury-identity/); the second needs only a $k \times k$ inverse. $\mathbb{E}[z \mid x]$ is the regression (Thomson) factor score of a point.

**Data and likelihood.** For $n$ independent points, the maximum likelihood estimate of $\mu$ is the sample mean, and the log likelihood depends on the data only through the [covariance matrix](/covariance-matrix/) $S$ with the divisor $n$:

$$\ell(\Lambda, \Psi) = -\frac{n}{2}\Big(d \ln 2\pi + \ln\det\Sigma + \operatorname{tr}(\Sigma^{-1} S)\Big).$$

## What it counts

- **Log likelihood** $\ell(\Lambda, \Psi)$, the value that the fit maximizes. Its upper bound is the value of the saturated model $\Sigma = S$, which is $-\frac n2 (d \ln 2\pi + \ln\det S + d)$ when $S$ is positive definite.
- **Free parameters.** $\Lambda$ and $\Psi$ have $dk + d$ entries, but $\Lambda$ and $\Lambda R$ give the same model for each orthogonal $k \times k$ matrix $R$, which removes $k(k-1)/2$. The model is a restriction of a general covariance (which has $d(d+1)/2$ entries) when
$$\frac{d(d+1)}{2} - \Big(dk + d - \frac{k(k-1)}{2}\Big) = \frac{(d - k)^2 - (d + k)}{2} \ge 0 .$$
For $d = 3$ and $k = 1$ the difference is 0; for $d = 6$ and $k = 2$ it is 4. The difference is the number of degrees of freedom of the likelihood ratio test of the model against the saturated one.
- **Communalities and uniquenesses** $h_i^2$ and $\psi_i$, often reported for standardized features, where $h_i^2 + \psi_i = 1$ at the fit.
- **Factor scores** $\mathbb{E}[z \mid x]$ for each point.

One evaluation of $\ell$ costs $O(d^3)$ given $S$, and computing $S$ costs $O(n d^2)$ once.

## Relation to other models

- **Probabilistic PCA.** [PPCA](/probabilistic-pca/) is the same model with the isotropic noise $\Psi = \sigma^2 I$. Its maximum likelihood fit is closed form from the eigenvectors of $S$. Factor analysis allows a different noise level for each feature, which costs the closed form.
- **PCA.** As $\sigma^2 \to 0$ in PPCA, the fit gives the principal subspace of [PCA](/principal-component-analysis/). Factor analysis and PCA differ in two ways. Factor analysis models only the shared covariance and leaves the diagonal to $\Psi$, while PCA explains the whole variance, including the noise of each feature. And factor analysis is equivariant under rescaling of the features: if $x$ becomes $D x$ for a diagonal $D > 0$, the fit becomes $D\Lambda$ and $D \Psi D$, with the same likelihood. PCA on the covariance and PCA on the correlation matrix give different answers, but maximum likelihood factor analysis gives the same answer up to this rescaling.
- **ICA.** If the factors are not Gaussian, the rotation is no longer free: [independent component analysis](/independent-component-analysis/) uses the non-Gaussianity to fix it.
- **Mixtures.** A mixture of factor analyzers is a [Gaussian mixture model](/gaussian-mixture-model/) whose component covariances are $\Lambda_j \Lambda_j^T + \Psi_j$, which keeps the number of parameters linear in $d$.
- **Over time.** A [linear Gaussian state-space model](/state-space-model/) is a factor model whose factors follow a linear dynamic; the factor model is its observation equation.
- **Nonlinear decoders.** A [variational autoencoder](/variational-autoencoder/) with a Gaussian decoder of diagonal covariance replaces $\mu + \Lambda z$ by a neural network of $z$.

## Known results in the model

### Rotation non-identifiability

For each orthogonal $R$, $(\Lambda R)(\Lambda R)^T = \Lambda \Lambda^T$, so $\Lambda$ and $\Lambda R$ give the same distribution of $x$ and the same likelihood. The data can never decide between them. For $k = 1$ this is only a sign. For $k \ge 2$ users choose a rotation that is easy to interpret, with each feature loading on few factors.

**Varimax** (Kaiser 1958) maximizes the sum over the factors of the variance of the squared loadings,

$$V(\Lambda) = \sum_{j=1}^{k} \bigg[\frac1d \sum_{i=1}^{d} \tilde\lambda_{ij}^4 - \Big(\frac1d \sum_{i=1}^{d} \tilde\lambda_{ij}^2\Big)^2\bigg], \qquad \tilde\lambda_{ij} = \lambda_{ij} / h_i ,$$

where the division by the communality $h_i$ is Kaiser's normalization (the raw criterion uses $\lambda_{ij}$). Kaiser's method rotates two factors $p, q$ at a time in their plane. With $u_i = \tilde\lambda_{ip}^2 - \tilde\lambda_{iq}^2$ and $v_i = 2 \tilde\lambda_{ip} \tilde\lambda_{iq}$, the best angle $\phi$ satisfies

$$\tan 4\phi = \frac{2 \sum_i u_i v_i - 2 \big(\sum_i u_i\big)\big(\sum_i v_i\big)/d}{\sum_i (u_i^2 - v_i^2) - \big((\sum_i u_i)^2 - (\sum_i v_i)^2\big)/d},$$

with the quadrant chosen so that $V$ grows. The method sweeps over all pairs until the angles are small. Oblique rotations, such as promax, drop the condition that $R$ is orthogonal and allow correlated factors.

### Fitting by EM

No closed form for the maximum likelihood estimate is known in general. Rubin and Thayer (1982) treat $z$ as missing data. With $\beta = \Lambda^T \Sigma^{-1}$, the E step needs only the averages $\frac1n \sum_i \mathbb{E}[z_i](x_i - \bar x)^T = \beta S$ and $G = \frac1n \sum_i \mathbb{E}[z_i z_i^T] = I - \beta\Lambda + \beta S \beta^T$. The M step is a [least squares](/linear-regression/) fit of $x$ on the expected factors (Bishop, Section 12.2.4):

```pseudo id=main
EM-FACTOR-ANALYSIS(S, n, k, ε)
L1  Λ ← random d × k matrix; Ψ ← diag(S)/2
L2  repeat
L3      β ← Λ^T (Λ Λ^T + Ψ)^(−1)                ▷ E step: E[z | x] = β(x − x̄)
L4      G ← I − βΛ + β S β^T                     ▷ the mean of E[z z^T | x] over the data
L5      Λ ← S β^T G^(−1)                         ▷ M step for the loadings
L6      Ψ ← diag(S − Λ β S)                      ▷ M step for the noise, with the new Λ
L7  until ℓ(Λ, Ψ) grew by less than ε (relative)
L8  return Λ, Ψ
```

**Monotonicity.** Each step is an EM step: L3 and L4 compute the expected complete-data statistics under the current parameters, and L5 and L6 maximize the expected complete-data log likelihood, first over $\Lambda$ and then over $\Psi$ given that $\Lambda$, which is its joint maximizer. By the general EM argument on the [expectation-maximization](/expectation-maximization/) page, $\ell$ never decreases. Like every local method, EM can stop at a local maximum or a saddle point, and it can be slow when the factors are weak.

**The fit matches the variances.** At a fixed point with all $\psi_i$ positive, $\operatorname{diag}(\Lambda \Lambda^T + \Psi) = \operatorname{diag}(S)$. *Proof.* Put $P = \beta\Lambda = \Lambda^T \Sigma^{-1} \Lambda$ and $Q = \beta S \beta^T$; both are symmetric. L5 at a fixed point says $\Lambda G = S \beta^T$, so $G \Lambda^T = \beta S$ and $G \Lambda^T \beta^T = \beta S \beta^T$, that is $(I - P + Q) P = Q$. This rearranges to $(P - Q)(I - P) = 0$. By the Woodbury identity $I - P = (I + \Lambda^T \Psi^{-1} \Lambda)^{-1}$, which is invertible, so $P = Q$ and $G = I$. Then $\Lambda \beta S = \Lambda G \Lambda^T = \Lambda \Lambda^T$, and L6 gives $\psi_i = S_{ii} - (\Lambda\Lambda^T)_{ii}$. $\square$

**Cost.** Given $S$, one pass costs $O(d^3)$ as written, or $O(d^2 k + k^3)$ with the Woodbury form of $\beta$. The $O(n d^2)$ cost of $S$ is paid once.

### Heywood cases

The maximum of $\ell$ can lie on the boundary $\psi_i = 0$, or an unconstrained method can give $\psi_i < 0$. This is a Heywood case: one feature is then explained entirely by the factors. It happens with small $n$, with too many factors, or when one feature is almost a linear function of the others. Implementations bound $\psi_i$ from below by a small positive number, as the code does, and report the case.

### A worked example: one factor, three features

Take the correlation matrix

$$S = \begin{pmatrix} 1 & 0.72 & 0.63 \\ 0.72 & 1 & 0.56 \\ 0.63 & 0.56 & 1 \end{pmatrix}.$$

With $k = 1$ and $d = 3$ the model has as many free parameters as $S$ has entries, and it fits exactly: the off-diagonal entries give $\lambda_i \lambda_j = S_{ij}$, so $\lambda_1^2 = S_{12} S_{13} / S_{23} = 0.81$, and in the same way $\lambda = (0.9, 0.8, 0.7)$ up to sign and $\psi = 1 - \lambda^2 = (0.19, 0.36, 0.51)$. EM started from $\lambda = (0.5, 0.5, 0.5)$ and $\psi = (0.5, 0.5, 0.5)$, with $n = 100$, gives

| step | $\lambda$ | $\psi$ | $\ell$ |
|---|---|---|---|
| 0 | (0.5, 0.5, 0.5) | (0.5, 0.5, 0.5) | −381.124 |
| 1 | (0.6304, 0.6116, 0.5874) | (0.4075, 0.4422, 0.4854) | −370.491 |
| 2 | (0.7025, 0.6748, 0.6290) | (0.3426, 0.3935, 0.4730) | −366.085 |
| 5 | (0.8061, 0.7616, 0.6717) | (0.2623, 0.3416, 0.4877) | −362.628 |
| 40 | (0.8987, 0.8006, 0.7003) | (0.1921, 0.3587, 0.5094) | −361.878 |

and reaches $\lambda = (0.9, 0.8, 0.7)$, $\psi = (0.19, 0.36, 0.51)$ to four decimals by step 80, where $\ell = -361.878$ equals the saturated value. Note that $\psi_2$ first falls below 0.36 and then rises again: EM moves all parameters together, and $\ell$ grows at every step even when one coordinate does not move monotonically.

### A worked example: rotation

Draw $n = 500$ points from a two-factor model with $d = 6$, loadings $(0.9, 0.8, 0.7)$ on the first factor for features 1 to 3 and $(0.8, 0.7, 0.6)$ on the second factor for features 4 to 6, and unit variances (`random.Random(2026)`). EM with $k = 2$ stops after 84 passes at $\ell = -3720.631$, with $\psi = (0.178, 0.363, 0.489, 0.319, 0.495, 0.568)$; the true values are $(0.19, 0.36, 0.51, 0.36, 0.51, 0.64)$. Rotating the fitted loadings by $45°$ gives

$$\Lambda R_{45} = \begin{pmatrix} 0.696 & -0.603 \\ 0.607 & -0.560 \\ 0.573 & -0.447 \\ -0.468 & -0.662 \\ -0.483 & -0.499 \\ -0.446 & -0.451 \end{pmatrix},$$

with the same $\ell = -3720.631$: every feature now seems to load on both factors. Varimax raises the raw criterion from 0.0176 to 0.1955 and returns

$$\begin{pmatrix} 0.921 & 0.001 \\ 0.826 & -0.025 \\ 0.726 & 0.038 \\ 0.080 & -0.807 \\ -0.038 & -0.693 \\ -0.042 & -0.633 \end{pmatrix},$$

the simple structure of the true model, up to the sign of the second factor.

### Choosing k

The likelihood ratio statistic $-2(\ell(\hat\Lambda, \hat\Psi) - \ell_{\text{saturated}})$ is approximately chi-squared with $((d-k)^2 - (d+k))/2$ degrees of freedom under the model, for large $n$. Information criteria such as BIC, held-out likelihood, the [scree plot](/scree-plot/) and parallel analysis are also used. The [explained variance](/explained-variance/) of PCA is often reported next to the communalities, but the two measure different things.

## References
