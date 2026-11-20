---
tag: FVJ0PD
kind: algorithm
slug: low-rank-plus-sparse-mri
name: Low-rank plus sparse dynamic MRI
aliases:
- L+S reconstruction
area: imaging-and-inverse-problems/mri-reconstruction
level: research
summary: Reconstruct a dynamic image series as the sum of a low rank background and a sparse dynamic part by proximal steps on nuclear and L1 norms.
solves: [mri-reconstruction-problem]
model: real-ram
complexity:
  vars: {n: the number of pixels in one frame, f: the number of frames, c: the number of coils, K: the number of iterations}
  time: {worst: O(K (c f n log n + n f^2 + f^3))}
  space: {extra: O(c f n)}
properties: {deterministic: true, iterative: true, convex: true, monotone: true, online: false, in_place: false}
history:
  year: 2015
  people: [Ricardo Otazo, Emmanuel J. Candès, Daniel K. Sodickson]
  note: Otazo, Candès and Sodickson applied the low rank plus sparse decomposition of robust PCA to undersampled dynamic MRI and solved it by iterative soft thresholding of singular values and of temporal Fourier coefficients.
prereqs: [robust-pca, compressed-sensing-mri, proximal-gradient-method]
see_also: [fista, iterative-shrinkage-thresholding, partial-separability-model, k-t-blast, matrix-completion, loraks, sense, principal-component-analysis]
sources:
  - paper: doi:10.1002/mrm.25240
    title: Ricardo Otazo, Emmanuel Candès and Daniel K. Sodickson, Low-rank plus sparse matrix decomposition for accelerated dynamic MRI with separation of background and dynamic components, Magnetic Resonance in Medicine 73(3), 2015, 1125 to 1136
    locator: Theory, the sections on L+S matrix decomposition and on L+S reconstruction of undersampled dynamic MRI (Table 1) and on the selection of the step size; Methods, image reconstruction (the encoding operator, the transforms and the choice of the weights)
  - paper: doi:10.1145/1970392.1970395
    title: Emmanuel J. Candès, Xiaodong Li, Yi Ma and John Wright, Robust principal component analysis?, Journal of the ACM 58(3), Article 11, 2011
    locator: principal component pursuit and its exact recovery theorem for fully observed matrices (general locator)
  - paper: doi:10.1137/080738970
    title: Jian-Feng Cai, Emmanuel J. Candès and Zuowei Shen, A singular value thresholding algorithm for matrix completion, SIAM Journal on Optimization 20(4), 2010, 1956 to 1982
    locator: the singular value shrinkage operator as the proximal map of the nuclear norm (general locator)
  - paper: doi:10.1137/080716542
    title: Amir Beck and Marc Teboulle, A fast iterative shrinkage-thresholding algorithm for linear inverse problems, SIAM Journal on Imaging Sciences 2(1), 2009, 183 to 202
    locator: the O(1/k) rate of proximal gradient with the step 1/Lip and the accelerated method (general locator)
  - paper: doi:10.1137/050626090
    title: Patrick L. Combettes and Valérie R. Wajs, Signal recovery by proximal forward-backward splitting, Multiscale Modeling and Simulation 4(4), 2005, 1168 to 1200
    locator: convergence of forward-backward splitting for steps below 2/Lip (general locator)
  - paper: doi:10.1109/TMI.2010.2100850
    title: Sajan Goud Lingala, Yue Hu, Edward DiBella and Mathews Jacob, Accelerated dynamic MRI exploiting sparsity and low-rank structure, k-t SLR, IEEE Transactions on Medical Imaging 30(5), 2011, 1042 to 1054
    locator: the joint low rank and sparse penalty on one dynamic series (general locator)
---

Low-rank plus sparse (L+S) reconstruction recovers a dynamic MR image series from undersampled k-space data. It writes the series as $X = L + S$. The part $L$ has low rank as a space by time matrix and holds the background that changes slowly and in the same way everywhere. The part $S$ is sparse after a transform along time and holds the local changes, such as contrast that moves through a vessel. The method minimizes a data term plus the nuclear norm of $L$ and the $\ell_1$ norm of $T S$, one proximal gradient step at a time. The decomposition is that of [robust PCA](/robust-pca/), with two differences: robust PCA sees the whole matrix and its $S$ is sparse in the matrix itself, while L+S sees only Fourier samples of each frame and its $S$ is sparse in a transform. It applies the ideas of [compressed sensing MRI](/compressed-sensing-mri/) to dynamic data.

## In plain words

Think of a cardiac scan as a film. Most of each frame is the same tissue, only a little brighter or darker over time. That part looks almost the same in every frame, so as a table with one column per frame it has only a few independent columns: it has low rank. The rest is small: a few pixels where something moves or where contrast flows in. Along time, these pixels change in a simple pattern, so few temporal frequencies describe them.

L+S keeps two guesses, one for each part. At each step it checks the sum against the measured k-space and corrects it. Then it cleans each part: it shrinks the singular values of the background, and it shrinks the temporal frequencies of the dynamic part. Small values become zero.

## The problem

The input is the undersampled k-space data $d$ of $n_t$ frames, a 0/1 mask $M_t$ for each frame, coil maps $c_1, \ldots, c_{n_c}$ (or one coil with $c = 1$), two weights $\lambda_L, \lambda_S \ge 0$, a step $t > 0$ and an iteration count $K$. A frame has $n$ pixels. The series is the $n \times n_t$ Casorati matrix with one column per frame.

The encoding operator $E$ maps frame $x_t$ and coil $j$ to $M_t F_u (c_j x_t)$, with the unitary 2D DFT $F_u$ ($F_u^H F_u = I$). This is the model of the [MRI reconstruction problem](/mri-reconstruction-problem/) and of [SENSE](/sense/), frame by frame. If $\sum_j |c_j|^2 \le 1$ at every pixel, then $\|E\| \le 1$. The transform $T$ is the unitary DFT along time at each pixel. The output is the pair $(L, S)$ that minimizes, as far as $K$ steps allow,

$$F(L, S) = \tfrac12 \|E(L + S) - d\|^2 + \lambda_L \|L\|_* + \lambda_S \|T S\|_1,$$

where $\|L\|_*$ is the sum of the singular values (the nuclear norm) and $\|\cdot\|_1$ is the sum of the moduli of the complex entries. The image series is $L + S$. $F$ is convex.

## The algorithm

The method is [proximal gradient](/proximal-gradient-method/) in the pair $z = (L, S)$. The data term has the same gradient $\gamma = E^H(E(L + S) - d)$ for $L$ and for $S$. The two penalties act on different variables, so the proximal step splits into singular value thresholding for $L$ and soft thresholding in the transform for $S$.

```pseudo id=main
L+S(d, E, T, lambda_L, lambda_S, t, K)
L1  L <- 0;  S <- 0;  M <- t E^H d         ▷ M = L + S - t gamma at the start
L2  repeat K times
L3      L_new <- SVT(M - S, t lambda_L)     ▷ shrink singular values
L4      S_new <- T^H soft(T(M - L), t lambda_S)   ▷ shrink temporal frequencies
L5      L <- L_new;  S <- S_new
L6      M <- (L + S) - t E^H(E(L + S) - d)   ▷ gradient step on the data term
L7  return L, S
```

Here $\operatorname{SVT}(Z, \tau) = U \operatorname{diag}(\max(\sigma_i - \tau, 0)) V^H$ for the SVD $Z = U \Sigma V^H$, and $\operatorname{soft}(w, \tau) = (w/|w|) \max(|w| - \tau, 0)$ for each complex entry. Note that $M - S = L - t\gamma$ and $M - L = S - t\gamma$, so lines L3 and L4 are the proximal step at the gradient point.

Table 1 of Otazo et al. has this form with $t = 1$ and $M_0 = E^H d$, $S_0 = 0$. The code starts at $L = S = 0$. For SVT it uses the $n_t \times n_t$ Gram matrix of the Casorati matrix, because $n_t$ is small and $n$ is large.

## Example

Take $n_t = 8$ frames of $8 \times 8$ pixels. The background is a disk of 32 pixels with the value 1, scaled in frame $t$ by a contrast curve $1.0, 1.4, 1.7, 1.8, 1.7, 1.5, 1.3, 1.2$. Three pixels inside the disk also oscillate with the amplitude 0.5: pixel $(3, 3)$ as $\cos(2\pi t/8)$, pixel $(3, 4)$ as $\sin(4\pi t/8)$ and pixel $(4, 4)$ as $\cos(6\pi t/8)$. The singular values of the true series are 23.5, 1.00, 0.995, 0.948 and then zero, so it has rank 4. The background alone has rank 1, but the curve makes it dense along temporal frequency.

Each frame keeps 3 of its 8 phase encoding rows, always row 0 and two others chosen at random (seed 1), with a different choice per frame. One coil, $c = 1$. Zero filling, $E^H d$, has a relative error of 0.443. The table gives the relative error of $L + S$ with $t = 0.9$ (measured with the code below):

| method and weights | 10 steps | 50 steps | 200 steps |
|---|---|---|---|
| L+S, $\lambda_L = 0.3$, $\lambda_S = 0.1$ | 0.262 | 0.150 | 0.091 |
| low rank only, $\lambda_L = 0.3$ ($S = 0$) | 0.372 | 0.193 | 0.107 |
| sparse only, $\lambda_S = 0.1$ ($L = 0$) | 0.223 | 0.115 | 0.114 |

After 200 steps, the singular values of $L$ are 22.9, 0.18, 0.07, so $L$ has taken the background, and $S$ holds the three oscillating pixels. On a 3 by 3 grid of weights with 150 steps, the best errors were 0.093 for L+S, 0.107 for the low rank part alone and 0.097 for the sparse part alone. On this small series, the gain of L+S over the better single prior is small. These are measurements on one series, not a theorem.

## Correctness

Three results hold, and all are proved in full below.

- **The steps are proximal maps.** Singular value thresholding is the proximal map of $\tau \|\cdot\|_*$ (Cai, Candès and Shen 2010), and $T^H \operatorname{soft}(T \cdot, \tau)$ is the proximal map of $\tau \|T \cdot\|_1$ for a unitary $T$. So lines L3 to L6 are one proximal gradient step on $F$.
- **Sufficient decrease.** The gradient of the data term in $(L, S)$ is Lipschitz with the constant $2\|E\|^2$, because $L$ and $S$ enter only through their sum. Each step gives $F(z_{k+1}) \le F(z_k) - (1/t - \|E\|^2) \|z_{k+1} - z_k\|^2$. So $F$ does not increase for $t \le 1/\|E\|^2$.
- **Convergence for small steps.** For $t < 1/\|E\|^2$ the iterates converge to a minimizer of $F$ by the general theory of forward-backward splitting (Combettes and Wajs 2005), and for $t \le 1/(2\|E\|^2)$, $F(z_k) - \min F \le \|z_0 - z^\star\|^2 / (2tk)$ (Beck and Teboulle 2009). Otazo et al. cite these results and do not prove convergence themselves.

With $\|E\| = 1$, the step $t = 1$ is the boundary case: $F$ does not increase, but the convergence results above do not apply. None of these results says that the minimizer of $F$ is close to the true series, or that it splits into the true background and dynamic parts. That depends on the sampling and the weights, and it is measured.

## Complexity

Let $n$ be the number of pixels in a frame, $n_t$ the number of frames and $n_c$ the number of coils. One step costs:

- $O(n_c n_t n \log n)$ for $E$ and $E^H$ with the FFT (line L6).
- $O(n n_t \log n_t)$ for $T$ and $T^H$ with the FFT along time (line L4); the code uses a direct DFT when $n_t$ is not a power of two, which costs $O(n n_t^2)$.
- $O(n n_t^2)$ to form the Gram matrix and the product $Z V \operatorname{diag}(g) V^H$ (line L3).
- $O(n_t^3)$ for the eigendecomposition of the Gram matrix with a dense solver. The code uses the cyclic Jacobi method on a $2n_t \times 2n_t$ real matrix, with $O(n_t^3)$ work per sweep and a number of sweeps that is small in practice but not bounded here.

So $K$ steps take $O(K (n_c n_t n \log n + n n_t^2 + n_t^3))$ in the [real RAM](/real-ram/), and the space is $O(n_c n_t n)$ for the data. The number of steps is a measured quantity. Otazo et al. stop when the relative change of $L + S$ falls below $10^{-5}$.

## Properties

- **Convex.** Unlike [LORAKS](/loraks/) and the [partial separability model](/partial-separability-model/) with a fixed rank, the objective is convex, so every local minimizer is global.
- **Two priors at once.** The background and the dynamic part are regularized in different ways and come out as separate images. This separation is useful in itself, for example to view contrast uptake without the background.
- **No training data.** Unlike [k-t BLAST](/k-t-blast/), L+S needs no low resolution training scan.
- **The split is not unique.** A rank one matrix that is also sparse in $T$, such as a constant series in one pixel, can sit in either part. The weights decide where it goes.

## Variants and improvements

- **Other transforms.** Otazo et al. use the temporal Fourier transform for cardiac perfusion and cine, temporal finite differences for abdominal contrast scans, and the identity for angiography, where the images are sparse already. With a transform that is not unitary, line L4 is no longer the exact proximal map.
- **Acceleration.** [FISTA](/fista/) adds a momentum step to the same iteration and improves the rate of $F$ to $O(1/k^2)$. [ADMM](/admm/) and other splitting methods solve the same problem.
- **Low rank and sparse in one variable.** k-t SLR (Lingala et al. 2011) asks one series to be both low rank and sparse, instead of the sum of two parts. Robust PCA on fully sampled data is the case $E = I$ and $T = I$.
- **Explicit low rank models.** The [partial separability model](/partial-separability-model/) fixes the rank and fits temporal basis functions from navigator data. This is a hard rank constraint and not a convex penalty.
- **Non-Cartesian data.** For radial or spiral sampling, $E$ uses a nonuniform FFT and $\|E\|$ must be computed or bounded before $t$ is chosen.

## When to use it

Use L+S for dynamic scans with a background that changes slowly and a dynamic part that is local, such as contrast enhanced perfusion or cine with a static field of view. Use it when you want the background and the dynamic part as separate images. If the whole series is close to low rank, a low rank method alone is simpler. If the motion is large, so that the background does not stay in place, the low rank assumption fails, and methods with motion correction do better.

## Pitfalls

- **The step at the boundary.** With $\|E\| = 1$, the step $t = 1$ of Table 1 sits exactly at $1/\|E\|^2$. On the example above with $\lambda_L = 0.1$, $\lambda_S = 0.01$ and 150 steps, $t = 1$ stopped at the error 0.545, above zero filling, with $F = 74.3$, while $t = 0.5$ reached the error 0.148 and $F = 1.93$. With $\lambda_L = 0.3$ and $\lambda_S = 0.1$, $t = 1$ worked well (0.094). Use $t < 1/\|E\|^2$, or check the result against a smaller step.
- **The weights are choices.** Otazo et al. pick $\lambda_L$ and $\lambda_S$ by hand for each kind of scan, after they scale the data by its largest magnitude. Their values are $\lambda_L = \lambda_S = 0.01$ for cardiac perfusion and $\lambda_L = 0.0025$, $\lambda_S = 0.00125$ for cine. They also report that the weight from the robust PCA theory did not work directly for undersampled data.
- **The norm of $E$.** The step bound uses $\|E\|$. Coil maps that are not normalized, or a Fourier transform that is not unitary, change $\|E\|$ and can make the steps too long.
- **The complex SVD.** A real SVD of the real and imaginary parts as separate columns is not the complex SVD. The code embeds the complex Gram matrix as a real symmetric matrix of twice the size, where each eigenvalue appears twice.
- **Leakage between the parts.** If $\lambda_S$ is small, $S$ takes the background too; if $\lambda_L$ is small, $L$ takes the dynamic part. The separation in the images is only as good as this balance.

## Implementations

## History

Robust PCA, the split of a matrix into a low rank part and a sparse part by the nuclear norm plus the $\ell_1$ norm, was analyzed by Candès, Li, Ma and Wright and by Chandrasekaran and coauthors around 2009 to 2011. In MRI, low rank models of dynamic data go back to the partial separability model of Liang (2007), and Lingala et al. (2011) combined low rank and sparse penalties on one series in k-t SLR. Otazo, Candès and Sodickson published L+S in Magnetic Resonance in Medicine in 2015. They used it on cardiac perfusion and cine, abdominal and breast contrast scans and angiography, with Cartesian and radial sampling, and they gave a simple iterative soft thresholding algorithm.

## References
