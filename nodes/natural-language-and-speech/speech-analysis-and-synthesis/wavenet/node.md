---
tag: 0NFQNJ
kind: model
slug: wavenet
name: WaveNet
aliases:
- dilated causal convolution vocoder
area: natural-language-and-speech/speech-analysis-and-synthesis
level: research
summary: "An autoregressive model of raw audio that predicts each mu-law quantized sample from the past with stacks of dilated causal convolutions."
history:
  year: 2016
  people: [Aäron van den Oord, Sander Dieleman, Heiga Zen, Karen Simonyan, Oriol Vinyals, Alex Graves, Nal Kalchbrenner, Andrew Senior, Koray Kavukcuoglu]
  note: "Modeled speech one sample at a time with a convolutional network and beat the best parametric and concatenative systems in listening tests. Later used as the vocoder of Tacotron 2."
prereqs: [discrete-convolution, scalar-quantization, causal-language-modeling]
see_also: [tacotron, hifi-gan, text-to-speech, unit-selection-synthesis, hmm-based-speech-synthesis, cross-entropy-loss, source-filter-model, mean-opinion-score]
sources:
  - paper: "Aäron van den Oord, Sander Dieleman, Heiga Zen, Karen Simonyan, Oriol Vinyals, Alex Graves, Nal Kalchbrenner, Andrew Senior and Koray Kavukcuoglu, WaveNet: A generative model for raw audio, arXiv:1609.03499, 2016"
    title: van den Oord et al. 2016
    locator: "Section 2 (dilated causal convolutions, the softmax over mu-law values, the gated activation, residual and skip connections, and conditioning), Section 3.2 (the text-to-speech experiments) and Table 1 (MOS)"
  - paper: doi:10.1109/ICASSP.2018.8461368
    title: "Jonathan Shen, Ruoming Pang, Ron J. Weiss and colleagues, Natural TTS synthesis by conditioning WaveNet on mel spectrogram predictions, ICASSP 2018"
    locator: "Section 2.3 (WaveNet as a vocoder on mel spectrograms, with a mixture of logistics output)"
---

WaveNet is a probability model of raw audio. It treats a waveform as a sequence of samples and predicts each sample from all the samples before it, like a [causal language model](/causal-language-modeling/) over a vocabulary of 256 amplitude levels. The network is a deep stack of causal convolutions, which see only the past, with dilations that double from layer to layer, so the receptive field grows exponentially with depth at a linear cost. To make speech from text, the model is conditioned on features from a [text-to-speech](/text-to-speech/) front end. In the original paper these were linguistic features and a pitch contour; in [Tacotron 2](/tacotron/) they are mel spectrogram frames, and WaveNet is used as a vocoder. Its listening scores were well above those of the parametric and concatenative systems of its time. Its weak point is speed, because generation makes one sample at a time.

## The machine

Sizes: $N$ samples at 16 kHz, $L$ layers, $C$ residual channels, kernel size $k = 2$, and $Q = 256$ output levels. Shapes are channels by time for one utterance.

**Factorization.** For a waveform $x = (x_1, \ldots, x_N)$ and a conditioning input $h$,

$$p(x \mid h) = \prod_{t=1}^{N} p(x_t \mid x_1, \ldots, x_{t-1}, h).$$

**Mu-law quantization.** Each sample $x_t \in (-1, 1)$ is compressed and then quantized to 256 levels:

$$F(x) = \operatorname{sign}(x)\, \frac{\ln(1 + \mu |x|)}{\ln(1 + \mu)}, \qquad \mu = 255.$$

This gives fine steps near 0, where most speech samples lie, and coarse steps for loud samples. The output for each $t$ is a softmax over the 256 levels, trained with the [cross-entropy loss](/cross-entropy-loss/).

**Dilated causal convolution.** A causal convolution with kernel size $k$ and dilation $r$ computes

$$y_t = \sum_{m=0}^{k-1} W_m\, x_{t - m r},$$

so output $t$ depends only on inputs at or before $t$. The dilations double, $1, 2, 4, \ldots, 512$, and this block of 10 layers is repeated. A stack of layers with dilations $r_1, \ldots, r_L$ has the receptive field

$$R = 1 + (k - 1) \sum_{l=1}^{L} r_l.$$

**Gated residual layer.** Layer $l$ maps its input $u$ of shape $C \times N$ to

$$z = \tanh(W_{f} * u) \odot \sigma(W_{g} * u),$$

where $*$ is the dilated causal convolution and $\sigma$ the logistic function. A $1 \times 1$ convolution of $z$ is added to $u$ to give the input of the next layer (the residual path), and another $1 \times 1$ convolution of $z$ goes to the skip path. The sum of all skip outputs goes through ReLU, $1 \times 1$ convolutions and the softmax, giving shape $256 \times N$.

**Conditioning.** A global input $h$, such as a speaker embedding, enters every layer as $z = \tanh(W_f * u + V_f^\top h) \odot \sigma(W_g * u + V_g^\top h)$. A local input, such as linguistic features or mel frames at a lower rate, is first upsampled to the sample rate by transposed convolutions, $y = f(h)$, and enters as $V_f * y$ and $V_g * y$ with $1 \times 1$ convolutions.

**Standing assumptions.** A fixed sample rate, a fixed quantization, and a fixed receptive field: the model sees no sample older than $R - 1$ steps, except through the conditioning input.

## What it counts

The model gives the probability of a whole waveform as the product of the softmax outputs. In training all $N$ outputs come from one parallel pass over the true waveform. In generation, each sample is drawn from the softmax and fed back as input.

- **Receptive field.** One block with dilations $1, \ldots, 512$ and $k = 2$ has $R = 1 + 1023 = 1024$ samples, 64 ms at 16 kHz. Three blocks give $1 + 3 \cdot 1023 = 3070$ samples. A plain causal stack of the same depth would see only $L + 1$ samples. The text-to-speech models of the paper had a receptive field of 240 ms.
- **Mu-law check values.** $F(0.5) = \ln 128.5 / \ln 256 \approx 0.8757$, $F(0.01) \approx 0.2285$ and $F(-0.25) \approx -0.7521$. With the level $\operatorname{round}((F + 1) / 2 \cdot 255)$, these fall in levels 239, 157 and 32 of 0 to 255. Since $1 + 255 \cdot 15 / 255 = 16 = \sqrt{256}$, $F(15 / 255) = 0.5$ exactly, so half of the levels cover $|x| < 15 / 255 \approx 0.0588$.
- **Cost of generation.** Each sample needs one pass through all $L$ layers, and the passes are sequential: 16000 passes per second of audio at 16 kHz. With caching of the past activations of each layer, a pass costs $O(L C^2)$, so one second costs $O(16000\, L C^2)$ and no step can start before the one before it ends.
- **Cost of training.** All outputs of a training clip are computed in one pass in $O(N L C^2)$, in parallel over time, because the true past samples are known.

## Relation to other models

- **[Causal language models](/causal-language-modeling/)** have the same factorization over tokens. WaveNet uses convolutions in place of attention or recurrence, and its tokens are amplitude levels.
- **PixelCNN** (van den Oord and colleagues 2016) is the image model that WaveNet adapts: masked convolutions and the same gated unit.
- **[Tacotron 2](/tacotron/)** uses a WaveNet as its vocoder, conditioned on mel frames, with a mixture of 10 logistic distributions in place of the 256-way softmax, for 16-bit samples at 24 kHz.
- **[HiFi-GAN](/hifi-gan/)** and other GAN vocoders make all samples in one parallel pass. In the HiFi-GAN paper, a WaveNet vocoder runs at 0.003 times real time on a GPU, against more than 100 times for HiFi-GAN V1.
- **[Unit selection](/unit-selection-synthesis/)** and **[HMM-based synthesis](/hmm-based-speech-synthesis/)** were the baselines it replaced. The parametric baseline used a vocoder based on the [source-filter model](/source-filter-model/); WaveNet learns the waveform with no such model.

## Known results in the model

- **Naturalness (measurement).** In blind tests with 100 held-out sentences, each rated by 8 crowd-sourced subjects on a 1 to 5 scale, WaveNet conditioned on linguistic features and log F0 had a [mean opinion score](/mean-opinion-score/) of 4.21 ± 0.081 in North American English, against 3.67 ± 0.098 for an LSTM parametric system, 3.86 ± 0.137 for an HMM-driven concatenative system and 4.55 ± 0.075 for 16-bit natural speech. In Mandarin Chinese the scores were 4.08 ± 0.085 for WaveNet, 3.79 ± 0.084 for the parametric system and 3.47 ± 0.108 for the concatenative one. The training data was 24.6 hours of English and 34.8 hours of Mandarin, each from one professional female speaker.
- **Exponential receptive field (theorem).** With doubling dilations, the receptive field of $L$ layers of kernel size 2 is $2^L$ samples within one block, by the formula for $R$ above, while the number of weights grows linearly in $L$.
- **Sequential sampling (theorem).** Exact sampling from the factorization needs sample $t - 1$ before the distribution of sample $t$ is known, so it takes $N$ dependent steps whatever the hardware. Parallel vocoders avoid this by changing the model, not the sampling.
- **Conditioning matters (measurement).** Without text conditioning, WaveNet trained on many speakers produced speech-like babble with no words but with a consistent voice for each speaker identity.
