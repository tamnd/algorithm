---
tag: 7N44VZ
kind: model
slug: rnn-transducer
name: RNN transducer
aliases:
- RNN-T
- neural transducer
area: natural-language-and-speech/speech-recognition
level: advanced
summary: A streaming end-to-end model joining an acoustic encoder and a label predictor network, trained by summing over alignments in a lattice.
history:
  year: 2012
  people: [Alex Graves]
  note: Graves proposed the transducer in 2012 to remove two limits of CTC, the independence of the outputs given the input and the rule that the output is not longer than the input, and tested it on TIMIT phone recognition.
prereqs: [connectionist-temporal-classification, forward-backward-algorithm, softmax-regression]
see_also: [ctc-prefix-beam-search, listen-attend-and-spell, joint-ctc-attention, conformer, beam-search, shallow-fusion, encoder-decoder-model, automatic-speech-recognition]
sources:
  - paper: "Alex Graves, Sequence transduction with recurrent neural networks, ICML 2012 Workshop on Representation Learning, arXiv:1211.3711, 2012 (preprint)"
    title: The transducer, its output lattice, the forward-backward recursions, the gradient and the beam search
    locator: "Section 2 (eqs. 12 to 22, the output lattice and the forward and backward variables), Section 2.6 (Algorithm 1, beam search) and Section 4 (TIMIT)"
  - paper: doi:10.21437/Interspeech.2020-3015
    title: "Anmol Gulati, James Qin, Chung-Cheng Chiu, Niki Parmar, Yu Zhang, Jiahui Yu, Wei Han, Shibo Wang, Zhengdong Zhang, Yonghui Wu and Ruoming Pang, Conformer: convolution-augmented transformer for speech recognition, Interspeech 2020, pages 5036 to 5040"
    locator: the sections on the model architecture (a Conformer encoder with a one-layer LSTM decoder) and the LibriSpeech results
---

The RNN transducer (RNN-T) is an end-to-end speech recognizer that maps $T$ acoustic frames to a label sequence $y = y_1 \ldots y_U$ of any length, with no frame alignment in the training data. It has three parts: an encoder that reads the audio, a prediction network that reads the labels emitted so far, and a joint network that combines one encoder frame and one prediction state into a distribution over the labels and a blank. A blank means "go to the next frame", and a label means "emit it and stay on this frame". Each way of interleaving $T$ blanks with the $U$ labels is an alignment, and the probability of $y$ is the sum over all alignments. A [forward-backward](/forward-backward-algorithm/) recursion on a $T \times (U + 1)$ lattice computes this sum and its gradient. Unlike [CTC](/connectionist-temporal-classification/), each output depends on the previous labels, and a frame can emit several labels. With a unidirectional encoder the model can emit text while the audio arrives, so it is the usual choice for streaming recognition on devices.

## The machine

The input is $x = x_1 \ldots x_T$, the labels come from an alphabet $L$, and $\varnothing$ is the blank. The model has three networks.

**Encoder** (the transcription network of Graves 2012). It maps $x$ to vectors $f_1, \ldots, f_T$. Graves used a bidirectional LSTM; a streaming model uses a unidirectional LSTM or a [Conformer](/conformer/) with limited look-ahead.

**Prediction network.** It reads the labels $y_1 \ldots y_u$ emitted so far, after a start symbol, and outputs a vector $g_u$ for $u = 0, \ldots, U$. It is a recurrent network that sees no audio, so it works like a language model over labels.

**Joint network.** For each lattice node $(t, u)$, it combines $f_t$ and $g_u$ into a distribution over $L \cup \{\varnothing\}$. Graves (2012) adds the two vectors and applies a softmax, $\Pr(k \mid t, u) = e^{f_t^k + g_u^k} / \sum_{k'} e^{f_t^{k'} + g_u^{k'}}$. Later systems put a small feedforward layer between the sum and the softmax. Write $y(t, u) = \Pr(y_{u+1} \mid t, u)$ and $\varnothing(t, u) = \Pr(\varnothing \mid t, u)$.

**The lattice.** An alignment starts at node $(1, 0)$. At node $(t, u)$, a blank moves to $(t + 1, u)$, and the label $y_{u+1}$ moves to $(t, u + 1)$. The alignment ends with the blank at $(T, U)$. So it has exactly $T$ blanks and $U$ labels, the last symbol is a blank, and the number of alignments is $\binom{T + U - 1}{U}$. The probability of an alignment is the product of the probabilities of its steps.

**Forward and backward variables** (Graves 2012, Section 2). With $\alpha(1, 0) = 1$,

$$\alpha(t, u) = \alpha(t - 1, u)\, \varnothing(t - 1, u) + \alpha(t, u - 1)\, y(t, u - 1),$$

where a term with an index outside the lattice is 0, and

$$\Pr(y \mid x) = \alpha(T, U)\, \varnothing(T, U).$$

The backward variable starts at $\beta(T, U) = \varnothing(T, U)$ and satisfies $\beta(t, u) = \beta(t + 1, u)\, \varnothing(t, u) + \beta(t, u + 1)\, y(t, u)$. For every node, $\alpha(t, u) \beta(t, u)$ is the probability of the alignments that pass through $(t, u)$.

**Training.** The loss is $-\ln \Pr(y \mid x)$. Its derivatives with respect to the outputs of the joint network are

$$\frac{\partial \Pr(y \mid x)}{\partial y(t, u)} = \alpha(t, u)\, \beta(t, u + 1), \qquad \frac{\partial \Pr(y \mid x)}{\partial \varnothing(t, u)} = \alpha(t, u)\, \beta(t + 1, u),$$

with $\beta(T + 1, U) = 1$ for the final blank, and the derivative is 0 for the other symbols. The chain rule through the softmax and the three networks gives the rest. All three networks are trained together.

**Decoding.** Graves (2012, Algorithm 1) gives a beam search over output prefixes. The prediction state depends on the whole prefix, so prefixes are not merged as freely as in [CTC prefix beam search](/ctc-prefix-beam-search/), and the search must allow several labels per frame. Greedy decoding emits the most probable symbol at each node until it is a blank, then moves to the next frame.

**Example.** Let $T = 2$, $y = a$ ($U = 1$), and let the joint network give $\Pr(a \mid 1, 0) = 0.5$, $\varnothing(1, 0) = 0.4$, $\varnothing(1, 1) = 0.7$, $\Pr(a \mid 2, 0) = 0.6$, $\varnothing(2, 0) = 0.3$ and $\varnothing(2, 1) = 0.8$. There are $\binom{2}{1} = 2$ alignments: "a ∅ ∅" (emit a at frame 1) and "∅ a ∅" (emit a at frame 2). The forward variables are $\alpha(1, 0) = 1$, $\alpha(1, 1) = 0.5$, $\alpha(2, 0) = 0.4$ and $\alpha(2, 1) = 0.5 \cdot 0.7 + 0.4 \cdot 0.6 = 0.59$. So $\Pr(a \mid x) = 0.59 \cdot 0.8 = 0.472$, which is $0.5 \cdot 0.7 \cdot 0.8 + 0.4 \cdot 0.6 \cdot 0.8 = 0.28 + 0.192$. From the end, $\beta(2, 1) = 0.8$, $\beta(1, 1) = 0.56$, $\beta(2, 0) = 0.48$ and $\beta(1, 0) = 0.4 \cdot 0.48 + 0.5 \cdot 0.56 = 0.472$, the same value.

## What it counts

The model gives $\ln \Pr(y \mid x)$, a normalized probability of the whole label sequence, and a decoder searches for the $y$ with the largest value, possibly with an external language model.

The cost is set by the joint network. Training evaluates it at all $T (U + 1)$ nodes, each with an output of size $|L| + 1$, so time and memory are $\Theta(T U |L|)$ for the joint outputs, plus the cost of the encoder on $T$ frames and of the prediction network on $U + 1$ prefixes. The forward and backward recursions take $\Theta(T U)$ time once the outputs are known. With thousands of word pieces and long utterances, the $T \times U \times |L|$ tensor is the memory limit of training; a frame rate reduction in the encoder makes $T$ smaller.

## Relation to other models

- **[CTC](/connectionist-temporal-classification/).** CTC also sums over alignments with a blank, but each frame emits exactly one symbol, the outputs are independent given the audio, and the output can be at most as long as the input. The transducer drops these three limits by the prediction network and the move "emit and stay on this frame".
- **[Listen, attend and spell](/listen-attend-and-spell/) and other attention models.** They also condition each label on the previous labels, but they attend over the whole utterance and have no monotonic alignment, so they do not stream without changes. The transducer is monotonic by construction.
- **[Hybrid DNN-HMM](/hybrid-dnn-hmm/).** A hybrid model needs a lexicon, tied states and a separate language model. The transducer learns the mapping from audio to characters or word pieces directly, and the prediction network takes the role of an internal language model.
- **[Joint CTC-attention](/joint-ctc-attention/).** Another way to get a monotonic alignment into an end-to-end model, by an extra CTC loss.
- **Encoders.** The transducer fixes only the loss and the decoding rule. LSTM, Transformer and [Conformer](/conformer/) encoders are all used with it; Gulati et al. (2020) used a Conformer encoder with a one-layer LSTM prediction network.

## Known results in the model

- **The forward recursion is exact.** It sums the probabilities of all $\binom{T + U - 1}{U}$ alignments in $\Theta(T U)$ operations, because every alignment that reaches $(t, u)$ arrives from $(t - 1, u)$ by a blank or from $(t, u - 1)$ by a label, never both (a theorem, by induction on $t + u$).
- **The number of alignments.** An alignment is a sequence of $T - 1$ blanks and $U$ labels in any order, followed by the final blank, so there are $\binom{T + U - 1}{U}$ of them (a theorem). For $T = 100$ and $U = 20$ that is about $2.5 \cdot 10^{22}$.
- **TIMIT.** Graves (2012) measured a phone error rate of 23.2% for the transducer against 25.5% for a CTC network on TIMIT (measurements).
- **LibriSpeech.** With a Conformer encoder, Gulati et al. (2020) measured word error rates of 2.1% on test-clean and 4.3% on test-other without a language model, and 1.9% and 3.9% with one (measurements).

## References
