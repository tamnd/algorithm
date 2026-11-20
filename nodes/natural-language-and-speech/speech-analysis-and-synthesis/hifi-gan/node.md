---
tag: EWV61N
kind: model
slug: hifi-gan
name: "HiFi-GAN"
aliases:
- HiFi-GAN vocoder
area: natural-language-and-speech/speech-analysis-and-synthesis
level: research
summary: "A GAN vocoder that turns mel spectrograms into waveforms with a convolutional generator, judged by multi-period and multi-scale discriminators."
history:
  year: 2020
  people: [Jungil Kong, Jaehyeon Kim, Jaekyoung Bae]
  note: "Added the multi-period discriminator to the multi-scale discriminator of MelGAN, and matched the quality of autoregressive vocoders at a far higher speed."
prereqs: [mel-filter-bank, discrete-convolution, short-time-fourier-transform]
see_also: [wavenet, vits, tacotron, fastspeech, griffin-lim-algorithm, text-to-speech, weight-normalization, spectral-normalization]
sources:
  - paper: "Jungil Kong, Jaehyeon Kim and Jaekyoung Bae, HiFi-GAN: Generative adversarial networks for efficient and high fidelity speech synthesis, Advances in Neural Information Processing Systems 33 (NeurIPS 2020), arXiv:2010.05646"
    title: Kong, Kim and Bae 2020
    locator: "Section 2 (the generator, the multi-receptive field fusion, the multi-period and multi-scale discriminators and the losses), Table 1 (MOS, speed and size on LJ Speech), the ablation table, the unseen speaker test on VCTK, and the appendix with the V1, V2 and V3 settings"
  - book: isbn:9780521899277
    title: "Paul Taylor, Text-to-Speech Synthesis, Cambridge University Press, 2009"
    locator: "Chapter 12 (Analysis of speech signals), for the spectrogram that the vocoder inverts"
---

HiFi-GAN is a neural vocoder: it turns a mel spectrogram into a waveform. It is the second stage of most two-stage [text-to-speech](/text-to-speech/) systems, after an acoustic model such as [Tacotron 2](/tacotron/) or [FastSpeech](/fastspeech/), and it is the decoder inside [VITS](/vits/). The generator is a stack of transposed convolutions that raise the frame rate to the sample rate, each followed by residual blocks with dilated convolutions. It runs on all samples in parallel, unlike [WaveNet](/wavenet/), which makes one sample at a time. The generator is trained as a generative adversarial network: two sets of discriminators judge the waveform, one by looking at samples spaced by a fixed period and one at several time scales. A mel spectrogram loss and a feature matching loss keep the output close to the target.

## The machine

Sizes: $T$ mel frames with $M = 80$ bands, hop $H = 256$ samples at 22.05 kHz, and $N = T H$ output samples. Shapes are written as channels by length for one utterance.

**Generator $G$.** A convolution maps the input $s$ of shape $M \times T$ to $h_u \times T$ ($h_u = 512$ in the V1 setting). Then four upsampling stages run in turn. Stage $k$ is a transposed convolution with stride $u_k$ and kernel size $2 u_k$ that halves the channels and multiplies the length by $u_k$, with $(u_1, u_2, u_3, u_4) = (8, 8, 2, 2)$ and $8 \cdot 8 \cdot 2 \cdot 2 = 256 = H$. After stage 4 the tensor has shape $32 \times N$. A final convolution and $\tanh$ give one channel of $N$ samples in $[-1, 1]$.

**Multi-receptive field fusion (MRF).** After each transposed convolution, three residual blocks with kernel sizes $3, 7, 11$ read the same input, and their outputs are averaged. In V1 each block has three pairs of dilated convolutions with dilations $1, 3, 5$, each pair with a leaky ReLU before each convolution and a residual sum. The blocks see patterns of different lengths in parallel. All convolutions of $G$ use [weight normalization](/weight-normalization/).

**Multi-period discriminator (MPD).** For each period $p \in \{2, 3, 5, 7, 11\}$, a sub-discriminator pads the waveform of length $N$ to a multiple of $p$ and reshapes it to a 2-D array of shape $(N / p) \times p$, so that column $r$ holds the samples $r, r + p, r + 2p, \ldots$. Convolutions with kernels of width 1 along the period axis then look at each column alone, at strides of $p$ samples. The periods are prime so that the sub-discriminators see different structure.

**Multi-scale discriminator (MSD).** Three sub-discriminators, taken from MelGAN, look at the raw waveform, the waveform average-pooled by 2, and the waveform average-pooled by 4, with 1-D grouped convolutions. The first uses [spectral normalization](/spectral-normalization/) and the others weight normalization.

**Losses.** With the least squares GAN form, for each sub-discriminator $D_k$, a real waveform $x$ and its mel spectrogram $s$:

$$L_{\text{adv}}(D_k) = \mathbb{E}\bigl[(D_k(x) - 1)^2 + D_k(G(s))^2\bigr], \qquad L_{\text{adv}}(G; D_k) = \mathbb{E}\bigl[(D_k(G(s)) - 1)^2\bigr].$$

The mel loss is $L_{\text{mel}} = \| \phi(x) - \phi(G(s)) \|_1$, where $\phi$ is the log mel spectrogram. The feature matching loss $L_{\text{fm}}$ is the L1 distance between the inner feature maps of each discriminator on $x$ and on $G(s)$, divided by their sizes. The generator minimizes

$$L_G = \sum_k \bigl( L_{\text{adv}}(G; D_k) + 2\, L_{\text{fm}}(G; D_k) \bigr) + 45\, L_{\text{mel}},$$

and each discriminator minimizes $L_{\text{adv}}(D_k)$. Both are trained with [AdamW](/adamw/), with $\beta_1 = 0.8$, $\beta_2 = 0.99$ and a learning rate of $2 \cdot 10^{-4}$ that decays by a factor of 0.999 each epoch.

**Standing assumptions.** A fixed sample rate and a fixed mel analysis (window, hop and bands) that the vocoder and the acoustic model share. The vocoder is trained on mel spectrograms of real speech and often fine-tuned on the outputs of the acoustic model.

## What it counts

The generator is a deterministic function from a mel spectrogram of shape $M \times T$ to a waveform of $T H$ samples. It has no noise input. The discriminators exist only for training.

- **Lengths.** Each mel frame becomes exactly $H$ samples. For example, 3 s at 22050 Hz is 66150 samples, about 258 frames at a hop of 256.
- **Cost of one pass.** Every layer is a convolution over the whole sequence, so the cost is linear in $N$ and all positions are computed in parallel. The arithmetic of a stage grows with its length times the square of its channel count. In the V1 setting (upsampling by 8, 8, 2 and 2, channels 256, 128, 64 and 32) that is 0.52M, 1.05M, 0.52M and 0.26M multiply-adds per layer, kernel tap and mel frame, so the second stage costs most and the last stage least.
- **Size.** The paper gives three settings: V1 for quality, and V2 and V3 with fewer channels or fewer blocks for speed.
- **Period view.** For period $p$ the reshaped array has $\lceil N / p \rceil$ rows. With $N = 66150$ and $p = 11$ the waveform is padded to 66154 samples and gives 6014 rows of 11 columns.

## Relation to other models

- **[WaveNet](/wavenet/)** models each sample given the past and must run $N$ steps one after the other. HiFi-GAN makes all samples in one parallel pass.
- **MelGAN** (Kumar and colleagues 2019) is the direct parent: a GAN vocoder with the same kind of transposed convolution generator and the multi-scale discriminator. HiFi-GAN adds the MPD, the MRF blocks and the mel loss.
- **[Griffin-Lim](/griffin-lim-algorithm/)** reconstructs a phase from a magnitude spectrogram by iteration and needs no training. It was the vocoder of the first [Tacotron](/tacotron/); its output has audible artifacts that neural vocoders avoid.
- **[VITS](/vits/)** uses the V1 generator as its decoder, with a latent sequence in place of the mel spectrogram, and the MPD as its discriminator.

## Known results in the model

- **Quality (measurement).** On LJ Speech, the paper reports a [mean opinion score](/mean-opinion-score/) of 4.36 ± 0.07 for V1, on a 1 to 5 scale, against 4.45 ± 0.06 for the recorded speech, 4.02 ± 0.08 for a WaveNet vocoder, 3.81 ± 0.08 for WaveGlow and 3.79 ± 0.09 for MelGAN. V2 has 4.23 ± 0.07 and V3 4.05 ± 0.08.
- **Speed (measurement).** On the GPU of the paper, V1 generates 167.86 times faster than real time and V3 1186.80 times. On a CPU, V1 runs at 1.43 times real time and V3 at 13.44 times. The WaveNet vocoder in the same table runs at 0.003 times real time on the GPU. V1 has 13.92 million weights, V2 0.92 million and V3 1.46 million.
- **The period view matters (measurement).** In the ablation with the V3 generator, the full model has a MOS of 4.10 ± 0.05. Without the MPD it falls to 2.28 ± 0.09, without the mel loss to 3.25 ± 0.05, without the MSD to 3.74 ± 0.05 and without the MRF to 3.92 ± 0.05. Periods 2, 4, 8, 16 and 32 in place of the primes give 3.90 ± 0.05.
- **Unseen speakers (measurement).** Trained on the VCTK corpus with nine speakers held out, V1 has a MOS of 3.77 ± 0.07 on the held-out speakers against 3.79 ± 0.07 for the recordings, with 50 utterances per speaker. So a mel spectrogram carries most of what the vocoder needs.
