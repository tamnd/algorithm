---
tag: 2F0V3H
kind: technique
slug: cepstral-mean-normalization
name: Cepstral mean normalization
aliases:
- CMN
- cepstral mean and variance normalization
- cepstral mean subtraction
- CMVN
area: natural-language-and-speech/speech-analysis-and-synthesis
level: core
summary: Subtract the mean of each cepstral coefficient over an utterance, which approximately removes a fixed channel filter, and often scale to unit variance.
prereqs: [cepstrum, mel-frequency-cepstral-coefficients]
see_also: [rasta-filtering, delta-features, mel-filter-bank, perceptual-linear-prediction, pre-emphasis, mel-scale, spectral-subtraction, automatic-speech-recognition]
sources:
  - paper: doi:10.1121/1.1914702
    title: B. S. Atal, Effectiveness of linear prediction characteristics of the speech wave for automatic speaker identification and verification, Journal of the Acoustical Society of America 55(6), 1974, 1304 to 1312
    locator: the subtraction of the average cepstrum over the utterance to reduce the effect of the transmission channel
  - paper: "Olli Viikki and Kari Laurila, Cepstral domain segmental feature vector normalization for noise robust speech recognition, Speech Communication 25(1-3), 1998, 133 to 147"
    title: Olli Viikki and Kari Laurila, Cepstral domain segmental feature vector normalization for noise robust speech recognition
    locator: the normalization of both the mean and the variance of each cepstral coefficient over a segment of frames
  - book: isbn:9780130226167
    title: Xuedong Huang, Alex Acero and Hsiao-Wuen Hon, Spoken Language Processing, Prentice Hall, 2001
    locator: "Chapter 10 (Environmental Robustness), the discussion of cepstral mean normalization and its relation to RASTA"
---

Cepstral mean normalization subtracts from each cepstral coefficient its mean over the frames of an utterance, or over a sliding window of frames, so that every coefficient has mean zero. A fixed channel, such as a microphone or a telephone line, adds a nearly constant vector to the cepstra, and the subtraction removes that vector, so the channel is removed approximately, not exactly. [RASTA filtering](/rasta-filtering/) also removes slow components but works frame by frame with a fixed filter, while CMN subtracts one mean per utterance or per window; [delta features](/delta-features/) are not changed by CMN at all, because they ignore constant offsets. The same subtraction works on the log energies of a [mel filter bank](/mel-filter-bank/) and on the cepstra of [MFCC](/mel-frequency-cepstral-coefficients/) or [PLP](/perceptual-linear-prediction/).

## In plain words

A microphone changes the sound in the same way for as long as it is used: it makes some frequencies a little louder and others a little softer. After the log, that change becomes the same number added to every frame. If we take the average of the features over a whole recording and subtract it, that constant part goes away, together with the average of the speech itself. What remains is how each frame differs from the average, and this depends much less on the microphone. Often each feature is also divided by its spread over the recording, so that every feature has about the same scale; this is mean and variance normalization.

## When it applies

- The features are cepstra or log band energies, where a multiplication of the spectrum becomes an addition.
- The channel changes slowly or not at all over the span used for the mean, and its impulse response is short compared with a frame of 25 ms.
- The span holds enough speech, at least a few seconds, for the mean of the speech to be stable. Over a long span the mean of the speech varies little from utterance to utterance, so subtracting it loses little.
- Additive noise is not the main problem. Noise adds to the power, not to the log, so its effect is not a constant offset of the cepstra.

## The template

For an utterance of frames $c_0, \ldots, c_{T-1}$, each a vector of $D$ cepstral coefficients:

1. Compute the mean $\mu = \frac{1}{T} \sum_{t} c_t$, one value per coefficient.
2. Return $c_t - \mu$ for every frame. This is CMN over the utterance.
3. For mean and variance normalization (CMVN), also compute $\sigma_j^2 = \frac{1}{T} \sum_t (c_{t,j} - \mu_j)^2$ for each coefficient $j$, and return $(c_{t,j} - \mu_j) / \sigma_j$.
4. For a stream, replace $\mu$ by the mean over a window of frames around or before $t$, for example the last 3 to 6 s, or by a running mean $\mu_t = \lambda \mu_{t-1} + (1 - \lambda) c_t$ with $\lambda$ near 0.995.

Always say which form is used: the mean over the utterance needs the whole utterance before the first output; the sliding and running means work online but adapt more slowly to a change of channel.

**Why the channel becomes an offset (approximation).** Let the received signal be $y = g * x$ for a fixed channel $g$. If $g$ is much shorter than the frame, the short-time spectrum satisfies $Y_t(f) \approx G(f) X_t(f)$. If $|G(f)|$ is nearly constant across mel band $m$, with value $G_m$, the band energy is about $|G_m|^2 E_{t,m}$ and its log is $\ln E_{t,m} + 2 \ln |G_m|$. The DCT is linear, so every cepstral vector gets the same added vector $\gamma$, the DCT of $(2 \ln|G_m|)_m$. Then the mean over the frames is $\mu + \gamma$, and $c_t + \gamma - (\mu + \gamma) = c_t - \mu$: the channel is gone. Each "about" in this argument is an approximation, which is why CMN removes a channel only approximately (heuristic).

**What is exact (theorem).** If every frame is changed by the same vector $v$, the output of step 2 is unchanged, and the output of step 3 is unchanged too. The output of step 2 has mean zero in every coefficient, and the output of step 3 also has unit variance in every coefficient that is not constant. Since the DCT is linear, subtracting the mean of the log mel energies and then taking the DCT gives the same result as taking the DCT and then subtracting the mean of the cepstra.

## Classic examples

**A small example.** For four frames of two coefficients, $c = [[1, 0], [3, 2], [2, -1], [2, 3]]$, the mean is $[2, 1]$ and CMN gives $[[-1, -1], [1, 1], [0, -2], [0, 2]]$. The variances are 0.5 and 2.5, so CMVN gives $[[-1.414, -0.632], [1.414, 0.632], [0, -1.265], [0, 1.265]]$. Adding $[5, -3]$ to every frame of $c$ gives exactly the same two results.

**A gain on the signal.** Multiplying the signal by $g$ adds $2\sqrt{26}\ln|g|$ to $c_0$ of 26-filter MFCC and nothing to the others, and CMN removes it exactly as long as no band energy hits the log floor. With $g = 3$ the shift is 11.204.

**Telephone speech.** A telephone channel cuts below about 300 Hz and above about 3.4 kHz. In the bands it cuts, $|G|$ changes fast, and the noise floor dominates, so CMN removes only part of the mismatch between wideband training data and telephone test data.

**Speaker recognition.** Atal used the subtraction of the mean cepstrum in 1974 to make speaker recognition less sensitive to the transmission channel, and it remains a standard step there.

## Variations

- **CMVN.** Also divide by the standard deviation, which reduces the effect of additive noise on the spread of the coefficients.
- **Sliding window.** Subtract the mean of a window of a few seconds, centered or causal. This follows a channel that changes during a long recording.
- **Running mean.** An exponentially weighted mean costs $O(D)$ per frame and needs no buffer. It is a first order high-pass filter on each coefficient, like [RASTA](/rasta-filtering/) without its low-pass part.
- **Per speaker.** Compute the statistics over all utterances of a speaker, which gives a stable mean even for short utterances.
- **Speech frames only.** Compute the mean over the frames that a [voice activity detector](/voice-activity-detection/) marks as speech, so that the mean does not depend on how much silence the recording holds.
- **Histogram equalization.** Map each coefficient so that its whole distribution, not just its mean and variance, matches a reference, for example a standard normal one.

## Pitfalls

- **Short utterances.** Over one second the mean of the speech itself depends strongly on which sounds were said, so CMN removes speech information as well as the channel. Use a per-speaker mean or a prior mean in that case.
- **Silence ratio.** If one recording is mostly silence and another mostly speech, their means differ even on the same channel. Use only the speech frames for the mean.
- **Train and test mismatch.** Apply the same normalization, with the same window and the same frames, to training and test data.
- **Online start.** A sliding or running mean has no good estimate during the first frames. Start from a mean computed on training data.
- **Variance with few frames.** With few frames, or with a constant coefficient, $\sigma_j$ is close to 0 and the division blows up. Use a floor on $\sigma_j$.
- **Not a noise remover.** CMN does not remove additive noise; [spectral subtraction](/spectral-subtraction/) and related methods address it.

## Exercises

1. Show that CMN of the log mel energies followed by the DCT equals the DCT followed by CMN of the cepstra.
2. For the four frames of the example, add $[5, -3]$ to every frame and verify that CMN and CMVN do not change.
3. Write the running mean $\mu_t = \lambda \mu_{t-1} + (1 - \lambda) c_t$ as a filter on each coefficient, and find the transfer function of $c_t - \mu_t$. Where is its zero?
4. Give a channel $g$ with an impulse response much longer than a frame, and explain why $Y_t \approx G X_t$ fails for it.
5. Show that the mean of the delta features over an utterance is not exactly 0 when the edge frames are repeated, and find its value for $\Theta = 1$.

## References
