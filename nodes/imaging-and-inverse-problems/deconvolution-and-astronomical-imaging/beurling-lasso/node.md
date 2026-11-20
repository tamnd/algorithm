---
tag: 5WAZ0Q
kind: problem
slug: beurling-lasso
name: Beurling LASSO
aliases:
- BLASSO
- off-the-grid sparse recovery
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: research
summary: Recover a sparse sum of spikes from low frequency or blurred data by minimizing the total variation norm over all measures. The spike positions are not tied to a grid.
model: real-ram
prereqs: [lasso-regression, basis-pursuit, discrete-fourier-transform, lagrangian-duality]
see_also: [super-resolution-total-variation-theorem, lasso-regression, basis-pursuit, compressed-sensing, semidefinite-programming, prony-method, music-algorithm, single-molecule-localization]
sources:
  - paper: doi:10.1016/j.jmaa.2012.05.011
    title: "Yohann de Castro and Fabrice Gamboa, Exact reconstruction using Beurling minimal extrapolation, Journal of Mathematical Analysis and Applications, 2012"
    locator: "total variation norm minimization over measures, and exact recovery of nonnegative sparse measures"
  - paper: doi:10.1051/cocv/2011205
    title: "Kristian Bredies and Hanna Katriina Pikkarainen, Inverse problems in spaces of measures, ESAIM: Control, Optimisation and Calculus of Variations, 2013"
    locator: "Tikhonov regularization with the total variation norm of a measure, existence of minimizers, optimality conditions and a conditional gradient method"
  - paper: doi:10.1002/cpa.21455
    title: "Emmanuel J. Candes and Carlos Fernandez-Granda, Towards a mathematical theory of super-resolution, Communications on Pure and Applied Mathematics 67(6), 2014, 906 to 956"
    locator: "exact recovery under a minimum separation, and the semidefinite program for the dual problem (Section 4)"
  - paper: doi:10.1007/s10208-014-9228-6
    title: "Vincent Duval and Gabriel Peyre, Exact support recovery for sparse spikes deconvolution, Foundations of Computational Mathematics, 2015"
    locator: "the dual certificate of minimal norm, the nondegenerate source condition, and support stability of the penalized problem at low noise"
---

## In plain words

Many imaging problems have a few point sources: stars, fluorescent molecules, or the frequencies of a sum of sine waves. The data are a blurred or low frequency view of them. The LASSO finds a sparse answer by penalizing the sum of the absolute amplitudes, but it needs a list of candidate positions, a grid. If a true source lies between two grid points, the LASSO splits it into two or more spikes and adds small false ones. The Beurling LASSO removes the grid: the unknown is any finite sum of spikes at any positions, or more generally any measure, and the penalty is the total mass of the absolute values. It is a convex problem in infinitely many unknowns. For Fourier data on an interval it can be solved exactly by a finite semidefinite program.

## Definition

Let $X$ be the domain of the positions, for example the torus $\mathbb T = [0, 1)$, and $\mathcal M(X)$ the space of finite signed (or complex) Radon measures on $X$ with the total variation norm $\lVert\mu\rVert_{TV} = |\mu|(X)$. For a sum of spikes $\mu = \sum_j a_j\delta_{t_j}$ with distinct $t_j$, $\lVert\mu\rVert_{TV} = \sum_j |a_j|$. The measurement operator is linear,

$$\Phi\mu = \int_X \varphi(t)\,d\mu(t) \in \mathbb C^m,$$

with a continuous kernel $\varphi$. For the low frequency Fourier coefficients up to the cutoff $f_c$, $\varphi(t) = (e^{-2\pi i k t})_{|k| \le f_c}$ and $m = 2f_c + 1$; for a sampled blur, $\varphi(t)$ is the vector of the PSF centered at $t$ at the sample points. Given $y = \Phi\mu_0 + w$, the **Beurling LASSO** is

$$\min_{\mu \in \mathcal M(X)} \tfrac12\lVert\Phi\mu - y\rVert^2 + \lambda\lVert\mu\rVert_{TV}, \qquad \lambda > 0,$$

and its noiseless limit is the constrained problem $\min \lVert\mu\rVert_{TV}$ subject to $\Phi\mu = y$, which de Castro and Gamboa called Beurling minimal extrapolation. Minimizers exist because the unit ball of $\mathcal M(X)$ is weak-star compact and $\Phi$ is weak-star continuous (Bredies and Pikkarainen 2013).

**Dual problem.** By [Lagrangian duality](/lagrangian-duality/) the dual of the penalized problem is

$$\max_{p \in \mathbb C^m} \operatorname{Re}\langle y, p\rangle - \tfrac\lambda2\lVert p\rVert^2 \quad\text{subject to}\quad \lVert\Phi^*p\rVert_\infty \le 1,$$

where $(\Phi^*p)(t) = \langle\varphi(t), p\rangle$ is a continuous function; for Fourier data it is a trigonometric polynomial of degree $f_c$. At the optimum, $p_\lambda = (y - \Phi\mu_\lambda)/\lambda$, and $\eta_\lambda = \Phi^*p_\lambda$ satisfies $|\eta_\lambda| \le 1$ everywhere and $\eta_\lambda = \operatorname{sign} a_j$ at each spike of the solution. So the spikes lie where $|\eta_\lambda| = 1$. A function $\eta = \Phi^*p$ with $\eta(t_j) = \operatorname{sign}a_j$ and $|\eta| < 1$ elsewhere is a **dual certificate** for the measure $\sum a_j\delta_{t_j}$.

## Variants

- **Constrained or penalized.** The equality constraint for exact data, the penalty for noisy data, or a constraint $\lVert\Phi\mu - y\rVert \le \delta$.
- **Nonnegative measures.** For positive sources (photon emitters) the problem can be restricted to $\mu \ge 0$, and the TV norm becomes the total mass.
- **Kernels.** Fourier coefficients (line spectral estimation), samples of a Gaussian or Airy blur (deconvolution of spikes, [single-molecule localization](/single-molecule-localization/) at high density), Laplace transforms, or several dimensions.
- **Atomic norm.** For Fourier data, the TV norm of the measure equals the atomic norm of the data vector with the atoms $\varphi(t)$, which gives the same problem in a finite form.
- **Grid version.** Restrict the positions to a grid; this is the [LASSO](/lasso-regression/) or [basis pursuit](/basis-pursuit/) with the columns $\varphi(t_g)$.

## Examples

**A grid LASSO solves a tiny instance.** Take $f_c = 4$, so $9$ Fourier coefficients, and the measure $\mu_0 = \delta_{0.1} - 0.7\,\delta_{0.6}$ on the torus, with $\lVert\mu_0\rVert_{TV} = 1.7$ and no noise. The separation $0.5$ is $2/f_c$, but the [exact recovery theorem](/super-resolution-total-variation-theorem/) needs $f_c \ge 128$. A direct certificate exists all the same: $\eta(t) = \cos(2\pi(t - 0.1))$ has degree $1$, equals $1$ at $0.1$ and $-1$ at $0.6$, and has $|\eta| < 1$ elsewhere, so $\mu_0$ is the unique solution of the constrained problem. This page does not solve the semidefinite program. Instead it solves the grid version with real amplitudes, $\lambda = 10^{-3}$, by $30000$ iterations of [FISTA](/fista/):

| grid | spikes found (position: amplitude) | $\ell_1$ norm |
|---|---|---|
| $50$ points, contains $0.1$ and $0.6$ | $0.1$: $0.9999$, $0.6$: $-0.6999$ | $1.6997$ |
| $64$ points, contains neither | $0.0938$: $0.6044$, $0.1094$: $0.4002$, $0.5938$: $-0.4219$, $0.6094$: $-0.2808$, and small spikes of about $\pm 0.002$ | $1.7176$ |

On the matching grid the LASSO finds the two spikes, shrunk slightly by $\lambda$. On the other grid each spike splits between its two neighbors and the norm is larger than $1.7$, because the true measure is not available on that grid. This is the basis mismatch that the off-the-grid problem avoids.

**Spikes of opposite sign that are too close.** Take $f_c = 1$, so the data are the coefficients $k = -1, 0, 1$, and the dipole $\mu_0 = \delta_{d/2} - \delta_{-d/2}$ with $0 < d < 1/2$. Its data are $0$ at $k = 0$ and $\mp 2i\sin(\pi d)$ at $k = \pm 1$. The measure $\nu = \sin(\pi d)(\delta_{1/4} - \delta_{-1/4})$ has the same data and the norm $2\sin(\pi d) < 2 = \lVert\mu_0\rVert_{TV}$: $0.618$, $1.414$ and $1.902$ for $d = 0.1$, $0.25$ and $0.4$. So $\mu_0$ is not recovered. In fact $\nu$ is the unique minimizer: $\eta(t) = \sin(2\pi t)$ is a trigonometric polynomial of degree $1$, equal to $\pm 1$ at $\pm 1/4$, with $|\eta| < 1$ elsewhere.

**Nonnegative spikes need no separation.** Let $\mu_0 = \sum_{j=1}^s a_j\delta_{t_j}$ with $a_j > 0$ and $s \le f_c$. The function $P(t) = \prod_j \sin^2(\pi(t - t_j))$ is a nonnegative trigonometric polynomial of degree $s$ that vanishes only at the $t_j$. So $\eta = 1 - P/\max P$ has degree at most $f_c$, equals $1$ at every $t_j$, and lies in $[0, 1)$ elsewhere: a dual certificate for $\mu_0$ however close the spikes are. This is the setting of de Castro and Gamboa (2012).

## Known algorithms

- **Semidefinite program of the dual (Fourier data).** The constraint $|\sum_{|k| \le f_c} p_k e^{2\pi ikt}| \le 1$ for all $t$ holds if and only if there is a Hermitian matrix $Q$ with $\begin{pmatrix} Q & p \\ p^* & 1\end{pmatrix} \succeq 0$ and $\sum_i Q_{i,i+j} = 1$ for $j = 0$ and $0$ for $j \ne 0$. So the constrained dual is a finite [semidefinite program](/semidefinite-programming/) (Candes and Fernandez-Granda 2014, Section 4). The support is then found as the points where the polynomial $1 - |\eta(t)|^2$ has its roots on the circle, and the amplitudes by least squares.
- **Grid LASSO.** Solve the LASSO on a fine grid by [iterative soft thresholding](/iterative-shrinkage-thresholding/), FISTA or [coordinate descent](/coordinate-descent/). Simple and general, but the answer is only as fine as the grid, and fine grids make the columns nearly equal.
- **Conditional gradient.** Add one spike at a time at the maximum of $|\eta|$ for the current residual, then refit the amplitudes (Bredies and Pikkarainen 2013). The sliding variant also moves the positions continuously after each step.
- **Nonconvex fitting.** Optimize the positions and amplitudes of a fixed number of spikes directly, starting from a grid solution.
- **Subspace methods.** Not convex and not based on the TV norm, but solve the same Fourier problem: [Prony's method](/prony-method/), [MUSIC](/music-algorithm/) and [ESPRIT](/esprit/).

## Bounds

- **Exact recovery.** For Fourier data with $f_c \ge 128$, every measure whose spikes are at least $2/f_c$ apart on the torus is the unique solution of the constrained problem ([exact super-resolution by total variation minimization](/super-resolution-total-variation-theorem/)).
- **Separation is needed for signed spikes.** The dipole example, repeated periodically, shows that for every $f_c$ a measure with spikes of opposite sign closer than $1/(2f_c)$ can fail to be recovered (see the tightness section of the theorem).
- **No separation for nonnegative spikes.** A nonnegative measure with at most $f_c$ spikes is recovered from the coefficients $|k| \le f_c$, by the certificate above. But the problem becomes badly conditioned as the spikes merge, so noise sets a practical limit.
- **Support stability.** If the dual certificate of minimal norm is nondegenerate (it equals $\pm 1$ only at the spikes and has a nonzero second derivative there), then for small noise and $\lambda$ of the order of the noise, the penalized problem has exactly as many spikes as $\mu_0$, close to the true positions (Duval and Peyre 2015).

## Reductions

- **From the LASSO.** The grid LASSO is the Beurling LASSO restricted to measures supported on the grid. A finer grid lowers the optimal value toward the off-the-grid value.
- **To a semidefinite program.** For Fourier data on the torus, the dual is a finite semidefinite program, so the problem is solved by an [interior point method](/interior-point-method/) in polynomial time in $f_c$.
- **To sparse recovery.** It is the measure analogue of [sparse signal recovery](/sparse-signal-recovery/) and [compressed sensing](/compressed-sensing/), but the columns $\varphi(t)$ form a continuum of nearly equal vectors, so the restricted isometry property fails and separation or positivity takes its place.

## Applications

The localization of many overlapping emitters in a frame of [single-molecule localization](/single-molecule-localization/) microscopy, [spectral estimation](/spectral-estimation/) of a few sine waves from a short record, the direction of arrival in arrays of antennas, point sources in astronomy and radio interferometry, and the deconvolution of spike trains in seismology and neuroscience.

## References
