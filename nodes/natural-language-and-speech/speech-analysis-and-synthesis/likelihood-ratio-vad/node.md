---
tag: 4HXQ9X
kind: algorithm
slug: likelihood-ratio-vad
name: Statistical model voice activity detection
aliases:
- Sohn VAD
- likelihood ratio VAD
area: natural-language-and-speech/speech-analysis-and-synthesis
level: advanced
summary: Decide speech or noise per frame by a likelihood ratio test of Gaussian models of the spectral bins, smoothed by an HMM hangover.
solves: [voice-activity-detection]
model: real-ram
complexity:
  vars: {F: the number of frames, N: the frame and FFT length}
  time: {worst: O(F N log N)}
  space: {extra: O(N)}
properties: {deterministic: true, online: true, in_place: false, exact: false}
history:
  year: 1999
  people: [Jongseo Sohn, Nam Soo Kim, Wonyong Sung]
  note: Sohn, Kim and Sung modeled the DFT coefficients of noise and of speech plus noise as complex Gaussians, estimated the a priori SNR by the decision-directed rule of Ephraim and Malah, and smoothed the decisions with a two-state Markov model.
prereqs: [likelihood-ratio-test, hidden-markov-model, short-time-fourier-transform]
see_also: [rabiner-sambur-endpoint-detection, ephraim-malah-estimator, neyman-pearson-lemma, forward-algorithm, spectral-subtraction, wiener-filter]
sources:
  - paper: doi:10.1109/97.736233
    title: Jongseo Sohn, Nam Soo Kim and Wonyong Sung, A statistical model-based voice activity detection, IEEE Signal Processing Letters 6(1), 1999, 1 to 3
    locator: the Gaussian models of the DFT coefficients, the likelihood ratio of each bin, the decision-directed estimate of the a priori SNR and the HMM-based hang-over scheme
  - book: isbn:9781466504219
    title: Philipos C. Loizou, Speech Enhancement, Theory and Practice, second edition, CRC Press, 2013
    locator: "Section 9.4.3.1 (likelihood ratio approach), p. 406"
---

The statistical model VAD of Sohn, Kim and Sung decides for each frame whether it contains speech by a [likelihood ratio test](/likelihood-ratio-test/) between two Gaussian models of its DFT coefficients, noise alone and speech plus noise, and then smooths the decisions with a two-state [hidden Markov model](/hidden-markov-model/). It is one solution of [voice activity detection](/voice-activity-detection/). The older [Rabiner-Sambur endpoint detector](/rabiner-sambur-endpoint-detection/) uses thresholds on energy and zero crossings instead, and finds only the start and end of one word; this method labels every frame and uses the same noise model as the [Ephraim-Malah estimator](/ephraim-malah-estimator/).

## In plain words

The method first listens to a short stretch of noise and learns how loud the noise is at each frequency. For every new frame, it asks two questions at each frequency: how likely is this frame if it is only noise, and how likely is it if speech is added. The ratio of the two answers says which story fits better. The ratios of all frequencies are multiplied, so a frame wins the "speech" vote only when many frequencies agree. Speech comes in runs of frames, not in single frames, so a small model of switching between "speech" and "noise" carries the belief from one frame to the next. This stops short gaps inside words from being cut.

## The problem

Given a signal cut into frames and a stretch of noise at the start, label each frame 1 for speech and 0 for noise. Each frame has DFT coefficients $X_k$, $k = 0, \dots, K - 1$. The two hypotheses are

$$H_0: X_k = N_k, \qquad H_1: X_k = S_k + N_k,$$

with $N_k$ and $S_k$ independent complex Gaussians of variances $\lambda_k$ and $\lambda_k \xi_k$, where $\lambda_k$ is the noise power and $\xi_k$ the a priori signal-to-noise ratio of bin $k$. The model treats the bins as independent.

## The algorithm

Under the model, $p(X_k \mid H_0) = \frac{1}{\pi \lambda_k} e^{-|X_k|^2 / \lambda_k}$ and $p(X_k \mid H_1) = \frac{1}{\pi \lambda_k (1 + \xi_k)} e^{-|X_k|^2 / (\lambda_k (1 + \xi_k))}$. With the a posteriori SNR $\gamma_k = |X_k|^2 / \lambda_k$, the ratio of one bin is

$$\Lambda_k = \frac{p(X_k \mid H_1)}{p(X_k \mid H_0)} = \frac{1}{1 + \xi_k} \exp\left(\frac{\gamma_k \xi_k}{1 + \xi_k}\right).$$

The noise power comes from the first frames, which must be noise. The a priori SNR is unknown and comes from the decision-directed rule $\xi_k = \max(\alpha \hat A_k^2 / \lambda_k + (1 - \alpha) \max(\gamma_k - 1, 0), \xi_{\min})$, where $\hat A_k^2$ is the estimated clean power of the previous frame. Two states, 0 for noise and 1 for speech, with $a_{01}$ the chance of a switch from noise to speech and $a_{10}$ the reverse, give the smoothed statistic $G(n)$.

```pseudo id=main
SOHN-VAD(x, frames of N samples, init frames, alpha, xi_min, a01, a10, threshold eta)
L1  X(n) <- the DFT of the windowed frame n, for every n
L2  lambda_k <- the mean of |X_k|^2 over the first init frames
L3  for each frame n: gamma_k <- |X_k(n)|^2 / lambda_k
L4      xi_k <- max(alpha A_k^2 / lambda_k + (1 - alpha) max(gamma_k - 1, 0), xi_min)
L5      log Lambda(n) <- sum over k of gamma_k xi_k / (1 + xi_k) - log(1 + xi_k)
L6      log G(n) <- log Lambda(n) + log(a01 + a11 G(n - 1)) - log(a00 + a10 G(n - 1))
L7      speech(n) <- [log G(n) > log eta]
L8      A_k^2 <- (xi_k / (1 + xi_k))^2 |X_k(n)|^2; if not speech(n), move lambda_k toward |X_k(n)|^2
```

Line L6 starts from the stationary odds $G(0) = a_{01} / a_{10}$. The code takes $\hat A_k^2$ from the Wiener gain $\xi_k / (1 + \xi_k)$; the amplitude of the [Ephraim-Malah estimator](/ephraim-malah-estimator/) is a common alternative. The noise power is updated with a factor 0.98 in the frames judged noise. All the sums are in log space, because the product over 129 bins easily overflows.

## Example

Take $f_s = 8000$ Hz, white Gaussian noise with standard deviation 0.01 for one second, and a 500 Hz tone of amplitude 0.01 from sample 2800 to sample 5200. The tone has half the power of the noise, an SNR of $-3$ dB over the whole band. Frames of 256 samples with a hop of 128 and the Hamming window give 61 frames and 129 bins. The parameters are $\alpha = 0.98$, $\xi_{\min} = 10^{-2.5}$, 10 noise frames at the start, $a_{01} = 0.2$, $a_{10} = 0.1$ and $\log \eta = 10$ (random seed 7).

| frame | start | $\log \Lambda(n)$ | $\log G(n)$ | decision |
|---|---|---|---|---|
| 19 | 2432 | 1.92 | 3.84 | 0 |
| 21 | 2688 | 5.34 | 7.28 | 0 |
| 22 | 2816 | 17.82 | 20.02 | 1 |
| 23 | 2944 | 30.33 | 32.53 | 1 |
| 39 | 4992 | 48.72 | 50.92 | 1 |
| 40 | 5120 | 0.41 | 2.61 | 0 |
| 42 | 5376 | -0.42 | 1.77 | 0 |

The decisions are frames 22 to 39, all inside the tone. Frames 20, 21 and 40 hold the tone for only part of their length and are labeled noise. The tone lies in a few bins, so it is found even though its total power is below the noise. In frame 42 the frame alone favors noise ($\log \Lambda < 0$), and the memory of the previous speech frames raises $\log G$ to 1.77, still below the threshold. These values are measurements of this run.

## Correctness

These are theorems, proved in proofs/correctness.md:

- **The bin ratio.** Under the two Gaussian models, $\log \Lambda_k = \gamma_k \xi_k / (1 + \xi_k) - \log(1 + \xi_k)$, and it increases with $\gamma_k$ for $\xi_k > 0$. So for known $\lambda_k$ and $\xi_k$, the test of line L7 without smoothing is the most powerful test of its size, by the [Neyman-Pearson lemma](/neyman-pearson-lemma/).
- **The smoothing is a forward recursion.** If the states form a Markov chain with transitions $a_{ij}$, started from its stationary law, and each frame depends only on its own state, then $G(n)$ of line L6 equals the posterior odds $P(q_n = 1 \mid X(1..n)) / P(q_n = 0 \mid X(1..n))$. This is the ratio of the two variables of the [forward algorithm](/forward-algorithm/).
- **No smoothing as a special case.** With $a_{01} = a_{10} = 1/2$, $G(n) = \Lambda(n)$.

The models are approximations: speech bins are not Gaussian, neighbor bins are correlated by the window, and $\xi_k$ is an estimate. The decision-directed estimate grows with the current $\gamma_k$, so even pure noise gives $\log \Lambda(n) > 0$ on average: in 5 runs of pure noise with these settings, every frame had $\log \Lambda(n)$ between 0.5 and 6.9. This is why the threshold $\log \eta = 10$ is tuned, not the value 0 that the posterior odds would suggest. That the method is robust at low SNR is a measurement, reported by Sohn, Kim and Sung against the G.729 Annex B VAD.

## Complexity

Each frame needs one FFT of $N$ points and $O(N)$ work for the ratios, the decision-directed rule and the noise update, so the time is $O(F N \log N)$ for $F$ frames. The state is the noise power, the previous clean power and $G$, so the extra memory is $O(N)$, and the method runs online with a delay of one frame.

## Properties

- **Adapts to the noise.** The noise power is updated in frames judged noise, so slowly changing noise is followed.
- **Uses the spectrum.** A tone or a formant that stands above the noise in a few bins is found even when the total energy barely changes, which energy thresholds miss.
- **Calibrated in principle.** $G(n)$ is a posterior odds under the model, so the threshold has a meaning. In practice the model errors shift it, as above.
- **Hang-over by a model.** The HMM replaces fixed rules of the form "keep speech for 5 more frames".

## Variants and improvements

- **Geometric mean.** Compare the mean $\frac{1}{K} \sum_k \log \Lambda_k$ with a threshold, which makes the threshold independent of the number of bins.
- **Other distributions.** Laplacian or Gamma models of the speech coefficients fit speech better than the Gaussian.
- **Better noise tracking.** Minimum statistics or MMSE noise trackers update the noise power during speech as well.
- **Multiple observations.** Use the ratios of several past and future frames in one test, at the cost of delay.
- **Learned detectors.** Neural VADs, trained on labeled speech, now reach lower error rates in hard noise; this method remains a light, training-free baseline.

## When to use it

Use it as a front end of speech coding, of enhancement with [spectral subtraction](/spectral-subtraction/) or a [Wiener filter](/wiener-filter/), and of recognition, when the noise is stationary or changes slowly and the start of the signal is noise. For clean, isolated words an energy and zero-crossing rule is simpler. For music, babble or other speech-like noise, a trained detector works better.

## Pitfalls

- **Speech at the start.** If the first frames contain speech, the noise power is too high and quiet speech is missed for a long time.
- **Noise power absorbing speech.** A false "noise" decision during long speech updates the noise power toward the speech and makes later misses more likely.
- **Threshold and bin count.** The sum over bins grows with the frame length, so the threshold must change with it, or use the geometric mean.
- **Floor of the SNR.** Without $\xi_{\min}$, $\xi_k$ can be 0, and then $\Lambda_k = 1$ for every input: the bin stops voting.
- **Overflow.** $\Lambda(n)$ for a loud frame is far beyond the range of floating point. Work with $\log \Lambda$ and $\log G$.

## Implementations

## History

Before 1999, VADs for speech coding, such as the one of the G.729 Annex B standard, combined thresholds on energy, zero crossings and spectral features. Jongseo Sohn, Nam Soo Kim and Wonyong Sung of Seoul National University proposed in 1999 to treat the decision as a likelihood ratio test of Gaussian models of the DFT coefficients, the models that Ephraim and Malah had used for speech enhancement in 1984, with the decision-directed estimate of the a priori SNR and a hang-over based on a hidden Markov model. The method became a standard baseline; MATLAB's voiceActivityDetector, for example, follows it, with switch probabilities of 0.2 and 0.1 by default.

## References
