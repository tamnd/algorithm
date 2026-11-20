---
tag: D7ZPSZ
kind: algorithm
slug: formant-synthesis
name: Formant synthesis
aliases:
- Klatt synthesizer
area: natural-language-and-speech/speech-analysis-and-synthesis
level: core
summary: Make speech by passing a source signal through resonators set to formant frequencies and bandwidths, controlled by rules over time.
model: real-ram
complexity:
  vars: {N: the number of output samples, K: the number of resonators, P: the number of parameter frames}
  time: {worst: O(N K + P K)}
  space: {extra: O(K)}
properties: {deterministic: true, online: true, in_place: false, exact: true}
history:
  year: 1980
  people: [Dennis H. Klatt]
  note: Klatt published a software synthesizer with second-order digital resonators in cascade and in parallel, updated every 5 ms at 10 kHz, with its FORTRAN listing. Hardware formant synthesizers had existed since the 1950s.
prereqs: [source-filter-model, iir-filter, frequency-response]
see_also: [formant-estimation, linear-predictive-coding, psola, transfer-function, z-transform, impulse-response, unit-selection-synthesis, pitch-detection]
sources:
  - paper: doi:10.1121/1.383940
    title: Dennis H. Klatt, Software for a cascade/parallel formant synthesizer, Journal of the Acoustical Society of America 67(3), 1980, 971 to 995
    locator: equations 1 to 5 (the digital resonator, its transfer function and the antiresonator), the description of the cascade and parallel branches, and Appendix B (the program listing)
  - book: isbn:9780132136037
    title: Lawrence R. Rabiner and Ronald W. Schafer, Digital Processing of Speech Signals, Prentice-Hall, 1978
    locator: Chapter 3 (digital models of the speech signal, the vocal tract as a cascade of resonators)
---

Formant synthesis makes speech from a few slowly changing numbers: a pitch, a source amplitude and the frequencies and bandwidths of the formants, the resonances of the vocal tract. A source of pulses or noise goes through a chain of second-order digital resonators, one per formant, as in the [source-filter model](/source-filter-model/). It is the inverse of [formant estimation](/formant-estimation/), which reads the formants from speech, and the oldest method of [text-to-speech](/text-to-speech/), where rules set the parameters over time; later methods such as [unit selection](/unit-selection-synthesis/) and [PSOLA](/psola/) join recorded speech instead.

## In plain words

When you say a vowel, your vocal folds make a buzz of short pulses, and your mouth and throat make some frequencies of that buzz louder than others. Those loud regions are the formants, and they tell the listener which vowel it is. A formant synthesizer copies this with arithmetic. It makes a train of pulses at the pitch you want. It sends them through a few simple filters, each of which rings at one frequency, like a bell, and dies away at a set speed. Every few milliseconds the program changes the pitch and the ring frequencies, and the vowel and pitch change with them. For sounds like "s", it uses noise instead of pulses.

## The problem

Given a sample rate $f_s$, an update period (5 ms), and for each update a fundamental frequency $F_0$ (0 for no voicing), a voicing amplitude $A_V$ and $K$ formants $(F_k, B_k)$ in Hz, produce the samples of the speech wave. The [text-to-speech](/text-to-speech/) problem adds the rules that turn phonemes into these parameter tracks; this page covers the signal part.

## The algorithm

The building block is the digital resonator of Klatt's equations 1 and 2. With the sample period $T = 1 / f_s$, center frequency $F$ and bandwidth $B$,

$$y[n] = A\, x[n] + B_1\, y[n-1] + C\, y[n-2],$$
$$C = -e^{-2\pi B T}, \qquad B_1 = 2 e^{-\pi B T} \cos(2\pi F T), \qquad A = 1 - B_1 - C .$$

(Klatt calls the middle coefficient $B$; it is $B_1$ here to keep it apart from the bandwidth.) Its transfer function is $H(z) = A / (1 - B_1 z^{-1} - C z^{-2})$. The poles are $r e^{\pm i\theta}$ with $r = e^{-\pi B T}$ and $\theta = 2\pi F T$, so the filter rings at $F$ and its envelope decays at a rate set by $B$. The choice of $A$ makes the gain at 0 Hz exactly 1. An antiresonator, for the zeros of nasals, uses $A' = 1/A$, $B_1' = -B_1/A$, $C' = -C/A$ in $y[n] = A' x[n] + B_1' x[n-1] + C' x[n-2]$, which is the inverse of the resonator (equations 4 and 5).

In the cascade form for vowels the resonators are in series, so their responses multiply and the relative formant levels come out right without separate gains. A parallel branch, with one gain per formant, is better for fricatives and is not in the code below.

```pseudo id=main
FORMANT-SYNTHESIS(frames of (F0, AV, (F_1, B_1) .. (F_K, B_K)), fs)
L1  for each parameter frame do
L2      compute (A_k, B1_k, C_k) for every formant k
L3      for each of the fs * 0.005 samples of the frame: emit a pulse of size AV when the pitch phase wraps, else 0
L4          v <- the pulse through a low-pass resonator at 0 Hz (the glottal source)
L5          for k <- 1 to K do v <- A_k v + B1_k y_k[n-1] + C_k y_k[n-2]
L6          output v - v_previous (the radiation at the lips)
```

The states $y_k[n-1]$ and $y_k[n-2]$ carry over from frame to frame, so a change of a formant does not reset the filter and does not click.

## Example

Take $f_s = 10000$ Hz, $F = 500$ Hz and $B = 60$ Hz. Then $r = e^{-\pi \cdot 0.006} = 0.98133$ and $\theta = 0.31416$ rad, and

$$C = -0.9630027, \qquad B_1 = 1.8665948, \qquad A = 1 - 1.8665948 + 0.9630027 = 0.0964078 .$$

The impulse response starts 0.096408, 0.179954, 0.243061, 0.280400, 0.289324, a sinusoid of 500 Hz under the envelope $A r^n / \sin\theta$. The gain at some frequencies:

| frequency (Hz) | 0 | 250 | 470 | 500 | 530 | 1000 | 2000 | 5000 |
|---|---|---|---|---|---|---|---|---|
| gain | 1.000 | 1.330 | 6.139 | 8.429 | 5.793 | 0.345 | 0.077 | 0.025 |
| dB | 0.0 | 2.5 | 15.8 | 18.5 | 15.3 | -9.2 | -22.3 | -32.0 |

The peak is at 499.13 Hz, slightly below $F$, and the gain falls by 3 dB at 468.1 and 528.4 Hz, a width of 60.25 Hz, close to $B$. The peak gain is close to $F / B = 8.33$.

A vowel like /a/ with $F_0 = 100$ Hz, formants (700, 130), (1220, 70) and (2600, 160) and a glottal low-pass with a bandwidth of 100 Hz gives a wave that repeats every 100 samples once the start has decayed. Its harmonics at 700 and 1200 Hz are more than three times as strong as those at 1000 and 1900 Hz, between the formants.

## Correctness

The output is a fixed linear recursion of the parameters, so the claims to prove are the properties of the resonator. These are theorems, proved in proofs/correctness.md: the gain at 0 Hz is 1; the filter is stable for every $B > 0$, since $r < 1$; the impulse response is $h[n] = A r^n \sin((n+1)\theta) / \sin\theta$; the peak of $|H|$ is where $\cos\omega = (1 + r^2) \cos\theta / (2r)$, when this is in $[-1, 1]$; the antiresonator is the exact inverse; and a cascade has the product of the responses. That the half-power width is close to $B$ is an approximation for $B \ll f_s$, checked here as a measurement.

Whether the output sounds like the intended speech depends on the rules and the parameters, which no theorem covers.

## Complexity

Each output sample costs one source step and one resonator step per formant, three multiplications each, so the time is $O(N K)$ for $N$ samples and $K$ resonators, plus $O(P K)$ for the coefficients of $P$ frames, each with one exponential and one cosine per resonator. The memory is two state values per resonator, $O(K)$. With $K = 5$ formants at 10 kHz this is about 150000 multiplications per second.

## Properties

- **Few parameters.** About 10 to 40 numbers every 5 ms describe the speech, which is why formant synthesis was used for very small systems and for speech research.
- **Full control.** Each acoustic property can be changed alone, which makes it the tool for perception experiments.
- **Intelligible but not natural.** Rule-driven formant synthesis can be highly intelligible but sounds buzzy and machine-like, because the simple source and the rules miss the fine detail of real speech; this is a judgment of listeners, measured with tests such as the [mean opinion score](/mean-opinion-score/).
- **Online.** Each sample depends only on the past, so the output can stream.

## Variants and improvements

- **Parallel branch.** Each formant has its own gain and the outputs add. This gives control of the levels for fricatives and plosives, at the cost of setting more gains.
- **Better sources.** A glottal pulse model with an open and a closed phase, instead of filtered impulses, gives a more natural voice; later versions of the design added such sources.
- **Noise source.** Gaussian or uniform noise through the same resonators gives aspiration and frication.
- **Rules.** Text-to-speech systems of the 1970s and 1980s, such as MITalk and its commercial descendant DECtalk, drove formant synthesizers with rules for each phoneme and its neighbors.
- **Articulatory synthesis.** Instead of formants, simulate the shape of the vocal tract; the formants then follow from the shape.

## When to use it

Use formant synthesis for speech perception experiments, where each cue must be set exactly, for teaching acoustics, and for systems with very little memory. For natural-sounding text-to-speech, neural methods such as [WaveNet](/wavenet/) and [HiFi-GAN](/hifi-gan/) have replaced it.

## Pitfalls

- **Coefficients from the wrong rate.** The coefficients depend on $T$. Formants above $f_s / 2$ fold back, so at 10 kHz the formants must stay below 5 kHz.
- **Resetting the state.** Making a new filter at each frame, instead of changing the coefficients of the running one, gives clicks at the frame edges.
- **Gain at the formant.** The gain at the peak is about $F / B$, so a narrow, high formant can overflow a fixed-point output. Scale the source.
- **A bandwidth of zero.** Then $r = 1$ and the resonator never decays. Keep $B > 0$.
- **The peak is not at $F$.** For wide bandwidths at low frequencies the peak moves below $F$, and if $(1 + r^2)\cos\theta / (2r) > 1$ there is no peak above 0 Hz at all.

## Implementations

## History

Electrical formant synthesizers appeared in the 1950s, among them Walter Lawrence's Parametric Artificial Talker (PAT) in England and Gunnar Fant's OVE in Sweden. John Holmes and others built rule systems for them in the 1960s. Dennis Klatt at MIT published a software design in 1980 with both a cascade and a parallel branch, sampled at 10 kHz and updated every 5 ms, and printed its FORTRAN code. Klatt's work led to the MITalk system and to DECtalk, which gave a voice to many users of speech aids. Since the 1990s, concatenative and then neural methods have replaced formant synthesis in products.

## References
