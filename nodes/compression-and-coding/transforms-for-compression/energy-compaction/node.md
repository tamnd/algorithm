---
tag: FX453X
kind: concept
slug: energy-compaction
name: Energy compaction
aliases:
- energy packing
- energy packing efficiency
area: compression-and-coding/transforms-for-compression
level: intro
summary: How much of the signal energy an orthogonal transform puts into a few coefficients. The KLT maximizes it.
prereqs: [orthogonal-transform]
see_also: [signal-decorrelation, karhunen-loeve-transform, discrete-cosine-transform, transform-coding, explained-variance, principal-component-analysis, zigzag-scan, courant-fischer-theorem]
sources:
  - book: isbn:9780132119139
    title: N. S. Jayant and Peter Noll, Digital Coding of Waveforms, Prentice-Hall, 1984
    locator: Chapter 12, Transform Coding (the variance distribution of the coefficients, the KLT and the DCT for first-order Markov sources)
  - paper: doi:10.1073/pnas.35.11.652
    title: Ky Fan, On a theorem of Weyl concerning eigenvalues of linear transformations I, Proceedings of the National Academy of Sciences of the USA 35(11), 1949
    locator: pp. 652 to 655 (the maximum of the trace of a Hermitian matrix over projections onto subspaces of a fixed dimension)
  - paper: doi:10.1049/ip-f-1.1981.0061
    title: R. J. Clarke, Relation between the Karhunen-Loève and cosine transforms, IEE Proceedings F 128(6), 1981
    locator: pp. 359 to 360 (the DCT as the limit of the KLT of a first-order Markov source as the correlation goes to 1)
  - paper: doi:10.1109/79.952802
    title: Vivek K. Goyal, Theoretical foundations of transform coding, IEEE Signal Processing Magazine 18(5), 2001
    locator: pp. 9 to 21 (the optimal transforms for coding and for approximation with a fixed number of coefficients)
---

Energy compaction is the property of an [orthogonal transform](/orthogonal-transform/) that puts most of the energy (for a random source, most of the variance) of a block into a few of its coefficients. It is measured by the fraction of the total that the $m$ largest coefficients carry, for each $m$. For a source with a known covariance, the [Karhunen-Loève transform](/karhunen-loeve-transform/) gives the largest fraction for every $m$ at the same time, and the [discrete cosine transform](/discrete-cosine-transform/) comes close for smooth signals. Compaction is one of the two aims of a transform in [transform coding](/transform-coding/); the other is [signal decorrelation](/signal-decorrelation/), and the two are not the same thing.

## In plain words

An orthogonal transform never adds or removes energy. It only moves energy between its outputs. A good transform for compression moves almost all of the energy into a few outputs and leaves the rest near zero. The coder then spends its bits on the few large outputs and sends the small ones as zero, or drops them.

Think of a smooth row of pixels. Its values are close to their average, so most of the information is in the average. A transform whose first output is the average, and whose other outputs measure slow and then fast changes, puts nearly all the energy into the first output. That is energy compaction.

## The idea

**Notation.** A block $x \in \mathbb{R}^N$ comes from a source with mean zero and covariance matrix $R = E[x x^{\mathsf T}]$ (subtract the mean first if it is not zero). An orthogonal matrix $A$ with rows $a_0, \dots, a_{N-1}$ gives the coefficients $y = Ax$. The *coefficient variances* are

$$\sigma_k^2 = E[y_k^2] = a_k^{\mathsf T} R\, a_k, \qquad k = 0, \dots, N-1 .$$

Because $A$ is orthogonal, $\sum_k \sigma_k^2 = \operatorname{tr}(A R A^{\mathsf T}) = \operatorname{tr} R$: the total does not depend on $A$. Sort the variances in non-increasing order, $\sigma_{(1)}^2 \ge \sigma_{(2)}^2 \ge \dots \ge \sigma_{(N)}^2$.

**The measures.**

- The *energy packing efficiency* of the first $m$ coefficients is
  $$\eta_m(A) = \frac{\sum_{i=1}^{m} \sigma_{(i)}^2}{\sum_{k} \sigma_k^2}, \qquad m = 1, \dots, N .$$
  Its complement $1 - \eta_m$ is the mean squared error, as a fraction of the total, when the decoder keeps only the $m$ largest-variance coefficients and sets the others to zero. This follows from the equal error in the two domains (fact 3 on the page [orthogonal transform](/orthogonal-transform/)).
- The *coding gain* $G(A) = \frac{\frac1N \sum_k \sigma_k^2}{\left(\prod_k \sigma_k^2\right)^{1/N}}$ is the ratio of the arithmetic and geometric means of the variances. It is 1 when the variances are equal and grows as they become more unequal. It is the gain in mean squared error of high-rate [transform coding](/transform-coding/) over coding the samples directly, and the page on transform coding proves this.
- For one block, without a probability model, the same fraction can be taken over the squared coefficients $y_k^2$ of that block. This is what a coder that keeps a fixed set of coefficients actually sees.

**The upper bound, and who reaches it.** Let $\lambda_1 \ge \dots \ge \lambda_N$ be the eigenvalues of $R$, with orthonormal eigenvectors $v_1, \dots, v_N$. Then for each orthogonal $A$ and each $m$,

$$\sum_{i=1}^{m} \sigma_{(i)}^2 \le \sum_{i=1}^{m} \lambda_i ,$$

and the Karhunen-Loève transform, whose rows are $v_1, \dots, v_N$, reaches equality for every $m$. This is Ky Fan's maximum principle (Fan 1949).

*Proof.* Take any $m$ orthonormal vectors $a_1, \dots, a_m$ (the rows with the $m$ largest variances). Write $c_{ik} = v_i^{\mathsf T} a_k$. By the [spectral theorem](/spectral-theorem/), $R = \sum_i \lambda_i v_i v_i^{\mathsf T}$, so

$$\sum_{k=1}^{m} a_k^{\mathsf T} R\, a_k = \sum_{i=1}^{N} \lambda_i w_i, \qquad w_i = \sum_{k=1}^{m} c_{ik}^2 .$$

Each $w_i$ is the squared length of the projection of the unit vector $v_i$ onto the span of $a_1, \dots, a_m$, so $0 \le w_i \le 1$. Also $\sum_i w_i = \sum_k \sum_i c_{ik}^2 = \sum_k \|a_k\|^2 = m$, because $v_1, \dots, v_N$ is an orthonormal basis. A sum $\sum_i \lambda_i w_i$ with weights in $[0, 1]$ that add up to $m$ is largest when the weight 1 goes to the $m$ largest $\lambda_i$: moving weight from a smaller $\lambda_j$ to a larger $\lambda_i$ never decreases the sum. So the sum is at most $\lambda_1 + \dots + \lambda_m$. For $a_k = v_k$ the weights are exactly $w_1 = \dots = w_m = 1$, so equality holds. $\square$

The coding gain has a matching bound: $G(A) \le G(\text{KLT})$, by Hadamard's inequality $\prod_k \sigma_k^2 \ge \det(ARA^{\mathsf T}) = \det R = \prod_i \lambda_i$. The proof is on the page [Karhunen-Loève transform](/karhunen-loeve-transform/).

**Compaction is not decorrelation.** Compaction looks only at the diagonal of the coefficient covariance $AR A^{\mathsf T}$: how the fixed total is spread over the coefficients. [Signal decorrelation](/signal-decorrelation/) looks only at the entries off the diagonal. The two can disagree in both directions:

- A white source, $R = \sigma^2 I$, is already decorrelated, and each orthogonal transform gives equal variances, so no transform compacts it. Its coding gain is 1 for every $A$.
- The [whitening](/whitening/) transform $R^{-1/2}$ decorrelates any source, but it makes all variances equal to 1. It is not orthogonal, and it destroys compaction.
- The DCT of a first-order autoregressive source does not fully decorrelate it, but its compaction is very close to the optimum (next section).

The two aims meet at the KLT. When the eigenvalues are distinct, it is the only orthogonal transform (up to the order and the signs of the rows) that reaches the compaction bound for every $m$, because equality for each $m$ forces the first $m$ rows to span the first $m$ eigenvectors. It is also the only one that makes the coefficients uncorrelated.

**Compaction is a property of a source and a transform together.** No transform compacts every signal. The DCT compacts smooth blocks, but a block of white noise or a single sharp edge spreads its energy over many DCT coefficients.

## Examples

**First-order autoregressive source.** Let the source be the stationary AR(1) process with unit variance and correlation $\rho$ between neighbors, so $R_{ij} = \rho^{|i-j|}$. For $N = 8$ and $\rho = 0.95$ the energy packing efficiency of four transforms is:

| $m$ | 1 | 2 | 3 | 4 | 8 |
|---|---|---|---|---|---|
| identity (no transform) | 0.125 | 0.250 | 0.375 | 0.500 | 1 |
| unitary DFT | 0.8781 | 0.9177 | 0.9572 | 0.9689 | 1 |
| Walsh-Hadamard | 0.8781 | 0.9390 | 0.9581 | 0.9750 | 1 |
| DCT-II | 0.8781 | 0.9500 | 0.9716 | 0.9819 | 1 |
| KLT | 0.8788 | 0.9507 | 0.9717 | 0.9819 | 1 |

The coefficient variances of the KLT (its eigenvalues) are $7.0303, 0.5751, 0.1683, 0.0818, 0.0509, 0.0370, 0.0300, 0.0266$. The DCT variances are $7.0249, 0.5749, 0.1733, 0.0820, 0.0512, 0.0370, 0.0300, 0.0266$. The coding gains are 7.667 (8.846 dB) for the KLT, 7.631 (8.826 dB) for the DCT, 6.232 for the Walsh-Hadamard transform and 5.738 for the unitary DFT. The DFT does worse than the DCT because its basis treats the block as one period of a periodic signal, and the jump from the last sample back to the first spreads energy into high frequencies; the DCT treats the block as half of a symmetric signal with no jump. The DFT variances also come in equal pairs ($0.3163$ twice, $0.0932$ twice, and so on) because a real input has conjugate-symmetric DFT coefficients.

As $\rho \to 1$, the KLT of this source tends to the DCT-II (Clarke 1981). For $N = 8$ the KLT and DCT gains are 1.093 dB and 1.050 dB at $\rho = 0.5$, 6.311 dB and 6.276 dB at $\rho = 0.9$, and 14.885 dB and 14.880 dB at $\rho = 0.99$.

**One block.** The row of eight pixel values $x = (10, 11, 12, 14, 15, 15, 14, 12)$ has energy $\|x\|^2 = 1351$. Its orthonormal DCT-II is $(36.416, -3.159, -3.616, 1.210, -0.354, 0.207, -0.416, -0.119)$. The first coefficient alone carries 98.159 percent of the energy, the first two 98.897 percent, and the first three 99.865 percent. If the decoder keeps only those three and sets the other five to zero, the squared error is the energy of the five dropped coefficients, $1.819$, which is 0.135 percent of the total.

**No compaction.** For a white source every orthogonal transform has $\eta_m = m/N$, the line of the identity in the table.

## Where it is used

- **Choosing a transform.** The KLT is the bound, but it depends on the source and costs $O(N^2)$ operations per block with no fast algorithm in general. The DCT is fixed, has fast algorithms, and loses little compaction on smooth image and audio data. This is why JPEG and MPEG use it, and why later video coders use integer approximations of it; see [JPEG compression](/jpeg-compression/) and [lossy image compression](/lossy-image-compression/).
- **Zonal coding and coefficient selection.** A coder that keeps only a fixed zone of $m$ low-frequency coefficients has a mean squared error of $1 - \eta_m$ times the signal power. The [zigzag scan](/zigzag-scan/) of JPEG orders the 64 coefficients of a block from low to high frequency, which is roughly the order of decreasing variance, so that the zero coefficients form long runs at the end.
- **Bit allocation.** Coefficients with a large variance get more bits. The optimal allocation and the coding gain are on the page [transform coding](/transform-coding/).
- **Dimension reduction.** In statistics and machine learning, the fraction $\eta_m$ of the KLT is the [explained variance](/explained-variance/) of the first $m$ principal components in [principal component analysis](/principal-component-analysis/). The quantity is the same; the use is different. PCA keeps the components to describe the data in fewer dimensions, while a coder keeps all coefficients and spends fewer bits on the small ones.
- **Wavelet and subband coders.** A wavelet transform compacts the energy of smooth regions into the low-pass band, and the energy of edges into a few large detail coefficients. See [subband coding](/subband-coding/) and [JPEG 2000](/jpeg-2000/).

## References
