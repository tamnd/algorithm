---
tag: YB908J
kind: technique
slug: shallow-fusion
name: Shallow fusion
aliases:
- external language model fusion
area: natural-language-and-speech/speech-recognition
level: advanced
summary: Add a weighted external language model log-probability to the score of an end-to-end recognizer at each step of beam search.
prereqs: [beam-search, encoder-decoder-model, n-gram-language-model]
see_also: [listen-attend-and-spell, rnn-transducer, connectionist-temporal-classification, ctc-prefix-beam-search, length-normalization, lattice-rescoring, recurrent-neural-network-language-model, perplexity]
sources:
  - url: https://arxiv.org/abs/1503.03535
    title: Caglar Gulcehre, Orhan Firat, Kelvin Xu, Kyunghyun Cho, Loic Barrault, Huei-Chi Lin, Fethi Bougares, Holger Schwenk and Yoshua Bengio, On using monolingual corpora in neural machine translation, 2015
    locator: Section 4.1 and equation 5 for shallow fusion, Section 4.2 for deep fusion, Section 6.2.1 for the tuned weight, Table 4 for the WMT-15 results
  - paper: doi:10.1109/ICASSP.2018.8462682
    title: Anjuli Kannan, Yonghui Wu, Patrick Nguyen, Tara N. Sainath, Zhifeng Chen and Rohit Prabhavalkar, An analysis of incorporating an external language model into a sequence-to-sequence model, ICASSP 2018
    locator: the abstract, which defines shallow fusion as log-linear interpolation with a separately trained language model at each step of the beam search and gives the 9.1% relative reduction of the word error rate
---

Shallow fusion adds an external language model to an end-to-end recognizer or translator at decoding time. The end-to-end model, such as an attention [encoder-decoder](/encoder-decoder-model/) or an [RNN transducer](/rnn-transducer/), gives $\log p_{e2e}(y_t \mid x, y_{<t})$ for the next token. The language model is trained separately on text alone and gives $\log p_{lm}(y_t \mid y_{<t})$. At each step of [beam search](/beam-search/), each candidate token gets the score $\log p_{e2e}(y_t \mid x, y_{<t}) + \lambda \log p_{lm}(y_t \mid y_{<t})$, and the beam keeps the hypotheses with the best sums. Nothing is trained jointly: only the weight $\lambda$, and often a length reward, are tuned on held-out data. Gulcehre et al. 2015 named the method for machine translation, and Kannan et al. 2018 studied it for speech recognition.

## In plain words

An end-to-end recognizer learns how words sound from paired audio and text, and there is never enough of that. Text alone is easy to get in very large amounts, and a language model trained on it knows which word sequences are likely.

Shallow fusion lets the two models vote during the search. At every step, each possible next word gets a score from the recognizer and a score from the language model, and the two scores are added with a weight. The recognizer stays as it was. The language model also stays as it was. Only the weight, and the search, are new.

## When it applies

- Both models give scores over the same tokens, for example the same word pieces or characters, so that the two scores can be added token by token.
- The language model is trained on text that is close to the target domain. The gain is largest when the domain of the paired data is narrow or different.
- The decoder is a left-to-right beam search: label-synchronous for attention models, or frame-synchronous for a transducer or [CTC](/connectionist-temporal-classification/), where the language model score is added each time a hypothesis emits a non-blank token, as in [CTC prefix beam search](/ctc-prefix-beam-search/).

## The template

1. **Train the two models apart.** The end-to-end model on paired data, the language model on text with the same token set.
2. **Score each extension.** For a hypothesis $y_{<t}$ in the beam and a candidate token $k$, compute
   $s(y_{<t} k) = s(y_{<t}) + \log p_{e2e}(k \mid x, y_{<t}) + \lambda \log p_{lm}(k \mid y_{<t})$.
   Gulcehre et al. 2015 first take the top candidates by the translation model score and then add the language model term to them. Their equation 5 writes the weight as $\beta$.
3. **Add a length term.** The language model term is a negative number for each token, so a larger $\lambda$ favors short outputs. Add a reward $\gamma$ for each token, or divide by the length ([length normalization](/length-normalization/)), and tune $\gamma$ with $\lambda$.
4. **Keep the best $B$ hypotheses** by the fused score, and continue until each hypothesis ends with the end-of-sentence token. The language model also scores that token.
5. **Tune $\lambda$ and $\gamma$** on held-out data by the error rate, not by the likelihood.

**What it computes.** With $\gamma = 0$, the search looks for $\arg\max_y \log p_{e2e}(y \mid x) + \lambda \log p_{lm}(y)$, a log-linear mix of the two models over whole sentences. Because both scores factor token by token, the fused score of a prefix is exact for every prefix in the beam. The method stays approximate only in the way every beam search is approximate: it can drop a prefix that the fused score would later prefer.

**Cost.** One language model step per hypothesis and step, with the same beam. For a neural language model this can double the cost of decoding. For an n-gram model the cost is small.

## Classic examples

**A homophone.** The recognizer hears "there" or "their" after "I like" with $p_{e2e}(\text{there}) = 0.55$ and $p_{e2e}(\text{their}) = 0.45$. The language model, given the history, prefers "their": $p_{lm}(\text{there}) = 0.2$ and $p_{lm}(\text{their}) = 0.7$.

| $\lambda$ | score of "there" | score of "their" | best |
|---|---|---|---|
| 0 | $-0.598$ | $-0.799$ | there |
| 0.3 | $-0.598 + 0.3 \cdot (-1.609) = -1.081$ | $-0.799 + 0.3 \cdot (-0.357) = -0.906$ | their |
| 1 | $-2.207$ | $-1.155$ | their |

The choice changes when $\lambda = \ln(0.55 / 0.45) / \ln(0.7 / 0.2) \approx 0.160$. Any weight above that lets the language model overrule the acoustic preference here.

**Speech recognition with a word-piece language model.** Kannan et al. 2018 added a neural language model over word pieces to an attention model for Google voice search. They report a 9.1% relative reduction of the word error rate, with no need for a second rescoring pass.

**Translation.** In Gulcehre et al. 2015, on the WMT-15 tasks, shallow fusion gave gains of 0.09 and 0.29 BLEU on German to English and Czech to English. Deep fusion, which joins the hidden states of the two networks, gave 0.39 and 0.47.

## Variations

- **Deep fusion.** Join the hidden states of the language model and the decoder with a trained gate (Gulcehre et al. 2015, Section 4.2). This needs a further training step.
- **Cold fusion.** Train the end-to-end model with a fixed language model already attached, so that it learns to use it.
- **Internal language model correction.** An end-to-end model learns an implicit language model of its training text. Subtract an estimate of it, $- \mu \log p_{ilm}(y_t \mid y_{<t})$, before adding the external model, to help in a new domain.
- **Fusion with an n-gram model or a WFST.** Use an n-gram model, or a graph with a lexicon, as the external model. This also allows the boosting of a list of words or phrases, such as contact names.
- **Rescoring instead.** Add the language model only to the final list of hypotheses or to a lattice ([lattice rescoring](/lattice-rescoring/)). This is cheaper but can only choose among the hypotheses that the beam kept.

## Pitfalls

- **Different token sets.** If the language model uses words and the recognizer uses word pieces, the scores cannot be added step by step without a mapping.
- **Short outputs.** A large $\lambda$ without a length reward makes the search stop early or drop words.
- **Double counting.** The end-to-end model already contains a language model of its training text. In the same domain, adding an external one helps less, and too large a weight hurts.
- **Weight transfer.** The best $\lambda$ depends on the domain, the beam width and the length reward. Tune them together on held-out data from the target domain.
- **Blank steps.** In CTC and transducer decoding, add the language model score only when a token is emitted, never on a blank.
- **End of sentence.** Score the end-of-sentence token with the language model too, or the fused model prefers hypotheses that never end.

## Exercises

1. Check the flip point $\lambda \approx 0.160$ in the example, and show that in general the choice flips at $\lambda = \ln(a_1/a_2) / \ln(l_2/l_1)$ when $a_1 > a_2$ and $l_2 > l_1$.
2. Show that with $\gamma = 0$, the fused score of a full hypothesis is $\log p_{e2e}(y \mid x) + \lambda \log p_{lm}(y)$.
3. Two hypotheses have the end-to-end score $-0.2$ per token, but one has 5 tokens and the other has 7. Each language model token score is $-2$. Find the length reward $\gamma$ for which the fused scores of the two are the same when $\lambda = 0.5$.
4. Explain why shallow fusion with a beam of width 1 can give a different output from rescoring a list of the 8 best hypotheses with the same $\lambda$.
5. In CTC prefix beam search, explain where in the update the language model term goes, and why it must not be added on the blank or repeated-token paths that do not extend the prefix.

## References
