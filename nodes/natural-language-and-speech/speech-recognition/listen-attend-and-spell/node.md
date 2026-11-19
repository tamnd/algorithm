---
tag: 9Z2KJ8
kind: model
slug: listen-attend-and-spell
name: "Listen, attend and spell"
aliases:
- attention-based speech recognizer
- LAS
area: natural-language-and-speech/speech-recognition
level: advanced
summary: An attention encoder-decoder recognizer with a pyramidal BiLSTM listener that emits characters without a lexicon or HMM.
history:
  year: 2016
  people: [William Chan, Navdeep Jaitly, Quoc V. Le, Oriol Vinyals]
  note: Chan, Jaitly, Le and Vinyals applied an attention encoder-decoder to large vocabulary speech recognition, with a pyramidal BLSTM encoder to shorten the input, and output characters directly.
prereqs: [encoder-decoder-model, additive-attention, beam-search]
see_also: [connectionist-temporal-classification, rnn-transducer, joint-ctc-attention, specaugment, scheduled-sampling, teacher-forcing, shallow-fusion, length-normalization]
sources:
  - paper: doi:10.1109/ICASSP.2016.7472621
    title: "William Chan, Navdeep Jaitly, Quoc V. Le and Oriol Vinyals, Listen, attend and spell: a neural network for large vocabulary conversational speech recognition, ICASSP 2016, pages 4960 to 4964"
    locator: "the sections on the listener (the pyramidal BLSTM, eq. 5), attend and spell (eqs. 9 to 11), learning, decoding and rescoring, and the voice search results"
  - paper: doi:10.21437/Interspeech.2019-2680
    title: "Daniel S. Park, William Chan, Yu Zhang, Chung-Cheng Chiu, Barret Zoph, Ekin D. Cubuk and Quoc V. Le, SpecAugment: a simple data augmentation method for automatic speech recognition, Interspeech 2019, pages 2613 to 2617"
    locator: the LAS models trained with SpecAugment and their LibriSpeech and Switchboard results
---

Listen, attend and spell (LAS) is a speech recognizer made of one neural network that reads the acoustic frames and writes the transcript one character at a time. The listener, a pyramidal bidirectional LSTM, turns the frames into a shorter sequence of feature vectors. The speller, an LSTM decoder, produces each character from the previous characters and a context vector, which an attention step computes as a weighted average of the listener features. There is no HMM, no pronunciation lexicon and no frame alignment: the model is trained on pairs of audio and text to maximize $\ln P(y \mid x)$. It does not assume that the outputs are independent given the audio, as [CTC](/connectionist-temporal-classification/) does, but the attention can jump anywhere, so the alignment is not forced to be monotonic and the whole utterance must be heard before decoding.

## The machine

The input is a sequence of filter bank frames $x = x_1 \ldots x_T$. The output is a character sequence $y = y_1 \ldots y_S$ that ends with an end-of-sentence symbol. The model factors

$$P(y \mid x) = \prod_{i=1}^{S} P(y_i \mid x, y_{<i}).$$

**Listener.** A bidirectional LSTM reads the frames. A pyramidal BLSTM layer (pBLSTM) then concatenates each pair of consecutive outputs of the layer below before it reads them (Chan et al. 2016, eq. 5):

$$h^{j}_{i} = \mathrm{pBLSTM}\big(h^{j}_{i-1}, [h^{j-1}_{2i}; h^{j-1}_{2i+1}]\big).$$

Each pBLSTM layer halves the length, so three of them reduce $T$ frames to $U = T / 8$ vectors $h = h_1 \ldots h_U$. The reduction makes the attention cheaper, and the attention has fewer positions to choose from at each step.

**Attend.** At output step $i$, the speller state $s_i$ and the listener vectors give scores, weights and a context (eqs. 9 to 11):

$$e_{i,u} = \langle \phi(s_i), \psi(h_u) \rangle, \qquad \alpha_{i,u} = \frac{e^{e_{i,u}}}{\sum_{u'} e^{e_{i,u'}}}, \qquad c_i = \sum_{u} \alpha_{i,u} h_u,$$

where $\phi$ and $\psi$ are small feedforward networks. This is a content-based attention, close to [additive attention](/additive-attention/) and to multiplicative attention.

**Spell.** A 2-layer LSTM with 512 units computes $s_i$ from $s_{i-1}$, $y_{i-1}$ and $c_{i-1}$, and a feedforward network with a softmax gives $P(y_i \mid x, y_{<i})$ from $s_i$ and $c_i$.

**Training.** The loss is $-\sum_i \ln P(y_i \mid x, y_{<i})$ with the true previous characters as inputs ([teacher forcing](/teacher-forcing/)). Chan et al. (2016) replaced the true previous character by a sample from the model in 10% of the steps, as in [scheduled sampling](/scheduled-sampling/), so the speller sees its own errors in training.

**Decoding.** A left-to-right [beam search](/beam-search/) (beam 32 in the paper) keeps the most probable prefixes and ends a hypothesis at the end symbol. The $n$ best hypotheses are then rescored with a language model:

$$s(y \mid x) = \frac{\ln P(y \mid x)}{|y|_c} + \lambda \ln P_{\mathrm{LM}}(y),$$

where $|y|_c$ is the number of characters and $\lambda = 0.008$ was set on held-out data. The division by the length counters the preference of the product for short outputs; see [length normalization](/length-normalization/).

## What it counts

The model gives $\ln P(y \mid x)$ for a character sequence. Training on an utterance costs $O(T)$ LSTM steps in the listener and, in the speller, $S$ LSTM steps and $S$ attention steps over $U$ vectors, so the attention costs $O(U S)$ dot products. Without the pyramid, $U$ would be $T$ and the attention would cost $O(T S)$, 8 times more. Decoding with a beam of width $B$ repeats the speller and the attention for each hypothesis, $O(B U S)$ in total, and it starts only after the listener has read the whole utterance.

## Relation to other models

- **[Encoder-decoder model](/encoder-decoder-model/).** LAS is an encoder-decoder with attention, as in neural machine translation, adapted to long acoustic inputs by the pyramid.
- **[CTC](/connectionist-temporal-classification/).** CTC outputs one symbol per frame and assumes the outputs are independent given the audio. LAS conditions on all previous characters and needs no blank, but it can skip or repeat parts of the audio. [Joint CTC-attention](/joint-ctc-attention/) adds a CTC loss on the listener to keep the alignment monotonic.
- **[RNN transducer](/rnn-transducer/).** Also conditions on the previous labels, but sums over monotonic alignments and can stream. LAS attends over the full utterance.
- **[Hybrid DNN-HMM](/hybrid-dnn-hmm/).** LAS replaces the acoustic model, the lexicon and most of the language model of a hybrid system by one network. In 2016 the hybrid system was still better on the same data.
- **[Conformer](/conformer/) and Transformer encoders.** Later attention recognizers keep the attend-and-spell structure and replace the BLSTM listener by self-attention encoders.

## Known results in the model

- **Voice search.** On a Google voice search task, Chan et al. (2016) measured word error rates of 16.2% on clean and 19.0% on noisy test data for the base model, 12.6% and 14.7% with language model rescoring, 14.1% and 16.5% with sampling in training, and 10.3% and 12.0% with both. A CLDNN-HMM hybrid system had 8.0% and 8.9% (measurements).
- **With augmentation.** Park et al. (2019) trained larger LAS models with [SpecAugment](/specaugment/) and measured 2.8% and 6.8% on LibriSpeech test-clean and test-other without a language model, and 2.5% and 5.8% with shallow fusion (measurements).
- **No monotonic alignment.** The attention weights at step $i$ may put mass anywhere in the utterance, so nothing in the model stops it from repeating or dropping words (a property of the model).

## References
