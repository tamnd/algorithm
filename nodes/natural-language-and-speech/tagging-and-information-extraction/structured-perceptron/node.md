---
tag: KYD1XY
kind: algorithm
slug: structured-perceptron
name: Structured perceptron
aliases:
- Collins perceptron
area: natural-language-and-speech/tagging-and-information-extraction
level: core
summary: Decode each training sentence by Viterbi and add the features of the gold tags minus those of the predicted tags; averaged in practice.
solves: [sequence-labeling]
model: word-ram
complexity:
  vars: {n: the total number of training tokens, k: the number of tags, t: the number of epochs, d: the number of features}
  time: {worst: "Θ(t n k^2)"}
  space: {extra: "O(n + d)"}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 2002
  people: [Michael Collins]
  note: "Collins applied the perceptron with Viterbi decoding to tagging and chunking at EMNLP 2002, with mistake bounds and the averaged variant."
prereqs: [perceptron, viterbi-algorithm, sequence-labeling]
see_also: [hmm-part-of-speech-tagger, maximum-entropy-markov-model, conditional-random-field, structured-prediction, bilstm-crf, text-chunking, beam-search, support-vector-machine]
sources:
  - paper: "Michael Collins, Discriminative training methods for hidden Markov models: theory and experiments with perceptron algorithms, Proceedings of the 2002 Conference on Empirical Methods in Natural Language Processing (EMNLP 2002), pages 1 to 8"
    title: Collins 2002
    locator: "Figure 1 (the tagging algorithm), Figure 2 (the general algorithm), Section 2.5 (averaged parameters), Section 3 (Definition 1 and Theorem 1 on separable data, Theorem 2 on inseparable data, Theorem 3 on generalization), Section 4 (part-of-speech tagging and NP chunking experiments)"
---

The structured perceptron learns the weights of a linear scoring function over whole tag sequences. For each training sentence it finds the best tag sequence under the current weights with the [Viterbi algorithm](/viterbi-algorithm/). If that sequence is wrong, it adds the feature counts of the gold sequence to the weights and subtracts those of the predicted sequence. It is the [perceptron](/perceptron/) with the argmax over $k$ classes replaced by an argmax over $k^n$ tag sequences. Unlike the [HMM tagger](/hmm-part-of-speech-tagger/) it does not estimate probabilities, so features can overlap freely, and unlike the [conditional random field](/conditional-random-field/) it needs no forward-backward pass, only decoding.

## In plain words

The tagger gives points to each small fact about a tagged sentence, such as "the word dog has tag N" or "tag N follows tag D". The score of a tagging is the sum of its points. To learn the points, go through the training sentences one by one. Find the tagging with the most points. If it is the right one, do nothing. If it is wrong, give one more point to each fact of the right tagging and take one point away from each fact of the wrong one. Facts that both taggings share cancel out. Repeat over the data a few times. In practice, use the average of the points over all steps, which makes the tagger much more stable on new text.

## The problem

Input: training pairs $(x_i, y_i)$, $i = 1, \ldots, N$, of sentences and gold tag sequences over $k$ tags; a feature map $\Phi(x, y) \in \mathbb{R}^d$; a number of epochs $T$. Output: a weight vector $w$ such that the tagger $F(x) = \arg\max_{y \in \mathrm{GEN}(x)} w \cdot \Phi(x, y)$ makes few errors. $\mathrm{GEN}(x)$ is the set of all $k^n$ tag sequences for a sentence of $n$ words.

To decode by dynamic programming, $\Phi$ must be a sum of local feature vectors, each depending on the words, the position $j$ and a few neighbouring tags. The code uses first-order features: one count for each transition $(y_{j-1}, y_j)$, with $y_0 = \langle s \rangle$ and $y_{n+1} = \langle /s \rangle$, and one for each pair (tag, word). Collins uses trigram tag features and the word features of Ratnaparkhi's maximum entropy tagger (suffixes, prefixes, capitalization, nearby words), which works the same way with a decoder over pairs of tags.

## The algorithm

```pseudo id=main
PERCEPTRON-TRAIN((x_1, y_1) .. (x_N, y_N), T)
L1  w ← 0; u ← 0; c ← 0                       ▷ u and c keep the average lazily
L2  for epoch ← 1 to T do
L3      for i ← 1 to N do
L4          z ← VITERBI(x_i, w)                ▷ argmax over z of w · Φ(x_i, z)
L5          if z ≠ y_i then
L6              d ← Φ(x_i, y_i) - Φ(x_i, z)
L7              w ← w + d; u ← u + c d
L8          c ← c + 1
L9  return w and the averaged weights w - u / c
```

The averaged weights are the mean of the weights after each of the $T N$ examples (Collins 2002, Section 2.5). Summing $w$ after every example costs $O(d)$ per example. The code uses the identity $\frac{1}{J} \sum_{j=1}^{J} w_j = w_J - \frac{1}{J} \sum_{i} (i - 1) d_i$, so each update costs only the size of $d$. The decoder breaks ties by taking the first tag in a fixed order, which makes the whole run deterministic.

## Example

Use the tags D, J, N, V in that order and three training sentences: "the/D runs/N", "dogs/N run/V" and "the/D dog/N runs/V". All weights start at 0.

1. "the runs": all taggings score 0, and the tie rule picks D D. The update adds 1 to $(D, N)$, (N, runs) and $(N, \langle /s \rangle)$, and subtracts 1 from $(D, D)$, (D, runs) and $(D, \langle /s \rangle)$. The shared features $(\langle s \rangle, D)$ and (D, the) cancel.
2. "dogs run": the decoder picks D N with score 2, using the weight of $(D, N)$ and $(N, \langle /s \rangle)$ from step 1. The gold is N V, so a second update follows. It moves $(D, N)$ back to 0 and $(N, \langle /s \rangle)$ back to 0.
3. "the dog runs": the decoder picks N V N with score 3. A third update adds, among others, 1 to (V, runs) and subtracts 1 from (N, runs).

In epoch 2, "the runs" comes out as D V, since (V, runs) is now 1 and (N, runs) is 0, and the fourth update fixes this. The other two sentences are right. Epoch 3 has no mistakes, so the mistakes per epoch are 3, 1, 0. The averaged weights are means over 9 steps, for example $14/9$ for the transition $(D, N)$ and $8/9$ for (N, runs); they also tag all three sentences correctly. The test file checks a run like this one on a larger corpus.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) has three parts. First, the score is a sum of local terms, so Viterbi returns a sequence of the highest score (a theorem; the test file compares it with a search over all $k^n$ sequences). Second, Collins's Theorem 1: if some unit vector $U$ separates the data with margin $\delta$, so that $U \cdot \Phi(x_i, y_i) - U \cdot \Phi(x_i, z) \ge \delta$ for all wrong $z$, and $\lVert \Phi(x_i, y_i) - \Phi(x_i, z) \rVert \le R$, then the algorithm makes at most $R^2 / \delta^2$ mistakes in total, however many epochs it runs. The proof is the one of Novikoff for the binary perceptron: each mistake raises $U \cdot w$ by at least $\delta$, while $\lVert w \rVert^2$ grows by at most $R^2$, since the predicted $z$ scored at least as high as $y_i$. Note that the bound does not depend on the number of sequences in $\mathrm{GEN}(x)$, which grows as $k^n$. Third, the lazy average is equal to the direct average, which the test file checks in exact rational arithmetic.

## Complexity

Each training step decodes one sentence. With first-order features, Viterbi takes $\Theta(n_i k^2)$ time for a sentence of $n_i$ words, so one epoch over $n$ tokens takes $\Theta(n k^2)$ time and $T$ epochs take $\Theta(T n k^2)$, plus the cost of computing the features. An update touches at most $O(n_i)$ features. With second-order features, as in Collins's experiments, decoding takes $\Theta(n_i k^3)$. Space is the $d$ weights and the second vector $u$ for the average, plus $O(n_i k)$ for the decoder. On separable data, Theorem 1 also bounds the number of updates by $R^2/\delta^2$, but the bound is often very loose: in the test file the runs make 0 to 18 mistakes against bounds between about 1300 and 20000.

## Properties

- Online and mistake-driven: it looks at one example at a time and changes $w$ only on a mistake.
- No learning rate: scaling all weights does not change the argmax, so a step size other than 1 gives the same predictions when $w$ starts at 0.
- Exact decoding is required by the proof: with an approximate decoder such as [beam search](/beam-search/), the predicted $z$ may score lower than $y_i$, and the upper bound step fails. Collins and Roark (2004) add an early update for this case.
- Not probabilistic: the scores are not normalized, so the model gives no marginal probabilities or confidence.
- Measured (Collins 2002, Section 4): on Penn Treebank part-of-speech tagging the averaged perceptron had an error rate of 2.89% against 3.28% for a maximum entropy tagger with the same features, and on NP chunking an F-measure of 93.63 against 93.29.

## Variants and improvements

- Averaged perceptron. The average of all weight vectors, as here. Collins motivates it as an approximation to the voted perceptron of Freund and Schapire (1999), and it gave clear gains over the last weight vector in his experiments.
- Voted perceptron. Each intermediate weight vector votes with a weight equal to the number of examples it survived; Collins's Theorem 3 bounds its expected error on new data.
- Inseparable data. Collins's Theorem 2 bounds the number of mistakes in terms of how far the data is from separable.
- Margin methods. MIRA and the structured [support vector machine](/support-vector-machine/) also learn from decoded outputs, but choose the step to reach a margin; [structured prediction](/structured-prediction/) covers them.
- Other structures. The same algorithm works for any output with an exact argmax: parse trees with a CKY decoder, segmentations with a [semi-Markov decoder](/semi-markov-crf/), [dependency parsing](/dependency-parsing/) and so on.
- Probabilistic training. Replacing the perceptron update by the gradient of the log likelihood gives the [conditional random field](/conditional-random-field/); the perceptron update is a subgradient step on a loss that uses the max where the CRF uses log-sum-exp.

## When to use it

Use the structured perceptron for a fast and simple discriminative tagger or chunker with rich, overlapping features, when you only need the best output and not probabilities. It is easy to implement on top of any exact decoder, needs no tuning of a learning rate, and trains in a few epochs. Use a CRF when you need calibrated probabilities or marginals, and a neural model such as the [BiLSTM-CRF](/bilstm-crf/) when you want learned features.

## Pitfalls

- Use the averaged weights for testing. The last weight vector depends strongly on the order of the last examples.
- Shuffle the data between epochs, or at least do not sort it by type; the result depends on the order.
- Ties in the decoder: with all-zero weights every sequence ties. A fixed tie rule keeps runs reproducible; the update is still correct whatever the tie rule is.
- The bound is for exact decoding. With a beam, a wrong output may score lower than the gold output, and the update can make things worse.
- The gold and the predicted sequences usually share most of their features, and these cancel in $\Phi(x, y) - \Phi(x, z)$. Compute the update as a sparse difference, not with dense vectors.
- The convergence result says nothing about new text. Run a fixed number of epochs and choose it on held-out data.

## Implementations

## History

Rosenblatt introduced the perceptron in 1958, and Novikoff proved its mistake bound for separable data in 1962. Freund and Schapire (1999) studied the voted perceptron and its averaged form. Collins (2002) brought the algorithm to sequence tasks: he replaced the argmax over classes by Viterbi decoding over tag sequences, proved that the bounds carry over with a margin and a radius defined on whole sequences, and showed that the averaged perceptron beats a maximum entropy tagger with the same features on part-of-speech tagging and NP chunking. The method became a standard way to train taggers and parsers in the following decade.

## References
