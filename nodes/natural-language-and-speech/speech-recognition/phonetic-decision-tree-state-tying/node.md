---
tag: 7CSFNE
kind: algorithm
slug: phonetic-decision-tree-state-tying
name: Phonetic decision tree state tying
aliases:
- tree-based state tying
area: natural-language-and-speech/speech-recognition
level: advanced
summary: Cluster triphone HMM states by a tree of yes or no questions about phone context, splitting greedily by likelihood gain.
model: real-ram
complexity:
  vars: {n: the number of triphone states in the pool, q: the number of questions, d: the dimension of the features, k: the number of leaves}
  time: {worst: "O(q n d k + k^3 d)"}
  space: {extra: "O(n d + q)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1994
  people: [Steve J. Young, Julian J. Odell, Philip C. Woodland]
  note: Young, Odell and Woodland tied the states of triphone HMMs by phonetic decision trees, with a split rule that needs only the occupancy, mean and variance of each state, and showed that the trees give models for triphones that do not occur in the training data.
prereqs: [triphone-model, decision-tree]
see_also: [gmm-hmm-acoustic-model, agglomerative-clustering, greedy-algorithm, maximum-likelihood-estimation, bayesian-information-criterion, minimum-description-length, viterbi-training, hybrid-dnn-hmm]
sources:
  - paper: "Steve J. Young, Julian J. Odell and Philip C. Woodland, Tree-based state tying for high accuracy acoustic modelling, Human Language Technology: Proceedings of a Workshop held at Plainsboro, New Jersey, 1994, pages 307 to 312 (ACL Anthology H94-1062)"
    locator: equations (1) to (3) for the likelihood and the split rule, Table 2 for the Resource Management results, and the Wall Street Journal results
  - paper: doi:10.1561/2000000004
    title: Mark Gales and Steve Young, The application of hidden Markov models in speech recognition, Foundations and Trends in Signal Processing 1(3), 2008, pages 195 to 304
    locator: the section on context-dependent phone models and decision tree clustering
  - paper: doi:10.1109/29.52701
    title: Kai-Fu Lee, Context-dependent phonetic hidden Markov models for speaker-independent continuous speech recognition, IEEE Transactions on Acoustics, Speech, and Signal Processing 38(4), 1990, pages 599 to 609
    locator: the generalized triphones, an earlier bottom-up clustering of triphone models
---

Phonetic decision tree state tying clusters the HMM states of [triphone models](/triphone-model/), so that states with similar acoustics share one output distribution. For each phone and each state position, it puts all the triphone states into one root node and splits the nodes by yes or no questions about the left and the right phone, for example "is the left phone a nasal?". Each split takes the question that most increases the log likelihood of the training frames under one Gaussian per node, and the splits stop when the gain falls below a threshold. Each leaf becomes one tied state, and a triphone that never occurs in the training data still reaches a leaf by its answers to the questions.

## In plain words

A recognizer that models each sound in the context of its two neighbors has tens of thousands of such sounds, and most of them occur only a few times in the training data, or never. So you group the contexts that sound alike and train one model per group.

To find the groups, start with all the contexts of one sound in one group. Ask a list of questions about the neighbors, such as "is the sound on the left a vowel?". Each question splits the group in two. Keep the question that makes the two halves fit the data best, and repeat on each half. Stop when no question helps enough. A new context that was never in the training data answers the same questions and lands in one of the groups, so it still gets a model.

## The problem

The input is the pool of triphone states of one base phone and one state position, for example the middle state of every triphone of "ae". State $s$ has a context (a left phone $l_s$ and a right phone $r_s$) and the statistics of its training frames from a [Viterbi](/viterbi-training/) or Baum-Welch alignment: the occupancy $N_s$, the mean $\mu_s$ and the diagonal variance $\sigma^2_s$, each of dimension $d$. There is also a list of questions. A question asks whether the left phone, or the right phone, is in a given set of phones, such as the nasals or the vowels.

For a set $S$ of states, let $L(S)$ be the log likelihood of all their frames under one diagonal Gaussian fitted to them by maximum likelihood. With natural logs,

$$L(S) = -\tfrac{1}{2} N(S) \Big( d \log(2 \pi) + \sum_{k=1}^{d} \log \sigma^2_k(S) + d \Big),$$

where $N(S) = \sum_{s \in S} N_s$ and the pooled variance is $\sigma^2_k(S) = \sum_s N_s (\sigma^2_{s,k} + \mu_{s,k}^2) / N(S) - \mu_k(S)^2$. So $L(S)$ needs only the statistics of the states and not the frames. The gain of a question $Q$ at a node $S$ is

$$\Delta(Q, S) = L(S_{\text{yes}}) + L(S_{\text{no}}) - L(S).$$

The task is a partition of the pool into tied states, one per leaf of a tree of questions, with a large total likelihood and with enough data in each leaf. The best such tree is not computed: the method is greedy.

## The algorithm

```pseudo id=main
BUILD-TREE(states, questions, θ, n_min)
L1  leaves ← [a root node with all the states]
L2  repeat
L3      for each new leaf: cand[leaf] ← the question with the largest gain Δ such that both sides have occupancy ≥ n_min
L4      ℓ ← the leaf with the largest candidate gain
L5      if no leaf has a candidate, or the gain of ℓ is below θ, then stop
L6      split ℓ by its question into a yes child and a no child, and record the question at ℓ
L7  return the tree and its leaves

MERGE(leaves, θ)
L8  while there are at least two clusters do
L9      find the pair a, b with the smallest loss L(a) + L(b) - L(a ∪ b)
L10     if that loss is at least θ then stop
L11     replace a and b by a ∪ b
```

Line L3 computes the candidate of the root first and then of each pair of new children. A question that puts all the states on one side is not a candidate. Ties go to the first question in the list. After the tree, the merge stage can join two leaves from different branches, which the tree alone cannot do. The function tie of the code runs both and returns the tied state of each triphone.

To find the tied state of a triphone, seen or unseen, start at the root of the tree of its base phone and state position, and follow its answers down to a leaf. The function classify of the code does this.

## Example

Take the middle state of four triphones of "ae", with $d = 1$, and three questions: "is the left phone a vowel?" (L_vowel), "is the right phone a nasal?" (R_nasal) and "is the right phone t?" (R_t). The threshold is $\theta = 5$ and $n_{\min} = 50$.

| state | $N_s$ | $\mu_s$ | $\sigma^2_s$ |
|---|---|---|---|
| k-ae+t | 100 | 1.0 | 0.5 |
| t-ae+k | 80 | 1.2 | 0.5 |
| iy-ae+t | 60 | 3.0 | 0.4 |
| aa-ae+n | 60 | 2.8 | 0.6 |

The root has $N = 300$, mean $1.813333$ and variance $1.297156$, so $L = -464.71$. The three questions give:

| question | yes side | $L(\text{yes})$ | $L(\text{no})$ | gain |
|---|---|---|---|---|
| L_vowel | iy-ae+t, aa-ae+n | -129.87 | -194.79 | 140.05 |
| R_nasal | aa-ae+n | -69.81 | -359.10 | 35.80 |
| R_t | k-ae+t, iy-ae+t | -253.95 | -209.63 | 1.13 |

The yes side of L_vowel has $N = 120$, mean $2.9$ and variance $0.51$, and the no side has $N = 180$, mean $1.088889$ and variance $0.509877$. The root splits by L_vowel. In the vowel child the best question is R_nasal with a gain of 2.41, and in the other child it is R_t with a gain of 1.76. Both are below $\theta = 5$, so the tree stops with two leaves: {iy-ae+t, aa-ae+n} and {k-ae+t, t-ae+k}. The merge stage would lose 140.05 by joining them, so it does nothing. The unseen triphone uw-ae+m answers yes to L_vowel, if uw is in the vowel set, and shares the model of the first leaf.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows four facts, all theorems.

- The pooled statistics of a set of states equal the mean and the variance of the union of their frames, so the split rule can work from statistics alone.
- $L(S)$ has the closed form above: at the maximum likelihood estimate, the quadratic term of the Gaussian log density sums to $N(S)\, d$ over the frames.
- The gain is never negative, because the two children can always use the parameters of the parent, and their own maximum likelihood estimates are at least as good.
- The tree that line L4 grows does not depend on the order in which the leaves split, if there is no limit on the number of leaves, because the decision at a leaf depends only on its states. The total log likelihood of the leaves is $L(\text{root})$ plus the sum of the gains of the splits, and every context reaches exactly one leaf.

The tree is not optimal. The proof gives an example in which the mean depends on the exclusive or of two questions: no single question has any gain, so the greedy tree stops at the root, while the tree with two levels gains a lot. The test test_greedy_misses_an_xor_context checks this.

## Complexity

A node with $n_v$ states evaluates $q$ questions, and each one pools the statistics of $n_v$ states in $O(n_v d)$ time. Each state is in one node per level of the tree, and the depth is less than $k$, so the tree takes $O(q n d k)$ time. In practice the tree is balanced enough that the depth is about $\log k$, and the time is close to $O(q n d \log k)$. The merge stage with cached cluster statistics takes $O(k^2 d)$ time per merge and $O(k^3 d)$ in all. The code recomputes the pooled statistics in each step, which is simpler and slower.

The space is the statistics of the states, $O(n d)$, the questions and the tree. A recognizer builds one tree for each phone and each state position, and each tree uses only the states of its pool, so the trees are independent and can be built in parallel.

## Properties

- **Statistics only.** The split rule needs $N_s$, $\mu_s$ and $\sigma^2_s$ of each state, and no frames. One alignment of the training data with single Gaussian untied triphones gives these statistics.
- **Unseen contexts.** Every left and right phone answers every question, so every triphone has a leaf, including the ones that never occur in the training data. Bottom-up clustering of the seen triphones has no rule for the unseen ones.
- **Phonetic knowledge.** The questions encode phonetic classes, such as nasals, fricatives or front vowels. The algorithm chooses which ones matter from the data.
- **Greedy.** Each split is the best one locally, and the result can miss structure that needs two questions together.
- **Heuristic thresholds.** The threshold $\theta$ and the minimum occupancy $n_{\min}$ set the number of tied states. They are tuned on development data, and the right values depend on the amount of data and on the features.

## Variants and improvements

- **Questions on a wider context.** The same method ties the states of quinphones, with questions about the phones two places away, and it can ask about word boundaries or stress.
- **One tree per phone.** Some systems build one tree for all the states of a phone, or for all phones, with questions about the state position and the base phone. This shares data between the positions.
- **Stopping rules from model selection.** A penalty from the [Bayesian information criterion](/bayesian-information-criterion/) or [minimum description length](/minimum-description-length/) in place of a fixed $\theta$ gives a threshold that grows with the number of parameters.
- **Gaussian mixtures after tying.** The trees use one Gaussian per state. After tying, the recognizer splits each tied state into a mixture of Gaussians and retrains it, as in a [GMM-HMM acoustic model](/gmm-hmm-acoustic-model/).
- **Neural acoustic models.** A [hybrid DNN-HMM](/hybrid-dnn-hmm/) uses the tied states of a GMM-HMM tree as its output classes, so the trees are still part of such systems.
- **Bottom-up clustering.** [Agglomerative clustering](/agglomerative-clustering/) of the seen triphones, as in the generalized triphones of Lee 1990, is the older method.

## When to use it

Use tree-based state tying for context-dependent HMM acoustic models when the number of contexts is much larger than the data can support, and when the recognizer must handle contexts that the training data does not contain, as in large vocabulary recognition across word boundaries. With a small vocabulary and enough data per word, whole word models need no tying.

## Pitfalls

- **Poor statistics.** The statistics come from an alignment. If the alignment is poor, the trees cluster noise. Align with a good model first.
- **The variance floor.** A state with very few frames, or with identical frames, has a variance near 0, and its log likelihood goes to $+\infty$. Floor the variances, and use the minimum occupancy.
- **A threshold in the wrong units.** The gain is a sum over frames, so it scales with the amount of data. A threshold tuned on one corpus does not transfer to a corpus of a different size.
- **A poor question set.** The tree can only use the classes in the questions. Include single phones as well as broad classes.
- **Expecting the global optimum.** The tree is greedy, and the merge stage only partly repairs this.

## Implementations

## History

Before decision trees, systems clustered triphone models bottom up: Lee 1990 merged similar triphone models into generalized triphones. Young, Odell and Woodland 1994 tied states and not whole models, and built the clusters top down with phonetic decision trees, with one tree for each state of each phone and a set of 202 questions. They stopped the splits by a threshold on the gain and a minimum occupancy, and then merged leaves, which reduced the number of states by 10 to 20 percent. These counts are from the paper. On the Resource Management Feb'89 test set, about 1600 tied states gave a word error rate of 3.87 percent, against 4.10 percent for bottom-up clustering (a measurement). On the Wall Street Journal Nov'93 tests the system had 4.90 percent errors on the 5k task and 12.67 percent on the 20k task (measurements). The method, as implemented in HTK and later in Kaldi, became the standard way to build context-dependent acoustic models (Gales and Young 2008).

## References
