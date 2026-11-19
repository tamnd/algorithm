---
tag: 93QYYQ
kind: model
slug: neural-codec-language-model
name: Neural codec language model
aliases:
- VALL-E
area: natural-language-and-speech/speech-analysis-and-synthesis
level: research
summary: "TTS as language modeling over the discrete tokens of a neural audio codec, prompted by a few seconds of a speaker to copy an unseen voice."
history:
  year: 2023
  people: [Chengyi Wang, Sanyuan Chen, Yu Wu, Ziqiang Zhang, Long Zhou, Shujie Liu, Zhuo Chen, Yanqing Liu, Huaming Wang, Jinyu Li, Lei He, Sheng Zhao, Furu Wei]
  note: "VALL-E trained transformer language models on the EnCodec tokens of 60000 hours of speech and copied unseen voices from a 3-second prompt."
prereqs: [vector-quantization, causal-language-modeling, transformer]
see_also: [text-to-speech, generative-pretrained-transformer, in-context-learning, autoregressive-decoding, top-k-sampling, wavenet, speaker-verification, word-error-rate]
sources:
  - paper: "Chengyi Wang, Sanyuan Chen, Yu Wu, Ziqiang Zhang, Long Zhou, Shujie Liu, Zhuo Chen, Yanqing Liu, Huaming Wang, Jinyu Li, Lei He, Sheng Zhao and Furu Wei, Neural codec language models are zero-shot text to speech synthesizers, arXiv:2301.02111, 2023"
    title: Wang et al. 2023
    locator: "Section 4 (the codec tokens, the autoregressive and non-autoregressive models and the inference), Section 5 (the setup on LibriLight), Tables 2 and 3 (LibriSpeech test-clean), Tables 4 and 5 (ablations) and the limitations section"
  - paper: doi:10.1109/TASLP.2021.3129994
    title: "Neil Zeghidour, Alejandro Luebs, Ahmed Omran, Jan Skoglund and Marco Tagliasacchi, SoundStream: An end-to-end neural audio codec, IEEE/ACM Transactions on Audio, Speech, and Language Processing 30, 495-507, 2022"
    locator: "the encoder, the residual vector quantizer and the decoder"
  - paper: "Alexandre Défossez, Jade Copet, Gabriel Synnaeve and Yossi Adi, High fidelity neural audio compression, Transactions on Machine Learning Research, 2023, arXiv:2210.13438"
    title: Défossez et al. 2023 (EnCodec)
    locator: "the model description, with the residual vector quantization and the bit rates"
---

A neural codec language model treats [text-to-speech](/text-to-speech/) as language modeling. A neural audio codec turns speech into a short sequence of discrete tokens and back. A [transformer](/transformer/) language model is trained to continue a sequence of such tokens, given the phonemes of the text. To speak in a new voice, the model gets a few seconds of a recording of that voice as a prompt and continues it with the new text, the way a text language model continues a prompt. VALL-E (Wang and colleagues 2023) is the first model of this kind for TTS. It uses the EnCodec codec, whose tokens come from residual [vector quantization](/vector-quantization/), and was trained on 60000 hours of audiobook speech. The approach copies the voice, the recording conditions and some of the emotion of the prompt, with no training on the new speaker.

## The machine

Sizes: $T$ codec frames at 75 Hz, $Q = 8$ codebooks of $K = 1024$ entries, $n$ phonemes, and a transformer of 12 layers, 16 heads, width 1024 and feedforward width 4096. Shapes are for one utterance.

**Codec.** EnCodec maps 24 kHz audio to frames at 75 Hz, one frame per 320 samples. A convolutional encoder gives a vector $e_t$ for each frame. Residual vector quantization codes it with $Q$ codebooks $B_1, \ldots, B_Q$:

$$r_0 = e_t, \qquad c_{t,q} = \operatorname{argmin}_{k} \| r_{q-1} - B_q[k] \|, \qquad r_q = r_{q-1} - B_q[c_{t,q}].$$

The decoder of the codec maps $\sum_q B_q[c_{t,q}]$ back to audio. A clip becomes a code matrix $C$ of shape $T \times 8$, with entries in $\{0, \ldots, 1023\}$. The first codebook carries the coarse content and the later ones the detail, because each codes what the earlier ones left.

**Autoregressive model (first codebook).** A decoder-only transformer with a causal mask reads the phonemes $x$ of the prompt and the target text, then the first-codebook tokens $\tilde c_{:,1}$ of the prompt, and continues with the tokens of the new speech:

$$p(c_{:,1} \mid x, \tilde c_{:,1}) = \prod_{t} p(c_{t,1} \mid c_{<t,1}, \tilde c_{:,1}, x).$$

An end token stops the sequence, so this model also decides the length of the speech and thus its durations.

**Non-autoregressive model (codebooks 2 to 8).** A second transformer, with no causal mask, predicts all frames of codebook $j$ at once, given the earlier codebooks of the new speech, the whole $T \times 8$ prompt $\tilde C$ and the phonemes:

$$p(C_{:,2:8} \mid x, \tilde C) = \prod_{j=2}^{8} p(c_{:,j} \mid C_{:,<j}, x, \tilde C).$$

The embeddings of the earlier codebooks are summed for each frame, and the stage $j$ enters through adaptive layer normalization. The full model is the product of the two parts.

**Inference.** The first codebook is sampled token by token from the autoregressive model; the paper uses sampling because beam search could loop forever. The other 7 codebooks are decoded greedily by the non-autoregressive model in 7 parallel passes. The codec decoder makes the waveform.

**Training.** The training data is LibriLight: 60000 hours of English audiobooks from about 7000 speakers, transcribed into phonemes by a speech recognizer. Each training example is a random crop of 10 to 20 seconds.

**Standing assumptions.** A frozen codec, a phoneme input, and a prompt from the target speaker with its phoneme transcription.

## What it counts

The model defines a distribution over code matrices given the phonemes and the prompt. The waveform is a fixed function of the code matrix.

- **Bit rate.** 75 frames per second times 8 codebooks times $\log_2 1024 = 10$ bits is 6000 bits per second. A 10 s clip is a matrix of $750 \times 8$ codes. Only the first codebook is generated step by step: 750 sequential steps for 10 s, against 240000 for a sample-level model such as [WaveNet](/wavenet/) at the same sample rate.
- **Example of residual quantization.** In two dimensions, take $e = (0.9, -0.3)$, $B_1 = \{(1, 0), (0, 1), (-1, 0), (0, -1)\}$ and $B_2 = \{(0.2, 0), (-0.2, 0), (0, 0.2), (0, -0.2)\}$. The first stage picks $(1, 0)$ and leaves $r_1 = (-0.1, -0.3)$, with $\|r_1\|^2 = 0.10$. The squared distances from $r_1$ to the entries of $B_2$ are $0.18$, $0.10$, $0.26$ and $0.02$, so the second stage picks $(0, -0.2)$ and leaves $r_2 = (-0.1, -0.1)$, with $\|r_2\|^2 = 0.02$. The codes are $(0, 3)$ and the reconstruction is $(1, -0.2)$.
- **Cost.** The autoregressive pass costs, with a [key-value cache](/key-value-cache/), $O(d^2 + (n + T) d)$ per layer and step over $T$ steps. Each non-autoregressive pass costs $O((n + T)^2 d + (n + T) d^2)$ per layer, and there are 7 of them.

## Relation to other models

- **[Causal language models](/causal-language-modeling/)** for text, such as [GPT](/generative-pretrained-transformer/), are the template. The prompt plays the role of [in-context learning](/in-context-learning/): the speaker is given by example, not by an embedding trained for it.
- **[Tacotron](/tacotron/), [FastSpeech](/fastspeech/) and [VITS](/vits/)** predict continuous features with a regression or a variational loss, mostly for speakers seen in training. The codec model predicts discrete tokens with a cross-entropy loss, so it can sample many different renderings of one text.
- **[WaveNet](/wavenet/)** also predicts discrete tokens with a softmax, but at the sample rate. The codec lowers the rate from 24000 to 75 steps per second.
- **SoundStream and EnCodec** are the codecs: a convolutional encoder and decoder trained with reconstruction and adversarial losses, and a residual vector quantizer between them. AudioLM had earlier used SoundStream tokens for speech continuation with no text.

## Known results in the model

- **Zero-shot quality on LibriSpeech (measurement).** On utterances of 4 to 10 s from LibriSpeech test-clean, with a 3 s prompt from another utterance of the same speaker, VALL-E had a [word error rate](/word-error-rate/) of 5.9% under an automatic recognizer and a speaker similarity of 0.580 from a [speaker verification](/speaker-verification/) model, against 7.7% and 0.337 for YourTTS and 2.2% and 0.754 for the recordings.
- **Listening tests (measurement).** On LibriSpeech with 40 speakers, the similarity MOS was 4.38 ± 0.10 for VALL-E, 3.45 ± 0.09 for YourTTS and 4.5 ± 0.10 for the recordings, on a 1 to 5 scale. On VCTK, where the accents differ from the training data, it was 3.81 ± 0.09 against 3.70 ± 0.09 for YourTTS and 4.29 ± 0.09 for the recordings.
- **The prompt sets the voice (measurement).** Without the acoustic prompt, the speaker similarity of the autoregressive model fell from 0.585 to 0.236 at the same word error rate. In the non-autoregressive model, given the true first codebook, the word error rate was 19.6% without any prompt and 2.8% with the phoneme and acoustic prompts.
- **Robustness (observation).** The paper reports that some words are unclear, skipped or repeated, and traces this to the attention alignment of the autoregressive model. This is the same kind of failure as in [Tacotron](/tacotron/), and it is not present in duration-based models.
- **Misuse (observation).** A model that copies a voice from 3 seconds of audio can be used to impersonate a speaker. The paper notes this risk and suggests a detection model for synthetic speech.
