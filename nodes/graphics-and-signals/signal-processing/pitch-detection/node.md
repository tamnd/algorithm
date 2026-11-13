---
tag: CP8HPZ
kind: problem
slug: pitch-detection
name: Pitch detection
aliases:
- fundamental frequency estimation
area: graphics-and-signals/signal-processing
level: core
summary: "Estimate the fundamental frequency of a nearly periodic signal, frame by frame. The common failure is the octave error, a period off by a factor of two."
model: real-ram
complexity:
  vars: {W: the frame length, T: the largest lag searched}
  time: {worst: O(W T)}
prereqs: [autocorrelation, discrete-fourier-transform]
see_also: [yin-algorithm, cepstrum, short-time-fourier-transform, linear-predictive-coding, time-frequency-analysis, hidden-markov-model, viterbi-algorithm, cross-correlation]
sources:
  - paper: doi:10.1121/1.1458024
    title: Alain de Cheveigné and Hideki Kawahara, YIN, a fundamental frequency estimator for speech and music, Journal of the Acoustical Society of America 111(4), 2002, 1917 to 1930
    locator: Section II, steps 1 to 6 (from the autocorrelation to the cumulative mean normalized difference and the threshold), and the evaluation of error rates, including octave errors
  - paper: doi:10.1109/TASSP.1977.1162905
    title: Lawrence R. Rabiner, On the use of autocorrelation analysis for pitch detection, IEEE Transactions on Acoustics, Speech, and Signal Processing 25(1), 1977, 24 to 33
    locator: the autocorrelation pitch detector and the effect of formants and of center clipping (general locator)
  - paper: doi:10.1121/1.1910339
    title: A. Michael Noll, Cepstrum pitch determination, Journal of the Acoustical Society of America 41(2), 1967, 293 to 309
    locator: the cepstral peak at the pitch period (general locator)
---

Pitch detection is the problem of estimating the fundamental frequency $F_0$ of a nearly periodic signal, such as voiced speech or a played note, and of following it over time. For a signal sampled at $f_s$ Hz, finding $F_0$ is the same as finding the period $P = f_s / F_0$ in samples, the smallest lag at which the signal repeats. The usual failure is the octave error: the estimate picks a multiple $2P$ of the period, or a submultiple $P/2$, and reports half or twice the true frequency. Real signals are only nearly periodic, may have a weak or missing fundamental, and stop being periodic in noise and in unvoiced sounds, so most detectors also decide in each frame whether there is a pitch at all.

## In plain words

When you sing a note, your vocal folds open and close many times a second, and the sound repeats with that rhythm. The repetition rate is the pitch you hear. A pitch detector listens to a short piece of the sound, finds how long it takes the waveform to repeat, and turns that time into a frequency.

It sounds easy, but a waveform that repeats every step also repeats every two steps, so a careless detector can report a note one octave too low. A sound with strong overtones can look as if it repeats twice as fast, and the detector reports a note one octave too high. Good detectors have rules to prefer the shortest true repeat, and they also say when a piece of sound has no pitch.

## Definition

The input is a signal $x[n]$ at a sample rate $f_s$ Hz, a frame length $W$, and a range of frequencies $[F_{\min}, F_{\max}]$, which gives the lag range $f_s / F_{\max} \le \tau \le f_s / F_{\min}$ in samples. For each frame starting at $t$, the output is either "unvoiced" or an estimate $\hat F_0$ in Hz.

A signal is periodic with period $P$ if $x[n + P] = x[n]$ for all $n$; its fundamental period is the smallest such $P > 0$, and $F_0 = f_s / P$. For a signal that is only nearly periodic, the target is the smallest lag $P$ at which a measure of mismatch, such as the difference function

$$d_t(\tau) = \sum_{j=t}^{t+W-1} \bigl(x[j] - x[j + \tau]\bigr)^2,$$

is close to its minimum. Every multiple $kP$ is also a lag of near repetition, which is the source of octave errors. The period need not be an integer number of samples.

The error measures are the gross error rate, the fraction of voiced frames whose estimate is off by more than a fixed tolerance such as 20 percent, of which most are octave errors, the fine error of the remaining frames, and the voicing error rate.

## Variants

- **Monophonic or polyphonic.** One pitch at a time, as in speech or a solo instrument, or several, as in chords. Multiple pitch estimation is much harder, because the harmonics of different notes overlap.
- **Offline or real time.** A real-time detector, as in a tuner, has a delay of at least the frame length, which must hold two periods of the lowest pitch.
- **With or without tracking.** Frame-by-frame estimates can be smoothed over time by a dynamic program over candidate pitches, often a [hidden Markov model](/hidden-markov-model/) decoded by the [Viterbi algorithm](/viterbi-algorithm/).
- **Speech or music.** Speech pitch ranges from about 50 to 500 Hz and changes fast; musical notes span about seven octaves and are steadier.
- **Pitch versus $F_0$.** Pitch is a perception, and $F_0$ is a physical quantity. With harmonics at 400, 600 and 800 Hz and nothing at 200 Hz, listeners hear 200 Hz, the missing fundamental, and a detector should report $F_0 = 200$ Hz.

## Examples

**An exact integer period.** A random integer pattern of 20 samples, repeated, at $f_s = 8000$ Hz, has $d(20) = d(40) = 0$ for frames of $W = 40$, and $F_0 = 8000 / 20 = 400$ Hz. The neighbours of the integer lag are $\tau = 19$ and $\tau = 21$, that is 421.1 Hz and 381.0 Hz, so an integer lag alone has a resolution of about 5 percent here, and interpolation between lags is needed for finer estimates.

**An octave error.** A signal of two harmonics with period $10.5$ samples repeats exactly every 21 samples. On a frame of $W = 63$ samples, $d(21) = 0$, while $d(10) = d(11) = 6741768 > 0$ for the integer version of the signal used on the [YIN algorithm](/yin-algorithm/) page. A detector that takes the global minimum of $d$ over $\tau \ge 1$ returns 21 samples, $8000 / 21 = 381.0$ Hz at $f_s = 8000$ Hz, one octave below the true $8000 / 10.5 = 761.9$ Hz. YIN's threshold on the normalized difference picks the first deep dip instead, at lag 10, and its parabolic interpolation gives exactly $21/2$.

**The missing fundamental.** Peak picking on a spectrum of harmonics at 400, 600 and 800 Hz returns 400 Hz, an octave too high. The autocorrelation and the difference function have their first full repeat at $f_s / 200$ samples, because all three harmonics line up again after 5 ms. The [cepstrum](/cepstrum/) has its peak at the same quefrency, because the log spectrum has ripples every 200 Hz.

## Known algorithms

| Method | Idea | Cost per frame | Typical failure |
|---|---|---|---|
| [Autocorrelation](/autocorrelation/) (Rabiner 1977) | first large peak of $r(\tau)$ after lag 0 | $O(W T)$ direct, $O((W + T) \log (W + T))$ by FFT | octave errors from formants; helped by center clipping |
| Average magnitude difference | minimum of $\sum \lvert x[j] - x[j + \tau] \rvert$ | $O(W T)$ | the dip at lag 0 and at multiples |
| [YIN algorithm](/yin-algorithm/) (2002) | difference function, cumulative mean normalization, absolute threshold, interpolation | as autocorrelation | far fewer gross errors than plain autocorrelation in its evaluation |
| [Cepstrum](/cepstrum/) (Noll 1967) | peak of the cepstrum in the lag range | $O(N \log N)$ for an $N$-point FFT | weak for high voices with few harmonics in the band |
| Harmonic product or sum spectrum | multiply or add the spectrum compressed by $1, 2, 3, \ldots$ | $O(N \log N)$ | octave errors when one harmonic is weak |
| LPC residual | inverse filter by [linear predictive coding](/linear-predictive-coding/), then autocorrelation of the residual | $O(W p + W T)$ for order $p$ | errors when the model fits poorly |
| Probabilistic and trained estimators | several candidates with a probability each, or a neural network on the waveform, then tracking | larger | need data, or a model of pitch changes |

## Bounds

- **Window length.** A frame must contain at least two periods of the lowest pitch for a lag-domain method to see one full repeat: for $F_{\min} = 50$ Hz that is 40 ms. This sets a worst case delay for real-time use.
- **Lag resolution.** An integer lag $\tau$ gives the frequencies $f_s / \tau$, which are $f_s / \tau^2$ Hz apart near $\tau$; at $f_s = 8000$ Hz and $\tau = 20$ that is about 20 Hz. Interpolation reduces this; the noise then sets the limit, and for a sinusoid in white noise the Cramér-Rao bound gives the smallest variance of any unbiased frequency estimate, an expected case bound.
- **Cost.** The direct difference function or autocorrelation costs $W$ multiplications per lag, $O(W T)$ per frame, in the worst case. With the FFT, all lags cost $O((W + T) \log(W + T))$.
- **Ambiguity.** For an exactly periodic signal, every multiple of the period is also a period, so any rule that picks the best lag without a preference for small lags is wrong by an octave on such signals. No detector is free of octave errors on all inputs; the published error rates are observed on test sets.

## Reductions

- **To period estimation of a lag function.** Autocorrelation, AMDF and YIN reduce the problem to finding the right minimum or maximum of a function of the lag, computed with the [cross-correlation](/cross-correlation/) of the frame with itself.
- **To harmonic analysis.** Spectral methods reduce it to finding the spacing of a set of peaks of the [short-time Fourier transform](/short-time-fourier-transform/), which is the spacing of the ripples of the log spectrum, and so to a peak of the [cepstrum](/cepstrum/).
- **Tracking to shortest paths.** With a cost for each candidate in each frame and a cost for each jump between frames, the best pitch track is a shortest path through a layered graph, found by dynamic programming.
- **Part of time-frequency analysis.** A pitch track is a ridge curve of a [time-frequency analysis](/time-frequency-analysis/) of the signal.

## Applications

- **Speech.** Intonation and stress, tone in tonal languages, speaker recognition, emotion detection, and voice pathology.
- **Speech coding.** The long-term predictor of CELP coders and the pitch of LPC vocoders.
- **Music.** Tuners, pitch correction, transcription of melodies, query by humming, and the score following of a performance.
- **Synthesis and modification.** Changing the pitch or the duration of speech and music needs pitch marks.
- **Bioacoustics.** The calls of birds, bats and whales.

## References
