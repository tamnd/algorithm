---
tag: YCRS0W
kind: algorithm
slug: span-ranking-coreference
name: End-to-end span-ranking coreference
aliases:
- e2e-coref
- Lee coreference model
area: natural-language-and-speech/tagging-and-information-extraction
level: research
summary: "Score every span up to a width as a mention, prune, score each span with its candidate antecedents and a dummy of score 0, train on the marginal likelihood of gold antecedents, then link."
solves: [coreference-resolution]
model: word-ram
complexity:
  vars: {n: the number of tokens, w: the maximum span width, k: the number of antecedents kept per span}
  time: {worst: "O(n w log(n w) + n^2 w + n k)"}
  space: {extra: "O(n w + n k)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2017
  people: [Kenton Lee, Luheng He, Mike Lewis, Luke Zettlemoyer]
  note: "Lee et al. 2017 gave the first coreference model that finds the mentions and the antecedents together, with no parser and no mention detector."
prereqs: [coreference-resolution, mention-pair-model, cross-entropy-loss]
see_also: [b-cubed-metric, contextual-word-embedding, bert, log-sum-exp-trick, correlation-clustering, semi-markov-crf, scaled-dot-product-attention, named-entity-recognition]
sources:
  - paper: doi:10.18653/v1/D17-1018
    title: "Kenton Lee, Luheng He, Mike Lewis and Luke Zettlemoyer, End-to-end neural coreference resolution, Proceedings of EMNLP 2017, pages 188 to 197"
    locator: "Section 3 (the task and the antecedent sets with the dummy), Section 4 (the span representations and the scores s_m and s_a), Section 5 (pruning with width L, ratio lambda, K antecedents and the crossing rule), Section 6 (the marginal log likelihood), Section 7 (L = 10, lambda = 0.4, K = 250), the results table on the CoNLL-2012 English test set"
  - paper: "Sameer Pradhan, Alessandro Moschitti, Nianwen Xue, Olga Uryupina and Yuchen Zhang, CoNLL-2012 shared task: modeling multilingual unrestricted coreference in OntoNotes, Proceedings of the Joint Conference on EMNLP and CoNLL: Shared Task, 2012, pages 1 to 40"
    title: Pradhan et al. 2012
    locator: the English data set and the official score, the mean of the MUC, B-cubed and CEAF-e F1 values
  - paper: doi:10.3115/v1/P14-2006
    title: "Sameer Pradhan, Xiaoqiang Luo, Marta Recasens, Eduard Hovy, Vincent Ng and Michael Strube, Scoring coreference partitions of predicted mentions: a reference implementation, ACL 2014 (short papers), pages 30 to 35"
    locator: the reference scorer used for the numbers on this page
---

The end-to-end span-ranking model of Lee, He, Lewis and Zettlemoyer (2017) solves [coreference resolution](/coreference-resolution/) without a parser and without a separate mention detector. It treats every span of a document up to a fixed width as a possible mention, gives each span a mention score, keeps the best spans, and lets each kept span choose one antecedent among the spans before it, or a dummy antecedent $\varepsilon$ that means "no antecedent". Training maximizes the marginal likelihood of all gold antecedents, so no single gold antecedent has to be chosen. The [mention-pair model](/mention-pair-model/) classifies pairs on their own; this model ranks the candidate antecedents of a span against each other with a softmax, and it learns the mentions at the same time.

## In plain words

Every short stretch of words could be a mention. The network gives each stretch a score that says how much it looks like a mention, and it keeps only the best ones, a fixed fraction of the document length. Then each kept stretch looks back at the stretches before it and gives each a score for "this one refers to the same thing as me". There is also a fixed option with score 0 that means "I start something new, or I am not a mention at all". The stretch picks its highest scoring option. Linked stretches form the groups. In training, the network is rewarded for putting probability on any correct earlier stretch, not on one fixed choice.

## The problem

Input: a document of $n$ tokens, with speaker and genre information if the data has it. A span $(a, b)$ covers the tokens $a + 1, \ldots, b$ (fencepost indices, $0 \le a < b \le n$). Output: a set of disjoint clusters of spans, where the spans of a cluster refer to the same entity. Spans that are in no cluster of size two or more are not output. In the CoNLL-2012 data (Pradhan et al. 2012) singletons are not annotated, so this matches the data.

The model gives each span $i$ an antecedent $y_i \in Y(i) = \{\varepsilon, 1, \ldots, i - 1\}$, where the spans are ordered by start and then by end. With the score $s(i, \varepsilon) = 0$ and

$$s(i, j) = s_m(i) + s_m(j) + s_a(i, j),$$

it takes the antecedents of different spans to be independent:

$$P(y_1, \ldots, y_N) = \prod_{i=1}^{N} \frac{\exp s(i, y_i)}{\sum_{y' \in Y(i)} \exp s(i, y')}.$$

The mention score $s_m(i)$ and the antecedent score $s_a(i, j)$ come from feed-forward networks (Lee et al. 2017, Section 4). The span representation joins the outputs of a bidirectional LSTM at the first and last token of the span, an attention-weighted sum of the word vectors of the span (a learned "head"), and a feature for the width. The pair network sees the two span representations, their elementwise product, and features for the speaker, the genre and the distance. Fixing the dummy score at 0 makes the scores relative: a span links to $j$ only if $s(i, j) > 0$ beats all other options.

With all $O(n^2)$ spans and all pairs, the model has $O(n^4)$ pair scores. Pruning makes it practical.

## The algorithm

The code takes the mention scores and pair scores of the network as given and implements the pruning, the antecedent distribution, the loss with its gradient, and the decoder. Logs are natural logs.

```pseudo id=main
SPAN-RANKING-COREF(n, s_m, s_a, L, λ, K, gold clusters)
L1  S ← all spans (a, b) with 0 ≤ a < b ≤ n and b - a ≤ L
L2  sort S by s_m, highest first (ties by start, then end)
L3  M ← empty; for each span t of S while |M| < floor(λ n): if t crosses no span of M then add t to M
L4  sort M by start, then by end; call its spans 1 .. m
L5  for i ← 1 to m do Y(i) ← ε and the up to K nearest spans of M before i
L6      s(i, ε) ← 0; s(i, j) ← s_m(i) + s_m(j) + s_a(i, j) for each other j in Y(i)
L7      log P(y | i) ← s(i, y) - log Σ_{y' in Y(i)} exp s(i, y')
L8      G(i) ← the spans of Y(i) in the gold cluster of i, or ε alone if there are none
L9      loss ← loss - log Σ_{y in G(i)} P(y | i)
L10     ŷ_i ← the first y of Y(i) with the largest s(i, y), ε first
L11 link each i with ŷ_i ≠ ε to the cluster of ŷ_i; return the clusters of two or more spans and the loss
```

Two spans $(a, b)$ and $(c, d)$ cross when $a < c < b < d$ or $c < a < d < b$: they overlap and neither holds the other. This is the rule of Section 5 of the paper, written with fencepost indices. Nested spans, such as "the president of the company" and "the company", may both be kept.

The gradient of the loss with respect to the score of a pair is $P(y \mid i) - Q(y \mid i)$, where $Q$ is $P$ restricted to $G(i)$ and renormalized. The network then passes this into $s_m$ and $s_a$ by the chain rule: $s_m(k)$ gets the sum over all pairs that contain $k$.

The paper gives only the maximum number $K$ of antecedents. The code keeps the $K$ nearest earlier spans. The paper sets $L = 10$, $\lambda = 0.4$ and $K = 250$ (Section 7), chosen for the CoNLL-2012 data; these are settings, not derived values.

## Example

Take "Alice met Bob and she smiled", with $n = 6$, $L = 2$, $\lambda = 0.75$ and $K = 3$. There are 11 spans of width 1 or 2. Say the network gives the mention scores Alice $(0, 1)$: 2.0, she $(4, 5)$: 1.8, "met Bob" $(1, 3)$: 1.6, "Alice met" $(0, 2)$: 1.55, Bob $(2, 3)$: 1.5, and $-3$ to every other span. The limit is $\lfloor 0.75 \cdot 6 \rfloor = 4$ spans.

Pruning takes Alice, she and "met Bob". "Alice met" crosses "met Bob" ($0 < 1 < 2 < 3$), so it is skipped. Bob is nested in "met Bob", so it is kept, and $M$ is full. In order, $M$ = Alice, "met Bob", Bob, she. The pruning kept a span that is not a mention, "met Bob"; the antecedent scores have to deal with it.

Let the pair scores be $s_a$ = 1.0 for (she, Alice), $-2.5$ for (she, Bob), and $-5$ or $-4$ for the other pairs. For "she" the four options score:

| antecedent | score | $P$ |
|---|---|---|
| $\varepsilon$ | 0 | 0.0080 |
| Bob | $1.8 + 1.5 - 2.5 = 0.8$ | 0.0178 |
| "met Bob" | $1.8 + 1.6 - 5 = -1.6$ | 0.0016 |
| Alice | $1.8 + 2.0 + 1.0 = 4.8$ | 0.9726 |

"Met Bob" scores $-1.4$ against Alice, and Bob scores $-1.9$ against "met Bob" and $-0.5$ against Alice, so both pick $\varepsilon$. The output is one cluster, {Alice, she}. With the gold cluster {Alice, she}, the loss is $\log(1 + e^{-1.4}) + \log(1 + e^{-1.9} + e^{-0.5}) + (\log(1 + e^{0.8} + e^{-1.6} + e^{4.8}) - 4.8) = 0.2204 + 0.5631 + 0.0278 = 0.8113$.

With $K = 2$, "she" sees only Bob and "met Bob". It links to Bob, because $0.8 > 0$. Its gold antecedent was cut off, so $G(\text{she}) = \{\varepsilon\}$, its loss term grows to 1.2318, and the training signal now asks "she" to start a new entity. The test file checks all these numbers.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows four things. The kept spans are at most $\lfloor \lambda n \rfloor$ and no two of them cross. The loss is the negative log of the total probability of all full antecedent assignments that agree with the gold clusters, because the model is a product over spans and the sum of a product over a product set factorizes. The gradient is $P - Q$ as above. The decoder returns a most probable assignment, since each factor can be maximized alone, and the links form a forest because each link points to an earlier span, so the clusters are well defined. The test file checks the loss against the sum over all assignments, the gradient against central finite differences, and the decoder against all assignments.

The model itself carries no guarantee: the scores come from a trained network, and the quality of the clusters is a measurement.

## Complexity

There are at most $n L$ spans. Sorting them costs $O(n L \log(n L))$. The crossing test in the code compares each span with the up to $\lambda n$ kept spans, $O(n^2 L)$ in total; a structure over the kept spans can make this faster, but it is not the bottleneck in practice. After pruning, the $\lfloor \lambda n \rfloor$ spans have at most $K$ candidates each, so scoring, the loss, the gradient and the decoding take $O(n K)$ pair evaluations of the network. Without pruning, all spans and all pairs give $O(n^4)$ pair scores (Lee et al. 2017, Section 4). The YAML uses $w$ for $L$ and $k$ for $K$.

## Properties

- The loss is a sum of one term per span, $\log Z_i - \log Z_i^G$, where $Z_i$ sums $\exp s(i, y)$ over $Y(i)$ and $Z_i^G$ over $G(i)$. This is the difference of two log-sum-exp functions of the scores. It is convex in the scores when $G(i)$ has one element, but not in general when a span has several gold antecedents, and it is not convex in the network weights.
- The decoder is exact for the model (a theorem, proved above), but the model ignores the constraint that clusters are transitive in a global sense: each span chooses alone, and the clusters are the connected components of the choices. Exact clustering under pairwise scores is [correlation clustering](/correlation-clustering/), which is NP-hard (Bansal, Blum and Chawla 2004); the model avoids it by its independence assumption.
- Measured accuracy (a measurement): on the CoNLL-2012 English test set, the single model of Lee et al. (2017) scored 67.2 average F1 (MUC 75.8, B-cubed 65.0, CEAF-phi4 60.8), and an ensemble of 5 models scored 68.8. The paper reports more than 92% recall of the gold mentions after pruning with $\lambda = 0.4$.
- Training truncates long documents: the paper keeps at most 50 sentences per document in training.

## Variants and improvements

- Higher-order inference and coarse-to-fine pruning: Lee, He and Zettlemoyer (2018, NAACL) refine the span representations with the expected antecedent and add a cheap bilinear score to prune antecedents before the full pair network.
- Better encoders: replacing the LSTM with [BERT](/bert/) or SpanBERT, which masks whole spans in pretraining, raised the CoNLL-2012 scores a great deal in later work; these gains are measurements of the encoder, not of the span-ranking algorithm.
- Mention-ranking models before 2017, for example by Wiseman, Rush, Shieber and Weston (2015) and Clark and Manning (2016), used the same antecedent softmax over gold or predicted mentions from a separate detector.
- Entity-level models score a span against a partial cluster instead of one antecedent, which brings back some transitivity at a higher cost.

## When to use it

Use the span-ranking model, or one of its descendants with a pretrained encoder, as the default for English coreference in data like OntoNotes. Use the [mention-pair model](/mention-pair-model/) to explain the basic ideas, or where little training data and no neural encoder are available. For pronouns alone with parse trees, the [Hobbs algorithm](/hobbs-algorithm/) is a strong rule-based baseline.

## Pitfalls

- Gold antecedents cut by pruning: if $K$ or $\lambda$ is too small, the gold set of a span becomes $\{\varepsilon\}$, and the loss teaches the model to say "new entity" for a mention that has an antecedent. The example above shows this with $K = 2$.
- Spans ordered differently: the antecedent set must follow the same span order in training and decoding. The paper orders by start and then by end.
- Underflow and overflow: the softmax must be computed in log space. A score of 900 makes $\exp$ overflow in double precision; the test file has such a case.
- Singletons: the CoNLL-2012 data has no singleton clusters, so spans with $\hat y = \varepsilon$ and no later link are dropped from the output. On data with singletons the output rule must change.
- Comparing scores: the CoNLL score depends on the scorer version. Use the reference scorer of Pradhan et al. (2014).

## Implementations

The code takes the mention and pair scores of the network as given and implements the pruning, the loss, its gradient and the decoding; it does not train a network.

## History

Before 2017, coreference systems first found mentions with a parser or a separate detector and then linked them. Mention-ranking models such as those of Denis and Baldridge (2008), Durrett and Klein (2013) and Wiseman et al. (2015) had already replaced pairwise classification with a softmax over candidate antecedents. Lee, He, Lewis and Zettlemoyer (2017) removed the pipeline: they scored all spans, pruned them by a learned mention score, and trained the whole model from the marginal likelihood of the gold antecedents. Their model and code became the base of most neural coreference systems that followed, including those with ELMo, BERT and SpanBERT encoders.

## References
