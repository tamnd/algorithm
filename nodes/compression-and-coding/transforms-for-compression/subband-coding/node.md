---
tag: WGFYEV
kind: technique
slug: subband-coding
name: Subband coding
aliases:
- filter-bank coding
- sub-band coding
area: compression-and-coding/transforms-for-compression
level: advanced
summary: "Split a signal into frequency bands with a critically sampled filter bank, then quantize each band with its own bit budget. The gain is AM over GM of band variances."
prereqs: [filter-bank, scalar-quantization]
see_also: [transform-coding, discrete-wavelet-transform, perfect-reconstruction, bit-plane-coding, jpeg-2000, laplacian-pyramid, modified-discrete-cosine-transform, energy-compaction]
sources:
  - paper: doi:10.1002/j.1538-7305.1976.tb02929.x
    title: R. E. Crochiere, S. A. Webber and J. L. Flanagan, Digital coding of speech in sub-bands, Bell System Technical Journal 55(8), 1976
    locator: pages 1069 to 1085 (the rationale for coding speech in sub-bands, the bit allocation across the bands on perceptual grounds, adaptive quantization in each band, and integer-band sampling)
  - paper: doi:10.1109/TASSP.1986.1164962
    title: John W. Woods and Sean D. O'Neil, Subband coding of images, IEEE Transactions on Acoustics, Speech, and Signal Processing 34(5), 1986
    locator: pages 1278 to 1288 (a 16-band split of an image by a tree of separable quadrature mirror filters, with DPCM coding of the bands)
  - paper: doi:10.1109/TCOM.1963.1088759
    title: J. J. Y. Huang and P. M. Schultheiss, Block quantization of correlated Gaussian random variables, IEEE Transactions on Communications Systems 11(3), 1963
    locator: pages 289 to 296 (the optimal bit allocation rule b_k = R + 1/2 lg of the variance over the geometric mean)
  - book: isbn:9780132119139
    title: N. S. Jayant and Peter Noll, Digital Coding of Waveforms, Prentice-Hall, 1984
    locator: the chapter on sub-band coding (the coding gain of a sub-band coder, bit allocation and the tree-structured banks)
  - book: isbn:9780130970800
    title: Martin Vetterli and Jelena Kovačević, Wavelets and Subband Coding, Prentice Hall, 1995
    locator: the chapter on signal compression and subband coding (the coding gain of orthogonal and biorthogonal banks, and the octave-band tree)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Section 10.3.3 (reverse water-filling for independent Gaussian sources)
  - paper: doi:10.1109/93.388209
    title: Davis Pan, A tutorial on MPEG/audio compression, IEEE MultiMedia 2(2), 1995
    locator: pages 60 to 74 (the 32-band polyphase filter bank of MPEG-1 audio and the allocation of bits by a psychoacoustic model)
---

Subband coding splits a signal into frequency bands with an analysis [filter bank](/filter-bank/), keeps only every $M$-th sample of each band so that the total number of samples does not change, and codes each band with its own [quantizer](/scalar-quantization/) and its own share of the bits. The decoder upsamples the bands and adds them through the synthesis bank. Crochiere, Webber and Flanagan (1976) used it for speech, with more bits in the bands where the ear notices noise. Woods and O'Neil (1986) carried it to images. For an orthonormal bank and a fixed total rate, the best split of the bits gives every band the same distortion, and the gain over coding the signal directly is the ratio of the arithmetic to the geometric mean of the band variances. The dyadic tree, which splits only the low band again and again, is the [discrete wavelet transform](/discrete-wavelet-transform/), the front end of [JPEG 2000](/jpeg-2000/).

## In plain words

Most signals put their energy in a few frequency ranges. A photo is mostly smooth areas, which are low frequencies; edges and texture, the high frequencies, are small and rare. Speech has strong low tones and weak hiss.

A subband coder separates these ranges first, like a graphic equalizer that splits music into bass, middle and treble. Each part then gets the number of bits that it deserves. A strong band gets many bits. A weak band gets few or none, because even large relative errors in it are small in absolute terms. The receiver decodes each band and adds the bands back together.

The total error is spread evenly over the bands, and the total number of bits is much smaller than for coding the raw signal at the same quality.

## When it applies

Use subband coding when the spectrum of the signal is far from flat, so that some bands carry much more power than others, and when the coder should control where the error goes in frequency, for example to hide it where the ear or eye is less sensitive. It needs a filter bank with [perfect reconstruction](/perfect-reconstruction/), so that the only error is the quantization error. For a source with a flat spectrum, such as white noise, there is nothing to gain.

**Set-up.** A critically sampled bank splits the $n$ samples of $x$ into bands $k = 1, \ldots, K$ with $n_k$ samples each and $\sum_k n_k = n$. Let $w_k = n_k / n$ be the fraction of the samples in band $k$, so $\sum_k w_k = 1$, and let $\sigma_k^2$ be the variance of the samples of band $k$. If the bank is orthonormal, the energy of the bands equals the energy of $x$, so the variance of the signal is $\sigma_x^2 = \sum_k w_k \sigma_k^2$, and the mean squared error of the decoded signal is the weighted mean of the band errors:
$$D = \sum_k w_k D_k.$$

**The bit allocation.** Band $k$ gets $b_k$ bits per sample, and the average rate is $R = \sum_k w_k b_k$. At high rate a quantizer of the same kind in every band has $D_k = c\, \sigma_k^2\, 2^{-2 b_k}$ for a constant $c$. Then
$$D = c \sum_k w_k \sigma_k^2 2^{-2 b_k} \;\ge\; c \prod_k \left(\sigma_k^2 2^{-2 b_k}\right)^{w_k} = c\, \Big(\prod_k \sigma_k^{2 w_k}\Big) 2^{-2R},$$
by the weighted inequality of the arithmetic and geometric means ([Jensen's inequality](/jensens-inequality/) for the logarithm). Equality holds exactly when all the terms $\sigma_k^2 2^{-2 b_k}$ are equal. So the optimal allocation gives every band the same distortion, which is the rule of Huang and Schultheiss (1963):
$$b_k = R + \frac{1}{2} \lg \frac{\sigma_k^2}{\prod_j \sigma_j^{2 w_j}}.$$

**The coding gain.** Coding $x$ directly with the same kind of quantizer at $R$ bits per sample gives $D_{\mathrm{PCM}} = c\, \sigma_x^2 2^{-2R}$. The ratio is
$$G_{\mathrm{SB}} = \frac{D_{\mathrm{PCM}}}{D} = \frac{\sum_k w_k \sigma_k^2}{\prod_k (\sigma_k^2)^{w_k}} \;\ge\; 1,$$
the weighted arithmetic mean over the weighted geometric mean of the band variances. It is 1 only when all the bands have the same variance. A gain $G$ saves $\frac{1}{2} \lg G$ bits per sample at the same distortion, or improves the SNR by $10 \log_{10} G$ dB at the same rate. As the bands get narrower with ideal filters, $G_{\mathrm{SB}}$ tends to the ratio of the arithmetic to the geometric mean of the [power spectral density](/power-spectral-density/), which is the largest gain that any linear coder of a Gaussian source can get at high rate.

**Negative bits.** At low rate the formula can give a weak band a negative number of bits. The correct optimum for $b_k \ge 0$ is *reverse water-filling*: pick a level $\theta$, give band $k$ the bits $\max(0, \frac{1}{2} \lg (\sigma_k^2 / \theta))$, and choose $\theta$ so that the rate is $R$. Bands with $\sigma_k^2 \le \theta$ get no bits and are decoded as 0, with distortion $\sigma_k^2$. This is also the rate distortion solution for independent Gaussian bands (Cover and Thomas, Section 10.3.3).

**Entropy-coded quantizers.** With a uniform quantizer and an ideal entropy coder in each band, $D_k \approx \Delta_k^2 / 12$ whatever the variance. Equal distortion then means *one step size $\Delta$ for every band* of an orthonormal bank, and the entropy coder spends more bits on the strong bands by itself.

**The tree.** A two-channel bank splits a band into a low half and a high half. Apply it again to some of the outputs to get more bands.

- The *dyadic* (octave) tree splits only the low band, $L$ times. It gives $L + 1$ bands with $w = 2^{-L}, 2^{-L}, 2^{-L+1}, \ldots, \frac{1}{2}$, narrow at low frequency and wide at high frequency. This suits spectra that fall with frequency, such as those of images and of most natural signals, and it is the discrete wavelet transform.
- The *full* tree splits every band, $L$ times, into $2^L$ equal bands (a wavelet packet).
- An *adaptive* tree splits a band only if the split lowers a cost, such as the estimated rate.

For images, a separable bank filters the rows and then the columns, which gives four bands per split: LL, LH, HL and HH. The dyadic tree splits LL again. Woods and O'Neil split all four bands once more, for 16 equal bands.

## The template

```pseudo id=main
SUBBAND-CODE(x, L, R)                         ▷ x: the signal, L: tree depth, R: bits per sample
L1  bands ← ANALYZE(x, L)
L2  for each band k with variance σk² and weight wk
L3      qk ← QUANTIZE(band k, Δk)              ▷ hole: Δk from the bits bk of ALLOCATE(σ², w, R)
L4      send qk with an entropy coder          ▷ hole: the band coder (PCM, DPCM, bit planes)
L5      band′k ← Δk · qk                       ▷ the decoder
L6  return SYNTHESIZE(band′)                   ▷ the inverse of ANALYZE
ANALYZE(x, L)                                  ▷ the dyadic tree
L7  for j ← 1 to L
L8      (low, highj) ← SPLIT(low)              ▷ hole: the two-channel filter bank; low starts as x
L9  return (low, highL, highL−1, …, high1)
ALLOCATE(σ², w, R)                             ▷ reverse water-filling
L10 find θ with Σk wk · max(0, ½ lg(σk² / θ)) = R    ▷ bisection on lg θ
L11 return bk = max(0, ½ lg(σk² / θ)) for every k
```

With a two-channel bank of filters of length $f$, ANALYZE and SYNTHESIZE cost $O(f n)$ for the dyadic tree, since the levels cost $n, n/2, n/4, \ldots$, and $O(f n L)$ for the full tree of depth $L$. The quantizers and entropy coders cost $O(n)$. ALLOCATE costs $O(K)$ per step of the bisection. The decoder needs the band variances or the steps, which are a few numbers of side information per band.

**The holes.** The filter bank of line L8 (Haar, the 5/3 or 9/7 wavelets, quadrature mirror filters, a cosine-modulated bank), the shape of the tree, the quantizer of line L3 and its step rule, and the band coder of line L4.

### Worked examples

**The bands of a ramp.** With the orthonormal Haar bank, low $= (a + b)/\sqrt{2}$ and high $= (a - b)/\sqrt{2}$ for each pair, the dyadic tree of depth 3 turns $x = (1, 2, \ldots, 8)$ into the bands
$$(12.728), \quad (-5.657), \quad (-2, -2), \quad (-0.707, -0.707, -0.707, -0.707).$$
The low band holds $36/\sqrt{8}$, the sum over $\sqrt 8$. The high bands are constant because a ramp has the same difference everywhere, and they get smaller toward high frequency. Their energies add up to $\sum x_i^2 = 204$.

**A first-order autoregressive source.** Let $x$ be a Gaussian AR(1) sequence with unit variance and correlation $\rho = 0.95$ between neighbours. The band variances of the Haar dyadic tree follow exactly from the autocorrelation $\rho^{|i - j|}$. One split gives $1 + \rho = 1.95$ and $1 - \rho = 0.05$, and a gain of $1/\sqrt{1 - \rho^2} = 3.20$, or 5.06 dB.

| depth $L$ | band variances, low to high | $G_{\mathrm{SB}}$ |
|---|---|---|
| 1 | 1.95, 0.05 | 5.055 dB |
| 2 | 3.756, 0.1438, 0.05 | 7.174 dB |
| 3 | 7.025, 0.4874, 0.1438, 0.05 | 7.942 dB |
| 4 | 12.41, 1.644, 0.4874, 0.1438, 0.05 | 8.182 dB |
| 5 | 19.85, 4.961, 1.644, 0.4874, 0.1438, 0.05 | 8.243 dB |
| 6 | 27.57, 12.13, 4.961, …, 0.05 | 8.254 dB |

The limit for ideal filters is $1/(1 - \rho^2) = 10.26$, or 10.11 dB. The short Haar filters leak power between bands, so their gain stops near 8.25 dB. The full tree of depth 3, with 8 equal bands, gains 7.946 dB, only 0.004 dB more than the dyadic tree with 4 bands: for this source the high bands are already nearly flat inside, and splitting them buys almost nothing.

**Bit allocation at depth 3.** The weights are $\frac18, \frac18, \frac14, \frac12$. At $R = 1$ bit per sample the rule gives $b = (3.725, 1.801, 0.920, 0.158)$, every band has distortion $0.0402\,c$, and PCM has $0.25\,c$: a gain of 6.23, the 7.94 dB of the table. At $R = 0.5$ the rule of Huang and Schultheiss gives the top band $-0.342$ bits. Reverse water-filling gives it 0 bits and gives $(2.884, 0.959, 0.079, 0)$ to the bands, for $D = 0.0895\,c$ against $0.5\,c$ for PCM.

**A complete coder.** Take 32 768 samples of the AR(1) source above (seed 1), the Haar dyadic tree of depth 3, a midtread quantizer with the same step $\Delta$ in every band, and measure the rate as the first-order entropy of the indices of each band. For $\Delta = 0.05, 0.1, 0.2$ the decoded MSE of both the subband coder and PCM is within 3% of $\Delta^2/12$, and the subband coder needs 1.339, 1.329 and 1.308 fewer bits per sample than PCM. The formula predicts $\frac{1}{2} \lg 6.23 = 1.319$ bits.

## Classic examples

- **Speech** (Crochiere, Webber and Flanagan 1976): the telephone band is split into a few sub-bands, each coded with an adaptive quantizer, and the bits are given to the bands on perceptual grounds rather than by the variance rule alone. The paper also uses *integer-band sampling*, in which a band from $m f_s$ to $(m+1) f_s$ is decimated directly, so that the aliasing moves it to baseband.
- **Images** (Woods and O'Neil 1986): a tree of separable quadrature mirror filters splits the image into 16 bands, and DPCM codes each band. Later coders replaced the equal bands by the dyadic tree of the [discrete wavelet transform](/discrete-wavelet-transform/) and the band coders by embedded [bit-plane](/bit-plane-coding/) coders, as in [SPIHT](/spiht/) and [JPEG 2000](/jpeg-2000/).
- **Audio**: MPEG-1 audio splits the signal into 32 equal bands with a polyphase filter bank and gives each band the bits that a psychoacoustic model asks for, so that the noise in each band stays below the masking threshold (Pan 1995). Layer III follows the filter bank with a [modified discrete cosine transform](/modified-discrete-cosine-transform/) in each band, a hybrid of subband and [transform coding](/transform-coding/).
- **Block transforms** as subband coders: an $N$-point orthonormal block transform, such as the [discrete cosine transform](/discrete-cosine-transform/) of JPEG, is a bank of $N$ filters of length $N$ decimated by $N$. Coefficient $k$ of every block forms band $k$, and the coding gain of transform coding is the same ratio of means.

## Variations

- **Perceptual allocation.** Weight the distortion of band $k$ by a sensitivity $s_k$ and minimize $\sum_k w_k s_k D_k$. The same argument gives equal *weighted* distortion in every band, which shapes the noise to follow the sensitivity of the ear or eye.
- **Integer allocation.** Give the bits one at a time, each to the band whose distortion falls most per bit, which for the model above is the band with the largest $\sigma_k^2 4^{-b_k}$. For bands of equal size and a convex distortion in each band, this greedy rule is optimal.
- **Biorthogonal banks.** The 5/3 and 9/7 banks of JPEG 2000 are not orthonormal. The error of band $k$ then reaches the signal multiplied by the squared norm of its synthesis filter, and the allocation must use these weights.
- **Predictive coding of the bands.** The low band of a shallow tree is still correlated, so DPCM in that band, as Woods and O'Neil did, adds gain. A deeper tree gets the same effect.
- **Integer banks** built by the [lifting scheme](/lifting-scheme/) map integers to integers, so that the finest quantizer gives lossless coding.
- **Oversampled pyramids.** The [Laplacian pyramid](/laplacian-pyramid/) is a band split with about $4/3$ times as many samples as the image. It is not critically sampled, so it has more coefficients to code, but it needs no alias cancellation.

## Pitfalls

- **Aliasing after quantization.** A perfect reconstruction bank cancels the aliasing of the decimated bands only if the bands arrive unchanged. Coarse quantization breaks the cancellation, and the alias terms become visible or audible. Filters with good stopbands keep these terms small.
- **The gain formula needs an orthonormal bank.** With other banks, the band variances do not add up to $\sigma_x^2$ and the band errors are not the signal error. Use the weights of the synthesis filters.
- **The rule needs high rate.** $D_k = c \sigma_k^2 2^{-2b_k}$ fails at a fraction of a bit per sample. Clip with reverse water-filling, and measure the real distortion of each quantizer at low rate.
- **Edges of finite signals.** A filter longer than 2 needs samples beyond the ends. Periodic extension makes a jump at the boundary, and zero padding adds samples. Symmetric extension of a symmetric filter keeps both the length and the smoothness.
- **The length must divide.** Each split halves the length, so the dyadic tree of depth $L$ needs a length that is a multiple of $2^L$, or some rule for odd lengths.
- **Side information.** The decoder needs the step or the bits of each band. For short blocks or many bands, this cost can eat the gain.

## Exercises

1. For the one-level Haar split of a unit-variance AR(1) source with correlation $\rho$, show that the band variances are $1 \pm \rho$ and that the coding gain is $1/\sqrt{1 - \rho^2}$.
2. Prove the reverse water-filling rule: minimize $\sum_k w_k \sigma_k^2 2^{-2 b_k}$ subject to $\sum_k w_k b_k = R$ and $b_k \ge 0$.
3. Take ideal filters and a source whose power spectral density is proportional to $1/|\omega|$ above some small cut-off. Show that every octave band of the dyadic tree has the same power, so that the variance per sample doubles at each level toward low frequency, and compute the coding gain of a tree of depth $L$.
4. Show that with entropy-coded uniform quantizers at high rate, a single step for all the bands of an orthonormal bank minimizes the distortion at a fixed rate. Why does this fail for the 9/7 bank?

## References
