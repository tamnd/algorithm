---
tag: F4V2Z2
kind: problem
slug: kemeny-rank-aggregation
name: Kemeny rank aggregation
aliases:
- Kemeny-Young method
- Kemeny optimal aggregation
area: algorithmic-game-theory/social-choice-and-voting
level: advanced
summary: Find the ranking that minimizes the total Kendall tau distance to the input rankings; NP-hard already for four input lists.
model: word-ram
complexity:
  vars: {n: the number of items, k: the number of input rankings}
  time: {worst: O(2^n n^2 + n^2 k)}
prereqs: [rank-aggregation, kendall-tau-distance, feedback-arc-set-problem, np-hard]
see_also: [borda-count, markov-chain-rank-aggregation, reciprocal-rank-fusion, spearman-footrule, ptas, approximation-ratio, assignment-problem, randomized-quicksort]
sources:
  - paper: "John G. Kemeny, Mathematics without numbers, Daedalus 88(4) (1959)"
    locator: the distance between two rankings and the proposal to take as consensus the ranking with the least total distance to the given ones
  - paper: doi:10.1137/0135023
    title: H. P. Young and A. Levenglick, A consistent extension of Condorcet's election principle, SIAM Journal on Applied Mathematics 35(2) (1978), 285-300
    locator: the characterization of the Kemeny rule as the only rule that is neutral, consistent and Condorcet
  - paper: doi:10.1007/BF00303169
    title: John Bartholdi III, Craig A. Tovey and Michael A. Trick, Voting schemes for which it can be difficult to tell who won the election, Social Choice and Welfare 6(2) (1989), 157-165
    locator: the proof that deciding a Kemeny winner is NP-hard when the number of voters is part of the input
  - paper: doi:10.1145/371920.372165
    title: Cynthia Dwork, Ravi Kumar, Moni Naor and D. Sivakumar, Rank aggregation methods for the Web, Proceedings of the 10th International World Wide Web Conference (WWW10), 613-622
    locator: NP-hardness of Kemeny optimal aggregation for four lists and every even number of lists from four on, the footrule optimal aggregation as a 2-approximation, and local Kemenization
  - paper: doi:10.1016/j.tcs.2005.08.031
    title: Edith Hemaspaandra, Holger Spakowski and Jörg Vogel, The complexity of Kemeny elections, Theoretical Computer Science 349(3) (2005), 382-391
    locator: the completeness of the Kemeny winner problem for the class Theta_2^p
  - paper: doi:10.1145/1411509.1411513
    title: Nir Ailon, Moses Charikar and Alantha Newman, Aggregating inconsistent information, ranking and clustering, Journal of the ACM 55(5), Article 23 (2008)
    locator: KwikSort and Pick-A-Perm, the expected ratio 11/7 for the better of the two (Theorem 8), and the ratio 4/3 with the LP-based pivot
  - paper: "Claire Kenyon-Mathieu and Warren Schudy, How to rank with few errors, Proceedings of the 39th ACM Symposium on Theory of Computing (STOC), 95 to 103 (2007)"
    locator: the PTAS for weighted feedback arc set in tournaments and for Kemeny rank aggregation
  - paper: doi:10.1016/j.jcss.2019.04.005
    title: Georg Bachmeier et al., k-Majority digraphs and the hardness of voting with a constant number of voters, Journal of Computer and System Sciences 105 (2019), 130-157
    locator: NP-hardness of the Kemeny rule for every odd number of voters from seven on
  - paper: doi:10.1145/1798596.1798608
    title: Don Coppersmith, Lisa K. Fleischer and Atri Rudra, Ordering by weighted number of wins gives a good ranking for weighted tournaments, ACM Transactions on Algorithms 6(3), Article 55 (2010)
    locator: the 5-approximation by weighted number of wins, which for full rankings is the Borda order
  - paper: "Persi Diaconis and R. L. Graham, Spearman's footrule as a measure of disarray, Journal of the Royal Statistical Society, Series B 39(2) (1977), 262-268"
    locator: the inequality between the Kendall tau distance and the Spearman footrule, K at most F at most 2K
  - paper: "Dominik Peters, Kemeny rank aggregation is NP-hard for three voters, arXiv:2607.25540 (2026), preprint"
    locator: the reduction from maximum cut that shows NP-hardness for three input rankings
  - paper: "Péter Madarasi, The complexity of Kemeny aggregation with three rankings, arXiv:2607.28588 (2026), preprint"
    locator: the independent proof that the Kemeny score problem is NP-complete for three rankings
---

Kemeny rank aggregation asks for the ranking of $n$ items whose total [Kendall tau distance](/kendall-tau-distance/) to $k$ given rankings is as small as possible. The Kendall tau distance counts the pairs of items that two rankings put in opposite orders, so a Kemeny ranking is one that disagrees with the voters on the fewest pairs in total. John Kemeny proposed it in 1959, and it is the reference objective of [rank aggregation](/rank-aggregation/). It is [NP-hard](/np-hard/) already for four input rankings. It is a weighted form of the [feedback arc set problem](/feedback-arc-set-problem/) on a tournament, so it can be solved exactly in $O(2^n n^2)$ time by a subset dynamic program, and it has a [PTAS](/ptas/).

## In plain words

Several judges each put the same items in order, and the orders do not agree. We want one order for all of them. Take any two items. Each judge puts one of them above the other. Our order also puts one above the other, and every judge who did it the other way disagrees with us on that pair. Count these disagreements over all pairs and all judges. A Kemeny order is an order with the smallest count. If most judges agree on every pair and these majorities fit together into one order, that order is the answer. Often they do not fit: most judges can prefer the first item to the second, the second to the third and the third to the first. Then some majorities must be broken, and the hard part is to choose which ones. No fast method is known that always finds the best choice.

## Definition

**Input.** A set $U$ of $n$ items and $k$ rankings $\tau_1, \ldots, \tau_k$ of $U$, each a total order. A ranking may occur more than once.

**Distance.** For two rankings $\pi$ and $\tau$, $K(\pi, \tau)$ is the number of unordered pairs $\{a, b\}$ that one of them puts as $a$ above $b$ and the other as $b$ above $a$. It is a metric on the $n!$ rankings, with values from 0 to $\binom{n}{2}$.

**Output.** A ranking $\pi^*$ of $U$ with the least Kemeny cost

$$C(\pi) = \sum_{i=1}^{k} K(\pi, \tau_i).$$

A Kemeny ranking is a median of the input rankings in the metric $K$. There can be several.

**Decision form.** Given the rankings and an integer $c$, is there a $\pi$ with $C(\pi) \le c$? This is NP-complete; a ranking with its cost is a certificate that is checked in $O(n^2 k)$ time.

**Pairwise form.** Let $w_{ab}$ be the number of input rankings that put $a$ above $b$, so $w_{ab} + w_{ba} = k$. A ranking $\pi$ that puts $a$ above $b$ disagrees on this pair with the $w_{ba}$ rankings that put $b$ first, so

$$C(\pi) = \sum_{a \text{ above } b \text{ in } \pi} w_{ba}.$$

The cost depends on the input only through the $n \times n$ matrix $w$, which is built in $O(n^2 k)$ time. Every algorithm below starts from it.

## Variants

- **Partial lists.** Each input ranks only some of the items, as the top results of a search engine do. A pair counts only for the lists that rank, or imply the order of, both items. Dwork, Kumar, Naor and Sivakumar studied this case for metasearch.
- **Weighted voters.** Ranking $\tau_i$ has weight $v_i \ge 0$, and $w_{ab}$ becomes the total weight of the rankings that put $a$ above $b$.
- **Kemeny winner.** Decide whether a given item is first in some Kemeny ranking. This is the form used in voting theory.
- **Ties.** Inputs or outputs may be weak orders, with a tie on a pair costing half a disagreement or a fixed amount. The definitions differ between papers.
- **Footrule aggregation.** Replace $K$ by the [Spearman footrule](/spearman-footrule/) $F$, the sum of the absolute differences of positions. This version is polynomial, and its optimum is a 2-approximation of the Kemeny cost (see Known algorithms).

## Examples

**A Condorcet ranking.** Five voters: three rank $a, b, c$ and two rank $b, c, a$. Then $w_{ab} = 3$, $w_{ac} = 3$ and $w_{bc} = 5$, so a majority puts $a$ above $b$, $a$ above $c$ and $b$ above $c$. These majorities form the order $a, b, c$, and its cost is $0 \cdot 3 + 2 \cdot 2 = 4$: the two voters of $b, c, a$ disagree on $\{a, b\}$ and $\{a, c\}$. The other orders cost more, for example 5 for $b, a, c$ and 6 for $b, c, a$. The [Borda count](/borda-count/) with points 3, 2 and 1 gives $a$ 11, $b$ 12 and $c$ 7, so it returns $b, a, c$ and does not rank the majority winner $a$ first.

**A cycle.** Three voters rank $a, b, c$, then $b, c, a$, then $c, a, b$. Each pair has a majority of 2 to 1, but the majorities go round: $a$ above $b$, $b$ above $c$ and $c$ above $a$. Each of the three input rankings costs $0 + 2 + 2 = 4$, and each of the three reversed rankings costs 5. So there are three Kemeny rankings, each with cost 4, and each breaks exactly one majority.

**Two lists.** On the toy collection, the [BM25](/bm25/) run for "sorted array search" and the second run of the collection both hold documents 1, 2, 4 and 8. Restricted to these, the lists are $1, 2, 8, 4$ and $1, 8, 2, 4$, at distance 1. Each list is a Kemeny ranking with cost 1. With two inputs this always holds: $K(\pi, \tau_1) + K(\pi, \tau_2) \ge K(\tau_1, \tau_2)$ by the [triangle inequality](/triangle-inequality/), with equality at $\pi = \tau_1$.

## Known algorithms

| algorithm | guarantee | time |
|---|---|---|
| try every ranking | exact | $O(n! \, n^2 + n^2 k)$ |
| subset dynamic programming | exact | $O(2^n n^2 + n^2 k)$ |
| best input ranking (Pick-A-Perm) | ratio 2 | $O(n^2 k)$ with $w$, or $O(k^2 n \log n)$ directly |
| footrule optimal aggregation | ratio 2 | $O(n^3 + n^2 k)$ |
| order by Borda score | ratio 5 | $O(nk + n \log n)$ |
| KwikSort on the majority relation | expected ratio 2 | expected $O(n \log n)$ comparisons with $w$ |
| better of KwikSort and Pick-A-Perm | expected ratio 11/7 | as the two parts |
| LP-based pivot and Pick-A-Perm | ratio 4/3 | polynomial, one linear program |
| Kenyon-Mathieu and Schudy (2007) | ratio $1 + \varepsilon$ | polynomial for fixed $\varepsilon$ |

**Subset dynamic programming.** Let $f(S)$ be the least cost of an order of the set $S$, counting only pairs inside $S$. The last item $v$ of the best order of $S$ is below every other item $u \in S \setminus \{v\}$, so it pays $w_{vu}$, the number of voters that put $v$ above $u$, for each of them. So $f(\emptyset) = 0$ and

$$f(S) = \min_{v \in S} \Bigl( f(S \setminus \{v\}) + \sum_{u \in S \setminus \{v\}} w_{vu} \Bigr).$$

The answer is $f(U)$. With the sums kept per set, this takes $O(2^n n^2)$ time and $O(2^n)$ space, the same scheme as [bitmask DP](/bitmask-dp/) for the feedback arc set problem.

**Best input ranking.** Let $\pi^*$ be optimal. For each input $\tau_j$, the triangle inequality gives $C(\tau_j) = \sum_i K(\tau_j, \tau_i) \le k \, K(\tau_j, \pi^*) + C(\pi^*)$. The average of $K(\tau_j, \pi^*)$ over $j$ is $C(\pi^*)/k$, so the average of $C(\tau_j)$ is at most $2 C(\pi^*)$, and the best input does at least as well as the average. Ailon, Charikar and Newman call the random choice Pick-A-Perm.

**Footrule optimal aggregation.** Minimizing $\sum_i F(\sigma, \tau_i)$ is an [assignment problem](/assignment-problem/): put item $a$ at position $p$ at cost $\sum_i |\tau_i(a) - p|$, and find a minimum cost perfect matching of items to positions. Diaconis and Graham proved $K \le F \le 2K$. So for the footrule optimum $\sigma$, $C(\sigma) \le \sum_i F(\sigma, \tau_i) \le \sum_i F(\pi^*, \tau_i) \le 2 C(\pi^*)$. Dwork, Kumar, Naor and Sivakumar used this for metasearch.

**KwikSort.** Pick a random pivot item, put each other item above or below it by the majority of $w$, and recurse on the two sides, as in [randomized quicksort](/randomized-quicksort/). Ailon, Charikar and Newman proved that on rank aggregation inputs it has an expected ratio of 2, and that the better of KwikSort and Pick-A-Perm has an expected ratio of 11/7. Rounding a linear program over the pairs in place of the majority gives 4/3.

**Local improvement.** Local Kemenization, described on the page on [Markov chain rank aggregation](/markov-chain-rank-aggregation/), swaps adjacent items while a majority prefers the swap. It never raises the cost and its result satisfies the extended Condorcet criterion, but it has no approximation guarantee of its own; it is used to clean up the output of a fast method.

**Exact solvers in practice.** Integer programs with one 0/1 variable per ordered pair and the transitivity constraints on each triple are the usual exact method. How large an instance they solve in a given time is a measured property of the inputs, not a proved bound.

## Bounds

**Lower bound on the cost.** Each pair costs at least $\min(w_{ab}, w_{ba})$, so $C(\pi) \ge \sum_{\{a, b\}} \min(w_{ab}, w_{ba})$ for every $\pi$. Equality holds exactly when $\pi$ agrees with the strict majority on every pair that has one. So if the strict majorities are defined on every pair and form a total order, the Condorcet ranking, that order is the unique Kemeny ranking.

**Hardness with many voters.** Bartholdi, Tovey and Trick (1989) proved that it is NP-hard to decide whether an item is a Kemeny winner when the number of voters is part of the input. Hemaspaandra, Spakowski and Vogel (2005) proved that the winner problem is complete for $\Theta_2^p$, the class of problems solved by polynomial time with $O(\log n)$ queries to an NP oracle.

**Hardness with few voters.** Dwork, Kumar, Naor and Sivakumar (2001) proved NP-hardness for $k = 4$ and for every even $k \ge 4$. Bachmeier and coauthors (2019) proved it for every odd $k \ge 7$. The case $k = 3$ stayed open until 2026, when a preprint by Dominik Peters and an independent preprint by Péter Madarasi gave NP-hardness for three rankings, and with the reduction that adds a ranking and its reverse, also for five. At the time of writing these are preprints, not reviewed papers. For $k = 1$ and $k = 2$ an input ranking is optimal, as the example shows.

**Approximation.** The PTAS of Kenyon-Mathieu and Schudy shows that the problem is not APX-hard unless P = NP. NP-hardness rules out an exact polynomial algorithm unless P = NP.

## Reductions

**To weighted feedback arc set.** Write each pair's cost as $\min(w_{ab}, w_{ba})$ plus $|w_{ab} - w_{ba}|$ if $\pi$ goes against the strict majority. Then

$$C(\pi) = \sum_{\{a, b\}} \min(w_{ab}, w_{ba}) + \sum_{\pi \text{ against the majority on } \{a, b\}} |w_{ab} - w_{ba}|.$$

The first sum does not depend on $\pi$. Draw the majority digraph, with an arc $a \to b$ of weight $w_{ab} - w_{ba}$ whenever $w_{ab} > w_{ba}$. The second sum is the weight of the arcs that $\pi$ points backwards. So a Kemeny ranking is exactly an order with a minimum weight set of backward arcs, a weighted feedback arc set of the majority digraph. With an odd number of voters every pair has a majority, and the digraph is a tournament.

**Adding a ranking and its reverse.** For every $\pi$, $K(\pi, \tau) + K(\pi, \bar\tau) = \binom{n}{2}$, where $\bar\tau$ is the reverse of $\tau$, because each pair agrees with exactly one of the two. Adding both to the input adds the same amount to every cost and keeps the set of Kemeny rankings. So hardness for $k$ rankings gives hardness for $k + 2$, which is how the results for four and three rankings spread to all even and all odd $k$.

**From tournaments.** The hardness proofs go the other way: they build input rankings whose majority digraph is a hard instance of feedback arc set on tournaments, or, in the preprint by Peters, encode an instance of [maximum cut](/maximum-cut/).

**Maximum likelihood.** In the Mallows model, a ranking $\tau$ is drawn with probability proportional to $\phi^{K(\tau, \pi_0)}$ for a central ranking $\pi_0$ and some $0 < \phi < 1$. The likelihood of $k$ independent draws is proportional to $\phi^{C(\pi_0)}$, so the [maximum likelihood estimate](/maximum-likelihood-estimation/) of $\pi_0$ is a Kemeny ranking.

## Applications

- **Metasearch.** Merge the result lists of several search engines. Dwork, Kumar, Naor and Sivakumar argued that the extended Condorcet criterion, which every Kemeny ranking satisfies, resists spam: if a majority of engines ranks each good page above each spam page, then all good pages come before all spam pages. Fast methods such as [reciprocal rank fusion](/reciprocal-rank-fusion/) and [CombMNZ](/combmnz/) are used in practice, and Kemeny serves as the objective to compare them with.
- **Elections.** The Kemeny rule elects the top of a Kemeny ranking. Young and Levenglick proved that it is the only rule that is neutral, consistent and Condorcet, so it is the natural extension of the majority principle to full rankings.
- **Consensus of rankers.** Combine the orders of several judges, sensors or learned models, for example in sports ranking or in the evaluation of systems on several metrics.

## References
