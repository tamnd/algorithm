---
tag: 7KBK03
kind: algorithm
slug: connectionist-temporal-classification
name: Connectionist temporal classification
aliases:
- CTC
- CTC loss
area: natural-language-and-speech/speech-recognition
level: advanced
summary: A loss for unaligned sequences that sums over all frame labelings with blanks and repeats collapsing to the target, by forward-backward.
solves: [automatic-speech-recognition, sequence-labeling]
model: floating-point-model
complexity:
  vars: {T: the number of frames, U: the length of the label sequence, K: the number of output symbols with the blank}
  time: {worst: "Θ(T (U + K))"}
  space: {extra: "Θ(T U)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2006
  people: [Alex Graves, Santiago Fernández, Faustino Gomez, Jürgen Schmidhuber]
  note: Graves, Fernández, Gomez and Schmidhuber introduced CTC at ICML 2006 to train recurrent networks on unsegmented sequences, and tested it on TIMIT phone recognition.
prereqs: [forward-backward-algorithm, softmax-regression, log-sum-exp-trick]
see_also: [ctc-prefix-beam-search, rnn-transducer, joint-ctc-attention, forced-alignment, hybrid-dnn-hmm, wav2vec-2, greedy-decoding, cross-entropy-loss]
sources:
  - paper: doi:10.1145/1143844.1143891
    title: "Alex Graves, Santiago Fernández, Faustino Gomez and Jürgen Schmidhuber, Connectionist temporal classification: labelling unsegmented sequence data with recurrent neural networks, Proceedings of the 23rd International Conference on Machine Learning (ICML 2006), pages 369 to 376"
    locator: "Section 3 (the map B and eqs. 2 to 4), Section 4.1 (forward and backward, eqs. 5 to 11), Section 4.2 (the gradient, eqs. 12 to 16) and Table 1"
  - paper: "Awni Y. Hannun, Andrew L. Maas, Daniel Jurafsky and Andrew Y. Ng, First-pass large vocabulary continuous speech recognition using bi-directional recurrent DNNs, arXiv:1408.2873, 2014 (preprint)"
    title: Prefix beam search for CTC with a language model
    locator: Section 3 (decoding) and Algorithm 1
  - paper: "Alexei Baevski, Henry Zhou, Abdelrahman Mohamed and Michael Auli, wav2vec 2.0: a framework for self-supervised learning of speech representations, Advances in Neural Information Processing Systems 33 (NeurIPS 2020), arXiv:2006.11477"
    title: Fine-tuning of a pretrained speech encoder with the CTC loss
    locator: the section on fine-tuning
---

Connectionist temporal classification (CTC) trains a network that reads $T$ frames and must output a shorter label sequence $l$, when nobody has marked which frame belongs to which label. The network outputs, at each frame, a distribution over the labels and one extra symbol, the blank. The probability of $l$ is the sum over all frame-level paths that become $l$ after merging repeats and deleting blanks. A [forward-backward](/forward-backward-algorithm/) recursion on the sequence $l$ with blanks inserted computes this sum and its gradient in $\Theta(T U)$ steps, although the number of paths grows exponentially in $T$. The loss is $-\ln p(l \mid x)$ in nats.

## In plain words

A speech network looks at many short slices of sound, but the word "cat" has only three letters. CTC lets the network say one thing for each slice: a letter, or a special "nothing here" symbol called the blank. To read the result, you merge letters that repeat next to each other and then delete the blanks. So "cc_aaa_t" and "c_a__tt" both read as "cat".

Many slice-by-slice outputs read as "cat". The training goal is to make the total probability of all of them large. Listing them is impossible, but a table with one row per slice and one column per position in "_c_a_t_" adds them up quickly, like counting paths through a grid. The same table, run from both ends, tells each slice how to change its output.

## The problem

The input is a matrix of network outputs $u_t(k)$ for frames $t = 1, \ldots, T$ and symbols $k$ of the alphabet $L \cup \{\varnothing\}$, with $K = |L| + 1$ symbols in all. The blank is written $\varnothing$ in formulas, "_" in examples and index 0 in the code. The output distribution of frame $t$ is $y_t = \mathrm{softmax}(u_t)$. The model assumes that the outputs of different frames are independent given the input $x$. This is an assumption of the model, not a property of speech.

A path is a sequence $\pi \in (L \cup \{\varnothing\})^T$, with $p(\pi \mid x) = \prod_t y_t(\pi_t)$. The map $\mathcal{B}$ first merges each run of equal symbols into one and then deletes the blanks, so $\mathcal{B}(\mathrm{aa\_ab\_}) = \mathrm{aab}$. The order matters: blanks first would turn "a_a" into "a", but $\mathcal{B}(\mathrm{a\_a}) = \mathrm{aa}$. For a label sequence $l = l_1 \ldots l_U$ over $L$,

$$p(l \mid x) = \sum_{\pi : \mathcal{B}(\pi) = l} \ \prod_{t=1}^{T} y_t(\pi_t), \qquad \mathcal{L}_{\mathrm{CTC}} = -\ln p(l \mid x).$$

The task is to compute $\mathcal{L}_{\mathrm{CTC}}$ and its gradient with respect to every $u_t(k)$. Two copies of the same label need a blank between them, so a path exists only if $T \ge U + r$, where $r$ is the number of adjacent repeats in $l$. Otherwise the loss is $+\infty$.

## The algorithm

Insert a blank before, between and after the labels: $l' = \varnothing\, l_1\, \varnothing\, l_2 \ldots \varnothing\, l_U\, \varnothing$, with $S = 2U + 1$ states. A path moves through $l'$ from left to right. At each frame it stays, moves one state, or skips one blank, and it may skip a blank only if the two labels on its sides differ. The forward variable $\alpha_t(s)$ sums the path prefixes that are in state $s$ at frame $t$ and includes $y_t$. The backward variable $\beta_t(s)$ sums the suffixes after frame $t$ and does not include $y_t$. The arrays store natural logs; $\oplus$ is log_add, so $a \oplus b = \ln(e^a + e^b)$.

```pseudo id=main
CTC-LOSS(u, l)                ▷ u: T × K logits, l = l_1 .. l_U, ∅ = index 0, ln is the natural log
L1  ln y_t ← log-softmax(u_t) for every t;   l' ← ∅ l_1 ∅ l_2 .. ∅ l_U ∅,  S ← 2U + 1
L2  α_1(1) ← ln y_1(∅),  α_1(2) ← ln y_1(l_1),  α_1(s) ← -∞ for s ≥ 3
L3  for t ← 2 to T do for s ← 1 to S do
L4      a ← α_{t-1}(s) ⊕ α_{t-1}(s - 1);  if l'_s ≠ ∅ and l'_s ≠ l'_{s-2} then a ← a ⊕ α_{t-1}(s - 2)
L5      α_t(s) ← a + ln y_t(l'_s)
L6  ln p ← α_T(S) ⊕ α_T(S - 1)
L7  β_T(S) ← β_T(S - 1) ← 0, else -∞;  β_t(s) ← ⊕ over s' ∈ {s, s + 1, s + 2 if allowed} of (β_{t+1}(s') + ln y_{t+1}(l'_{s'}))
L8  g_t(k) ← y_t(k) - exp( ⊕_{s : l'_s = k} (α_t(s) + β_t(s)) - ln p )   for every t and k
L9  return -ln p and g
```

Line L4 is the whole structure of CTC. A path in state $s$ at frame $t$ was in $s$ (a repeat of the same symbol), in $s - 1$ (one step), or in $s - 2$ (a skip over a blank). The skip is not allowed into a blank, and it is not allowed between two equal labels, because "aa" without a blank between would merge into one "a". A path must start in the first blank or the first label (line L2) and end in the last label or the last blank (line L6).

Line L8 is the gradient of the loss with respect to the logits, $\partial \mathcal{L} / \partial u_t(k) = y_t(k) - \frac{1}{p} \sum_{s : l'_s = k} \alpha_t(s) \beta_t(s)$. This form holds with $\beta$ defined without frame $t$, as here. Graves et al. (2006) put $y_t$ inside their $\beta$, so their eq. (16) has an extra factor $1 / y_t(k)$ in the sum; the two forms are equal.

## Example

Take the alphabet {_, a, b}, the target "ab" and $T = 3$ frames with these outputs:

| frame | _ | a | b |
|---|---|---|---|
| 1 | 0.5 | 0.4 | 0.1 |
| 2 | 0.4 | 0.3 | 0.3 |
| 3 | 0.3 | 0.1 | 0.6 |

The extended sequence is $l' = $ _ a _ b _. Exactly 5 paths of length 3 collapse to "ab": _ab (0.09), a_b (0.096), aab (0.072), ab_ (0.036) and abb (0.072), so $p(\mathrm{ab} \mid x) = 0.366$. The forward table, in probabilities (the code stores the logs), gets the same number without listing the paths:

| $\alpha_t(s)$ | _ | a | _ | b | _ |
|---|---|---|---|---|---|
| $t = 1$ | 0.5 | 0.4 | 0 | 0 | 0 |
| $t = 2$ | 0.2 | 0.27 | 0.16 | 0.12 | 0 |
| $t = 3$ | 0.06 | 0.047 | 0.129 | 0.33 | 0.036 |

For example, $\alpha_2(\mathrm{b}) = (\alpha_1(\mathrm{b}) + \alpha_1(\_) + \alpha_1(\mathrm{a})) \cdot 0.3 = 0.4 \cdot 0.3 = 0.12$: the path may skip the blank from a to b because a and b differ. The answer is $\alpha_3(\mathrm{b}) + \alpha_3(\_) = 0.33 + 0.036 = 0.366$, and the loss is $-\ln 0.366 = 1.005122$ nats. The gradient for frame 1 is $(0.254098, -0.354098, 0.1)$ for (_, a, b): the loss falls if the network raises "a" at frame 1.

The example also shows that greedy decoding is not the same as finding the most probable labeling. The best symbol of each frame is _, _ and b, which reads "b", with $p(\mathrm{b} \mid x) = 0.294$. But "ab" has $p = 0.366$. Every single path of "ab" is less likely than the greedy path _ _ b (0.12), yet their sum is larger.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It first shows that the paths $\pi$ with $\mathcal{B}(\pi) = l$ are in one-to-one correspondence with the state sequences through $l'$ that obey the start, step, skip and end rules of lines L2, L4 and L6. Then an induction on $t$ shows that $\alpha_t(s)$ sums the valid prefixes that end in $s$, and a downward induction does the same for $\beta_t(s)$ and the suffixes. So $\alpha_t(s)\beta_t(s)$ is the total probability of the paths in state $s$ at frame $t$, and $\sum_s \alpha_t(s)\beta_t(s) = p(l \mid x)$ for every $t$. The gradient follows from the chain rule through the softmax, with $\sum_k \gamma_t(k) = p$ for $\gamma_t(k) = \sum_{s : l'_s = k} \alpha_t(s)\beta_t(s)$.

## Complexity

The softmax and the gradient cost $\Theta(K)$ per frame. The forward and backward passes cost a constant number of log_add operations per cell, and there are $T S = T(2U + 1)$ cells. The total is $\Theta(T(U + K))$ operations. Only the cells that lie on some complete path matter. They form a band whose width grows with the slack $T - U - r$, so a banded implementation saves time when $T$ is close to $U + r$.

The $\alpha$ and $\beta$ tables take $\Theta(T U)$ numbers; the gradient output itself takes $T K$. To compute only the loss, keep one column of $\alpha$, which takes $\Theta(U)$ memory. In practice a batch of utterances runs on a GPU, and the $\Theta(T)$ sequential steps of the recursion, not the arithmetic, limit the speed.

A product of a few hundred probabilities underflows in double precision. The test with $T = 300$, 30 equally likely symbols and the target "ab" has $p = 339746225 \cdot 30^{-300} \approx e^{-1000.7}$. The forward pass in probabilities returns 0.0, and the log-space pass returns $-1000.7155$, the exact value to 9 digits. Graves et al. (2006) rescale $\alpha$ and $\beta$ at each frame instead, which also works. This is why the page uses the floating-point model.

## Properties

- **Exact sum.** The forward pass gives $p(l \mid x)$ exactly in exact arithmetic (a theorem; see Correctness). It is the [forward algorithm](/forward-algorithm/) of a left-to-right HMM with $S$ states whose emissions are the network outputs.
- **Conditional independence.** The model treats the frames as independent given the input. A label can depend on the acoustic context through the network, but not on the other output labels. This is why CTC needs an external language model for good word accuracy, and why the [RNN transducer](/rnn-transducer/) adds a prediction network.
- **Monotone alignment.** Every path reads the labels in order, so CTC cannot model reordering. For speech this is right.
- **Peaky outputs.** A trained CTC network outputs the blank on most frames and each label on one or a few frames. This is an observation about trained models, not a theorem.
- **Gradient sums to zero per frame.** Because softmax ignores a shift of its inputs, $\sum_k \partial \mathcal{L} / \partial u_t(k) = 0$ for every frame.
- **Best path is not best labeling.** Greedy decoding takes the best symbol of each frame and applies $\mathcal{B}$. It finds the labeling of the most probable path, which is not in general the most probable labeling (Graves et al. 2006, Section 3.2); see the Example. [CTC prefix beam search](/ctc-prefix-beam-search/) sums over the paths of each prefix.

## Variants and improvements

- **Decoding.** Greedy (best path) decoding, prefix search (Graves et al. 2006), and [prefix beam search](/ctc-prefix-beam-search/) with a language model (Hannun et al. 2014). A WFST decoder can also compose a CTC "token" transducer with a lexicon and a grammar, in the style of the [HCLG graph](/hclg-decoding-graph/).
- **Viterbi alignment.** Replace $\oplus$ by $\max$ in lines L4 and L6 (the Viterbi semiring of nlslog). With [traceback](/traceback/) this gives the best path, a [forced alignment](/forced-alignment/) of the labels to the frames.
- **Joint CTC-attention.** Add the CTC loss to an attention encoder-decoder as an auxiliary loss, and combine the scores in decoding ([joint CTC-attention](/joint-ctc-attention/)).
- **Fine-tuning pretrained encoders.** [wav2vec 2.0](/wav2vec-2/) fine-tunes its pretrained encoder with a CTC loss on characters.
- **RNN transducer.** The [RNN transducer](/rnn-transducer/) removes the independence assumption with a prediction network over the previous labels, at the cost of a $T \times U$ lattice per joint output.

## When to use it

Use CTC when the input is much longer than the output, the order is monotone, and no alignment is given: speech recognition, handwriting recognition, and keyword spotting. It is simple, it trains fast, and greedy decoding is cheap and can run frame by frame. If the output labels depend strongly on each other, or if the outputs are words or long subwords, an attention model or a transducer usually gives a lower error rate without a language model. In many systems CTC is an auxiliary loss on the encoder of such a model.

## Pitfalls

- **Too few frames.** If $T < U + r$, no path exists and the loss is infinite. Subsampling the frames by 4 or 8 can cause this for fast speech or for character targets. Check the lengths, or drop such utterances.
- **The blank index.** The code here uses 0. Some toolkits use the last index. A mismatch trains a model that cannot output one of the labels.
- **The order of the collapse.** Merge repeats first, then delete blanks. The other order maps "a_a" to "a" and is wrong.
- **Products of probabilities.** Without log space or rescaling the forward pass underflows after a few hundred frames.
- **The two forms of the gradient.** Mixing the $\beta$ of Graves et al. (with $y_t$) and the $\beta$ of this page (without $y_t$) gives a gradient that is off by a factor $y_t(k)$. Test against finite differences.
- **Gradient with respect to what.** The formula of line L8 is the gradient with respect to the logits $u_t(k)$. With respect to $y_t(k)$ it is $-\gamma_t(k) / (p\, y_t(k))$. Do not apply a second softmax derivative on top of line L8.

## Implementations

The code takes the per-frame output logits of the network as given and implements the CTC loss, its gradient and greedy decoding; it does not train a network. A generic forward pass takes any semiring of nlslog, so the same code computes $p(l \mid x)$ (probability), $\ln p(l \mid x)$ (log), the best path (Viterbi) and the number of paths (counting).

## History

Graves, Fernández, Gomez and Schmidhuber (2006) introduced CTC to train bidirectional LSTM networks on unsegmented speech. On TIMIT phone recognition they measured a label error rate of 31.47% with best path decoding and 30.51% with prefix search, against 33.84% for a hybrid BLSTM/HMM system (their Table 1). Hannun, Maas, Jurafsky and Ng (2014) combined a CTC network with an n-gram language model through prefix beam search for large vocabulary recognition. CTC later became the fine-tuning loss of self-supervised speech encoders such as [wav2vec 2.0](/wav2vec-2/) (Baevski et al. 2020) and an auxiliary loss of attention models.

## References
