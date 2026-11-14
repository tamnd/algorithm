---
tag: 677AW6
kind: problem
slug: kde-bandwidth-selection
name: Bandwidth selection
aliases:
- Silverman's rule of thumb
- smoothing parameter selection
area: statistics-and-inference/nonparametric-and-robust-statistics
level: core
summary: Choose the bandwidth of a kernel estimator, by a rule of thumb, by cross-validation or by plug-in estimates of the integrated squared error.
prereqs: [kernel-density-estimation, cross-validation, mean-squared-error, bias-variance-tradeoff]
see_also: [nadaraya-watson-estimator, local-polynomial-regression, smoothing-spline, golden-section-search, quantile, kullback-leibler-divergence, fast-fourier-transform, akaike-information-criterion]
sources:
  - book: isbn:9780412246203
    title: B. W. Silverman, Density Estimation for Statistics and Data Analysis, Chapman and Hall, 1986
    locator: Section 3.4 (the normal reference bandwidth 1.06 sigma n^(-1/5), the robust version with the interquartile range, and least squares and likelihood cross-validation)
  - book: isbn:9780412552700
    title: M. P. Wand and M. C. Jones, Kernel Smoothing, Chapman and Hall, 1995
    locator: Chapter 3 (bandwidth selection; the estimation of psi_r in Section 3.5 and the two-stage direct plug-in in Section 3.6.1)
  - paper: "Mats Rudemo, Empirical choice of histograms and kernel density estimators, Scandinavian Journal of Statistics 9(2), 1982, pp. 65 to 78"
    locator: The whole paper (least squares cross-validation)
  - paper: doi:10.1093/biomet/71.2.353
    title: Adrian W. Bowman, An alternative method of cross-validation for the smoothing of density estimates, Biometrika 71(2), 1984
    locator: pp. 353 to 360 (least squares cross-validation)
  - paper: doi:10.1214/aos/1176346792
    title: Charles J. Stone, An asymptotically optimal window selection rule for kernel density estimates, The Annals of Statistics 12(4), 1984
    locator: pp. 1285 to 1297 (the integrated squared error at the cross-validated bandwidth is asymptotically optimal)
  - paper: doi:10.1007/BF00363516
    title: Peter Hall and J. S. Marron, Extent to which least-squares cross-validation minimises integrated square error in nonparametric density estimation, Probability Theory and Related Fields 74(4), 1987
    locator: pp. 567 to 581 (the relative error of the cross-validated bandwidth is of order n^(-1/10))
  - paper: doi:10.1111/j.2517-6161.1991.tb01857.x
    title: S. J. Sheather and M. C. Jones, A reliable data-based bandwidth selection method for kernel density estimation, Journal of the Royal Statistical Society Series B 53(3), 1991
    locator: pp. 683 to 690 (the solve-the-equation plug-in selector and its relative rate n^(-5/14))
  - paper: doi:10.1214/aos/1176348653
    title: J. S. Marron and M. P. Wand, Exact mean integrated squared error, The Annals of Statistics 20(2), 1992
    locator: pp. 712 to 736 (the exact MISE for normal mixtures with a Gaussian kernel)
  - paper: doi:10.1080/01621459.1996.10476701
    title: M. C. Jones, J. S. Marron and S. J. Sheather, A brief survey of bandwidth selection for density estimation, Journal of the American Statistical Association 91(433), 1996
    locator: pp. 401 to 407 (comparison of rules, cross-validation and plug-in selectors)
---

Bandwidth selection is the problem of choosing, from the data alone, the bandwidth $h$ of a [kernel density estimate](/kernel-density-estimation/) or another kernel smoother. The bandwidth sets the balance between bias and variance, and it changes the estimate much more than the choice of kernel does. The target is the $h$ that makes the integrated squared error small, but that error depends on the unknown density. So every method replaces it by something it can compute: the error at a normal density with the same scale (a rule of thumb), an unbiased estimate of the error from the sample (cross-validation), or the asymptotic formula with the unknown functional estimated from the data (plug-in).

## In plain words

A kernel density estimate puts a bump on every data point, and the bandwidth is the width of the bumps. Too narrow, and the curve shows a peak at every point. Too wide, and two real groups melt into one. We want the width that makes the estimate closest to the true curve, but we do not know the true curve.

There are three common ways out. Pretend the data are bell shaped and use the best width for a bell curve. Or leave out each point in turn, and see how well the estimate made from the other points predicts it. Or use the formula for the best width, which needs the curvature of the true curve, and estimate that curvature from the data. The first is quick but can smooth too much. The second follows the data but is noisy. The third is a good default.

## Definition

The input is a sample $X_1, \ldots, X_n$ from an unknown density $f$ on $\mathbb{R}$ and a kernel $K$. For each $h > 0$ let $\hat f_h(x) = (nh)^{-1}\sum_i K((x - X_i)/h)$. The loss of $h$ is the integrated squared error, and its mean is the MISE:
$$\mathrm{ISE}(h) = \int (\hat f_h - f)^2, \qquad \mathrm{MISE}(h) = \mathbb{E}\,\mathrm{ISE}(h).$$
A bandwidth selector is a function $\hat h = \hat h(X_1, \ldots, X_n)$. Its targets are $h_{\mathrm{ISE}}$, the minimizer of the ISE for the sample at hand, and $h_{\mathrm{MISE}}$, the minimizer of the MISE. A selector is judged by its relative error $\hat h/h_{\mathrm{MISE}} - 1$, and the usual measure is the power $\alpha$ for which this error is of order $n^{-\alpha}$.

For a kernel with $\int K = 1$, $\mu_2 = \int u^2 K$ and $R(K) = \int K^2$, and a density with a smooth second derivative, the asymptotic MISE is minimized at
$$h_{\mathrm{AMISE}} = \left(\frac{R(K)}{\mu_2^2\, R(f'')\, n}\right)^{1/5}, \qquad R(f'') = \int f''(x)^2\,dx = \psi_4,$$
where $\psi_r = \int f^{(r)} f = \mathbb{E}\,f^{(r)}(X)$; the last identity for $\psi_4$ is integration by parts twice. The proof is on the [kernel density estimation](/kernel-density-estimation/) page. The only unknown is $R(f'')$, the total curvature of $f$.

## Variants

- **Target.** Minimize the ISE of the sample, the MISE, or the asymptotic MISE. They agree to first order but differ for small samples, and $h_{\mathrm{ISE}}$ itself varies from sample to sample with relative error of order $n^{-1/10}$.
- **Other losses.** The integrated absolute error, or the Kullback-Leibler loss, which likelihood cross-validation targets. They lead to different bandwidths, especially in the tails.
- **Several dimensions.** A bandwidth matrix $H$ in place of $h$. A diagonal $H$ has $d$ parameters and a full one has $d(d+1)/2$; the normal reference rule becomes $H = (4/((d+2)n))^{2/(d+4)}\hat\Sigma$.
- **Local and adaptive bandwidths.** A bandwidth $h(x)$ that changes along the line, or one $h_i$ for each data point.
- **Regression.** For the [Nadaraya-Watson estimator](/nadaraya-watson-estimator/) and [local polynomial regression](/local-polynomial-regression/), the loss is the squared error of the fitted mean, and leave-one-out prediction error is the cross-validation criterion.

## Examples

Fourteen points in two groups:
$$-1.9,\ -1.6,\ -1.5,\ -1.3,\ -1.2,\ -1.0,\ -0.8,\ 0.9,\ 1.1,\ 1.2,\ 1.4,\ 1.5,\ 1.7,\ 2.0.$$
The sample standard deviation is $s = 1.4606$. The quartiles, by linear interpolation at position $(n-1)p$, are $-1.275$ and $1.35$, so the interquartile range is $2.625$. With the Gaussian kernel, the selectors of the code on this page give:

| selector | formula | $h$ | estimate at the dip $x = 0$ | highest value |
|---|---|---|---|---|
| normal reference | $(4/(3n))^{1/5} s$ | 0.913 | 0.155 | 0.208 |
| Silverman (1986), robust | $0.9 \min(s, \mathrm{IQR}/1.34)\, n^{-1/5}$ | 0.775 | 0.130 | 0.235 |
| least squares cross-validation | minimizer of LSCV | 0.464 | 0.040 | 0.338 |
| two-stage direct plug-in | $(R(K)/(\hat\psi_4 n))^{1/5}$ | 0.537 | 0.063 | 0.309 |

All four estimates have two modes, near $-1.3$ and $1.35$. The two rules smooth much more, because a sample with two well separated groups has a large standard deviation but a small spread within each group. Here $\mathrm{IQR}/1.34 = 1.959 > s$, so the robust rule uses $s$ and differs from the normal reference only by its factor 0.9. The LSCV criterion, as a function of $h$:

| $h$ | 0.1 | 0.2 | 0.3 | 0.4 | 0.6 | 0.8 | 1.0 |
|---|---|---|---|---|---|---|---|
| LSCV($h$) | 0.0916 | −0.1364 | −0.2199 | −0.2479 | −0.2410 | −0.2099 | −0.1840 |

It is flat near its minimum: values of $h$ from 0.4 to 0.6 differ by less than 0.01. This flatness is the reason the cross-validated bandwidth varies so much between samples.

**Measured behaviour on simulated data.** These are measurements with the code of this page, not theorems. The reference $h_{\mathrm{MISE}}$ is computed from the exact MISE formula of Marron and Wand (1992).

| data | $n$ | $h_{\mathrm{MISE}}$ | normal reference | robust 0.9 rule | LSCV | plug-in |
|---|---|---|---|---|---|---|
| $N(0, 1)$, 30 samples | 100 | 0.446 | 0.94 (0.80 to 1.09) | 0.77 (0.53 to 0.91) | 0.94 (0.27 to 1.48) | 0.92 (0.59 to 1.21) |
| $N(0, 1)$, 30 samples | 400 | 0.330 | 0.96 (0.91 to 1.02) | 0.80 (0.76 to 0.87) | 0.97 (0.36 to 1.23) | 0.95 (0.74 to 1.06) |

The entries are the mean of $\hat h/h_{\mathrm{MISE}}$, with the smallest and largest value in brackets. For normal data the normal reference rule is close to the target and has the least spread. LSCV is nearly unbiased but very variable. For the separated bimodal mixture $\frac12 N(-1.5, 0.5^2) + \frac12 N(1.5, 0.5^2)$ with $n = 200$ (10 samples), $h_{\mathrm{MISE}} = 0.224$. The mean selected bandwidths were 0.579 (normal reference), 0.492 (robust rule), 0.220 (LSCV) and 0.259 (plug-in), and the MISE at the selected bandwidth was on average 4.97, 3.41, 1.12 and 1.05 times the smallest MISE. The rules oversmooth badly when the density is far from normal.

## Known algorithms

- **Normal reference rule.** Put the normal value $R(f'') = 3/(8\sqrt\pi\,\sigma^5)$ into $h_{\mathrm{AMISE}}$. For the Gaussian kernel this gives $h = (4/(3n))^{1/5}\hat\sigma \approx 1.06\,\hat\sigma n^{-1/5}$. Silverman (1986) suggests $0.9 \min(\hat\sigma, \mathrm{IQR}/1.34)\,n^{-1/5}$: the interquartile range of a normal density is $1.349\sigma$, so the minimum protects against heavy tails and outliers, and the factor 0.9 instead of 1.06 protects a little against bimodality. Cost $O(n)$, with the quartiles by [selection](/quantile/) or $O(n \log n)$ by sorting. The code checks both formulas.
- **Least squares cross-validation (LSCV).** Since $\mathrm{ISE}(h) = R(\hat f_h) - 2\int \hat f_h f + R(f)$ and the last term does not depend on $h$, minimize
  $$\mathrm{LSCV}(h) = R(\hat f_h) - \frac2n\sum_{i=1}^n \hat f_{h,-i}(X_i),$$
  where $\hat f_{h,-i}$ leaves out $X_i$. With the Gaussian kernel, $\phi_h * \phi_h = \phi_{h\sqrt2}$ gives the closed form $R(\hat f_h) = n^{-2}\sum_{i,j}\phi_{h\sqrt2}(X_i - X_j)$. Each value costs $O(n^2)$, or $O(n + m\log m)$ with binning on $m$ grid points. LSCV can have several local minima, so the code evaluates it on a log-spaced grid and then refines the best grid point by [golden section search](/golden-section-search/). The tests compare the closed form with numerical integration of $\hat f_h^2$ and explicit leave-one-out sums.
- **Plug-in.** Estimate $\psi_4 = R(f'')$ by the kernel estimate $\hat\psi_r(g) = n^{-2}\sum_{i,j} L_g^{(r)}(X_i - X_j)$ with a pilot bandwidth $g$. The best $g$ for $\hat\psi_4$ depends on $\psi_6$, whose best pilot depends on $\psi_8$, and so on. The two-stage direct plug-in of Wand and Jones stops this chain with a normal value for $\psi_8$, then estimates $\psi_6$ and $\psi_4$ in turn, each with its asymptotically optimal pilot $g = (2L^{(r)}(0)/(-\mu_2\psi_{r+2} n))^{1/(r+3)}$, and returns $h = (R(K)/(\mu_2^2\hat\psi_4 n))^{1/5}$. The code uses the Gaussian kernel for $L$ and $\min(\hat\sigma, \mathrm{IQR}/1.349)$ for the normal scale. The tests check $\hat\psi_r$ against the identity $\hat\psi_r(g) = (-1)^{r/2}\int (\hat f_{g/\sqrt2}^{(r/2)})^2$, computed by quadrature. Cost $O(n^2)$, or $O(n + m \log m)$ binned.
- **Solve-the-equation plug-in (Sheather and Jones 1991).** Make the pilot bandwidth for $\psi_4$ a function of $h$ itself, $g = \gamma(h)$, through the ratio of the two optimal bandwidths, and solve $h = (R(K)/(\mu_2^2\hat\psi_4(\gamma(h))\,n))^{1/5}$ by a root finder. This is the most widely recommended general selector.
- **Biased cross-validation and smoothed cross-validation.** Variants of LSCV that estimate $R(f'')$ inside the cross-validation criterion, or smooth the criterion. They trade some bias for much less variance.
- **Likelihood cross-validation.** Maximize $\sum_i \log \hat f_{h,-i}(X_i)$. It targets the Kullback-Leibler loss and breaks down for heavy tails, where one isolated point forces a large $h$.

## Bounds

- **LSCV is unbiased up to a constant.** $\mathbb{E}\,\mathrm{LSCV}(h) = \mathrm{MISE}(h) - R(f)$, exactly, for every $n$ and $h$. Proof: $\hat f_{h,-i}(X_i)$ is an estimate from $n - 1$ points, which are independent of $X_i$, so $\mathbb{E}\,\hat f_{h,-i}(X_i) = \int \mathbb{E}[\hat f_{h,n-1}(x)]\,f(x)\,dx = \int (K_h * f) f$, and the mean of a kernel estimate does not depend on the sample size. So $\mathbb{E}\,\mathrm{LSCV}(h) = \mathbb{E}\,R(\hat f_h) - 2\,\mathbb{E}\int \hat f_h f = \mathrm{MISE}(h) - R(f)$.
- **Rates of the selectors.** Stone (1984) proved that LSCV is asymptotically optimal: $\mathrm{ISE}(\hat h)/\min_h \mathrm{ISE}(h) \to 1$ almost surely. Hall and Marron (1987) showed that its relative error is of order $n^{-1/10}$, which is very slow. The Sheather-Jones plug-in has relative error of order $n^{-5/14}$. These rates are cited, not proved here.
- **Rules are not consistent for the target.** The normal reference bandwidth converges to the right value only if $f$ is normal. For other densities, $\hat h/h_{\mathrm{AMISE}}$ converges to $(R(f'')/R(\phi_\sigma''))^{1/5}$, which is different from 1, and for densities with several modes it is larger than 1: the rule oversmooths.
- **Upper bound in practice.** Over all densities with a given variance $\sigma^2$, the largest AMISE-optimal bandwidth is $3(R(K)/(35\mu_2^2 n))^{1/5}\sigma$, which is $1.144\,\sigma n^{-1/5}$ for the Gaussian kernel, only 8 percent above the normal reference value (Terrell's maximal smoothing principle, 1990). So the normal reference bandwidth is a sensible upper end of a range of bandwidths to look at.
- **Cost.** Rules cost $O(n)$. Cross-validation and plug-in cost $O(n^2)$ for each evaluation exactly, or $O(n + m\log m)$ with binning.

## Reductions

- **Plug-in reduces to estimating a functional.** Bandwidth selection by plug-in is the estimation of $R(f'') = \psi_4$, the integrated squared second derivative. That problem has its own bandwidth, which is why the method has stages.
- **Cross-validation reduces to model selection.** LSCV is leave-one-out [cross-validation](/cross-validation/) with the loss $\int \hat f^2 - 2\hat f(X)$, an unbiased estimate of the MISE up to a constant. Likelihood cross-validation is the same with the log loss, the density version of model selection by [Kullback-Leibler divergence](/kullback-leibler-divergence/) or the [AIC](/akaike-information-criterion/).
- **Histograms.** Choosing the bin width of a histogram is the same problem with a different bias: the best width is of order $n^{-1/3}$, and rules such as $2\,\mathrm{IQR}\,n^{-1/3}$ (Freedman and Diaconis) come from the same normal reference idea.
- **Smoothing in regression.** The smoothing parameter of a [smoothing spline](/smoothing-spline/), the span of LOESS and the bandwidth of kernel regression are chosen by the same tools: cross-validation, generalized cross-validation and plug-in.

## Applications

- **Default plots.** Every density plot in statistical software needs a bandwidth without user input. R's `density` uses the robust 0.9 rule by default and offers the Sheather-Jones selector.
- **Exploratory analysis.** Use several bandwidths, such as the rule, the plug-in and half of the rule, to decide whether a second mode is real.
- **Smoothing in other methods.** [Mean shift](/mean-shift/) clustering, kernel classifiers and density ratio estimates depend on the bandwidth in the same way, and use the same selectors.
- **Nonparametric regression.** The bandwidth of a [Nadaraya-Watson estimator](/nadaraya-watson-estimator/) or a local linear fit is chosen by leave-one-out prediction error or by a plug-in for the regression AMISE.

## References
