---
tag: 960N1V
kind: problem
slug: multiframe-super-resolution
name: Multi-frame super-resolution
aliases:
- multi-image super-resolution
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: advanced
summary: "Combine several undersampled images of one scene, offset by subpixel shifts, into one image on a finer grid. It undoes aliasing from coarse pixels, not the optical diffraction limit."
model: real-ram
prereqs: [aliasing, sampling-theorem, point-spread-function, image-registration]
see_also: [super-resolution, iterative-back-projection-super-resolution, drizzle, image-deblurring, tikhonov-regularization, total-variation-denoising, structured-illumination-microscopy, lucky-imaging]
sources:
  - paper: doi:10.1109/83.650118
    title: "Michael Elad and Arie Feuer, Restoration of a single superresolution image from several blurred, noisy, and undersampled measured images, IEEE Transactions on Image Processing 6(12), 1997, 1646 to 1658"
    locator: "the model with a warp, a blur and a decimation for each frame, and its maximum likelihood, MAP and set-theoretic solutions"
  - paper: doi:10.1016/1049-9652(91)90045-L
    title: "Michal Irani and Shmuel Peleg, Improving resolution by image registration, CVGIP: Graphical Models and Image Processing 53(3), 1991, 231 to 239"
    locator: registration of the frames and the iterative back-projection reconstruction
  - paper: doi:10.1109/TPAMI.2002.1033210
    title: "Simon Baker and Takeo Kanade, Limits on super-resolution and how to break them, IEEE Transactions on Pattern Analysis and Machine Intelligence 24(9), 2002, 1167 to 1183"
    locator: "the analysis of the reconstruction constraints as the magnification grows, and the use of learned priors (general locator)"
  - paper: doi:10.1109/TIP.2004.834669
    title: "Sina Farsiu, M. Dirk Robinson, Michael Elad and Peyman Milanfar, Fast and robust multiframe super resolution, IEEE Transactions on Image Processing 13(10), 2004, 1327 to 1344"
    locator: "the L1 data term, the median and mean shift-and-add for pure translation, and the bilateral total variation prior"
  - paper: doi:10.1086/338393
    title: "Andrew S. Fruchter and Richard N. Hook, Drizzle: a method for the linear reconstruction of undersampled images, Publications of the Astronomical Society of the Pacific 114(792), 2002, 144 to 152"
    locator: the combination of dithered undersampled frames in astronomy
---

## In plain words

A camera with large pixels misses fine detail: each pixel adds up the light over its area, and the pixel grid is too coarse to record fine patterns, which show up as false coarse patterns (aliasing). If you take several pictures of the same scene and move the camera by a fraction of a pixel between them, each picture samples the scene at different places. Together the pictures sample the scene on a finer grid. Multi-frame super-resolution is the task of putting them together into one sharper image on that finer grid.

Here the new information comes from the extra samples of the other frames. Single-image methods on the broader [super-resolution](/super-resolution/) page get it only from a prior. Neither recovers detail that the optics removed; that needs optical methods such as [structured illumination](/structured-illumination-microscopy/) or [single-molecule localization](/single-molecule-localization/).

## Definition

Let $x$ be the unknown image on a fine grid of $n$ pixels, and let $L$ be the magnification factor, the ratio of the coarse pixel side to the fine one. Frame $k = 1, \ldots, K$ is

$$y_k = D\, B\, W_k\, x + e_k,$$

where $W_k$ is the motion of frame $k$ on the fine grid (a shift, an affine map or a flow field), $B$ is the blur of the optics and of the pixel area (the [PSF](/point-spread-function/) on the fine grid), $D$ keeps every $L$-th pixel in each direction, and $e_k$ is the noise. Given $y_1, \ldots, y_K$, and either the $W_k$ or a way to estimate them by [image registration](/image-registration/), find $x$. In the least squares form, minimize $\sum_k \lVert y_k - DBW_kx\rVert^2 + \lambda R(x)$ with a prior $R$.

**Identifiability (theorem).** Take a 1D periodic grid with $L$ dividing $n$, integer shifts $s_k$ on the fine grid, and a blur whose DFT $H_q$ has no zero. The stacked operator $x \mapsto (DBW_kx)_k$ is injective if and only if the residues $s_k \bmod L$ cover $\{0, \ldots, L - 1\}$. If they cover each residue once, its normal matrix is $B^TB$, so the problem is the deblurring of $x$ on the fine grid, with the singular values $|H_q|$. The proof is Claim 3 and Lemma 2 of the proof of [iterative back-projection](/iterative-back-projection-super-resolution/). A shift by a whole coarse pixel adds no information. In 2D the same holds for pairs of residues, so $L^2$ well placed frames are needed.

## Variants

- **Motion model.** Global translation (the classical case, which drizzle and shift-and-add handle), affine or projective motion, or local motion in video, where the registration is the hard part.
- **Known or unknown motion.** With unknown motion, the registration and the reconstruction can be done in turn or jointly; registration errors are a main source of artifacts.
- **Known or unknown blur.** A blind version also estimates the PSF.
- **Noise model.** Gaussian noise leads to least squares; outliers, such as wrong registration or moving objects, lead to an L1 data term. For pure translation, the L2 and L1 fits on the fine grid are the mean and the median of the samples that land on each fine pixel (Farsiu et al. 2004).
- **Prior.** None, Tikhonov, [total variation](/total-variation-denoising/), Markov random fields, or learned priors.
- **Colour and video.** Joint demosaicing and super-resolution; super-resolution of each frame of a video from its neighbors.

## Examples

**Aliasing and a second frame.** Take $n = 8$, $L = 2$ and the blur $h = (\frac16, \frac23, \frac16)$ centered at index $0$, whose DFT is $H_q = \frac23 + \frac13\cos(2\pi q/8)$: $H_0 = 1$, $H_1 = 0.9024$, $H_2 = 0.6667$, $H_3 = 0.4310$ and $H_4 = 1/3$. The signals $\cos(2\pi j/8)/H_1$ and $\cos(2\pi \cdot 3j/8)/H_3$ blur to $\cos(2\pi j/8)$ and $\cos(2\pi\cdot 3j/8)$, which agree at the even indices $j$, because $3\pi j'/2 = 2\pi j' - \pi j'/2$ for $j = 2j'$. So a frame with the shift $0$ cannot tell them apart: the frequency $3$ is aliased to the frequency $1$. At the odd indices the two blurred signals are negatives of each other, so a second frame with the shift $1$ separates them.

**Conditioning.** With the shifts $\{0, 1\}$ the two frames give $8$ equations for $8$ unknowns, and the singular values of the stacked operator are the $|H_q|$, from $1$ down to $1/3$: the condition number is $3$. With the shifts $\{0, 2\}$ the residue $1$ is missing, and every $x = B^{-1}v$ with $v$ zero at the even indices gives zero data.

**Astronomy.** The Hubble Deep Field frames were undersampled by the camera and dithered by subpixel offsets; [drizzle](/drizzle/) combined them on a finer grid.

## Known algorithms

- **Shift-and-add.** Place each sample on the fine grid by its shift and average (or take the median). Exact least squares (or L1) for pure translation, before deblurring.
- **[Drizzle](/drizzle/).** Shrink each input pixel to a drop, add it to the overlapped output pixels with area weights, and divide by the weights. Keeps flux; standard in astronomy.
- **[Iterative back-projection](/iterative-back-projection-super-resolution/).** Simulate each frame from the estimate and back-project the differences. Landweber iteration on the stacked operator when the kernel is the mirrored PSF.
- **Regularized least squares.** Minimize the data misfit plus a [Tikhonov](/tikhonov-regularization/) or total variation term, by [conjugate gradients](/conjugate-gradient-method/) or proximal methods.
- **MAP estimation.** A [maximum a posteriori](/maximum-a-posteriori-estimation/) estimate with a Markov random field or a learned prior (Elad and Feuer 1997 give the ML, MAP and set-theoretic forms in one model).
- **Robust methods.** An L1 data term and a bilateral total variation prior (Farsiu et al. 2004).
- **Frequency-domain methods.** For pure global translation, the aliasing relations between the DFTs of the frames give a small linear system per frequency; this was the earliest approach (Tsai and Huang, 1984).

## Bounds

- **Information.** By the identifiability theorem, at least $L^2$ frames with distinct subpixel shifts are needed for a magnification $L$ in 2D, unless a prior fills the gaps.
- **Conditioning.** With a complete set of shifts the problem is deblurring, so the noise in frequency $q$ grows like $1/|H_q|$. The blur of the pixel area itself, a box of the coarse pixel size, has zeros, so some frequencies are lost however many frames are taken.
- **Limits of the reconstruction constraints.** Baker and Kanade (2002) showed that, as the magnification grows, the reconstruction constraints from the frames give less and less information, so the prior dominates the result at large factors. They used learned priors to go further.
- **Optics.** No multi-frame method recovers frequencies above the cutoff of the optical transfer function ([Abbe limit](/abbe-diffraction-limit/)). Multi-frame super-resolution removes the aliasing and the blur of the pixel, up to that cutoff.

## Reductions

- **To deblurring.** With integer shifts that cover every residue once, the problem is [image deblurring](/image-deblurring/) on the fine grid (identifiability theorem).
- **To least squares.** For known motion and blur and Gaussian noise, the problem is a large sparse [least squares problem](/least-squares-problem/), usually regularized.
- **From registration.** Unknown motion adds an [image registration](/image-registration/) problem for each frame, often solved first by [phase correlation](/phase-correlation/) or [Lucas-Kanade](/lucas-kanade-method/).

## Applications

Astronomy (dithered space telescope images, combined by drizzle), satellite and aerial imaging, video enhancement in cameras and phones (bursts of frames from a hand-held camera, whose small motions give the subpixel shifts), document and license plate reading, medical imaging with shifted acquisitions, and microscopy with a moved stage. In fluorescence microscopy, the methods that go beyond the diffraction limit are optical, not multi-frame image processing.

## References
