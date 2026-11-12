---
tag: H7K4T6
kind: technique
slug: transform-coding
name: Transform coding
aliases:
- block transform coding
area: compression-and-coding/transforms-for-compression
level: core
summary: Applies a decorrelating transform, quantizes the coefficients, then entropy-codes them.
prereqs: [orthogonal-transform, energy-compaction, signal-decorrelation]
see_also: [scalar-quantization, discrete-cosine-transform, karhunen-loeve-transform, jpeg-compression, subband-coding, predictive-coding, lossy-compression, modified-discrete-cosine-transform]
sources:
  - paper: doi:10.1109/TCOM.1963.1088759
    title: J. J. Y. Huang and P. M. Schultheiss, Block quantization of correlated Gaussian random variables, IEEE Transactions on Communications Systems 11(3), 1963
    locator: pp. 289 to 296 (the KLT, the optimal bit allocation and the gain of block quantization of Gaussian vectors)
  - book: isbn:9780132119139
    title: N. S. Jayant and Peter Noll, Digital Coding of Waveforms, Prentice-Hall, 1984
    locator: Chapter 12, Transform Coding (bit allocation, the transform coding gain as the ratio of the arithmetic and geometric means of the coefficient variances, and the comparison of transforms)
  - book: isbn:9780792391814
    title: Allen Gersho and Robert M. Gray, Vector Quantization and Signal Compression, Kluwer, 1992
    locator: Chapter 8, Bit Allocation and Transform Coding
  - paper: doi:10.1109/79.952802
    title: Vivek K. Goyal, Theoretical foundations of transform coding, IEEE Signal Processing Magazine 18(5), 2001
    locator: pp. 9 to 21 (the standard model, the high-resolution analysis, and when the KLT is and is not optimal)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Section 10.3.3, simultaneous description of independent Gaussian random variables (reverse water-filling)
  - book: isbn:9780128094747
    title: Khalid Sayood, Introduction to Data Compression, fifth edition, Morgan Kaufmann, 2017
    locator: Chapter 13, Transform Coding
  - url: https://www.w3.org/Graphics/JPEG/itu-t81.pdf
    title: ITU-T Recommendation T.81 (09/92), Digital compression and coding of continuous-tone still images, Requirements and guidelines
    locator: Annex A.3 (the 8 x 8 FDCT, quantization and the zigzag order) and Annex F (sequential DCT-based mode)
---

Transform coding is the method of [lossy compression](/lossy-compression/) that cuts a signal into blocks, maps each block by an [orthogonal transform](/orthogonal-transform/) to coefficients, quantizes each coefficient on its own with [scalar quantization](/scalar-quantization/), and codes the quantized values with an entropy coder such as [Huffman coding](/huffman-coding/) or [arithmetic coding](/arithmetic-coding/). The transform does no compression by itself. It [decorrelates](/signal-decorrelation/) the samples and [compacts the energy](/energy-compaction/) into a few coefficients, so that simple scalar quantizers on the coefficients do almost as well as a much harder quantizer on the whole block. For a Gaussian source at high rate, the gain over quantizing the samples directly is the ratio of the arithmetic and geometric means of the coefficient variances. JPEG, MP3, AAC and most video coders are transform coders.

## In plain words

Neighboring samples of a picture or a sound are similar, so coding each sample alone repeats the same information many times. A transform coder first rewrites each block of samples as a mix of fixed patterns: a flat pattern, a slow wave, a faster wave, and so on. For smooth data, a few patterns carry almost all of the block, and the rest have tiny weights.

The coder then rounds each weight to a step size. Large, important weights get fine steps and many bits. Small weights get coarse steps and often become zero, which costs almost nothing to send. A lossless coder then packs the rounded weights.

The decoder multiplies the rounded weights by the patterns and adds them up. Because the patterns are at right angles to each other, the error in the rebuilt block is exactly the rounding error of the weights.

## When it applies

- **The source is correlated.** Samples near each other have a large correlation, so a transform can move most of the variance into a few coefficients. For a white source every orthogonal transform gives equal variances, and the gain is 1.
- **The distortion is the mean squared error**, or a weighted version of it. An orthogonal transform keeps squared error, so an error budget in the signal domain becomes a budget in the coefficient domain.
- **Blocks are natural.** The data can be cut into blocks of a fixed size $N$ (8 x 8 pixels, 576 or 1024 audio samples), or into overlapping frames as with the MDCT.
- **The model of the analysis.** The gain formula below assumes a zero-mean source with covariance matrix $R$, Gaussian when optimality is claimed, and the high-resolution model of each quantizer. At low rates it is a guide, not a law.

## The template

**Notation.** $x \in \mathbb{R}^N$ is a block, $R = E[xx^{\mathsf T}]$ its covariance, $T$ an orthogonal $N \times N$ matrix, $y = Tx$ the coefficients with variances $\sigma_k^2 = (TRT^{\mathsf T})_{kk}$, $\Delta_k$ the quantizer step of coefficient $k$, $b_k$ its rate in bits per coefficient, and $b = \frac1N \sum_k b_k$ the mean rate in bits per sample.

```pseudo id=main
TRANSFORM-CODE(x, T, Δ)                   ▷ encode one block
L1  y ← T x
L2  for k ← 0 to N − 1 do
L3      q[k] ← round(y[k] / Δ[k])
L4  return ENTROPY-CODE(q)

TRANSFORM-DECODE(bits, T, Δ)              ▷ decode one block
L5  q ← ENTROPY-DECODE(bits)
L6  ŷ[k] ← q[k] · Δ[k] for each k
L7  return T^T ŷ
```

The reconstruction error is $x - \hat x = T^{\mathsf T}(y - \hat y)$, so $\|x - \hat x\|^2 = \|y - \hat y\|^2$: the squared error of the block is the sum of the squared errors of the coefficients. This is the property that lets the coder treat each coefficient on its own.

**The high-resolution model.** A scalar quantizer at rate $b_k$ bits on a coefficient of variance $\sigma_k^2$ has mean squared error

$$D_k = c\, \sigma_k^2\, 2^{-2b_k},$$

where the constant $c$ depends on the shape of the distribution and the kind of quantizer. For a Gaussian coefficient and a uniform quantizer followed by an ideal entropy coder, $c = \pi e/6 \approx 1.42$; the distortion is $\Delta^2/12$ and the rate is the differential entropy minus $\log_2 \Delta$. The model holds when the step is small compared to $\sigma_k$.

**Theorem (optimal bit allocation and coding gain).** Fix the mean rate $b$ and let the $b_k$ be real numbers with $\frac1N \sum_k b_k = b$. The mean distortion $D = \frac1N \sum_k D_k$ is smallest when

$$b_k = b + \frac12 \log_2 \frac{\sigma_k^2}{\mathrm{GM}}, \qquad \mathrm{GM} = \Big(\prod_k \sigma_k^2\Big)^{1/N},$$

and then $D_{\mathrm{TC}} = c \cdot \mathrm{GM} \cdot 2^{-2b}$. Quantizing the samples directly (PCM) at the same rate gives $D_{\mathrm{PCM}} = c\,\sigma_x^2\, 2^{-2b}$ with $\sigma_x^2 = \frac1N \operatorname{tr} R$. So the coding gain is

$$G_{\mathrm{TC}} = \frac{D_{\mathrm{PCM}}}{D_{\mathrm{TC}}} = \frac{\mathrm{AM}}{\mathrm{GM}} = \frac{\frac1N \sum_k \sigma_k^2}{\left(\prod_k \sigma_k^2\right)^{1/N}} .$$

*Proof.* By the inequality of the arithmetic and geometric means,

$$D = \frac1N \sum_k D_k \ge \Big(\prod_k D_k\Big)^{1/N} = c \Big(\prod_k \sigma_k^2\Big)^{1/N} 2^{-\frac2N \sum_k b_k} = c \cdot \mathrm{GM} \cdot 2^{-2b},$$

and the lower bound does not depend on the allocation. Equality holds exactly when all $D_k$ are equal. The given $b_k$ make $D_k = c\,\sigma_k^2\, 2^{-2b}\, \mathrm{GM}/\sigma_k^2 = c \cdot \mathrm{GM} \cdot 2^{-2b}$ for each $k$, and their mean is $b$ because $\sum_k \log_2(\sigma_k^2/\mathrm{GM}) = 0$. So they reach the bound. For PCM each sample has variance $R_{ii}$; with the same rate $b$ for each sample the mean distortion is $c\, 2^{-2b} \frac1N \sum_i R_{ii} = c\,\sigma_x^2\, 2^{-2b}$. Because $T$ is orthogonal, $\sum_k \sigma_k^2 = \operatorname{tr}(TRT^{\mathsf T}) = \operatorname{tr} R$, so $\sigma_x^2 = \mathrm{AM}$. $\square$

At a fixed distortion the gain becomes a rate saving of $\frac12 \log_2 G_{\mathrm{TC}}$ bits per sample. The result and the allocation rule are due to Huang and Schultheiss (1963); Jayant and Noll (Chapter 12) and Gersho and Gray (Chapter 8) give the same analysis.

**Which transform.** For each orthogonal $T$, Hadamard's inequality gives $\prod_k \sigma_k^2 \ge \det(TRT^{\mathsf T}) = \det R$, with equality when $TRT^{\mathsf T}$ is diagonal. So the [Karhunen-Loève transform](/karhunen-loeve-transform/) has the largest gain, $G_{\mathrm{KLT}} = \mathrm{AM}/(\det R)^{1/N}$. For a Gaussian source at high rate it is the optimal transform. For the first-order autoregressive covariance $R_{ij} = \rho^{|i-j|}$, $\det R = (1-\rho^2)^{N-1}$ and $G_{\mathrm{KLT}} = (1-\rho^2)^{-(N-1)/N}$. The [discrete cosine transform](/discrete-cosine-transform/) comes close and is fast, which is why it is used in practice.

**Low rates: reverse water-filling.** The rule above can give negative $b_k$ for coefficients with $\sigma_k^2 < \mathrm{GM}\, 2^{-2b}$. A practical coder then sets those $b_k$ to 0 and spreads the rate over the others. For independent Gaussian coefficients the exact answer is the rate-distortion function of parallel Gaussian sources (Cover and Thomas, Section 10.3.3): choose a level $\theta$ and set

$$D_k = \min(\theta, \sigma_k^2), \qquad b_k = \max\Big(0, \frac12 \log_2 \frac{\sigma_k^2}{\theta}\Big), \qquad \frac1N\sum_k b_k = b .$$

Coefficients with a variance below $\theta$ get no bits and are sent as zero. When $\theta$ is below every $\sigma_k^2$, this is the high-rate rule with $\theta = \mathrm{GM}\, 2^{-2b}$.

## Classic examples

**AR(1) with the DCT.** Let $N = 8$ and $R_{ij} = 0.9^{|i-j|}$, so $\sigma_x^2 = 1$. The orthonormal DCT-II gives the coefficient variances

$$\sigma_k^2 = (6.1855, 1.0059, 0.3461, 0.1659, 0.1046, 0.0757, 0.0616, 0.0547),$$

which add up to 8. Their geometric mean is 0.23572, so $G_{\mathrm{DCT}} = 1/0.23572 = 4.2424$, or 6.276 dB. The KLT gain is $(1 - 0.81)^{-7/8} = 4.2765$, or 6.311 dB. At $b = 2$ bits per sample the optimal allocation is

$$b_k = (4.357, 3.047, 2.277, 1.747, 1.414, 1.181, 1.032, 0.946),$$

and each coefficient gets the same distortion $c \cdot 0.23572 \cdot 2^{-4}$, against $c \cdot 2^{-4}$ for PCM. At $b = 1$ the formula asks for $-0.054$ bits for the last coefficient. Reverse water-filling at $b = 1$ gives $\theta = 0.05956$ and

$$b_k = (3.349, 2.039, 1.269, 0.739, 0.406, 0.173, 0.024, 0),$$

and at $b = 0.5$ it gives $\theta = 0.2034$, rates $(2.463, 1.153, 0.384, 0, 0, 0, 0, 0)$ and a mean distortion of 0.1341: five of the eight coefficients are not sent at all.

**A measured rate saving.** The test of this page draws 20000 blocks of this AR(1) source (Gaussian, seed 4), quantizes the samples and the DCT coefficients with the same uniform step $\Delta = 0.02$, and measures the empirical entropy of the quantizer indices. Both coders have the same mean squared error, close to $\Delta^2/12$. The transform coder needs 1.0448 fewer bits per sample than PCM; the formula $\frac12 \log_2 4.2424$ predicts 1.0424.

**JPEG.** The baseline mode of ITU-T T.81 cuts each image component into 8 x 8 blocks, subtracts 128, applies the 2D DCT (Annex A.3.3), divides each coefficient by its entry in a quantization table and rounds, reads the coefficients in [zigzag order](/zigzag-scan/), and codes runs of zeros and the nonzero values with Huffman codes. The table gives large steps to high frequencies, which plays the role of the bit allocation. See [JPEG compression](/jpeg-compression/).

**Audio.** MP3, AAC and Vorbis use the lapped [modified discrete cosine transform](/modified-discrete-cosine-transform/) and choose the step of each band from a model of hearing, not from the variance alone.

**Video.** H.264 and HEVC apply integer approximations of the DCT to the residual that is left after motion-compensated prediction.

## Variations

- **Threshold coding versus zonal coding.** Zonal coding keeps a fixed set of coefficients in each block. Threshold coding keeps those that are large in this block, and sends their positions. JPEG is a threshold coder with run-length codes for the positions.
- **Adaptive transform coding.** Change the transform, the steps or the allocation from block to block, and send the choice as side information.
- **Dead-zone and entropy-constrained quantizers.** A wider zero bin and an entropy coder after a uniform quantizer are close to optimal at all rates for many sources.
- **Lapped transforms and filter banks.** Overlapping basis functions remove block edges; see [filter bank](/filter-bank/), [subband coding](/subband-coding/) and [JPEG 2000](/jpeg-2000/), where the same analysis applies with subband variances in place of coefficient variances.
- **Integer and reversible transforms.** Integer approximations of the DCT and lifting-based wavelets allow lossless coding and identical decoding on all machines.
- **Transform plus prediction.** Video coders predict a block from earlier frames and transform the prediction error. [Predictive coding](/predictive-coding/) alone reaches the same gain as the KLT in the limit of long blocks for a stationary Gaussian source.
- **Beyond the KLT.** For non-Gaussian sources, at low rates, or with a fixed entropy coder, the KLT need not be optimal; Goyal (2001) surveys these cases.

## Pitfalls

- **Negative rates.** The high-rate formula gives negative $b_k$ at low rates. Clip and redistribute, or use reverse water-filling.
- **Integer rates.** A fixed-rate coder needs whole numbers of bits. Rounding the optimal $b_k$ loses some of the gain; greedy allocation of one bit at a time to the coefficient with the largest distortion reduction is the usual fix.
- **A non-orthogonal transform.** If $T$ is not orthogonal, the error in the signal is $T^{-1}(y - \hat y)$, which can be larger than the error of the coefficients, and the gain formula does not hold. A scaled orthogonal transform is fine if the scale goes into the steps.
- **The gain is not the compression ratio.** The coding gain compares distortions at the same rate under the high-resolution model. It does not say how many bytes a real coder saves on a given file.
- **The KLT has a cost.** It depends on the source, needs side information or a training step, and has no fast algorithm in general.
- **Block artifacts.** At low rates each block is coded on its own, and the edges between blocks become visible.
- **Removing the mean.** The analysis assumes zero mean. JPEG subtracts 128 before the DCT; a coder of data with a large mean wastes rate on the DC coefficient if it does not.

## Exercises

1. Show that the coding gain of any orthogonal transform on a white source ($R = \sigma^2 I$) is 1.
2. For $N = 2$ and $R = \begin{pmatrix} 1 & \rho \\ \rho & 1 \end{pmatrix}$, find the KLT and show that its gain is $1/\sqrt{1-\rho^2}$. How many bits per sample does it save at $\rho = 0.9$?
3. Prove that the high-rate allocation gives all coefficients the same distortion, and that any other allocation with the same mean rate has a larger mean distortion.
4. In reverse water-filling, show that the mean rate is a continuous, strictly decreasing function of $\theta$ on $(0, \max_k \sigma_k^2)$, so that bisection on $\theta$ finds the level for each $b > 0$.
5. For the AR(1) source, show that $\det R_N = (1-\rho^2)^{N-1}$ and that the KLT gain tends to $1/(1-\rho^2)$ as $N \to \infty$.
6. Quantize the four coefficients of the example on the page [orthogonal transform](/orthogonal-transform/) with step 4 instead of 2. Compute the error in both domains.

## References
