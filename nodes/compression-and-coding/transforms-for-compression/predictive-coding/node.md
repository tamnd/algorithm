---
tag: 5989T7
kind: technique
slug: predictive-coding
name: Predictive coding
aliases:
- prediction-based coding
- differential pulse-code modulation
area: compression-and-coding/transforms-for-compression
level: intro
summary: Code each sample as its difference from a prediction made from samples the decoder already has; good predictions leave small residuals that an entropy coder packs well.
prereqs: [delta-encoding, lossless-compression]
see_also: [linear-prediction, linear-predictive-coding, scalar-quantization, transform-coding, rice-coding, context-modeling, jpeg-compression, signal-decorrelation]
sources:
  - paper: "P. Elias, Predictive coding, Parts I and II, IRE Transactions on Information Theory 1(1), March 1955"
    title: Peter Elias, Predictive coding
    locator: pages 16 to 33 (both parts; page numbers from memory, not checked)
  - paper: "ITU-T Recommendation T.81 (ISO/IEC 10918-1), Digital compression and coding of continuous-tone still images, requirements and guidelines, 1992"
    title: ITU-T T.81, the JPEG standard
    locator: Annex H, Table H.1 (the predictors for lossless coding) and the rules for the first line and the first column in H.1.2.1 (section number not checked)
  - paper: doi:10.1109/83.855427
    title: Marcelo J. Weinberger, Gadiel Seroussi and Guillermo Sapiro, The LOCO-I lossless image compression algorithm, principles and standardization into JPEG-LS, IEEE Transactions on Image Processing 9(8), 2000
    locator: pages 1309 to 1324 (the median edge detector as the fixed predictor, and the context modeling of the residuals)
  - paper: "RFC 9639, Martijn van Beurden and Andrew Weaver, Free Lossless Audio Codec (FLAC), IETF, 2024"
    title: RFC 9639, FLAC
    locator: the fixed predictor subframe, orders 0 to 4, and its warm-up samples (exact section not checked)
---

Predictive coding is the technique of coding each sample of a signal as its difference from a prediction, where the prediction uses only data that the decoder has already decoded. The decoder makes the same prediction and adds the difference back. When the signal is smooth or regular, the differences, called *residuals*, are small and cluster near zero, so an entropy coder such as a [Rice code](/rice-coding/) or a [Huffman code](/huffman-coding/) needs far fewer bits for them than for the samples. With a quantizer on the residual the scheme becomes lossy, and is called differential pulse-code modulation (DPCM); the encoder must then predict from the reconstructed samples, not from the input, so that both sides stay in step. C. Chapin Cutler of Bell Labs patented DPCM in 1952, and Elias gave the information-theoretic account in "Predictive coding" (1955). It is the core of lossless JPEG, JPEG-LS, the PNG filters, FLAC and the speech coders based on [linear prediction](/linear-predictive-coding/).

## In plain words

In most sound and in most pictures, a value is close to the values next to it. So the next value is easy to guess from the ones just before it.

Instead of sending each value, send only how far it is from your guess. The receiver makes the same guess, because it has the same earlier values, and adds the difference back to get the true value.

If the guesses are good, the differences are small numbers, mostly close to zero. Small numbers that repeat a lot can be written with very few bits.

You may also round each difference to save more bits. Then the receiver gets values that are a little off. To keep these small errors from adding up, the sender must make its guesses from the rounded values that the receiver will have, not from the true ones.

## When it applies

- **Each sample is close to a function of the earlier ones.** Audio, images, sensor readings and time series are of this kind. On random data, no predictor helps.
- **The predictor uses only causal data.** For a 1-D signal, the earlier samples. For an image coded in raster order, the left neighbour $a$, the upper neighbour $b$, the upper-left neighbour $c$, and others in the rows above.
- **The decoder can repeat the prediction exactly.** The predictor is fixed, or its parameters are sent (as for the coefficients of linear prediction), or it adapts from decoded data by a rule that both sides follow. Integer arithmetic, or floating point with a fixed rounding, keeps the two sides equal.
- **A coder for small numbers follows.** The residuals are usually close to a two-sided geometric distribution, which a [Golomb code](/golomb-coding/) or Rice code after a zigzag map, or an [arithmetic coder](/arithmetic-coding/) with context modeling, codes well.

## The template

The encoder below is closed-loop: the prediction uses the reconstructed samples $\hat{x}$. With $\mathit{step} = 1$, QUANTIZE is the identity, $\hat{x} = x$, and the code is lossless. Otherwise QUANTIZE$(d, \mathit{step})$ is the integer nearest to $d / \mathit{step}$.

```pseudo id=main
PREDICTIVE-ENCODE(x[0 .. n − 1], predict, step)
L1  for t ← 0 to n − 1 do
L2      p ← predict(x̂[0 .. t − 1])                 ▷ only what the decoder has
L3      q[t] ← QUANTIZE(x[t] − p, step)
L4      x̂[t] ← p + q[t] · step                      ▷ the value the decoder will get
L5      send q[t] to the entropy coder
L6  return q
```

The decoder runs lines L2 and L4 with the same predictor, so it computes the same $p$ and the same $\hat{x}[t]$ at every step. For the reconstruction error, $x[t] - \hat{x}[t] = (x[t] - p) - q[t] \cdot \mathit{step}$, which is the error of one rounding, so $|x[t] - \hat{x}[t]| \le \mathit{step}/2$ for all $t$. The error does not build up. The cost is $n$ calls of the predictor; for the predictors below each call takes $O(1)$ time, so the whole pass is $O(n)$.

**Example, one dimension.** Take $x = 10, 12, 15, 15, 14, 20, 30, 31$ and the predictor $\hat{x}[t-1]$ (0 at the start).

- With $\mathit{step} = 1$, the residuals are $10, 2, 3, 0, -1, 6, 10, 1$. They are the deltas of [delta encoding](/delta-encoding/).
- With $\mathit{step} = 4$, closed loop, the indices are $3, 0, 1, 0, -1, 2, 3, 0$. The decoder gets $12, 12, 16, 16, 12, 20, 32, 32$, and each value is within 2 of the input.
- With $\mathit{step} = 4$ in open loop, the encoder predicts from $x[t-1]$. The decoder, which does not have $x$, gets $12, 16, 20, 20, 20, 28, 40, 40$. The error grows to 10, since each rounding error stays in all later samples.

**Example, an image.** Lossless JPEG (T.81, Table H.1) has seven predictors:

| selection | prediction |
|---|---|
| 1 | $a$ |
| 2 | $b$ |
| 3 | $c$ |
| 4 | $a + b - c$ |
| 5 | $a + ((b - c) \gg 1)$ |
| 6 | $b + ((a - c) \gg 1)$ |
| 7 | $(a + b) \gg 1$ |

The first sample of the image is predicted by $2^{P-1}$ for samples of $P$ bits (with no point transform), the rest of the first line by $a$, and the first sample of each other line by $b$. Residuals are taken modulo $2^{16}$. For the 8-bit image below, selection 4 gives these residuals (shown signed; the first is stored as $65536 - 78$):

| image | | | residuals, selection 4 | | |
|---|---|---|---|---|---|
| 50 | 52 | 54 | $-78$ | 2 | 2 |
| 51 | 53 | 90 | 1 | 0 | 35 |
| 52 | 90 | 92 | 1 | 36 | $-35$ |

At the lower right, $a = b = 90$ and $c = 53$: the plane through the neighbours predicts $127$, past the edge. The median edge detector of LOCO-I and JPEG-LS,

$$
\mathrm{MED}(a, b, c) = \begin{cases} \min(a, b) & \text{if } c \ge \max(a, b) \\ \max(a, b) & \text{if } c \le \min(a, b) \\ a + b - c & \text{otherwise,} \end{cases}
$$

predicts $90$ and leaves the residual 2. MED is the median of $a$, $b$ and $a + b - c$.

## Classic examples

- **Lossless JPEG.** The seven predictors above, chosen once for each scan, followed by Huffman or arithmetic coding of the residuals. See [JPEG compression](/jpeg-compression/).
- **JPEG-LS (LOCO-I).** The MED predictor, a bias correction learned per context, and Golomb codes with a parameter chosen per context. See [context modeling](/context-modeling/).
- **PNG filters.** Each scanline chooses one of five filters: none, $a$, $b$, $\lfloor (a + b)/2 \rfloor$, and the Paeth predictor, which picks whichever of $a$, $b$, $c$ is closest to $a + b - c$. The bytes of the residuals, modulo 256, then go to [DEFLATE](/deflate/).
- **FLAC.** Fixed polynomial predictors of orders 0 to 4, whose residuals are the $k$-th differences of the samples, or a [linear predictor](/linear-prediction/) of up to order 32 with quantized coefficients; the residuals are Rice coded.
- **Speech coding.** [Linear predictive coding](/linear-predictive-coding/) fits the coefficients for each frame with the [Levinson-Durbin recursion](/levinson-durbin-recursion/), and ADPCM coders for telephone speech adapt the step size of the quantizer.
- **Delta encoding.** The predictor "the previous value" gives [delta encoding](/delta-encoding/), used for sorted lists and time stamps.

## Variations

- **Fixed or adaptive.** A fixed predictor needs no side data. A forward-adaptive one sends parameters for each block (FLAC, LPC speech). A backward-adaptive one updates its parameters from decoded data, as in ADPCM and in the bias correction of JPEG-LS.
- **Linear or nonlinear.** Linear predictors take a weighted sum of past samples; the best weights solve the normal equations of [linear prediction](/linear-prediction/). MED and Paeth are nonlinear and switch between neighbours at edges.
- **Choice among predictors.** Lossless JPEG chooses one predictor for each scan, PNG one for each line, and some coders mix several predictions with weights.
- **Lossy, with a quantizer.** DPCM puts a [scalar quantizer](/scalar-quantization/) in the loop; the near-lossless mode of JPEG-LS bounds the error of each sample by a set value in this way.
- **Prediction of a distribution.** Context modeling predicts a probability distribution for the next symbol instead of one value, and the residual of a value predictor is often coded with such a model.

## Pitfalls

- **Open loop with a quantizer.** If the encoder predicts from the input samples, the decoder output drifts: the rounding errors add up. Always predict from what the decoder will have.
- **Overflow of the residual.** A residual of $P$-bit samples can need $P + 1$ bits. Lossless JPEG takes residuals modulo $2^{16}$, and PNG modulo 256; both are reversible since the decoder also works modulo the same number.
- **Mismatch between the two sides.** Floating-point predictors give different results on different machines unless the rounding is fixed. Standards use integer arithmetic and fixed shifts.
- **Shift of negative numbers.** Predictors 5 and 6 of T.81 shift a difference that can be negative. A shift right and a division by 2 round negative values differently, so the encoder and the decoder must use the same one.
- **Boundaries and restarts.** The first line and the first column have no full neighbourhood, and each one needs a rule that the decoder knows. In lossless JPEG the first line of each restart interval uses the same rule as the first line of the image.
- **A predictor that does not fit.** Prediction from neighbours spreads noise: on a noisy image, $a + b - c$ adds three noise terms. On data with no local correlation, the residuals can need more bits than the samples.

## Exercises

1. Show that $\mathrm{MED}(a, b, c)$ is the median of $a$, $b$ and $a + b - c$.
2. Show that the residuals of the fixed predictor of order $k$ (with the first $k$ samples sent as they are) are the $k$-th differences of the samples, and so are zero for a polynomial of degree less than $k$.
3. Prove that in closed-loop coding with a quantizer that rounds to the nearest multiple of $\mathit{step}$, $|x[t] - \hat{x}[t]| \le \mathit{step}/2$ for every $t$ and every predictor.
4. With the predictor $x[t-1]$ in open loop, show that the decoder error at time $t$ is the sum of the rounding errors at the times $0$ to $t$.
5. Give a $2 \times 2$ image on which selection 4 of lossless JPEG leaves a larger residual at the lower right than MED does, and one on which it leaves a smaller one.

## References
