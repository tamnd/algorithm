---
tag: HA15NQ
kind: model
slug: wav2vec-2
name: "wav2vec 2.0"
aliases:
- wav2vec2
area: natural-language-and-speech/speech-recognition
level: research
summary: Self-supervised speech pretraining that masks latent frames and learns to pick the true quantized latent among distractors by contrastive loss.
history:
  year: 2020
  people: [Alexei Baevski, Henry Zhou, Abdelrahman Mohamed, Michael Auli]
  note: Baevski, Zhou, Mohamed and Auli pretrained a Transformer on unlabeled speech by masking and a contrastive task over learned discrete units, then fine-tuned it with CTC on as little as ten minutes of transcribed audio.
prereqs: [transformer, masked-language-modeling, vector-quantization, connectionist-temporal-classification]
see_also: [bert, gumbel-max-trick, noise-contrastive-estimation, product-quantization, conformer, specaugment, rnn-transducer, automatic-speech-recognition]
sources:
  - paper: "Alexei Baevski, Henry Zhou, Abdelrahman Mohamed and Michael Auli, wav2vec 2.0: a framework for self-supervised learning of speech representations, Advances in Neural Information Processing Systems 33 (NeurIPS 2020), arXiv:2006.11477"
    title: The model, the quantization module, the masking, the contrastive and diversity losses, fine-tuning with CTC and the LibriSpeech results
    locator: "Section 2 (feature encoder, contextualized representations, quantization module), Section 3 (masking, the objective, fine-tuning), Section 4 (the setup, BASE and LARGE) and Section 5 (results with 10 minutes to 960 hours of labeled data)"
---

wav2vec 2.0 learns speech representations from raw audio without transcripts and then turns them into a recognizer with very little labeled data. A convolutional feature encoder maps the waveform to latent vectors, about one every 20 ms. Some spans of these latents are masked, and a [Transformer](/transformer/) reads the masked sequence. For each masked position, the model must pick out the true latent, discretized by a learned quantizer, from 100 distractors taken from other masked positions of the same utterance. This is a contrastive task, in the spirit of [masked language modeling](/masked-language-modeling/) but with speech units that the model learns itself. After pretraining, a linear layer and a [CTC](/connectionist-temporal-classification/) loss fine-tune the network on transcribed speech. With ten minutes of labeled audio it reached word error rates that earlier systems needed hundreds of hours for.

## The machine

**Feature encoder.** Seven 1-D convolution layers with 512 channels, strides $(5, 2, 2, 2, 2, 2, 2)$ and kernel widths $(10, 3, 3, 3, 3, 2, 2)$, map 16 kHz audio $x$ to latent vectors $z_1 \ldots z_T$. The total stride is $5 \cdot 2^6 = 320$ samples, 20 ms, so there are about 49 vectors per second, and each $z_t$ sees $10 + 2 \cdot 5 + 2 \cdot 10 + 2 \cdot 20 + 2 \cdot 40 + 80 + 160 = 400$ samples, 25 ms of audio.

**Context network.** A Transformer reads the latents, after a projection, and outputs context vectors $c_1 \ldots c_T$. Instead of fixed position embeddings, a convolution with kernel size 128 and 16 groups adds relative position information. The paper has two sizes:

| model | blocks | width | feedforward width | heads | parameters |
|---|---|---|---|---|---|
| BASE | 12 | 768 | 3072 | 8 | 95 M |
| LARGE | 24 | 1024 | 4096 | 16 | 317 M |

**Quantization module.** It maps each $z_t$ to a discrete code $q_t$, the training target. There are $G = 2$ codebooks with $V = 320$ entries each. A linear layer maps $z_t$ to logits $l_{g,v}$, and one entry is chosen from each codebook by a Gumbel softmax: in the forward pass the entry with the largest $l_{g,v} + n_v$, where $n_v$ is Gumbel noise (the [Gumbel-max trick](/gumbel-max-trick/)), and in the backward pass the gradient of the softmax with temperature $\tau$ (the straight-through estimator). The temperature falls from 2 to 0.5 (BASE) or 0.1 (LARGE) during training. The chosen entries are concatenated and mapped linearly to $q_t$. This gives $320^2 = 102\,400$ possible codes, as in [product quantization](/product-quantization/).

**Masking.** Each time step is chosen as a span start with probability $p = 0.065$, and the $M = 10$ steps from each start are masked; spans may overlap. The masked $z_t$ are replaced by one learned vector before the Transformer. About $1 - (1 - 0.065)^{10} \approx 49\%$ of the steps end up masked, in spans of 14.7 steps on average.

**Objective.** For each masked step $t$, with the cosine similarity $\mathrm{sim}$, a temperature $\kappa = 0.1$ and a set $Q_t$ that holds $q_t$ and $K = 100$ distractors sampled from other masked steps of the same utterance,

$$\mathcal{L}_m = -\ln \frac{\exp(\mathrm{sim}(c_t, q_t) / \kappa)}{\sum_{\tilde q \in Q_t} \exp(\mathrm{sim}(c_t, \tilde q) / \kappa)}.$$

A diversity loss $\mathcal{L}_d = \frac{1}{G V} \sum_{g=1}^{G} \sum_{v=1}^{V} \bar p_{g,v} \ln \bar p_{g,v}$, where $\bar p_{g,v}$ is the softmax probability of entry $v$ averaged over a batch, rewards using all codebook entries. The loss is $\mathcal{L} = \mathcal{L}_m + 0.1\, \mathcal{L}_d$.

**Fine-tuning.** A linear layer on the context vectors maps to the output symbols (for LibriSpeech, 29 characters plus a word boundary token), and the model is trained with the CTC loss on the labeled data. Decoding may add an n-gram or Transformer language model.

**Example.** Take 2 seconds of audio: $32\,000$ samples give about 99 latent vectors. With $p = 0.065$, about 6 or 7 span starts are drawn, and their 10-step spans mask roughly half of the vectors. Each masked position gives one 101-way classification: its own quantized latent against 100 others from the masked positions of the same 2 seconds.

## What it counts

Pretraining gives a network whose context vectors $c_t$ are a representation of the audio around $t$; it does not output text. Fine-tuning with CTC turns it into a recognizer, with $\ln p(y \mid x)$ from the CTC forward algorithm. The cost per utterance of $T$ latent steps is $\Theta(T)$ for the feature encoder, $\Theta(N (T d^2 + T^2 d))$ for a Transformer of $N$ blocks and width $d$, $\Theta(T G V)$ for the quantizer, and $\Theta(T_m K d)$ for the contrastive loss over $T_m$ masked steps. The self-attention term dominates for long inputs.

## Relation to other models

- **[BERT](/bert/) and masked language modeling.** Both mask parts of the input and predict them from the context. Text has a fixed vocabulary of tokens; speech has none, so wav2vec 2.0 learns the units by quantization and uses a contrastive loss instead of a softmax over a vocabulary.
- **Contrastive predictive coding and [noise contrastive estimation](/noise-contrastive-estimation/).** The loss picks the true target among sampled distractors, a contrastive method in the same family.
- **[CTC](/connectionist-temporal-classification/).** The fine-tuning loss. Other heads, such as a [transducer](/rnn-transducer/) or an attention decoder, can also be put on the pretrained encoder.
- **[SpecAugment](/specaugment/).** The masking of time spans in the latent space resembles the time masks of SpecAugment, but here the masked spans are the prediction targets, not only noise.
- **[Hybrid](/hybrid-dnn-hmm/) and supervised end-to-end models.** They need many hours of transcribed audio. wav2vec 2.0 moves most of the learning to unlabeled audio.

## Known results in the model

- **LibriSpeech with little labeled data.** With the LARGE model pretrained on the largest unlabeled set and a language model in decoding, Baevski et al. (2020) report word error rates of 4.8% on test-clean and 8.2% on test-other with 10 minutes of labeled data, 2.0% and 4.0% with 100 hours, and 1.8% and 3.3% with all 960 hours (measurements).
- **Masking statistics.** With $p = 0.065$ and $M = 10$, the expected fraction of masked steps is $1 - (1 - p)^{M} \approx 0.49$ for steps far from the ends (a calculation, which matches the 49% the paper reports).
- **Feature rate.** The feature encoder has a stride of 20 ms and a receptive field of 25 ms (a property of the layer sizes).
- **Number of codes.** Two codebooks of 320 entries give $102\,400$ codes, of which the diversity loss pushes the model to use many (a property of the construction).

## References
