---
tag: 3YEMMH
kind: definition
slug: b-cubed-metric
name: B-cubed metric
aliases:
- B3 coreference score
area: natural-language-and-speech/tagging-and-information-extraction
level: advanced
summary: Coreference precision and recall averaged over mentions, from the overlap of the predicted and gold clusters that hold each mention.
prereqs: [coreference-resolution, precision-and-recall]
see_also: [span-f1-score, mention-pair-model, span-ranking-coreference, hungarian-algorithm, assignment-problem, bell-numbers, agglomerative-clustering]
sources:
  - paper: "Amit Bagga and Breck Baldwin, Algorithms for scoring coreference chains, Proceedings of the LREC 1998 Workshop on Linguistic Coreference, pages 563 to 566"
    title: Bagga and Baldwin 1998
    locator: "the critique of the MUC score, the B-cubed definition with weights per mention, and the example with key clusters of 5, 2 and 5 mentions"
  - paper: "Marc Vilain, John Burger, John Aberdeen, Dennis Connolly and Lynette Hirschman, A model-theoretic coreference scoring scheme, Proceedings of the Sixth Message Understanding Conference (MUC-6), 1995"
    title: Vilain et al. 1995
    locator: the MUC link-based recall and precision
  - paper: "Xiaoqiang Luo, On coreference resolution performance metrics, Proceedings of HLT-EMNLP 2005, pages 25 to 32"
    title: Luo 2005
    locator: the CEAF metric and its comparison with MUC and B-cubed
  - paper: doi:10.3115/v1/P14-2006
    title: "Sameer Pradhan, Xiaoqiang Luo, Marta Recasens, Eduard Hovy, Vincent Ng and Michael Strube, Scoring coreference partitions of predicted mentions: a reference implementation, ACL 2014, pages 30 to 35"
    locator: the definitions of MUC, B-cubed and CEAF as implemented in the reference scorer, and their extension to predicted mentions
---

The B-cubed metric scores a [coreference resolution](/coreference-resolution/) system by asking, for each mention, how much the system's cluster of that mention agrees with the gold cluster of that mention. Bagga and Baldwin (1998) proposed it because the earlier MUC score counts only links and cannot tell a small merge error from a large one. B-cubed (B3 for short) is one of the three scores whose mean is the CoNLL coreference score, with MUC and CEAF-e. It is defined on partitions of the same set of mentions; with mentions found by the system the two sides cover different mentions, and the reference scorer of Pradhan et al. (2014) fixes how to extend it.

## Definition

Let $M$ be a set of $N$ mentions. The key $\mathcal{K}$ is the gold partition of $M$ into entities, and the response $\mathcal{R}$ is the system's partition of the same $M$. For a mention $m$, let $K(m)$ be the key cluster and $R(m)$ the response cluster that contain $m$. The precision and recall of the mention are

$$P(m) = \frac{|K(m) \cap R(m)|}{|R(m)|}, \qquad \mathrm{Rec}(m) = \frac{|K(m) \cap R(m)|}{|K(m)|}.$$

B-cubed precision and recall are the averages over mentions, $P = \frac{1}{N} \sum_m P(m)$ and $\mathrm{Rec} = \frac{1}{N} \sum_m \mathrm{Rec}(m)$, and $F_1 = 2 P \cdot \mathrm{Rec} / (P + \mathrm{Rec})$. Bagga and Baldwin allow a weight per mention in place of $1/N$; the equal weights are the usual choice and the one the code uses.

```pseudo id=main
B-CUBED(key K, response R over the same mentions)
L1  for each mention m do
L2      c ← |K(m) ∩ R(m)|
L3      P ← P + c / |R(m)|
L4      Rec ← Rec + c / |K(m)|
L5  P ← P / N, Rec ← Rec / N
L6  return P, Rec, and F1 = 2 P Rec / (P + Rec)
```

Grouping the mentions by the pair of clusters that holds them gives the same values as a sum over cells: $P = \frac{1}{N} \sum_{K \in \mathcal{K}} \sum_{S \in \mathcal{R}} |K \cap S|^2 / |S|$, and the same with $|K|$ for recall. So B-cubed costs $O(N)$ time with a hash map from mentions to clusters.

Properties (theorems, from the definition). Every $P(m)$ and $\mathrm{Rec}(m)$ is positive, because $m$ itself is in both clusters, so $P$ and $R$ are above 0. Swapping key and response swaps precision and recall. $F_1 = 1$ exactly when the response equals the key. A response of all singletons has precision 1, and a response of one cluster has recall 1. The test file checks these facts and the cell formula with exact fractions on random partitions.

For contrast, the MUC score of Vilain et al. (1995) counts links: its recall is $\sum_{K} (|K| - |p(K)|) / \sum_K (|K| - 1)$, where $p(K)$ is the set of parts that the response cuts $K$ into, and precision swaps the roles. CEAF (Luo 2005) aligns key and response entities one to one with the best total similarity, an [assignment problem](/assignment-problem/) solved by the [Hungarian algorithm](/hungarian-algorithm/); CEAF-e uses the similarity $2 |K \cap S| / (|K| + |S|)$. The CoNLL score is the mean of the MUC, B-cubed and CEAF-e F1 values.

## Examples and non-examples

The example of Bagga and Baldwin (1998) has 12 mentions and the key $\{1, \ldots, 5\}$, $\{6, 7\}$, $\{8, 9, A, B, C\}$. Two responses each make one merge:

| response | MUC P | MUC R | B3 P | B3 R |
|---|---|---|---|---|
| merge $\{6, 7\}$ into $\{8, \ldots, C\}$ | 9/10 | 1 | 16/21 ≈ 0.762 | 1 |
| merge $\{1, \ldots, 5\}$ with $\{8, \ldots, C\}$ | 9/10 | 1 | 7/12 ≈ 0.583 | 1 |

For the first response, the 5 mentions of $\{1, \ldots, 5\}$ have precision 1, mentions 6 and 7 have $2/7$, and the 5 others have $5/7$; the mean is $(5 + 4/7 + 25/7)/12 = 16/21$. In the second, 10 mentions have precision $5/10$ and 2 have 1, so the mean is $7/12$. MUC gives the same 9/10 to both, since each response has one wrong link; B-cubed says that joining two large entities is the worse error.

The extremes show what each score rewards. With the same key:

| response | MUC P, R, F1 | B3 P, R, F1 |
|---|---|---|
| all 12 singletons | 0, 0, 0 | 1, 1/4, 2/5 |
| one cluster of all 12 | 9/11, 1, 9/10 | 3/8, 1, 6/11 |

MUC gives a high score to the single cluster and nothing to the singletons. B-cubed is milder in both directions, and it gives a lot of precision credit to singletons, which is why scores on data with many singleton mentions look high.

Non-examples:

- Mention-level accuracy (the share of mentions given the right antecedent) is not B-cubed: it depends on which antecedent was chosen, while B-cubed sees only the clusters.
- Pairwise F1, over all pairs of mentions placed in the same cluster, is a different score; it weighs large clusters quadratically.
- B-cubed on key and response with different mention sets is not defined by the formula above: a mention found only by the system has no key cluster. Reference scorers add such mentions as singletons or remove them; report which.

## Related definitions

- [Span F1 score](/span-f1-score/): precision, recall and F1 for finding mentions or entities as spans, which is the step before clustering.
- MUC and CEAF: the other two scores of the CoNLL average. MUC ignores singletons, CEAF-e counts each entity once through the alignment.
- Partitions: the number of possible responses on $N$ mentions is the Bell number (see [Bell numbers](/bell-numbers/)), so a score cannot be maximized by trying them all except for tiny $N$.
- [Mention-pair model](/mention-pair-model/) and [span-ranking model](/span-ranking-coreference/): the systems usually scored with these metrics.

## References
