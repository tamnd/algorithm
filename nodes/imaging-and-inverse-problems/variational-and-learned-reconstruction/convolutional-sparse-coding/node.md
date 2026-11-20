---
tag: VZD7T3
kind: model
slug: convolutional-sparse-coding
name: Convolutional sparse coding
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: research
summary: Model a whole image as a sum of small filters convolved with sparse feature maps, solved efficiently in the Fourier domain.
prereqs: [dictionary-learning, convolution-theorem, admm]
see_also: [k-svd, mutual-coherence, fast-fourier-transform, iterative-shrinkage-thresholding, analysis-and-synthesis-sparsity, algorithm-unrolling, image-denoising, sparse-signal-recovery]
sources:
  - paper: doi:10.1109/CVPR.2010.5539957
    title: Matthew D. Zeiler, Dilip Krishnan, Graham W. Taylor and Rob Fergus, Deconvolutional networks, Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, 2010
    locator: the whole paper (images as sums of filters convolved with sparse feature maps, learned layer by layer)
  - paper: doi:10.1109/TIP.2015.2495260
    title: Brendt Wohlberg, Efficient algorithms for convolutional sparse representations, IEEE Transactions on Image Processing 25(1), 2016
    locator: pages 301 to 315 (ADMM for convolutional basis pursuit denoising in the Fourier domain, with one rank-one linear system per frequency solved by the Sherman-Morrison formula)
  - paper: doi:10.1109/TSP.2017.2733447
    title: Vardan Papyan, Jeremias Sulam and Michael Elad, Working locally thinking globally, theoretical guarantees for convolutional sparse coding, IEEE Transactions on Signal Processing 65(21), 2017
    locator: pages 5687 to 5701 (the local sparsity measure, uniqueness, and the success of OMP and basis pursuit under local sparsity)
---

Convolutional sparse coding models a whole signal or image as a sum of a few small filters, each convolved with its own sparse map of coefficients. It is [dictionary learning](/dictionary-learning/) with a dictionary that is invariant to shifts: instead of $K$ atoms of the size of a patch, used on overlapping patches that are coded separately, it uses $K$ filters that may appear at any position of the image, and codes the whole image at once. The global dictionary is a union of $K$ convolution matrices. The [convolution theorem](/convolution-theorem/) turns it into $N$ small independent problems, one per frequency, and this is why the model is practical. [K-SVD](/k-svd/) learns a dictionary for patches; this page describes the model that replaces patches by the whole image.

## The machine

- **Unknowns.** $K$ sparse coefficient maps $x_1, \dots, x_K$, each of the size of the image, $N$ pixels in all. A nonzero entry of $x_k$ at position $p$ says that filter $k$ appears at $p$ with that amplitude.
- **Parameters.** $K$ filters $d_1, \dots, d_K$, each supported on a small window of $P$ pixels, for example $8 \times 8$ or $11 \times 11$, with $\|d_k\|_2 \le 1$. They are given, or learned from training images.
- **Forward map.** The image is

$$y = \sum_{k=1}^K d_k * x_k + w,$$

where $*$ is 2D convolution and $w$ is noise, usually modeled as white Gaussian. In matrix form, $y = Dx + w$ with $x = (x_1; \dots; x_K) \in \mathbb{R}^{KN}$ and $D = [\,C_{d_1} \mid \dots \mid C_{d_K}\,] \in \mathbb{R}^{N \times KN}$, where $C_{d_k}$ is the matrix of convolution with $d_k$. Each column of $D$ is one filter at one position.
- **Boundaries.** The fast algorithms take the convolution as circular, so that each $C_{d_k}$ is a circulant matrix (block circulant in 2D) diagonalized by the [discrete Fourier transform](/discrete-fourier-transform/). This is valid when the image is padded or its borders do not matter. Otherwise the image is extended and a mask selects the observed pixels.
- **Sparsity.** Most entries of each $x_k$ are 0. The model is valid for images that are made of repeated local structures, such as edges, textures and blobs, at arbitrary positions.

## What it counts

The model predicts the image as the sum of filter responses $\sum_k d_k * x_k$. A fit with fixed filters is convolutional basis pursuit denoising,

$$\min_{x_1, \dots, x_K}\ \frac12\Big\|\sum_{k=1}^K d_k * x_k - y\Big\|_2^2 + \lambda\sum_{k=1}^K\|x_k\|_1,$$

which is the [LASSO](/lasso-regression/) for the matrix $D$. Learning the filters minimizes the same objective over the $d_k$ as well, over a set of training images, with $d_k$ restricted to its window and $\|d_k\|_2 \le 1$.

**In the Fourier domain.** Write $\hat{\cdot}$ for the DFT of the padded arrays. Circular convolution becomes a product, so $\hat y = \sum_k \hat d_k \odot \hat x_k + \hat w$: at each frequency $\omega$, the data value $\hat y(\omega)$ depends only on the $K$ numbers $\hat x_1(\omega), \dots, \hat x_K(\omega)$. A least squares step in the model, $\min_x\frac12\|Dx - y\|^2 + \frac\rho2\|x - b\|^2$, which is the main step of [ADMM](/admm/) for the problem above, then splits into $N$ independent systems

$$\big(a_\omega a_\omega^H + \rho I_K\big)z_\omega = c_\omega, \qquad a_\omega = \big(\overline{\hat d_1(\omega)}, \dots, \overline{\hat d_K(\omega)}\big)^T,$$

of size $K \times K$, each the identity plus a rank-one matrix. The Sherman-Morrison formula solves each one in $O(K)$ operations:

$$z_\omega = \frac1\rho\Big(c_\omega - \frac{a_\omega\,(a_\omega^Hc_\omega)}{\rho + a_\omega^Ha_\omega}\Big).$$

So one ADMM iteration costs $O(KN\log N)$ for the [FFTs](/fast-fourier-transform/) and $O(KN)$ for the solves, in place of a dense system of size $KN$.

**A small example.** Take a 1D signal of length $N = 4$, one filter $d = (1, 1, 0, 0)$ and circular convolution, $y(t) = x(t) + x(t - 1)$. The map $x = e_0 = (1, 0, 0, 0)$ gives $y = (1, 1, 0, 0)$. In the Fourier domain $\hat d(\omega) = 1 + (-i)^\omega$, that is $(2, 1 - i, 0, 1 + i)$, and $\hat x = (1, 1, 1, 1)$, so $\hat y = \hat d \odot \hat x = (2, 1 - i, 0, 1 + i)$, the DFT of $(1, 1, 0, 0)$. Because $\hat d(2) = 0$, the alternating map $(1, -1, 1, -1)$ is in the null space, and $x' = e_0 - (1, -1, 1, -1) = (0, 1, -1, 1)$ gives the same $y$: check $y(0) = 0 + 1$, $y(1) = 1 + 0$, $y(2) = -1 + 1$, $y(3) = 1 - 1$. The sparse map $e_0$, with $\ell_1$ norm 1, is preferred to $x'$, with $\ell_1$ norm 3. A zero of a filter's transform always gives such a null vector, and the sparsity prior is what removes it.

## Relation to other models

- **Patch-based sparse coding.** [Dictionary learning](/dictionary-learning/) and [K-SVD](/k-svd/) code each patch on its own and average the overlaps. The patches are not consistent with one global image, and a dictionary for patches learns many shifted copies of the same structure. Convolutional sparse coding is the global model of which the patch model is a local approximation: each patch of $y$ equals a local dictionary, made of all the filters at all shifts that touch the patch, times a stripe of $x$.
- **Shift-invariant dictionaries.** The columns of $D$ are all shifts of $K$ filters, so the model is invariant to translation. The cost is a large [mutual coherence](/mutual-coherence/): a filter and its shift by one pixel are usually almost parallel.
- **Deconvolutional and convolutional networks.** Zeiler, Krishnan, Taylor and Fergus (2010) stacked convolutional sparse coding layers into deconvolutional networks. Papyan, Romano and Elad later showed that the forward pass of a convolutional neural network with ReLU can be read as layered thresholding for a multilayer version of the model. Unrolled solvers of the model give network layers; see [algorithm unrolling](/algorithm-unrolling/).
- **Analysis models.** A total variation or wavelet prior says that a fixed filter bank applied to the image gives sparse output. That is an analysis model; convolutional sparse coding is a synthesis model with learned filters. See [analysis and synthesis sparsity](/analysis-and-synthesis-sparsity/).

## Known results in the model

**Diagonalization.** With circular boundaries, $D^HD$ is block diagonal after a DFT, with one $K \times K$ block $a_\omega a_\omega^H$ per frequency. This is the convolution theorem applied to each $C_{d_k}$, and it gives the cost of $O(KN\log N)$ per iteration above. Fourier-domain ADMM for the problem is due to Bristow, Eriksson and Lucey (2013), and Wohlberg (2016) reduced the solve per frequency to $O(K)$ with the Sherman-Morrison formula.

**Ambiguities.** Shifting a filter one way and its map the other way leaves $y$ unchanged: $d * x = (S_\tau d) * (S_{-\tau}x)$ for every circular shift $S_\tau$. Inside a fixed window, this ambiguity remains whenever the filter does not fill its window. Scaling $d_k$ by $c$ and $x_k$ by $1/c$ is removed by the norm constraint. For each frequency $\omega$ with $K \ge 2$, the vector of the $K$ values $\hat x_k(\omega)$ is determined by $\hat y(\omega)$ only up to the $K - 1$ dimensional null space of $a_\omega^H$, so without the sparsity prior the coefficients are never determined.

**Local sparsity guarantees.** The global coherence of $D$ is at least the largest correlation of a filter with its own shifts, so classical guarantees that bound the total number $\|x\|_0$ of nonzeros by $\tfrac12(1 + 1/\mu)$ allow only a few nonzeros in a whole image. Papyan, Sulam and Elad (2017) replaced $\|x\|_0$ by the $\ell_{0,\infty}$ measure, the largest number of nonzeros in any stripe of $x$ that affects one patch of $y$. They proved that if $\|x\|_{0,\infty} < \tfrac12(1 + 1/\mu(D))$, then $x$ is the sparsest representation in this measure, and that [orthogonal matching pursuit](/orthogonal-matching-pursuit/) and basis pursuit find it, with stability bounds for noise. These conditions allow a number of nonzeros that grows with the size of the image.

**Learning.** Filter learning alternates the coding step above with a filter update that is also solved in the Fourier domain, with the window constraint enforced by a projection. As for patch dictionary learning, the joint problem is not convex, and the guarantees are for the coding step, not for the learning.

## References
