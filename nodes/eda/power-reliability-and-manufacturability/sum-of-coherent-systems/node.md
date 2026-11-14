---
tag: 5NQR8Z
kind: algorithm
slug: sum-of-coherent-systems
name: Sum of coherent systems
aliases:
- SOCS
- Cobb decomposition
area: eda/power-reliability-and-manufacturability
level: advanced
summary: Cobb's fast lithography simulation that eigendecomposes the TCC and approximates the aerial image by a few coherent kernels convolved with the mask.
model: word-ram
complexity:
  vars: {N: the number of frequencies in the band of the TCC, S: the number of source points, w: the number of Jacobi sweeps, K: the number of kernels kept, n: the number of image points}
  time: {build: "O(S N^2 + w N^3)", query: "O(K n log n)"}
  space: {extra: "O(N^2 + K n)"}
properties: {deterministic: true, exact: false, recursive: false, online: false}
history:
  year: 1998
  people: [Nicolas Bailey Cobb]
  note: Cobb named the sum of coherent systems and used it for fast optical proximity correction in his 1995 report and 1998 thesis at Berkeley; the eigen-expansion of partial coherence goes back to Gamo (1964), and Pati and Kailath (1994) used optimal coherent approximations of the Hopkins model for mask design.
prereqs: [hopkins-imaging-model, spectral-theorem, jacobi-eigenvalue-algorithm]
see_also: [optical-proximity-correction, inverse-lithography-technology, singular-value-decomposition, power-iteration, fast-fourier-transform, convolution, positive-definite-matrix, discrete-fourier-transform]
sources:
  - paper: "Nicolas Bailey Cobb, Fast Optical and Process Proximity Correction Algorithms for Integrated Circuit Manufacturing, PhD thesis, Department of Electrical Engineering and Computer Sciences, University of California at Berkeley, 1998"
    locator: the decomposition of the Hopkins imaging equation into a sum of coherent systems (SOCS), computed from the matrix of transmission cross coefficients by the singular value decomposition, and its use for fast aerial image computation in proximity correction
  - paper: doi:10.1016/S0079-6638(08)70571-7
    title: Hideya Gamo, Matrix treatment of partial coherence, Progress in Optics 3, 187 to 332, 1964
    locator: the mutual intensity of partially coherent light treated as a Hermitian matrix and expanded in its eigenvectors, the decomposition that SOCS starts from
  - paper: doi:10.1364/JOSAA.11.002438
    title: Y. C. Pati and T. Kailath, Phase-shifting masks for microlithography, automated design and mask requirements, Journal of the Optical Society of America A 11(9), 2438 to 2452, 1994
    locator: optimal coherent approximations of partially coherent imaging systems in the Hopkins model, used to reduce mask design to phase retrieval
  - paper: doi:10.1007/BF02288367
    title: Carl Eckart and Gale Young, The approximation of one matrix by another of lower rank, Psychometrika 1(3), 211 to 218, 1936
    locator: the best approximation of a matrix by one of lower rank is the truncation of its singular value decomposition
---

The sum of coherent systems, or SOCS, computes the aerial image of a photomask under partially coherent light as a weighted sum of a few coherent images. It starts from the [Hopkins imaging model](/hopkins-imaging-model/), where the image is a quadratic form in the mask spectrum with a Hermitian positive semidefinite kernel, the transmission cross coefficient (TCC). The eigendecomposition of the TCC turns the quadratic form into a sum of squared moduli of linear filters of the mask, and keeping the $K$ largest eigenvalues gives an approximation whose error is set by the eigenvalues left out. Cobb named the method and made it the engine of fast model-based [optical proximity correction](/optical-proximity-correction/). That page shows where SOCS sits in the correction loop; this page gives the algorithm, proves that it is exact at full rank, and bounds the error of the truncation.

## In plain words

Partially coherent light comes from many source points at once. Each point makes its own sharp image of the mask, and the camera sees the sum of their brightnesses. Computing one image per source point works, but it needs many images.

The trick is to change the basis. The light that the source and lens let through can be described by a table that does not depend on the mask. Breaking that table into its eigenvectors gives a new set of "virtual sources". Each one is still a sharp, coherent system: filter the mask, take the squared size of the result. But now the systems are sorted by how much light they carry, and the light falls off fast.

So a handful of filters gives nearly the whole image. The filters are computed once for a scanner setting and reused for every mask.

## The problem

Work in one dimension with a mask of period $P$; two dimensions only change the index set. The mask has Fourier coefficients $M(f)$ at the frequencies $f = k/P$. The source is a set of points $s$ with weights $J(s) \ge 0$, and the pupil is a function $H(f)$ that vanishes for $|f| > \mathrm{NA}/\lambda$. Let $f_1, \dots, f_N$ be the frequencies in the band where the TCC can be nonzero, $|f| \le (1 + \sigma)\mathrm{NA}/\lambda$ for a source of radius $\sigma \mathrm{NA}/\lambda$ (the band limit of the Hopkins page). The TCC is the $N \times N$ matrix

$$ T_{ab} = \sum_s J(s)\, H(f_a + s)\, \overline{H(f_b + s)}, $$

and the Hopkins image is

$$ I(x) = \sum_{a, b} T_{ab}\, M(f_a)\, \overline{M(f_b)}\, e^{2\pi i (f_a - f_b) x}. $$

**Input:** the source, the pupil, the band, a number $K \le N$ of kernels, a mask and the image points $x$. **Output:** the image $I_K(x)$, an approximation of $I(x)$ that uses $K$ coherent systems, together with the eigenvalues of $T$, which measure the error.

## The algorithm

```pseudo id=main
SUM-OF-COHERENT-SYSTEMS(source J, pupil H, band f_1..f_N, K, mask, points x)
L1  T[a][b] ← Σ_s J(s) H(f_a + s) conj(H(f_b + s))   for all a, b
L2  (λ, V) ← eigenpairs of the Hermitian matrix T by complex Jacobi rotations
L3  sort the pairs so that λ_1 ≥ λ_2 ≥ ... ≥ λ_N
L4  keep the kernels (λ_j, v_j) for j = 1..K
L5  M(f_a) ← Fourier coefficients of the mask on the band
L6  for j = 1..K
L7      E_j(x) ← Σ_a v_j(a) M(f_a) e^{2πi f_a x}
L8  return I_K(x) = Σ_{j ≤ K} λ_j |E_j(x)|^2
```

Lines L1 to L4 are the setup, done once for a source, pupil and band. Lines L5 to L8 run for every mask. The vector $v_j$ is the spectrum of the $j$th kernel $\phi_j$, so line L7 is the [convolution](/convolution/) $E_j = \phi_j * m$, computed as a pointwise product of spectra and one inverse [fast Fourier transform](/fast-fourier-transform/) on the image grid.

Line L2 uses the [Jacobi eigenvalue algorithm](/jacobi-eigenvalue-algorithm/) in its complex Hermitian form. For a pivot $T_{pq} = r e^{i\varphi}$ with $r > 0$, the rotation acts on rows and columns $p$ and $q$ as $U = W R$, where $W = \operatorname{diag}(1, e^{-i\varphi})$ makes the pivot real and $R = \begin{pmatrix} c & s \\ -s & c \end{pmatrix}$ with $c = 1/\sqrt{t^2 + 1}$, $s = tc$ and

$$ t = \frac{\operatorname{sgn}(\theta)}{|\theta| + \sqrt{\theta^2 + 1}}, \qquad \theta = \frac{T_{qq} - T_{pp}}{2r}, $$

zeroes it. The rotations sweep over all pairs until the off-diagonal part is negligible. Any Hermitian eigensolver can take its place, and for large $N$ one that finds only the top $K$ pairs is better (see the variants).

## Example

Take units with $\mathrm{NA}/\lambda = 1$, the ideal pupil $H = 1$ on $[-1, 1]$, period $P = 2$, and three source points $s \in \{-\frac12, 0, \frac12\}$ with weight $\frac13$ each, so $\sigma = \frac12$. The band is $|k/2| \le \frac32$, that is $k = -3, \dots, 3$, and $N = 7$.

Source point $s$ passes the frequencies $k/2$ with $|k/2 + s| \le 1$: $s = \frac12$ passes $k \in \{-3, \dots, 1\}$, $s = 0$ passes $\{-2, \dots, 2\}$ and $s = -\frac12$ passes $\{-1, \dots, 3\}$. Write $h_+$, $h_0$, $h_-$ for the indicator vectors of these sets. Then $T = \frac13 (h_+ h_+^{\mathsf T} + h_0 h_0^{\mathsf T} + h_- h_-^{\mathsf T})$, and each entry is $\frac13$ times the number of source points that pass both frequencies:

| $k$ | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ | $3$ |
|---|---|---|---|---|---|---|---|
| $-3$ | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| $-2$ | 1 | 2 | 2 | 2 | 2 | 1 | 0 |
| $-1, 0, 1$ | 1 | 2 | 3 | 3 | 3 | 2 | 1 |
| $2$ | 0 | 1 | 2 | 2 | 2 | 2 | 1 |
| $3$ | 0 | 0 | 1 | 1 | 1 | 1 | 1 |

(entries times $\frac13$). The rank is $3$, since $T$ is a sum of three rank-one terms, and the trace is $5$.

*Eigenvalues by hand.* The vector $d = h_+ - h_- = (1, 1, 0, 0, 0, -1, -1)$ has $h_+ \cdot d = 2$, $h_0 \cdot d = 0$ and $h_- \cdot d = -2$, so $T d = \frac13 (2 h_+ - 2 h_-) = \frac23 d$. The even vectors $h_0$ and $g = h_+ + h_-$ span an invariant plane: from the inner products $h_0 \cdot h_0 = h_+ \cdot h_+ = 5$, $h_0 \cdot h_\pm = 4$ and $h_+ \cdot h_- = 3$,

$$ T h_0 = \tfrac13 (5 h_0 + 4 g), \qquad T g = \tfrac13 (8 h_0 + 8 g). $$

The matrix $\frac13 \begin{pmatrix} 5 & 8 \\ 4 & 8 \end{pmatrix}$ has trace $\frac{13}{3}$ and determinant $\frac89$, so its eigenvalues are $\frac{13 \pm \sqrt{137}}{6}$. In order, $\lambda_1 = 4.11745$, $\lambda_2 = \frac23$, $\lambda_3 = 0.21588$, and $\lambda_4 = \dots = \lambda_7 = 0$. They add up to the trace $5$. Jacobi gives the same values to $10^{-12}$.

*Images.* Take equal lines and spaces, $m = 1$ on $[-\frac12, \frac12]$ in each period, so $M(0) = \frac12$, $M(\pm 1) = \frac1\pi$, $M(\pm 2) = 0$ and $M(\pm 3) = -\frac{1}{3\pi}$. At the center of the line, the edge, and the center of the space:

| $x$ | $0$ | $0.5$ | $1$ |
|---|---|---|---|
| $I_1$ | $1.138562$ | $0.249594$ | $0.004603$ |
| $I_2$ | $1.138562$ | $0.257099$ | $0.004603$ |
| $I_3$ | $1.138611$ | $0.257505$ | $0.006842$ |
| direct Hopkins $I$ | $1.138611$ | $0.257505$ | $0.006842$ |

With three kernels the image is exact, since the rank is three. The second kernel $d/2$ is odd, and the mask is even about $x = 0$ and $x = 1$, so $E_2$ vanishes there and adds only at the edge. One kernel is already within $0.008$ of the image, far below the guaranteed bound $\lambda_2 \sum |M|^2 = \frac23 \cdot 0.4752 = 0.3168$. The bound is reached only by the worst mask, as the correctness section shows.

## Correctness

The full proof is in the [correctness proof](proofs/correctness/). Write the image at a point $x$ as $I(x) = u^* T u$ with $u_a = \overline{M(f_a)} e^{-2\pi i f_a x}$. Since $T$ is Hermitian and positive semidefinite (proved on the [Hopkins page](/hopkins-imaging-model/)), the [spectral theorem](/spectral-theorem/) gives $T = \sum_j \lambda_j v_j v_j^*$ with $\lambda_j \ge 0$. Then $u^* v_j v_j^* u = |v_j^* u|^2 = |E_j(x)|^2$, so $I = \sum_j \lambda_j |E_j|^2$ exactly, and the truncation error is

$$ I(x) - I_K(x) = u^* (T - T_K) u = \sum_{j > K} \lambda_j |E_j(x)|^2 , \qquad T_K = \sum_{j \le K} \lambda_j v_j v_j^*. $$

This gives three facts. The error is never negative, so $I_K$ underestimates the image. It is at most $\lambda_{K+1} \sum_a |M(f_a)|^2$, which is at most $\lambda_{K+1}$ for any mask with $|m| \le 1$ by Parseval. The factor $\lambda_{K+1}$ is the spectral norm $\|T - T_K\|_2$, and the bound is attained at $x = 0$ by a mask whose band spectrum is a multiple of $\overline{v_{K+1}}$. Summed over the $N$ single-frequency masks, the error at any point is $\sum_{j > K} \lambda_j$, the trace norm $\|T - T_K\|_*$; this is also the mean error for random coefficients with $\mathbb{E}[u u^*] = I$. By the theorem of Eckart and Young and its extension by Mirsky, $T_K$ is the best rank-$K$ approximation of $T$ in both norms, so no other $K$ coherent systems built from a rank-$K$ kernel do better in these measures. Finally, for $S$ source points, $T$ is a sum of $S$ rank-one matrices, so $\operatorname{rank} T \le S$ and $K = S$ kernels are exact.

## Complexity

- **Setup.** Line L1 adds $S$ rank-one terms of size $N \times N$: $O(S N^2)$. Each Jacobi sweep visits $N(N-1)/2$ pairs at $O(N)$ each, so $w$ sweeps cost $O(w N^3)$. Cyclic Jacobi converges quadratically in the end, so $w$ is small in practice (it is under $10$ in the tests). Storage is $O(N^2)$.
- **Per mask.** Line L5 is one forward transform. Each kernel needs $N$ products and one inverse transform onto $n$ image points, $O(n \log n)$, so the image costs $O(K n \log n)$. The direct Hopkins sum needs $N^2$ products per image instead, and Abbe's method one transform per source point, $O(S n \log n)$. In two dimensions $N$ grows with the square of the period while $K$ stays near ten for typical settings, which is the source of the speed-up.

## Properties

- **Exact at full rank.** With $K = \operatorname{rank} T$ the output is the Hopkins image. With smaller $K$ it is a lower approximation, which is why the property `exact` is false.
- **Monotone in $K$.** Each added kernel adds $\lambda_j |E_j|^2 \ge 0$, so the error falls with $K$ at every point.
- **Mask independent setup.** The kernels depend only on the source, pupil and band.
- **Kernels are defined up to phase.** If $v_j$ is an eigenvector, so is $e^{i\alpha} v_j$, and $|E_j|^2$ does not change. Equal eigenvalues allow any orthonormal basis of the eigenspace.
- **Deterministic.** The eigensolver and the transforms are deterministic.

## Variants and improvements

- **Singular value decomposition.** Cobb computed the kernels with the [singular value decomposition](/singular-value-decomposition/) of the TCC matrix. For a Hermitian positive semidefinite matrix it equals the eigendecomposition.
- **Top-$K$ eigensolvers.** Only $K$ pairs are needed, so [power iteration](/power-iteration/) with deflation, subspace iteration or Lanczos replace the full solver when $N$ is large. Matrix-vector products with $T$ cost $O(S N)$ through its factored form $\sum_s J(s) h_s h_s^*$.
- **Factored form.** The same factored form shows that the kernels are the left singular vectors of the $N \times S$ matrix with columns $\sqrt{J(s)}\, h_s$, and the eigenvalues are the squared singular values. A thin decomposition of that matrix costs $O(N S \min(N, S))$ and avoids forming $T$.
- **Optimal coherent approximation.** Pati and Kailath (1994) kept one or a few coherent systems of this kind to turn mask design into a phase retrieval problem.
- **Kernels in space.** Instead of transforms, each kernel can be convolved once with basic shapes and stored in tables, so that the field of a polygon mask is a sum of table values. This suits sparse evaluation at the sites used by [optical proximity correction](/optical-proximity-correction/).
- **Gradients for mask optimization.** Since $I_K = \sum_j \lambda_j |\phi_j * m|^2$, the gradient of a weighted image $\int w(x) I_K(x)\, dx$ with respect to a real mask is $2 \sum_j \lambda_j \operatorname{Re}\big(\tilde\phi_j * (w \cdot (\phi_j * m))\big)$, with $\tilde\phi_j(x) = \overline{\phi_j(-x)}$. So one gradient costs about two transforms per kernel. [Inverse lithography](/inverse-lithography-technology/) uses this form.
- **Focus and dose.** Defocus changes the pupil phase, so each focus setting has its own TCC and kernels.

## When to use it

Use it when many masks are imaged with the same optics: proximity correction, inverse lithography and lithography verification over a full chip. Choose $K$ from the eigenvalues, for example the least $K$ with $\sum_{j > K} \lambda_j$ below a tolerance times the trace. When the source itself changes at every step, as in source and mask optimization, the setup is repeated each time, and Abbe's method over source points is often simpler.

## Pitfalls

- **Band too small.** The band must reach $(1 + \sigma)\mathrm{NA}/\lambda$. A smaller band drops terms of $T$ that are not small, and no choice of $K$ recovers them.
- **Error in the image, not the edge.** The bound is on intensity. Where the image is flat near the resist threshold, a small intensity error moves the printed edge far.
- **Periodic boundaries.** The transform treats the mask as periodic. Pad the simulation region by the reach of the kernels, or a feature wraps around.
- **Tiny negative eigenvalues.** Rounding can give eigenvalues just below zero. Set them to zero; they do not belong to the kernel set.
- **Comparing kernels.** Kernels from two settings may differ by a phase or by a rotation within an eigenspace. Compare images or projectors $v_j v_j^*$, not raw kernels.
- **Normalization.** Divide by the clear-field image $T(0, 0)$, as on the Hopkins page, before applying a resist threshold.

## Implementations

## History

Hopkins (1953) wrote partially coherent imaging with a kernel that does not depend on the object. Gamo (1964) treated the mutual intensity of partially coherent light as a Hermitian matrix and expanded it in eigenvectors. Pati and Kailath (1994) applied optimal coherent approximations of the Hopkins model to the design of phase-shifting masks. Cobb, in a 1995 Berkeley report and his 1998 thesis, called the decomposition the sum of coherent systems, computed it with the singular value decomposition of the TCC matrix, and built fast proximity correction on it. It became the standard aerial image engine of full-chip OPC tools.

## References
