---
tag: AM4AFG
kind: model
slug: fastspeech
name: "FastSpeech"
aliases:
- FastSpeech 2
area: natural-language-and-speech/speech-analysis-and-synthesis
level: research
summary: "A non-autoregressive transformer TTS model that repeats each phoneme encoding by its predicted duration and outputs all mel frames in parallel."
history:
  year: 2019
  people: [Yi Ren, Yangjun Ruan, Xu Tan, Tao Qin, Sheng Zhao, Zhou Zhao, Tie-Yan Liu]
  note: "Replaced the attention of autoregressive TTS by a length regulator with durations taken from a teacher model. FastSpeech 2 (2021) trained on real mel frames with forced-aligned durations and added pitch and energy."
prereqs: [text-to-speech, transformer, knowledge-distillation]
see_also: [tacotron, vits, hifi-gan, wavenet, forced-alignment, hidden-semi-markov-model, hmm-based-speech-synthesis, mean-opinion-score]
sources:
  - paper: "Yi Ren, Yangjun Ruan, Xu Tan, Tao Qin, Sheng Zhao, Zhou Zhao and Tie-Yan Liu, FastSpeech: Fast, robust and controllable text to speech, Advances in Neural Information Processing Systems 32 (NeurIPS 2019), arXiv:1905.09263"
    title: Ren et al. 2019
    locator: "Section 3 (the feed-forward transformer, the length regulator and the duration predictor), Section 4 (the setup on LJ Speech), and the tables of MOS, speed and robustness"
  - paper: "Yi Ren, Chenxu Hu, Xu Tan, Tao Qin, Sheng Zhao, Zhou Zhao and Tie-Yan Liu, FastSpeech 2: Fast and high-quality end-to-end text to speech, ICLR 2021, arXiv:2006.04558"
    title: Ren et al. 2021
    locator: "Section 2 (the variance adaptor, the pitch and energy predictors, and FastSpeech 2s) and the tables of MOS and training and inference time"
---

FastSpeech is a [text-to-speech](/text-to-speech/) model that makes all mel spectrogram frames of an utterance at once. Models such as [Tacotron](/tacotron/) make one frame per step and use soft attention to find where they are in the text; this is slow, and the attention can skip or repeat words. FastSpeech removes the attention. A [transformer](/transformer/) style encoder turns each phoneme into a vector. A duration predictor says how many frames each phoneme lasts. The length regulator repeats each phoneme vector that many times, and a second transformer stack turns the expanded sequence into mel frames in parallel. A vocoder, WaveGlow in the paper, makes the waveform. The first FastSpeech learned its durations and its targets from an autoregressive teacher. FastSpeech 2 uses durations from a [forced aligner](/forced-alignment/), trains on the real mel frames, and also predicts pitch and energy.

## The machine

Sizes: $n$ phonemes, $T$ mel frames, $M = 80$ mel bands, model width $d = 384$, $h = 2$ heads, and a hop of 256 samples at 22.05 kHz. Shapes are for one utterance.

**Feed-forward transformer (FFT) block.** A block is multi-head self-attention followed by a two-layer 1-D convolution network in place of the position-wise feedforward layer, each with a residual connection, [layer normalization](/layer-normalization/) and dropout. The convolutions have kernel size 3 and map $384 \to 1536 \to 384$ with a ReLU. A block maps shape $L \times d$ to $L \times d$.

**Encoder.** A phoneme embedding plus a positional encoding, then 6 FFT blocks, give $H_{\text{pho}}$ of shape $n \times d$.

**Length regulator.** Given integer durations $D = (d_1, \ldots, d_n)$ with $\sum_i d_i = T$, it repeats row $i$ of $H_{\text{pho}}$ exactly $d_i$ times:

$$H_{\text{mel}} = \mathrm{LR}(H_{\text{pho}}, D, \alpha), \qquad \text{shape } T' \times d, \quad T' = \sum_i \operatorname{round}(\alpha\, d_i).$$

The factor $\alpha$ sets the speaking rate: $\alpha > 1$ is slower and $\alpha < 1$ faster. Lengthening or shortening one phoneme, or the pauses, gives local control.

**Decoder.** A positional encoding on $H_{\text{mel}}$, 6 FFT blocks and a linear map to $M$ give the mel spectrogram of shape $T' \times 80$.

**Duration predictor.** Two 1-D convolutions with ReLU, each followed by layer normalization and dropout, and a linear map to one number per phoneme. It reads $H_{\text{pho}}$ and predicts $\log d_i$, trained with the squared error. At synthesis time the prediction is rounded to a positive integer.

**Teacher, durations and targets (FastSpeech).** An autoregressive Transformer TTS model is trained first. For each of its attention heads, the focus rate $F = \frac{1}{S} \sum_{s=1}^{S} \max_{t} a_{s,t}$ measures how diagonal the alignment is, over the $S$ mel frames and the text positions $t$. The head with the largest $F$ is used, and $d_i$ is the number of frames whose largest attention weight is on phoneme $i$. The teacher also generates the mel targets for the training texts, a form of sequence-level [knowledge distillation](/knowledge-distillation/), which gives simpler targets than the recordings.

**Variance adaptor (FastSpeech 2).** FastSpeech 2 drops the teacher. Durations come from the Montreal Forced Aligner, and the targets are the real mel frames. After the length regulator it adds a pitch predictor and an energy predictor, with the same layout as the duration predictor. The pitch contour is decomposed by a continuous wavelet transform into 10 scales and the predictor outputs that pitch spectrogram. Pitch is quantized into 256 values on a log scale and energy, the L2 norm of each STFT frame, into 256 uniform values; the embedding of each quantized value is added to the hidden sequence. Training uses the true pitch, energy and durations, and synthesis uses the predicted ones. FastSpeech 2s also makes the waveform directly from the hidden sequence, with an adversarially trained waveform decoder.

**Standing assumptions.** A phoneme input from a G2P front end, a monotonic alignment in which every frame belongs to exactly one phoneme, and integer durations.

## What it counts

The network is a deterministic map from phonemes and durations to mel frames. Given the durations, frame $j$ of the decoder input is the encoding of phoneme $a(j)$, where $a$ is the monotonic alignment that the durations define.

- **Example of the length regulator.** With $D = (2, 4, 6)$ and $\alpha = 1$, the expanded sequence is $h_1 h_1\, h_2 h_2 h_2 h_2\, h_3 h_3 h_3 h_3 h_3 h_3$, with 12 rows. With $\alpha = 0.5$ the durations are $(1, 2, 3)$ and there are 6 rows. With $\alpha = 1.3$ they are $\operatorname{round}(2.6, 5.2, 7.8) = (3, 5, 8)$ and there are 16 rows.
- **Cost.** Self-attention in the decoder costs $\Theta(T^2 d)$ and the convolutions $\Theta(T d^2)$, but all frames are computed at once. The number of sequential steps does not grow with $T$, against $T$ steps for an autoregressive decoder.
- **No skipping.** Every phoneme with $d_i \ge 1$ appears in the output, and in order, so the model cannot skip or repeat a word as attention can. It can still give a wrong duration.

## Relation to other models

- **[Tacotron](/tacotron/)** and Transformer TTS are autoregressive with soft attention. FastSpeech keeps the transformer layers and replaces the attention between text and frames by explicit durations.
- **[HMM-based speech synthesis](/hmm-based-speech-synthesis/)** also predicted a duration for each state and expanded the states to frames. The length regulator is the same idea with learned vectors in place of Gaussian states, and the expanded sequence is a [hidden semi-Markov](/hidden-semi-markov-model/) style segmentation.
- **[VITS](/vits/)** learns its durations without a teacher or an aligner, by monotonic alignment search during training, and samples them from a stochastic predictor.
- **[HiFi-GAN](/hifi-gan/)** and other parallel vocoders complete a fully parallel system. FastSpeech 2s goes further and makes the waveform itself.

## Known results in the model

- **Speed (measurement).** On one V100 GPU with batch size 1 and mel outputs of about 560 frames, FastSpeech generated mel spectrograms in 0.025 s against 6.735 s for the Transformer TTS teacher, 269.40 times faster, and was 38.30 times faster end to end with the WaveGlow vocoder.
- **Quality (measurement).** On LJ Speech with WaveGlow, FastSpeech had a [mean opinion score](/mean-opinion-score/) of 3.84 ± 0.08 (95% confidence interval, 1 to 5 scale), against 3.88 ± 0.09 for Transformer TTS, 3.86 ± 0.09 for Tacotron 2 and 4.41 ± 0.08 for the recordings.
- **Robustness (measurement).** On 50 hard sentences, Tacotron 2 had 4 repeated and 11 skipped words, with errors in 24% of the sentences, and Transformer TTS 34%. FastSpeech had no repeats or skips.
- **FastSpeech 2 (measurement).** With a Parallel WaveGAN vocoder, FastSpeech 2 had a MOS of 3.83 ± 0.08 against 3.68 ± 0.09 for FastSpeech and 4.30 ± 0.07 for the recordings, in a different test from the one above, so the two sets of numbers are not comparable. Its acoustic model trained in 17.02 hours against 53.12 hours for FastSpeech. The forced aligner gave phoneme boundaries with a mean error of 12.47 ms against 19.68 ms for the teacher attention.
