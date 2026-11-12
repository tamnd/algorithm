---
tag: RPTZE3
kind: algorithm
slug: independent-component-analysis
name: Independent component analysis
aliases:
- ICA
- linear ICA
area: machine-learning/dimensionality-reduction
level: core
summary: "Recover independent non-Gaussian sources s from mixtures x = A s, up to order and scale. Whiten the data, then rotate it to maximize non-Gaussianity such as kurtosis."
solves: [blind-source-separation]
model: real-ram
complexity:
  vars: {n: the number of observations, d: "the number of sources and of mixtures", S: the number of Jacobi sweeps, G: the number of trial angles per pair}
  time: {worst: "O(n d^2 + d^3 + S d^2 (n + G))"}
  space: {extra: "Θ(n d + d^2)"}
properties: {deterministic: true, online: false, exact: false, recursive: false, supervised: false, linear: true}
history:
  year: 1994
  people: [Pierre Comon, Christian Jutten, Jeanny Hérault]
  note: Jutten and Hérault built the first neural separation rule in the 1980s. Comon defined ICA in 1994, proved identifiability, and gave a contrast-based Jacobi algorithm.
prereqs: [covariance-matrix, whitening]
see_also: [blind-source-separation, fastica, projection-pursuit, principal-component-analysis, factor-analysis, nonnegative-matrix-factorization, jacobi-eigenvalue-algorithm, central-limit-theorem]
sources:
  - paper: doi:10.1016/0165-1684(94)90029-9
    title: Pierre Comon, Independent component analysis, a new concept?, Signal Processing 36(3), 1994
    locator: pp. 287 to 314 (the definition, contrast functions, Theorem 11 on identifiability, the pairwise Jacobi algorithm)
  - book: isbn:9780471405405
    title: Aapo Hyvärinen, Juha Karhunen and Erkki Oja, Independent Component Analysis, Wiley, 2001
    locator: Chapter 7 (the model and its ambiguities), Chapter 8 (ICA by maximization of non-Gaussianity), Chapter 11 (tensorial methods and JADE)
  - paper: doi:10.1016/S0893-6080(00)00026-5
    title: Aapo Hyvärinen and Erkki Oja, Independent component analysis, algorithms and applications, Neural Networks 13(4-5), 2000
    locator: pp. 411 to 430 (kurtosis, negentropy, whitening, FastICA)
  - paper: doi:10.1162/neco.1995.7.6.1129
    title: Anthony J. Bell and Terrence J. Sejnowski, An information-maximization approach to blind separation and blind deconvolution, Neural Computation 7(6), 1995
    locator: pp. 1129 to 1159 (the infomax rule)
  - paper: doi:10.1049/ip-f-2.1993.0054
    title: Jean-François Cardoso and Antoine Souloumiac, Blind beamforming for non-Gaussian signals, IEE Proceedings F 140(6), 1993
    locator: pp. 362 to 370 (JADE, joint diagonalization of cumulant matrices)
  - paper: doi:10.1016/0165-1684(91)90079-X
    title: Christian Jutten and Jeanny Hérault, Blind separation of sources, part I, Signal Processing 24(1), 1991
    locator: pp. 1 to 10 (the adaptive neuromimetic separation rule)
---

Independent component analysis (ICA) is an unsupervised linear method. It assumes that the observed vectors are linear mixtures $x = A s$ of $d$ hidden sources $s_1, \ldots, s_d$ that are statistically independent and non-Gaussian, and it estimates an unmixing matrix $B$ such that $B x$ recovers the sources up to their order, scale and sign. It is the standard method for [blind source separation](/blind-source-separation/). [Principal component analysis](/principal-component-analysis/) only makes the components uncorrelated, and that fixes the answer only up to a rotation. ICA uses higher-order statistics to choose the rotation. This page gives the model, Comon's identifiability result, the usual contrasts (kurtosis and negentropy), and Comon's pairwise Jacobi algorithm. The fixed-point method is on the [FastICA](/fastica/) page.

## In plain words

Several microphones record several people who talk at the same time. Each microphone hears a different blend of the voices. ICA tries to undo the blend when it knows neither the voices nor the blend. Its only clue is that the voices are independent of each other.

The key fact is that a blend of independent signals looks more like the bell curve than the signals do. So ICA turns the recorded data until each output looks as far from the bell curve as possible. It first removes the simple correlations, which leaves only a turn to find. Then it tries turns on two outputs at a time and keeps each turn that makes the outputs less bell shaped.

## The problem

The data are $n$ observations $x_1, \ldots, x_n \in \mathbb{R}^d$. The model is
$$ x = A s , $$
where $A$ is an unknown invertible $d \times d$ mixing matrix and $s = (s_1, \ldots, s_d)$ is a random vector with independent components. The scale of each source is not identifiable, because $A s = (A D)(D^{-1} s)$ for every invertible diagonal $D$, so the convention is $E[s_j] = 0$ and $\operatorname{Var}(s_j) = 1$. The order is not identifiable either. The goal is a matrix $B$ with
$$ B A = \Pi D , $$
with $\Pi$ a permutation and $D$ diagonal; with the unit-variance convention, $D$ has entries $\pm 1$.

**Identifiability** (Comon 1994, Theorem 11). If at most one source is Gaussian, then every $B$ that makes the components of $B x$ pairwise independent has the form above. The proof uses the Darmois-Skitovich theorem. If two sources are Gaussian, any rotation of them is again a pair of independent Gaussians, so they cannot be separated.

**Contrasts.** Since independence cannot be measured directly from a sample, ICA maximizes a contrast, a function of the output distribution that is largest at the separated solution. Two contrasts are standard.

- **Kurtosis.** The fourth cumulant $\operatorname{kurt}(u) = E[u^4] - 3 (E[u^2])^2$ is 0 for a Gaussian, negative for flat variables such as the uniform (sub-Gaussian), and positive for peaked variables such as the Laplace (super-Gaussian). For independent sources, $\operatorname{kurt}(\sum_j p_j s_j) = \sum_j p_j^4 \operatorname{kurt}(s_j)$.
- **Negentropy.** $J(u) = H(u_{\text{gauss}}) - H(u)$, where $H$ is the differential entropy and $u_{\text{gauss}}$ is a Gaussian with the same variance. It is never negative, and it is 0 only for a Gaussian, because the Gaussian has the largest entropy for a given variance. Minimizing the mutual information of whitened outputs is the same as maximizing the sum of their negentropies. In practice negentropy is approximated, for example by $J(u) \approx c\,(E[G(u)] - E[G(\nu)])^2$ with $\nu$ standard Gaussian and $G(u) = \log \cosh u$.

## The algorithm

The algorithm first [whitens](/whitening/) the data, so that the remaining unknown is an orthogonal matrix, and then it applies plane rotations to pairs of components in sweeps, like the [Jacobi eigenvalue algorithm](/jacobi-eigenvalue-algorithm/). Each rotation maximizes the fourth-order contrast $\Phi(y) = \sum_i \operatorname{kurt}(y_i)^2$ over the angle.

```pseudo id=main
ICA-JACOBI(X)
L1  μ ← mean of X;  C ← covariance of X = E Λ Eᵀ;  V ← Λ^(−1/2) Eᵀ;  z_t ← V (x_t − μ) for all t
L2  W ← I
L3  repeat                                                            ▷ one sweep
L4      for each pair i < j do
L5          θ ← the angle in [0, π/2) that maximizes kurt(y_i)² + kurt(y_j)² for y_i = cos θ z_i + sin θ z_j, y_j = −sin θ z_i + cos θ z_j
L6          if this increases the contrast, replace rows i and j of z and of W by the rotated rows
L7  until no rotation in a sweep increases the contrast by more than tol
L8  return B = W V and the components z
```

In line L5 the rows $z_i$ and $z_j$ have sample variance 1 and covariance 0, so each kurtosis is a quartic polynomial in $(\cos\theta, \sin\theta)$ whose coefficients are the five sample moments $m_a = \overline{z_i^a z_j^{4-a}}$. The implementation computes these in one pass and then searches a fine grid of angles that includes $\theta = 0$, followed by a golden section refinement. Closed-form angle rules also exist, for example in JADE; the grid keeps the code short and makes the step monotone by construction. An estimate of the sources for a new point $x$ is $B(x - \mu)$.

## Example

Take a uniform source with variance 1 ($\kappa_1 = -1.2$) and a Laplace source with variance 1 ($\kappa_2 = 3$). After whitening, the data are $z = P s$ for an unknown rotation $P$ by the angle $\varphi$. By the additivity rule, the two components have kurtoses $\kappa_1 \cos^4\varphi + \kappa_2 \sin^4\varphi$ and $\kappa_1 \sin^4\varphi + \kappa_2 \cos^4\varphi$.

| $\varphi$ | kurt of $z_1$ | kurt of $z_2$ | contrast $\Phi$ |
|---|---|---|---|
| 0° | −1.2 | 3.0 | 10.44 |
| 15° | −1.031 | 2.606 | 7.855 |
| 30° | −0.488 | 1.613 | 2.838 |
| 45° | 0.45 | 0.45 | 0.405 |

At 45° both mixtures have the same small kurtosis 0.45, so they look much more Gaussian than either source. The contrast is largest, 10.44, exactly when the rotation is undone. Theorem 1 of the proof shows that this holds for any number of sources: $\Phi \le \sum_j \kappa_j^2$, with equality only at signed permutations.

On a sample of 2000 points of this kind, mixed by a 45° rotation, the sample kurtoses of the sources are −1.23 and 1.86; the Laplace estimate is noisy because of its heavy tails. Line L1 gives components with contrast 1.96. One rotation raises it to 5.61, and the sweep after it makes no change. The product of the estimated unmixing matrix and the true mixing matrix is
$$ B A \approx \begin{pmatrix} 0.995 & 0.016 \\ 0.057 & -1.022 \end{pmatrix} , $$
so the first output is the uniform source and the second is the Laplace source with its sign flipped.

## Correctness

Whitening makes $z = Q s$ with $Q$ orthogonal, so every later step is a rotation and the outputs stay uncorrelated with unit variance. By the additivity rule for the fourth cumulant, $\Phi(P s) = \sum_i (\sum_j P_{ij}^4 \kappa_j)^2$, and two applications of the Cauchy-Schwarz inequality with $\sum_j P_{ij}^4 \le 1$ give $\Phi \le \sum_j \kappa_j^2$. Equality forces each column of $P$ with $\kappa_j \ne 0$ to be a signed unit vector, so if at most one source has kurtosis 0, the maximizers are exactly the signed permutations. Each Jacobi step searches over angles that include 0, so the sample contrast never decreases. The full proofs are below.

## Complexity

The model is the [real RAM](/real-ram/), and the costs count arithmetic operations.

- **Whitening.** $\Theta(n d^2)$ for the covariance and to apply $V$, and $O(d^3)$ for a [symmetric eigendecomposition](/symmetric-eigenproblem/).
- **One pair step.** $\Theta(n)$ for the five moments, $\Theta(G)$ to search $G$ angles, and $\Theta(n)$ to rotate two rows.
- **Total.** A sweep has $d(d-1)/2$ pair steps, so $S$ sweeps cost $O(n d^2 + d^3 + S d^2 (n + G))$. In practice a few sweeps are enough. The extra memory is $\Theta(n d + d^2)$.

## Properties

- **Ambiguities.** The order, scale and sign of the sources cannot be found. The variance of each output is fixed at 1.
- **At most one Gaussian source.** Gaussian sources can be found only as a group, as a subspace with no preferred rotation.
- **The mixing matrix does not matter much.** Whitening reduces every invertible $A$ to a rotation, and the contrast of a rotation of $s$ depends only on $s$. So a badly conditioned $A$ does not harm the separation in the population, apart from numerical effects.
- **Second order is not enough.** Every rotation of whitened data has the same covariance $I$. All the information that fixes the rotation is in the higher-order statistics.
- **Not dimensionality reduction by itself.** The basic model is square. To find $k < d$ sources, first reduce to $k$ dimensions with PCA.

## Variants and improvements

- **FastICA.** A fixed-point iteration that maximizes a negentropy approximation one component at a time or all at once, with cubic convergence for the kurtosis nonlinearity. See [FastICA](/fastica/).
- **Infomax and maximum likelihood.** Bell and Sejnowski (1995) maximize the output entropy of a neural network with a sigmoid output; this is the maximum likelihood estimator for a fixed source density. The natural gradient form of Amari, Cichocki and Yang removes the matrix inverse from the update.
- **JADE.** Cardoso and Souloumiac (1993) jointly diagonalize a set of fourth-order cumulant matrices with Jacobi rotations. It is the matrix form of the method on this page.
- **Time structure.** If the sources are time series with different spectra, second-order methods such as AMUSE and SOBI separate them even when they are Gaussian. See [blind source separation](/blind-source-separation/).
- **Projection pursuit.** Finding one direction of maximal non-Gaussianity is [projection pursuit](/projection-pursuit/) with negentropy as the index.
- **Overcomplete and noisy ICA.** More sources than sensors, or $x = A s + \varepsilon$, need a prior on $s$ and are much harder.

## When to use it

Use ICA when the data are a linear, instantaneous mixture of independent sources and the sources are not Gaussian: EEG and MEG artifact removal, the separation of audio recorded by several microphones in a room without echo, fMRI components, and the analysis of financial returns. It also finds edge-like filters in natural image patches. Do not use it when the mixing is convolutive (echoes), when the sources are nearly Gaussian, or when the number of samples is small compared with the fourth moments that must be estimated.

## Pitfalls

- **Skipping whitening.** Rotations preserve the contrast only for whitened data. Without whitening, the search space is all invertible matrices.
- **Zero kurtosis.** The kurtosis contrast cannot see a non-Gaussian source with kurtosis 0. Negentropy-based contrasts do not have this blind spot.
- **Outliers.** Sample kurtosis depends on fourth powers, so a few large values can dominate it. Robust nonlinearities such as $\log\cosh$ are safer.
- **Local maxima.** With more than two sources the Jacobi sweeps can stop at a local maximum. Restart from a random rotation and keep the best contrast.
- **Order and sign.** Comparing runs, or matching outputs to known sources, needs a matching step, or a score that ignores order and sign such as the Amari index of $B A$.
- **Dependent sources.** If the sources are not independent, ICA still returns maximally non-Gaussian directions, but they need not mean anything.

## Implementations

## History

Hérault and Jutten proposed an adaptive neural network for source separation in the mid 1980s, and published the method in detail in 1991. Pierre Comon named and defined independent component analysis in a 1994 paper. He proved that the model is identifiable when at most one source is Gaussian, introduced contrast functions, and gave a Jacobi algorithm on pairs of components. Cardoso and Souloumiac gave JADE in 1993, Bell and Sejnowski gave the infomax rule in 1995, and Hyvärinen and Oja gave FastICA in 1997. The 2001 book of Hyvärinen, Karhunen and Oja collected the theory.

## References
