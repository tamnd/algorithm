---
tag: D01A4J
kind: algorithm
slug: rapt-pitch-tracker
name: RAPT pitch tracker
aliases:
- robust algorithm for pitch tracking
area: natural-language-and-speech/speech-analysis-and-synthesis
level: advanced
summary: Talkin's pitch tracker. Candidate periods from normalized cross-correlation peaks, then a dynamic program picks the best voiced or unvoiced path.
solves: [pitch-detection]
model: real-ram
complexity:
  vars: {F: the number of frames, K: the largest lag in samples, n: the correlation window in samples, C: the most candidates per frame}
  time: {worst: O(F (K n + C^2))}
  space: {extra: O(K + n + F C)}
properties: {deterministic: true, online: false, in_place: false, exact: false}
history:
  year: 1995
  people: [David Talkin]
  note: Talkin described RAPT in a chapter of the book Speech Coding and Synthesis. It combined the normalized cross-correlation, a coarse pass on a downsampled signal and a dynamic program over candidates with voicing costs.
prereqs: [pitch-detection, normalized-cross-correlation, dag-dynamic-programming]
see_also: [pyin, cepstral-pitch-detection, yin-algorithm, autocorrelation, viterbi-algorithm, linear-predictive-coding, voice-activity-detection, sample-rate-conversion]
sources:
  - book: isbn:9780444821690
    title: David Talkin, A robust algorithm for pitch tracking (RAPT), chapter 14 of W. B. Kleijn and K. K. Paliwal (editors), Speech Coding and Synthesis, Elsevier, 1995, 495 to 518
    locator: "Section 2.2.6 (the normalized cross-correlation, equations 2.6 and 2.7), Section 3.3 (the two passes), Section 3.5 (the dynamic program, equations 3.6 to 3.20) and the table of parameters on page 509"
  - book: isbn:9780132136037
    title: Lawrence R. Rabiner and Ronald W. Schafer, Digital Processing of Speech Signals, Prentice-Hall, 1978
    locator: the sections on autocorrelation methods of pitch detection
---

RAPT, the robust algorithm for pitch tracking, is a pitch tracker by David Talkin (1995) that finds several period candidates in each frame and then chooses one candidate, or the label unvoiced, per frame with a dynamic program. The candidates are the peaks of the [normalized cross-correlation](/normalized-cross-correlation/) (NCCF) of the frame with later parts of the signal, and the dynamic program adds costs for weak peaks, for changes of pitch and for switches of voicing. It is close to [pYIN](/pyin/), which also keeps candidates and decodes a track, but with probabilities from YIN and a hidden Markov model instead of hand-set costs, and to the [cepstral detector](/cepstral-pitch-detection/), which decides each frame alone.

## In plain words

Take a short piece of the sound and slide it along the sound that follows. Where the piece matches the sound one period later, the match score is close to 1. In speech, the score is also high at two and three periods, and noise gives small bumps everywhere. RAPT keeps every clear bump as a possible period, plus one "no pitch" choice. Then it looks at the whole utterance. It prefers strong bumps, short periods, small changes from one frame to the next, and few switches between voice and silence. A switch is cheaper where the loudness or the spectrum changes. The cheapest path through all the choices is the pitch track.

## The problem

Given a signal at a sample rate $f_s$ and a pitch range $F_{0\min}$ to $F_{0\max}$ (50 to 500 Hz by default), return for every frame (every 10 ms by default) either a fundamental frequency in Hz or the label unvoiced. The task and its error measures are on the [pitch detection](/pitch-detection/) page. The lag range in samples is $k_{\min} = \lfloor f_s / F_{0\max} \rfloor$ to $K = \lceil f_s / F_{0\min} \rceil$.

## The algorithm

For a frame that starts at sample $m$, with a window of $n$ samples (7.5 ms by default), the NCCF at lag $k$ is

$$\phi(k) = \frac{\sum_{j=m}^{m+n-1} x_j\, x_{j+k}}{\sqrt{e_m\, e_{m+k}}}, \qquad e_j = \sum_{l=j}^{j+n-1} x_l^2 .$$

Unlike the plain [autocorrelation](/autocorrelation/), each lag is normalized by the energy of both windows, so $|\phi(k)| \le 1$ and the value does not fall off at long lags. The voiced candidates of the frame are the local maxima of $\phi$ with $\phi \ge$ CAND_TR times the largest value, at most N_CANDS minus 1 of them, refined by a parabola through three points. Each candidate $j$ has a lag $L_j$ and a value $C_j$. One more candidate means unvoiced.

The local costs of frame $i$ are (Talkin's equations 3.6 and 3.7)

$$d_{i,j} = 1 - C_{i,j} \Bigl(1 - \frac{\text{LAG\_WT}}{K} L_{i,j}\Bigr), \qquad d_{i,\text{unv}} = \text{VO\_BIAS} + \max_j C_{i,j}.$$

The transition costs from candidate $k$ of frame $i - 1$ to candidate $j$ of frame $i$ are, with $\xi = |\ln(L_{i,j} / L_{i-1,k})|$ (equations 3.8 to 3.15),

| from | to | cost |
|---|---|---|
| voiced | voiced | FREQ_WT $\cdot \min(\xi,\ \text{DOUBL\_C} + \lvert \xi - \ln 2 \rvert)$ |
| unvoiced | voiced | VTRAN_C + VTR_S_C $\cdot S_i$ + VTR_A_C $/ r_i$ |
| voiced | unvoiced | VTRAN_C + VTR_S_C $\cdot S_i$ + VTR_A_C $\cdot r_i$ |
| unvoiced | unvoiced | 0 |

Here $r_i$ is the ratio of the RMS of frame $i$ to the RMS of frame $i - 1$, so an onset is cheap where the level rises and an offset is cheap where it falls. $S_i = 0.2 / (I_i - 0.8)$, where $I_i \ge 1$ is the Itakura ratio of the LPC spectra of the two frames, so a voicing switch is cheap where the spectrum changes. The defaults (Talkin's table) are CAND_TR 0.3, LAG_WT 0.3, FREQ_WT 0.02, VTRAN_C 0.005, VTR_A_C 0.5, VTR_S_C 0.5, VO_BIAS 0, DOUBL_C 0.35 and N_CANDS 20.

```pseudo id=main
RAPT(x, fs)
L1  for each frame i: phi_i(k) <- the NCCF at lag k for k_min - 1 <= k <= K + 1
L2      cands_i <- the interpolated local maxima of phi_i with value >= CAND_TR * max, at most N_CANDS - 1, plus unvoiced
L3      d_i(j) <- 1 - C_j (1 - LAG_WT L_j / K) for voiced j; d_i(unvoiced) <- VO_BIAS + max_j C_j
L4      r_i <- RMS ratio to frame i - 1; S_i <- 0.2 / (Itakura ratio - 0.8)
L5  D_1(j) <- d_1(j) for every candidate j of frame 1
L6  for i <- 2 to F do
L7      D_i(j) <- d_i(j) + min over k of (D_{i-1}(k) + delta_i(k, j)); psi_i(j) <- the argmin
L8  j_F <- the argmin of D_F
L9  for i <- F down to 2 do j_{i-1} <- psi_i(j_i)
L10 return fs / L for each frame whose chosen candidate is voiced, else unvoiced
```

Lines L1 to L4 are the per-frame stage and lines L5 to L9 the dynamic program (equations 3.17 and 3.18). The code here computes the NCCF at the full rate. The paper does it in two passes, which is faster: a first pass on a copy of the signal downsampled to about $4 F_{0\max}$ finds the rough peaks, and a second pass computes the NCCF at the full rate only near those peaks.

## Example

**The dynamic program.** Take $f_s = 8000$ Hz, so $K = 160$ and LAG_WT$/K = 0.001875$. Four frames have these voiced candidates (lag, value) and frame values $r_i$ and $S_i$:

| frame | candidates | $r_i$ | $S_i$ |
|---|---|---|---|
| 1 | (40, 0.95), (80, 0.90) | | |
| 2 | (40, 0.45), (120, 0.40) | 1 | 1 |
| 3 | (40, 0.94), (80, 0.88) | 1 | 1 |
| 4 | (97, 0.30) | 0.1 | 0.2 |

The local costs are

| frame | first | second | unvoiced |
|---|---|---|---|
| 1 | 0.12125 | 0.235 | 0.95 |
| 2 | 0.58375 | 0.69 | 0.45 |
| 3 | 0.1305 | 0.252 | 0.94 |
| 4 | 0.75456 | | 0.30 |

Alone, frame 2 would be unvoiced, since $0.45 < 0.58375$. But each switch between frames 1 to 3 costs $0.005 + 0.5 + 0.5 = 1.005$, so the path 40, unvoiced, 40 pays 2.01 for two switches. The best path is 40, 40, 40, unvoiced, with cost

$$0.12125 + 0.58375 + 0.1305 + 0.30 + (0.005 + 0.5 \cdot 0.2 + 0.5 \cdot 0.1) = 1.2905 .$$

The last switch is cheap, 0.155, because the level falls by a factor of 10 and the spectrum changes. The next best path, which starts at lag 80 in frame 1, costs 1.41125. The frequency of the first three frames is $8000 / 40 = 200$ Hz. A search over all $3 \cdot 3 \cdot 3 \cdot 2 = 54$ paths gives the same answer.

**A track.** A 160 Hz pulse train through a resonance at 500 Hz, 1200 samples long, followed by 800 samples of noise with standard deviation 0.02, gives 23 frames. On the periodic part the NCCF is 1.0 at lags 50, 100 and 150, and the lag cost picks 50, so the first 14 frames give 159.85 to 160.2 Hz. On the noise the largest NCCF peak is between 0.25 and 0.4, the unvoiced cost is lower, and the offset is cheap there ($r = 0.585$ and $S = 0.166$ at frame 14), so the last 9 frames are unvoiced.

## Correctness

RAPT is an estimator, so no theorem says that its track is the true pitch. The provable parts are these. The NCCF lies in $[-1, 1]$ by the Cauchy-Schwarz inequality, and it equals 1 at every multiple of the period of a periodic signal with a nonzero frame. The Itakura ratio is at least 1, because the LPC inverse filter of a frame minimizes the quadratic form of its autocorrelation matrix, so $S_i \le 1$. And the dynamic program returns a path of least total cost, by induction on the frames: the best path to candidate $j$ of frame $i$ extends a best path to some candidate of frame $i - 1$, because the cost is a sum of terms that each depend on one frame or one pair of neighbors. The proofs are in proofs/correctness.md.

The costs themselves are heuristics. Talkin chose the defaults by hand on speech data.

## Complexity

In the [real RAM](/real-ram/), line L1 costs $O(K n)$ per frame, with running sums for the energies $e_{m+k}$. Line L2 costs $O(K \log K)$, line L4 $O(n p + p^2)$ for LPC order $p$, and line L7 $O(C^2)$ for $C$ candidates per frame. The total is $O(F (K n + C^2))$ time, with $O(F C)$ memory for the back pointers. At 8 kHz with defaults, $K n = 160 \cdot 60 = 9600$ products per frame. The two passes of the paper reduce this: the first pass works on a signal downsampled by a factor $q$, which costs about $1/q^2$ as much, and the second pass computes only a few lags around each peak.

## Properties

- **Candidates, not decisions.** Each frame keeps up to 19 periods and an unvoiced choice, so a weak frame inside a vowel can still get the right period from its neighbors.
- **Voicing from costs.** The voicing decision uses the correlation, the level change and the spectral change together, not a fixed threshold.
- **Short delay in practice.** The best paths to the candidates of the current frame usually share their start, so the decision for an older frame is fixed after a short delay. Talkin reports that this delay is rarely over 100 ms, which is a measurement.
- **Octave jumps are allowed.** The term DOUBL_C $+ |\xi - \ln 2|$ makes a jump of one octave cost $0.02 \cdot 0.35 = 0.007$ instead of $0.02 \ln 2 = 0.014$, so real octave jumps, such as into vocal fry, are not blocked.
- **Deterministic.** The same input gives the same track.

## Variants and improvements

- **Two passes.** The paper's form, described above. It is the main speed difference from this code.
- **Other candidate sources.** [YIN](/yin-algorithm/) dips or [cepstral](/cepstral-pitch-detection/) peaks can feed the same dynamic program.
- **Probabilistic costs.** [pYIN](/pyin/) replaces the hand-set costs by probabilities and the dynamic program by the [Viterbi algorithm](/viterbi-algorithm/) on a hidden Markov model.
- **Later trackers by Talkin.** REAPER, from Google, also uses an NCCF and dynamic programming, and adds glottal closure instants.

## When to use it

Use RAPT for speech when a robust offline pitch track with voicing decisions is needed and no training data are available, for example for prosody analysis, speech synthesis corpora and voice research. It is a common reference tracker. For music with a wide pitch range, or when a voicing probability is needed, pYIN is a better fit. For noisy speech, learned trackers are now often better; their results depend on the data.

## Pitfalls

- **The frame needs more signal than the window.** The NCCF uses $n + K + 1$ samples from the frame start; at 50 Hz and 16 kHz that is more than 320 lags.
- **Silent frames.** If $e_m e_{m+k} = 0$, the NCCF is undefined. This code returns 0 there; a small constant in the denominator also works and lowers the values in very quiet frames.
- **Parameters for another sample rate.** The defaults are in seconds and in hertz, so they carry over, but the lag weight uses $K$, which depends on $F_{0\min}$. Changing the range changes the costs.
- **Sub-octave errors.** Every multiple of the period also gives an NCCF peak close to 1. Only the lag weight, LAG_WT, prefers the shortest one. If LAG_WT is 0, the tracker can choose half the true frequency.
- **Hand-set costs.** The costs are not probabilities, so the total cost has no meaning outside the comparison of paths.

## Implementations

## History

Talkin's program get_f0, which implements RAPT, shipped with the ESPS speech tools of Entropic Research Laboratory. The 1995 book chapter is the reference description. The method combined ideas older than it: the normalized cross-correlation for periodicity, a coarse search on a downsampled signal, and dynamic programming over frame candidates, which earlier trackers had used for smoothing. RAPT became a standard baseline in speech research.

## References
