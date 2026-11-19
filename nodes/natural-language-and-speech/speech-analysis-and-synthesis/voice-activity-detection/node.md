---
tag: B7QV94
kind: problem
slug: voice-activity-detection
name: Voice activity detection
aliases:
- VAD
- speech activity detection
- speech detection
area: natural-language-and-speech/speech-analysis-and-synthesis
level: core
summary: Mark which frames of an audio signal contain speech and which contain only silence or noise.
prereqs: [zero-crossing-rate, likelihood-ratio-test]
see_also: [likelihood-ratio-vad, rabiner-sambur-endpoint-detection, neyman-pearson-lemma, hidden-markov-model, spectral-subtraction, speaker-diarization, keyword-spotting, cepstral-mean-normalization]
sources:
  - paper: "Jongseo Sohn, Nam Soo Kim and Wonyong Sung, A statistical model-based voice activity detection, IEEE Signal Processing Letters 6(1), 1999"
    title: Jongseo Sohn, Nam Soo Kim and Wonyong Sung, A statistical model-based voice activity detection
    locator: the frame decision as a likelihood ratio test between noise only and speech plus noise, with Gaussian models of the DFT coefficients
  - paper: doi:10.1002/j.1538-7305.1975.tb02840.x
    title: L. R. Rabiner and M. R. Sambur, An algorithm for determining the endpoints of isolated utterances, The Bell System Technical Journal 54(2), 1975, 297 to 315
    locator: the endpoints of an isolated word from energy and zero-crossing thresholds set on the silence at the start
  - book: isbn:9780132136037
    title: L. R. Rabiner and R. W. Schafer, Digital Processing of Speech Signals, Prentice Hall, 1978
    locator: "Chapter 4 (time domain processing of speech), the discussion of speech and silence discrimination with energy and zero-crossing rate"
---

Voice activity detection asks, for each short frame of an audio signal, whether it contains speech or only silence and noise. It is a decision problem: the [zero-crossing rate](/zero-crossing-rate/) and the frame energy are measurements that detectors use, not detectors themselves. The [Rabiner-Sambur endpoint detector](/rabiner-sambur-endpoint-detection/) solves the narrower task of finding one start and one end of an isolated word, while a [likelihood ratio VAD](/likelihood-ratio-vad/) labels every frame by a statistical test and can find many speech segments.

## In plain words

A recording usually holds speech only part of the time. The rest is pauses, breathing, room noise or traffic. A voice activity detector goes through the recording in small steps of about 10 ms and says "speech" or "no speech" for each step. A phone uses this to send fewer bits when nobody talks, and a speech recognizer uses it to skip the silence. The task is easy when the background is quiet and hard when the noise is loud or sounds like speech, such as music or other people talking. Every detector makes two kinds of mistakes: it can cut off quiet speech, or it can call noise speech, and tuning it trades one mistake for the other.

## Definition

**Input.** A signal $x$ sampled at $f_s$, cut into frames $x_0, \ldots, x_{T-1}$, for example 25 ms frames with a hop of 10 ms. In the batch form all frames are given; in the online form frame $t$ must be labeled after at most $\Delta$ further frames have arrived.

**Output.** A label $v_t \in \{0, 1\}$ for each frame, where 1 means that the frame contains speech.

**Model.** Each frame is one of two hypotheses:

$$H_0: x_t = n_t \qquad \text{or} \qquad H_1: x_t = s_t + n_t,$$

where $n_t$ is noise and $s_t$ is speech. This makes each frame a binary [statistical hypothesis test](/statistical-hypothesis-test/).

**Quality.** Against reference labels $r_t$, the **miss rate** is the fraction of speech frames ($r_t = 1$) labeled 0, which clips speech, and the **false alarm rate** is the fraction of non-speech frames ($r_t = 0$) labeled 1. The frame error rate is the fraction of frames with $v_t \ne r_t$. A detector with a threshold traces a curve of miss rate against false alarm rate as the threshold moves, and the operating point depends on the application.

## Variants

- **Endpoint detection.** Find only the first and the last speech frame of an utterance that holds one word or one command; see the [Rabiner-Sambur endpoint detector](/rabiner-sambur-endpoint-detection/).
- **Online with bounded delay.** Speech coders and telephony need a decision within a few frames. Batch systems, such as preprocessing for [speaker diarization](/speaker-diarization/), can use the whole recording.
- **Segment output.** Many systems output speech segments with a start and an end time, after smoothing the frame labels and removing segments that are too short.
- **More classes.** Some detectors separate speech, music and noise, or detect only the speech of one target speaker.
- **Several microphones.** With a microphone array, the direction of the sound helps to separate a talker from diffuse noise.

## Examples

**A quiet room.** If the background is digital silence, every frame with nonzero energy is speech, and a threshold on the energy solves the problem exactly.

**A word with weak fricatives.** Take the synthetic recording of the [Rabiner-Sambur](/rabiner-sambur-endpoint-detection/) example at 16 kHz with 10 ms frames: 30 frames of low-pass background noise, 10 frames of a weak fricative, 50 frames of a tone, 8 frames of the fricative and 30 frames of background, 128 frames in all, of which frames 30 to 97 are speech. A threshold on the energy at its ITL value finds frames 40 to 89 and misses all 18 fricative frames, a miss rate of $18 / 68 = 26.5$ percent and a frame error rate of $18 / 128 = 14.1$ percent. Adding the zero-crossing test of Rabiner and Sambur finds frames 30 to 97 and gets every frame right.

**Babble noise.** When the noise is other people talking, the noise frames have the same spectral shape as speech, and detectors based on energy or on the spectrum make many errors. This case needs models of the target voice or a trained classifier.

## Known algorithms

- **Energy and zero-crossing thresholds.** Thresholds on the short-time energy and the [zero-crossing rate](/zero-crossing-rate/), set from a stretch of known silence. The [Rabiner-Sambur endpoint detector](/rabiner-sambur-endpoint-detection/) is the classic example, at $O(L)$ time for $L$ samples.
- **Statistical model tests.** Model the DFT coefficients of noise and of speech plus noise as Gaussian, estimate the noise spectrum in non-speech frames, and compare the likelihood ratio of each frame with a threshold. The [likelihood ratio VAD](/likelihood-ratio-vad/) of Sohn, Kim and Sung (1999) is this approach, with a hidden Markov smoothing of the decisions.
- **Spectral features.** Thresholds on the spectral entropy, the spectral flatness, or the long-term spectral divergence from a noise estimate.
- **Trained classifiers.** Gaussian mixture models on subband energies, or neural networks on log mel energies, trained on labeled speech and noise. These work best on realistic noise, at the cost of training data.
- **Smoothing.** Nearly every detector adds a hangover, which keeps the speech label for a few frames after the evidence drops, so that weak word endings are not cut, and removes speech segments shorter than a minimum length.

## Bounds

- **Optimal frame test (theorem).** If the densities $p(x_t \mid H_0)$ and $p(x_t \mid H_1)$ are known, the [Neyman-Pearson lemma](/neyman-pearson-lemma/) shows that a threshold on the likelihood ratio $p(x_t \mid H_1) / p(x_t \mid H_0)$ has the smallest miss rate among all frame tests with the same false alarm rate. Every practical detector approximates these densities, and its errors are at least those of this test.
- **Errors do not vanish at low SNR (theorem).** When speech is weak compared with the noise, the two densities overlap, and the Bayes error of any frame test is bounded below by a positive number that depends only on the overlap of the two densities. Using several frames together, as hangover and HMM smoothing do, lowers the error because speech segments last many frames.
- **Time.** Any detector must read every sample, so it needs $\Omega(L)$ time. Energy detectors run in $O(L)$, and spectral detectors in $O(L \log N)$ with frames of $N$ samples and a fixed overlap.
- **Delay.** An online detector with a delay of $\Delta$ frames can use only the frames up to $t + \Delta$. The hangover, and any look-ahead for weak onsets, cost delay.

## Reductions

- **To hypothesis testing.** Each frame decision is a binary test between noise only and speech plus noise, as in the definition.
- **To sequence decoding.** With a two-state hidden Markov model, one state for speech and one for non-speech, the best label sequence is the [HMM decoding](/hmm-decoding/) of the frame likelihoods, and the transition probabilities give the hangover in a principled way.
- **Endpoint detection from VAD.** Given frame labels, the first and the last speech frame after smoothing solve endpoint detection, so endpoint detection is no harder than VAD.
- **To change-point detection.** The boundaries between speech and non-speech are change points of the frame statistics; see [change-point detection](/change-point-detection/).

## Applications

- **Speech coding.** Telephone codecs send few or no bits in non-speech frames and let the receiver play comfort noise, which saves bandwidth and power.
- **Speech recognition.** Recognizers skip non-speech frames, cut long recordings into utterances, and compute [cepstral mean normalization](/cepstral-mean-normalization/) over speech frames only.
- **Noise estimation.** Noise reduction such as [spectral subtraction](/spectral-subtraction/) updates its noise spectrum in the frames that the detector marks as non-speech.
- **Speaker diarization and keyword spotting.** [Speaker diarization](/speaker-diarization/) uses VAD to find the regions to cluster, and [keyword spotting](/keyword-spotting/) uses it to wake the larger model only when someone speaks.

## References
