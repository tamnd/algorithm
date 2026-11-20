---
tag: BVB5NT
kind: concept
slug: data-fidelity-term
name: Data fidelity term
aliases:
- data discrepancy functional
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: intro
summary: The term of a variational objective that measures misfit to the data, chosen as the negative log likelihood of the noise, such as least squares or Kullback-Leibler.
prereqs: [inverse-problem, maximum-likelihood-estimation]
see_also: [variational-regularization, kullback-leibler-divergence, poisson-distribution, huber-m-estimator, image-noise, maximum-a-posteriori-estimation, mlem-reconstruction, proximal-operator]
sources:
  - paper: doi:10.1017/S0962492918000016
    title: Martin Benning and Martin Burger, Modern regularization methods for inverse problems, Acta Numerica 27, 2018
    locator: pages 1 to 111 (data fidelity terms from noise models and the variational framework)
  - paper: doi:10.1088/0266-5611/25/12/123006
    title: Mario Bertero, Patrizia Boccacci, Gabriele Desidera and Giuseppe Vicidomini, Image deblurring with Poisson data, from cells to galaxies, Inverse Problems 25(12), 2009
    locator: article 123006 (the Kullback-Leibler data term for photon counting and its use in microscopy and astronomy)
  - paper: doi:10.1023/B:JMIV.0000011326.88682.e5
    title: Mila Nikolova, A variational approach to remove outliers and impulse noise, Journal of Mathematical Imaging and Vision 20(1-2), 2004
    locator: pages 99 to 120 (nonsmooth l1 data fidelity and the exact fit of most data entries)
  - paper: doi:10.1137/060671814
    title: Gilles Aubert and Jean-Francois Aujol, A variational approach to removing multiplicative noise, SIAM Journal on Applied Mathematics 68(4), 2008
    locator: pages 925 to 946 (the data term for gamma distributed multiplicative noise)
  - paper: doi:10.1017/S096249291600009X
    title: Antonin Chambolle and Thomas Pock, An introduction to continuous optimization for imaging, Acta Numerica 25, 2016
    locator: pages 161 to 319 (proximal operators of the common data terms)
---

The data fidelity term $\mathcal{D}(Ax, y)$ is the part of a [variational](/variational-regularization/) objective $\mathcal{D}(Ax, y) + \lambda R(x)$ that measures how badly a candidate $x$ explains the data $y$. The standard choice is the negative log likelihood of the noise model: least squares $\tfrac12\|Ax - y\|^2$ for Gaussian noise, the Kullback-Leibler divergence for photon counts, and the $\ell_1$ norm for impulsive noise and outliers. A wrong data term gives a biased or unstable reconstruction even with a good regularizer.

## In plain words

A measured image is a noisy copy of what the instrument would show for the true object. To judge a candidate object, simulate what the instrument would show for it and compare that with the measurement. The data fidelity term is the rule for this comparison. A good rule punishes the errors that the noise rarely makes and forgives the errors that it often makes. If the noise is usually small, large differences must cost a lot. If the noise sometimes makes a few huge errors, a few large differences must not cost too much. If the noise grows with the brightness, bright pixels may differ more than dark ones.

## The idea

**From likelihood to data term.** Let the data have the density $p(y \mid x)$. The [maximum likelihood](/maximum-likelihood-estimation/) estimate maximizes it, and the [maximum a posteriori estimate](/maximum-a-posteriori-estimation/) with prior density proportional to $e^{-\beta R(x)}$ minimizes

$$-\log p(y \mid x) + \beta R(x).$$

So the data term is $\mathcal{D}(Ax, y) = -\log p(y \mid x)$ with the terms that do not depend on $x$ removed. This gives the table below, with $z = Ax$ the predicted data and $b \ge 0$ a known background.

| noise model | data term $\mathcal{D}(z, y)$ | proximal operator of $\tau\mathcal{D}$, per entry |
|---|---|---|
| Gaussian, $\mathcal{N}(0, \sigma^2 I)$ | $\frac{1}{2\sigma^2}\|z - y\|^2$ | $(v + \tau y/\sigma^2)/(1 + \tau/\sigma^2)$ |
| Gaussian, covariance $\Sigma$ | $\tfrac12(z - y)^\top\Sigma^{-1}(z - y)$ | a linear solve |
| Poisson counts | $\sum_i (z + b)_i - y_i\log(z + b)_i$ | $t = \tfrac12\big(v - \tau + \sqrt{(v - \tau)^2 + 4\tau y}\big)$ for $b = 0$ |
| Laplace, impulse noise | $\|z - y\|_1$ | soft thresholding of $v - y$ by $\tau$, then add $y$ |
| Gaussian with outliers | Huber function of $z - y$ | piecewise linear in $v$ |
| Gamma, multiplicative | $\sum_i \log z_i + y_i/z_i$ | root of a cubic |

The Poisson term equals the [Kullback-Leibler divergence](/kullback-leibler-divergence/) $\mathrm{KL}(y, z + b) = \sum_i y_i\log\frac{y_i}{(z + b)_i} - y_i + (z + b)_i$ up to a constant. The KL form is 0 when the prediction equals the data and is positive otherwise, so it is a true measure of misfit. It is defined only for $z + b > 0$ where $y_i > 0$, which adds a positivity constraint to the problem.

**Why the choice matters.** The data term decides which residuals $Ax - y$ are cheap. Least squares makes large residuals very costly, so a single outlier moves the solution far. The $\ell_1$ term grows only linearly, and its minimizers fit most entries exactly and ignore a few (Nikolova 2004). The Poisson term weights each residual by about $1/y_i$, so bright pixels may have larger residuals, as their noise is larger.

**The noise level in the deterministic theory.** In the rz pages of this area the noise is a bound $\|y^\delta - y\| \le \delta$ in the Hilbert norm, and the data term is $\tfrac12\|Ax - y^\delta\|^2$. Other data terms need their own form of $\delta$, for example a bound on $\mathrm{KL}(y^\delta, y)$, and their own convergence theory. The theorems of [variational regularization](/variational-regularization/) for least squares do not transfer without change.

**Convexity and the solver.** Each term in the table except the gamma term is convex in $z$, and so convex in $x$. The gamma term $\log z + y/z$ is convex only for $z < 2y$; Aubert and Aujol (2008) study this model and its nonconvexity. The Gaussian term has a gradient with Lipschitz constant $\|A\|^2/\sigma^2$, so [proximal gradient](/proximal-gradient-method/) steps are possible. The Poisson and $\ell_1$ terms have no Lipschitz gradient, so solvers such as the [Chambolle-Pock algorithm](/chambolle-pock-algorithm/) use their [proximal operator](/proximal-operator/) in the table instead.

## Examples

**Gaussian against Poisson for one count.** Let $y = 4$ counts. The Poisson term in its KL form is $\mathrm{KL}(4, t) = 4\log(4/t) - 4 + t$. The Gaussian term with the same variance $\sigma^2 = 4$ is $(t - 4)^2/8$.

| prediction $t$ | 2 | 4 | 6 |
|---|---|---|---|
| $\mathrm{KL}(4, t)$ | 0.7726 | 0 | 0.3781 |
| $(t - 4)^2/8$ | 0.5 | 0 | 0.5 |

The Gaussian term is symmetric. The Poisson term punishes a prediction that is too low more than one that is too high, and it is infinite at $t = 0$, as a Poisson source with mean 0 cannot give 4 counts.

**The Poisson proximal step.** The proximal operator of $\tau(t - y\log t)$ at $v$ solves $t - v + \tau - \tau y/t = 0$, the quadratic $t^2 + (\tau - v)t - \tau y = 0$. Its positive root is the formula in the table. For $v = 1$, $\tau = 0.5$ and $y = 4$ it is $t = 1.68614$; for $y = 0$ it is $t = 0.5 = v - \tau$, a plain shift.

**An outlier.** Fit one constant $c$ to the data $(1, 2, 3, 100)$, so $A$ is the column of ones. Least squares gives the mean $c = 26.5$, far from three of the four values. The $\ell_1$ term $\sum_i |c - y_i|$ is minimal for every $c$ in $[2, 3]$, the set of medians, and the outlier 100 has no effect on it.

**Salt and pepper noise.** In an image where a few pixels are set to 0 or 255 and the rest are exact, the total variation model with $\ell_1$ data term restores the image and keeps most pixels exactly equal to the data. The model with a squared data term spreads the error of each corrupted pixel over its neighbors.

## Where it is used

- **Least squares**: most deblurring, inpainting, MRI and tomography models, where the noise after many independent events is near Gaussian; the [Tikhonov](/tikhonov-regularization/) and total variation models of this area.
- **Kullback-Leibler**: emission tomography, fluorescence microscopy and astronomy at low counts (Bertero et al. 2009); without a regularizer its minimization is the [MLEM](/mlem-reconstruction/) iteration.
- **$\ell_1$ and Huber**: impulse noise, dead pixels, and data with a few corrupt detector entries; the [Huber estimator](/huber-m-estimator/) is the robust statistics form.
- **Multiplicative terms**: speckle in synthetic aperture radar and ultrasound, often handled through a log transform.
- **Mixed Poisson and Gaussian**: camera images at low light, where photon noise and read noise are both present; see [image noise](/image-noise/) for the models.

## References
