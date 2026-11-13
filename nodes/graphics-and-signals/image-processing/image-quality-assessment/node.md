---
tag: M0GMJ7
kind: problem
slug: image-quality-assessment
name: Image quality assessment
aliases:
- image quality metrics
- objective image quality assessment
area: graphics-and-signals/image-processing
level: advanced
summary: Compute a score for an image, with or without an undistorted reference, that agrees with the quality that human viewers would report.
prereqs: [psnr, digital-image]
see_also: [structural-similarity-index, mean-squared-error, image-noise, lossy-image-compression, jpeg-compression, image-denoising, super-resolution, normalized-cross-correlation]
sources:
  - paper: doi:10.1109/TIP.2003.819861
    title: "Zhou Wang, Alan C. Bovik, Hamid R. Sheikh and Eero P. Simoncelli, Image quality assessment: from error visibility to structural similarity, IEEE Transactions on Image Processing 13(4), 2004"
    locator: the introduction (full-reference, no-reference and reduced-reference methods) and the review of the error sensitivity approach; Fig. 2 (distorted images with the same MSE of 210 and different SSIM)
  - paper: doi:10.1109/MSP.2008.930649
    title: "Zhou Wang and Alan C. Bovik, Mean squared error: love it or leave it? A new look at signal fidelity measures, IEEE Signal Processing Magazine 26(1), 2009"
    locator: pages 98 to 117 (why MSE fails as a quality measure, and the alternatives)
  - paper: "Hamid R. Sheikh, Muhammad F. Sabir and Alan C. Bovik, A statistical evaluation of recent full reference image quality assessment algorithms, IEEE Transactions on Image Processing 15(11), 2006"
    locator: the subjective study behind the LIVE image quality database and the comparison of full-reference measures against its scores
  - paper: doi:10.1049/el:20080522
    title: Quan Huynh-Thu and Mohammed Ghanbari, Scope of validity of PSNR in image/video quality assessment, Electronics Letters 44(13), 2008
    locator: pages 800 to 801
---

Image quality assessment is the problem of computing a number for an image that predicts how good human viewers would find it. In the full-reference form, the input is a distorted image and its undistorted reference, and the score measures how close they are, as [PSNR](/psnr/) and [SSIM](/structural-similarity-index/) do; in the reduced-reference form only some features of the reference are known, and in the no-reference form there is no reference at all. A method is judged by how well its scores agree with mean opinion scores from subjective tests. The point of the problem is that the simplest distance, the [mean squared error](/mean-squared-error/), often disagrees with what viewers see.

## In plain words

When a photo is compressed, resized or cleaned of noise, someone has to decide whether the result is still good. Asking a room of people is the real test, but it is slow and costly, so we want a program that gives the same answer. If the original photo is available, the program can compare the two pictures. The obvious way, adding up how much each pixel changed, is often wrong: a slightly brighter photo can count as worse than a photo full of visible grain. Better programs look at local patterns, edges and texture, as the eye does. Without the original, the program must guess the quality from the picture alone, by looking for typical faults such as blur, blocks or noise. Every such program is checked against scores from real viewers.

## Definition

**The model.** Images are [digital images](/digital-image/) of $W \times H$ pixels, usually 8-bit gamma-encoded codes, gray or color. Full-reference methods assume that the test image $y$ and the reference $x$ have the same size and are aligned pixel by pixel. Methods that use windows state their window, their border rule and the channel they use.

**Subjective quality.** In a subjective test, viewers rate each image, or each pair of reference and test image, under controlled viewing conditions. The mean over viewers is the mean opinion score (MOS) of the image; the difference between the scores of the test and the reference image is the DMOS.

**The full-reference problem.** Find a function $q(x, y)$ such that, over a database of distorted images $y_j$ with references $x_j$ and scores $s_j$, the values $q(x_j, y_j)$ are monotonically related to $s_j$ as closely as possible. The usual criteria are the Spearman rank correlation between $q$ and $s$, which needs only the order, and the Pearson correlation after a monotone, usually logistic, fit of $q$ to $s$.

**The reduced-reference and no-reference problems.** The same, with $q(f(x), y)$ for a short feature vector $f(x)$ sent with the image, or with $q(y)$ alone.

## Variants

- **Full reference (FR).** The reference is available: compression and transmission tests, denoising and super-resolution benchmarks.
- **Reduced reference (RR).** A small summary of the reference is sent alongside, to monitor quality at the receiver of a network.
- **No reference (NR), or blind.** Only the test image is known, as for photos from a camera or images uploaded by users. Methods either target one distortion, such as blur or block artifacts, or learn from many.
- **Video.** Scores per frame are pooled over time, and motion and temporal artifacts are added.
- **Task-based quality.** The score is the success of a later task, such as recognition or measurement, and not the opinion of viewers.

## Examples

The measured examples below use $L = 255$, the [SSIM](/structural-similarity-index/) defaults ($11 \times 11$ Gaussian window, $\sigma = 1.5$, $K_1 = 0.01$, $K_2 = 0.03$, valid windows only) and gray values as stored.

**Same MSE, different quality.** The $48 \times 48$ test image $x(r, q) = 40 + 2q + r + 30 \cdot ((\lfloor q/8 \rfloor + \lfloor r/8 \rfloor) \bmod 2)$ was changed in two ways: 10 added to every pixel, and $\pm 10$ added with random signs from `random.Random(2026)`.

| distortion | MSE | PSNR | MSSIM |
|---|---|---|---|
| brightness shift of 10 | 100 | 28.13 dB | 0.9967 |
| random signs, $\pm 10$ | 100 | 28.13 dB | 0.7740 |

A viewer sees the first as the same picture, slightly brighter, and the second as noisy. MSE and PSNR cannot tell them apart; SSIM can. Wang and coauthors make the same point with a set of distorted versions of one photo that all have MSE 210 but look very different.

- **Content matters.** Gaussian noise of standard deviation 10 on a flat $64 \times 64$ gray image (`random.Random(6)`) gives PSNR 28.09 dB, about the same as above, but MSSIM 0.3836. Noise on a flat region is easy to see, and SSIM falls more than on the textured test image.
- **A shift of one pixel.** Moving an image by one pixel keeps its quality for a viewer but can lower PSNR and SSIM a lot, because both assume alignment. FR methods need registration first.
- **No reference.** A blind blur detector can score sharpness from the strength of edges in $y$ alone, but it cannot tell a blurred photo from a sharp photo of a soft scene.

## Known algorithms

| method | type | idea | cost for $W \times H$ pixels |
|---|---|---|---|
| [MSE](/mean-squared-error/) and [PSNR](/psnr/) | FR | mean squared pixel error, on a log scale for PSNR | $\Theta(WH)$ |
| [SSIM](/structural-similarity-index/) | FR | local luminance, contrast and structure in windows | $\Theta(WHk)$ for a separable $k$-tap window |
| multiscale SSIM | FR | SSIM terms over several scales of a pyramid | $\Theta(WHk)$ in total over the scales |
| error visibility models | FR | weight the error by a model of the eye's sensitivity to each frequency and of masking | depends on the model |
| information-based and learned measures | FR, RR or NR | compare statistics of natural images, or features of a trained network | depends on the model |

## Bounds

- **Reading every pixel.** An FR method whose score depends on every pixel takes $\Omega(WH)$ time, so MSE, PSNR and SSIM with a fixed window are optimal up to constant factors.
- **The limit set by viewers.** Viewers do not agree exactly with each other, so the MOS of a database has its own noise. No method can agree with the MOS better than a new group of viewers agrees with it, which bounds the achievable correlation below 1.
- **No measure can be perfect for every use.** The same change, such as stronger contrast or added sharpening, can be judged better by some viewers and worse by others, so quality is not a function of the images alone.

## Reductions

- **PSNR and MSE rank the same.** PSNR is a strictly decreasing function of MSE, so their rank correlations with any MOS are the same; they differ only in the shape of the fitted curve.
- **The structure term is correlation.** With $C_2 = 0$, the structure term of SSIM in each window is the local [normalized cross-correlation](/normalized-cross-correlation/) of the two images.
- **Quality of a sequence.** Video quality reduces to image quality per frame with a pooling step, plus temporal terms.
- **Compression as optimization.** A codec that chooses its parameters to minimize MSE at a given rate is optimizing PSNR; replacing MSE by a perceptual measure in that search is how quality measures enter [lossy image compression](/lossy-image-compression/).

## Applications

Quality measures compare and tune [image compression](/jpeg-compression/) and video codecs, score the output of [denoising](/image-denoising/), [super-resolution](/super-resolution/) and other restoration methods against a clean reference, serve as training losses for image networks, monitor the quality of streamed video, and sort photos in large collections by technical quality. In benchmarks the custom is to report both [PSNR](/psnr/) and [SSIM](/structural-similarity-index/), with their settings stated, because each misses failures that the other catches.

## References
