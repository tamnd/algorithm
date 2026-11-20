---
tag: MVRMMT
kind: algorithm
slug: k-t-blast
name: k-t BLAST
aliases:
- k-t SENSE
area: imaging-and-inverse-problems/mri-reconstruction
level: advanced
summary: Undersample dynamic MRI in k-space and time on a lattice and unfold the aliases in x-f space with a prior from low resolution training data.
solves: [mri-reconstruction-problem]
model: real-ram
complexity:
  vars: {n: the number of pixels in one frame, f: the number of frames, c: the number of coils, R: the acceleration factor}
  time: {worst: O(c n f log(n f) + n f c^2 + n f c^3 / R)}
  space: {extra: O(c n f)}
properties: {deterministic: true, iterative: false, online: false, in_place: false}
history:
  year: 2003
  people: [Jeffrey Tsao, Peter Boesiger, Klaas P. Pruessmann]
  note: Tsao, Boesiger and Pruessmann sampled k-t space on a sheared lattice and unfolded the x-f aliases with a Wiener-type estimate whose prior came from low resolution training data, for one coil (k-t BLAST) and with coil maps (k-t SENSE).
prereqs: [sense, wiener-filter, k-space]
see_also: [low-rank-plus-sparse-mri, partial-separability-model, compressed-sensing-mri, aliasing, cg-sense, grappa, mri-reconstruction-problem, robust-pca]
sources:
  - paper: doi:10.1002/mrm.10611
    title: Jeffrey Tsao, Peter Boesiger and Klaas P. Pruessmann, k-t BLAST and k-t SENSE, dynamic MRI with high frame rate exploiting spatiotemporal correlations, Magnetic Resonance in Medicine 50(5), 2003, 1031 to 1042
    locator: the lattice sampling in k-t space, the point spread function in x-f space, the reconstruction formula with the training estimate and the noise term, baseline subtraction, and the coil version (general locator)
  - paper: "Bruno Madore, Gary H. Glover and Norbert J. Pelc, Unaliasing by Fourier-encoding the overlaps using the temporal dimension (UNFOLD), applied to cardiac imaging and fMRI, Magnetic Resonance in Medicine 42(5), 1999, 813 to 828"
    locator: the shifted sampling in k-t space that moves aliases to other temporal frequencies (general locator)
  - paper: "Henrik Pedersen, Sebastian Kozerke, Steffen Ringgaard, Kay Nehrke and Won Yong Kim, k-t PCA, temporally constrained k-t BLAST reconstruction using principal component analysis, Magnetic Resonance in Medicine 62(3), 2009, 706 to 716"
    locator: the use of a temporal basis from the training data in the k-t BLAST reconstruction (general locator)
---

k-t BLAST (Broad-use Linear Acquisition Speed-up Technique) speeds up dynamic MRI by sampling only every $R$-th phase encoding line in each frame, on a pattern that shifts from frame to frame. After a Fourier transform along space and along time, the missing lines show up as aliases in x-f space, the space of position and temporal frequency. Each measured x-f value is a sum of $R$ unknown values. k-t BLAST splits each sum with a Wiener-type estimate. The prior power of each value comes from a short training scan of low spatial resolution. With coil maps, the same estimate also uses the coil sensitivities, and the method is called k-t SENSE. Unlike [low-rank plus sparse MRI](/low-rank-plus-sparse-mri/) and [compressed sensing MRI](/compressed-sensing-mri/), the reconstruction is linear and not iterative, but it needs the training data.

## In plain words

In a heart scan, most pixels hardly change over time, and the pixels that do change are in a small region. Take the time course of each pixel and look at its frequencies. Static pixels have only the zero frequency. Moving pixels have a few low frequencies.

If you skip lines in k-space, each image gets copies of itself laid over it. k-t BLAST skips different lines in each frame, so the copies also move to other temporal frequencies. Most of the time, a copy lands where the true signal is near zero. A low resolution training scan tells the method where the signal is large and where it is small. For each overlap, it gives the measured value mostly to the place where the training scan expects signal.

## The problem

The input is a dynamic series of $n_t$ frames with $n$ pixels along the phase encoding direction (a 1D model; the read direction is fully sampled and separates). The sampled k-t data are $d_c(k, t)$ for coil $c$, at the points of a lattice: frame $t$ keeps the lines $k \equiv s t \pmod R$. The acceleration $R$ divides $n$ and $n_t$, and the shift $s$ is prime to $R$, so every line is sampled in $n_t / R$ frames. The other inputs are a prior power $p(y, f) \ge 0$ for each x-f point, a noise variance $\psi \ge 0$ and, for k-t SENSE, the coil maps $c(y)$. The unitary DFT along time of the series is $\rho(y, f)$. The output is an estimate of the series.

Zero fill the data, apply the unitary inverse DFT along $k$ and the unitary DFT along $t$. The result is the aliased x-f signal

$$\rho_{\text{alias}, c}(y, f) = \frac1R \sum_{j=0}^{R-1} c(y_j)\, \rho(y_j, f_j), \qquad y_j = y + \frac{jn}{R}, \quad f_j = f + \frac{j s n_t}{R}.$$

So the x-f grid splits into groups of $R$ points that fold onto one point, and each group is a small linear system $v = A \rho_G$ with the $n_c \times R$ matrix $A_{cj} = c(y_j)/R$. The [aliasing](/aliasing/) is the same as in [SENSE](/sense/), but in x-f space and not in image space.

## The algorithm

```pseudo id=main
KTBLAST(d, lattice, p, psi, coils)
L1  b(k) <- mean of d(k, t) over the frames t that sample line k   ▷ baseline
L2  d(k, t) <- d(k, t) - b(k) on the sampled points
L3  rho_alias <- DFT along t of the inverse DFT along k of the zero filled d
L4  for each alias group G = {(y_j, f_j)} folding onto (y_0, f_0) do
L5      A <- the n_c x R matrix c(y_j) / R;  P <- diag(p(y_j, f_j))
L6      rho(G) <- P A^H (A P A^H + psi I)^(-1) rho_alias(y_0, f_0)
L7  x <- inverse DFT along t of rho
L8  return x + the image of b
```

Line L6 is the [Wiener filter](/wiener-filter/) of one group. If the values $\rho_G$ have mean 0 and covariance $P$ and the noise has covariance $\psi I$, it is the linear estimate with the least mean squared error. In the paper, $P$ is the squared magnitude of the training x-f signal, and $\psi$ is the noise variance. The training data are a few central k-space lines, fully sampled in every frame, so they give a low resolution series. The baseline (the time average) is removed from the data and from the training data before the unfolding and is added back at the end, because the time average is large and its prior would hide the dynamic part. With one coil, line L6 is a scalar formula:

$$\hat\rho(y_j, f_j) = \frac{R\, p_j}{\sum_i p_i + R^2 \psi}\, \rho_{\text{alias}}(y_0, f_0).$$

## Example

Take $n = 32$ pixels and $n_t = 16$ frames. The body is 1 on the pixels 4 to 27. A bright region of height 1 between two edges at $12 - 2.5 \cos(2\pi t/16)$ and $20 + 2.5 \cos(2\pi t/16)$, with smooth edges, models a beating heart. Pixels 24 to 26 also rise linearly by 0.5 over the scan, like contrast uptake. Sample with $R = 4$ and $s = 1$, so each frame keeps 8 of 32 lines. The training series uses the $2w - 1$ central lines of each frame. The table gives the relative error of the whole series (measured with the code below, one coil, no noise).

| reconstruction | relative error |
|---|---|
| zero filled, scaled by $R$, no baseline | 1.728 |
| the time average alone | 0.160 |
| flat prior $p = 1$, with baseline | 0.142 |
| training with 3 lines, $\psi = 10^{-6}$ | 0.055 |
| training with 7 lines, $\psi = 10^{-6}$ | 0.052 |
| training with 11 lines, $\psi = 10^{-6}$ | 0.048 |
| training with 7 lines, $\psi = 0.01$ | 0.071 |
| the true power as the prior, $\psi = 10^{-9}$ | 0.047 |

A flat prior splits each alias value evenly among the $R$ points, which leaves the aliases in place. Even 3 training lines cut the error by more than half. The true power does not give zero error: some groups hold two points with signal, such as the two moving edges, and one coil cannot separate them. The shift $s = 3$ gives the same numbers on this series. Without the baseline, the flat prior gives 0.867 and the training prior gives the same errors as with it, because the data have no noise.

## Correctness

The following results hold, and all are proved in full below.

- **Aliasing.** For the lattice above, the zero filled x-f signal is exactly $\frac1R \sum_j c(y_j) \rho(y_j, f_j)$, and the groups partition the x-f grid. The proof writes the mask as a sum of $R$ complex exponentials, each of which shifts the signal in $y$ and in $f$.
- **Wiener estimate.** Line L6 minimizes the mean squared error among linear estimates, under the prior and noise model above. For $\psi > 0$ and $P > 0$ it also equals $(A^H A/\psi + P^{-1})^{-1} A^H v/\psi$, the minimizer of $\|v - A\rho\|^2/\psi + \sum_j |\rho_j|^2/p_j$.
- **Exact cases.** If the true group signal is zero where $p = 0$, and the columns of $A$ where $p > 0$ are independent, the estimate tends to the truth as $\psi \to 0$. This covers one signal point per group with one coil, k-t SENSE with at least $R$ coils whose maps separate the group, and full sampling.
- **Baseline.** The baseline from the sampled data is the true time average plus copies of the signal at the temporal frequencies that are nonzero multiples of $n_t/R$. A static series is recovered exactly.

The model of a zero-mean prior with independent values is a heuristic. Real x-f signals are not Gaussian, and the training power is only an estimate of the true power. So the quality of the result for a real scan is measured, not proved.

## Complexity

Let $n$ be the number of pixels along the phase encoding direction, $n_t$ the number of frames and $n_c$ the number of coils. The FFTs along $k$ and $t$ cost $O(n_c n n_t \log(n n_t))$ (lines L3 and L7). There are $n n_t / R$ groups, and each needs the $n_c \times n_c$ matrix $A P A^H + \psi I$ in $O(n_c^2 R)$ and one solve in $O(n_c^3)$ (lines L5 and L6). The total is $O(n_c n n_t \log(n n_t) + n n_t n_c^2 + n n_t n_c^3 / R)$ in the [real RAM](/real-ram/), with $O(n_c n n_t)$ space for the data. For one coil this is $O(n n_t \log(n n_t))$, the cost of the FFTs. The method makes one pass and needs no iterations. The training scan costs extra scan time: a few central lines in every frame.

## Properties

- **Linear and direct.** The output is a linear function of the data for a fixed prior. There is no iteration and no tuning of a step size.
- **Needs training data.** The prior comes from a separate low resolution scan, or from the central lines acquired together with the lattice.
- **Local in x-f.** Each group is solved alone, so the work is easy to split.
- **Temporal blurring.** Where the training prior is wrong or too smooth, the estimate pulls the dynamic signal toward zero. This shows up as a loss of temporal detail in small moving structures.

## Variants and improvements

- **k-t SENSE.** With coil maps, $A$ has one row per coil, and line L6 is SENSE unfolding with a prior. With at least $R$ coils that separate each group, it is exact in the noiseless limit. k-t SENSE is the name of this coil version, from the same paper.
- **UNFOLD.** Madore, Glover and Pelc (1999) used the same shifted sampling to move aliases to other temporal frequencies and removed them with a fixed temporal filter, with no training data. k-t BLAST replaces the fixed filter by the data adaptive prior.
- **k-t PCA.** Pedersen et al. (2009) restricted the temporal signal of each pixel to a few principal components of the training data. This is close to the [partial separability model](/partial-separability-model/), which also uses a low rank temporal basis.
- **Sparse and low rank priors.** [Compressed sensing MRI](/compressed-sensing-mri/) and [L+S](/low-rank-plus-sparse-mri/) replace the training prior by sparsity or low rank, and need random sampling instead of a lattice.

## When to use it

Use k-t BLAST or k-t SENSE for dynamic scans where most of the field of view is static or slowly changing, such as cardiac cine, and when a short training scan is acceptable. It is fast and direct, so it suits real-time display. For scans with large motion across the field of view, or when no training data can be acquired, use a method with a sparse or low rank prior instead.

## Pitfalls

- **The lattice conditions.** The shift $s$ must be prime to $R$, and $R$ must divide $n$ and $n_t$. Otherwise some lines are never sampled, and the groups do not partition the x-f grid.
- **Points that share a group.** With one coil, two points in one group with signal cannot be separated. In the example, this keeps the error at 0.047 even with the true power. Choose the shift so that the aliases of the dynamic region land on static regions.
- **The noise term.** $\psi$ trades noise against temporal detail. In the example, $\psi = 0.01$ raises the error from 0.052 to 0.071. With real noise, $\psi = 0$ amplifies it.
- **Wrong training data.** If the patient moves between the training scan and the main scan, the prior puts the signal in the wrong place.
- **Signal at multiples of $n_t/R$.** The baseline from the sampled data mixes in the signal at these temporal frequencies, and the groups at $f = 0$ are set to zero after the subtraction.

## Implementations

## History

Madore, Glover and Pelc introduced UNFOLD in 1999, which shifts the sampling from frame to frame so that aliases move along the temporal frequency axis. In the same year Pruessmann and coauthors published SENSE. In 2003 Tsao, Boesiger and Pruessmann joined the two ideas: lattice sampling in k-t space, aliases in x-f space, and an unfolding with a prior from training data, for one coil (k-t BLAST) and for several coils (k-t SENSE). Later work, such as k-t PCA in 2009, constrained the temporal signal further, and the compressed sensing and low rank methods of the following years removed the need for training data.

## References
