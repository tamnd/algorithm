---
tag: 90WS5S
kind: model
slug: triphone-model
name: Triphone model
aliases:
- context-dependent phone model
area: natural-language-and-speech/speech-recognition
level: core
summary: A phone model that depends on the phones to its left and right, which captures coarticulation at the cost of many more models.
prereqs: [gmm-hmm-acoustic-model, pronunciation-lexicon]
see_also: [phonetic-decision-tree-state-tying, hclg-decoding-graph, agglomerative-clustering, forced-alignment, viterbi-training, hybrid-dnn-hmm, weighted-transducer-composition, grapheme-to-phoneme-conversion]
sources:
  - paper: doi:10.1109/ICASSP.1985.1168283
    title: R. Schwartz, Y. Chow, O. Kimball, S. Roucos, M. Krasner and J. Makhoul, Context-dependent modeling for acoustic-phonetic recognition of continuous speech, ICASSP '85, IEEE International Conference on Acoustics, Speech, and Signal Processing 10, 1985, pages 1205 to 1208
    locator: the phone models that depend on the left and the right phone, and their combination with less specific models
  - paper: doi:10.1109/29.52701
    title: Kai-Fu Lee, Context-dependent phonetic hidden Markov models for speaker-independent continuous speech recognition, IEEE Transactions on Acoustics, Speech, and Signal Processing 38(4), 1990, pages 599 to 609
    locator: the generalized triphones, which merge similar triphone models by a bottom-up clustering
  - paper: "Steve J. Young, Julian J. Odell and Philip C. Woodland, Tree-based state tying for high accuracy acoustic modelling, Human Language Technology: Proceedings of a Workshop held at Plainsboro, New Jersey, 1994, pages 307 to 312 (ACL Anthology H94-1062)"
    locator: the comparison of state tying with model tying, and the cross-word triphones of the Wall Street Journal system
  - paper: doi:10.1561/2000000004
    title: Mark Gales and Steve Young, The application of hidden Markov models in speech recognition, Foundations and Trends in Signal Processing 1(3), 2008, pages 195 to 304
    locator: the section on context-dependent phone models
---

A triphone model is an HMM for one phone in the context of its left and right neighbors, written l-p+r for the phone p after l and before r. The sound of a phone changes with its neighbors, because the mouth moves toward the next sound while it makes the current one (coarticulation), and a model per context captures this. With about 40 phones there are up to $40^3 = 64\,000$ triphones, and most of them are rare or absent in any training set, so their states are tied, usually by [phonetic decision trees](/phonetic-decision-tree-state-tying/). Schwartz et al. 1985 used such models in an early continuous speech system, and tied-state triphones became the standard units of [GMM-HMM](/gmm-hmm-acoustic-model/) and [hybrid](/hybrid-dnn-hmm/) recognizers.

## The machine

Fix a phone set $\Phi$ of size $P$. A monophone model has one HMM for each phone. A triphone model has one HMM for each triple $(l, p, r) \in \Phi^3$ that it needs, with the same topology as a monophone, for example three emitting states in a left-to-right chain with Gaussian mixture emissions.

**Expanding a phone sequence.** The [pronunciation lexicon](/pronunciation-lexicon/) turns a word sequence into phones. Each phone $\phi_i$ then becomes the triphone $\phi_{i-1}\text{-}\phi_i\text{+}\phi_{i+1}$. For example, "cat" with the phones k ae t, between two silences, becomes

$$\text{sil-k+ae}, \quad \text{k-ae+t}, \quad \text{ae-t+sil}.$$

**Word-internal and cross-word.** A word-internal system uses the context only inside a word, and at the word edges it uses a biphone or a monophone. A cross-word system also uses the last phone of the previous word and the first phone of the next word. The cross-word context depends on the word sequence, so the decoder must expand it during the search; in the weighted transducer view, the context transducer C of the [HCLG decoding graph](/hclg-decoding-graph/) does this.

**Tying.** The model shares parameters between triphones. Generalized triphones (Lee 1990) merge whole triphone models by a bottom-up clustering. Tied states (Young, Odell and Woodland 1994) share the output distribution of corresponding states. A decision tree for each phone and state position puts each state of each triphone in a cluster, and the cluster has one Gaussian mixture. A triphone that never occurs in training still gets a model, because the tree gives a cluster for every context.

**Training.** A common recipe trains monophones first, uses them to align the data by [forced alignment](/forced-alignment/), clones each monophone into all the triphones seen in the data, collects one Gaussian per state, builds the trees from those statistics, and then retrains the tied states with more mixture components.

## What it counts

The model counts the parameters it needs and the data each one gets. With $P$ phones there are up to $P^3$ triphones and $3 P^3$ states. Without tying, the training data is spread over all of them: if a corpus has $F$ frames, an average state gets $F / (3 P^3)$ frames, and the distribution of the counts is very skewed, with many states that get no frames at all. Tying to $K$ clusters gives each cluster about $F / K$ frames. Systems use a few thousand tied states. Young, Odell and Woodland 1994 used about 1600 on Resource Management, and the right number depends on the data, which makes it a heuristic choice.

The cost of a triphone model in decoding is the larger search space. A cross-word triphone recognizer must keep apart the hypotheses that differ in the last phone of a word, because the next phone depends on it.

## Relation to other models

- **Monophones and biphones.** A monophone model ignores the context and a biphone model uses one side only. Each is a triphone model with all the contexts of a phone tied together on one or both sides, and both serve as back-off models for rare contexts.
- **Wider contexts.** Quinphone models use two phones on each side. They need still more tying, and the decision trees ask questions about the outer phones as well.
- **[GMM-HMM acoustic model](/gmm-hmm-acoustic-model/).** The triphone model is the choice of units, and the GMM-HMM is the model of each unit. The two choices are independent.
- **[Hybrid DNN-HMM](/hybrid-dnn-hmm/).** Uses the tied triphone states as the output classes of its neural network.
- **[Agglomerative clustering](/agglomerative-clustering/).** The generalized triphones of Lee 1990 cluster bottom up. They cannot give a model to a triphone that did not occur in the training data.
- **Graphemes.** For languages with regular spelling, letters in the context of their neighbors (trigraphemes) can replace triphones, and then no lexicon of phones is needed.

## Known results in the model

- **Context helps.** Schwartz et al. 1985 found that triphone models, combined with less specific models for rare contexts, recognize phones better than context-independent models. This and the later results are measurements on the systems and corpora of each paper.
- **State tying against model tying.** Young, Odell and Woodland 1994 reported that tying states gave 3 to 20 percent fewer word errors than tying whole models, 14 percent on average (measurements).
- **Decision trees against bottom-up clustering.** In the same paper, about 1600 tree-tied states gave a word error rate of 3.87 percent on the Resource Management Feb'89 test set, against 4.10 percent for bottom-up clustering (measurements).
- **The count of contexts.** With $P$ phones, the number of possible triphones is $P^3$, and in a lexicon of real words only a fraction of them occur. Any finite training set leaves some possible cross-word triphones unseen, so a triphone system needs a rule for unseen contexts. The decision tree is such a rule; this is a structural fact of the model, not a measurement.

## References
