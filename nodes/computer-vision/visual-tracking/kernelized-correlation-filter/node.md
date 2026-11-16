---
tag: D8MKGV
kind: algorithm
slug: kernelized-correlation-filter
name: Kernelized correlation filter
aliases:
- KCF tracker
area: computer-vision/visual-tracking
level: advanced
summary: Ridge regression on all cyclic shifts of the target patch, made fast because for shift-invariant kernels the kernel matrix of the shifts is circulant and diagonal in the Fourier domain.
solves: [visual-object-tracking]
model: real-ram
complexity:
  vars: {P: the number of pixels in the patch, N: the number of frames tracked}
  time: {worst: Θ(N P log P), average: Θ(N P log P), best: Θ(N P log P)}
  space: {extra: Θ(P)}
properties: {deterministic: true, exact: false, local: true, iterative: false, online: true}
history:
  year: 2015
  people: [João F. Henriques, Rui Caseiro, Pedro Martins, Jorge Batista]
  note: Henriques, Caseiro, Martins and Batista showed that ridge regression on all cyclic shifts of a patch has a circulant data matrix (ECCV 2012), and extended the result to kernels and multichannel features in the 2015 journal paper.
prereqs: [mosse-filter, ridge-regression, kernel-trick]
see_also: [correlation-filter-tracking, discrete-fourier-transform, fast-fourier-transform, support-vector-machine, siamese-tracking, tracking-by-detection, visual-object-tracking, cross-correlation]
sources:
  - paper: doi:10.1109/TPAMI.2014.2345390
    title: João F. Henriques, Rui Caseiro, Pedro Martins and Jorge Batista, High-speed tracking with kernelized correlation filters, IEEE Transactions on Pattern Analysis and Machine Intelligence 37(3), 2015, 583 to 596 (also arXiv 1404.7584)
    locator: Theorem 1 (the circulant kernel matrix for permutation-invariant kernels), the formulas for training and detection, the Gaussian and linear kernel correlations, and the parameters of the experiments
  - paper: "João F. Henriques, Rui Caseiro, Pedro Martins and Jorge Batista, Exploiting the circulant structure of tracking-by-detection with kernels, European Conference on Computer Vision (ECCV), 2012"
    locator: the whole paper (the first form, with raw pixels)
  - paper: doi:10.1561/0100000006
    title: Robert M. Gray, Toeplitz and circulant matrices, a review, Foundations and Trends in Communications and Information Theory 2(3), 2006, 155 to 239
    locator: the chapter on circulant matrices (diagonalization by the discrete Fourier transform)
  - paper: doi:10.1109/CVPR.2010.5539960
    title: David S. Bolme, J. Ross Beveridge, Bruce A. Draper and Yui Man Lui, Visual object tracking using adaptive correlation filters, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2010, 2544 to 2550
    locator: the whole paper (the MOSSE filter that the linear case reproduces)
---

The kernelized correlation filter (KCF) is a tracker that trains a [ridge regression](/ridge-regression/) on every cyclic shift of the patch around the target. Each shifted patch is a training sample, with a label that is high for small shifts and low for large ones. With $P$ pixels there are $P$ samples, and solving the regression directly would cost a $P \times P$ system per frame. Henriques, Caseiro, Martins and Batista showed that for a kernel that does not change when both of its arguments are shifted in the same way, the kernel matrix of all shifts is circulant. A circulant matrix is diagonal in the basis of the [discrete Fourier transform](/discrete-fourier-transform/), so the solution and the responses at all shifts of a new patch cost a few [FFTs](/fast-fourier-transform/). With the linear kernel the method reduces to a [MOSSE filter](/mosse-filter/) trained on one patch; with a Gaussian kernel it is a nonlinear regression at almost the same cost.

## In plain words

To find the target in the next picture, we train a scorer that says how well a patch is centered on the target. Good examples are the target patch itself; bad examples are copies of it moved a little to the side. KCF uses every possible move as an example, with a score that drops the farther the move is. That many examples would normally make training slow. But all the examples are moves of the same patch, so the comparison between any two of them depends only on the difference of the two moves. That pattern lets the frequency transform do the whole training with one division per frequency, and lets it score every position of the next patch in one go.

## The problem

A patch $x$ is an $r \times c$ real array with $P = r c$ pixels and $r$, $c$ powers of two, indexed modulo its size. The cyclic shift by $d$ is $(S_d x)(t) = x(t - d)$. The training set is $\{ S_d x : d \}$ with labels $y(d) = \exp(-|d|^2 / (2 s^2))$, where $d$ is taken in $[-r/2, r/2) \times [-c/2, c/2)$, so the label is 1 for $d = 0$ and falls off with the size of the shift. Kernel ridge regression with a kernel $\kappa$ and $\lambda > 0$ asks for

$$
f(w) = \sum_e \alpha(e)\, \kappa(w, S_e x), \qquad \alpha = (K + \lambda I)^{-1} y, \qquad K_{d e} = \kappa(S_d x, S_e x),
$$

as given by the [kernel trick](/kernel-trick/). For a new patch $z$, the response at $d$ is $f(S_{-d} z)$: if $z = S_d x$, the target moved by $d$ and the response at $d$ is $f(x)$, close to the peak label.

The key condition is permutation invariance: $\kappa(S_d a, S_d b) = \kappa(a, b)$. It holds for the linear kernel $\langle a, b \rangle / P$ and for the Gaussian kernel $\exp(-|a - b|^2 / (\sigma^2 P))$ (the division by $P$ follows the authors' code). Under it, $K_{d e} = k(e - d)$ with $k(s) = \kappa(x, S_s x)$, so $K$ is circulant. With $\odot$ the entry-by-entry product and $\hat a$ the DFT,

$$
\hat \alpha = \frac{\hat y}{\hat k + \lambda}, \qquad \widehat{\text{resp}} = \hat k_z \odot \overline{\hat \alpha}, \qquad k_z(s) = \kappa(z, S_s x).
$$

Both kernel arrays come from one correlation computed by FFT: $\langle z, S_s x \rangle$ for every $s$ is the inverse transform of $\hat z \odot \overline{\hat x}$, and $|z - S_s x|^2 = |z|^2 + |x|^2 - 2 \langle z, S_s x \rangle$.

## The algorithm

```pseudo id=main
KERNEL(z, x)                                                ▷ k[s] = κ(z, S_s x) for every shift s
L1   c ← IFFT(ẑ ⊙ conj(x̂))                                 ▷ c[s] = ⟨z, S_s x⟩
L2   return exp(-(|z|² + |x|² - 2c) / (σ² P))               ▷ or c / P for the linear kernel

TRAIN(x, y)
L3   k ← KERNEL(x, x)
L4   return α̂ ← ŷ / (k̂ + λ)

DETECT(α̂, x, z)
L5   k_z ← KERNEL(z, x)
L6   return IFFT(k̂_z ⊙ conj(α̂))

TRACK(F_t)                                                  ▷ model x, α̂; position p
L7   resp ← DETECT(α̂, x, features of F_t at p)
L8   p ← p + the shift d of the largest value of resp
L9   x′ ← features of F_t at p;  α̂′ ← TRAIN(x′, y)
L10  x ← (1 - γ) x + γ x′;  α̂ ← (1 - γ) α̂ + γ α̂′
L11  return p
```

The features of a frame at $p$ are a patch centered at $p$ and larger than the target, so that it holds some background, multiplied by a cosine window. The paper uses raw gray values or HOG cells of 4 pixels. Its parameters are $\lambda = 10^{-4}$, the label width $s = \sqrt{w h} / 10$ for a target of $w \times h$ pixels (counted in cells for HOG), $\sigma = 0.2$ and $\gamma = 0.075$ for raw pixels, and $\sigma = 0.5$ and $\gamma = 0.02$ for HOG. For multichannel features, line L1 sums the correlation over the channels.

## Example

**The linear kernel by hand.** Take one row, $r = 1$ and $c = P = 4$, the patch $x = (1, 2, 0, -1)$, the labels $y = (1, 0, 0, 0)$, the linear kernel and $\lambda = 0.1$. The kernel array is $k(s) = \langle x, S_s x \rangle / 4$, the autocorrelation of $x$ divided by 4:

$$
k = (6, 1, -4, 1) / 4 = (1.5, 0.25, -1, 0.25), \qquad \hat k = (1, 2.5, 0, 2.5) .
$$

These are $|\hat x|^2 / 4$, since $\hat x = (2, 1 - 3i, 0, 1 + 3i)$. With $\hat y = (1, 1, 1, 1)$, $\hat \alpha = (1/1.1, 1/2.6, 1/0.1, 1/2.6) = (0.909, 0.385, 10, 0.385)$, and $\alpha = (2.920, -2.273, 2.535, -2.273)$. The response to $x$ itself is $(0.708, 0.227, -0.253, 0.227)$, with the peak at shift 0. For $z = S_1 x = (-1, 1, 2, 0)$ the response is $(0.227, 0.708, 0.227, -0.253)$: the peak has moved to shift 1. The frequency where $\hat x = 0$ gets the large coefficient $1/\lambda$, but in the response it is multiplied by $\hat k_z$, which is 0 there for every shift of $x$.

**Against brute force.** For random $4 \times 8$ patches ($P = 32$), the tests build the $32 \times 32$ matrix $K + \lambda I$ from the definition and solve it directly. The $\alpha$ from line L4 and the responses from line L6 agree with the direct solution to about $10^{-15}$ for both the linear and the Gaussian kernel, and with the linear kernel the responses equal those of primal ridge regression on the 32 shifted patches.

**Tracking.** The frames are $64 \times 64$ with a background of Gaussian blobs and a $13 \times 13$ target with its own blob texture, which moves by $(2.4, 1.7)$ per frame. The features are raw gray values scaled to $[-0.5, 0.5]$ on a $32 \times 32$ patch with a cosine window, with $\sigma = 0.2$, $\lambda = 10^{-4}$, $s = 1.3$ and $\gamma = 0.075$. Over 9 frames, every tracked center is within 1.2 pixels of the truth; the error comes from the integer peak, since the true centers are not on the pixel grid.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). These are theorems.

- **Circulant Gram matrix.** If $\kappa$ is permutation invariant, $K_{d e}$ depends only on $e - d$. This is Theorem 1 of Henriques and colleagues. A kernel that weights pixel positions does not have this property, and the Fourier formulas then do not solve its regression.
- **Diagonalization.** A circulant matrix acts as a circular convolution, so the DFT turns $(K + \lambda I)\alpha = y$ into $(\hat k + \lambda) \odot \hat \alpha = \hat y$. Since $K$ is positive semidefinite, $\hat k \ge 0$, and the division is always defined.
- **Kernel arrays.** Lines L1 and L2 compute $\kappa(z, S_s x)$ for every $s$ exactly, by the correlation theorem.
- **Detection.** Line L6 gives $f(S_{-d} z)$ for every $d$.
- **Linear case.** With the linear kernel, the dual solution and primal ridge regression on the shifted patches give the same function.

These are exact for the training set of cyclic shifts. Real motion brings new content in at the border, so the claim that the response peak is the motion of the target is a heuristic, and the running averages of line L10 are a heuristic as well.

## Complexity

Each kernel array costs two forward FFTs and one inverse FFT, $\Theta(P \log P)$, plus $\Theta(P)$ for the exponentials. TRAIN and DETECT each cost $\Theta(P \log P)$, so a frame costs $\Theta(P \log P)$ and $N$ frames cost $\Theta(N P \log P)$, against $\Theta(P^3)$ per frame for solving the $P \times P$ system directly. With $C$ feature channels the correlation of line L1 costs $\Theta(C P \log P)$. The extra space is $\Theta(P)$ for the model.

## Properties

- **Dense sampling for free.** All $P$ shifts are training samples, and all $P$ positions are scored, at the cost of a few FFTs.
- **Kernel choice.** The Gaussian kernel gives a nonlinear scorer; the linear kernel gives the faster dual correlation filter, which with one channel is a MOSSE filter of one patch.
- **Multichannel.** Features such as HOG enter only through the sum over channels in line L1, and the paper reports a large gain in accuracy over raw pixels.
- **Fixed scale and integer peak.** Like MOSSE, the plain method neither changes the patch size nor locates the peak between pixels.
- **Boundary effect.** The cyclic shifts are not real motions; shifted samples far from 0 wrap the target around the patch border.

## Variants and improvements

- **DCF.** The linear kernel with multichannel features, which avoids the exponentials and is faster than the Gaussian kernel.
- **Scale estimation.** A separate filter over a few scales of the patch, or a search over scaled patches.
- **Spatially regularized filters.** Penalize filter values far from the center, which reduces the boundary effect at the cost of an iterative solver.
- **Subpixel peak.** Fit a parabola to the response near the peak.
- **Learned features.** Use feature maps of a network instead of HOG; [siamese tracking](/siamese-tracking/) takes this further and learns the comparison itself.

## When to use it

Use KCF when you need a fast single-target tracker that runs on a CPU, the target changes slowly, and moves less than about half the patch between frames. It is a common baseline and a clear example of how structure in the data turns a large linear system into FFTs. For large changes of scale or appearance, or for recovery after the target leaves the view, use a re-detection scheme such as [tracking-learning-detection](/tracking-learning-detection/) or a learned tracker.

## Pitfalls

- **A kernel that is not permutation invariant.** The Fourier formulas then compute something, but not the regression on the shifts. Check the condition before using a new kernel.
- **The scale of $\sigma$.** Without the division by $P$, the squared distance grows with the patch size and the Gaussian kernel becomes nearly 0 everywhere. Follow one convention.
- **Shift direction.** Whether the response peak is at $+d$ or $-d$ depends on which side is conjugated. Check it with a known shift, as in the example.
- **Labels with the peak in the middle.** The formulas assume the label peak at shift 0, the corner of the array. A Gaussian centered in the middle of the array gives responses offset by half the patch.
- **Too small a patch.** The target must stay well inside the patch after the move, or the wrapped copies dominate.

## Implementations

## History

Bolme and colleagues introduced the [MOSSE filter](/mosse-filter/) in 2010. In 2012 Henriques, Caseiro, Martins and Batista showed at ECCV that training on all cyclic shifts of a patch gives a circulant data matrix, and used it with a Gaussian kernel on raw pixels (the CSK tracker). Their 2015 journal paper stated the general result for permutation-invariant kernels, added multichannel features such as HOG, and gave the KCF and DCF trackers, which became common baselines for fast tracking. The circulant structure itself is classical; see Gray's review of Toeplitz and circulant matrices.

## References
