---
tag: BHYQT7
kind: algorithm
slug: kwiksort-rank-aggregation
name: KwikSort for rank aggregation
aliases:
- Ailon-Charikar-Newman algorithm
- pivot algorithm for Kemeny aggregation
area: algorithmic-game-theory/social-choice-and-voting
level: advanced
summary: "Quicksort with random pivots on pairwise majorities. It is an expected 2-approximation for Kemeny aggregation, and 11/7 when the better of it and an input ranking is kept."
model: word-ram
complexity:
  vars: {n: the number of voters, m: the number of candidates}
  time: {worst: O(n m^2)}
  space: {extra: O(m^2)}
properties: {deterministic: false, comparison: true, recursive: true}
history:
  year: 2005
  people: [Nir Ailon, Moses Charikar, Alantha Newman]
  note: "Ailon, Charikar and Newman gave KwikSort and its analysis at STOC 2005, with the full version in the Journal of the ACM in 2008."
prereqs: [kemeny-rank-aggregation, randomized-quicksort, kendall-tau-distance]
see_also: [rank-aggregation, feedback-arc-set-problem, slater-rule, markov-chain-rank-aggregation, approximation-ratio, quicksort, randomized-algorithm, smith-set]
sources:
  - paper: doi:10.1145/1411509.1411513
    title: "Nir Ailon, Moses Charikar and Alantha Newman, Aggregating inconsistent information: ranking and clustering, Journal of the ACM 55(5) (2008), Article 23"
    locator: "the analysis of KwikSort for feedback arc set in tournaments (expected ratio 3, by a fractional packing of triangles), and the section on rank aggregation (expected ratio 2 for KwikSort on the majority tournament, and 11/7 for the better of KwikSort and Pick-A-Perm)"
  - paper: doi:10.1145/1060590.1060692
    title: "Nir Ailon, Moses Charikar and Alantha Newman, Aggregating inconsistent information: ranking and clustering, Proceedings of the 37th ACM Symposium on Theory of Computing (STOC 2005), 684-693"
    locator: "the conference version of the same results"
---

KwikSort is a fast approximation algorithm for [Kemeny rank aggregation](/kemeny-rank-aggregation/): given the rankings of many voters, find one ranking that disagrees with them as little as possible in total. Finding the best ranking is NP-hard. KwikSort runs [quicksort with random pivots](/randomized-quicksort/), but compares two candidates by the majority of the voters instead of by a key. Because the majority relation can have cycles, the result depends on the pivots, and the analysis bounds its expected cost. Ailon, Charikar and Newman proved that the expected cost is at most 2 times the optimum. Keeping the better of the KwikSort ranking and one of the input rankings lowers the ratio to $11/7$. The same algorithm on any tournament has expected ratio 3 for the [feedback arc set](/feedback-arc-set-problem/) problem, which is the [Slater rule](/slater-rule/) for voting.

## In plain words

You want one ranking that agrees with many voters as much as possible. Pick a candidate at random. Put every candidate that most voters prefer to it on its left, and every other candidate on its right. Then do the same, separately, inside the left group and inside the right group, until every group has one candidate. Because majorities can go in circles, some choices of the random candidate work better than others, but on average the result costs at most twice the best possible. As a safety net, compare the result with the best ballot that some voter cast, and keep the better one.

## The problem

There are $m$ candidates $A = \{0, \ldots, m - 1\}$ and a profile $P$ of $n$ rankings. Let $N(x, y)$ be the number of voters who rank $x$ above $y$. The Kemeny cost of a ranking $r$ is the sum of its [Kendall tau distances](/kendall-tau-distance/) to the ballots,

$$K(r) = \sum_{x \text{ above } y \text{ in } r} N(y, x),$$

and the problem is to find a ranking with the least cost, $\mathrm{OPT}$. The majority tournament $T$ has an arc $x \to y$ when $N(x, y) > N(y, x)$; this page breaks ties toward the candidate with the smaller index, so $T$ has exactly one arc between each pair. An algorithm with expected ratio $\alpha$ returns a ranking with $\mathbb{E}[K(r)] \le \alpha \cdot \mathrm{OPT}$ on every profile.

## The algorithm

```pseudo id=main
KWIKSORT(V, T)
L1  if |V| ≤ 1 then return V
L2  p ← a uniformly random member of V
L3  L ← [u ∈ V \ {p} : u → p in T]
L4  R ← [u ∈ V \ {p} : p → u in T]
L5  return KWIKSORT(L, T), then p, then KWIKSORT(R, T)

AGGREGATE(P, m)
L6  T ← majority tournament of P
L7  r1 ← KWIKSORT(A, T)
L8  r2 ← the ballot of P with the least Kemeny cost
L9  return r2 if K(r2) ≤ K(r1), else r1
```

Lines L1 to L5 are randomized quicksort with the arcs of $T$ as the comparisons. The code runs it with an explicit stack and a seeded random generator, so a run can be repeated. Line L8 is a deterministic form of Pick-A-Perm, which in the paper takes a ballot at random. The best ballot costs no more than a random one, so every bound for the better of KwikSort and Pick-A-Perm holds for line L9.

## Example

Take the profile of the example on the [Slater rule](/slater-rule/) page, with four candidates $a, b, c, d$ and 13 voters:

| voters | ranking |
|---|---|
| 4 | $d \succ b \succ c \succ a$ |
| 6 | $b \succ a \succ d \succ c$ |
| 3 | $c \succ a \succ d \succ b$ |

The majority tournament has the arcs $b \to a$, $b \to c$, $d \to c$, $a \to d$, $c \to a$ and $d \to b$. Each of the four first pivots has probability $1/4$:

| first pivot | left, right | output | $K$ |
|---|---|---|---|
| $a$ | $\{b, c\}$, $\{d\}$ | $b \succ c \succ a \succ d$ | 33 |
| $b$ | $\{d\}$, $\{a, c\}$ | $d \succ b \succ c \succ a$ | 30 |
| $c$ | $\{b, d\}$, $\{a\}$ | $d \succ b \succ c \succ a$ | 30 |
| $d$ | $\{a\}$, $\{b, c\}$ | $a \succ d \succ b \succ c$ | 33 |

Every group of two is sorted by its single arc. The expected Kemeny cost of KwikSort is $31.5$. The optimum is $27$, reached by $b \succ a \succ d \succ c$, which is also the ballot of the 6 voters. So line L8 finds it and line L9 returns it. Here KwikSort alone has ratio $31.5/27 = 7/6$, and the combined algorithm is exact.

## Correctness

KwikSort always returns a ranking of all candidates, since each call places its pivot and passes every other candidate to exactly one side. If the majority relation is transitive, every split agrees with it, and the output is that order, which is then optimal. The ratio 3 for feedback arc set in tournaments has a short proof, given in full in `proofs/correctness.md`. A pair $u \to v$ ends in the wrong order only when a pivot $w$ separates them with $v \to w \to u$, so that $u, v, w$ form a directed triangle. So the cost equals the number of triangles whose three candidates are still together when one of them becomes the pivot. Each arc can be charged by at most one such triangle, and each of the three arcs of a triangle is equally likely to be the charged one. So the probabilities of the triangles, divided by 3, form a fractional packing of triangles into arcs, which is a lower bound on the optimum. For rank aggregation, Ailon, Charikar and Newman extend the argument with weights, and the tests check the ratios 2 and $11/7$ exactly on small profiles by computing the full output distribution.

## Complexity

Counting $N$ takes $O(n m^2)$ time, and line L8 also takes $O(n m^2)$ to compute the cost of every ballot. KwikSort itself compares each pair at most once, so it makes at most $m(m - 1)/2$ comparisons. When the majority relation is a linear order, it is exactly randomized quicksort and makes $O(m \log m)$ comparisons in expectation. The total is $O(n m^2)$ time in the worst case on the [word RAM](/word-ram/), with $O(m^2)$ space for $N$ and $T$. This is the same as the cost of reading the pairwise counts, while the exact problem is NP-hard.

## Properties

- **Expected ratios.** On every profile, $\mathbb{E}[K(\mathrm{KwikSort})] \le 2 \cdot \mathrm{OPT}$, and the better of KwikSort and Pick-A-Perm has expected cost at most $\frac{11}{7} \cdot \mathrm{OPT}$. On any tournament, the expected number of backward arcs is at most 3 times the minimum.
- **The best ballot is a 2-approximation.** By the triangle inequality for the Kendall tau distance, some ballot has cost at most $2 \cdot \mathrm{OPT}$. Line L9 is never worse than this.
- **Smith set on top.** Every member of the [Smith set](/smith-set/) beats every outsider, so no pivot sends an outsider to the left of a member. KwikSort always ranks the Smith set first, and a Condorcet winner first of all.
- **Randomized.** Different pivots can give rankings of different cost, as in the example. With a fixed seed, the code is deterministic.

## Variants and improvements

- **LP-based pivoting.** In the same paper, Ailon, Charikar and Newman also round an LP relaxation with the pivot rule and get a smaller ratio for rank aggregation, at the cost of solving the LP.
- **Deterministic pivots.** Later work chooses the pivots by rules that follow the LP solution or the ranking by scores, and keeps a constant ratio without randomness.
- **Better algorithms.** The weighted feedback arc set problem in tournaments, and so Kemeny aggregation, has a polynomial time approximation scheme. See the [Kemeny rank aggregation](/kemeny-rank-aggregation/) page for the details.
- **Correlation clustering.** The same pivot idea, with "similar" and "different" in place of "above" and "below", gives an expected 3-approximation for correlation clustering on complete graphs, also in the paper by Ailon, Charikar and Newman.
- **Local search.** A common practice is to improve the KwikSort output by swaps or moves of single candidates while the Kemeny cost goes down.

## When to use it

Use KwikSort when you need a good consensus ranking of many candidates quickly, as in meta search, where many search engines rank the same pages, or in the fusion of ranked lists in recommendation systems. It needs only the majority relation, so it also works when the inputs are partial lists, if the pairwise counts can be formed. For a few dozen candidates, an exact integer program solver for [Kemeny's rule](/kemeny-rank-aggregation/) is often fast enough and gives the optimum.

## Pitfalls

- **Expecting the optimum.** KwikSort is an approximation. On profiles with cycles it can return a ranking that costs much more than the best ballot. Keep the comparison of line L9.
- **Ties in the majority relation.** With an even number of voters, some pairs are tied. Break the ties by a fixed rule so that every comparison has an answer. A tie sent to both sides, or to neither, loses candidates or repeats them.
- **Running time of the counts.** The sort is fast, but the counts take $O(n m^2)$ time. For very long lists, sample voters or count only the pairs that the sort compares.
- **Recursion depth.** With bad luck the recursion is $m$ levels deep. Use an explicit stack, as the code does.

## Implementations

## History

Nir Ailon, Moses Charikar and Alantha Newman introduced KwikSort at STOC 2005 in a paper on aggregating inconsistent information, which treats feedback arc set in tournaments, rank aggregation and correlation clustering with one pivot method. The full version appeared in the Journal of the ACM in 2008. Their analysis by fractional triangle packings became a standard tool. Rank aggregation itself was studied for the web by Dwork, Kumar, Naor and Sivakumar in 2001, and Kemeny proposed the cost in 1959.

## References
