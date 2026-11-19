---
tag: HW04HE
kind: model
slug: vits
name: VITS
aliases:
- variational inference text-to-speech
area: natural-language-and-speech/speech-analysis-and-synthesis
level: research
summary: "End-to-end TTS that joins a conditional VAE, a normalizing flow and adversarial training, and finds durations by monotonic alignment search."
history:
  year: 2021
  people: [Jaehyeon Kim, Jungil Kong, Juhee Son]
  note: "Joined the prior of Glow-TTS, its monotonic alignment search and the HiFi-GAN generator into one model trained from text and audio, with no separate vocoder."
prereqs: [variational-autoencoder, hifi-gan, evidence-lower-bound]
see_also: [text-to-speech, fastspeech, tacotron, dynamic-time-warping, forced-alignment, viterbi-algorithm, kullback-leibler-divergence, transformer]
sources:
  - paper: "Jaehyeon Kim, Jungil Kong and Juhee Son, Conditional variational autoencoder with adversarial learning for end-to-end text-to-speech, Proceedings of ICML 2021, PMLR 139, pages 5530 to 5540, arXiv:2106.06103"
    title: Kim, Kong and Son 2021
    locator: "Section 2 (the variational inference, the alignment estimation, the adversarial training and the final loss), the MOS table on LJ Speech, the synthesis speed table, and Figure 2 (the lengths of sampled utterances)"
  - paper: "Jaehyeon Kim, Sungwon Kim, Jungil Kong and Sungroh Yoon, Glow-TTS: A generative flow for text-to-speech via monotonic alignment search, Advances in Neural Information Processing Systems 33 (NeurIPS 2020), pages 8067 to 8077, arXiv:2005.11129"
    title: Kim, Kim, Kong and Yoon 2020
    locator: "Section 3 (the monotonic alignment search and its recursion)"
  - paper: "Jungil Kong, Jaehyeon Kim and Jaekyoung Bae, HiFi-GAN: Generative adversarial networks for efficient and high fidelity speech synthesis, Advances in Neural Information Processing Systems 33 (NeurIPS 2020), arXiv:2010.05646"
    title: Kong, Kim and Bae 2020
    locator: the generator and the multi-period discriminator, which VITS reuses
---

VITS is a [text-to-speech](/text-to-speech/) model that goes from a phoneme sequence straight to a waveform in one network, trained end to end. It is a [variational autoencoder](/variational-autoencoder/) whose latent variable $z$ is a sequence of frames. A posterior encoder reads the linear spectrogram of the training audio and gives $z$. A decoder, the [HiFi-GAN](/hifi-gan/) generator, turns $z$ back into a waveform and is trained with a discriminator. A prior encoder reads the text and gives a normal distribution for each phoneme; a normalizing flow makes the prior more flexible. The link between phonemes and frames is not known, so during training the model finds it with monotonic alignment search, a [Viterbi](/viterbi-algorithm/) style dynamic program from Glow-TTS. A separate duration predictor learns the frame counts that this search finds, and at synthesis time it replaces the search.

## The machine

Sizes: $n$ phonemes, $T$ latent frames, $d$ latent channels (192 in the paper), $F$ linear spectrogram bins, hop $H$ samples per frame, and a waveform of $T H$ samples. Shapes are written for one utterance.

**Posterior encoder.** The linear spectrogram $x_{\text{lin}}$ of shape $T \times F$ (FFT size 1024, hop 256) goes through 16 non-causal WaveNet style residual blocks and gives a mean and a log standard deviation of shape $T \times d$. A sample is $z = \mu_q + \sigma_q \odot \epsilon$, with $\epsilon$ standard normal of shape $T \times d$, so $q(z \mid x)$ is a diagonal normal.

**Decoder.** The HiFi-GAN V1 generator maps $z$ of shape $T \times d$ to a waveform of $T H$ samples. To save memory it is trained on random windows of 32 frames of $z$ and the matching stretch of audio, not on the whole utterance.

**Prior encoder.** A [transformer](/transformer/) encoder with relative positions reads the phonemes $c$, with a blank token between each pair of phonemes, and gives $\mu_\theta$ and $\sigma_\theta$ of shape $n \times d$. An invertible flow $f_\theta$ of affine coupling layers, of shape $T \times d$ to $T \times d$ with Jacobian determinant 1, maps $z$ to $f_\theta(z)$. With an alignment $A$ that sends frame $j$ to phoneme $a(j)$, the prior density is

$$p_\theta(z \mid c, A) = \mathcal{N}\bigl(f_\theta(z);\, \mu_\theta[a],\, \sigma_\theta[a]\bigr)\, \Bigl|\det \frac{\partial f_\theta(z)}{\partial z}\Bigr|,$$

where $\mu_\theta[a]$ repeats row $a(j)$ for frame $j$.

**Monotonic alignment search.** An alignment is monotonic and onto: $a(0) = 0$, $a(T - 1) = n - 1$ and $a(j + 1) - a(j) \in \{0, 1\}$. With $v_{i,j} = \log \mathcal{N}(f_\theta(z)_j; \mu_{\theta,i}, \sigma_{\theta,i})$, a matrix of shape $n \times T$, the search picks the alignment of largest $\sum_j v_{a(j), j}$. It is a dynamic program in the Viterbi semiring (max, +):

```pseudo id=main
MONOTONIC-ALIGNMENT-SEARCH(v)        // v has n rows (phonemes) and T columns (frames), T >= n
L1  Q[i, j] <- -inf for all i, j
L2  Q[0, 0] <- v[0, 0]
L3  for j <- 1 to T - 1 do
L4      for i <- 0 to min(j, n - 1) do
L5          Q[i, j] <- v[i, j] + max(Q[i, j - 1], Q[i - 1, j - 1])    // Q[-1, .] = -inf
L6  i <- n - 1
L7  for j <- T - 1 down to 0 do
L8      a(j) <- i
L9      if j > 0 and i > 0 and Q[i - 1, j - 1] > Q[i, j - 1] then
L10         i <- i - 1
L11 return a, Q[n - 1, T - 1]
```

The search runs with no gradient. The network is trained for the alignment it returns, and the alignment changes as the prior improves.

**Duration predictor.** The durations $d_i = |\{ j : a(j) = i \}|$ are the targets of a stochastic duration predictor, itself a small flow trained by a variational bound. At synthesis time it samples durations, the rows of $\mu_\theta$ and $\sigma_\theta$ are repeated by them, a sample from that normal goes through $f_\theta^{-1}$, and the decoder makes the waveform.

**Training loss.** The loss is the negative [evidence lower bound](/evidence-lower-bound/) plus adversarial terms:

$$L = L_{\text{recon}} + L_{\text{kl}} + L_{\text{dur}} + L_{\text{adv}}(G) + L_{\text{fm}}(G).$$

$L_{\text{recon}}$ is the L1 distance between the mel spectrograms of the target and of the generated waveform. $L_{\text{kl}} = \log q(z \mid x) - \log p_\theta(z \mid c, A)$ at the sampled $z$. $L_{\text{dur}}$ is the bound of the duration predictor. The adversarial and feature matching terms use the multi-period discriminator of HiFi-GAN with the least squares loss, plus the first sub-discriminator of its multi-scale discriminator, the one on the raw waveform.

**Standing assumptions.** A fixed phoneme set and a single speaker, or a speaker embedding for many speakers; a monotonic alignment in which every phoneme gets at least one frame; and training pairs of text and audio with no hand-made alignment.

## What it counts

The model defines a distribution over waveforms given the text. Training maximizes a lower bound on $\log p(x \mid c)$ for the mel target, with the alignment fixed to the result of the search at each step, plus the adversarial terms.

- **Alignment search.** Lines L3 to L5 fill $\Theta(n T)$ cells, each in constant time, and the traceback takes $T$ steps. The search runs once for each training utterance at each step.
- **Count of alignments.** There are $\binom{T - 1}{n - 1}$ monotonic alignments, one for each choice of the $n - 1$ frames where a new phoneme starts. With $n = 3$ and $T = 6$ there are 10. The search finds the best of them without listing them.
- **Synthesis.** All steps run in parallel over frames and samples: one pass of the text encoder, the duration predictor, the inverse flow and the generator. There is no step-by-step loop over frames as in [Tacotron](/tacotron/), so the cost grows linearly with the length of the audio.

**Example.** Take $n = 3$ and $T = 6$ with

| $v_{i,j}$ | $j = 0$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $i = 0$ | $-1$ | $-1$ | $-4$ | $-6$ | $-6$ | $-9$ |
| $i = 1$ | $-5$ | $-2$ | $-1$ | $-1$ | $-5$ | $-5$ |
| $i = 2$ | $-9$ | $-7$ | $-5$ | $-2$ | $-1$ | $-1$ |

The table $Q$ is, row by row: $(-1, -2, -6, -12, -18, -27)$; $(-\infty, -3, -3, -4, -9, -14)$; $(-\infty, -\infty, -8, -5, -5, -6)$. For example $Q_{1,2} = -1 + \max(-3, -2) = -3$. The traceback from $Q_{2,5} = -6$ stays on phoneme 2 at frame 4, because $Q_{2,4} = -5$ is larger than $Q_{1,4} = -9$, and moves down at frames 3 and 1. The alignment is $(0, 0, 1, 1, 2, 2)$ with score $-6$, and the durations are $(2, 2, 2)$. The test file checks this example and compares the search with all alignments.

The code with this page takes the score matrix $v$ as given and implements monotonic alignment search, its tie rule and the Gaussian scores; it does not train a network.

## Relation to other models

- **Glow-TTS** (Kim, Kim, Kong and Yoon 2020) is the parent: a flow from mel frames to a text-conditioned normal prior, trained by exact likelihood with monotonic alignment search. VITS keeps the prior and the search, makes the latent variable a VAE latent, and adds the waveform decoder.
- **[HiFi-GAN](/hifi-gan/)** gives the decoder and the discriminator. In a two-stage system the vocoder is trained on mel spectrograms; in VITS it is trained jointly on the latent $z$.
- **[FastSpeech](/fastspeech/)** also expands phoneme states by durations, but takes the durations from a teacher model or an external aligner. VITS finds them during training with its own search.
- **[Tacotron](/tacotron/)** learns a soft attention alignment and generates frames one by one; it can skip or repeat words when the attention fails. The monotonic alignment of VITS cannot skip a phoneme by construction.
- **[Forced alignment](/forced-alignment/)** and [dynamic time warping](/dynamic-time-warping/) solve the same kind of monotonic alignment problem with an HMM or a frame distance in place of the flow prior.

## Known results in the model

- **Exactness of the search (theorem).** Monotonic alignment search returns an alignment of largest total log-likelihood among all $\binom{T - 1}{n - 1}$ monotonic alignments, in $\Theta(n T)$ time. The proof is the usual principle of optimality for a path in a grid; it is in the proofs folder of this page, with the tie rule.
- **Training is a bound (theorem).** For a fixed alignment, $-L_{\text{recon}} - L_{\text{kl}}$ is, up to constants and the weight of the reconstruction term, the evidence lower bound $\mathbb{E}_q[\log p(x \mid z)] - \mathrm{KL}(q(z \mid x) \,\|\, p(z \mid c, A))$, estimated with one sample. Maximizing the bound over the alignment is what the search does for the prior term.
- **Quality on LJ Speech (measurement).** The paper reports a [mean opinion score](/mean-opinion-score/) of 4.43 ± 0.06 for VITS on the LJ Speech data set, on a 1 to 5 scale with crowd-sourced raters, against 4.46 ± 0.06 for the recordings. In the same test, Tacotron 2 with a fine-tuned HiFi-GAN vocoder has 4.25 ± 0.07 and Glow-TTS with a fine-tuned HiFi-GAN has 4.32 ± 0.07.
- **Speed (measurement).** On one V100 GPU with a batch of 1, VITS generates about 67 times faster than real time, against about 27 times for Glow-TTS with HiFi-GAN.
- **Variety (measurement).** Because the duration predictor is stochastic, the same text gives different lengths on different samples. Over 100 samples of one sentence, the spread of lengths of VITS is close to that of Tacotron 2, while Glow-TTS always gives the same length.
