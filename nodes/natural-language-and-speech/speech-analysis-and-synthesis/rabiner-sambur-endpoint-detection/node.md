---
tag: B6AHEG
kind: algorithm
slug: rabiner-sambur-endpoint-detection
name: Rabiner-Sambur endpoint detection
aliases:
- energy and zero-crossing endpoint detection
- Rabiner-Sambur algorithm
area: natural-language-and-speech/speech-analysis-and-synthesis
level: core
summary: Find the start and end of an isolated word from short-time energy thresholds, refined by zero-crossing rate to keep weak fricatives.
solves: [voice-activity-detection]
model: real-ram
complexity:
  vars: {L: the number of samples, T: the number of 10 ms frames}
  time: {worst: O(L)}
  space: {extra: O(T)}
properties: {deterministic: true, online: false, in_place: false, exact: true}
history:
  year: 1975
  people: [Lawrence R. Rabiner, Marvin R. Sambur]
  note: Rabiner and Sambur set two energy thresholds and one zero-crossing threshold from the first 100 ms of a recording, which they took as silence, and used them to find the endpoints of isolated words, including words that begin or end with weak fricatives.
prereqs: [zero-crossing-rate, voice-activity-detection]
see_also: [likelihood-ratio-vad, dynamic-time-warping, keyword-spotting, energy-detector, pre-emphasis, mel-frequency-cepstral-coefficients, automatic-speech-recognition, hidden-markov-model]
sources:
  - paper: doi:10.1002/j.1538-7305.1975.tb02840.x
    title: L. R. Rabiner and M. R. Sambur, An algorithm for determining the endpoints of isolated utterances, The Bell System Technical Journal 54(2), 1975, 297 to 315
    locator: "the description of the algorithm: the silence statistics of the first 100 ms, the thresholds ITL, ITU and IZCT, the energy search for N1 and N2, and the search over 25 frames for weak fricatives"
  - book: isbn:9780132136037
    title: L. R. Rabiner and R. W. Schafer, Digital Processing of Speech Signals, Prentice Hall, 1978
    locator: "Chapter 4 (time domain processing of speech), the discussion of speech and silence discrimination with energy and zero-crossing rate"
---

The Rabiner-Sambur algorithm finds the first and the last frame of a single spoken word in a recording that starts with about 100 ms of silence. It uses only two numbers per 10 ms frame: the short-time energy and the [zero-crossing rate](/zero-crossing-rate/). It returns one pair of endpoints for the whole recording, while a general [voice activity detector](/voice-activity-detection/) labels every frame as speech or non-speech and can find many segments. The thresholds are rules of thumb fixed from the silence at the start, where a [likelihood ratio VAD](/likelihood-ratio-vad/) uses a statistical model of the noise and of speech.

## In plain words

Before a person says a word, the recording holds only background noise. The algorithm listens to this short quiet part to learn how loud and how busy the background is. Then it looks for the place where the sound becomes clearly louder than the background, and for the place where it becomes quiet again. Loudness alone misses soft sounds such as "f", "th" or "h" at the start or end of a word, because they are hardly louder than the noise. Such sounds are hiss, so the signal crosses zero many more times than in the background. The algorithm therefore looks a little before the start and a little after the end, and if it finds enough hissing frames there, it moves the endpoint out to include them.

## The problem

Given a recording $s$ of an isolated word at a sample rate $f_s$, in which the first 100 ms are background only, find frame indices $N_1 \le N_2$ such that the word occupies the frames $N_1$ to $N_2$, or report that there is no word. The frames are 10 ms long, with no overlap and no padding, so a recording of $L$ samples gives $T = \lfloor L / (f_s / 100) \rfloor$ frames. This page uses $f_s = 16$ kHz, so a frame has 160 samples.

## The algorithm

For each frame $i$ the energy is $E[i] = \sum_n |s[n]|$ over the frame, and $Z[i]$ is the number of adjacent sample pairs in the frame with different signs, where 0 counts as positive. All the constants below are the heuristic values of the paper.

```pseudo id=main
RABINER-SAMBUR(s, f_s)
L1  cut s into 10 ms frames; for each frame i: E[i] ← Σ |s[n]|, Z[i] ← number of sign changes
L2  IZC, σ ← mean and standard deviation of Z[0 .. 9]; IZCT ← min(25, IZC + 2σ)
L3  IMN ← mean of E[0 .. 9]; IMX ← max E; ITL ← min(0.03 (IMX - IMN) + IMN, 4 IMN); ITU ← 5 ITL
L4  N1 ← first i, going forward, with E[i] > ITL after which E goes above ITU before it falls to ITL or below; if there is none, return "no word"
L5  N2 ← the same, going backward from the last frame
L6  if at least 3 of the 25 frames before N1 have Z > IZCT, then N1 ← the earliest of them
L7  if at least 3 of the 25 frames after N2 have Z > IZCT, then N2 ← the latest of them
L8  return (N1, N2)
```

Line L4 rejects short bursts: a frame above ITL starts the word only if the energy then reaches ITU without dropping back first, so a click that stays under ITU is skipped. The fixed bound of 25 crossings per 10 ms in line L2 keeps a noisy background from raising IZCT above the level of a fricative. The search in lines L6 and L7 is limited to 25 frames, 250 ms, because a weak fricative is shorter than that.

The paper calls IMN the energy of the silence measured in the first 100 ms; this page takes it as the mean of $E$ over those 10 frames, and takes $\sigma$ as the population standard deviation.

## Example

Take a recording of 128 frames at 16 kHz: 300 ms of low-pass background noise, 10 frames of white noise with standard deviation 0.006 as a weak fricative, 500 ms of a 300 Hz tone with amplitude 0.3 as the voiced part, 8 more frames of the fricative, and 300 ms of background. The background is white noise of standard deviation 0.0006 through the one-pole filter $1/(1 - 0.98 z^{-1})$, so it has few zero crossings.

Lines L2 and L3 give $IZC = 8.9$ and $IZCT = 20.37$, $IMN = 0.4288$ and $IMX = 30.69$. Since $0.03(IMX - IMN) + IMN = 1.3368$ is below $4\,IMN = 1.715$, $ITL = 1.3368$ and $ITU = 6.6838$. The fricative frames have energies between about 0.73 and 0.82, below ITL, so lines L4 and L5 find only the tone: $N_1 = 40$ and $N_2 = 89$. But the fricative frames have between 62 and 96 crossings, far above IZCT, while the background frames have about 9. In line L6, all 10 frames 30 to 39 before $N_1$ have $Z > IZCT$, so $N_1$ moves to 30. In line L7, the 8 frames 90 to 97 qualify, so $N_2$ moves to 97. The result is $(30, 97)$, which is the whole word. The same recording without the fricatives gives $(30, 79)$, the tone alone, because the refinement finds no frames with high $Z$.

## Correctness

Whether the frames $N_1$ to $N_2$ are the word depends on the recording, and the thresholds are heuristics that Rabiner and Sambur tuned on their data. What can be proved is what the output means in terms of $E$ and $Z$. The full proofs are below.

- **The thresholds are ordered.** If $IMN > 0$, then $IMN < ITL$ when $IMX > IMN$, and $ITL < ITU$ always (theorem).
- **The interval holds every loud frame.** If line L4 finds $N_1$, then line L5 finds an $N_2 \ge N_1$, every frame with $E > ITU$ lies between $N_1$ and $N_2$ after lines L4 and L5, and the refinement only widens the interval (theorem).
- **The ends are word-like.** After line L5, $E[N_1] > ITL$ and $E[N_2] > ITL$, and each connects to a frame above ITU through frames above ITL. After lines L6 and L7, a moved endpoint is a frame with $Z > IZCT$ (theorem).
- **Gain does not matter.** Multiplying the recording by $c > 0$ multiplies every $E$ and every threshold of line L3 by $c$ and leaves every $Z$ unchanged, so the endpoints do not change (theorem).

## Complexity

In the [real RAM](/real-ram/), line L1 reads every sample once, $O(L)$ time. Lines L2 and L3 cost $O(T)$, lines L4 and L5 each scan at most $T$ frames, and lines L6 and L7 look at 25 frames each. The total is $O(L)$ time, and the arrays $E$ and $Z$ take $O(T)$ memory. For one second at 16 kHz this is 16 000 samples and 100 frames.

## Properties

- **Offline.** IMX in line L3 is the maximum over the whole recording, and line L5 scans from the end, so the algorithm needs the whole recording before it answers.
- **One word.** It returns one interval. Pauses inside the word, such as the closure before a stop consonant, stay inside the interval, but two words with a long pause give one interval that holds both.
- **Few parameters.** All thresholds adapt to the recording through IMN, IMX and the statistics of $Z$ in the silence. Nothing is trained.
- **Gain invariant, not offset invariant.** A gain changes nothing, but a DC offset changes the zero crossings of the quiet frames.

## Variants and improvements

- **Squared energy or log energy.** Many later detectors use $\sum s[n]^2$ or its log in place of the sum of magnitudes. The thresholds must then be set again, since the ratios 0.03, 4 and 5 were chosen for the sum of magnitudes.
- **Adaptive background.** Continuous speech systems update the noise statistics in pauses, in place of reading them once from the first 100 ms. This turns the method into a frame-wise [voice activity detector](/voice-activity-detection/).
- **Statistical detectors.** A [likelihood ratio VAD](/likelihood-ratio-vad/) models the noise and the speech spectra and decides per frame, which works at a lower signal to noise ratio.
- **Hangover.** Detectors for streams keep the speech label for a few frames after the energy drops, which plays the role of the backward search here.

## When to use it

Use the Rabiner-Sambur detector for isolated words recorded in a quiet room, such as command words for a [dynamic time warping](/dynamic-time-warping/) recognizer, where a clean start and end matter and the recording begins with silence. It is cheap and needs no training data. Do not use it for continuous speech, for streams without a known silent start, or at low signal to noise ratios: there a statistical [voice activity detector](/voice-activity-detection/) or the silence model of an [HMM](/hidden-markov-model/) recognizer does better.

## Pitfalls

- **No silence at the start.** If the speaker starts at once, the first 10 frames contain speech, IMN and IZC are far too high, and the word is cut or missed.
- **DC offset.** A constant offset can make the background never cross zero, so IZC is near 0 and IZCT is small, or it can hide the crossings of a fricative. Remove the mean before line L1.
- **Hum and hiss.** A background with many zero crossings, such as broadband hiss, makes IZCT reach the bound of 25, and then fricatives that are quieter than the hiss are not found.
- **Mouth noise.** Lip smacks and breaths just before or after the word can exceed ITU or have high $Z$, and then they are included.
- **Frame length.** The bound of 25 crossings is per 10 ms. With another frame length, scale it by the frame length.

## Implementations

## History

Endpoint detection was a central problem for the isolated word recognizers of the 1970s, which matched a whole word against stored templates and failed when the word boundaries were wrong. Rabiner and Sambur published their detector in 1975, at Bell Laboratories, and added the zero-crossing search to recover the weak fricatives that an energy detector cuts off. The method appears in the 1978 textbook of Rabiner and Schafer and became a standard teaching example of time domain speech processing. Later recognizers based on hidden Markov models handled silence with their own models, and modern systems use statistical or neural voice activity detectors.

## References
