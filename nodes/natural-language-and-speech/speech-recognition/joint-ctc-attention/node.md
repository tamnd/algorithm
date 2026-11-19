---
tag: B2YXXF
kind: technique
slug: joint-ctc-attention
name: Joint CTC-attention
aliases:
- hybrid CTC-attention
- joint CTC-attention decoding
area: natural-language-and-speech/speech-recognition
level: research
summary: Train an attention encoder-decoder with an extra CTC loss on the encoder, and combine both scores in decoding for monotonic alignment.
prereqs: [connectionist-temporal-classification, listen-attend-and-spell, ctc-prefix-beam-search]
see_also: [rnn-transducer, conformer, beam-search, shallow-fusion, length-normalization, encoder-decoder-model, additive-attention, word-error-rate]
sources:
  - paper: doi:10.1109/ICASSP.2017.7953075
    title: Suyoun Kim, Takaaki Hori and Shinji Watanabe, Joint CTC-attention based end-to-end speech recognition using multi-task learning, ICASSP 2017, pages 4835 to 4839
    locator: the sections on the multi-task objective, the experimental setup (the BLSTM encoder and location-based attention) and the results on WSJ1 and CHiME-4
  - paper: doi:10.1109/JSTSP.2017.2763455
    title: Shinji Watanabe, Takaaki Hori, Suyoun Kim, John R. Hershey and Tomoki Hayashi, Hybrid CTC/attention architecture for end-to-end speech recognition, IEEE Journal of Selected Topics in Signal Processing 11(8), 2017, pages 1240 to 1253
    locator: the sections on the multi-objective training and on joint decoding (rescoring, one-pass beam search and the CTC prefix score)
---

Joint CTC-attention combines the two main end-to-end losses for speech recognition in one model. An attention encoder-decoder, such as [listen, attend and spell](/listen-attend-and-spell/), conditions each output on all previous outputs but has no notion of monotonic alignment, so it can skip or repeat parts of the audio, and it learns its alignment slowly. [CTC](/connectionist-temporal-classification/) aligns the audio to the labels monotonically, but assumes the outputs are independent given the audio. The technique adds a CTC output layer on the shared encoder and trains with a weighted sum of the two losses. In decoding, each hypothesis of the attention decoder also gets the CTC probability of its prefix, so hypotheses that do not fit a monotonic alignment of the whole audio score low.

## In plain words

Two students transcribe the same recording. The first writes fluent sentences but sometimes loses their place and repeats a line or skips one. The second follows the audio second by second and never loses their place, but writes clumsy text. Joint CTC-attention trains both students on one shared listening skill, and then lets them grade each other's drafts.

In training, the shared part of the network must serve both, so it learns to follow the audio in order. In decoding, the fluent student proposes the next letters, and the careful student checks whether the text so far still fits the audio from start to end. A draft that skipped a line fits badly and drops out of the search.

## When it applies

- The model is an attention encoder-decoder for a task with a monotonic alignment between input and output, such as speech recognition or handwriting recognition. It does not suit machine translation, where the word order changes.
- The encoder outputs have a frame structure, so a CTC layer can read them, and they are at least as many as the labels (after any time reduction).
- The label set for CTC is the output vocabulary of the decoder plus a blank.

## The template

**Model.** A shared encoder maps the input $x$ to $h_1 \ldots h_L$. A CTC head (a linear layer and a softmax with a blank) gives $p(z_t \mid x)$ for each $h_t$. An attention decoder gives $p_{\mathrm{att}}(y_i \mid x, y_{<i})$.

**Training.** Minimize

$$\mathcal{L} = \lambda\, \mathcal{L}_{\mathrm{CTC}} + (1 - \lambda)\, \mathcal{L}_{\mathrm{att}}, \qquad 0 \le \lambda \le 1,$$

where $\mathcal{L}_{\mathrm{CTC}} = -\ln p_{\mathrm{ctc}}(y \mid x)$ by the CTC forward algorithm and $\mathcal{L}_{\mathrm{att}} = -\sum_i \ln p_{\mathrm{att}}(y_i \mid x, y_{<i})$ with teacher forcing (Kim, Hori and Watanabe 2017).

**Decoding** (Watanabe et al. 2017). Run a beam search over output prefixes of the decoder. A prefix $h$ gets the score

$$\alpha(h) = \lambda \ln p_{\mathrm{ctc}}(h, \ldots \mid x) + (1 - \lambda) \ln p_{\mathrm{att}}(h \mid x),$$

optionally plus $\gamma \ln p_{\mathrm{lm}}(h)$. Here $p_{\mathrm{ctc}}(h, \ldots \mid x)$ is the CTC prefix probability: the total CTC probability of all labelings that begin with $h$. For a complete hypothesis that ends with the end symbol, the CTC term is the full probability $p_{\mathrm{ctc}}(h \mid x)$.

**The CTC prefix probability.** For $h = g c$, keep for each frame $t$ the probabilities $\gamma^{n}_t(h)$ and $\gamma^{b}_t(h)$ of the paths over frames $1..t$ that collapse to $h$ and end in a label or in a blank, the same two numbers as in [CTC prefix beam search](/ctc-prefix-beam-search/). With the values of $g$ stored, and $\Phi_{t-1} = \gamma^b_{t-1}(g) + \gamma^n_{t-1}(g)$ if the last label of $g$ is not $c$, $\Phi_{t-1} = \gamma^b_{t-1}(g)$ if it is,

$$\gamma^n_t(h) = \big(\gamma^n_{t-1}(h) + \Phi_{t-1}\big)\, y_t(c), \qquad \gamma^b_t(h) = \big(\gamma^b_{t-1}(h) + \gamma^n_{t-1}(h)\big)\, y_t(\varnothing),$$

$$p_{\mathrm{ctc}}(h, \ldots \mid x) = \gamma^n_1(h) + \sum_{t=2}^{L} \Phi_{t-1}\, y_t(c),$$

where $\gamma^n_1(h) = y_1(c)$ if $g$ is empty and 0 otherwise. Each term of the sum is the probability of the paths in which the label $c$ of $h$ first appears at frame $t$. The cost is $O(L)$ for each new prefix. In the rescoring variant, the attention beam search runs alone and the CTC score is added to its $n$ best hypotheses.

## Classic examples

**A worked prefix score.** Use the CTC outputs of the example on the CTC page, with frames 1 to 3 and the symbols blank, a and b: $(0.5, 0.4, 0.1)$, $(0.4, 0.3, 0.3)$ and $(0.3, 0.1, 0.6)$. From the empty prefix, $\gamma^b(\varepsilon) = 0.5, 0.2, 0.06$ and $\gamma^n(\varepsilon) = 0$. For $h = $ "a": $\gamma^n_1 = 0.4$, then $\Phi_1 = 0.5$ adds $0.5 \cdot 0.3 = 0.15$ and $\Phi_2 = 0.2$ adds $0.2 \cdot 0.1 = 0.02$, so $p_{\mathrm{ctc}}(\mathrm{a}, \ldots) = 0.57$. In the same way $p_{\mathrm{ctc}}(\mathrm{b}, \ldots) = 0.1 + 0.15 + 0.12 = 0.37$. With the probability 0.06 of the empty labeling, $0.57 + 0.37 + 0.06 = 1$. If the attention decoder gives $p_{\mathrm{att}}(\mathrm{a}) = 0.45$ and $p_{\mathrm{att}}(\mathrm{b}) = 0.55$, then with $\lambda = 0.5$ the scores are $\alpha(\mathrm{a}) = 0.5(\ln 0.57 + \ln 0.45) = -0.680$ and $\alpha(\mathrm{b}) = 0.5(\ln 0.37 + \ln 0.55) = -0.796$, so the CTC term moves "a" ahead. The full CTC probability of "a" alone is only 0.176; most of its prefix probability is in "ab" (0.378 as a prefix).

**Multi-task training on WSJ and CHiME-4.** Kim, Hori and Watanabe (2017) used a 4-layer BLSTM encoder with 320 cells that reduces the frame rate by 4, and location-based attention, with $\lambda \in \{0.2, 0.5, 0.8\}$. With $\lambda = 0.2$, the character error rate on WSJ1 was 7.36%, against 8.97% for CTC alone and 8.17% for attention alone; on CHiME-4 it was 44.99%, against 48.79% and 47.58% (measurements, beam 20). The attention weights also became monotonic after fewer training steps.

**Joint decoding.** Watanabe et al. (2017) added the CTC prefix score to the beam search of the attention decoder, either by rescoring the $n$ best hypotheses or in one pass with the recursion above.

## Variations

- **Weight in training and in decoding.** The weight of the CTC term may differ between the two. A small weight in training (0.1 to 0.3) is common, and the decoding weight is tuned on held-out data.
- **Encoders.** The same combination works with Transformer and [Conformer](/conformer/) encoders; the CTC head reads the last encoder layer, or an intermediate one.
- **CTC as an auxiliary loss only.** Train with both losses and decode with the attention decoder alone. This keeps most of the training benefit and the cost of decoding is lower.
- **Attention rescoring of CTC.** Decode with [CTC prefix beam search](/ctc-prefix-beam-search/), which can stream, and rescore its $n$ best list with the attention decoder.
- **Transducers.** An [RNN transducer](/rnn-transducer/) gets a monotonic alignment by its own loss; CTC can also be added to its encoder as an extra loss.

## Pitfalls

- **Prefix probability and full probability.** The prefix probability of $h$ counts every labeling that begins with $h$, not $h$ itself. A finished hypothesis must use the full CTC probability $p_{\mathrm{ctc}}(h \mid x)$ when the end symbol is added, or short hypotheses win.
- **Cost of the prefix score.** The prefix score costs $O(L)$ for every candidate extension of every hypothesis. Limit the candidates to the best few labels of the attention decoder.
- **Time reduction too strong.** CTC needs at least as many encoder frames as labels, plus one for each repeated label. A strong reduction of the frame rate with short sub-word units can make some targets impossible.
- **Different vocabularies.** The CTC head and the decoder must share the label set; the end symbol of the decoder has no CTC label.

## Exercises

1. Show that $p_{\mathrm{ctc}}(g, \ldots \mid x)$ equals $p_{\mathrm{ctc}}(g \mid x)$ plus the sum of $p_{\mathrm{ctc}}(g c, \ldots \mid x)$ over all labels $c$. Check it on the example for $g = $ "a" with $p_{\mathrm{ctc}}(\mathrm{a}) = 0.176$, $p_{\mathrm{ctc}}(\mathrm{aa}, \ldots) = 0.016$ and $p_{\mathrm{ctc}}(\mathrm{ab}, \ldots) = 0.378$.
2. Explain why $\Phi_{t-1}$ leaves out $\gamma^n_{t-1}(g)$ when $c$ equals the last label of $g$.
3. With $\lambda = 1$ in decoding, what does the beam search compute? Is it the same as CTC prefix beam search?
4. Give an input where an attention decoder alone would prefer a hypothesis that drops a word, and show how the CTC prefix score penalizes it.

## References
