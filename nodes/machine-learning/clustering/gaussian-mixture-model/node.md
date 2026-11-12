---
tag: 4RQ4DM
kind: model
slug: gaussian-mixture-model
name: Gaussian mixture model
aliases:
- GMM
- mixture of Gaussians
- finite Gaussian mixture
- normal mixture model
area: machine-learning/clustering
level: core
summary: Probabilistic clustering model in which the data come from a mixture of Gaussian components.
prereqs: [maximum-likelihood-estimation, covariance-matrix, hard-and-soft-clustering]
see_also: [expectation-maximization, k-means, k-means-problem, fuzzy-c-means, hidden-markov-model, probabilistic-pca, dirichlet-process, quadratic-discriminant-analysis]
sources:
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: "Section 9.2 (mixtures of Gaussians, with 9.2.1 on the singularities of the likelihood and 9.2.2 on EM for Gaussian mixtures) and Section 9.3.2 (relation to K-means)"
  - paper: "A. P. Dempster, N. M. Laird and D. B. Rubin, Maximum likelihood from incomplete data via the EM algorithm, Journal of the Royal Statistical Society, Series B 39(1):1-38, 1977"
    title: Dempster, Laird and Rubin 1977
    locator: the EM algorithm, its monotonicity, and finite mixtures as an example
  - book: isbn:9780471006268
    title: Geoffrey McLachlan and David Peel, Finite Mixture Models, Wiley, 2000
    locator: "Chapters 1 to 3 (mixture models, identifiability, ML fitting by EM) and Chapter 6 (choice of the number of components)"
  - paper: "H. Teicher, Identifiability of finite mixtures, Annals of Mathematical Statistics 34(4):1265-1269, 1963"
    title: Teicher 1963
    locator: identifiability of finite mixtures of one-dimensional normal distributions
  - paper: "S. J. Yakowitz and J. D. Spragins, On the identifiability of finite mixtures, Annals of Mathematical Statistics 39(1):209-214, 1968"
    title: Yakowitz and Spragins 1968
    locator: finite mixtures of multivariate normal distributions are identifiable
  - paper: "N. E. Day, Estimating the components of a mixture of normal distributions, Biometrika 56(3):463-474, 1969"
    title: Day 1969
    locator: the likelihood of a normal mixture is unbounded; EM-like iteration for two components
  - paper: "R. J. Hathaway, A constrained formulation of maximum-likelihood estimation for normal mixture distributions, Annals of Statistics 13(2):795-800, 1985"
    title: Hathaway 1985
    locator: constraints on the ratios of the variances give a bounded likelihood and a consistent estimator
  - paper: "G. Schwarz, Estimating the dimension of a model, Annals of Statistics 6(2):461-464, 1978"
    title: Schwarz 1978
    locator: the Bayesian information criterion
  - paper: "C. Fraley and A. E. Raftery, Model-based clustering, discriminant analysis, and density estimation, Journal of the American Statistical Association 97(458):611-631, 2002"
    title: Fraley and Raftery 2002
    locator: covariance structures by eigenvalue decomposition and the choice of the model and of k by BIC
  - paper: "C. Fraley and A. E. Raftery, Bayesian regularization for normal mixture estimation and model-based clustering, Journal of Classification 24:155-181, 2007"
    title: Fraley and Raftery 2007
    locator: a conjugate prior that avoids degenerate covariances, with BIC on the MAP fit
  - paper: "S. Dasgupta, Learning mixtures of Gaussians, Proceedings of FOCS 1999"
    title: Dasgupta 1999
    locator: a provable algorithm for well-separated Gaussian mixtures
  - paper: "A. Moitra and G. Valiant, Settling the polynomial learnability of mixtures of Gaussians, Proceedings of FOCS 2010"
    title: Moitra and Valiant 2010
    locator: polynomial learnability for a fixed number of components and a sample lower bound exponential in k
---

A Gaussian mixture model (GMM) says that each data point comes from one of $k$ Gaussian distributions, chosen at random with fixed weights, and that the label of the chosen component is hidden. Its parameters are the weights $\pi_j$, the means $\mu_j$ and the [covariance matrices](/covariance-matrix/) $\Sigma_j$. A fitted model gives each point a posterior probability of each component, which makes it the standard model for [soft clustering](/hard-and-soft-clustering/). The parameters are usually fitted by [maximum likelihood](/maximum-likelihood-estimation/) with the [EM algorithm](/expectation-maximization/), and [k-means](/k-means/) is the limit of this fit when all components share a spherical covariance that shrinks to zero.

## The machine

A GMM with $k$ components in $\mathbb{R}^d$ has the parameters $\theta = (\pi_1, \ldots, \pi_k, \mu_1, \ldots, \mu_k, \Sigma_1, \ldots, \Sigma_k)$, where $\pi_j > 0$, $\sum_j \pi_j = 1$, $\mu_j \in \mathbb{R}^d$ and each $\Sigma_j$ is a symmetric positive definite $d \times d$ matrix. It generates a point in two steps:

1. Draw a hidden label $z \in \{1, \ldots, k\}$ with $\Pr[z = j] = \pi_j$.
2. Draw $x$ from the normal distribution $\mathcal{N}(\mu_z, \Sigma_z)$.

So the density of $x$ is the mixture

$$p(x \mid \theta) = \sum_{j=1}^{k} \pi_j \, \mathcal{N}(x \mid \mu_j, \Sigma_j), \qquad \mathcal{N}(x \mid \mu, \Sigma) = \frac{\exp\big(-\tfrac12 (x - \mu)^\top \Sigma^{-1} (x - \mu)\big)}{(2\pi)^{d/2} \det(\Sigma)^{1/2}}.$$

The data are $n$ independent draws $x_1, \ldots, x_n$. The labels $z_i$ are not seen. The log likelihood is

$$\ell(\theta) = \sum_{i=1}^{n} \log \sum_{j=1}^{k} \pi_j \, \mathcal{N}(x_i \mid \mu_j, \Sigma_j).$$

By Bayes' rule, the posterior probability that $x_i$ came from component $j$ is the responsibility

$$r_{ij} = \Pr[z_i = j \mid x_i, \theta] = \frac{\pi_j \, \mathcal{N}(x_i \mid \mu_j, \Sigma_j)}{\sum_{l=1}^{k} \pi_l \, \mathcal{N}(x_i \mid \mu_l, \Sigma_l)}.$$

The rows $(r_{i1}, \ldots, r_{ik})$ are a soft clustering. A hard clustering gives $x_i$ the label $\arg\max_j r_{ij}$.

The covariance matrices can be restricted. A full matrix has $d(d+1)/2$ free entries, a diagonal one $d$, and a spherical one $\sigma_j^2 I$ only one. In a tied model all components share one $\Sigma$. Fraley and Raftery (2002) write $\Sigma_j = \lambda_j D_j A_j D_j^\top$ (volume, orientation, shape) and constrain each factor to get a family of models.

## What it counts

The model assigns a number to a data set and a parameter value: the log likelihood $\ell(\theta)$. Fitting means to find a $\theta$ with a large $\ell(\theta)$, possibly with a penalty. The other quantities are derived from the fit:

- **Responsibilities.** The $n \times k$ matrix $r_{ij}$, the soft labels of the points.
- **Density.** $p(x \mid \theta)$ for a new point, which is used for density estimation and for anomaly detection, where a low density marks an outlier.
- **Model size.** With full covariances the number of free parameters is
  $$p = (k - 1) + k d + k \frac{d (d + 1)}{2},$$
  for the weights, the means and the covariances. For $d = 2$ and $k = 2$ this is $1 + 4 + 6 = 11$.
- **Bayesian information criterion.** $\mathrm{BIC} = -2 \ell(\hat\theta) + p \ln n$ (Schwarz 1978) trades the fit against the number of parameters. A smaller value is better. It is the usual way to choose $k$ and the covariance structure.

One evaluation of $\ell(\theta)$ costs $O(k d^3)$ for the [Cholesky factors](/cholesky-decomposition/) of the $\Sigma_j$ and then $O(n k d^2)$ for the quadratic forms. In floating point, compute $\log \sum_j$ with the log-sum-exp trick, since the densities underflow for points far from all means.

## Relation to other models

- **k-means.** Fix $\pi_j = 1/k$ and $\Sigma_j = \varepsilon I$ for all $j$. Then
  $$r_{ij} = \frac{\exp(-\|x_i - \mu_j\|^2 / 2 \varepsilon)}{\sum_l \exp(-\|x_i - \mu_l\|^2 / 2 \varepsilon)}.$$
  As $\varepsilon \to 0$, the term with the smallest $\|x_i - \mu_l\|^2$ dominates, so $r_{ij} \to 1$ for the nearest mean and $r_{ij} \to 0$ for the others (if the nearest mean is unique). The M step for the means is then the mean of the points nearest to $\mu_j$. So EM becomes Lloyd's algorithm for the [k-means problem](/k-means-problem/), and $-2\varepsilon$ times the expected complete-data log likelihood tends to the k-means objective (Bishop, Section 9.3.2).
- **Fuzzy c-means.** [Fuzzy c-means](/fuzzy-c-means/) also gives soft memberships, but they come from a fuzzifier and not from a probability model. A GMM gives memberships that are posterior probabilities.
- **Hidden Markov model.** A [hidden Markov model](/hidden-markov-model/) with Gaussian emissions is a GMM whose hidden labels form a Markov chain instead of independent draws. With an initial distribution and transition rows that all equal $(\pi_1, \ldots, \pi_k)$, the labels are independent and the model is exactly a GMM.
- **Supervised counterpart.** When the labels are seen, the same model is [quadratic discriminant analysis](/quadratic-discriminant-analysis/), and the maximum likelihood fit is closed form: the class frequencies, means and covariances.
- **Low-rank components.** Mixtures of [probabilistic PCA](/probabilistic-pca/) or of [factor analysis](/factor-analysis/) models restrict each $\Sigma_j$ to a low-rank part plus a diagonal, which helps in high dimension.
- **Infinite mixtures.** A [Dirichlet process](/dirichlet-process/) mixture of Gaussians lets the number of components grow with the data.

## Known results in the model

### Identifiability only up to labels

The parameters are never unique: if $\sigma$ is a permutation of $\{1, \ldots, k\}$, then $(\pi_{\sigma(j)}, \mu_{\sigma(j)}, \Sigma_{\sigma(j)})_j$ gives the same density, since the sum over $j$ does not depend on the order of its terms. So each local maximum of $\ell$ appears $k!$ times, and two fits can only be compared after the labels are matched, for example with the [Hungarian algorithm](/hungarian-algorithm/). Teicher (1963) for one dimension and Yakowitz and Spragins (1968) for several showed that this is the only freedom: if two mixtures of distinct normal components with positive weights have the same density, then they have the same number of components and the same components and weights, up to a permutation of the labels.

### The likelihood is unbounded

Day (1969) observed that maximum likelihood for normal mixtures is not well posed without a restriction. Take $k \ge 2$ and set $\mu_1 = x_1$ and $\Sigma_1 = s I$, and keep the other components fixed with positive weights. Each term of $\ell$ is at least the log of one of its summands. For $i = 1$ use $j = 1$: $\log(\pi_1 \mathcal{N}(x_1 \mid x_1, s I)) = \log \pi_1 - \frac{d}{2} \log(2 \pi s)$, which tends to $+\infty$ as $s \to 0$. For $i \ge 2$ use $j = 2$, which gives a term that does not depend on $s$. So $\ell \to +\infty$, and no global maximum exists. For the five points $0, 1, 2, 3, 10$, with $\mu_1 = 10$, $\Sigma_1 = s$, $\mu_2 = 1.5$, $\Sigma_2 = 1.25$ and equal weights, $\ell$ grows by $\frac12 \ln 10 \approx 1.15$ for each factor 10 in $s$ once $s$ is small.

EM can run into such a singularity when a component gets only one point, or several equal points. The usual remedies are:

- **Regularization.** Maximize $\ell(\theta) - \frac{\lambda}{2} \sum_j \operatorname{tr}(\Sigma_j^{-1})$ with $\lambda > 0$. The penalty tends to $-\infty$ faster than $-\frac12 \log \det \Sigma_j$ tends to $+\infty$, so the objective is bounded above. The M step becomes $\Sigma_j = (S_j + \lambda I)/N_j$ (below), which is also the common practice of adding a small multiple of $I$ to each covariance. A conjugate prior gives a similar MAP estimate (Fraley and Raftery 2007).
- **Constraints.** Hathaway (1985) bounded the ratios of the eigenvalues of the $\Sigma_j$ from below. Then the constrained maximum exists and is a consistent estimator.
- **Tied or spherical covariances** with a lower bound on the variance.
- **Restarts.** Discard a run in which a component collapses, and start again.

### Fitting by EM

EM (Dempster, Laird and Rubin 1977) alternates two steps. The E step computes the responsibilities $r_{ij}$ for the current $\theta$. The M step maximizes the expected complete-data log likelihood

$$Q(\theta) = \sum_{i=1}^{n} \sum_{j=1}^{k} r_{ij} \big(\log \pi_j + \log \mathcal{N}(x_i \mid \mu_j, \Sigma_j)\big).$$

With $N_j = \sum_i r_{ij}$, a [Lagrange multiplier](/lagrange-multiplier/) for $\sum_j \pi_j = 1$ gives $\pi_j = N_j / n$. For each fixed $\Sigma_j$ the best $\mu_j$ is the weighted mean $\sum_i r_{ij} x_i / N_j$. With $S_j = \sum_i r_{ij} (x_i - \mu_j)(x_i - \mu_j)^\top$, the terms with $\Sigma_j$ are $-\frac{N_j}{2} \log \det \Sigma_j - \frac12 \operatorname{tr}(\Sigma_j^{-1} S_j)$, which have the maximizer $\Sigma_j = S_j / N_j$ when $S_j$ is positive definite. With the penalty, $S_j$ becomes $S_j + \lambda I$.

```pseudo id=main
EM-GMM(x[1..n], k, λ, ε)
L1  π_j ← 1/k; μ_j ← k distinct data points; Σ_j ← the covariance of all the data
L2  repeat
L3      E step: r_ij ← π_j N(x_i | μ_j, Σ_j) / Σ_l π_l N(x_i | μ_l, Σ_l) for all i, j (in log space)
L4      M step: N_j ← Σ_i r_ij; π_j ← N_j / n
L5          μ_j ← Σ_i r_ij x_i / N_j
L6          Σ_j ← (Σ_i r_ij (x_i − μ_j)(x_i − μ_j)^T + λ I) / N_j
L7  until the penalized log likelihood grew by less than ε (relative)
L8  return π, μ, Σ and the responsibilities r
```

**EM never decreases the objective.** For any $r_i$ on the simplex, [Jensen's inequality](/jensens-inequality/) for the concave $\log$ gives

$$\log \sum_j \pi_j \mathcal{N}(x_i \mid \mu_j, \Sigma_j) \ge \sum_j r_{ij} \log \frac{\pi_j \mathcal{N}(x_i \mid \mu_j, \Sigma_j)}{r_{ij}},$$

with equality when $r_{ij}$ is the posterior under the same $\theta$. Add over $i$ and call the right side $F(r, \theta)$; it is $Q(\theta)$ plus a term that depends only on $r$. Let $r^{(t)}$ be the posterior under $\theta^{(t)}$. Then $\ell(\theta^{(t+1)}) \ge F(r^{(t)}, \theta^{(t+1)}) \ge F(r^{(t)}, \theta^{(t)}) = \ell(\theta^{(t)})$, where the middle step holds because the M step maximizes $F(r^{(t)}, \cdot)$. The penalty depends only on $\theta$, so the same chain holds for the penalized objective. The values converge when they are bounded above, which the penalty ensures. Like every local method, EM can stop at a local maximum or a saddle point, and the result depends on the start; k-means or [k-means++](/k-means-plus-plus/) seeds are common.

A pass costs $O(n k d^2 + k d^3)$ time with full covariances and $O(n k d)$ with diagonal ones, and $O(n k + k d^2)$ space.

### A worked step

Take the five points $1, 2, 4, 7, 8$ on the line, $k = 2$, and start from $\pi = (0.5, 0.5)$, $\mu = (2, 6)$, $\sigma^2 = (1, 4)$, with $\lambda = 0$. The log likelihood is $\ell \approx -11.2948$. The E step gives these responsibilities of component 1:

| $x_i$ | 1 | 2 | 4 | 7 | 8 |
|---|---|---|---|---|---|
| $r_{i1}$ | 0.9650 | 0.9366 | 0.3086 | 0.0000 | 0.0000 |

For the point 4: $0.5\,\mathcal{N}(4 \mid 2, 1) \approx 0.02700$ and $0.5\,\mathcal{N}(4 \mid 6, 4) \approx 0.06049$, so $r_{31} \approx 0.02700 / 0.08749 \approx 0.3086$. The M step gives $\pi \approx (0.4420, 0.5580)$, $\mu \approx (1.8426, 6.4261)$ and $\sigma^2 \approx (0.9704, 3.2788)$, and $\ell$ rises to about $-11.1064$. The next values of $\ell$ are about $-11.0645$, $-11.0058$ and $-10.8426$. The point 4 moves to component 2, and after 16 passes EM stops at $\pi \approx (0.390, 0.610)$, $\mu \approx (1.492, 6.261)$, $\sigma^2 \approx (0.250, 3.168)$ with $\ell \approx -10.6246$.

With $k = 3$ and $\lambda = 0$, EM on these five points drives one variance to zero, the singularity above. With $\lambda > 0$ it stays bounded.

### Choosing k

$\ell(\hat\theta)$ grows with $k$, so it cannot choose $k$ alone. BIC adds $p \ln n$, with $p$ from the formula above, and Fraley and Raftery (2002) choose both $k$ and the covariance structure by the least BIC. On the five points above, BIC is about $27.44$ for $k = 1$ and $29.30$ for $k = 2$, so it prefers one component for so little data. The likelihood is unbounded, so BIC must use a regularized or constrained fit. Other choices are AIC, the integrated completed likelihood, and cross-validated likelihood.

### Learning with guarantees

EM has no general guarantee of finding the global maximum. Dasgupta (1999) gave the first provable algorithm for mixtures whose means are far apart. Moitra and Valiant (2010) showed that for each fixed $k$ the parameters can be learned to a given accuracy with a number of samples and a running time polynomial in the dimension and in the inverse of the accuracy, and that the number of samples must grow exponentially in $k$ in general.

## References
