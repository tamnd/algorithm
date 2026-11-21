---
tag: 1TPE50
kind: model
slug: emission-tomography-model
name: Emission tomography model
aliases:
- Poisson model for PET and SPECT
area: imaging-and-inverse-problems/tomographic-reconstruction
level: core
summary: Model the counts of each detector bin as independent Poisson variables whose means are weighted line sums of the unknown activity map plus a known background.
prereqs: [poisson-distribution, radon-transform, maximum-likelihood-estimation]
see_also: [mlem-reconstruction, attenuated-radon-transform, beer-lambert-law, linear-gaussian-inverse-problem, richardson-lucy-deconvolution, kullback-leibler-divergence, fisher-information-matrix, cramer-rao-bound]
sources:
  - paper: doi:10.1109/TMI.1982.4307558
    title: L. A. Shepp and Y. Vardi, Maximum likelihood reconstruction for emission tomography, IEEE Transactions on Medical Imaging 1(2), 1982
    locator: pp. 113 to 122 (the Poisson model of PET data and its likelihood)
  - paper: doi:10.1080/01621459.1985.10477119
    title: Y. Vardi, L. A. Shepp and L. Kaufman, A statistical model for positron emission tomography, Journal of the American Statistical Association 80(389), 1985
    locator: pp. 8 to 20 (the model, the likelihood and its maximizers)
  - paper: "K. Lange and R. Carson, EM reconstruction algorithms for emission and transmission tomography, Journal of Computer Assisted Tomography 8(2), 1984"
    locator: the Poisson models of emission and transmission data (general locator)
  - book: isbn:9780898714944
    title: A. C. Kak and M. Slaney, Principles of Computerized Tomographic Imaging, SIAM Classics in Applied Mathematics 33, 2001
    locator: Chapter 4, emission computed tomography (single photon and positron emission, attenuation)
---

The emission tomography model describes the data of PET (positron emission tomography) and SPECT (single photon emission computed tomography). A radioactive tracer in the body emits photons. The scanner counts the photons that reach each detector bin $i$. The model says that the counts $y_1, \ldots, y_m$ are independent [Poisson](/poisson-distribution/) variables,
$$y_i \sim \operatorname{Poisson}(\bar y_i), \qquad \bar y = A x + b,$$
where $x \ge 0$ is the unknown activity image with $N$ pixels, $A$ is a known $m \times N$ matrix with $a_{ij} \ge 0$, and $b \ge 0$ is a known background. In the continuous limit, $A x$ is the [Radon transform](/radon-transform/) of the activity for PET after the attenuation correction, and the [attenuated Radon transform](/attenuated-radon-transform/) for SPECT. The model is the base of [MLEM](/mlem-reconstruction/), [OSEM](/osem/) and the penalized likelihood methods.

## The machine

**The spaces.** The image $x \in \mathbb{R}^N$, $x \ge 0$, holds the expected number of decays in each pixel during the scan. For an $n \times n$ image, $N = n^2$. The data $y \in \{0, 1, 2, \ldots\}^m$ hold the counts of the $m$ detector bins. For a scan with $a$ angles of $d$ bins each, $m = a d$. In PET a bin is a line of response, the line between two detectors that see a coincidence. In SPECT a bin is a position on a detector behind a collimator, at one angle of the camera.

**The parameters.** The system matrix $A$ and the background $b$ are known before the reconstruction.

- $a_{ij}$ is the probability that a decay in pixel $j$ gives a count in bin $i$. It includes the geometry of the scanner, the efficiency of each detector, the attenuation in the body and, if modeled, the blur of the detector. So $\sum_i a_{ij} \le 1$. The sum $s_j = \sum_i a_{ij}$ is the *sensitivity* of pixel $j$.
- $b_i$ is the expected number of counts in bin $i$ that do not come from a direct path: random coincidences in PET and scattered photons. It is estimated from separate measurements or from a model.

**The noise model.** The number of decays in pixel $j$ is $\operatorname{Poisson}(x_j)$, and the pixels are independent. Each decay is detected in bin $i$ with probability $a_{ij}$, or not at all, independently of all other decays. By the thinning property of the Poisson process, the counts $z_{ij}$ from pixel $j$ in bin $i$ are independent with $z_{ij} \sim \operatorname{Poisson}(a_{ij} x_j)$. A sum of independent Poisson variables is Poisson, so $y_i = \sum_j z_{ij} + (\text{background counts})$ is $\operatorname{Poisson}((A x)_i + b_i)$, and the $y_i$ are independent. The variance of each count equals its mean.

**The likelihood.** The log-likelihood of $x$ is
$$L(x) = \sum_i \big[y_i \log \bar y_i - \bar y_i - \log y_i!\big], \qquad \bar y = A x + b.$$
Up to a constant, $-L(x)$ is the generalized [Kullback-Leibler divergence](/kullback-leibler-divergence/) between the data and the mean,
$$\operatorname{KL}(y, \bar y) = \sum_i \Big[y_i \log \frac{y_i}{\bar y_i} - y_i + \bar y_i\Big],$$
so maximum likelihood is the same as minimum KL divergence.

**Attenuation.** In PET the two photons of one decay fly in opposite directions along the line of response. Both must leave the body, so the attenuation factor is $\exp(-\int_\ell \mu)$ over the whole line $\ell$, for every position of the decay on the line. The factor goes into $a_{ij}$ as one number per bin, and the data are a weighted Radon transform with weights that do not depend on the position. In SPECT one photon flies from the decay to the detector, so the factor depends on the position along the line. This gives the [attenuated Radon transform](/attenuated-radon-transform/).

**The conditions of validity.** The model holds for the raw counts of a scanner without dead time and without pile-up, with a known matrix and a known background. It fails in these cases:

- The data are precorrected. If the scanner subtracts an estimate of the random coincidences, the result can be negative and its variance is larger than its mean, so it is not Poisson.
- The count rate is high, and the detectors lose counts in their dead time.
- The activity changes during the scan, or the patient moves.
- The matrix is wrong, for example from a wrong attenuation map. Then the model is consistent but describes the wrong scanner.

**A small example.** Take one pixel and one bin, $\bar y = a x + b$ with $a > 0$. The likelihood $y \log(a x + b) - (a x + b)$ is largest at $a x + b = y$, so the maximum likelihood estimate on $x \ge 0$ is $\hat x = \max(0, (y - b)/a)$. For $a = 0.1$, $b = 2$ and $y = 7$ this is $\hat x = 50$. The Fisher information is $a^2/(a x + b)$, so an unbiased estimator has a variance of at least $(a x + b)/a^2$, which is $700$ at $x = 50$: a relative standard deviation of $0.53$ from 7 counts.

## What it counts

The model has two outputs, and one cost.

- **The estimate.** An image $\hat x \ge 0$, usually a maximizer of $L$ or of $L$ minus a penalty. The model gives no closed form for it. It is computed by iterative methods such as [MLEM](/mlem-reconstruction/).
- **The uncertainty.** The [Fisher information matrix](/fisher-information-matrix/) is $F(x) = A^T \operatorname{diag}(1/\bar y)\, A$, because the Hessian of $L$ is $-A^T \operatorname{diag}(y/\bar y^2) A$ and $\mathbb{E}\, y_i = \bar y_i$. The [Cramer-Rao bound](/cramer-rao-bound/) says that an unbiased estimator has a covariance of at least $F(x)^{-1}$ when $F$ is invertible. The counts set the noise: if all means are multiplied by $c$, the relative standard deviation of each count falls as $1/\sqrt{c}$.
- **The cost.** One evaluation of $\bar y$ or of $A^T v$ costs one pass over the nonzero entries of $A$, which is $O(a d n)$ for a ray-driven projector on an $n \times n$ image. The iterative methods of the model are counted in these projections.

## Relation to other models

- **The linear Gaussian model.** With many counts per bin, $\operatorname{Poisson}(\bar y_i)$ is close to a Gaussian with mean and variance $\bar y_i$. Then the likelihood is close to a weighted least squares cost $\sum_i (y_i - \bar y_i)^2 / y_i$, which is the [linear Gaussian inverse problem](/linear-gaussian-inverse-problem/) with a diagonal noise covariance. This approximation is poor for bins with few counts, and it does not keep $x \ge 0$.
- **Transmission tomography.** In CT and in the attenuation scan of PET, the source is outside the body, and the counts are $y_i \sim \operatorname{Poisson}(I_0 e^{-[A \mu]_i} + r_i)$ by the [Beer-Lambert law](/beer-lambert-law/). The mean is not linear in the unknown $\mu$. Lange and Carson (1984) gave EM methods for both models.
- **Deconvolution.** If $A$ is a convolution with a point spread function, the same model describes photon-limited images in astronomy and microscopy. Then MLEM is the [Richardson-Lucy deconvolution](/richardson-lucy-deconvolution/).
- **The continuous model.** For a fine grid, $\bar y$ approaches the samples of the Radon transform (PET) or of the attenuated Radon transform (SPECT) of an activity density. The analytic inversion formulas, [filtered back-projection](/filtered-back-projection/) and the [Novikov formula](/novikov-inversion-formula/), use this limit and ignore the Poisson noise.

## Known results in the model

- **Concavity.** $L$ is concave on $x \ge 0$, because each term is the logarithm of an affine function minus an affine function. If the rows of $A$ with $y_i > 0$ form a matrix of full column rank, $L$ is strictly concave and its maximizer is unique.
- **Existence.** If every sensitivity $s_j$ is positive, a maximizer of $L$ over $x \ge 0$ exists, because $\sum_i \bar y_i = \sum_j s_j x_j + \sum_i b_i$ grows linearly in $x$ while the logarithms grow slowly.
- **The KKT conditions.** $\hat x \ge 0$ is a maximizer if and only if $\sum_i a_{ij} y_i / \bar y_i \le s_j$ for every $j$, with equality where $\hat x_j > 0$. This is the [KKT](/kkt-conditions/) system of a concave function on the orthant.
- **MLEM.** Shepp and Vardi (1982) applied the [EM algorithm](/expectation-maximization/) with the complete data $z_{ij}$ of the noise model. The result is a multiplicative update that keeps $x \ge 0$ and does not decrease $L$. Vardi, Shepp and Kaufman (1985) proved that it converges to a maximizer for $b = 0$.
- **The maximizer is noisy.** The problem is ill-posed, and for a fine grid the maximizer of $L$ fits the noise of the counts. This is an observation that the measurements on the [MLEM page](/mlem-reconstruction/) show; in practice the iteration is stopped early or the likelihood gets a penalty, as in the [one-step-late algorithm](/one-step-late-algorithm/) and [separable paraboloidal surrogates](/separable-paraboloidal-surrogates/).

## References
