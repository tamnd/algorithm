---
tag: 6E4ZBZ
kind: problem
slug: formant-estimation
name: Formant estimation
aliases:
- formant tracking
area: natural-language-and-speech/speech-analysis-and-synthesis
level: core
summary: Find the resonance frequencies of the vocal tract over time, often as the angles of the roots of an LPC polynomial.
prereqs: [linear-predictive-coding, source-filter-model, polynomial-root-finding]
see_also: [formant-synthesis, levinson-durbin-recursion, cepstrum, companion-matrix-method, durand-kerner-method, pitch-detection, dag-dynamic-programming, kalman-filter]
sources:
  - paper: doi:10.1109/TASSP.1974.1162559
    title: Stanley S. McCandless, An algorithm for automatic formant extraction using linear prediction spectra, IEEE Transactions on Acoustics, Speech, and Signal Processing 22(2), 1974, 135 to 141
    locator: the formant candidates from the peaks of the LPC spectrum and the use of continuity between frames
  - book: isbn:9780132136037
    title: Lawrence R. Rabiner and Ronald W. Schafer, Digital Processing of Speech Signals, Prentice-Hall, 1978
    locator: Chapter 8 (linear predictive coding of speech, including formant analysis from the predictor polynomial) and Chapter 7 (homomorphic speech processing, formants from the smoothed spectrum)
---

Formant estimation is the problem of finding the formants of speech, the resonance frequencies and bandwidths of the vocal tract, in each short frame, and formant tracking adds the task of linking them across frames into smooth tracks $F_1(t), F_2(t), \ldots$. The usual method fits an all-pole model by [linear predictive coding](/linear-predictive-coding/) and reads the formants from the roots of its polynomial, which turns the problem into [polynomial root finding](/polynomial-root-finding/). It is the inverse of [formant synthesis](/formant-synthesis/), which makes speech from given formants, and it is a different task from [pitch detection](/pitch-detection/): the pitch is a property of the source, the formants are properties of the filter in the [source-filter model](/source-filter-model/).

## In plain words

Your mouth and throat are a tube, and a tube makes some frequencies louder than others. These loud regions are the formants. When you change a vowel, from "ee" to "ah", you change the shape of the tube and the formants move. The first two formants are enough to tell most vowels apart. A formant estimator looks at a short piece of a recording, about 25 milliseconds, and says where these loud regions are and how wide they are. A tracker does this every few milliseconds and joins the answers into lines. The hard parts are telling the formants apart from the harmonics of the voice, finding two formants that are close together, and not losing a weak formant.

## Definition

**Input.** A speech signal $x$ sampled at $f_s$, cut into frames $x_1, \ldots, x_T$ (often 20 to 30 ms, every 5 to 10 ms), and a number $K$ of formants to report (often 3 or 4).

**Model.** In a voiced frame without nasal coupling, the vocal tract acts as an all-pole filter,

$$V(z) = \frac{G}{\prod_{k} (1 - z_k z^{-1})(1 - \bar z_k z^{-1})}, \qquad z_k = r_k e^{i\theta_k},\ 0 < r_k < 1,$$

excited by a periodic source. Each pole pair is a formant with frequency and bandwidth

$$F_k = \frac{\theta_k f_s}{2\pi}, \qquad B_k = -\frac{f_s}{\pi} \ln r_k .$$

**Output.** For each frame $t$, the values $(F_1(t), B_1(t)), \ldots, (F_K(t), B_K(t))$ with $F_1 < F_2 < \cdots$, the formants of the vocal tract, or no value for frames without a clear resonance structure, such as silence.

**Measure.** Errors are measured against hand-labeled tracks or against synthetic speech with known formants, as the mean absolute error in Hz per formant. No exact answer exists for real speech, since the all-pole model is an approximation.

## Variants

- **Frame estimation.** Each frame alone, giving candidate resonances.
- **Tracking.** Assign the candidates to $F_1, F_2, F_3$ over time with continuity, usually by [dynamic programming](/dag-dynamic-programming/) or a [Kalman filter](/kalman-filter/).
- **With antiresonances.** For nasals and some consonants the tract has zeros as well as poles; a pole-zero model is then needed.
- **Formants of singing.** The high pitch of sopranos samples the spectral envelope at widely spaced harmonics, which makes the formants hard to see.

## Examples

**One pole pair.** The polynomial $1 - 1.8665948 z^{-1} + 0.9630027 z^{-2}$ has the roots $z = 0.9332974 \pm 0.3032467\, i$. Their modulus is $r = 0.981327$ and their angle is $\theta = 0.314159$ rad. At $f_s = 10000$ Hz this gives $F = 0.314159 \cdot 10000 / 2\pi = 500.0$ Hz and $B = -(10000/\pi) \ln 0.981327 = 60.0$ Hz. This is the resonator of the example on the [formant synthesis](/formant-synthesis/) page, so estimation recovers what synthesis put in.

**A synthetic vowel.** Pass a 100 Hz pulse train at $f_s = 10000$ Hz through two resonances, (500 Hz, 60 Hz) and (1500 Hz, 100 Hz), so the true $A(z)$ is

$$1 - 3.005808 z^{-1} + 4.028553 z^{-2} - 2.849987 z^{-3} + 0.904357 z^{-4}.$$

Take 400 samples from sample 1000, apply a Hamming window, and fit LPC of order 4 by the autocorrelation method and the [Levinson-Durbin recursion](/levinson-durbin-recursion/). The fitted polynomial is $1 - 3.016608 z^{-1} + 4.056667 z^{-2} - 2.880564 z^{-3} + 0.918318 z^{-4}$, and its roots give

| | true | estimated |
|---|---|---|
| $F_1$, $B_1$ | 500, 60 | 500.3, 44.0 |
| $F_2$, $B_2$ | 1500, 100 | 1501.5, 91.6 |

The frequencies are within 2 Hz, but the bandwidths come out too small; the window and the harmonic source bias them. With order 10 on the same frame, the two formants are again found (500.1 Hz with $B$ = 42.5 Hz and 1500.1 Hz with $B$ = 89.7 Hz), together with three extra root pairs at 813, 2467 and 4202 Hz whose bandwidths exceed 3600 Hz. A bandwidth limit removes them.

**A non-example.** In a nasal such as /m/, the closed mouth adds antiresonances. An all-pole fit then places poles to imitate the dips, and the roots no longer match the resonances of the tract.

## Known algorithms

- **LPC roots.** Fit LPC of order about $f_s / 1000 + 2$, find the roots of $A(z)$ with a [companion matrix](/companion-matrix-method/) eigenvalue solver or the [Durand-Kerner method](/durand-kerner-method/), keep the roots with positive angle and a bandwidth under a limit, and sort them by frequency. This is the most common method; the order rule is a heuristic.
- **LPC spectrum peaks.** Evaluate $1/|A(e^{i\omega})|$ on a grid and pick the peaks, which avoids root finding but can merge close formants. McCandless (1974) used peaks of the LPC spectrum with rules for continuity between frames.
- **Cepstral smoothing.** Keep the low quefrencies of the [cepstrum](/cepstrum/) to get a smoothed spectrum without the harmonics, and pick its peaks.
- **Tracking by dynamic programming.** Score each assignment of candidates to $F_1, F_2, F_3$ by bandwidth and by the change from the last frame, and find the best sequence, as for the candidates of the [RAPT](/rapt-pitch-tracker/) pitch tracker.
- **Kalman and learned trackers.** State space models smooth the tracks, and neural networks trained on labeled data predict formants directly.

## Bounds

- **At most $p/2$ formants from order $p$.** A real polynomial of degree $p$ has at most $p/2$ complex-conjugate root pairs, so LPC of order $p$ can show at most $\lfloor p/2 \rfloor$ resonances. This is a theorem.
- **Resolution.** In a frame of $N$ samples the spectral resolution is about $f_s / N$ Hz, so two formants closer than that are hard to separate with spectral peak picking. Parametric fits do better, but not much better when noise is present. This is a heuristic.
- **Sampling by harmonics.** A voiced spectrum has values only at multiples of $F_0$. With $F_0 = 300$ Hz, a formant at 500 Hz lies between the harmonics at 300 and 600 Hz, and the estimates are pulled toward the harmonics. This bias grows with $F_0$ and is a known measured effect.
- **Cost.** The autocorrelation LPC of a frame costs $O(N p + p^2)$ and the roots $O(p^3)$ with a companion matrix. At the usual orders, 10 to 18, this is small next to the cost of reading the signal.

## Reductions

- **To root finding.** Given the LPC polynomial, the formants are its roots mapped by $F = \theta f_s / 2\pi$ and $B = -(f_s/\pi)\ln r$.
- **To the normal equations.** Fitting the all-pole model by least squares is the [linear prediction](/linear-prediction/) problem, solved by the Levinson-Durbin recursion in $O(p^2)$ time.
- **Tracking to shortest paths.** With a cost per candidate and per transition, choosing a track is a shortest path in a layered graph.

## Applications

- **Phonetics.** Vowel charts of $F_1$ against $F_2$, studies of accents, and speech development.
- **Speech synthesis.** The parameters for [formant synthesis](/formant-synthesis/) come from formant analysis of natural speech.
- **Forensic and clinical work.** Speaker comparison and voice disorder assessment use formant measurements.
- **Features.** Early speech recognizers used formants; modern ones use [MFCC](/mel-frequency-cepstral-coefficients/) or learned features, which carry the same information less explicitly.

## References
