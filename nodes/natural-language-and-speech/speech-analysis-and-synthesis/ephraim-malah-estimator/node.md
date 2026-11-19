---
tag: EV1Q5W
kind: algorithm
slug: ephraim-malah-estimator
name: Ephraim-Malah estimator
aliases:
- MMSE short-time spectral amplitude estimator
- MMSE-STSA
area: natural-language-and-speech/speech-analysis-and-synthesis
level: advanced
summary: Speech enhancement by the minimum mean squared error estimate of each spectral amplitude under Gaussian models, with decision-directed SNR.
model: real-ram
complexity:
  vars: {F: the number of frames, N: the frame and FFT length}
  time: {worst: O(F N log N)}
  space: {extra: O(N)}
properties: {deterministic: true, online: true, in_place: false, exact: false}
history:
  year: 1984
  people: [Yariv Ephraim, David Malah]
  note: "Ephraim and Malah derived the MMSE estimator of the short-time spectral amplitude under Gaussian models and the decision-directed estimate of the a priori SNR in 1984, and the log-spectral version in 1985."
prereqs: [wiener-filter, short-time-fourier-transform, bayes-estimator]
see_also: [spectral-subtraction, likelihood-ratio-vad, voice-activity-detection, overlap-add-method, numerical-integration]
sources:
  - paper: doi:10.1109/TASSP.1984.1164453
    title: "Y. Ephraim and D. Malah, Speech enhancement using a minimum-mean square error short-time spectral amplitude estimator, IEEE Transactions on Acoustics, Speech, and Signal Processing 32(6), 1984, 1109 to 1121"
    locator: "the derivation of the amplitude estimator under the Gaussian model, its gain function, and the decision-directed estimate of the a priori SNR"
  - paper: doi:10.1109/TASSP.1985.1164550
    title: "Y. Ephraim and D. Malah, Speech enhancement using a minimum mean-square error log-spectral amplitude estimator, IEEE Transactions on Acoustics, Speech, and Signal Processing 33(2), 1985, 443 to 445"
    locator: the whole paper (the estimator of the log amplitude)
  - paper: doi:10.1109/89.279283
    title: "O. Cappé, Elimination of the musical noise phenomenon with the Ephraim and Malah noise suppressor, IEEE Transactions on Speech and Audio Processing 2(2), 1994, 345 to 349"
    locator: the whole paper (why the decision-directed estimate reduces musical noise)
  - book: isbn:9781466504219
    title: "Philipos C. Loizou, Speech Enhancement, Theory and Practice, second edition, CRC Press, 2013"
    locator: "Chapter 7, Sections 7.3.1 (p. 211), 7.3.3.2 (p. 218) and 7.7 (log-MMSE, p. 227), and Appendix B (p. 661)"
---

The Ephraim-Malah estimator removes stationary noise from speech. In each frame of the short-time Fourier transform it multiplies every bin by a gain that makes the amplitude of the bin the minimum mean squared error estimate of the clean amplitude, under Gaussian models of speech and noise, and it keeps the noisy phase. It belongs with the [Wiener filter](/wiener-filter/), which estimates the complex coefficient instead of the amplitude and gives the gain $\xi / (1 + \xi)$, and with [spectral subtraction](/spectral-subtraction/), which subtracts a noise power and is the simplest of the three. The [statistical model VAD](/likelihood-ratio-vad/) uses the same models to decide whether a frame is speech.

## In plain words

Noisy speech is cut into short overlapping pieces, and each piece is split into frequencies. At each frequency we know how strong the noise usually is, and we guess how strong the speech is from the previous piece. If a frequency is much louder than the noise, it is probably speech, and the method keeps most of it. If it is about as loud as the noise, it is probably noise, and the method turns it down. The exact amount follows from probability: of all possible clean values, it picks the one with the smallest average squared error. The guess of the speech strength changes slowly from piece to piece, which avoids the short random tones, called musical noise, that simpler methods leave behind.

## The problem

In one frame, a DFT bin is $Y = X + D$, where the clean coefficient $X = A e^{i\alpha}$ and the noise $D$ are independent complex Gaussians with mean 0 and variances $\lambda_x$ and $\lambda_d$. Given $Y$, $\lambda_d$ and the a priori SNR $\xi = \lambda_x / \lambda_d$, find the estimate $\hat A$ that minimizes $E[(A - \hat A)^2]$. The noise power $\lambda_d$ comes from frames without speech, and $\xi$ must be estimated as well.

## The algorithm

With the a posteriori SNR $\gamma = |Y|^2 / \lambda_d$ and $v = \xi\gamma / (1 + \xi)$, the estimate is $\hat A = G(\xi, \gamma)\, |Y|$ with

$$G(\xi, \gamma) = \frac{\sqrt{\pi}}{2} \frac{\sqrt{v}}{\gamma} e^{-v/2} \left[(1 + v) I_0\!\left(\frac{v}{2}\right) + v\, I_1\!\left(\frac{v}{2}\right)\right],$$

where $I_0$ and $I_1$ are the modified Bessel functions of the first kind. The a priori SNR comes from the decision-directed rule, which mixes the clean estimate of the previous frame with the current frame.

```pseudo id=main
EPHRAIM-MALAH(y, frames of N samples, init frames, alpha, xi_min)
L1  Y(n) <- the DFT of frame n with the periodic Hann window, hop N / 2
L2  lambda_d[k] <- the mean of |Y_k|^2 over the first init frames
L3  for each frame n and bin k: gamma <- |Y_k(n)|^2 / lambda_d[k]
L4      xi <- max(alpha A_k^2 / lambda_d[k] + (1 - alpha) max(gamma - 1, 0), xi_min)
L5      G <- G(xi, gamma)
L6      X_k(n) <- G Y_k(n); A_k <- G |Y_k(n)|
L7  y_hat <- overlap-add of the inverse DFTs of X(n)
```

The Hann window shifted by $N/2$ adds to 1, so with $G = 1$ the output equals the input. The code computes $e^{-x} I_\nu(x)$ directly, by the power series in log space for $x < 50$ and by the asymptotic series above, so that no exponential overflows.

## Example

Some values of the gain, against the Wiener gain $\xi / (1 + \xi)$:

| $\xi$ | $\gamma = 0.5$ | $\gamma = 1$ | $\gamma = 4$ | $\gamma = 25$ | Wiener |
|---|---|---|---|---|---|
| 0.1 | 0.3864 | 0.2792 | 0.1569 | 0.1017 | 0.0909 |
| 1 | 0.9937 | 0.7743 | 0.5681 | 0.5101 | 0.5000 |
| 10 | 1.4522 | 1.1912 | 0.9745 | 0.9191 | 0.9091 |

For a fixed $\xi$ the gain falls toward the Wiener gain as $\gamma$ grows. For a small $\gamma$ it is larger, and it can exceed 1: a bin weaker than the model expects is raised.

On a signal of one second at $f_s = 8000$ Hz, with 0.2 s of white noise of standard deviation 0.05 and then a 500 Hz tone of amplitude 0.1 in the same noise (random seed 3), frames of 256 samples, 10 noise frames, $\alpha = 0.98$ and $\xi_{\min} = 10^{-2.5}$ give these measurements:

- The SNR over samples 2400 to 7600 rises from 2.89 dB to 15.00 dB.
- In the noise-only part, the power falls from 0.00243 to 0.0000489, by 17 dB.
- The Wiener gain with the same decision-directed $\xi$ gives 18.89 dB and a residual noise power of 0.0000019 on this signal.

The Wiener gain wins here because a pure tone in white noise needs only strong suppression. The Ephraim-Malah gain minimizes the error of the amplitude under the Gaussian model, not the SNR, and its advantage on speech is a smaller musical noise, which is a judgment of listeners.

## Correctness

These are theorems, proved in proofs/correctness.md:

- **The gain gives the posterior mean.** Under the Gaussian model, the posterior of $A$ given $Y$ has density proportional to $a\, e^{-a^2 (1/\lambda_x + 1/\lambda_d)} I_0(2 a |Y| / \lambda_d)$, and $E[A \mid Y] = G(\xi, \gamma) |Y|$. The posterior mean minimizes the mean squared error over all functions of $Y$, so the estimate is optimal for the stated criterion.
- **The limit is the Wiener gain.** For a fixed $\xi$, $G(\xi, \gamma) = \frac{\xi}{1 + \xi} + \frac{1}{4\gamma} + O(1/\gamma^2)$ as $\gamma \to \infty$.
- **Identity.** With $G = 1$ the output equals the input, except in the first and last half frames.

The tests check the first statement against a numerical integral of the posterior, the second for $\gamma = 10^4$ and $10^6$, and the third exactly. The use of the noisy phase is also justified by Ephraim and Malah: the MMSE estimate of the complex exponential of the phase has the noisy phase. In practice $\xi$ and $\lambda_d$ are estimates and speech is not Gaussian, so on real speech the optimality is a heuristic.

## Complexity

Each frame costs one FFT, one inverse FFT and one gain per bin. The gain needs two Bessel values, a constant number of operations for each $v$ up to a fixed bound, so the time is $O(F N \log N)$ for $F$ frames. The state is the noise power and the previous clean amplitudes, $O(N)$, and the method runs online with a delay of one frame. Real systems take the gain from a table indexed by $\xi$ and $\gamma$.

## Properties

- **Soft decision.** Every bin is scaled, never set to 0, so the speech is not cut abruptly.
- **Low musical noise.** The decision-directed $\xi$ changes slowly in noise, so the gain does not jump from frame to frame. Cappé traced most of the reduction of musical noise to this smoothing.
- **Noisy phase.** Only the amplitudes change. At low SNR the phase error limits the quality.
- **Needs a noise estimate.** Like all methods of this family it fails when the noise changes faster than the estimate of $\lambda_d$.

## Variants and improvements

- **Log-spectral amplitude (log-MMSE).** Minimize $E[(\log A - \log \hat A)^2]$ instead. The gain is $\frac{\xi}{1 + \xi} \exp\left(\frac12 \int_v^\infty \frac{e^{-t}}{t}\, dt\right)$. It suppresses more noise with little more distortion, and Ephraim and Malah published it in 1985.
- **Speech presence uncertainty.** Multiply the gain by the probability that speech is present in the bin, computed from the same likelihood ratio as the [statistical model VAD](/likelihood-ratio-vad/).
- **Other priors.** Laplacian, Gamma or super-Gaussian models of the speech coefficients fit speech better and give other gain functions.
- **Better noise tracking.** Minimum statistics and MMSE noise trackers update $\lambda_d$ during speech.
- **Neural enhancement.** Networks that predict the gain or the clean spectrum now give better quality when training data exist.

## When to use it

Use it to reduce stationary or slowly changing noise in speech, for telephony, hearing aids and the front end of recognizers, when no training data are available and the delay must be small. For noise that changes fast, such as other talkers, it does little; use a trained model or several microphones.

## Pitfalls

- **Overflow of the Bessel functions.** $I_0(v/2)$ grows like $e^{v/2}$ and overflows for $v$ above about 1400. Compute $e^{-x} I_\nu(x)$ directly, as the code does.
- **No floor on the a priori SNR.** Without $\xi_{\min}$, the gain in noise goes to 0 and the residual noise sounds unnatural. A floor of about $-25$ dB is common.
- **A smoothing factor too small.** With $\alpha$ well below 0.98, $\xi$ follows the noise and the musical noise returns.
- **Speech in the noise estimate.** If the first frames contain speech, $\lambda_d$ is too large and the speech is suppressed.
- **Gains above 1.** For $\gamma < 1$ the gain can exceed 1; some systems clip it to 1.

## Implementations

## History

Yariv Ephraim and David Malah, at the Technion in Israel, published the estimator in 1984 in the IEEE Transactions on Acoustics, Speech, and Signal Processing. The same paper introduced the decision-directed estimate of the a priori SNR, which became standard in speech enhancement. Their 1985 paper gave the log-spectral version. Olivier Cappé analyzed in 1994 why the method leaves little musical noise. The Gaussian model and the decision-directed rule were later used for voice activity detection by Sohn, Kim and Sung, and they remain the baseline that neural enhancement methods are compared with.

## References
