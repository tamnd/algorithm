---
tag: 2VGRQM
kind: problem
slug: single-molecule-localization
name: Single-molecule localization
aliases:
- PALM and STORM localization
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: advanced
summary: Find the positions of sparse fluorescent emitters in each frame of a movie to a precision far below the diffraction limit. Then render all positions as one image.
model: real-ram
prereqs: [point-spread-function, poisson-distribution, maximum-likelihood-estimation, abbe-diffraction-limit]
see_also: [maximum-likelihood-localization, localization-precision-formula, cramer-rao-bound, sofi, structured-illumination-microscopy, super-resolution, rayleigh-criterion, beurling-lasso]
sources:
  - paper: doi:10.1126/science.1127344
    title: "E. Betzig, G. H. Patterson, R. Sougrat, O. W. Lindwasser, S. Olenych, J. S. Bonifacino, M. W. Davidson, J. Lippincott-Schwartz and H. F. Hess, Imaging intracellular fluorescent proteins at nanometer resolution, Science 313(5793), 2006, 1642 to 1645"
    locator: "PALM, the activation of sparse subsets of photoactivatable fluorescent proteins and the localization of each molecule"
  - paper: doi:10.1529/biophysj.106.091116
    title: "S. T. Hess, T. P. K. Girirajan and M. D. Mason, Ultra-high resolution imaging by fluorescence photoactivation localization microscopy, Biophysical Journal 91(11), 2006, 4258 to 4272"
    locator: "FPALM, the activation, localization and bleaching cycle, and the localization precision"
  - paper: doi:10.1038/nmeth929
    title: "M. J. Rust, M. Bates and X. Zhuang, Sub-diffraction-limit imaging by stochastic optical reconstruction microscopy (STORM), Nature Methods 3(10), 2006, 793 to 796"
    locator: "STORM with photoswitchable dye pairs, switched on and off over many cycles"
  - paper: doi:10.1016/S0006-3495(02)75618-X
    title: "R. E. Thompson, D. R. Larson and W. W. Webb, Precise nanometer localization analysis for individual fluorescent probes, Biophysical Journal 82(5), 2002, 2775 to 2783"
    locator: "the precision of fitting the position of one fluorescent probe, with the photon, pixel and background terms"
  - paper: doi:10.1016/S0006-3495(04)74193-4
    title: "R. J. Ober, S. Ram and E. S. Ward, Localization accuracy in single-molecule microscopy, Biophysical Journal 86(2), 2004, 1185 to 1200"
    locator: the Fisher information of the photon detection process and the limit of the localization accuracy
---

## In plain words

A light microscope cannot separate two glowing molecules that are closer than about a quarter of a micrometer: their blurred spots merge. But a single isolated spot can be measured very precisely: its center can be found to a few nanometers, because many photons together pin it down. Single-molecule localization uses this. Special dyes are switched on a few at a time, so that in each camera frame the glowing molecules are far apart. Each spot is found and its center is measured. Then the dyes are switched off and another random few are switched on. After thousands of frames, almost every molecule has been seen and measured once or more, and the list of positions is drawn as an image that is ten times sharper than the normal one.

The gain is optical: the switching keeps the spots apart. The computation only solves many small, well-posed fits.

## Definition

The input is a movie of frames of photon counts. In frame $t$ a sparse random set of emitters is on. The expected count of pixel $p$ is

$$\mu_t(p) = b_t(p) + \sum_{k \text{ on in frame } t} N_{k,t} \int_{\text{pixel } p} \mathrm{PSF}(\xi - r_k)\, d\xi,$$

with the positions $r_k$, the photon counts $N_{k,t}$ and a background $b_t$, and the counts are Poisson (plus camera noise). The task has three parts:

1. **Detection.** Find the spots in each frame, usually by filtering and a threshold on the local maxima.
2. **Localization.** For each spot, estimate the position $r_k$ (and the photon count, the background and perhaps the depth), with an uncertainty.
3. **Assembly.** Correct the drift of the sample, merge repeated localizations of the same molecule, discard poor fits, and render the positions, for example as a 2D histogram or as a sum of Gaussians with the width of each localization uncertainty.

The localization of one isolated spot is the core estimation problem: a nonlinear fit of a PSF model with four or more parameters to a window of a few hundred pixels.

## Variants

- **PALM** (photoactivated localization microscopy): photoactivatable fluorescent proteins, switched on by a weak violet light and bleached after imaging (Betzig et al. 2006). **FPALM** is the same idea, published at the same time (Hess et al. 2006).
- **STORM** (stochastic optical reconstruction microscopy): photoswitchable dye pairs, switched on and off many times (Rust, Bates and Zhuang 2006). dSTORM uses single dyes in a switching buffer.
- **PAINT**: dyes that bind for a short time from the solution, so each binding event is a short blink.
- **3D localization**: the depth from an astigmatic PSF, from two focal planes, or from engineered PSFs such as the double helix.
- **High density**: overlapping spots, handled by multi-emitter fitting or by sparse recovery on a grid or off the grid ([Beurling LASSO](/beurling-lasso/)).
- **Single-particle tracking**: the same localization, linked from frame to frame into trajectories.

## Examples

A Gaussian PSF of width $s = 100$ nm on pixels of $100$ nm, with no background, gives the Cramer-Rao bound $3.29$ nm on the standard deviation of each coordinate for $N = 1000$ photons, and $10.4$ nm for $N = 100$, since the bound scales as $1/\sqrt N$ (see the [localization precision formula](/localization-precision-formula/)). With infinitely small pixels the bound is $s/\sqrt N = 3.16$ nm for $1000$ photons. For the Airy PSF of an ideal lens, the same Fisher information computation without pixels or background gives $\lambda/(2\pi\,\mathrm{NA}\sqrt N)$, which is $1.80$ nm for $\lambda = 500$ nm, $\mathrm{NA} = 1.4$ and $N = 1000$; the derivation is in the localization precision page.

The [maximum likelihood localization](/maximum-likelihood-localization/) page fits a $9 \times 9$ window with $s = 1.3$ pixels and $500$ photons over a background of $2$ per pixel; over $200$ simulated images the sample variances of the two coordinates are $1.08$ and $1.02$ times the bound (a measurement).

## Known algorithms

- **Centroid.** The intensity-weighted mean of the window after background subtraction. Fast, but biased by the background and the window, and far from the bound.
- **Least squares Gaussian fitting.** Fit a Gaussian by [Levenberg-Marquardt](/levenberg-marquardt/); close to the bound at high background, worse at low background.
- **[Maximum likelihood localization](/maximum-likelihood-localization/).** Fit a pixel-integrated Gaussian or a measured PSF under the Poisson model by Newton steps. For large photon counts and a correct PSF it nears the Cramer-Rao bound.
- **Radial symmetry and phasor methods.** Closed-form estimates of the center, almost as precise as fitting for good data.
- **Multi-emitter and sparse methods.** Fit several emitters per window, or solve a sparse recovery problem for dense frames.
- **Learned methods.** Neural networks trained on simulated frames, for dense frames and complex PSFs.

## Bounds

- **Cramer-Rao bound.** No unbiased estimator has a variance below the inverse Fisher information of the photon model (Ober, Ram and Ward 2004). Without pixels or background it is $s^2/N$ for a Gaussian PSF of width $s$. See the [localization precision formula](/localization-precision-formula/) for the effect of pixels and background, and the Thompson-Larson-Webb approximation.
- **Resolution of the image.** The rendered image is limited by the localization precision and also by the density of the labels: a structure is resolved only if the labels sample it densely enough. A common rule of thumb asks for a label spacing below half the desired resolution; it is a heuristic, by analogy with the [sampling theorem](/sampling-theorem/).
- **Sparsity.** Isolated-spot fitting needs the spots of active emitters to be farther apart than a few PSF widths; this caps the number of molecules per frame and so the speed of imaging.

## Reductions

- **To parameter estimation.** Each isolated spot is a small [maximum likelihood estimation](/maximum-likelihood-estimation/) or [nonlinear least squares](/nonlinear-least-squares/) problem.
- **To sparse recovery.** Dense frames are a [sparse signal recovery](/sparse-signal-recovery/) problem on a fine grid, or a Beurling LASSO problem off the grid.
- **Drift correction to registration.** Drift is often estimated by the [cross-correlation](/cross-correlation/) of images rendered from blocks of frames.

## Applications

Imaging cell structures at the scale of tens of nanometers (the cytoskeleton, synapses, the nuclear pore complex), counting molecules in clusters, tracking single proteins in living cells, and imaging with DNA-based probes. The method needs many frames, so it is slower than [structured illumination](/structured-illumination-microscopy/) or [SOFI](/sofi/), but it reaches a higher resolution.

## References
