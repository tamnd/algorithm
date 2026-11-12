---
tag: JRTS3R
kind: concept
slug: lossy-compression
name: Lossy compression
aliases:
- irreversible compression
area: compression-and-coding/transforms-for-compression
level: intro
summary: "Compression that lets the decoded data differ from the input. Rate distortion theory gives the least rate R(D) for an allowed mean distortion D."
prereqs: [lossless-compression, shannon-entropy]
see_also: [scalar-quantization, vector-quantization, transform-coding, predictive-coding, lossy-image-compression, jpeg-compression, jpeg-2000, source-coding-theorem]
sources:
  - paper: "Claude E. Shannon, Coding theorems for a discrete source with a fidelity criterion, IRE National Convention Record, Part 4, 1959"
    locator: pages 142 to 163 (the rate distortion function and the coding theorem and its converse for a memoryless source)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition
    locator: "Chapter 10: Theorem 10.2.1 (the rate distortion theorem), Sections 10.3.1 and 10.3.2 (the Bernoulli and Gaussian sources), Section 10.8 (computation by the Blahut-Arimoto algorithm)"
  - paper: doi:10.1109/TIT.1972.1054855
    title: Richard E. Blahut, Computation of channel capacity and rate-distortion functions, IEEE Transactions on Information Theory 18(4), 1972
    locator: pages 460 to 473 (the alternating iteration for R(D) with a slope parameter)
  - paper: doi:10.1109/TIT.1972.1054753
    title: Suguru Arimoto, An algorithm for computing the capacity of arbitrary discrete memoryless channels, IEEE Transactions on Information Theory 18(1), 1972
    locator: pages 14 to 20 (the same alternating method, for channel capacity)
  - paper: doi:10.1109/18.720541
    title: Robert M. Gray and David L. Neuhoff, Quantization, IEEE Transactions on Information Theory 44(6), 1998
    locator: pages 2325 to 2383 (history of quantization and its relation to rate distortion theory, including the high-rate gap of entropy-coded scalar quantizers)
  - book: isbn:9780128094747
    title: Khalid Sayood, Introduction to Data Compression, fifth edition, 2017
    locator: Chapter 8 (mathematical preliminaries for lossy coding, distortion measures and the rate distortion function)
---

Lossy compression stores data in fewer bits by allowing the decoded data to differ from the input, and it measures the difference with a *distortion measure* such as the mean squared error. For a source model, rate distortion theory (Shannon 1959) gives the least number of bits per symbol $R(D)$ that any code needs for a mean distortion of at most $D$. This is the lossy counterpart of the [source coding theorem](/source-coding-theorem/), where the bound is the [entropy](/shannon-entropy/) and the output must be exact. JPEG, MP3, AAC and every video codec are lossy, because exact coding of sampled sound and images costs far more bits than the eye or the ear can use.

## In plain words

A photo stored without loss keeps every small change in brightness, even the changes that nobody can see. Lossy compression throws away detail that matters little, and keeps what matters most. The decoder then gives back a picture that is close to the original, but not the same.

There is a trade. Fewer bits give a worse copy, and more bits give a better one. To speak about "better" you need a number that says how far the copy is from the original, for example the mean of the squared differences of the pixels.

For a source of random data with known statistics, information theory gives a curve. For each allowed error it gives the smallest number of bits per symbol that any method can reach. No method can go below the curve, and long blocks of data can come as close to it as you want.

## The idea

**Notation.** The model is a *memoryless source*: symbols $X_1, X_2, \ldots$ are independent, each with the law $p(x)$ on an alphabet $\Sigma$ of size $\sigma$. A decoder outputs symbols of a reproduction alphabet $\hat\Sigma$. A distortion measure is a function $d : \Sigma \times \hat\Sigma \to [0, \infty)$. Logarithms are base 2 and rates are in bits per source symbol, unless a line says nats.

### Distortion measures

- *Hamming distortion* on a finite alphabet: $d(x, \hat x) = 0$ if $x = \hat x$, else 1. The mean distortion is the symbol error rate.
- *Squared error* on real values: $d(x, \hat x) = (x - \hat x)^2$. For two sequences of length $n$, the *mean squared error* is $\mathrm{MSE} = \frac{1}{n} \sum_i (x_i - \hat x_i)^2$.
- *Peak signal to noise ratio* for samples with largest value $M$ (for 8-bit pixels, $M = 255$): $\mathrm{PSNR} = 10 \log_{10}(M^2 / \mathrm{MSE})$ in decibels. See [PSNR](/psnr/). A halving of the MSE adds $10 \log_{10} 2 \approx 3.01$ dB.
- *Perceptual measures* such as the [structural similarity index](/structural-similarity-index/) follow the human eye more closely than the MSE. They are treated on the page about [lossy image compression](/lossy-image-compression/).

### The rate distortion function

A block code of length $N$ and rate $R$ has an encoder $f : \Sigma^N \to \{1, \ldots, 2^{NR}\}$ and a decoder $g : \{1, \ldots, 2^{NR}\} \to \hat\Sigma^N$. Its distortion is $E\big[\frac{1}{N} \sum_{i=1}^{N} d(X_i, \hat X_i)\big]$ with $\hat X^N = g(f(X^N))$. A pair $(R, D)$ is *achievable* if for every $\epsilon > 0$ and all large enough $N$ some code of length $N$ and rate at most $R + \epsilon$ has distortion at most $D + \epsilon$. The *rate distortion function* is

$$R(D) = \min_{p(\hat x \mid x)\,:\; E[d(X, \hat X)] \le D} I(X; \hat X),$$

where the minimum is over all *test channels* $p(\hat x \mid x)$, and $I(X; \hat X) = \sum_{x, \hat x} p(x) p(\hat x \mid x) \log \frac{p(\hat x \mid x)}{q(\hat x)}$ is the mutual information, with $q(\hat x) = \sum_x p(x) p(\hat x \mid x)$ the law of the output.

**Theorem (Shannon 1959; Cover and Thomas, Theorem 10.2.1).** For a memoryless source with a finite alphabet and a bounded distortion measure, $(R, D)$ is achievable if and only if $R \ge R(D)$.

The proof of the "if" part is a random code with $2^{NR}$ codewords drawn from the output law $q$ of the best test channel, and joint typicality. The converse uses the chain rule and the convexity below. The full proof is in Cover and Thomas, Sections 10.4 to 10.6.

**$R(D)$ is non-increasing and convex.** A larger $D$ allows more test channels, so the minimum cannot grow. For convexity, let channels $P_1$ and $P_2$ reach $R(D_1)$ and $R(D_2)$, and let $P = \lambda P_1 + (1 - \lambda) P_2$ for $0 \le \lambda \le 1$. The distortion is linear in the channel, so $P$ has distortion at most $\lambda D_1 + (1 - \lambda) D_2$. For a fixed $p(x)$, $I(X; \hat X)$ is a convex function of the channel (Cover and Thomas, Theorem 2.7.4). So $R(\lambda D_1 + (1 - \lambda) D_2) \le I_P \le \lambda R(D_1) + (1 - \lambda) R(D_2)$.

### Two closed forms

**Bernoulli source, Hamming distortion.** Let $X \sim$ Bernoulli$(p)$ with $p \le 1/2$, and let $h(t) = -t \log t - (1 - t) \log (1 - t)$ be the [binary entropy function](/binary-entropy-function/). Then

$$R(D) = h(p) - h(D) \quad \text{for } 0 \le D \le p, \qquad R(D) = 0 \quad \text{for } D > p.$$

*Proof.* Lower bound: let $Z = X \oplus \hat X$, so $P(Z = 1) = E[d(X, \hat X)] \le D$. Then $I(X; \hat X) = h(p) - H(X \mid \hat X) = h(p) - H(Z \mid \hat X) \ge h(p) - H(Z) \ge h(p) - h(D)$, because conditioning does not raise entropy and $h$ is increasing on $[0, 1/2]$. Upper bound: take $\hat X \sim$ Bernoulli$(r)$ with $r = (p - D)/(1 - 2D)$, which is in $[0, 1]$ for $D \le p \le 1/2$, and $X = \hat X \oplus Z$ with $Z \sim$ Bernoulli$(D)$ independent of $\hat X$. Then $P(X = 1) = r(1 - D) + (1 - r) D = p$, the distortion is $D$, and $I(X; \hat X) = H(X) - H(Z) = h(p) - h(D)$. For $D > p$ the decoder outputs 0 always, with rate 0 and distortion $p$. $\square$

**Gaussian source, squared error.** Let $X \sim N(0, \sigma^2)$. Then

$$R(D) = \tfrac{1}{2} \log \frac{\sigma^2}{D} \quad \text{for } 0 < D \le \sigma^2, \qquad R(D) = 0 \quad \text{for } D > \sigma^2.$$

*Proof.* The theorem above is for finite alphabets. Cover and Thomas (Section 10.3.2) state it for this continuous source. Lower bound: with differential entropy $h(\cdot)$, $I(X; \hat X) = h(X) - h(X - \hat X \mid \hat X) \ge h(X) - h(X - \hat X)$. A variable with $E[(X - \hat X)^2] \le D$ has differential entropy at most $\frac{1}{2} \log (2 \pi e D)$, the value of the Gaussian. With $h(X) = \frac{1}{2} \log (2 \pi e \sigma^2)$ this gives $I \ge \frac{1}{2} \log (\sigma^2 / D)$. Upper bound: take $\hat X \sim N(0, \sigma^2 - D)$ and $X = \hat X + Z$ with $Z \sim N(0, D)$ independent; then the distortion is $D$ and $I(X; \hat X) = \frac{1}{2} \log (\sigma^2 / D)$. $\square$

Solve for $D$: $D(R) = \sigma^2 2^{-2R}$. So each extra bit per sample divides the mean squared error by 4, which raises the signal to noise ratio $10 \log_{10}(\sigma^2 / D)$ by $20 \log_{10} 2 \approx 6.02$ dB. The same "6 dB per bit" rule holds for a uniform [scalar quantizer](/scalar-quantization/) at high rate.

### Computing R(D): the Blahut-Arimoto algorithm

For most sources there is no closed form. Blahut (1972) gave an alternating minimization that computes points of the curve for a finite source. Arimoto (1972) gave the same kind of iteration for channel capacity. Fix a slope parameter $\beta > 0$ and minimize $I(X; \hat X) + \beta E[d]$ in nats. The minimum over the channel for a fixed output law $q$ is $Q(\hat x \mid x) = q(\hat x) e^{-\beta d(x, \hat x)} / Z(x)$, and the best $q$ for a fixed channel is its output law. Each half step does not raise the objective.

```pseudo id=main
BLAHUT-ARIMOTO(p, d, β)                       ▷ p: source law on Σ; d: distortion on Σ × Σ̂; β > 0
L1  q(y) ← 1 / |Σ̂| for each y in Σ̂
L2  repeat
L3      Z(x) ← Σ_y q(y) · exp(−β d(x, y)) for each x in Σ
L4      q(y) ← q(y) · Σ_x p(x) exp(−β d(x, y)) / Z(x) for each y
L5  until q changes by less than a tolerance
L6  Q(y | x) ← q(y) exp(−β d(x, y)) / Z(x); D ← Σ p(x) Q(y | x) d(x, y)
L7  return R = Σ p(x) Q(y | x) log(Q(y | x) / q(y)) and D
```

Line L4 is the two half steps in one: the channel of line L6 for the old $q$, then its output law. An iteration costs $O(\sigma |\hat\Sigma|)$ arithmetic operations. The returned pair is a point of the $R(D)$ curve where the slope $dR/dD$ in nats is $-\beta$. A sweep over $\beta$ traces the curve, and a bisection on $\beta$ finds the point for a given $D$. Cover and Thomas, Section 10.8, show that the alternating steps converge to the minimum.

## Examples

**PSNR.** Four pixels $x = (52, 55, 61, 66)$ decode as $\hat x = (54, 55, 60, 70)$. The errors are $-2, 0, 1, -4$, so $\mathrm{MSE} = (4 + 0 + 1 + 16)/4 = 5.25$ and $\mathrm{PSNR} = 10 \log_{10}(65025 / 5.25) \approx 40.93$ dB.

**A binary source.** For a Bernoulli$(0.25)$ source, lossless coding needs $h(0.25) \approx 0.8113$ bits per symbol. If one symbol in ten may be wrong ($D = 0.1$), the rate falls to $h(0.25) - h(0.1) \approx 0.8113 - 0.4690 = 0.3423$ bits per symbol. At $D = 0.25$ the rate is 0: output all zeros.

**Blahut-Arimoto on Bernoulli$(0.3)$.** With Hamming distortion, the point of slope $-\beta$ has $D = 1/(1 + e^{\beta})$ whenever that value is below $p$. The iteration gives these points, and each one agrees with $h(0.3) - h(D)$ to about $10^{-15}$:

| $\beta$ | $D$ | $R$ (bits) |
|---|---|---|
| 1 | 0.26894 | 0.04135 |
| 2 | 0.11920 | 0.35423 |
| 3 | 0.04743 | 0.60593 |
| 5 | 0.00669 | 0.82332 |

**A Gaussian source.** At $\sigma^2 = 1$, one bit per sample gives at best $D = 0.25$ (6.02 dB), two bits give $D = 0.0625$ (12.04 dB). The Blahut-Arimoto iteration on a fine grid of the Gaussian density, with squared error, returns $D = 1/(2\beta)$ and a rate within $10^{-3}$ bits of $\frac{1}{2} \log(1/D)$; the grid is the only source of the difference.

**The gap of simple quantizers.** A uniform scalar quantizer followed by an ideal entropy coder needs about $\frac{1}{2} \log \frac{\pi e}{6} \approx 0.254$ bits per sample more than $R(D)$ at high rate, for any smooth density (a result of Gish and Pierce from 1968, given in the survey of Gray and Neuhoff). [Vector quantization](/vector-quantization/) of long blocks closes this gap.

## Where it is used

- [Scalar quantization](/scalar-quantization/) and [vector quantization](/vector-quantization/) are the step that loses information; the rest of a lossy coder is lossless.
- [Transform coding](/transform-coding/) and [subband coding](/subband-coding/) first make the samples nearly independent with a transform or a [filter bank](/filter-bank/), then quantize each coefficient. The bit allocation between coefficients is the reverse water-filling solution of $R(D)$ for independent Gaussians (Cover and Thomas, Section 10.3.3).
- [Predictive coding](/predictive-coding/) quantizes the error of a prediction.
- Image codecs: [JPEG](/jpeg-compression/), [JPEG 2000](/jpeg-2000/) and [SPIHT](/spiht/), see [lossy image compression](/lossy-image-compression/). Audio codecs use the [modified discrete cosine transform](/modified-discrete-cosine-transform/).
- [Color quantization](/color-quantization/) reduces the colors of an image to a small palette, a vector quantization of the color space.
- Embedded coders such as [bit-plane coding](/bit-plane-coding/) give one bit stream that a decoder can cut at any length, which yields a whole range of points on the rate distortion trade.

## References
