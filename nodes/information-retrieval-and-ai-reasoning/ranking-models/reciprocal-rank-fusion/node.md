---
tag: 552S8S
kind: algorithm
slug: reciprocal-rank-fusion
name: Reciprocal rank fusion
aliases:
- RRF
area: information-retrieval-and-ai-reasoning/ranking-models
level: core
summary: Scores each document by the sum over input rankings of 1/(k + rank), a simple fusion that needs no score calibration.
solves: [rank-aggregation]
model: word-ram
complexity:
  vars: {N: the total length of the input rankings, n: the number of distinct documents in them}
  time: {worst: O(N + n log n)}
  space: {extra: O(n)}
properties: {deterministic: true, comparison: false, recursive: false}
history:
  year: 2009
  people: [Gordon V. Cormack, Charles L. A. Clarke, Stefan Büttcher]
  note: Cormack, Clarke and Büttcher proposed RRF at SIGIR 2009 as a baseline and found that it beat Condorcet fusion and the best single system on several TREC tasks and on LETOR 3.
prereqs: [rank-aggregation]
see_also: [borda-count, combmnz, markov-chain-rank-aggregation, kemeny-rank-aggregation, dense-passage-retrieval, bm25, learning-to-rank]
sources:
  - paper: doi:10.1145/1571941.1572114
    title: Gordon V. Cormack, Charles L. A. Clarke and Stefan Büttcher, Reciprocal rank fusion outperforms Condorcet and individual rank learning methods, Proceedings of the 32nd Annual International ACM SIGIR Conference (SIGIR 2009), 758-759
    locator: Section 1 (the formula, "k = 60 was fixed during a pilot investigation", the pilot results of Table 1, the TREC results of Table 2 and the LETOR 3 results of Table 3) and Section 2 (discussion)
  - paper: doi:10.1145/383952.384007
    title: Javed A. Aslam and Mark H. Montague, Models for metasearch, Proceedings of the 24th Annual International ACM SIGIR Conference (SIGIR 2001), 276-284
    locator: Borda-fuse, the rank-based fusion with linear points that RRF replaces by reciprocal points
---

Reciprocal rank fusion (RRF) merges several ranked lists of documents into one by giving each document the sum, over the lists, of $1/(k + r)$, where $r$ is its rank in the list and $k$ is a constant, usually 60. Documents that are not in a list get nothing from it. RRF uses only the ranks, so it can merge the outputs of systems whose scores have different scales, such as [BM25](/bm25/) and a [dense retriever](/dense-passage-retrieval/), with no training and no score normalization. Gordon Cormack, Charles Clarke and Stefan Büttcher proposed it in 2009 as a simple baseline for [rank aggregation](/rank-aggregation/), and it is now a common default for hybrid search.

## In plain words

Several search systems each return a ranked list for the same query. We want one list. Each system gives each of its documents a small vote: the top document gets the largest vote, the second a slightly smaller one, and so on, and the votes get smaller slowly, not fast. A document's final score is the sum of its votes from all systems. A document that two systems both return gets two votes, so it usually beats a document that only one system returns, even near the top. A document that one system puts first still gets a strong vote, so one confident system can lift it. The method never looks at the systems' own scores, which often cannot be compared.

## The problem

The input is $m$ ranked lists $L_1, \ldots, L_m$ for one query. Each list holds distinct documents, best first, and may be partial, as the top $c$ results of a search system are. For a list $L$ that holds $d$, $L(d)$ is the rank of $d$, from 1. The output is one ranking of the union of the lists. Scores may exist, but the method does not use them. The constant $k > 0$ is a parameter.

## The algorithm

```pseudo id=main
RRF(L1, ..., Lm, k)
L1  s ← an empty map from documents to scores
L2  for each list L:
L3      for i ← 1 to |L|:
L4          s(L[i]) ← s(L[i]) + 1 / (k + i)          ▷ a missing entry counts as 0
L5  return the documents of s sorted by s, highest first, ties to the smaller id
```

So $s(d) = \sum_{l : d \in L_l} 1/(k + L_l(d))$. The constant $k$ controls how flat the votes are. With $k = 0$ the vote of rank 1 is twice the vote of rank 2. With $k = 60$ the votes of ranks 1 and 2 are $1/61$ and $1/62$, which differ by less than 2 percent, and the vote of rank 61 is still half the vote of rank 1. The paper says that $k = 60$ "was fixed during a pilot investigation and not altered during subsequent validation", and that $k$ "mitigates the impact of high rankings by outlier systems". The value 60 is a tuned constant, not the result of a theorem.

## Example

Take the two runs of the toy collection for the query "sorted array search": the BM25 list $A = 1, 2, 8, 7, 4$ and a second list $B = 1, 6, 8, 2, 4$. With $k = 60$, the table shows the scores after each pass of line L2, to 6 places.

| document | 1 | 2 | 8 | 4 | 6 | 7 |
|---|---|---|---|---|---|---|
| rank in $A$ | 1 | 2 | 3 | 5 | none | 4 |
| score after $A$ | 0.016393 | 0.016129 | 0.015873 | 0.015385 | 0 | 0.015625 |
| rank in $B$ | 1 | 4 | 3 | 5 | 2 | none |
| score after $B$ | 0.032787 | 0.031754 | 0.031746 | 0.030769 | 0.016129 | 0.015625 |

Line L5 returns $1, 2, 8, 4, 6, 7$. The exact scores of documents 2 and 8 are $1/62 + 1/64 = 63/1984$ and $2/63$, which differ by about $8 \cdot 10^{-6}$. Document 4 is fifth in both lists, and its two votes, $2/65$, beat the single vote of document 6, which $B$ ranks second. With $k = 60$ and two lists, any document that both lists hold in their top 61 beats any document that only one list holds, wherever that list ranks it. The [Borda count](/borda-count/) on the same lists gives $1, 2, 8, 6, 4, 7$, so the two methods differ exactly on documents 4 and 6.

If each list is first cut to its top 2, the scores are $2/61$ for document 1 and $1/62$ for documents 2 and 6, and the result is $1, 2, 6$: the tie goes to the smaller id.

A second example shows that RRF is not an order by average rank. With two lists, let $x$ be at ranks 1 and 41 and $y$ at ranks 20 and 20. The total rank of $y$ is 40, smaller than the 42 of $x$, but $s(x) = 1/61 + 1/101 \approx 0.026294$ beats $s(y) = 2/80 = 0.025$.

## Correctness

The file proofs/correctness.md proves that lines L1 to L4 compute $s$ exactly: the loop invariant is that after $j$ lists, each document seen so far holds the sum of its votes from those $j$ lists. It also proves that one list comes back unchanged, and that if every list that holds $y$ ranks $x$ above $y$, then $s(x) > s(y)$. For full rankings of $n$ documents and $k > m n^2$, the RRF order is the order by total rank, which is the Borda order; the proof writes $1/(k + r) = (1/k)(1 - r/(k + r))$ and bounds the second part. For the usual $k = 60$ no such statement holds, as the second example shows.

What RRF does not have is a proof of quality. Cormack, Clarke and Büttcher measured it. On their pilot, with 30 system configurations on TREC topics 351 to 400, the [mean average precision](/mean-average-precision/) went from 0.2072 at $k = 0$ to 0.2145 at $k = 60$ and 0.2147 at $k = 80$, so the choice of $k$ mattered little. On submitted runs for TREC 3, TREC 5, TREC 9 and the TREC 2004 Robust track, RRF beat Condorcet fusion on all four and CombMNZ on three. On LETOR 3, fusing the published [learning to rank](/learning-to-rank/) baselines beat each of them, while CombMNZ scored slightly higher than RRF there. These are measurements on those collections.

## Complexity

Line L4 runs once for each entry of each list, so lines L2 to L4 take $\Theta(N)$ expected time with a hash map, where $N = \sum_l |L_l|$. Line L5 sorts $n$ documents in $O(n \log n)$; if only the top $t$ are needed, a heap gives $O(n \log t)$. The extra space is $O(n)$ for the map. The lists can be read one at a time, as the paper notes, so they need not all be in memory at once. With exact fractions, as in the code, the arithmetic costs more, but the counts of operations are the same.

## Properties

- **Rank only.** Any change to a system's scores that keeps its order leaves the result the same. This is the main reason to use RRF.
- **Unanimity.** If every list that holds $y$ ranks $x$ above $y$, and some list holds $x$, RRF ranks $x$ above $y$.
- **Presence counts.** Each list that holds a document adds a positive amount, so being in more lists helps. With $k = 60$ this effect is strong, as the toy example shows.
- **Separable.** The score is a sum over lists, so lists can be added one at a time, and a weight per list is a simple change.
- **Not a Kemeny method.** RRF has no approximation guarantee for the [Kemeny](/kemeny-rank-aggregation/) objective. It is a positional rule, like Borda, with points $1/(k + i)$ in place of $n - i + 1$.

## Variants and improvements

- **Weighted RRF.** Multiply the vote of list $l$ by a weight $w_l$, for example to trust a lexical retriever more than a dense one. The weights are tuned on training queries.
- **Other $k$.** Small $k$ gives more weight to the very top of each list, and large $k$ moves RRF toward Borda on the total rank, by the theorem above. Systems tune $k$ per collection when they have judged queries.
- **Depth cut.** Fuse only the top $c$ of each list. This bounds the work and matches what search systems return, but it changes the scores, as the depth-2 example shows.
- **Score fusion.** When the scores are comparable, or can be normalized, [CombSUM and CombMNZ](/combmnz/) use them. In the paper, CombMNZ was close to RRF and sometimes better.
- **Pairwise and stationary methods.** Condorcet fusion and [Markov chain rank aggregation](/markov-chain-rank-aggregation/) use pairwise majorities in place of positions.

## When to use it

Use RRF as the default way to merge ranked lists from different retrievers, for example a lexical and a dense retriever in hybrid search or a [retrieval-augmented generation](/retrieval-augmented-generation/) pipeline, when you have no training data or no time to calibrate scores. It is a few lines of code, it is hard to get badly wrong, and it is a strong baseline in the published experiments. If you have judged queries, try weighted RRF or a learned fusion, and compare them to plain RRF on held-out queries.

## Pitfalls

- **Ranks from 0.** Writing $1/(k + i)$ with $i$ from 0 in line L3 shifts every vote and gives a different method from the paper's. Count ranks from 1, as in line L3, or say that you use $k + 1$.
- **Floating point ties.** The scores of documents 2 and 8 differ by $8 \cdot 10^{-6}$; with many lists and long lists, true ties and near ties are common. Sorting floats in line L5 can then order equal scores by rounding noise. Keep exact fractions, or sum the votes in a fixed order and break ties by a stated rule.
- **Duplicate entries.** If a list holds the same document twice, line L4 counts both votes. Remove duplicates from each list first.
- **Treating k = 60 as proved.** The constant came from one pilot on TREC data. On other data a different $k$, or weights per list, can be better. Tune it if you can, and report it.
- **Lists of very different length.** A list of 1,000 documents gives votes of about $1/1060$ to its tail, which can add up across many lists and lift documents that every system ranks low. Cut all lists to the same depth.

## Implementations

## History

Cormack, Clarke and Büttcher presented RRF in a two-page poster at SIGIR 2009. They came up with it as an unsupervised baseline while they studied learning to rank, and they reported that it almost always beat the best of the lists it combined. They chose the reciprocal form because highly ranked documents should count more, but the weight of lower ranks should not vanish as it would with an exponential decay. The method builds on earlier rank-based fusion such as Aslam and Montague's Borda-fuse of 2001 and Montague and Aslam's Condorcet fusion of 2002. Its later spread came from hybrid search, where lexical and neural retrievers return scores that cannot be compared, and several search engines now offer it with $k = 60$ as the default.

## References
