---
tag: V3PXA1
kind: model
slug: source-channel-speech-recognition
name: Source-channel model of speech recognition
aliases:
- fundamental equation of speech recognition
area: natural-language-and-speech/speech-recognition
level: intro
summary: Choose the word sequence W that maximizes P(O | W) P(W), an acoustic model times a language model, for the acoustic features O.
prereqs: [automatic-speech-recognition, bayes-theorem, language-model]
see_also: [noisy-channel-spelling-correction, gmm-hmm-acoustic-model, n-gram-language-model, hybrid-dnn-hmm, hclg-decoding-graph, maximum-mutual-information-training, shallow-fusion, word-error-rate]
sources:
  - paper: doi:10.1109/PROC.1976.10159
    title: Frederick Jelinek, Continuous speech recognition by statistical methods, Proceedings of the IEEE 64(4), 1976, pages 532 to 556
    locator: the view of the speaker and the acoustic processor as a noisy channel, and the decoding rule
  - paper: doi:10.1109/TPAMI.1983.4767370
    title: Lalit R. Bahl, Frederick Jelinek and Robert L. Mercer, A maximum likelihood approach to continuous speech recognition, IEEE Transactions on Pattern Analysis and Machine Intelligence PAMI-5(2), 1983, pages 179 to 190
    locator: the communication theory view of recognition, with the text generator, the speaker, the acoustic processor and the linguistic decoder
  - book: isbn:9780262100663
    title: Frederick Jelinek, Statistical Methods for Speech Recognition, MIT Press, 1997
    locator: Chapter 1 (the mathematical formulation of speech recognition)
  - paper: doi:10.1561/2000000004
    title: Mark Gales and Steve Young, The application of hidden Markov models in speech recognition, Foundations and Trends in Signal Processing 1(3), 2008, pages 195 to 304
    locator: the chapter on the architecture of an HMM-based recognizer
---

The source-channel model treats speech recognition as the decoding of a noisy channel. A source, the speaker's language, produces a word sequence $W$ with probability $P(W)$, and a channel, the speaker's voice and the front end, turns it into acoustic features $O = o_1 \ldots o_T$ with probability density $p(O \mid W)$. The recognizer outputs $W^* = \arg\max_W p(O \mid W) P(W)$, the product of an acoustic model and a [language model](/language-model/). Jelinek 1976 and Bahl, Jelinek and Mercer 1983 stated speech recognition in this form, and it was the frame of almost all recognizers until neural end-to-end models.

## The machine

The model is a generative story with four parts.

1. **The source.** A language model gives the prior $P(W)$ of each word sequence $W = w_1 \ldots w_U$. An [n-gram model](/n-gram-language-model/) writes $P(W) = \prod_u P(w_u \mid w_{u-n+1} \ldots w_{u-1})$.
2. **The channel.** An acoustic model gives the density $p(O \mid W)$ of the frames for each word sequence. In an HMM recognizer it is built from the [pronunciation lexicon](/pronunciation-lexicon/), which turns $W$ into phones, and from the phone HMMs, for example a [GMM-HMM acoustic model](/gmm-hmm-acoustic-model/) with [triphones](/triphone-model/): $p(O \mid W) = \sum_Q p(O, Q \mid W)$ over the state paths $Q$ of the HMM of $W$.
3. **The decoder.** By [Bayes' theorem](/bayes-theorem/), $P(W \mid O) = p(O \mid W) P(W) / p(O)$, and $p(O)$ is the same for every $W$, so
$$W^* = \arg\max_W P(W \mid O) = \arg\max_W p(O \mid W)\, P(W).$$
4. **The training.** The two models are trained apart: the acoustic model on audio with transcripts, and the language model on text alone, which is available in much larger amounts.

In practice the decoder uses the Viterbi approximation $p(O \mid W) \approx \max_Q p(O, Q \mid W)$, and it works in log space with two extra constants:

$$W^* = \arg\max_W \Big( \log p(O \mid W) + \alpha \log P(W) + \beta\, |W| \Big).$$

The language model weight $\alpha > 1$ and the word insertion penalty $\beta$ are tuned on development data. They correct for the acoustic model, which treats the frames as independent given the states and so is much too confident. This is a heuristic, not a consequence of the model.

## What it counts

The model scores a hypothesis $W$ by $\log p(O \mid W) + \log P(W)$, and the decision rule picks the best score. If the two models were the true distributions, this rule would minimize the probability of a sentence error, that is, of any error in $W$ (a theorem of Bayes decision theory). It does not minimize the expected number of word errors, which is what the [word error rate](/word-error-rate/) counts. A minimum Bayes risk decoder, for example one that picks the best path of a [confusion network](/confusion-network/), targets the word errors.

The cost of the model is the cost of the search. With the Viterbi approximation, an n-gram language model and HMMs, the search is a best path problem in one large graph, the [HCLG decoding graph](/hclg-decoding-graph/), with one layer per frame. The time is linear in $T$ times the number of arcs, and decoders prune it with a [beam](/time-synchronous-beam-search/).

## Relation to other models

- **Noisy channel spelling correction.** [Noisy channel spelling correction](/noisy-channel-spelling-correction/) uses the same decomposition: a language model of the intended words times an error model of the typed letters. The statistical machine translation of the IBM group used it as well.
- **Hybrid models.** A [hybrid DNN-HMM](/hybrid-dnn-hmm/) gives state posteriors $P(q \mid o_t)$, not the likelihoods $p(o_t \mid q)$. Dividing by the state priors gives scaled likelihoods, which the source-channel decoder uses unchanged. The model stays the same, and only the estimate of the channel changes.
- **Discriminative training.** [Maximum mutual information training](/maximum-mutual-information-training/) trains the acoustic model to raise $P(W \mid O)$ of the correct transcript, computed through the source-channel product. It keeps the decoding rule and changes the training goal.
- **Direct models.** [CTC](/connectionist-temporal-classification/), the [RNN transducer](/rnn-transducer/) and [Listen, Attend and Spell](/listen-attend-and-spell/) model $P(W \mid O)$ directly with one network. They can add an external language model by [shallow fusion](/shallow-fusion/), a log-linear sum that looks like the source-channel score but has no prior to divide out.
- **HMM decoding.** With the Viterbi approximation, the decision rule is [HMM decoding](/hmm-decoding/) on the HMM of all the word sequences that the language model allows.

## Known results in the model

- **The decision rule.** For the 0-1 loss on whole sentences, the rule $\arg\max_W P(W \mid O)$ is optimal among all decision rules, if the probabilities are the true ones (a theorem). With estimated models this is no longer a guarantee.
- **Exact decoding is hard.** The exact rule sums over the state paths of each word sequence. Finding the most probable string emitted by a hidden Markov model is NP-hard (Lyngsø and Pedersen 2002, a theorem), so the exact rule is not computed. The Viterbi approximation of the joint best path takes time linear in $T$ times the size of the graph.
- **Separate training.** The acoustic model and the language model have separate maximum likelihood estimates, because $\log p(O \mid W) P(W)$ splits into two terms with separate parameters. This is why a language model can be changed without retraining the acoustic model.
- **Measured accuracy.** Systems of this form reached word error rates of a few percent on read speech with a vocabulary of 5000 words, for example 4.90 percent on the Wall Street Journal Nov'93 5k test (Young, Odell and Woodland 1994, a measurement).

## References
