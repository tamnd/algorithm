---
tag: 2CGC7D
kind: algorithm
slug: borda-count
name: Borda count
aliases:
- Borda method
area: information-retrieval-and-ai-reasoning/ranking-models
level: intro
summary: Gives each item points by its position in each input ranking and sorts the items by the total of their points.
solves: [rank-aggregation]
model: word-ram
complexity:
  vars: {n: the number of distinct items in the input lists, k: the number of lists}
  time: {worst: O(n k + n log n)}
  space: {extra: O(n)}
properties: {deterministic: true, comparison: false, recursive: false}
history:
  year: 1784
  people: [Jean-Charles de Borda]
  note: Borda described the rule for elections to the French Academy of Sciences in a memoir printed in 1784 in the volume for 1781; Aslam and Montague used it for metasearch in 2001.
prereqs: [rank-aggregation]
see_also: [kemeny-rank-aggregation, markov-chain-rank-aggregation, reciprocal-rank-fusion, combmnz, spearman-footrule, kendall-tau-distance]
sources:
  - paper: "Jean-Charles de Borda, Mémoire sur les élections au scrutin, Histoire de l'Académie Royale des Sciences, année 1781 (printed 1784), 657-665"
    locator: the rule that gives a candidate points by its place on each ballot and elects the candidate with the largest total
  - paper: doi:10.1145/383952.384007
    title: Javed A. Aslam and Mark H. Montague, Models for metasearch, Proceedings of the 24th Annual International ACM SIGIR Conference (SIGIR 2001), 276-284
    locator: Borda-fuse, the Borda count used to merge the result lists of several retrieval systems
  - paper: doi:10.1145/1798596.1798608
    title: Don Coppersmith, Lisa K. Fleischer and Atri Rudra, Ordering by weighted number of wins gives a good ranking for weighted tournaments, ACM Transactions on Algorithms 6(3), Article 55 (2010)
    locator: the proof that ordering by weighted number of wins, which for full rankings is the Borda order, is a 5-approximation of the minimum feedback arc set in a weighted tournament, and so of the Kemeny ranking
  - paper: doi:10.1145/371920.372165
    title: Cynthia Dwork, Ravi Kumar, Moni Naor and D. Sivakumar, Rank aggregation methods for the Web, Proceedings of the 10th International World Wide Web Conference (WWW10), 613-622
    locator: Borda aggregation as one of the methods compared for metasearch, with partial lists
---

The Borda count merges several rankings of the same items into one. Each ranking gives points to the items by their positions, the top item gets the most, and the merged ranking sorts the items by their total points. Jean-Charles de Borda proposed it in the 18th century for elections, where each voter ranks the candidates. In information retrieval it is a standard method of [rank aggregation](/rank-aggregation/), often called Borda-fuse, that merges the result lists of several search systems using only the ranks, not the scores.

## In plain words

Several voters each put the same candidates in order. In each order, the last candidate gets 1 point, the one above it gets 2, and so on up to the top candidate. Add up the points that each candidate gets from all voters, and sort the candidates by their totals. A search system that returns only its top results is a voter who did not rank everyone. The candidates that it left out share the points of the empty places equally, so every voter gives out the same number of points. The total also counts something easy to explain: how many of the head-to-head contests a candidate wins, summed over all voters. The method is fast and fair to each voter, but it can elect a candidate other than the one that a majority prefers to each rival.

## The problem

The input is $k$ ranked lists $L_1, \ldots, L_k$. Each list holds distinct items, best first, and it may be partial. Let $U$ be the union of the items and $n = |U|$. For a list $L$ that holds $x$, $L(x)$ is the rank of $x$ in $L$, from 1. The output is one ranking of all of $U$. No scores are given, and the lists may hold different items, as is usual for the top results of different search engines.

## The algorithm

```pseudo id=main
BORDA(L1, ..., Lk)
L1  U ← the union of the items of L1, ..., Lk; n ← |U|
L2  s(x) ← 0 for each x in U
L3  for each list L:
L4      for i ← 1 to |L|: s(L[i]) ← s(L[i]) + (n - i + 1)
L5      for each x in U not in L: s(x) ← s(x) + (n - |L| + 1) / 2
L6  return U sorted by s, highest first, ties to the smaller item
```

Line L4 gives $n$ points to the top of each list, $n - 1$ to the second, and so on. Line L5 handles partial lists: the ranks $|L| + 1$ to $n$ are empty, and their points, $1 + 2 + \cdots + (n - |L|)$, are shared equally by the $n - |L|$ missing items, which gives each one $(n - |L| + 1)/2$. This is the rule that Borda-fuse uses. With it, every list hands out exactly $n(n+1)/2$ points, full or not. The code keeps the scores as exact fractions, because the half points of line L5 must not cause rounding errors in the tie test of line L6.

## Example

Take the two runs of the toy collection for the query "sorted array search": the [BM25](/bm25/) list $A = 1, 2, 8, 7, 4$ and a second list $B = 1, 6, 8, 2, 4$. The union is $\{1, 2, 4, 6, 7, 8\}$, so $n = 6$. Each list holds 5 items and misses one, which gets $(6 - 5 + 1)/2 = 1$ point. The table shows the scores after each pass of line L3.

| document | 1 | 2 | 8 | 6 | 7 | 4 |
|---|---|---|---|---|---|---|
| points from $A$ | 6 | 5 | 4 | 1 (missing) | 3 | 2 |
| score after $A$ | 6 | 5 | 4 | 1 | 3 | 2 |
| points from $B$ | 6 | 3 | 4 | 5 | 1 (missing) | 2 |
| score after $B$ | 12 | 8 | 8 | 6 | 4 | 4 |

Line L6 returns $1, 2, 8, 6, 4, 7$. Documents 2 and 8 tie at 8 points and documents 4 and 7 tie at 4, so the tie rule decides those places. Ties like these are common with few lists.

Now take three candidates and five voters: three ballots say $a, b, c$ and two say $b, c, a$. The scores are $a = 3 \cdot 3 + 2 \cdot 1 = 11$, $b = 3 \cdot 2 + 2 \cdot 3 = 12$ and $c = 3 \cdot 1 + 2 \cdot 2 = 7$, so Borda elects $b$. Yet $a$ beats $b$ on 3 of the 5 ballots and beats $c$ on 3 of 5: $a$ is the Condorcet winner, the candidate that a majority prefers to each rival. Borda adds margins, and $b$'s large lead over $c$ (5 to 0) outweighs its small loss to $a$. The [Kemeny ranking](/kemeny-rank-aggregation/) of this profile is $a, b, c$, with total [Kendall tau distance](/kendall-tau-distance/) 4, while the Borda order $b, a, c$ has distance 5.

## Correctness

Lines L1 to L5 compute $s(x) = \sum_l p_l(x)$, where $p_l(x)$ is $n - L_l(x) + 1$ when $L_l$ holds $x$ and $(n - |L_l| + 1)/2$ when it does not, and line L6 sorts by $s$. The file proofs/correctness.md proves what this score means. Extend each list by putting its missing items below its listed items, tied with each other. Then $s(x)$ is $k$ plus the number of items that $x$ beats, summed over the lists, with a tie worth half. For full lists, every order by decreasing $s$ minimizes the sum over the lists of $\sum_x (\sigma(x) - L(x))^2$, the squared distance between rank positions; the proof expands the square and uses an exchange argument.

For the Kemeny objective there is a proved bound that the code inherits. Coppersmith, Fleischer and Rudra prove that, on full lists, the Borda order has a total Kendall tau distance at most 5 times the minimum. The tests check this by brute force over all permutations of up to 6 items. On those random profiles the worst ratio was below 2; that is a measurement on small random inputs, not a bound.

## Complexity

Line L4 runs once for each entry of each list and line L5 once for each missing pair of an item and a list, so lines L3 to L5 take $\Theta(n k)$ time with a hash map for the scores. Line L6 sorts $n$ items in $O(n \log n)$. The total is $O(n k + n \log n)$ time, and the extra space is $O(n)$ for the scores and the set of items of the current list. If only the listed items are needed, line L5 can add the shares lazily: keep one running total of the shares of each list and subtract the shares of the listed items, which brings the time to $O(\sum_l |L_l| + n \log n)$.

## Properties

- **Anonymous and neutral.** Renaming the lists or the items does not change the result, apart from the tie rule of line L6.
- **Scores add.** The score of a profile is the sum of the scores of its lists. So if two groups of lists each rank $x$ above $y$ by score, their union does too.
- **Monotone.** Moving $x$ up one place in one list raises $s(x)$ by 1, lowers the item that it passes by 1 and changes no other score, so $x$ never falls in the result.
- **Not Condorcet consistent.** The five-voter profile above shows that the Borda winner need not be the Condorcet winner. On full lists Borda never puts a Condorcet loser, an item that a majority ranks below each rival, first: by the pairwise form of the score, such an item wins fewer than $k/2$ contests against each rival, so its score is below the average score $k(n+1)/2$, and some other item scores more.
- **Not independent of other items.** In the same profile, deleting $c$ leaves $a$ against $b$, which $a$ wins 3 to 2. So the order of $a$ and $b$ depends on a third candidate.

## Variants and improvements

- **Weighted Borda.** Multiply the points of each list by a weight for its system, learned from training queries. The pairwise form still holds, with weighted counts.
- **Other position weights.** Any decreasing points per rank give a positional method. The weight $1/(k + i)$ for rank $i$ is [reciprocal rank fusion](/reciprocal-rank-fusion/), which gives much more weight to the top ranks than the linear Borda points do.
- **Missing items get nothing.** Some systems give 0 points to missing items. Then a long list gives out more points than a short one, so the lists that return more results have more influence on the merged order.
- **Local Kemenization.** Run the clean-up pass of [Markov chain rank aggregation](/markov-chain-rank-aggregation/) on the Borda order. It swaps neighbours that a strict majority orders the other way, and it never increases the Kendall distance. On the five-voter profile it turns $b, a, c$ into $a, b, c$.
- **Score fusion.** When the systems give comparable scores, [CombSUM and CombMNZ](/combmnz/) use the scores in place of the ranks.

## When to use it

Use the Borda count when you must merge ranked lists whose scores cannot be compared, the lists are short or have similar lengths, and you want a method that is simple to explain and to compute. It is a good first baseline for metasearch and for merging the votes of several rankers in an ensemble. If the top of each list matters much more than the middle, as in most web search, reciprocal rank fusion is a better default. If majorities matter, as in the five-voter example, add local Kemenization or use a pairwise method.

## Pitfalls

- **Points scaled by the list length.** Giving $|L| - i + 1$ points in line L4 in place of $n - i + 1$ makes the top of a short list worth less than the top of a long list, so the result depends on how deep each system returned results. Use $n$, the size of the union, for every list.
- **Missing items left out of the count.** If line L5 is dropped, an item that a list misses gets 0 from it, while line L5 gives it the average of the empty places. With $n = 100$ and a list of 10, that is 0 in place of 45.5, against 91 for the tenth item of the list. The two rules give different results whenever items differ in how many lists hold them, so keep line L5 or drop it on purpose, and say which.
- **Floating point halves.** The share $(n - |L| + 1)/2$ is a half when $n - |L|$ is even, and sums of halves in floats can split exact ties. Keep the scores as integers times 2, or as fractions, before line L6.
- **Ties decided by accident.** With two lists, ties are frequent, as documents 2 and 8 show. State the tie rule of line L6, or break ties by a third signal such as the best single rank.
- **Strategic lists.** A system that wants to push $x$ can put $x$ first and a strong rival last, as the ballots $b, c, a$ do to $a$. Borda is known to be open to this kind of manipulation, so do not use it to merge lists from parties that compete.

## Implementations

## History

Borda read a paper on elections to the French Academy of Sciences in 1770, and his memoir appeared in 1784 in the Academy's volume for 1781. He argued that plurality voting can elect a candidate whom most voters rank last, and proposed giving each candidate points by its place on each ballot. Condorcet, who edited the volume, criticized the rule because it can reject the candidate who wins every head-to-head majority, which is the failure shown in the example. In information retrieval, Aslam and Montague adapted it as Borda-fuse in 2001, and reported that it often beat the best single input system on TREC data; that is a measurement on those runs. Dwork, Kumar, Naor and Sivakumar used it the same year as a baseline for web metasearch, and Coppersmith, Fleischer and Rudra later proved its factor 5 bound for the Kemeny objective.

## References
