---
tag: Z76XPX
kind: algorithm
slug: psola
name: Pitch-synchronous overlap-add
aliases:
- PSOLA
- TD-PSOLA
area: natural-language-and-speech/speech-analysis-and-synthesis
level: core
summary: Change pitch and duration by cutting windowed segments centered on pitch marks and overlap-adding them at new spacing.
model: real-ram
complexity:
  vars: {M: the number of synthesis marks, P: the largest local pitch period in samples, K: the number of analysis pitch marks}
  time: {worst: O(M P + K)}
  space: {extra: O(P)}
properties: {deterministic: true, online: true, in_place: false, exact: false}
history:
  year: 1990
  people: [Eric Moulines, Francis Charpentier]
  note: Developed at CNET in France in the late 1980s for diphone text-to-speech. Moulines and Charpentier described the time-domain, frequency-domain and LPC versions in Speech Communication in 1990.
prereqs: [overlap-add-method, pitch-detection, window-functions]
see_also: [phase-vocoder, source-filter-model, formant-synthesis, rapt-pitch-tracker, yin-algorithm, sample-rate-conversion]
sources:
  - paper: doi:10.1016/0167-6393(90)90021-Z
    title: Eric Moulines and Francis Charpentier, Pitch-synchronous waveform processing techniques for text-to-speech synthesis using diphones, Speech Communication 9(5-6), 1990, 453 to 467
    locator: the sections on the time-domain PSOLA method (pitch-synchronous analysis windows, synthesis pitch marks, time-scale and pitch-scale modification)
---

PSOLA changes the pitch and the duration of a voiced speech signal directly on the wave. It needs the pitch marks of the input, one per period, from a [pitch detector](/pitch-detection/) or a detector of glottal closures. Around each mark it cuts a segment of two periods with a smooth window, and it adds the segments back with [overlap-add](/overlap-add-method/) at new marks: closer together for a higher pitch, and repeated or skipped for a longer or shorter sound. The [phase vocoder](/phase-vocoder/) does the same jobs in the frequency domain without pitch marks, and works on music; PSOLA is cheaper and sounds more natural on one voice.

## In plain words

A voiced sound like a vowel is a series of nearly identical pulses, one per vibration of the vocal folds, and each pulse rings with the shape of the mouth. PSOLA cuts the sound into small overlapping pieces, each centered on one pulse. To raise the pitch, it puts the pieces back closer together, so more pulses come per second. Each piece keeps its own shape, so the ringing, and with it the vowel, stays the same. To make the sound longer, it uses some pieces twice; to make it shorter, it leaves some out. Because the pieces are cut where the pulses are, they fit together without breaks.

## The problem

Given a voiced signal $x$ with pitch marks $t_1 < \dots < t_K$, a pitch factor $\beta > 0$ and a duration factor $\alpha > 0$, produce a signal $y$ of $\alpha$ times the length whose pitch is $\beta$ times the pitch of $x$ at the corresponding time, and whose spectral envelope, the formants, is the same as that of $x$. This is the signal part of concatenative [text-to-speech](/text-to-speech/), where the units chosen by [unit selection](/unit-selection-synthesis/) must be brought to the target pitch and duration.

## The algorithm

The local period at mark $i$ is $P_i = \text{round}((t_{i+1} - t_{i-1}) / 2)$, with the one neighbor gap at the two ends. The segment of mark $i$ is $g_i[j] = w_i[j]\, x[t_i - P_i + j]$ for $j = 0, \dots, 2P_i$, with the symmetric Hann window $w_i$ of length $2P_i + 1$.

```pseudo id=main
TD-PSOLA(x, marks t_1 .. t_K, pitch factor beta, duration factor alpha)
L1  P_i <- the local period at each mark
L2  y <- zeros of length round(alpha |x|); s <- alpha t_1
L3  while s <= alpha t_K do
L4      i <- the analysis mark nearest to s / alpha
L5      g <- Hann window of length 2 P_i + 1 times x[t_i - P_i .. t_i + P_i]
L6      add g to y, centered on round(s)
L7      s <- s + P_i / beta
L8  return y
```

The synthesis marks $s$ are spaced by the local period divided by $\beta$, which sets the new pitch. The map $s / \alpha$ back to the original time axis sets the duration: for $\alpha = 2$ each analysis mark is nearest to two synthesis marks in a row, so each segment is used twice. Unvoiced parts have no pitch marks; systems put marks at a fixed rate there, for example every 10 ms, and do not change their spacing.

## Example

Take $f_s = 8000$ Hz and 1600 samples of a 100 Hz pulse train through one resonator at 500 Hz with a bandwidth of 60 Hz, a one-formant vowel. The pitch marks are the 20 pulses at $0, 80, \dots, 1520$, so $P_i = 80$.

- **Pitch up by $\beta = 1.25$.** The synthesis marks are $0, 64, 128, \dots, 1472$, 24 of them, and they take the segments of the analysis marks $0, 1, 2, \dots, 18$. The output has 1600 samples and a period of 64 samples, 125 Hz. Its strongest harmonic is still at 500 Hz:

| | harmonic below | 500 Hz | harmonic above |
|---|---|---|---|
| input (100 Hz) | 400 Hz: 0.2254 | 0.7092 | 600 Hz: 0.1864 |
| output (125 Hz) | 375 Hz: 0.2622 | 0.8863 | 625 Hz: 0.2117 |

- **Pitch down by $\beta = 0.8$.** The output has a period of 100 samples, 80 Hz, and its strongest harmonic is the one nearest the formant, at 480 Hz.
- **Twice as long, $\alpha = 2$.** The output has 3200 samples and 39 synthesis marks, still 80 apart, and they use the analysis segments $0, 1, 1, 2, 2, 3, 3, \dots$.

The amplitudes come from the Fourier sums over whole periods of the signals, a measurement. The level at 500 Hz rises by $0.8863 / 0.7092 = 1.2497$, close to $\beta$, because the segments are added $\beta$ times as often; systems scale the output by $1 / \beta$ when this matters.

## Correctness

These are theorems, proved in proofs/correctness.md:

- **Identity.** If the marks are spaced by a constant $P$ and $\alpha = \beta = 1$, then $y[n] = x[n]$ for $t_1 \le n \le t_K$, because the Hann windows of length $2P + 1$ at the spacing $P$ add to 1.
- **Pitch change of a periodic signal.** If $x$ has period $P$, the marks are spaced by $P$ and $Q = P / \beta$ is an integer, then all segments are equal to one segment $g$, and away from its ends the output is periodic with period $Q$. Its Fourier coefficients over one period have the moduli $|G(2\pi k / Q)| / Q$, where $G$ is the DTFT of $g$. So the new harmonics sample the spectrum of one segment.
- **Duration.** The output has $\text{round}(\alpha |x|)$ samples, and the synthesis marks cover the time $\alpha t_1$ to $\alpha t_K$.

That $G$ follows the spectral envelope of the speech, so that the formants stay in place, is a heuristic. It holds well when the segment of two periods contains the decaying response of the vocal tract to one pulse, and it gets worse as $\beta$ moves far from 1, as the measurements above show.

## Complexity

Each synthesis mark adds a segment of $2P_i + 1$ samples, and the search for the nearest analysis mark moves only forward, so the time is $O(M P + K)$ for $M$ synthesis marks, $K$ analysis marks and a largest period $P$. Apart from the output, the memory is one window, $O(P)$. Since $M P$ is about $2 \beta$ times the output length, this is a few operations per output sample, much less than the FFTs of the phase vocoder.

## Properties

- **Time domain.** No transform and no phase estimate; the waveform shape inside each period is copied as it is.
- **Needs pitch marks.** The quality depends on marks that sit at the same point of each period. Errors of a few samples make the segments add out of phase.
- **Keeps the envelope.** The formants stay in place for moderate changes of pitch, without any explicit vocal tract model.
- **Online.** Each output segment needs the input up to one period after its mark.

## Variants and improvements

- **FD-PSOLA and LP-PSOLA.** Moulines and Charpentier also described a frequency-domain version and a version that applies PSOLA to the residual of linear prediction, which gives separate control of the envelope.
- **Waveform similarity overlap-add (WSOLA).** For time stretching only, choose each segment by cross-correlation with the previous output, instead of by pitch marks.
- **Resynthesis of the units.** Some systems first resynthesize all units of the database at one constant pitch with fixed phases, so that PSOLA can join them without errors from the pitch marks.
- **Sinusoidal and harmonic models.** Model the voiced speech as a sum of harmonics and change their frequencies directly; this handles larger changes of pitch.

## When to use it

Use PSOLA to change the pitch and duration of a single voice by moderate factors, about 0.5 to 2, as in concatenative [text-to-speech](/text-to-speech/), prosody experiments and voice changers. For music, chords or noise, use the [phase vocoder](/phase-vocoder/). For large changes, a model that separates source and filter, such as the [source-filter model](/source-filter-model/), sounds better.

## Pitfalls

- **Bad pitch marks.** Marks that move from one point of the period to another, or a detected period that is half or double the true one, give rough or doubled voices.
- **Very low pitch.** For $\beta < 0.5$ the segments, of two periods, no longer overlap, and the output gets gaps between the pulses.
- **Repeated noise.** Stretching an unvoiced sound by repeating the same segments makes a buzz at the repetition rate. Reverse every second copy or use fresh noise.
- **Level change.** The output level scales about with $\beta$, as in the example. Scale by $1 / \beta$.
- **Phase mismatch at joins.** Units from different recordings may have marks at different points of the period, which gives a click at the join.

## Implementations

## History

PSOLA was developed in the late 1980s at the Centre national d'études des télécommunications (CNET) in France, for text-to-speech by concatenation of diphones. Eric Moulines and Francis Charpentier described its time-domain, frequency-domain and LPC versions in Speech Communication in 1990. The time-domain version became the standard way to change the prosody of recorded speech in the concatenative systems of the 1990s, until statistical and neural synthesis made the waveform from parameters directly.

## References
