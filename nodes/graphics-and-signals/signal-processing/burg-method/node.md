---
tag: CXSG6S
kind: algorithm
slug: burg-method
name: Burg's method
aliases:
- Burg AR estimation
area: graphics-and-signals/signal-processing
level: advanced
summary: "Fit an autoregressive model to a record stage by stage, choosing each reflection coefficient to minimize the forward plus backward prediction error; the model is always stable."
solves: [spectral-estimation]
model: real-ram
complexity:
  vars: {N: the number of samples, p: the model order}
  time: {worst: Θ(N p), average: Θ(N p), best: Θ(N p)}
  space: {extra: Θ(N)}
properties: {deterministic: true, parametric: true, stable_model: true, order_recursive: true}
history:
  year: 1967
  people: [John Parker Burg]
  note: Burg presented maximum entropy spectral analysis, with the lattice estimate of the reflection coefficients, at the 1967 meeting of the Society of Exploration Geophysicists.
prereqs: [autocorrelation, power-spectral-density, levinson-durbin-recursion]
see_also: [spectral-estimation, linear-prediction, linear-predictive-coding, periodogram, welch-method, music-algorithm, prony-method, minimum-phase]
sources:
  - paper: "John Parker Burg, Maximum entropy spectral analysis, 37th Annual International Meeting of the Society of Exploration Geophysicists, Oklahoma City, 1967; reprinted in D. G. Childers (ed.), Modern Spectrum Analysis, IEEE Press, 1978"
    locator: the whole paper (the maximum entropy spectrum and the estimate of the prediction filter from the data by forward and backward errors)
  - book: isbn:9780131139565
    title: Petre Stoica and Randolph L. Moses, Spectral Analysis of Signals, Pearson Prentice Hall, 2005
    locator: Section 3.4.1 (the Yule-Walker method), Section 3.5.1 (the Levinson-Durbin algorithm and reflection coefficients) and Section 3.9.3 (Burg's method)
  - book: isbn:9780471594314
    title: Monson H. Hayes, Statistical Digital Signal Processing and Modeling, Wiley, 1996
    locator: Chapter 6, Lattice Filters (the forward and backward errors of the lattice and the Burg algorithm) and Chapter 8, Spectrum Estimation (autoregressive spectrum estimation)
  - paper: doi:10.1109/PROC.1981.12184
    title: Steven M. Kay and Stanley L. Marple, Spectrum analysis, a modern perspective, Proceedings of the IEEE 69(11), 1981
    locator: pp. 1380 to 1419 (the AR estimators compared, with the line splitting and frequency bias of the Burg estimate)
---

Burg's method fits an autoregressive (AR) model of order $p$ to a record $x[0], \dots, x[N-1]$ and uses it as a [power spectral density](/power-spectral-density/) estimate, $\hat S(\omega) = E_p / |A_p(e^{i\omega})|^2$. It builds the prediction error filter $A_p(z)$ one order at a time, like the [Levinson-Durbin recursion](/levinson-durbin-recursion/), but it never forms an autocorrelation estimate. At each stage it chooses the reflection coefficient $k_m$ that minimizes the energy of the forward and backward prediction errors together, computed from the data. That choice always gives $|k_m| \le 1$, so the model is stable, and on short records it resolves close peaks that the [periodogram](/periodogram/) merges. It is one of the parametric answers to [spectral estimation](/spectral-estimation/).

## In plain words

Guess each sample from the few samples just before it, with fixed weights. The best weights describe the signal: their frequency response, turned upside down, is its spectrum. Burg finds the weights one at a time. At each step it adds one more weight and picks the value that makes the guessing errors smallest, guessing both forward in time and backward. Because it uses the guesses in both directions on the same data, the chosen value can never be larger than one in size. That keeps the model stable. A short record can then give sharp spectral peaks.

## The problem

Given a record of a zero-mean stationary process sampled at the rate $f_s$ and an order $p < N$, find the coefficients $a[1], \dots, a[p]$ and a noise power $E$ of an AR model $x[n] = -\sum_{i=1}^{p} a[i]\,x[n-i] + e[n]$, with $e$ white of variance $E$, and report the spectrum $E/|A(e^{i\omega})|^2$, $\omega$ in radians per sample, where $A(z) = 1 + \sum_i a[i]z^{-i}$. The [spectral estimation](/spectral-estimation/) page lists the other estimators.

## The algorithm

The forward error $f_m[t]$ predicts $x[t]$ from the $m$ samples before it; the backward error $b_m[t]$ predicts $x[t-m]$ from the $m$ samples after it. Both are defined for $m \le t \le N-1$. A bar is the complex conjugate.

```pseudo id=main
BURG(x[0 .. N − 1], p)                           ▷ 0 ≤ p < N
L1  f ← x, b ← x, E ← (1/N) Σ |x[t]|², a ← (1)   ▷ order 0
L2  for m ← 1 to p do
L3      C ← Σ_{t=m}^{N−1} f[t]·conj(b[t−1]),  G ← Σ_{t=m}^{N−1} (|f[t]|² + |b[t−1]|²)
L4      k ← −2C / G   (k ← 0 if G = 0)        ▷ |k| ≤ 1
L5      a ← (a[0], …, a[m−1], 0) + k · conj(0, a[m−1], …, a[0])   ▷ Levinson update
L6      for t ← N − 1 down to m do (f[t], b[t]) ← (f[t] + k·b[t−1], b[t−1] + conj(k)·f[t])
L7      E ← (1 − |k|²) · E
L8  return a, (k_1, …, k_p), E                   ▷ Ŝ(ω) = E / |Σ_i a[i] e^{−iωi}|²
```

Line L3 measures how the forward errors and the delayed backward errors line up, and line L4 sets the coefficient that cancels as much as possible of both. Line L5 extends the filter: entry $i$ of the new filter is $a[i] + k\,\overline{a[m-i]}$. Line L6 updates both error sequences with the lattice equations. The new values on the right side use the old $f[t]$ and $b[t-1]$; running $t$ downward keeps $b[t-1]$ unchanged until it is read, which is the same as computing all new values from a copy, as the implementation does. Line L7 updates the noise power.

## Example

Take $x[n] = 2\cos(\pi n/3)$ for $n = 0, \dots, 7$, that is $x = (2, 1, -1, -2, -1, 1, 2, 1)$, and $p = 2$. A pure tone satisfies $x[n] = x[n-1] - x[n-2]$, so the ideal filter is $A(z) = 1 - z^{-1} + z^{-2}$ with zeros at $e^{\pm i\pi/3}$. The implementation runs in exact rationals and gives:

| stage $m$ | $C$ | $G$ | $k_m$ | $a_m$ | $E_m$ |
|---|---|---|---|---|---|
| 0 | none | none | none | $(1)$ | $17/8 = 2.125$ |
| 1 | 8 | 29 | $-16/29 \approx -0.5517$ | $(1, -16/29)$ | $9945/6728 \approx 1.478$ |
| 2 | $-7542/841 \approx -8.968$ | $15192/841 \approx 18.06$ | $419/422 \approx 0.9929$ | $(1, -232/211, 419/422)$ | $29835/1424672 \approx 0.0209$ |

At stage 1 the sums run over $t = 1, \dots, 7$: $C = \sum x[t]x[t-1] = 2 - 1 + 2 + 2 - 1 + 2 + 2 = 8$ and $G = 13 + 16 = 29$ (the energy of $x[1..7]$ plus that of $x[0..6]$), so $k_1 = -16/29$. At stage 2, $k_2$ is close to $1$, as it must be for a model of a pure tone, and the error power drops by a factor of about 70. The zeros of $A_2$ are $0.5498 \pm 0.8311i$, with modulus $0.9964$ and angle $\pm 0.9864$ rad. The true frequency is $\pi/3 \approx 1.0472$. The error of $0.061$ rad is the frequency bias of the Burg estimate of a sinusoid, which depends on the phase of the tone in the record and shrinks as $N$ grows.

## Correctness

By induction on $m$, after stage $m$ the arrays hold the outputs of the filter $a_m$ and of its reversed conjugate: $f_m[t] = \sum_i a_m[i]\,x[t-i]$ and $b_m[t] = \sum_i \overline{a_m[i]}\,x[t-m+i]$. The energy $J(k)$ of the order-$m$ errors is a quadratic in $k$, $J(k) = (1+|k|^2)G + 4\operatorname{Re}(\overline{k}C)$, and line L4 is its unique minimizer. Cauchy-Schwarz and the inequality of the means give $2|C| \le G$, so $|k_m| \le 1$, with equality only when the two error sequences are proportional with a unit-modulus factor. If every $|k_m| < 1$, Rouché's theorem applied to $z^m A_m(z) = z \cdot z^{m-1}A_{m-1}(z) + k_m \cdot (\text{its reversed conjugate})$ shows that all zeros of $A_p$ are inside the unit circle, so $1/A_p$ is a stable causal filter. The full proof is below.

## Complexity

**Time.** Stage $m$ costs $N - m$ products for $C$ and $2(N - m)$ squared magnitudes for $G$ in line L3, $m$ multiplies in line L5 and $2(N - m)$ multiplies in line L6, about $5(N - m)$ in all. Summed over $m = 1, \dots, p$ this is $5Np - \frac{5}{2}p^2 + O(N + p) = \Theta(Np)$ in the real-RAM model for $p < N$. The order recursion gives all models of orders $1$ to $p$ for the same price, which is what an order selection rule needs. Evaluating the spectrum on $L$ frequencies costs one FFT of the zero-padded $a$, $O(L \log L)$.

**Space.** The two error arrays: $\Theta(N)$ numbers, plus $\Theta(p)$ for the filter.

## Properties

- **Stable by construction.** $|k_m| \le 1$ always, so the model never has poles outside the unit circle, unlike the least-squares (covariance) method. Measured: over 500 random Gaussian records, real and complex, with $3 \le N \le 40$ and random $p < N$ (seed 4601), every $|k_m|$ was strictly below 1. In exact arithmetic $|k| = 1$ happens for degenerate records, such as $x = (1, 1)$ with $p = 1$, where $k_1 = -1$.
- **Accurate on AR data.** For the AR(2) model $A(z) = 1 - 0.75z^{-1} + 0.5z^{-2}$ with unit noise and $N = 2000$, over seeds 7000 to 7099 (200 samples of burn-in), the errors of $a[1]$ and $a[2]$ had means $0.0028$ and $0.0008$, standard deviations $0.0221$ and $0.0202$, and largest sizes $0.060$ and $0.052$. The asymptotic standard deviation for this model is $\sqrt{(1 - a[2]^2)/N} = 0.0194$. The estimate of the noise power $E = 1$ had standard deviation $0.033$.
- **High resolution on short records.** The AR spectrum is a smooth rational function with no side lobes, so two tones closer than $2\pi/N$ can show as two peaks if the order is high enough.
- **Order recursive.** Stage $m$ reuses all of stage $m - 1$, and the reflection coefficients are the coefficients of a lattice filter that implements $A_p$ directly.
- **Exact for Fraction input.** Only additions, multiplications and one division per stage are used, so rational data give rational coefficients, as in the example.

## Variants and improvements

- **Yule-Walker (autocorrelation) method.** Estimate the biased [autocorrelation](/autocorrelation/) and solve the Toeplitz equations with the Levinson-Durbin recursion. It is also stable, but the implicit zero padding of the record smears the peaks, and on short records it resolves less than Burg.
- **Covariance and modified covariance methods.** Least squares over forward errors, or forward and backward errors, with all $p$ coefficients free. The modified covariance method has a smaller frequency bias than Burg and is reported not to split lines, but stability is not guaranteed and the cost is $\Theta(Np + p^2)$ with a structured solver.
- **Windowed Burg.** Weighting the sums of line L3 by a taper reduces the bias of the frequency estimates of sinusoids.
- **Order selection.** Akaike's criteria (FPE, AIC) or MDL choose $p$ from the sequence of error powers $E_m$, which the recursion gives for free.
- **Linear prediction in speech.** The same lattice, with the reflection coefficients quantized, is a coder for [linear predictive coding](/linear-predictive-coding/).

## When to use it

Use Burg's method for short records whose spectrum has a few sharp peaks or is well described by a low-order all-pole model, for example in geophysics, speech and vibration analysis, and when a stable model is required for a later filter or coder. It costs about the same as a periodogram for moderate $p$. For long records of broadband noise, the [Welch method](/welch-method/) is simpler and its variance is easy to state. For the frequencies of a few pure tones in white noise, subspace methods such as [MUSIC](/music-algorithm/) and [ESPRIT](/esprit/) are less biased.

## Pitfalls

- **Conjugating in the wrong place in line L5.** The update is $a[i] + k\,\overline{a[m-i]}$. Using $a[m-i]$ without the conjugate is correct only for real data; for complex data it breaks Lemma 1 of the proof and the errors of line L6 no longer belong to the filter.
- **Updating in place in the wrong order in line L6.** $b[t]$ needs the old $b[t-1]$. Running $t$ upward in place reads a value that was already updated. Run $t$ downward or keep a copy.
- **Too high an order.** With $p$ close to $N/2$, the model fits the noise and a single tone can show up as two close peaks (line splitting), in particular when the record holds a non-integer number of periods and the initial phase is unfavorable. Choose $p$ with an order criterion.
- **Reading the frequency of a tone off the peak.** As the example shows, the Burg estimate of a sinusoid is biased, by an amount that depends on its phase; a subspace method or a least-squares fit is better when the frequency itself is the answer.
- **Forgetting the mean.** A nonzero mean is a zero-frequency line. Subtract the sample mean before line L1.

## Implementations

## History

John Parker Burg introduced maximum entropy spectral analysis at the 1967 meeting of the Society of Exploration Geophysicists, motivated by seismic data. The maximum entropy spectrum consistent with given autocorrelation values $r[0], \dots, r[p]$ is the AR($p$) spectrum, and Burg's practical contribution was to estimate the reflection coefficients from the data, by forward and backward errors, rather than from a padded autocorrelation estimate. His 1975 Stanford thesis, with the same title, developed the theory. The method spread through geophysics, speech processing and radar in the 1970s, and the reviews of the early 1980s, among them Kay and Marple's, documented its line splitting and frequency bias.

## References
