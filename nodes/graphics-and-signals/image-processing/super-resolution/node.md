---
tag: YS0WCS
kind: problem
slug: super-resolution
name: Super-resolution
aliases:
- image upscaling from low resolution
area: graphics-and-signals/image-processing
level: advanced
summary: Reconstruct a high-resolution image from one or more low-resolution observations.
prereqs: [image-resampling, image-deblurring, aliasing, least-squares-problem]
see_also: [image-registration, image-warping, sampling-theorem, pseudoinverse, tikhonov-regularization, image-denoising, image-inpainting, point-spread-function]
sources:
  - paper: doi:10.1016/1049-9652(91)90045-L
    title: Michal Irani and Shmuel Peleg, Improving resolution by image registration, CVGIP, Graphical Models and Image Processing 53(3):231-239, 1991
    locator: the imaging model with registration, blur and decimation, and the iterative back-projection of the simulation error
  - paper: doi:10.1109/TPAMI.2002.1033210
    title: Simon Baker and Takeo Kanade, Limits on super-resolution and how to break them, IEEE Transactions on Pattern Analysis and Machine Intelligence 24(9):1167-1183, 2002
    locator: the analysis of the reconstruction constraints as the magnification grows, and recognition-based priors
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: the chapter on computational photography (super-resolution and blur removal)
---

Super-resolution is the problem of computing an image with more pixels and finer detail than the images that were observed. In multi-frame super-resolution, the input is several low-resolution images of the same scene, each shifted by a fraction of a pixel, and the output combines them. In single-image super-resolution, the input is one image, and the missing detail must come from a prior, usually learned from pairs of high- and low-resolution images. The standard model is $f_k = D B W_k u + n_k$: the unknown sharp image $u$ is warped by the motion $W_k$ of frame $k$, blurred by the [point spread function](/point-spread-function/) $B$ of the camera, subsampled by $D$, and corrupted by noise. Multi-frame methods work only because the frames are [aliased](/aliasing/): each frame folds high frequencies into low ones in a different way, and several frames together can separate them again. Plain [image resampling](/image-resampling/) with an interpolation kernel adds pixels but no information, and it is the baseline that super-resolution methods are compared with.

## In plain words

A small photo has few pixels, so fine details such as text and faces are lost. Making the photo bigger by stretching it only makes the pixels bigger or blurrier. Super-resolution tries to add real detail. One way is to take many photos of the same scene, each shifted a little, less than one pixel. Each photo sees the scene through a slightly different grid, so together they know more than any one of them. Another way uses only one photo, and fills in detail that is typical of such scenes, as learned from many examples. The first way recovers real detail up to a limit; the second way can draw detail that looks right but was never in the scene.

## Definition

Let $u$ be the unknown image on a fine grid of $N$ pixels, and $f_1, \ldots, f_K$ the observed images on a coarse grid, $s$ times coarser in each direction. The observation model is

$$f_k = A_k u + n_k, \qquad A_k = D B W_k,$$

with $W_k$ the geometric motion of frame $k$ (a subpixel shift in the simplest case), $B$ the blur of the optics and the sensor, $D$ the subsampling by $s$, and $n_k$ noise. The problem is to estimate $u$ from the $f_k$, given the $A_k$ or after estimating the motions by [image registration](/image-registration/). Stacking the frames gives one linear system $f = Au + n$. The usual estimate is

$$\hat u = \arg\min_u \sum_k \lVert A_k u - f_k\rVert^2 + \alpha R(u),$$

a [least squares problem](/least-squares-problem/) with a regularizer $R$, or the maximum a posteriori estimate under a prior on $u$. Single-image super-resolution is the case $K = 1$, where $A$ has fewer rows than columns and the prior must supply the rest.

## Variants

- Multi-frame from a burst or a video, with known or estimated motion between frames.
- Single-image, with an interpolation, a prior on edges, examples from the image itself, or a learned mapping.
- Video super-resolution, where each output frame uses its neighbors in time.
- Super-resolution of special classes, such as faces and text, with a prior specific to the class.
- The magnification factor $s$, usually 2, 3 or 4; at larger factors almost all the detail must come from the prior.
- In optics, "super-resolution microscopy" means methods that resolve detail below the diffraction limit of the lens, with special illumination or molecules that blink. That is a different problem, which changes the imaging process instead of combining pixels.

## Examples

Take a row of 8 fine pixels $u_0, \ldots, u_7$ with periodic borders, and coarse pixels that are the mean of two fine pixels. One frame gives the 4 values $(u_{2i} + u_{2i+1})/2$, a system of rank 4: half of the unknowns are free. A second frame shifted by one fine pixel gives $(u_{2i+1} + u_{2i+2})/2$. In exact arithmetic, the 8 equations of both frames have rank 7, not 8: the pattern $(1, -1, 1, -1, 1, -1, 1, -1)$ sums to 0 over every pair, so both frames are blind to it. The two-pixel mean has a zero in its transfer function at the highest frequency, and no number of shifted frames can recover that frequency.

With the same two shifts and other blurs:

| coarse pixel | rank of 2 frames (of 8) |
|---|---|
| mean of 2 fine pixels | 7 |
| mean of 3 fine pixels, centered | 8 |
| point sample of 1 fine pixel | 8 |

The mean of three pixels has transfer function $\tfrac13 + \tfrac23 \cos\omega$, which is $-\tfrac13$ at the highest frequency, not 0, so the two frames determine $u$. With point samples, the two frames are the even and the odd fine pixels, and interleaving them gives $u$ exactly. A full rank is not enough in practice: when the transfer function is small but not zero, the system is badly conditioned and noise is amplified, as in [deblurring](/image-deblurring/).

## Known algorithms

- Interpolation, the baseline: nearest, bilinear, bicubic and Lanczos [resampling](/image-resampling/). It does not add frequencies above the coarse Nyquist limit.
- Shift-and-add: register the frames, place their samples on the fine grid, average, then deblur.
- Iterative back-projection, by Irani and Peleg: simulate the frames from the current estimate, and add the back-projected difference between the real and the simulated frames.
- Regularized least squares and maximum a posteriori methods: minimize the data term with a Tikhonov, total variation or robust prior, by conjugate gradients or proximal methods; the frequency-domain method of Tsai and Huang solves the case of pure translation.
- Example-based methods: Freeman, Jones and Pasztor matched patches of the input to a database of pairs of low- and high-resolution patches; later methods use patches of the image itself at other scales, and sparse codes over learned dictionaries.
- Learned methods: convolutional networks trained on pairs of downsampled and original images, starting with SRCNN by Dong, Loy, He and Tang, and generative models that aim at images that look sharp rather than at the least squared error.

## Bounds

- Multi-frame methods can recover at most the frequencies that the blur $B$ passes: where its transfer function is zero, every frame is blind, as in the example.
- If the frames are band-limited below their own Nyquist frequency, they are not aliased, and by the [sampling theorem](/sampling-theorem/) every frame is an exact interpolation of any other; then extra frames reduce noise but add no resolution.
- Counting unknowns, magnification $s$ in each direction needs at least $s^2$ frames with distinct shifts to give as many equations as unknowns.
- Baker and Kanade showed that, for a box-shaped sensor and growing magnification, the reconstruction constraints give less and less information, and the null space or the poorly conditioned subspace grows, so large factors need a strong prior.
- Single-image super-resolution has no unique answer: many sharp images give the same small image, and a learned method picks one typical of its training data.

## Reductions

- With known motion, multi-frame super-resolution is a linear inverse problem, solved by [least squares](/least-squares-problem/), the [pseudoinverse](/pseudoinverse/) or [Tikhonov regularization](/tikhonov-regularization/).
- With one frame and $D = I$, it is [deblurring](/image-deblurring/); with $D = I$ and $B = I$, it is [denoising](/image-denoising/).
- With $B = I$ and point samples on a fine grid that is partly observed, it is [inpainting](/image-inpainting/) of the missing fine pixels.
- The motions $W_k$ come from [image registration](/image-registration/) or [optical flow](/optical-flow/), and they are applied by [image warping](/image-warping/).

## Applications

- Smartphone cameras that merge a burst of frames, shifted by hand shake, into one sharper photo.
- Satellite and aerial imaging, from several passes or from sensors with shifted pixel grids.
- Surveillance video, to read license plates and faces.
- Medical imaging, such as MRI slices merged into a finer volume.
- Upscaling old video and games to high-resolution displays.

## References
