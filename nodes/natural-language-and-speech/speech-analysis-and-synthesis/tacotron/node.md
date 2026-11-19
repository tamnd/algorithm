---
tag: 2HQKP5
kind: model
slug: tacotron
name: Tacotron
aliases:
- Tacotron 2
area: natural-language-and-speech/speech-analysis-and-synthesis
level: research
summary: "An attention-based encoder-decoder that maps characters or phonemes to mel spectrogram frames, one step at a time, followed by a vocoder."
history:
  year: 2017
  people: [Yuxuan Wang, RJ Skerry-Ryan, Daisy Stanton, Yonghui Wu, Ron J. Weiss, Navdeep Jaitly, Zongheng Yang, Samy Bengio, Quoc Le, Rif A. Saurous]
  note: "Trained a single network from characters to spectrogram frames, with Griffin-Lim to make the waveform. Tacotron 2 (Shen and colleagues 2018) changed the network and used a WaveNet vocoder."
prereqs: [text-to-speech, encoder-decoder-model, additive-attention]
see_also: [wavenet, griffin-lim-algorithm, fastspeech, hifi-gan, vits, mel-filter-bank, teacher-forcing, mean-opinion-score]
sources:
  - paper: "Yuxuan Wang, RJ Skerry-Ryan, Daisy Stanton, Yonghui Wu, Ron J. Weiss, Navdeep Jaitly, Zongheng Yang, Ying Xiao, Zhifeng Chen, Samy Bengio, Quoc Le, Yannis Agiomyrgiannakis, Rob Clark and Rif A. Saurous, Tacotron: Towards end-to-end speech synthesis, Proceedings of Interspeech 2017, pages 4006 to 4010, arXiv:1703.10135"
    title: Wang et al. 2017
    locator: "Section 3 (the CBHG module, the encoder, the decoder, the post-processing net and Griffin-Lim), Table 1 (the hyper-parameters) and the MOS table"
  - paper: doi:10.1109/ICASSP.2018.8461368
    title: "Jonathan Shen, Ruoming Pang, Ron J. Weiss and colleagues, Natural TTS synthesis by conditioning WaveNet on mel spectrogram predictions, ICASSP 2018, arXiv:1712.05884"
    locator: "Section 2 (the mel spectrogram, the encoder, the location-sensitive attention, the decoder, the post-net and the WaveNet vocoder) and Table 1 (MOS)"
  - book: isbn:9780521899277
    title: "Paul Taylor, Text-to-Speech Synthesis, Cambridge University Press, 2009"
    locator: "Chapter 3 (The text-to-speech problem), for the front end and back end that Tacotron replaces with one network"
---

Tacotron is a [text-to-speech](/text-to-speech/) model that maps a sequence of characters, or phonemes, to a sequence of spectrogram frames. It is an [encoder-decoder model](/encoder-decoder-model/) with attention, the same design as neural machine translation. The encoder reads the text once. The decoder is a recurrent network that makes the frames one step at a time, and at each step an attention layer chooses which part of the text to read. The first Tacotron (Wang and colleagues 2017) predicted mel frames, turned them into a linear spectrogram, and made the waveform with the [Griffin-Lim algorithm](/griffin-lim-algorithm/). Tacotron 2 (Shen and colleagues 2018) predicts mel frames only and makes the waveform with a [WaveNet](/wavenet/) vocoder. Both learn the alignment between text and sound from pairs of text and audio, with no hand-made durations.

## The machine

Sizes: $n$ input symbols, $T$ output frames, $M = 80$ mel bands, frames of 50 ms with a hop of 12.5 ms, and audio at 24 kHz. Shapes are for one utterance. The description is of Tacotron 2; the first version follows.

**Mel spectrogram.** The target is the [short-time Fourier transform](/short-time-fourier-transform/) magnitude with a Hann window, passed through an 80-band [mel filter bank](/mel-filter-bank/) from 125 Hz to 7.6 kHz, clipped below at 0.01 and log-compressed. It has shape $T \times 80$.

**Encoder.** The characters go through a learned embedding of size 512, three 1-D convolutions with 512 filters of width 5, batch normalization and ReLU, and one bidirectional LSTM with 256 units in each direction. The output $h$ has shape $n \times 512$.

**Attention.** Location-sensitive attention is [additive attention](/additive-attention/) that also sees where it looked before. At decoder step $t$, with the decoder state $s_{t-1}$ and the sum $\bar\alpha_{t-1}$ of all earlier attention weights, a vector of shape $n$,

$$f = F * \bar\alpha_{t-1}, \qquad e_{t,i} = w^\top \tanh(W s_{t-1} + V h_i + U f_i + b), \qquad \alpha_t = \operatorname{softmax}(e_t).$$

$F$ is 32 filters of length 31, so $f$ has shape $n \times 32$, and the hidden size of the score is 128. The context vector is $c_t = \sum_i \alpha_{t,i} h_i$, of shape 512. The location term pushes the attention to move forward through the text.

**Decoder.** The previous frame goes through a pre-net of two layers of 256 ReLU units with dropout 0.5, which is kept on at synthesis time. Its output and $c_t$ feed two LSTM layers of 1024 units. A linear map of the LSTM output and $c_t$ gives the next frame, of shape 80, and a second linear map with a sigmoid gives the probability that the utterance has ended. Generation stops at the first frame where that probability is above 0.5. One frame is made per step.

**Post-net.** Five 1-D convolutions with 512 filters of width 5 and tanh read the whole predicted mel spectrogram and add a residual to it, which corrects details using frames on both sides.

**Training.** The loss is the summed squared error of the frames before and after the post-net, plus the stop token loss. During training the decoder gets the true previous frame ([teacher forcing](/teacher-forcing/)).

**Vocoder.** A WaveNet of 30 dilated convolution layers in 3 cycles is trained on the predicted mel spectrograms. Its output is a mixture of 10 logistic distributions for each 16-bit sample.

**The first Tacotron.** It used a character embedding of size 256 and the CBHG module: a bank of 1-D convolutions of widths 1 to 16, max pooling, projections, a highway network and a bidirectional GRU. The decoder had a GRU attention layer with content-based tanh attention and two residual GRU layers of 256 cells, and it emitted $r = 2$ frames per step. A second CBHG module mapped the 80-band mel output to a linear magnitude spectrogram, and Griffin-Lim made the waveform from the magnitudes raised to the power 1.2. The paper reports that Griffin-Lim converges by 50 iterations.

**Standing assumptions.** Normalized text (numbers and abbreviations written out), one speaker or a speaker embedding, and an attention that moves forward through the text.

## What it counts

The decoder defines a sequence of frames $y_1, \ldots, y_T$ by $y_t = g(y_{t-1}, s_{t-1}, c_t)$. It is trained as a regression, so it gives one output, close to the mean of the training frames for a context; it is not a probability model of the frames.

- **Steps.** Synthesis takes $T$ sequential decoder steps, or $T / r$ for the first version. One second of audio at a hop of 12.5 ms is 80 frames, so 80 steps.
- **Attention cost.** Each step scores all $n$ encoder outputs, so the attention costs $\Theta(n T)$ over the utterance, and the location convolution adds $\Theta(n \cdot 32 \cdot 31)$ per step.
- **Vocoder cost.** The WaveNet vocoder of Tacotron 2 is autoregressive over samples: 24000 sequential steps per second of audio. This, not the mel decoder, is the slow part.
- **Example of the location features.** With $n = 4$ and earlier weights $\bar\alpha = (1, 0.8, 0.2, 0)$, a filter that weighs the next position, $f_i = \bar\alpha_{i-1}$, gives $f = (0, 1, 0.8, 0.2)$. The score can use it to favor positions just after the ones already read.

## Relation to other models

- **[Encoder-decoder models](/encoder-decoder-model/) with attention** for translation are the template. The differences are a continuous output with a regression loss, a stop token in place of an end symbol, and the location term in the attention.
- **[FastSpeech](/fastspeech/)** replaces the attention and the step-by-step decoder by explicit durations and a parallel decoder. Its first version took the durations from the attention of an autoregressive teacher.
- **[VITS](/vits/)** finds a hard monotonic alignment by dynamic programming in place of soft attention, and makes the waveform in the same network.
- **[WaveNet](/wavenet/)** in its first form was conditioned on linguistic features from a classic front end. Tacotron 2 conditions it on predicted mel frames, which removes the hand-made front end apart from text normalization.
- **[HiFi-GAN](/hifi-gan/)** and other parallel vocoders can replace WaveNet behind the same mel output; the VITS paper uses this pairing as a baseline.

## Known results in the model

- **Tacotron quality (measurement).** On 100 unseen phrases, each rated 8 times by crowd-sourced native speakers on a 1 to 5 scale, the first Tacotron had a [mean opinion score](/mean-opinion-score/) of 3.82 ± 0.085, against 3.69 ± 0.109 for an LSTM parametric system and 4.09 ± 0.119 for a concatenative system. The training data was about 24.6 hours of one female speaker of North American English.
- **Tacotron 2 quality (measurement).** On 100 test examples with at least 8 ratings each, Tacotron 2 had a MOS of 4.526 ± 0.066 (95% confidence interval) against 4.582 ± 0.053 for the recordings, 4.341 ± 0.051 for WaveNet with linguistic features, 4.166 ± 0.091 for concatenative synthesis and 4.001 ± 0.087 for Tacotron with Griffin-Lim.
- **Attention failures (observation).** Soft attention can skip, repeat or stop early on long or unusual inputs, because nothing forces it to be monotonic. The location term reduces this. Later models make the alignment monotonic by construction, with durations or a dynamic program.
- **Regression to the mean (observation).** A squared error loss on frames gives smooth, averaged spectra. The post-net and the neural vocoder restore much of the detail, but the model cannot sample different prosodies for one text, apart from the variation that pre-net dropout gives.
