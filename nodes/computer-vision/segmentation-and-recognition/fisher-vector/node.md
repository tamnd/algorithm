---
tag: WR6YRW
kind: algorithm
slug: fisher-vector
name: Fisher vector
aliases:
- Fisher vector image representation
area: computer-vision/segmentation-and-recognition
level: advanced
summary: "Represent an image by the gradient of the log-likelihood of its descriptors under a Gaussian mixture with respect to the means and variances, whitened and normalized."
solves: [image-retrieval]
model: real-ram
complexity:
  vars: {n: the number of local descriptors of the image, K: the number of mixture components, D: the descriptor dimension}
  time: {worst: O(n K D), best: O(n K D)}
  space: {extra: O(K D)}
properties: {deterministic: true, exact: true, order_invariant: true, output_size: 2 K D}
history:
  year: 2007
  people: [Tommi Jaakkola, David Haussler, Florent Perronnin, Christopher Dance, Jorge Sanchez, Thomas Mensink]
  note: "Jaakkola and Haussler (1998) defined the Fisher kernel. Perronnin and Dance (CVPR 2007) applied it to a Gaussian mixture of local descriptors. Perronnin, Sanchez and Mensink (ECCV 2010) added the power and L2 normalizations, and Sanchez et al. (IJCV 2013) gave the full account."
prereqs: [gaussian-mixture-model, fisher-information-matrix, bag-of-visual-words]
see_also: [vlad, bag-of-visual-words, score-function, expectation-maximization, support-vector-machine, kernel-trick, spatial-pyramid-matching, image-retrieval]
sources:
  - url: https://mlanthology.org/neurips/1998/jaakkola1998neurips-exploiting/
    title: "Tommi Jaakkola and David Haussler, Exploiting generative models in discriminative classifiers, Advances in Neural Information Processing Systems 11 (NIPS 1998), 487-493"
    locator: "The Fisher score, the Fisher information as a metric, and the Fisher kernel"
  - paper: doi:10.1109/CVPR.2007.383266
    title: "Florent Perronnin and Christopher Dance, Fisher kernels on visual vocabularies for image categorization, CVPR 2007"
    locator: "The gradient of the log-likelihood of a Gaussian mixture of local descriptors as an image signature"
  - paper: doi:10.1007/978-3-642-15561-1_11
    title: "Florent Perronnin, Jorge Sanchez and Thomas Mensink, Improving the Fisher kernel for large-scale image classification, ECCV 2010, LNCS 6314, 143-156"
    locator: "The gradients with respect to the means and variances only (2 K D values), L2 normalization, power normalization and spatial pyramids"
  - paper: doi:10.1007/s11263-013-0636-x
    title: "Jorge Sanchez, Florent Perronnin, Thomas Mensink and Jakob Verbeek, Image classification with the Fisher vector: theory and practice, International Journal of Computer Vision 105(3), 2013, 222-245"
    locator: "Section 2.1 (Fisher kernel, Eq. 1 to 4), Section 2.2 (Gaussian mixture gradients, Eq. 16 to 19, and Algorithm 1), Section 2.3 (L2 and power normalization, Eq. 30), Section 2.5 (relation to the bag of words and VLAD), Appendix A (diagonal Fisher information)"
---

The Fisher vector describes the set of local descriptors of an image by how the parameters of a fixed [Gaussian mixture model](/gaussian-mixture-model/) would have to change to fit that set better. It is the gradient of the average log-likelihood of the descriptors with respect to the means and the standard deviations of the mixture, scaled by the inverse square root of the [Fisher information](/fisher-information-matrix/), then power and L2 normalized. With $K$ components in dimension $D$, it has $2 K D$ values. Compared with [VLAD](/vlad/), it uses soft assignments and also keeps second order statistics; compared with the [bag of visual words](/bag-of-visual-words/), which only counts, it keeps the first and second moments of the descriptors per component.

## In plain words

First, learn a model of what local patches look like in general: a mixture of a few dozen or a few hundred bell-shaped clouds. Then, for a new image, ask: if I wanted this general model to describe the patches of this image better, how should I move each cloud, and how should I make it wider or narrower?

The answer is a list of small pushes, one for each cloud and each descriptor coordinate. Two images that need the same pushes have similar content. The pushes are scaled so that each one counts the same on average, and large values are damped so that one repeated pattern cannot dominate. A linear classifier on this vector works about as well as much slower nonlinear methods on simpler image signatures.

## The problem

**Input.** A diagonal Gaussian mixture $u$ with $K$ components: weights $w_k > 0$ with $\sum_k w_k = 1$, means $\mu_k \in \mathbb{R}^D$ and standard deviations $\sigma_k \in \mathbb{R}^D_{>0}$. It is learned once, usually by [expectation maximization](/expectation-maximization/) on training descriptors. Also the $n$ local descriptors $X = \{x_1, \ldots, x_n\}$ of one image, and the power $\rho \in (0, 1]$ (usually $1/2$).

**Output.** A vector $z \in \mathbb{R}^{2KD}$ (or $\mathbb{R}^{(2D+1)K}$ with the weight part). The *Fisher score* of the image is $\nabla_\lambda \frac1n \sum_t \log u(x_t)$, the gradient with respect to the parameters $\lambda$; see [score function](/score-function/). The *Fisher kernel* of Jaakkola and Haussler compares two images by $G_X^\top F^{-1} G_Y$, where $F$ is the Fisher information of $u$. Writing $F^{-1} = L^\top L$, the Fisher vector is $\mathcal{G}_X = L\, G_X$, so the kernel becomes a plain inner product (Sanchez et al. 2013, Section 2.1). With the posterior $\gamma_t(k) = w_k \mathcal{N}(x_t; \mu_k, \sigma_k) / \sum_j w_j \mathcal{N}(x_t; \mu_j, \sigma_j)$, and all operations on vectors taken per coordinate, the entries are (Sanchez et al., Eq. 16 to 18, divided by $n$)
$$\mathcal{G}_{\alpha_k} = \frac{1}{n\sqrt{w_k}} \sum_{t=1}^{n} (\gamma_t(k) - w_k), \quad \mathcal{G}_{\mu_k} = \frac{1}{n\sqrt{w_k}} \sum_{t=1}^{n} \gamma_t(k) \frac{x_t - \mu_k}{\sigma_k}, \quad \mathcal{G}_{\sigma_k} = \frac{1}{n\sqrt{2 w_k}} \sum_{t=1}^{n} \gamma_t(k) \Big[ \frac{(x_t - \mu_k)^2}{\sigma_k^2} - 1 \Big].$$
Here $\alpha$ are the soft-max parameters with $w = \mathrm{softmax}(\alpha)$. The weight part is often left out, as in Perronnin et al. (2010), since it adds only $K$ values.

## The algorithm

```pseudo id=main
FISHER-VECTOR(X, w, mu, sigma, rho)       ▷ n = |X|, K components, dimension D
L1  S0_k ← 0, S1_k ← 0 in R^D, S2_k ← 0 in R^D for k = 1..K
L2  for each descriptor x_t in X do
L3      gamma_t(k) ← w_k N(x_t; mu_k, sigma_k) / sum_j w_j N(x_t; mu_j, sigma_j) for all k
L4      for each k, with r = (x_t - mu_k) / sigma_k: S0_k += gamma_t(k); S1_k += gamma_t(k) r; S2_k += gamma_t(k) (r^2 - 1)
L5  G_alpha_k ← (S0_k - n w_k) / (n sqrt(w_k))   ▷ optional weight part
L6  G_mu_k ← S1_k / (n sqrt(w_k))
L7  G_sigma_k ← S2_k / (n sqrt(2 w_k))
L8  z ← the concatenation of (G_mu_k, G_sigma_k) for k = 1..K
L9  z_i ← sign(z_i) |z_i|^rho for each i
L10 if z ≠ 0 then z ← z / ||z||
L11 return z
```

Line L3 is computed in the log domain with the log-sum-exp trick. A descriptor far from every component makes all densities underflow to 0 in floating point, and a direct division then gives 0/0. Lines L1 to L4 collect the statistics $S_0$, $S_1$ and $S_2$ of Sanchez et al. (Eq. 20 to 22, in a centered form), and lines L5 to L7 turn them into the normalized gradient. Lines L9 and L10 are the improvements of Perronnin et al. (2010). This is Algorithm 1 of Sanchez et al.

## Example

Take $D = 1$, $K = 2$, $w = (0.5, 0.5)$, $\mu = (-1, 1)$, $\sigma = (1, 1)$, and $n = 3$ descriptors $0$, $1$, $2$. The log ratio of the two components at $x$ is $((x+1)^2 - (x-1)^2)/2 = 2x$, so $\gamma(2) = 1/(1 + e^{-2x})$.

| $x_t$ | $\gamma_t(1)$ | $\gamma_t(2)$ | $z$ for comp. 1 | $z$ for comp. 2 |
|---|---|---|---|---|
| 0 | 0.5 | 0.5 | 1 | $-1$ |
| 1 | 0.119203 | 0.880797 | 2 | 0 |
| 2 | 0.017986 | 0.982014 | 3 | 1 |

Here $z = (x_t - \mu_k)/\sigma_k$. The statistics are $S_0 = (0.637189, 2.362811)$, $S_1 = (0.5 + 2 \cdot 0.119203 + 3 \cdot 0.017986,\ -0.5 + 0.982014) = (0.792364, 0.482014)$ and $S_2 = (3 \cdot 0.119203 + 8 \cdot 0.017986,\ -0.880797) = (0.501497, -0.880797)$. With $n \sqrt{w_k} = 2.1213$ and $n \sqrt{2 w_k} = 3$, lines L5 to L7 give
$$\mathcal{G}_\alpha = (-0.4067, 0.4067), \quad \mathcal{G}_\mu = (0.3735, 0.2272), \quad \mathcal{G}_\sigma = (0.1672, -0.2936).$$
The weight part sums to zero, as it must, since $\sum_k (\gamma_t(k) - w_k) = 0$ and the weights are equal. The 4 values of the means and sigmas, in the order $(\mu_1, \sigma_1, \mu_2, \sigma_2)$, are $(0.3735, 0.1672, 0.2272, -0.2936)$. After the signed square root and L2 normalization they become $(0.5932, 0.3968, 0.4627, -0.5259)$. The negative $\mathcal{G}_{\sigma_2}$ says that the descriptors near component 2 are less spread than the model expects: two of them sit at distance 0 and 1 from its mean.

## Correctness

The proof in the correctness file first derives the gradients of $\log u$ with respect to $\alpha_k$, $\mu_k$ and $\sigma_k$; the tests check them against finite differences. Then it computes the Fisher information under the assumption of Sanchez et al. (Appendix A) that each descriptor comes from one component with a posterior of 0 or 1 (well separated components). Under this assumption, the blocks for the means and the standard deviations are diagonal, with entries $w_k / \sigma_{k,i}^2$ and $2 w_k / \sigma_{k,i}^2$, so $F^{-1/2}$ multiplies the gradients by $\sigma_{k,i}/\sqrt{w_k}$ and $\sigma_{k,i}/\sqrt{2 w_k}$. This is exactly lines L6 and L7. It also shows that each normalized entry for one descriptor has mean 0 and variance 1 under the model. For the weights, the block is $\mathrm{diag}(w) - w w^\top$, which is singular; the factor $1/\sqrt{w_k}$ of line L5 is its diagonal approximation without the $w w^\top$ term, and the variance of a normalized weight entry is $1 - w_k$, not 1. When the components overlap, the diagonal form is an approximation, so the whitening is approximate. The code computes the definition exactly up to floating point.

## Complexity

In the [real RAM](/real-ram/), line L3 costs $O(K D)$ per descriptor (one diagonal Gaussian density per component), and line L4 costs $O(K D)$. So lines L2 to L4 cost $O(n K D)$, and lines L5 to L11 cost $O(K D)$. Extra space is $O(K D)$ for the statistics and the output. The $\exp$ and $\log$ calls are counted as one operation each. In practice many posteriors are below a small threshold and are skipped, which saves time but changes the result slightly.

For example, $K = 256$ and SIFT reduced to $D = 64$ by [principal component analysis](/principal-component-analysis/) give a vector with $2 \cdot 256 \cdot 64 = 32{,}768$ values. The PCA step also decorrelates the coordinates, which makes the diagonal covariance model fit better.

## Properties

- **Order invariant.** The statistics are sums over descriptors.
- **Generalizes the bag of words and VLAD.** The weight part is a centered, scaled soft histogram of words. With hard posteriors, equal weights and unit variances, the mean part is $(\sqrt{K}/n)$ times [VLAD](/vlad/) (Sanchez et al., Section 2.5). The tests check this identity.
- **Zero for a typical image.** If the descriptors of an image follow $u$ exactly, the expected score is zero. An image differs from the model through its nonzero entries.
- **A kernel.** Without the power step, the inner product of two Fisher vectors is a sum over pairs of descriptors, as for VLAD, so it is a positive semidefinite match kernel (Sanchez et al., Eq. 38).
- **Dense and high-dimensional.** Most entries are nonzero, which makes storage large. Sanchez et al. compress the vectors with [product quantization](/product-quantization/) for large data sets.
- **Depends on the mixture.** The vector is defined only for one fixed $u$. Vectors from different mixtures cannot be compared.

## Variants and improvements

- **Power normalization** (line L9, $\rho = 1/2$). It reduces the effect of bursty descriptors and of the sparsity that comes with large $K$. Sanchez et al. relate it to the Hellinger kernel.
- **L2 normalization** (line L10). Perronnin et al. (2010) motivate it as removing the part of the score that depends on the amount of image-specific background. It is a heuristic with that motivation, not a theorem.
- **Spatial pyramid.** One Fisher vector per cell of a grid, concatenated, as in [spatial pyramid matching](/spatial-pyramid-matching/).
- **Weight gradient.** Including line L5 gives $(2D + 1) K$ values. Its benefit is small.
- **Full or exact Fisher information.** Using the exact $F$ instead of the diagonal approximation is possible but costs much more and is rare.
- **VLAD.** The simplified version with hard assignment and the mean part only is [VLAD](/vlad/).

## When to use it

Use the Fisher vector when you need a fixed-length image signature that works well with a linear classifier, for example a linear [support vector machine](/support-vector-machine/). The linear classifier then costs $O(2KD)$ per image, while a nonlinear kernel on a bag of words costs much more at scale. For retrieval it is a strong alternative to VLAD at a higher cost. On most recognition benchmarks, features from convolutional networks later did better, and the Fisher vector is now used mostly on top of such features or as a baseline.

## Pitfalls

- **Variance, not standard deviation.** Some texts take the gradient with respect to $\sigma^2$. The normalized vector is the same up to a constant per entry only if the Fisher normalization is also redone for that parameter. Mixing the two gives wrong scales.
- **Underflow in line L3.** Compute the posteriors in the log domain.
- **Forgetting $1/n$.** Without it, images with more descriptors get larger vectors before L2 normalization, and the power step then acts differently on them.
- **A mixture with tiny $\sigma$.** EM can produce components with very small variance on a few training points. Their entries then explode. Put a floor on the variances during training.
- **Using full covariances.** The formulas of this page are for diagonal covariances. Decorrelate the descriptors with PCA first, or the model fits poorly.
- **Power step on a vector that is then compared with another kernel.** After line L9 the inner product is no longer a sum over pairs of descriptors.

## Implementations

The Python code computes the posteriors with log-sum-exp, the statistics, the normalized gradient with an optional weight part and an optional hard assignment, the signed power and the L2 normalization. A separate function gives the unnormalized gradients and the log-likelihood. The tests check the example of this page, the gradients against central finite differences, the scaling of the gradients by the diagonal Fisher factors, a Monte Carlo check that the normalized entries have mean 0 and variance 1 (and $1 - w_k$ for the weights) on well separated components, the identity with scaled VLAD under hard assignment, and order invariance.

## History

Jaakkola and Haussler (1998) proposed the Fisher kernel to use a generative model inside a discriminative classifier, with protein sequences and hidden Markov models as the first application. Perronnin and Dance (2007) used a Gaussian mixture over local image descriptors as the generative model and showed that the Fisher kernel gives a compact image signature for categorization. Perronnin, Sanchez and Mensink (2010) kept only the mean and variance gradients and added power and L2 normalization and spatial pyramids, which made the Fisher vector competitive with much more costly methods. Sanchez, Perronnin, Mensink and Verbeek (2013) gave the complete derivation, the approximations and an extensive experimental study.

## References
