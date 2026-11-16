---
tag: 5F7SJW
kind: concept
slug: scale-space-representation
name: Scale space
aliases:
- linear scale space
- Gaussian scale space
area: computer-vision/local-features
level: core
summary: The family of images made by smoothing one image with Gaussians of growing width, so that structures of every size can be found at their own scale.
prereqs: [gaussian-filter, linear-filtering, digital-image]
see_also: [automatic-scale-selection, gaussian-pyramid, laplacian-of-gaussian, heat-equation, difference-of-gaussians-detector, anisotropic-diffusion, image-pyramid, sift]
sources:
  - paper: "Andrew P. Witkin, Scale-space filtering, Proceedings of the Eighth International Joint Conference on Artificial Intelligence (IJCAI 1983), Volume 2, 1019-1022, 1983"
    locator: the scale-space image of a 1D signal and the tracking of zero crossings over scale
  - paper: doi:10.1007/BF00336961
    title: Jan J. Koenderink, The structure of images, Biological Cybernetics 50(5), 363-370, 1984
    locator: the causality requirement and the diffusion equation
  - paper: doi:10.1109/TPAMI.1986.4767749
    title: Jean Babaud, Andrew P. Witkin, Michel Baudin and Richard O. Duda, Uniqueness of the Gaussian kernel for scale-space filtering, IEEE Transactions on Pattern Analysis and Machine Intelligence 8(1), 26-33, 1986
    locator: the uniqueness theorem for 1D signals
  - book: isbn:978-0-7923-9418-1
    title: Tony Lindeberg, Scale-Space Theory in Computer Vision, Kluwer Academic Publishers, 1994
    locator: the chapters on the axioms of linear scale space, the discrete scale-space kernel and Gaussian derivatives
  - paper: doi:10.1023/A:1008344623873
    title: Joachim Weickert, Seiji Ishikawa and Atsushi Imiya, Linear scale-space has first been proposed in Japan, Journal of Mathematical Imaging and Vision 10(3), 237-252, 1999
    locator: the account of the axioms of Iijima
  - paper: doi:10.1109/34.56189
    title: Lawrence M. Lifshitz and Stephen M. Pizer, A multiresolution hierarchical approach to image segmentation based on intensity extrema, IEEE Transactions on Pattern Analysis and Machine Intelligence 12(6), 529-540, 1990
    locator: the discussion of extrema that appear in 2D images under Gaussian smoothing
---

The scale space of an image $f$ is the family of smoothed images

$$L(\mathbf x, t) = (g_t \ast f)(\mathbf x), \qquad g_t(\mathbf x) = \frac{1}{2\pi t} e^{-\lvert\mathbf x\rvert^2 / (2t)},$$

for all scales $t \ge 0$, with $L(\cdot, 0) = f$. The scale $t = \sigma^2$ is the variance of the [Gaussian filter](/gaussian-filter/), so details smaller than about $\sqrt t$ are smoothed away at scale $t$. The family is the solution of the [heat equation](/heat-equation/) $\partial_t L = \frac12 \nabla^2 L$ with $f$ as the start value. It is the only family of linear, shift invariant smoothings that has a small set of natural properties, among them that smoothing never creates new structure. Feature detectors use it to look at an image at every size at once: the [DoG detector](/difference-of-gaussians-detector/), the [determinant of Hessian detector](/determinant-of-hessian-detector/) and the [Harris-Laplace detector](/harris-laplace-detector/) search for maxima over position and scale, and [automatic scale selection](/automatic-scale-selection/) says at which scale to read each feature.

## In plain words

A photograph holds things of many sizes: the grain of a wall, the bricks, the windows, the whole house. Which ones matter depends on the task, and the right size is not known in advance. Scale space keeps all sizes. It makes a stack of copies of the image, each one more blurred than the one before. Small details disappear first, then larger ones. A detail that stays visible over a long part of the stack is a real structure of that size. The blur is a special one, the Gaussian, because it is the only blur that never adds new spots or edges while it removes the old ones, so every structure in a blurred copy comes from the original image.

## The idea

**Smoothing as a family.** Let $f$ be a gray [digital image](/digital-image/), seen as a function on the plane. Take the Gaussian $g_t$ of variance $t$ in each direction and define $L(\cdot, t) = g_t \ast f$. Then $L$ is a function of three variables, two of position and one of scale. The units of $t$ are pixels squared; a scale parameter $\sigma = \sqrt t$ in pixels is also common.

**The semigroup property.** Gaussians add their variances: $g_s \ast g_t = g_{s + t}$. So the image at scale $s + t$ is the image at scale $s$ smoothed by $g_t$, and a coarse scale can be computed from a finer one. This is what makes a [Gaussian pyramid](/gaussian-pyramid/) cheap: each level smooths the one before it a little more, and halves the size when $\sigma$ doubles.

**The diffusion equation.** $g_t$ satisfies $\partial_t g_t = \frac12 \nabla^2 g_t$, and so does $L$. Smoothing is diffusion of the gray values, as heat spreads in a plate. At a local maximum of $L$ in space the Laplacian is negative or zero, so the value can only fall as $t$ grows; at a local minimum it can only rise. This is the causality requirement of Koenderink: a level line at a coarse scale always comes from a level line at a finer scale.

**Derivatives commute with smoothing.** $\partial_x (g_t \ast f) = (\partial_x g_t) \ast f$. So the derivatives of $L$ at scale $t$ are well defined for any image, even one with jumps, and are computed by filtering with Gaussian derivatives. This scale-space derivative is the basis of the [Laplacian of Gaussian](/laplacian-of-gaussian/), the Harris measure, the Hessian and most detectors on this site.

**Why the Gaussian.** Several sets of axioms single out the Gaussian kernel. Among linear and shift invariant smoothings with the semigroup property that treat all directions and all scales alike, the Gaussian is the only one that does not create new local extrema in 1D signals (Babaud and others, 1986) or new level lines in the sense of causality (Koenderink, 1984). Iijima gave an axiomatic derivation in Japan much earlier, as Weickert and others describe. In 2D the statement must be made with care: the Gaussian does not enhance extrema, but new local extrema can appear in an image under Gaussian smoothing, as Lifshitz and Pizer observed.

**Discrete scale space.** On the pixel grid, the sampled Gaussian is only an approximation, and for small $t$ it is a poor one. Lindeberg derived the discrete analogue: the kernel $T(n, t) = e^{-t} I_n(t)$, where $I_n$ is the modified Bessel function of integer order. It sums to $1$, has the variance $t$ exactly, satisfies the semigroup property exactly, and does not create local extrema in 1D. In 2D it is used separably along rows and columns.

## Examples

**The two kernels at small and medium scale.** The table gives the values at $n = 0, 1, 2, 3$, the sum and the variance.

| $t$ | kernel | $n = 0$ | $n = 1$ | $n = 2$ | $n = 3$ | sum | variance |
|---|---|---|---|---|---|---|---|
| 0.25 | discrete $e^{-t} I_n(t)$ | 0.7910 | 0.0981 | 0.0061 | 0.0003 | 1.0000 | 0.250 |
| 0.25 | sampled Gaussian | 0.7979 | 0.1080 | 0.0003 | 0.0000 | 1.0144 | 0.215 |
| 1 | discrete $e^{-t} I_n(t)$ | 0.4658 | 0.2079 | 0.0499 | 0.0082 | 1.0000 | 1.000 |
| 1 | sampled Gaussian | 0.3989 | 0.2420 | 0.0540 | 0.0044 | 1.0000 | 1.000 |

At $t = 1$ the two kernels are close and both have variance $1$. At $t = 0.25$ the sampled Gaussian does not sum to $1$ and, after normalization, has the variance $0.215$ instead of $0.25$: it smooths less than it should.

**Extrema disappear and do not appear in 1D.** Take the 22 values $0, 0, 3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9, 3, 2, 3, 0, 0$ and smooth them with the discrete kernel, with the clamp border rule. The number of strict local extrema inside the signal is:

| $t$ | 0 | 0.5 | 1 | 2 | 4 | 8 | 16 |
|---|---|---|---|---|---|---|---|
| extrema | 13 | 11 | 5 | 3 | 1 | 1 | 1 |

The count never grows. At $t = 4$ one maximum is left, at the position of the largest mass of high values, and it stays.

**A blob.** A Gaussian blob $f = \exp(-\lvert\mathbf x\rvert^2 / (2t_0))$ has the scale space $L(\mathbf x, t) = \frac{t_0}{t_0 + t} \exp(-\lvert\mathbf x\rvert^2 / (2(t_0 + t)))$: it gets wider and lower, and its variance grows from $t_0$ to $t_0 + t$. Its normalized Laplacian at the center is largest at $t = t_0$, which is how [automatic scale selection](/automatic-scale-selection/) finds the size of the blob.

**An edge.** A unit step along $x$ becomes $L(x, t) = \Phi(x / \sqrt t)$, with $\Phi$ the normal distribution function. The gradient at the edge is $1/\sqrt{2\pi t}$, which falls with $t$. The product $\sqrt t \cdot L_x = 1/\sqrt{2\pi}$ does not depend on $t$: this is the normalized derivative with $\gamma = 1$, and it shows that a perfect step has no scale of its own.

## Where it is used

- **Scale invariant detectors.** The DoG detector of [SIFT](/sift/), the determinant of Hessian detector, [SURF](/surf/), Harris-Laplace and Hessian-Laplace all search maxima of a normalized measure in the three dimensions of scale space.
- **Scale selection.** [Automatic scale selection](/automatic-scale-selection/) chooses the scale of each feature from the scale-space derivatives.
- **Pyramids.** [Gaussian pyramids](/gaussian-pyramid/) and [image pyramids](/image-pyramid/) sample scale space at a few scales and reduce the size of the coarse images.
- **Edges and derivatives.** The [Canny edge detector](/canny-edge-detector/) smooths with a Gaussian of chosen scale before it takes derivatives. Derivatives at a known scale also enter optical flow, stereo and the [histogram of oriented gradients](/histogram-of-oriented-gradients/).
- **Nonlinear scale spaces.** [Anisotropic diffusion](/anisotropic-diffusion/) replaces the heat equation by one that smooths less across edges. [KAZE features](/kaze-features/) detect points in such a nonlinear scale space.

## References
