---
tag: XJ8G58
kind: algorithm
slug: mention-pair-model
name: Mention-pair coreference model
aliases:
- Soon mention-pair model
area: natural-language-and-speech/tagging-and-information-extraction
level: core
summary: "Classify each pair of mentions as coreferent or not, then link each mention to its closest (or most probable) earlier mention classified as coreferent."
solves: [coreference-resolution]
model: word-ram
complexity:
  vars: {n: the number of mentions in the document, d: the number of features of a pair}
  time: {worst: "O(n^2 d)"}
  space: {extra: "O(n)"}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 2001
  people: [Wee Meng Soon, Hwee Tou Ng, Daniel Chung Yong Lim, Vincent Ng, Claire Cardie]
  note: "Soon, Ng and Lim (2001) gave the standard learned pairwise model with closest-first linking; Ng and Cardie (2002) added best-first linking and more features."
prereqs: [coreference-resolution, logistic-regression, disjoint-set]
see_also: [span-ranking-coreference, hobbs-algorithm, correlation-clustering, b-cubed-metric, agglomerative-clustering, named-entity-recognition, precision-and-recall]
sources:
  - paper: doi:10.1162/089120101753342653
    title: "Wee Meng Soon, Hwee Tou Ng and Daniel Chung Yong Lim, A machine learning approach to coreference resolution of noun phrases, Computational Linguistics 27(4), 2001, pages 521 to 544"
    locator: "Section 2.2 (the 12 features), Section 2.3 (the training pairs), Section 2.4 (the C5 decision tree), Section 2.5 (closest-first linking), the MUC-6 and MUC-7 results"
  - paper: doi:10.3115/1073083.1073102
    title: "Vincent Ng and Claire Cardie, Improving machine learning approaches to coreference resolution, ACL 2002, pages 104 to 111"
    locator: "Section 3 (best-first clustering, the new training pairs, the split string match features), Table 2 (MUC-6 and MUC-7 results)"
  - paper: doi:10.1023/B:MACH.0000033116.57574.95
    title: "Nikhil Bansal, Avrim Blum and Shuchi Chawla, Correlation clustering, Machine Learning 56, 2004, pages 89 to 113"
    locator: the NP-hardness of correlation clustering on complete graphs with positive and negative edges
---

The mention-pair model splits [coreference resolution](/coreference-resolution/) into two steps. A classifier looks at one pair of mentions at a time and gives the probability that they refer to the same entity. A linker then walks through the document and gives each mention at most one antecedent among the earlier mentions, and the entities are the groups of linked mentions. Soon, Ng and Lim (2001) made this the standard learned approach, with a decision tree on 12 features and closest-first linking. It is simple and fast, and it is the base that later methods improved on: the [span-ranking model](/span-ranking-coreference/) replaces the independent pair decisions by a softmax over the candidate antecedents and learns the mentions too.

## In plain words

For every mention, look back at the mentions before it, one by one, starting with the nearest. For each earlier mention, a trained classifier says how likely it is that both name the same thing, using clues such as the same words, the same gender and number, or a pronoun close by. In the Soon version, link the mention to the nearest earlier mention that the classifier accepts. In the Ng and Cardie version, link it to the accepted one with the highest probability. Mentions that are linked, directly or through others, form one entity.

## The problem

Input: the mentions $0, 1, \ldots, N - 1$ of a document in text order, already found (by a parser, a chunker or a named entity tagger), and for training, gold chains. A feature function $\phi(i, j)$ describes a pair $i < j$. Output: a partition of the mentions into entities.

Soon et al. (2001, Section 2.2) use 12 features of a pair: the sentence distance, whether $i$ is a pronoun, whether $j$ is a pronoun, string match after removing articles and demonstratives, whether $j$ is a definite NP, whether $j$ is a demonstrative NP, number agreement, semantic class agreement, gender agreement, whether both are proper names, whether one is an alias of the other, and whether $j$ is in apposition to $i$.

## The algorithm

```pseudo id=main
MENTION-PAIR(mentions 0 .. N-1, gold chains, features φ)
L1  for each mention j with an earlier mention of its chain: i ← the closest such mention
L2      add (i, j) as a positive pair, and (k, j) as a negative pair for each i < k < j
L3  train a classifier p(i, j) = P(coreferent | φ(i, j)) on these pairs
L4  for j ← 1 to N-1 do
L5      for i ← j-1 downto 0 do
L6          if p(i, j) > 0.5 then link j to i and stop this loop      ▷ closest first
L7  return the connected components of the links (union-find)
```

Soon et al. train a C5 decision tree (Section 2.4). The code trains logistic regression by gradient descent instead; the linker only needs a probability. Ng and Cardie (2002, Section 3) change two steps:

- Best first: instead of line L6, link $j$ to the $i$ with the highest $p(i, j)$ among those above 0.5. The code breaks ties toward the closest $i$.
- Training pairs: for a non-pronominal anaphor, the positive pair uses the closest non-pronominal mention of its chain, because a name is a more reliable antecedent for a name than a pronoun is; for a pronoun, the closest mention of its chain, as before. Negatives are the mentions between the two, as in Soon et al. The paper does not say what to do with mentions of the same chain that lie between them; the code skips them so that no coreferent pair is labeled negative.

The threshold 0.5 is the decision rule of a probabilistic classifier, not a tuned value. Ng and Cardie turn the leaf counts of the tree into a smoothed probability.

## Example

Take "Mary met John. He gave her a book. Mary thanked him." and the first six mentions: Mary (0), John (1), He (2), her (3), a book (4) and Mary (5). The gold chains are {0, 3, 5}, {1, 2} and {4}.

Training pairs of Soon et al.: He (2) has the closest antecedent John (1), so (1, 2) is positive. Her (3) has the closest antecedent Mary (0), so (0, 3) is positive and (1, 3) and (2, 3) are negative. Mary (5) has the closest antecedent her (3), so (3, 5) is positive and (4, 5) is negative. Ng and Cardie instead pair Mary (5) with Mary (0) as the positive pair, since 5 is a name; the negatives are (1, 5), (2, 5) and (4, 5), and her (3) is skipped as a chain mate.

Now suppose the classifier gives these probabilities, with 0.05 for every pair that contains "a book":

| pair | (0,1) | (0,2) | (1,2) | (0,3) | (1,3) | (2,3) | (0,5) | (1,5) | (2,5) | (3,5) |
|---|---|---|---|---|---|---|---|---|---|---|
| $p$ | 0.10 | 0.20 | 0.90 | 0.80 | 0.30 | 0.52 | 0.95 | 0.10 | 0.10 | 0.40 |

Closest first: He (2) links to John (1). Her (3) tries He (2) first, and $0.52 > 0.5$, so it links to He, which is wrong. A book (4) finds nothing. Mary (5) tries her (0.40), a book, He, John, and links to Mary (0). The entities are {0, 5}, {1, 2, 3} and {4}.

Best first: her (3) takes the highest of 0.80, 0.30 and 0.52, which is Mary (0). The entities are {0, 3, 5}, {1, 2} and {4}, which is the gold partition.

The classifier is not transitive here: it accepts (2, 3) and (0, 3) but rejects (0, 2). Linking every accepted pair and closing it would give one big entity {0, 1, 2, 3, 5}. The test file checks all of this.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows that the training pairs have the right labels (no mention between the closest antecedent and the anaphor can be in its chain), that the gradient of the logistic loss is $\frac{1}{m} \sum (\sigma(w \cdot x) - y) x + \lambda w$, that closest first returns $\max\{i < j : p(i, j) > 0.5\}$ and best first the most probable $i$ above 0.5, and that the links form a forest, so the output is a partition. It also gives the example of non-transitive decisions.

The model has no guarantee of finding the best partition. Finding the partition that agrees most with weighted pairwise decisions is [correlation clustering](/correlation-clustering/), which is NP-hard (Bansal, Blum and Chawla 2004). Closest first and best first are greedy heuristics.

## Complexity

With $n$ mentions and $d$ features per pair, closest first classifies up to $j$ pairs for mention $j$, so $O(n^2 d)$ in the worst case; it often stops early. Best first always classifies all $n(n-1)/2$ pairs, $\Theta(n^2 d)$. The union-find step takes near linear time. Training builds $O(n^2)$ pairs per document in the worst case, but only $O(n \cdot g)$ when the gaps between chain mates are at most $g$ mentions. Many systems limit the search to a window of a few sentences.

## Properties

- Online in the mentions: each mention is resolved when it is reached, using only earlier mentions.
- Local decisions: each pair is classified without looking at the other mentions of the entity, so the model cannot use entity-level facts such as "this entity already has a female pronoun".
- Not transitive: the pairwise decisions need not be consistent; the linker makes the output a partition.
- Measured accuracy (a measurement, MUC score, with mentions found by the system): Soon et al. report recall 58.6, precision 67.3 and F 62.6 on MUC-6, and 56.1, 65.5 and 60.4 on MUC-7. Ng and Cardie report up to F 70.4 on MUC-6 (with RIPPER and hand-selected features) and 63.4 on MUC-7 (with C4.5), in their Table 2.

## Variants and improvements

- Best-first linking and new training pairs (Ng and Cardie 2002), as above. In their Table 2 each change alone gives a small effect, and the gain comes with the other changes and the features.
- Aggressive merge: link every pair above the threshold and take the transitive closure. It finds more links but can chain errors together.
- Global clustering: solve [correlation clustering](/correlation-clustering/) approximately, or use [agglomerative clustering](/agglomerative-clustering/) on the pair scores.
- Mention ranking and entity models: rank all candidate antecedents of a mention together, or score a mention against a whole partial entity. The [span-ranking model](/span-ranking-coreference/) is a neural mention-ranking model.

## When to use it

Use the mention-pair model to learn or teach coreference, as a baseline, or where you need a small, fast model with readable features. For the best accuracy on large annotated data, use a neural model such as the [span-ranking model](/span-ranking-coreference/). For pronouns alone with parse trees and no training data, the [Hobbs algorithm](/hobbs-algorithm/) is a rule-based option.

## Pitfalls

- Class imbalance: most pairs are not coreferent. The Soon pair selection keeps the negatives near the anaphor, which keeps the imbalance in check; using all pairs makes it much worse.
- Training and testing must match: the training pairs of Soon et al. teach the classifier about the closest antecedent, which suits closest first. Ng and Cardie changed the training pairs together with best first for this reason.
- Transitive closure of errors: one wrong link can merge two large entities. The MUC score penalizes such a merge only lightly; the [B-cubed metric](/b-cubed-metric/) penalizes it more.
- Mentions found by the system: errors in finding mentions limit recall and precision. Compare numbers only with the same mention detection and the same scorer.

## Implementations

## History

Rule-based methods such as the [Hobbs algorithm](/hobbs-algorithm/) resolved pronouns from syntax. In the 1990s, the MUC-6 and MUC-7 evaluations made coreference of all noun phrases a task with annotated data, and learned pairwise classifiers appeared (McCarthy and Lehnert 1995, and Aone and Bennett 1995, among others). Soon, Ng and Lim (2001) gave the version that became the standard baseline, with 12 simple features and closest-first linking, and they were the first learned system to reach results close to the best systems of MUC-6 and MUC-7. Ng and Cardie (2002) improved it with best-first linking, new training pairs and many more features.

## References
