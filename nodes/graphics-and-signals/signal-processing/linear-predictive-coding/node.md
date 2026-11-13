---
tag: YG23QB
kind: algorithm
slug: linear-predictive-coding
name: Linear predictive coding
aliases:
- LPC
area: graphics-and-signals/signal-processing
level: core
summary: "Fit an all-pole model to each frame of a signal: window it, compute its autocorrelation, solve the normal equations by Durbin's recursion, and resynthesize with the filter G/A(z)."
solves: [linear-prediction]
model: real-ram
complexity:
  vars: {N: the number of samples in one frame, p: the order of the predictor}
  time: {worst: O(N p + p^2)}
  space: {extra: O(p)}
properties: {deterministic: true, online: true, recursive: false, exact: false}
history:
  year: 1971
  people: [Bishnu S. Atal, Suzanne L. Hanauer, John Makhoul]
  note: "Atal and Hanauer described speech analysis and synthesis by linear prediction in 1971; Makhoul's tutorial review of 1975 fixed the autocorrelation and covariance methods as the standard forms."
prereqs: [linear-prediction, levinson-durbin-recursion]
see_also: [predictive-coding, burg-method, autocorrelation, window-functions, minimum-phase, cepstrum, pitch-detection, short-time-fourier-transform]
sources:
  - paper: doi:10.1121/1.1912679
    title: "B. S. Atal and Suzanne L. Hanauer, Speech analysis and synthesis by linear prediction of the speech wave, Journal of the Acoustical Society of America 50(2B), 1971, pages 637 to 655"
    locator: "the model of speech as the output of an all-pole filter, the predictor from previous samples, and the synthesis from the predictor, the pitch and the gain"
  - paper: doi:10.1109/PROC.1975.9792
    title: "John Makhoul, Linear prediction: A tutorial review, Proceedings of the IEEE 63(4), 1975, pages 561 to 580"
    locator: "the autocorrelation method with a window, the stability of the all-pole filter, the gain, and the choice of order"
  - book: isbn:9780131873742
    title: "John G. Proakis and Dimitris G. Manolakis, Digital Signal Processing, Principles, Algorithms, and Applications, fourth edition, Pearson Prentice Hall, 2007"
    locator: "Chapter 12 (Section 12.4, solution of the normal equations by the Levinson-Durbin algorithm, and Section 12.5, the minimum-phase property of the forward prediction-error filter)"
  - paper: "J. Durbin, The fitting of time-series models, Revue de l'Institut International de Statistique 28(3), 1960"
    locator: "pages 233 to 244, the order recursion for the Yule-Walker equations"
---

Linear predictive coding (LPC) represents each short frame of a signal by the coefficients of a [linear predictor](/linear-prediction/) of order $p$ and the power of its prediction error. It multiplies the frame by a window, computes $p + 1$ values of its [autocorrelation](/autocorrelation/), and solves the Toeplitz normal equations by Durbin's form of the [Levinson-Durbin recursion](/levinson-durbin-recursion/) in $O(p^2)$ operations. The result is an all-pole filter $G / A(z)$ with $A(z) = 1 - \sum_{k=1}^{p} a_k z^{-k}$, whose [frequency response](/frequency-response/) follows the spectral envelope of the frame. With this method the filter is always stable, so a decoder can run it on an excitation signal to rebuild the frame. Speech coders send the coefficients, the gain and a description of the excitation, which takes far fewer numbers than the samples.

## In plain words

Speech is made by a sound source, such as the buzz of the vocal cords or a hiss of air, shaped by the throat and mouth. The shaping changes slowly, so over a short piece of sound it acts like a fixed filter. LPC finds that filter for each short piece. It asks which weighted sum of the last few samples best guesses the next sample, and the best weights describe the filter. What the guess misses is the source. A coder sends the weights and a rough picture of the source instead of every sample. The receiver makes a source signal, sends it through the filter, and gets back speech that sounds close to the original. The method used here always gives a filter that does not blow up.

## The problem

The input is a frame $x[0 \ldots N-1]$ of real samples, an order $p \ge 1$, and a window $w[0 \ldots N-1]$. Let $s[n] = w[n]\, x[n]$, with $s[n] = 0$ outside $0 \le n \le N - 1$. The output is the vector $a = (a_1, \ldots, a_p)$ that minimizes the energy of the prediction error over all $n$,

$$E(a) = \sum_{n = -\infty}^{\infty} \Big(s[n] - \sum_{k=1}^{p} a_k\, s[n-k]\Big)^2,$$

together with the minimum $E_p$, the reflection coefficients $k_1, \ldots, k_p$ and the gain $G = \sqrt{E_p}$. This is the autocorrelation method of the [linear prediction](/linear-prediction/) problem, applied to one frame. A long signal is cut into frames of $N$ samples, usually 20 to 30 ms long, with a hop of $H \le N$ samples between frame starts.

## The algorithm

Lines L4 to L8 are Durbin's recursion with the sign convention of signal processing. The [Levinson-Durbin recursion](/levinson-durbin-recursion/) page writes it for $y = -a$ and $\alpha_k = -k_i$.

```pseudo id=main
LPC-ANALYZE(x, p, w)                     ▷ frame x[0..N−1], order p, window w
L1  s[n] ← w[n] · x[n] for n = 0 .. N − 1
L2  r[k] ← Σ_{n=k}^{N−1} s[n] · s[n−k] for k = 0 .. p
L3  if r[0] = 0 then return a = 0, k = 0, E = 0, G = 0       ▷ silent frame
L4  a ← empty vector; E ← r[0]
L5  for i ← 1 to p do
L6      k_i ← (r[i] − Σ_{j=1}^{i−1} a_j · r[i−j]) / E
L7      (a_1, .., a_{i−1}) ← (a_j − k_i · a_{i−j} for j = 1 .. i−1); a_i ← k_i    ▷ all at once
L8      E ← (1 − k_i²) · E
L9  G ← √E
L10 return a, k, E, G
LPC-SYNTHESIZE(a, G, e)                  ▷ excitation e[0], e[1], ...
L11 for n ← 0, 1, 2, ... do
L12     ŝ[n] ← G · e[n] + Σ_{k=1}^{p} a_k · ŝ[n−k]           ▷ ŝ[m] = 0 for m < 0
```

Line L1 applies the window, usually a Hamming or a Hann window, so that the frame fades in and out and the samples near its ends get small weight. Line L2 computes the autocorrelation of the windowed frame with zeros outside it; these are the entries of the $p \times p$ Toeplitz matrix $R = (r[|i-j|])$ and of the right side $(r[1], \ldots, r[p])$. Line L3 handles a frame that is zero after the window. In the loop of line L5, pass $i$ extends the predictor of order $i - 1$ to order $i$: line L6 computes the reflection coefficient from the part of $r[i]$ that the old predictor does not explain, line L7 corrects the old coefficients with their reverse, and line L8 reduces the error. Line L9 sets the gain so that the impulse response of $G/A(z)$ has the same autocorrelation values $r[0], \ldots, r[p]$ as the windowed frame; Makhoul calls this the autocorrelation matching property. The synthesis procedure is the recursion of the IIR filter $G/A(z)$: line L12 adds the scaled excitation to the prediction from the last $p$ outputs.

## Example

Take the frame $x = (1, 2, 1)$ with a rectangular window and $p = 2$. Line L2 gives $r = (6, 4, 1)$.

| pass $i$ | $k_i$ (line L6) | $a$ after line L7 | $E$ after line L8 |
|---|---|---|---|
| start | | ( ) | $6$ |
| 1 | $4/6 = 2/3$ | $(2/3)$ | $6 \cdot (1 - 4/9) = 10/3$ |
| 2 | $(1 - \tfrac23 \cdot 4)/(10/3) = -1/2$ | $(\tfrac23 + \tfrac12 \cdot \tfrac23,\ -\tfrac12) = (1, -\tfrac12)$ | $\tfrac{10}{3} \cdot \tfrac34 = 5/2$ |

So $A(z) = 1 - z^{-1} + \tfrac12 z^{-2}$, $E_2 = 5/2$ and $G = \sqrt{5/2} \approx 1.581$. The prediction error over the whole support is $e[n] = s[n] - s[n-1] + \tfrac12 s[n-2] = (1, 1, -\tfrac12, 0, \tfrac12)$, with energy $1 + 1 + \tfrac14 + 0 + \tfrac14 = 5/2 = E_2$. The zeros of $A$ solve $z^2 - z + \tfrac12 = 0$, so they are $z = (1 \pm i)/2$, of modulus $1/\sqrt2 \approx 0.707$: inside the unit circle, as the theorem below says. Running LPC-SYNTHESIZE with $G = 1$ on the excitation $e$ gives back $(1, 2, 1, 0, 0)$, because $1/A(z)$ undoes $A(z)$.

## Correctness

**Claim.** For a frame that is not zero after the window, LPC-ANALYZE returns the unique minimizer $a$ of $E(a)$, the minimum $E_p = E(a) > 0$ and reflection coefficients with $|k_i| < 1$; and every zero of $A(z)$ has modulus less than $1$, so the synthesis filter $G/A(z)$ is causal and stable.

**Key invariant.** After pass $i$ of the loop of line L5, the vector $a$ solves the normal equations of order $i$, $\sum_{j=1}^{i} a_j\, r[|m - j|] = r[m]$ for $m = 1, \ldots, i$, and $E = r[0] - \sum_{j} a_j\, r[j] > 0$.

The invariant holds because the Toeplitz matrix of an autocorrelation of a nonzero finite sequence is positive definite, and $E$ is the ratio of two of its leading determinants. Stability follows from optimality: if $z_0$ were a zero with $|z_0| \ge 1$, replacing the factor $1 - z_0 z^{-1}$ of $A$ by $1 - \beta z^{-1}$ with the best $\beta$ would lower the error, and the Cauchy-Schwarz inequality shows that the best $\beta$ has $|\beta| < 1$. The full proof is below.

## Complexity

Line L2 costs $\sum_{k=0}^{p} (N - k) = (p+1) N - p(p+1)/2$ multiplications. Pass $i$ of the loop costs $i - 1$ multiplications in line L6, $i - 1$ in line L7, two in line L8 and one division, so the recursion costs about $p^2$ multiplications in total. One frame thus costs $O(Np + p^2)$ operations in the [real RAM](/real-ram/), and $O(Np)$ when $p < N$, which is the usual case. With a hop of $H$ samples the analysis cost per input sample is $((p + 1) N + p^2)/H$ multiplications, about $11 \cdot 240 / 80 + 100/80 \approx 34$ for $p = 10$, $N = 240$ and $H = 80$ at 8 kHz. Synthesis costs $p + 1$ multiplications per output sample. The extra space is $O(p)$ for $r$, $a$ and $k$, plus the frame.

## Properties

- **Stable synthesis filter.** For the autocorrelation method, the zeros of $A(z)$ are inside the unit circle, so $A$ is [minimum phase](/minimum-phase/) and $1/A$ is causal and stable. The covariance method has no such guarantee.
- **Reflection coefficients of modulus below one.** $|k_i| < 1$ for every $i$. A coder can quantize the $k_i$, or functions of them, in $(-1, 1)$ and keep stability; a lattice synthesis filter uses the $k_i$ directly.
- **All orders at once.** The loop computes the predictors and errors of every order $1, \ldots, p$, and $E_0 \ge E_1 \ge \cdots \ge E_p$. The drop of $E_i$ with $i$ guides the choice of order.
- **Spectral envelope.** $G^2/|A(e^{i\omega})|^2$, with $\omega$ in radians per sample, matches the autocorrelation $r[0..p]$ of the frame, and it fits the peaks of the frame spectrum better than its valleys.
- **Exactness.** In exact arithmetic lines L1 to L8 compute rational functions of the data; the implementation gives exact results on fractions. Only the square root of line L9 is irrational. In floating point the recursion is weakly stable for positive definite matrices (see the Levinson-Durbin page), and the errors grow when $|k_i|$ is near $1$.
- **Not linear in the signal.** The coefficients depend on the frame in a nonlinear way; scaling the frame by $c$ leaves $a$ and $k$ unchanged and scales $G$ by $|c|$.

## Variants and improvements

- **Covariance method.** Minimize the error only over samples with a full past and no window. The matrix is not Toeplitz, a [Cholesky decomposition](/cholesky-decomposition/) solves it in $O(p^3)$, and the filter can be unstable.
- **[Burg method](/burg-method/).** Estimate each $k_i$ from the data by minimizing the sum of forward and backward errors of the lattice, without a window. It keeps $|k_i| \le 1$ and has better resolution on short frames.
- **Pre-emphasis.** Filter the signal by $1 - \mu z^{-1}$ with $\mu$ near $0.9$ to $0.97$ before analysis, to flatten the steep fall of speech spectra and improve the conditioning of $R$.
- **Lag window and white-noise correction.** Multiply $r[k]$ by a smooth window in $k$ and $r[0]$ by $1 + \epsilon$ for a small $\epsilon$ after line L2. This widens sharp spectral peaks a little and keeps the recursion well conditioned in floating point.
- **Line spectral frequencies.** Convert $A(z)$ into the zeros of two polynomials on the unit circle. They interpolate and quantize well, and coders send them instead of $a$ or $k$.
- **Excitation models.** The classic vocoder uses a pulse train at the pitch period for voiced sounds and white noise for unvoiced ones, with a [pitch detection](/pitch-detection/) step. Code-excited linear prediction (CELP) picks the excitation from a codebook by analysis by synthesis.
- **LPC cepstrum.** A recursion converts $a$ into the [cepstrum](/cepstrum/) of $1/A(z)$, a common feature for recognition.

## When to use it

Use LPC when you need a compact, smooth model of the short-time spectral envelope of a signal, above all speech, and when a stable all-pole synthesis filter matters, as in speech coders and synthesizers. Use it as the predictor of a lossless audio coder, where the residual is entropy coded, see [predictive coding](/predictive-coding/). For formant estimation, take $p$ about two more than the sampling rate in kHz, for example $p = 10$ at 8 kHz. Prefer the [Burg method](/burg-method/) for very short records or sharp spectral lines, and a nonparametric estimate such as the [periodogram](/periodogram/) or the [short-time Fourier transform](/short-time-fourier-transform/) when the spectrum has deep zeros, which an all-pole model fits poorly.

## Pitfalls

- **Updating the coefficients in place.** Writing line L7 as a loop $a_j \leftarrow a_j - k_i a_{i-j}$ for $j = 1, 2, \ldots$ in the same array reads values of $a_{i-j}$ that were already changed for $j > i/2$. Line L7 must use the old vector for all $j$, through a copy or by updating the pairs $(a_j, a_{i-j})$ together.
- **A silent frame.** Without line L3, a frame of zeros, or one made zero by the window, gives $E = 0$ and a division by zero in line L6. Line L3 must return the zero predictor and zero gain.
- **The sign of the predictor.** Some texts write $A(z) = 1 + \sum a_k z^{-k}$. Mixing the conventions in line L6, for example with $+\sum a_j r[i-j]$ for the predictor of line L12, gives a wrong and often unstable filter. Line L6 subtracts the old prediction because line L12 adds it.
- **No window on a cut frame.** With a rectangular window in line L1, the abrupt ends of the frame add a large error at the start and the end of the support and bias the spectrum. Line L1 must use a tapered window unless the frame is a whole, isolated signal, as in the example.
- **Ill-conditioning in floating point.** For signals with a large spectral dynamic range, $E$ in line L8 becomes small and $|k_i|$ comes near $1$, and rounding can give $|k_i| \ge 1$ and an unstable filter. Add pre-emphasis before line L1 and a white-noise correction after line L2.

## Implementations

## History

Linear prediction of time series goes back to Yule's autoregressive models of 1927, to Wiener's prediction theory, and to the recursions of Levinson in 1947 and Durbin in 1960. Its use for speech came in the late 1960s, from Itakura and Saito in Japan and from Atal and Schroeder at Bell Laboratories. Atal and Hanauer published the full analysis and synthesis system in 1971, with a predictor of 12 previous samples at a 10 kHz rate. Makhoul's tutorial of 1975 set out the autocorrelation and covariance methods, the stability result and the spectral view. The 2.4 kbit/s LPC-10 vocoder became a United States federal standard, and code-excited linear prediction, described by Schroeder and Atal in 1985, is the core of most later speech codecs.

## References
