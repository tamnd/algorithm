---
tag: 9H0GWC
kind: problem
slug: rank-aggregation
name: Rank aggregation
aliases:
- ranking fusion
- metasearch aggregation
area: information-retrieval-and-ai-reasoning/ranking-models
level: core
summary: Combine several rankings of the same items into one consensus ranking that agrees with them as much as possible.
model: word-ram
complexity:
  vars: {n: the number of distinct items, k: the number of input rankings}
  time: {worst: O(n^3 + n^2 k)}
prereqs: [kendall-tau-distance, spearman-footrule]
see_also: [kemeny-rank-aggregation, borda-count, reciprocal-rank-fusion, combmnz, markov-chain-rank-aggregation, federated-search, learning-to-rank, ranking-comparison-kendall-tau]
sources:
  - paper: doi:10.1145/371920.372165
    title: Cynthia Dwork, Ravi Kumar, Moni Naor and D. Sivakumar, Rank aggregation methods for the Web, Proceedings of the 10th International World Wide Web Conference (WWW10), 613-622
    locator: the problem of rank aggregation for metasearch with partial lists, Kemeny optimal and footrule optimal aggregation, the Markov chain methods and local Kemenization
  - paper: doi:10.1145/383952.384007
    title: Javed A. Aslam and Mark H. Montague, Models for metasearch, Proceedings of the 24th Annual International ACM SIGIR Conference (SIGIR 2001), 276-284
    locator: metasearch with rank-based fusion, Borda-fuse, compared with score-based fusion on TREC runs
  - paper: "Edward A. Fox and Joseph A. Shaw, Combination of multiple searches, The Second Text REtrieval Conference (TREC-2), NIST Special Publication 500-215 (1994), 243-252"
    locator: the score-based combination rules CombSUM and CombMNZ
  - paper: doi:10.1145/1571941.1572114
    title: Gordon V. Cormack, Charles L. A. Clarke and Stefan Büttcher, Reciprocal rank fusion outperforms Condorcet and individual rank learning methods, Proceedings of the 32nd Annual International ACM SIGIR Conference (SIGIR 2009), 758-759
    locator: reciprocal rank fusion and its comparison with Condorcet fusion and CombMNZ on TREC and LETOR 3
  - paper: "Persi Diaconis and R. L. Graham, Spearman's footrule as a measure of disarray, Journal of the Royal Statistical Society, Series B 39(2) (1977), 262-268"
    locator: the inequality between the Kendall tau distance and the Spearman footrule, K at most F at most 2K
---

Rank aggregation takes several rankings of the same items and builds one ranking that agrees with them as much as possible. In information retrieval the rankings are the result lists of several search systems, or of one system with several query versions, and the problem is also called data fusion or metasearch. The usual measure of agreement is the [Kendall tau distance](/kendall-tau-distance/), and the ranking that minimizes the total distance is the [Kemeny ranking](/kemeny-rank-aggregation/), which is NP-hard to find. With the [Spearman footrule](/spearman-footrule/) in place of Kendall tau the optimum is found in polynomial time, and fast rules such as the [Borda count](/borda-count/), [reciprocal rank fusion](/reciprocal-rank-fusion/) and [CombMNZ](/combmnz/) are what systems use in practice.

## In plain words

Several search engines, or several judges, each give us an ordered list of the same things, and the lists do not fully agree. We want one list that is a fair summary of all of them. One way to say what fair means: for each pair of things, look at which one each input list puts higher, and try to agree with as many lists as possible over all pairs. Finding the list that does this best is hard when there are many things. So in practice we use simple rules. We can give points by position and add them up. We can add the systems' own scores after we put them on a common scale. Or we can let a random walk move from worse to better items and see where it spends its time.

## Definition

**Input.** A universe $U$ of $n$ items and $k$ input rankings $\tau_1, \ldots, \tau_k$. Each $\tau_i$ is a total order of a subset $U_i \subseteq U$, best first; it is full if $U_i = U$ and partial otherwise, as a top 1000 list is. Some inputs also carry a real score for each ranked item.

**Output.** One total order $\pi$ of $U$, or of its top part.

**Question.** Which $\pi$ agrees best with the inputs? The standard answer fixes a distance $d$ between rankings and asks for

$$\pi^* \in \arg\min_{\pi} \sum_{i=1}^{k} d(\pi, \tau_i).$$

With $d$ the Kendall tau distance $K$, the number of pairs in opposite order, this is Kemeny optimal aggregation. With $d$ the footrule $F$, the sum over items of the absolute difference of their positions, it is footrule optimal aggregation. For partial lists, Dwork, Kumar, Naor and Sivakumar count only the pairs, or items, that a list ranks.

**Known complexity.** Kemeny optimal aggregation is NP-hard for every even $k \ge 4$ and every odd $k \ge 7$, and by two 2026 preprints also for $k = 3$ and so for $k = 5$; it can be solved in $O(2^n n^2 + n^2 k)$ time. Footrule optimal aggregation of full rankings is an [assignment problem](/assignment-problem/) and takes $O(n^3 + n^2 k)$ time. The positional and score rules take $O(N + n \log n)$, where $N$ is the total length of the inputs. Any exact method must read all of the input, so $\Omega(N)$ is a lower bound.

## Variants

- **Rank-only or score fusion.** Rank-only methods use the positions, so they work for systems whose scores have different scales. Score methods such as CombSUM and CombMNZ use normalized scores and keep the gaps between items.
- **Full or partial lists.** In metasearch, each engine returns only its top results, and an item missing from a list can mean "ranked low" or "never seen". Methods differ in how they treat it.
- **Weighted inputs.** Each list gets a weight, set by hand or learned on training queries. With training data the problem becomes supervised fusion, a form of [learning to rank](/learning-to-rank/).
- **Top part only.** Only the first few positions of $\pi$ matter, as on a search results page.
- **Winner only.** In voting, only the top item is wanted, as in the Kemeny winner problem.
- **Federated search.** The lists come from different collections, so they rarely overlap. Merging them is part of [federated search](/federated-search/), where overlap-based rules such as CombMNZ help little.

## Examples

**Two runs on the toy collection.** For the query "sorted array search", the [BM25](/bm25/) list is $A = 1, 2, 8, 7, 4$ and the second run of the collection gives $B = 1, 6, 8, 2, 4$, with scores 2.0, 2.0, 1.5, 1.0 and 1.0. The lists share documents 1, 2, 4 and 8, and they disagree only on the pair $\{2, 8\}$. The table shows the outputs of five methods and their Kendall cost, the number of pairs ranked by a list that the output puts in the other order, summed over the two lists.

| method | output | Kendall cost |
|---|---|---|
| Borda count, missing items share the last points | $1, 2, 8, 6, 4, 7$ | 4 |
| reciprocal rank fusion, $k = 60$ | $1, 2, 8, 4, 6, 7$ | 5 |
| CombSUM, min-max scores | $1, 6, 8, 2, 7, 4$ | 1 |
| CombMNZ, min-max scores | $1, 8, 2, 6, 7, 4$ | 3 |
| MC4 Markov chain, $\varepsilon = 0.15$ | $1, 6, 2, 8, 7, 4$ | 1 |

The pair $\{2, 8\}$ costs 1 for every output, so 1 is the least possible cost. An exhaustive search over the 720 orders finds exactly two with cost 1: $1, 6, 2, 8, 7, 4$ and $1, 6, 8, 2, 7, 4$. They must put document 6 just below 1, because $B$ ranks it above 8, 2 and 4 and $A$ does not rank it, and document 7 just above 4. Borda and RRF give low points to an item that a list does not hold, so they push 6 and 7 down and break pairs that a list ranks. This is a choice about what a missing item means, not an error.

**A majority winner that Borda misses.** Five voters: three rank $a, b, c$ and two rank $b, c, a$. A majority puts $a$ above each other item. The Kemeny ranking is $a, b, c$ with cost 4. Borda, with points 3, 2 and 1, gives $b$ 12, $a$ 11 and $c$ 7, so it returns $b, a, c$, which costs 5.

## Known algorithms

| algorithm | uses | guarantee for the Kendall objective | time |
|---|---|---|---|
| [Borda count](/borda-count/) | ranks | ratio 5 on full lists | $O(N + n \log n)$ |
| [Reciprocal rank fusion](/reciprocal-rank-fusion/) | ranks | none | $O(N + n \log n)$ |
| [CombSUM and CombMNZ](/combmnz/) | scores | none | $O(N + n \log n)$ |
| [Markov chain aggregation](/markov-chain-rank-aggregation/) | pairwise majorities | none | $O(n^2 k + n^2 t)$ for $t$ rounds |
| footrule optimal aggregation | positions | ratio 2 on full lists | $O(n^3 + n^2 k)$ |
| best input list | ranks | ratio 2 on full lists | $O(k^2 n \log n)$ |
| [Kemeny](/kemeny-rank-aggregation/) by subset DP | pairwise counts | exact | $O(2^n n^2 + n^2 k)$ |
| PTAS of Kenyon-Mathieu and Schudy | pairwise counts | ratio $1 + \varepsilon$ | polynomial for fixed $\varepsilon$ |

The guarantees of the last four rows are proved on the Kemeny page. The first four rows have measured, not proved, quality as retrieval methods: Fox and Shaw, Lee, Aslam and Montague, and Cormack, Clarke and Büttcher each found that fusion often beats the best single input on TREC runs.

**Local Kemenization.** Any output can be improved by swapping adjacent items while the majority of the lists that rank both prefers the swap. Dwork, Kumar, Naor and Sivakumar showed that the result is locally Kemeny optimal and satisfies the extended Condorcet criterion: if a majority ranks every item of a set $S$ above every item outside $S$, then all of $S$ comes first.

## Bounds

**Hardness.** Kemeny optimal aggregation is NP-hard, already for four lists; see the [Kemeny page](/kemeny-rank-aggregation/) for the precise results.

**Footrule versus Kendall.** Diaconis and Graham proved $K(\pi, \tau) \le F(\pi, \tau) \le 2 K(\pi, \tau)$ for full rankings. So the footrule optimum, which is polynomial, is within a factor 2 of the Kemeny optimum.

**No perfect rule.** For three or more items, Arrow's theorem shows that no rule that maps every profile of full rankings to a ranking can be at once unanimous, independent of irrelevant alternatives and not a dictatorship. Every method in the table gives up one of these properties; the Kemeny rule, for example, is not independent of irrelevant alternatives.

**Reading the input.** Every method that depends on all lists must read them, which costs $\Omega(N)$ time.

## Reductions

- **Kemeny to feedback arc set.** The Kemeny problem is a weighted [feedback arc set](/feedback-arc-set-problem/) problem on the majority digraph, with the margins as weights.
- **Footrule to assignment.** Put item $a$ at position $p$ at cost $\sum_i |\tau_i(a) - p|$; a minimum cost perfect matching of items to positions is a footrule optimal ranking.
- **Borda to mean position.** On full lists, the Borda order is the order by mean position, and it minimizes the total squared difference of positions, as the [Borda page](/borda-count/) proves.
- **Markov chains to PageRank.** The Markov chain methods compute a stationary distribution of a walk on items with a teleport step, as [PageRank](/pagerank/) does on web pages.

## Applications

- **Metasearch.** Merge the result lists of several search engines into one page, the setting of Dwork, Kumar, Naor and Sivakumar and of Aslam and Montague.
- **Hybrid retrieval.** Merge a lexical list such as BM25 with a dense retriever, often with reciprocal rank fusion, for example in [retrieval-augmented generation](/retrieval-augmented-generation/).
- **Query variants.** Run several versions of a query and fuse the lists.
- **Voting and judging.** Combine the rankings of voters or judges, where the Kemeny and Borda rules come from.
- **Evaluation.** Combine the rankings of systems under several metrics or test collections into one leaderboard, and compare rankings with [rank correlation](/ranking-comparison-kendall-tau/).

## References
