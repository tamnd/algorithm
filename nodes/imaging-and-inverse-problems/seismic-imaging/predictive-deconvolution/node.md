---
tag: R3R43H
kind: algorithm
slug: predictive-deconvolution
name: Predictive deconvolution
aliases:
- spiking deconvolution
- gapped deconvolution
area: imaging-and-inverse-problems/seismic-imaging
level: core
summary: "Design a Wiener prediction error filter from the trace autocorrelation. With white reflectivity and a minimum-phase wavelet it compresses the wavelet and removes short-period multiples."
model: real-ram
complexity:
  vars: {n: the number of samples of the trace, p: the number of prediction taps, g: the prediction gap}
  time: {worst: O(n (p + g) + p^2), average: O(n (p + g) + p^2), best: O(n (p + g) + p^2)}
  space: {extra: O(n + p + g)}
properties: {deterministic: true, linear_in_data: false, least_squares: true, assumes: "white reflectivity, minimum-phase wavelet", output_filter_minimum_phase: "for gap 1"}
history:
  year: 1969
  people: [Kenneth L. Peacock, Sven Treitel]
  note: Robinson (1957) applied Wiener prediction to seismic traces and modeled the trace as a wavelet convolved with reflectivity. Peacock and Treitel (1969) gave predictive deconvolution with a prediction distance (the gap) and showed how the gap controls the output wavelet and the removal of multiples.
prereqs: [seismic-reflection-model, autocorrelation, levinson-durbin-recursion]
see_also: [linear-prediction, wiener-filter, minimum-phase, toeplitz-system-solving, minimum-entropy-deconvolution, surface-related-multiple-elimination, parabolic-radon-transform, cepstrum]
sources:
  - paper: doi:10.1190/1.1440003
    title: Kenneth L. Peacock and Sven Treitel, Predictive deconvolution, theory and practice, Geophysics 34(2), 1969, 155 to 169
    locator: the prediction error filter with a prediction distance, its normal equations from the autocorrelation, and the effect of the gap on the wavelet and on reverberations
  - paper: doi:10.1190/1.1438415
    title: Enders A. Robinson, Predictive decomposition of seismic traces, Geophysics 22(4), 1957, 767 to 778
    locator: the model of a trace as a wavelet convolved with an uncorrelated series, and the prediction error operator that recovers the series
  - paper: doi:10.1002/sapm1946251261
    title: Norman Levinson, The Wiener RMS (root mean square) error criterion in filter design and prediction, Journal of Mathematics and Physics 25(1-4), 1946, 261 to 278
    locator: the recursive solution of the Toeplitz normal equations of the Wiener filter
  - book: isbn:9781560800941
    title: Oz Yilmaz, Seismic Data Analysis, Society of Exploration Geophysicists, 2001, Investigations in Geophysics 10
    locator: the chapter on deconvolution (spiking and predictive deconvolution, prewhitening, the design window)
---

Predictive deconvolution sharpens a seismic trace and removes periodic multiples with one least-squares filter. It treats the trace as a signal that can be partly predicted from its past: the predictable part is the long tail of the source wavelet and the repeats of reverberations, and the part that cannot be predicted is the reflectivity of the earth. The filter predicts the trace a gap of $\alpha$ samples ahead and subtracts the prediction. With $\alpha = 1$ it is spiking deconvolution. The filter comes from the autocorrelation of the trace through Toeplitz normal equations, which the [Levinson-Durbin recursion](/levinson-durbin-recursion/) solves. It is [linear prediction](/linear-prediction/) applied to the [convolutional model of a seismic trace](/seismic-reflection-model/), a special case of the [Wiener filter](/wiener-filter/).

## In plain words

A seismic trace is the earth's list of echoes, blurred by the shape of the sound pulse. The pulse rings for a while, so each sample of the trace says something about the next few samples. The echoes of the earth come at random, so they cannot be guessed from the past. The method learns, from the trace itself, the best rule to guess each sample from the samples before it. Then it subtracts the guess. What is left is the part that no rule could guess: the sharp echoes. If the guess looks further ahead, the method keeps the start of the pulse and removes only what repeats later, such as the ringing of sound trapped in a water layer.

## The problem

Input: a trace $d_0, \ldots, d_{n-1}$; the number of taps $p$; the gap $\alpha \ge 1$; the prewhitening $\varepsilon \ge 0$; optionally a design window. Output: the prediction error filter $f$ and the output trace $e = f * d$. The filter taps $a$ minimize the energy of the prediction error
$$E(a) = \sum_t \Big(d_{t+\alpha} - \sum_{j=0}^{p-1} a_j d_{t-j}\Big)^2,$$
which leads to the normal equations $\sum_{j} a_j r_{|i-j|} = r_{\alpha+i}$, $i = 0, \ldots, p - 1$, where $r_k = \sum_t d_t d_{t+k}$. The model behind it is the convolutional model $d = w * \rho$ with a white reflectivity $\rho$ and a minimum-phase wavelet $w$. The whiteness makes the autocorrelation of the trace a multiple of the autocorrelation of the wavelet, so the trace alone tells the filter what the wavelet is, up to its phase, which the minimum-phase assumption fixes.

## The algorithm

```pseudo id=main
PREDICTIVE-DECON(d, p, α, ε, window)
L1  r_k ← Σ_t d_t d_{t+k} for k = 0 … p + α - 1, over the design window
L2  r'_0 ← (1 + ε) r_0;  r'_k ← r_k for k ≥ 1          ▷ prewhitening
L3  solve Σ_j a_j r'_|i-j| = r_{α+i}, i = 0 … p - 1, by Levinson recursion
L4  f ← (1, 0, …, 0, -a_0, …, -a_{p-1})                 ▷ α - 1 zeros after the 1
L5  e_t ← Σ_k f_k d_{t-k} for every t                    ▷ apply to the whole trace
L6  return (e, f)
```

The filter of line L4 has length $p + \alpha$. For $\alpha = 1$ it is the spiking filter, whose output is as close to white as $p$ taps allow. For a larger gap the first $\alpha$ samples of the wavelet pass unchanged and only the later, predictable part is removed. Prewhitening adds $\varepsilon r_0$ to the diagonal, as if white noise were added to the trace; it keeps the system well conditioned and limits the boost at frequencies where the trace has little energy. A value of $\varepsilon$ between 0.1 and 1 percent is common; it is a tuning choice.

## Example

**An exact case.** The wavelet $w_k = (1/2)^k$ has the autocorrelation $(4/3)(1/2)^k$. With exact fractions, the spiking filter with $p = 5$ gets the taps $a = (1/2, 0, 0, 0, 0)$, so $f = (1, -1/2, 0, \ldots)$, and $f * w = (1, 0, 0, \ldots)$: the wavelet becomes a spike. With the gap $\alpha = 3$ the taps are $(1/8, 0, 0, 0)$, and the output keeps $(1, 1/2, 1/4)$ and is zero after.

**A water-layer reverberation.** A spike under a water layer with the sea floor reflection $c = 1/2$ and the two-way water time $\tau = 6$ samples gives $d_t = (-1/2)^m$ at $t = 6m$ and zero elsewhere, an endless ringing. The autocorrelation is nonzero only at multiples of 6. With the gap $\alpha = 6$ and $p = 8$, line L3 returns $a = (-1/2, 0, \ldots, 0)$, so $f$ is 1 at lag 0 and $+1/2$ at lag 6. The output is a single spike: the filter removed all the multiples and kept the primary.

**A synthetic trace.** A reflectivity of 1500 samples has a Gaussian value with probability 0.1 and zero otherwise (seed 5). It is convolved with the decaying wavelet $0.8^k$, $k < 60$. The correlation between the trace and the reflectivity is 0.60. Spiking deconvolution with $p = 12$ and $\varepsilon = 0.1$ percent gives the filter $(1, -0.795, 0.049, -0.086, 0.022, \ldots)$, close to the ideal $(1, -0.8)$, and the correlation of the output with the reflectivity rises to 0.997. The filter is not exact because the sample autocorrelation of the reflectivity is only close to white: its lags 1 to 3 are $-0.004$, $-0.055$ and $0.046$ of lag 0. These numbers are measurements on one seed.

## Correctness

The normal equations have exactly one solution, because the Toeplitz matrix is the Gram matrix of shifted copies of a nonzero trace and so is positive definite; prewhitening adds a ridge term and keeps it so. The Levinson recursion solves the system: it grows a forward and a backward solution one order at a time, and each reflection coefficient has $|k| < 1$. From $|k| < 1$ and Rouché's theorem, the spiking filter has all its zeros outside the unit circle, so it is minimum phase and has a stable causal inverse. Under the ideal model (white reflectivity, an autoregressive minimum-phase wavelet of order at most $p$, the expected autocorrelation) the output is the reflectivity convolved with the first $\alpha$ wavelet samples, and for $\alpha = 1$ it is the reflectivity. The proofs are in proofs/correctness.md.

## Complexity

In the real-RAM model, the autocorrelation costs $O(n (p + \alpha))$, the Levinson recursion $O(p^2)$ and the filter application $O(n (p + \alpha))$. A general dense solver would cost $O(p^3)$. The autocorrelation and the convolution can use the FFT, at $O(n \log n)$ each. Extra space is $O(n + p + \alpha)$.

## Properties

- Least squares: the filter minimizes the prediction error energy on the design window (a theorem, Claim 1).
- Data adaptive and so not linear: the filter depends on the trace, and the output is not a linear function of the input.
- The spiking filter is minimum phase (a theorem, Claim 3).
- Only the amplitude spectrum of the wavelet is estimated, from the autocorrelation. The phase comes from the minimum-phase assumption, not from the data. If the wavelet is not minimum phase, the output has a phase error.
- Whiteness of the reflectivity is an assumption. Real reflectivity often has more energy at high frequencies than a white series, and the filter then removes part of the earth signal.

## Variants and improvements

- Time-variant deconvolution: design separate filters in several time gates, because the wavelet changes with time as the earth absorbs high frequencies.
- Surface-consistent deconvolution: split the filter into source, receiver, offset and midpoint terms and estimate them over the whole survey.
- Multichannel prediction: predict one trace from several, for multiples with moveout.
- [Minimum entropy deconvolution](/minimum-entropy-deconvolution/) drops the white and minimum-phase assumptions and asks for a sparse output instead.
- Homomorphic deconvolution works in the [cepstrum](/cepstrum/) domain and can handle mixed-phase wavelets.
- For multiples with long periods and moveout, [surface-related multiple elimination](/surface-related-multiple-elimination/) and the [parabolic Radon transform](/parabolic-radon-transform/) work better.

## When to use it

Use spiking deconvolution early in processing, before stacking, to compress the wavelet and widen the spectrum. Use gapped deconvolution on shallow water data where the reverberation period is short and nearly constant; on zero-offset or near-offset traces, or in the tau-p domain, where the period does not change with offset.

## Pitfalls

- With too little prewhitening, the filter boosts frequencies where the trace holds only noise, and the output is noisy.
- The design window must hold enough samples, several times the filter length, and must not hold strong coherent noise; the sample autocorrelation is then a poor estimate.
- A gap that does not match the multiple period leaves part of the multiples; a gap that is too small also shortens the primary wavelet.
- Multiples are periodic only at zero offset in flat layers. At far offsets their period changes, and a single-channel filter removes them only in part.
- A wavelet that is not minimum phase, such as the zero-phase wavelet of a processed vibroseis record, is not compressed correctly unless it is first converted to minimum phase.

## Implementations

## History

Levinson (Journal of Mathematics and Physics, volume 25, dated 1946 and often cited as 1947) gave the recursive solution of the Toeplitz equations of Wiener's least-squares prediction. Robinson (1957) modeled the trace as a wavelet convolved with an uncorrelated series and used the prediction error operator to recover that series. Peacock and Treitel (1969) made predictive deconvolution with a gap a standard tool and showed how the gap length controls the output wavelet and the attenuation of reverberations.

## References
