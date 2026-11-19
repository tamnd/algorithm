---
tag: M9RGV0
kind: algorithm
slug: phase-vocoder
name: Phase vocoder
aliases:
- phase vocoder time stretching
area: natural-language-and-speech/speech-analysis-and-synthesis
level: core
summary: Time-stretch or pitch-shift audio by changing the hop of the STFT and advancing each bin's phase by its estimated instantaneous frequency.
model: real-ram
complexity:
  vars: {F: the number of analysis frames, N: the frame and FFT length}
  time: {worst: O(F N log N)}
  space: {extra: O(N)}
properties: {deterministic: true, online: true, in_place: false, exact: false}
history:
  year: 1966
  people: [James L. Flanagan, Roger M. Golden]
  note: Flanagan and Golden described the phase vocoder at Bell Labs for speech coding, as the magnitude and the phase derivative of a bank of channels. Portnoff put it on the FFT in 1976, and Laroche and Dolson added phase locking in 1999.
prereqs: [short-time-fourier-transform, fast-fourier-transform, overlap-add-method]
see_also: [psola, griffin-lim-algorithm, sample-rate-conversion, window-functions, hilbert-transform, pitch-detection, discrete-fourier-transform]
sources:
  - paper: doi:10.1002/j.1538-7305.1966.tb01706.x
    title: J. L. Flanagan and R. M. Golden, Phase Vocoder, Bell System Technical Journal 45(9), 1966, 1493 to 1509
    locator: the whole paper (the analysis into magnitude and phase derivative per channel, and the synthesis from them)
  - paper: doi:10.1109/TASSP.1976.1162810
    title: M. R. Portnoff, Implementation of the digital phase vocoder using the fast Fourier transform, IEEE Transactions on Acoustics, Speech, and Signal Processing 24(3), 1976, 243 to 248
    locator: the whole paper (the phase vocoder computed with the FFT)
  - paper: doi:10.1109/89.759041
    title: J. Laroche and M. Dolson, Improved phase vocoder time-scale modification of audio, IEEE Transactions on Speech and Audio Processing 7(3), 1999, 323 to 332
    locator: the description of the standard phase vocoder, its phasiness, and the phase locking methods
---

The phase vocoder changes the duration of a sound without changing its pitch, or the pitch without changing the duration. It takes the [short-time Fourier transform](/short-time-fourier-transform/) of the input with a hop $H_a$, keeps the magnitude of each bin, gives each bin a new phase that advances by $H_s$ times the bin's instantaneous frequency, and puts the frames back with [overlap-add](/overlap-add-method/) at a hop $H_s$. [PSOLA](/psola/) does the same jobs in the time domain, one pitch period at a time, and works better on a single voice; the phase vocoder needs no pitch marks and works on any sound.

## In plain words

Cut the sound into short, overlapping pieces and find which frequencies are in each piece. To make the sound slower, put the pieces back farther apart than they were cut. If you only move the pieces, the waves in neighboring pieces no longer line up where they overlap, and they cancel or beat. So for each frequency the method measures how far the wave turned between two input pieces, works out the exact frequency from that turn, and turns the wave by the correct, larger amount between two output pieces. The waves then line up again. The result is longer, but every tone keeps its frequency. To raise the pitch, stretch first and then play the result faster.

## The problem

Given a signal $x$ and a ratio $\alpha > 0$, produce a signal $y$ of about $\alpha$ times the duration of $x$ in which every stationary sinusoid of $x$ appears with the same frequency and amplitude. A pitch shift by a factor $\beta$ is a stretch by $\beta$ followed by [sample-rate conversion](/sample-rate-conversion/) by $\beta$. There is no single correct output for a general sound, so the requirement is exact only for sinusoids.

## The algorithm

Let $w$ be a window of length $N$, let $\omega_k = 2\pi k / N$ be the center of bin $k$, let $H_s = \text{round}(\alpha H_a)$, and let $\text{princarg}$ map an angle to $[-\pi, \pi)$ by adding a multiple of $2\pi$.

```pseudo id=main
PHASE-VOCODER-STRETCH(x, alpha, window w of length N, analysis hop Ha)
L1  X_t <- FFT(w * x[t Ha .. t Ha + N - 1]) for t = 0 .. F - 1
L2  psi <- arg X_0; the first output frame is IFFT(X_0)
L3  for t <- 1 to F - 1 do
L4      delta_k <- princarg(arg X_t[k] - arg X_{t-1}[k] - Ha omega_k) for every bin k
L5      omega'_k <- omega_k + delta_k / Ha          (the instantaneous frequency)
L6      psi_k <- psi_k + Hs omega'_k
L7      the output frame t is IFFT(|X_t[k]| e^{i psi_k})
L8  y <- sum over t of w * frame t at t Hs, divided by the sum of w^2 at t Hs
```

Lines L4 and L5 are the core. The phase of bin $k$ moves by $H_a \omega$ between two frames if the bin holds a sinusoid of frequency $\omega$. The measured phase change is only known up to a multiple of $2\pi$, so the expected part $H_a \omega_k$ is taken away and the rest is wrapped to $[-\pi, \pi)$. If the true frequency is within $\pi / H_a$ of the bin center, the wrapped rest is exactly $H_a(\omega - \omega_k)$. Line L8 is the weighted overlap-add, which divides by the sum of the squared windows.

## Example

Take $f_s = 8000$ Hz, $N = 1024$, $H_a = 256$ with the periodic Hann window, and a sine of 440 Hz with amplitude 0.5. The bins are 7.8125 Hz apart, and the largest one in each frame is $k = 56$ at 437.5 Hz, with magnitude 119.77.

- The phases of bin 56 in frames 0 and 1 are $-0.56549$ and $-0.06283$ rad.
- The expected advance is $H_a \omega_{56} = 256 \cdot 2\pi \cdot 56 / 1024 = 28\pi = 87.9646$ rad.
- The raw rest $-0.06283 + 0.56549 - 87.9646 = -87.4619$ wraps to $\delta = 0.502655$ rad.
- So $\omega' = 0.343612 + 0.502655 / 256 = 0.345575$ rad per sample, which is $0.345575 \cdot 8000 / 2\pi = 440.0000$ Hz.

The bins 55, 57 and 58, with magnitudes 35.1, 94.1 and 11.2, also give 440.0000 Hz: all the bins near a sinusoid estimate the same frequency. A stretch by $\alpha = 1.5$ has $H_s = 384$, so each output frame advances the phase of these bins by $384 \cdot 0.345575 = 132.70$ rad. The 4096 input samples give 13 frames and $12 \cdot 384 + 1024 = 5632$ output samples. Measured by the zero crossings in the middle of the signals, the input is at 440.17 Hz and the output at 440.09 Hz, with a peak of 0.515. A pitch shift by 1.25 gives 549.97 Hz.

## Correctness

These are theorems, proved in proofs/correctness.md:

- **Exact frequency for one exponential.** If $x[n] = c\, e^{i\omega n}$ and $|\omega - \omega_k| H_a < \pi$, then line L5 gives $\omega'_k = \omega$ exactly, for any window.
- **Identity.** If $H_s = H_a$, every output frame equals the analysis frame, and the output equals $x$ at every sample where the sum of the squared windows is not 0.
- **Exact stretch of one exponential.** If $x[n] = c\, e^{i\omega n}$ and the condition above holds in every bin where $X_0[k] \ne 0$, then output frame $t$ is $w[m]\, c\, e^{i\omega(t H_s + m)}$, and the overlap-add gives $y[n] = c\, e^{i\omega n}$: the same frequency and amplitude, at any length. With the periodic Hann window and $\omega$ on a bin center, this holds for every $H_a < N / 2$.

A real sinusoid is the sum of two exponentials, and their leakage into each other's bins makes the estimate only close; the 440.0000 Hz above is a measurement. For sounds with several sinusoids in one bin, or with fast changes, the method is a heuristic, and its errors are the artifacts listed under Pitfalls.

## Complexity

With $F$ analysis frames of $N$ samples, each frame needs one FFT, $N$ phase updates and one inverse FFT, so the time is $O(F N \log N)$. A streaming version keeps one previous spectrum, the phase array and an output buffer of $N$ samples, so the extra memory is $O(N)$. The code on this page keeps all the frames for clarity. For a stretch of $L$ input samples, $F \approx L / H_a$, so the cost per input sample is $O((N / H_a) \log N)$, which is $O(\log N)$ for the usual overlap of 4.

## Properties

- **No pitch marks.** Unlike PSOLA, it works on music, chords and noise, and needs no pitch detection.
- **Constant frequency resolution.** Every bin is $f_s / N$ wide. A long window resolves close partials but smears the onsets in time; a short window does the reverse.
- **Online.** Each output frame depends on two input frames, so the method can stream with a delay of one frame.
- **Not exact for real signals.** Only single exponentials are kept exactly; everything else is approximate.

## Variants and improvements

- **Phase locking.** Laroche and Dolson lock the phases of the bins around each spectral peak to the phase of the peak, which keeps the vertical coherence across bins and reduces phasiness.
- **Transient handling.** Reset the phases to the analysis phases at detected onsets, so that drum hits stay sharp.
- **Pitch shift.** Stretch by $\beta$, then resample by $\beta$; or move the bins in frequency directly and scale their phase advances.
- **Phase from magnitude.** When only magnitudes exist, as in neural speech synthesis, the [Griffin-Lim algorithm](/griffin-lim-algorithm/) finds phases that fit them by iteration.

## When to use it

Use it to change the speed of music or other polyphonic sound, and for large stretch ratios. For a single voice with small changes of pitch and duration, as in [text-to-speech](/text-to-speech/) by concatenation, PSOLA is cheaper and sounds more natural.

## Pitfalls

- **Phasiness.** Each bin gets its own phase, so the bins of one partial drift apart and the sound gets a reverberant, distant quality. This is the main artifact of the basic method.
- **Smeared transients.** An attack is spread over a whole window and repeated by the overlap.
- **Hop too large.** The estimate is exact only in the bins whose center is within $\pi / H_a$ of the frequency, that is within $N / (2 H_a)$ bins. The main lobe of the Hann window covers the bins up to 2 bins from the frequency, so all of them are inside only if $H_a < N / 4$. The usual choice $H_a = N / 4$ is at this limit, and the outer bins of the lobe can then get a wrong frequency.
- **Window sum.** Without dividing by the sum of the squared windows, the output gets an amplitude ripple at the hop rate, because for most synthesis hops this sum is not constant over time.
- **Formants in pitch shifting.** Resampling moves the spectral envelope with the pitch, so a voice shifted up by more than a few semitones sounds smaller. Keep the envelope apart, as in the [source-filter model](/source-filter-model/).

## Implementations

## History

James Flanagan and Roger Golden of Bell Labs published the phase vocoder in 1966 for speech coding: each channel of a filter bank was sent as its magnitude and its phase derivative, the instantaneous frequency, which change slowly and need fewer bits than the wave. Michael Portnoff showed in 1976 how to compute it with the FFT, which made it practical, and it became a standard tool for time stretching and pitch shifting in computer music. Jean Laroche and Mark Dolson analyzed its phasiness in 1999 and proposed phase locking around spectral peaks, which most later implementations use.

## References
