---
tag: DWVCRA
kind: problem
slug: lossy-image-compression
name: Lossy image compression
aliases:
- lossy image coding
area: compression-and-coding/transforms-for-compression
level: intro
summary: "Code a digital image in as few bits as possible when the decoded image may differ from the original, with the error measured by MSE, PSNR or SSIM."
prereqs: [lossy-compression, digital-image]
see_also: [jpeg-compression, jpeg-2000, spiht, transform-coding, psnr, structural-similarity-index, color-spaces, image-quality-assessment]
sources:
  - paper: doi:10.1109/TIP.2003.819861
    title: Zhou Wang, Alan C. Bovik, Hamid R. Sheikh and Eero P. Simoncelli, Image quality assessment, from error visibility to structural similarity, IEEE Transactions on Image Processing 13(4), 2004
    locator: pages 600 to 612; Section III (the luminance, contrast and structure terms, the SSIM formula with C1 = (K1 L)^2 and C2 = (K2 L)^2, K1 = 0.01, K2 = 0.03, the 11 x 11 Gaussian window with standard deviation 1.5, and the mean SSIM)
  - url: https://www.w3.org/Graphics/JPEG/jfif3.pdf
    title: Eric Hamilton, JPEG File Interchange Format, Version 1.02, C-Cube Microsystems, 1992
    locator: section Conversion to and from RGB (the YCbCr equations)
  - url: https://www.itu.int/rec/T-REC-T.871
    title: ITU-T Recommendation T.871 (05/2011), Information technology, Digital compression and coding of continuous-tone still images, JPEG File Interchange Format (JFIF)
    locator: clause 7, conversion to and from RGB
  - url: https://www.w3.org/Graphics/JPEG/itu-t81.pdf
    title: ITU-T Recommendation T.81 (09/92), Digital compression and coding of continuous-tone still images, Requirements and guidelines
    locator: Clause 4 (overview of the coding processes) and Annex A (sampling factors of the components, and the DCT-based process)
  - url: https://www.itu.int/rec/T-REC-T.800
    title: ITU-T Recommendation T.800, Information technology, JPEG 2000 image coding system, Core coding system (also ISO/IEC 15444-1)
    locator: Annex A (the codestream) and Annex G (DC level shifting and the component transforms)
  - paper: doi:10.1145/103085.103089
    title: Gregory K. Wallace, The JPEG still picture compression standard, Communications of the ACM 34(4), 1991
    locator: pages 30 to 44
  - book: isbn:9780792375197
    title: David S. Taubman and Michael W. Marcellin, JPEG2000, Image Compression Fundamentals, Standards and Practice, Kluwer, 2002
    locator: Part I (image compression fundamentals, quantization, transforms and rate control)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Chapter 10, Rate distortion theory (Section 10.3.3, reverse water-filling for independent Gaussian components)
---

Lossy image compression is the problem of coding a [digital image](/digital-image/) in as few bits as possible when the decoded image may differ from the original. The coder trades rate, in bits per pixel, against distortion, measured by the mean squared error and [PSNR](/psnr/) or by a perceptual index such as [SSIM](/structural-similarity-index/). Most practical coders follow one pipeline: a colour transform to luma and chroma, chroma subsampling, a decorrelating transform such as the [DCT](/discrete-cosine-transform/) or the [wavelet transform](/discrete-wavelet-transform/), [quantization](/scalar-quantization/), and entropy coding. [JPEG](/jpeg-compression/) (1992) and [JPEG 2000](/jpeg-2000/) (2000) are the two standard solutions for still images.

## In plain words

A photo has millions of numbers, but the eye does not see most of the fine detail, and neighbouring pixels are very alike. A lossy coder uses both facts. It keeps the brightness at full size and stores the colour at a lower resolution, because the eye sees colour detail poorly. It then rewrites each small area as a sum of smooth and fine patterns, and stores the strength of each pattern with few digits, dropping the fine patterns that are too weak to see. A final step packs the remaining numbers tightly.

The decoded photo is not the same as the original, so you need a way to say how far it is from it. One way counts the average squared difference of the pixels. Another way compares local brightness, contrast and structure, which matches what people see more closely.

## Definition

**Input.** An image $x$ with $H$ rows, $W$ columns and $C$ components (1 for grey, 3 for colour), each sample an integer with $B$ bits, often $B = 8$. A target rate $R$ in bits per pixel, or a target distortion $D$.

**Output.** An encoder $E$ that maps the image to a bit string and a decoder $G$ that maps the bit string to an image $\hat x = G(E(x))$ of the same size, such that $|E(x)| \le R \cdot HW$ and the distortion $d(x, \hat x)$ is as small as possible, or $d(x, \hat x) \le D$ with $|E(x)|$ as small as possible.

The problem has no exact optimum in practice. For a random source of images with a known distribution, the best trade-off on average is the rate distortion function $R(D)$ of [lossy compression](/lossy-compression/), but natural images have no agreed probability model, so coders are compared by measuring rate and distortion on test images.

**Mean squared error and PSNR.** For one component with $N = HW$ samples,

$$\mathrm{MSE} = \frac{1}{N} \sum_{i} (x_i - \hat x_i)^2, \qquad \mathrm{PSNR} = 10 \log_{10} \frac{P^2}{\mathrm{MSE}} \ \text{dB},$$

with peak $P = 2^B - 1 = 255$ for 8-bit samples. PSNR is infinite for equal images.

**SSIM.** Wang, Bovik, Sheikh and Simoncelli (2004) compare two windows $x$ and $y$ by their weighted means $\mu_x, \mu_y$, variances $\sigma_x^2, \sigma_y^2$ and covariance $\sigma_{xy}$:

$$\mathrm{SSIM}(x, y) = \frac{(2 \mu_x \mu_y + C_1)(2 \sigma_{xy} + C_2)}{(\mu_x^2 + \mu_y^2 + C_1)(\sigma_x^2 + \sigma_y^2 + C_2)},$$

with $C_1 = (K_1 P)^2$, $C_2 = (K_2 P)^2$, $K_1 = 0.01$ and $K_2 = 0.03$. The first factor compares luminance; the second is the product of their contrast and structure terms when the structure constant is $C_2/2$. The mean SSIM of two images averages the index over local windows, an $11 \times 11$ circular Gaussian window with standard deviation 1.5 samples in the paper. SSIM is 1 only for equal windows, is symmetric, and is at most 1.

```pseudo id=main
SSIM(x, y, w)                 ▷ two windows of n samples, weights w with Σ w_i = 1
L1  C1 ← (K1 · P)², C2 ← (K2 · P)²
L2  μx ← Σ w_i x_i; μy ← Σ w_i y_i
L3  σx² ← Σ w_i (x_i − μx)²; σy² ← Σ w_i (y_i − μy)²; σxy ← Σ w_i (x_i − μx)(y_i − μy)
L4  return (2 μx μy + C1)(2 σxy + C2) / ((μx² + μy² + C1)(σx² + σy² + C2))
MEAN-SSIM(X, Y)
L5  for each position of an 11 × 11 window that lies inside the image
L6      add SSIM(window of X, window of Y, Gaussian weights with σ = 1.5)
L7  return the sum divided by the number of positions
```

The mean SSIM costs $O(HW s^2)$ for an $s \times s$ window. The code on this page uses every window that fits inside the image.

## Variants

- **Fixed rate or fixed quality.** A coder meets a bit budget (rate control) or a quality target. JPEG has no rate control of its own: the encoder scales the quantization table and tries again. JPEG 2000 cuts its embedded code blocks to an exact budget.
- **Embedded or progressive coding.** Every prefix of the bit stream decodes to an image, of rising quality, as in [SPIHT](/spiht/) and JPEG 2000, or the progressive mode of JPEG.
- **Near-lossless coding.** Every sample error is at most a given $\delta$, a bound on the maximum error instead of the mean.
- **Region of interest.** Some regions get more bits than others.
- **Perceptual criteria.** The distortion is weighted by the contrast sensitivity of the eye, as in the quantization tables of JPEG, or measured by SSIM and its multiscale forms. See [image quality assessment](/image-quality-assessment/).
- **Grey or colour, and the bit depth.** Medical and scientific images have 12 or 16 bits per sample, which JPEG baseline does not support and JPEG 2000 does.

## Examples

**PSNR.** The samples $(52, 55, 61, 66)$ decoded as $(54, 55, 60, 70)$ have squared errors $4, 0, 1, 16$, so $\mathrm{MSE} = 5.25$ and $\mathrm{PSNR} = 10 \log_{10}(65025 / 5.25) = 40.93$ dB.

**SSIM of one window.** With equal weights on the same four samples, $\mu_x = 58.5$, $\mu_y = 59.75$, $\sigma_x^2 = 29.25$, $\sigma_y^2 = 40.1875$ and $\sigma_{xy} = 32.875$. With $C_1 = 6.5025$ and $C_2 = 58.5225$ the luminance factor is 0.99978 and the contrast and structure factor is 0.97118, so SSIM is 0.97097.

**Same PSNR, different SSIM.** Take a $32 \times 32$ image that is a gradient, $40 + 4r + 2c$, plus 30 on the dark squares of a checkerboard of $4 \times 4$ squares. Adding 10 to every pixel and adding $\pm 10$ at random (seed 7) both give $\mathrm{MSE} = 100$ and $\mathrm{PSNR} = 28.13$ dB. The mean SSIM with the $11 \times 11$ Gaussian window is 0.9976 for the shift and 0.8530 for the noise: the shift changes only the luminance term, while the noise breaks the local structure.

**Colour.** The JFIF conversion maps 8-bit $(R, G, B)$ to

$$Y = 0.299 R + 0.587 G + 0.114 B,$$
$$C_b = -0.1687 R - 0.3313 G + 0.5 B + 128, \qquad C_r = 0.5 R - 0.4187 G - 0.0813 B + 128,$$

and back by $R = Y + 1.402 (C_r - 128)$, $G = Y - 0.34414 (C_b - 128) - 0.71414 (C_r - 128)$, $B = Y + 1.772 (C_b - 128)$. White goes to $(255, 128, 128)$ and every grey has $C_b = C_r = 128$. Pure red gives $C_r = 255.5$, which must be clamped to 255. With the values rounded to integers and clamped, the round trip changes no channel by more than 1 on a grid of every fifth value. These are the luma weights of ITU-R BT.601, used here with the full range 0 to 255.

**Chroma subsampling 4:2:0.** Keep $Y$ at full size and replace $C_b$ and $C_r$ by the mean of each $2 \times 2$ block. The image then has $1 + 2/4 = 1.5$ samples per pixel instead of 3, half as many, before any transform. A constant chroma plane comes back exactly; a one-pixel checkerboard of chroma comes back as a flat 127.5.

## Known algorithms

**The usual pipeline.**

1. *Colour transform.* RGB to YCbCr (JPEG, JFIF), or the reversible integer transform RCT or the real ICT of JPEG 2000. See [colour spaces](/color-spaces/).
2. *Chroma subsampling.* 4:2:0, 4:2:2 or none, set in JPEG by the sampling factors of each component.
3. *Transform.* The $8 \times 8$ [DCT](/discrete-cosine-transform/) in JPEG ([transform coding](/transform-coding/)); the [discrete wavelet transform](/discrete-wavelet-transform/) in JPEG 2000 and SPIHT ([subband coding](/subband-coding/)); integer DCT-like transforms with [prediction](/predictive-coding/) inside the frame in the image formats that reuse video codecs.
4. *Quantization.* A uniform or dead-zone [scalar quantizer](/scalar-quantization/) per coefficient, or [vector quantization](/vector-quantization/).
5. *Ordering and entropy coding.* The [zigzag scan](/zigzag-scan/) with run-length and [Huffman coding](/huffman-coding/) in JPEG; [bit-plane coding](/bit-plane-coding/) with context-adaptive [arithmetic coding](/arithmetic-coding/) in JPEG 2000; set partitioning in SPIHT.

**Standard and classic coders.**

| method | transform | quantizer | entropy coding | embedded |
|---|---|---|---|---|
| [JPEG](/jpeg-compression/) baseline (T.81) | $8 \times 8$ DCT | uniform, table per component | Huffman of run/size | no |
| [JPEG 2000](/jpeg-2000/) (T.800) | 5/3 or 9/7 wavelet | dead zone per subband | bit planes, MQ arithmetic coder | yes |
| [SPIHT](/spiht/) | wavelet | bit planes (embedded) | set partitioning, optional arithmetic coding | yes |
| [Vector quantization](/vector-quantization/) | none or a transform | codebook | fixed or entropy coded indices | no |

All of them run in time linear in the number of pixels for a fixed block size, number of levels and codebook size.

## Bounds

- **Rate distortion.** For a stationary Gaussian model of the image with a known power spectrum, the rate distortion function under MSE is given by reverse water-filling over the spectrum (Cover and Thomas, Section 10.3.3 for independent components). It bounds every coder for that model, and transform coding with an ideal entropy coder reaches it at high rate up to the space-filling loss of scalar quantizers, $\pi e / 6$ or 1.53 dB.
- **High rate.** Each extra bit per coefficient lowers the MSE by a factor of 4, which is 6.02 dB of PSNR.
- **No bound for real images.** Without a model, no lower bound on the bits for a given PSNR is known, and claims of a coder's gain hold only for the test images used.

## Reductions

- **Colour to grey.** After the colour transform, each component is coded as a grey image, with its own quantizer and rate. The colour transform removes most of the correlation between the RGB channels.
- **Image coding to scalar quantization.** A transform with good [energy compaction](/energy-compaction/) turns the image into nearly uncorrelated coefficients, so that one scalar quantizer per coefficient does almost as well as a vector quantizer on the whole block.
- **Near-lossless to lossless.** Quantizing the prediction residuals with step $2\delta + 1$ gives a maximum error of $\delta$, and the quantized residuals are then coded losslessly.
- **Lossless as a limit.** With $D = 0$ the problem becomes [lossless compression](/lossless-compression/); JPEG 2000 with the reversible 5/3 transform and no quantization solves both in one codestream.

## Applications

Photographs in cameras, phones and on the web are mostly JPEG files. JPEG 2000 is used in digital cinema, in DICOM medical images, and in archives and satellite imagery, where its high bit depths, lossless mode and embedded stream matter. Image formats built on the intra-frame coding of video codecs, such as WebP and AVIF, apply the same pipeline with prediction, larger and variable transforms, and arithmetic coding. Quality measures like PSNR and SSIM are used to set encoder parameters and to compare coders.

## References
