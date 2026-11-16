---
tag: DF298Z
kind: algorithm
slug: markov-chain-rank-aggregation
name: Markov chain rank aggregation
aliases:
- MC4 aggregation
- Dwork-Kumar-Naor-Sivakumar aggregation
area: information-retrieval-and-ai-reasoning/ranking-models
level: advanced
summary: Builds a Markov chain that moves from an item to one that a majority of rankings prefer, and ranks items by its stationary distribution.
solves: [rank-aggregation]
model: word-ram
complexity:
  vars: {n: the number of distinct items in the input lists, k: the number of lists, t: the number of rounds of power iteration}
  time: {worst: O(n^2 k + n^2 t)}
  space: {extra: O(n^2 + n k)}
properties: {deterministic: true, comparison: false, recursive: false}
history:
  year: 2001
  people: [Cynthia Dwork, Ravi Kumar, Moni Naor, D. Sivakumar]
  note: Dwork, Kumar, Naor and Sivakumar proposed the four chains MC1 to MC4 and local Kemenization at WWW10 in 2001, as tools for metasearch that resist spam.
prereqs: [rank-aggregation, markov-chain, stationary-distribution, power-iteration]
see_also: [kemeny-rank-aggregation, borda-count, reciprocal-rank-fusion, combmnz, pagerank, kendall-tau-distance, spearman-footrule]
sources:
  - paper: doi:10.1145/371920.372165
    title: Cynthia Dwork, Ravi Kumar, Moni Naor and D. Sivakumar, Rank aggregation methods for the Web, Proceedings of the 10th International World Wide Web Conference (WWW10), 613-622
    locator: the Markov chain methods MC1 to MC4, the definition of local Kemenization and the extended Condorcet criterion, and the NP-hardness of Kemeny aggregation for four lists
  - paper: "Cynthia Dwork, Ravi Kumar, Moni Naor and D. Sivakumar, Rank aggregation revisited, manuscript (2001)"
    locator: the longer version of the WWW10 paper, with the proofs on local Kemenization and on the footrule as an approximation of the Kendall distance
---

Markov chain rank aggregation combines several ranked lists into one by a random walk on the items. Each list is a vote. The walk moves from an item to an item that the lists rank higher, and the final ranking orders the items by how much time the walk spends at each one in the long run, which is the [stationary distribution](/stationary-distribution/) of the [Markov chain](/markov-chain/). Cynthia Dwork, Ravi Kumar, Moni Naor and D. Sivakumar defined four such chains, MC1 to MC4, in 2001 for metasearch, the [rank aggregation](/rank-aggregation/) of the result lists of several search engines. The same paper defines local Kemenization, a cheap clean-up pass that makes any aggregate agree with every strict majority on neighbouring items.

## In plain words

Several search engines each give a ranked list of results. We want one list. Put a walker on one of the results. At each step the walker looks at another result and asks the lists which of the two is better. If most of the lists that show both results prefer the other one, the walker moves there, else it stays. Good results pull the walker in and keep it, so after many steps the walker is mostly at good results. We rank the results by how often the walker is at each one. To keep the walker from being stuck in a corner of the graph, it sometimes jumps to a random result, as in PageRank. A last pass then walks down the list and swaps any two neighbours when most lists prefer the lower one.

## The problem

The input is $k$ ranked lists $\tau_1, \ldots, \tau_k$. Each list holds distinct items, best first, and it may be partial: a search engine returns only its top results, so two lists can hold different items. Let $U$ be the union of the items and $n = |U|$. The output is one full ranking of $U$. For a list $\tau$ that holds $x$, $\tau(x)$ is the rank of $x$ in it. Item $Q$ *beats* item $P$, written $Q \succ P$, when strictly more of the lists that hold both items put $Q$ above $P$ than put $P$ above $Q$. A list that misses one of the two items does not vote on that pair.

The ideal answer is a Kemeny ranking, which minimizes the total [Kendall tau distance](/kendall-tau-distance/) to the lists. Finding it is [NP-hard](/np-hard/), as the [Kemeny rank aggregation](/kemeny-rank-aggregation/) page explains, so this method gives a fast heuristic answer, with no bound on its distance from the Kemeny optimum.

## The algorithm

Line L2 fills one row of the transition matrix $M$ for each item $P$. The four chains differ only in the rule that picks the next state.

| chain | next state when the walk is at $P$ |
|---|---|
| MC1 | an item chosen uniformly from the multiset of all items that some list holding $P$ ranks at or above $P$ |
| MC2 | a list chosen uniformly among the lists that hold $P$, then an item chosen uniformly among the items it ranks at or above $P$ |
| MC3 | a list chosen uniformly among the lists that hold $P$, then an item $Q$ chosen uniformly from that list; go to $Q$ if the list ranks $Q$ above $P$, else stay at $P$ |
| MC4 | an item $Q$ chosen uniformly from $U$; go to $Q$ if $Q \succ P$, else stay at $P$ |

MC4 is the majority chain: it moves only along pairwise majorities. MC3 is the same walk with one list as the judge in place of the majority.

```pseudo id=main
MC-AGGREGATE(τ1, ..., τk, chain, ε)
L1  U ← the union of the items of τ1, ..., τk, in sorted order; n ← |U|
L2  for each P in U: fill row P of M by the move rule of chain
L3  M ← (1 - ε) M + (ε / n) J              ▷ J is the n × n matrix of ones
L4  π ← (1/n, ..., 1/n)
L5  repeat π ← π M until the L1 change of π is below tol
L6  return U sorted by π, highest first, ties to the smaller item

LOCAL-KEMENIZE(σ, τ1, ..., τk)
L7  for each x of σ, in order: append x to the end of ρ
L8      while x has an upper neighbour y in ρ and x ≻ y
L9          swap x and y in ρ
    return ρ
```

Line L3 is the teleport of [PageRank](/pagerank/): with probability $\varepsilon$ the walk jumps to a uniform random item. Line L5 is [power iteration](/power-iteration/). Lines L7 to L9 are [insertion sort](/insertion-sort/) with the majority relation as the comparison, but $\succ$ need not be transitive, so the result is not a sorted order in general. The usual use is to run lines L7 to L9 on the output of line L6, or on the output of any other aggregation method.

## Example

Take three items and five voters: three lists say $a, b, c$ and two lists say $b, c, a$. The majorities are $a \succ b$ (3 to 2), $a \succ c$ (3 to 2) and $b \succ c$ (5 to 0), so $a$ is the Condorcet winner, the item that beats every other item. The [Borda count](/borda-count/) gives $b$ 12 points and $a$ 11, so it puts $b$ first.

For MC4, the walk at $a$ never moves, because nothing beats $a$. At $b$ it moves to $a$ with probability $1/3$. At $c$ it moves to $a$ or $b$ with probability $1/3$ each. With $\varepsilon = 0.15$, line L3 gives the rows $a: (9/10, 1/20, 1/20)$, $b: (1/3, 37/60, 1/20)$ and $c: (1/3, 1/3, 1/3)$. The table shows the state of line L5 after each round, to 4 places.

| round | $\pi(a)$ | $\pi(b)$ | $\pi(c)$ |
|---|---|---|---|
| 0 | 0.3333 | 0.3333 | 0.3333 |
| 1 | 0.5222 | 0.3333 | 0.1444 |
| 2 | 0.6293 | 0.2798 | 0.0909 |
| 3 | 0.6899 | 0.2343 | 0.0758 |
| 4 | 0.7243 | 0.2042 | 0.0715 |
| 5 | 0.7438 | 0.1860 | 0.0702 |
| 6 | 0.7548 | 0.1753 | 0.0699 |
| 7 | 0.7611 | 0.1691 | 0.0698 |
| 8 | 0.7646 | 0.1656 | 0.0698 |
| limit | $10/13 \approx 0.7692$ | $90/559 \approx 0.1610$ | $3/43 \approx 0.0698$ |

The order is $a, b, c$ from round 1 on, and it is the Kemeny ranking of this profile (total distance 4, against 5 for the Borda order $b, a, c$). With $\varepsilon = 0$ all the mass ends at $a$, and $b$ and $c$ both get 0. MC3 on the same lists, with $\varepsilon = 0.15$, has the stationary distribution $(33/82, 6517/14842, 1176/7421) \approx (0.4024, 0.4391, 0.1585)$ and gives $b, a, c$, like Borda. Local Kemenization of $b, a, c$ inserts $b$, then inserts $a$ and swaps it up because $a \succ b$, then inserts $c$, which stays because $b \succ c$. The result is $a, b, c$.

On the two runs of the toy collection for the query "sorted array search", the [BM25](/bm25/) list $1, 2, 8, 7, 4$ and the second list $1, 6, 8, 2, 4$, MC4 with $\varepsilon = 0.15$ gives the exact stationary values $\pi(1) = 4/7$, $\pi(6) = 39072/215579 \approx 0.1812$, $\pi(2) = \pi(8) = 2580/30797 \approx 0.0838$, $\pi(7) = 120/2369 \approx 0.0507$ and $\pi(4) = 3/103 \approx 0.0291$. The order is $1, 6, 2, 8, 7, 4$. Document 6 comes second although only one list holds it: that list puts it above 8, 2 and 4, and the other list does not vote on those pairs, so 6 beats each of them 1 to 0. Documents 2 and 8 tie because the two lists disagree on them.

## Correctness

The file proofs/correctness.md proves four facts. Every row of $M$ is a probability distribution, for each of the four chains. For $\varepsilon > 0$, line L3 makes the map $\pi \mapsto \pi M$ shrink the $L_1$ distance between two distributions by the factor $1 - \varepsilon$, so the stationary distribution is unique and the vectors of line L5 are within $2 (1 - \varepsilon)^t$ of it after $t$ rounds. With $\varepsilon = 0$ and a Condorcet winner, MC4 makes the winner absorbing and puts all the mass on it. On full lists, one round of MC3 from the uniform vector already gives the Borda order.

For lines L7 to L9 the invariant is that, after each insertion, no item of $\rho$ is directly below an item that it beats. Each swap of line L9 exchanges two neighbours of a full ranking with the lower one beating the upper one, so it lowers the total Kendall distance by at least 1. The output is therefore locally Kemeny optimal, it is never worse than its input, and it satisfies the extended Condorcet criterion: if every item of a set $C$ beats every item outside $C$, the items of $C$ come first.

The method itself has no approximation guarantee for the Kemeny objective. Its order is the order of a stationary distribution, which is a different objective, and the toy example shows how far apart the two can be on partial lists.

## Complexity

Line L2 takes $O(n^2 k)$ time for each of the four chains with a position map for each list: MC4 asks each list about each pair of items, and MC1 to MC3 scan, for each item, the lists that hold it. Each round of line L5 is a vector times a dense $n \times n$ matrix, $O(n^2)$ time. By the contraction bound, $t \le \lceil \ln(2/\mathrm{tol}) / \varepsilon \rceil + 1$ rounds reach the tolerance, so with $\varepsilon = 0.15$ and $\mathrm{tol} = 10^{-12}$ at most 190 rounds are needed. Line L6 sorts in $O(n \log n)$. The total is $O(n^2 k + n^2 t)$ time and $O(n^2 + n k)$ extra space for the matrix and the position maps. Lines L7 to L9 make $O(n^2)$ comparisons in the worst case, each a count over the $k$ lists, so $O(n^2 k)$ time as written; the paper notes a faster way that uses $O(n \log n)$ comparisons.

## Properties

- **Majority driven.** MC4 depends on the lists only through the majority relation $\succ$. Two profiles with the same majorities give the same chain, however large the margins are.
- **Condorcet consistent at $\varepsilon = 0$.** A Condorcet winner takes all the mass. With $\varepsilon > 0$ it gets the largest share in the examples above, but the theorem covers only $\varepsilon = 0$.
- **Handles partial lists.** No chain needs a full ranking. A list votes only on items that it holds.
- **Deterministic.** The chain and the tie rule of line L6 depend only on the input. The walk is a way to define the scores; nothing in the computation is random.
- **Not a metric optimum.** The output need not minimize the Kendall or the footrule distance, and Dwork and coauthors note that the chains need not satisfy the extended Condorcet criterion, which is why the paper adds local Kemenization.

## Variants and improvements

- **MC1 to MC3.** These chains move to an item that one list ranks higher, with no majority vote. MC1 favours items that many lists hold near the top, and MC3 behaves like a smoothed Borda count, as the one-step result shows.
- **Missing items below.** A common change is to treat an item that a list misses as ranked below every item it holds. Then that list votes on the pair. On the toy runs this gives $1, 2, 8, 6, 4, 7$, the Borda order, and document 6 no longer climbs on a one-list majority.
- **Footrule aggregation.** The ranking that minimizes the total [Spearman footrule](/spearman-footrule/) distance to full lists is a [minimum weight perfect matching](/minimum-weight-perfect-matching/) of items to positions, so it can be found in polynomial time, and it is within a factor 2 of the Kemeny optimum by the Diaconis-Graham inequality. The paper uses it as another starting point for local Kemenization.
- **Exact stationary vector.** For small $n$, solving $\pi M = \pi$ with $\sum \pi = 1$ by [Gaussian elimination](/gaussian-elimination/) gives $\pi$ directly. The test file does this in rational numbers as the reference.
- **Other fusion methods.** [Reciprocal rank fusion](/reciprocal-rank-fusion/) and [CombMNZ](/combmnz/) are linear time and need no matrix; they are the common choices when only speed matters.

## When to use it

Use MC4 when the lists come from systems whose scores cannot be compared, when you care about pairwise majorities more than about rank positions, and when the number of items to merge is small enough for an $n \times n$ matrix, a few hundred to a few thousand. Run local Kemenization on the result, or on the output of any cheaper method, when one bad list must not lift an item above the item that most lists prefer. For large lists of web results, a positional method such as Borda or reciprocal rank fusion is simpler and faster.

## Pitfalls

- **A majority of one list.** The MC4 rule of line L2 counts only the lists that hold both items. An item that appears in one list only beats every item that this list ranks below it, as document 6 does in the toy example. If missing items should count as poor, change line L2 so that a list votes $Q$ over $P$ when it holds $Q$ and not $P$, as in the variant above.
- **No teleport.** With $\varepsilon = 0$, line L3 does nothing, the chain is usually reducible, and line L5 can converge to a vector with many zeros. The order of the items with probability 0 is then only the tie rule of line L6: the toy runs at $\varepsilon = 0$ give $1, 2, 4, 6, 7, 8$, which is document 1 followed by the documents in id order. Keep $\varepsilon > 0$, or use the zero entries only to find the top item.
- **Rounding splits ties.** Documents 2 and 8 have the same exact probability, but power iteration gives two floats that can differ in the last bits. Sorting the raw floats in line L6 then orders them by noise. Round the probabilities to well above the tolerance, or compare exact values, before the sort.
- **Quadratic memory.** The dense matrix of line L2 has $n^2$ entries. Merge only the top of each list, or store MC4 as the majority relation and compute each row when it is needed.
- **Local Kemenization keeps the input order.** Lines L7 to L9 only repair neighbours. Two items that no majority links stay in the order of the input, so the result still depends on the method that produced it.

## Implementations

## History

Dwork, Kumar, Naor and Sivakumar presented rank aggregation for the web at the WWW10 conference in Hong Kong in 2001. Their aim was a metasearch engine that resists spam: a page that tricks one search engine should not reach the top of the merged list. The paper proves that the Kemeny ranking is NP-hard to find already for four lists, which motivated the cheap chains. It defines MC1 to MC4 as heuristics, compares them with Borda and footrule aggregation on the results of real search engines, and introduces local Kemenization and the extended Condorcet criterion. The paper builds the chains without a jump; the teleport of line L3 is the standard repair, taken from PageRank, that later uses of these chains add to make the stationary distribution unique.

## References
