---
tag: 85NC9H
kind: algorithm
slug: pivot-algorithm
name: Pivot algorithm for correlation clustering
aliases:
- KwikCluster
- random pivot clustering
- CC-Pivot
area: machine-learning/clustering
level: research
summary: "Pick a random pivot, cluster it with its + neighbors, remove them, repeat. An expected 3-approximation for correlation clustering on complete graphs (Ailon, Charikar, Newman)."
solves: [correlation-clustering]
model: real-ram
complexity:
  vars: {n: the number of items, m: the number of + pairs}
  time: {worst: "O(n + m)"}
  space: {extra: "O(n)"}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2005
  people: [Nir Ailon, Moses Charikar, Alantha Newman]
  note: Ailon, Charikar and Newman presented the pivot algorithm at STOC 2005 (as CC-Pivot) and in the Journal of the ACM in 2008 (as KwikCluster), with the same analysis for ranking by a feedback arc set in tournaments.
prereqs: [correlation-clustering, randomized-approximation-algorithm, linearity-of-expectation]
see_also: [consensus-clustering, randomized-quicksort, feedback-arc-set-problem, linear-programming-rounding, lp-relaxation, approximation-ratio, apx, random-permutation]
sources:
  - paper: doi:10.1145/1411509.1411513
    title: "Nir Ailon, Moses Charikar and Alantha Newman, Aggregating inconsistent information: ranking and clustering, Journal of the ACM 55(5), 2008, article 23"
    locator: "KwikCluster and its analysis by a fractional packing of bad triangles (expected ratio 3), the LP-based pivot (expected ratio 2.5), the weighted cases, and Table 1 of results"
  - paper: doi:10.1145/1060590.1060692
    title: "Nir Ailon, Moses Charikar and Alantha Newman, Aggregating inconsistent information: ranking and clustering, Proceedings of the 37th ACM Symposium on Theory of Computing (STOC 2005), pages 684 to 693"
    locator: the conference version, where the algorithm is called CC-Pivot
  - paper: doi:10.1145/2746539.2746604
    title: "Shuchi Chawla, Konstantin Makarychev, Tselil Schramm and Grigory Yaroslavtsev, Near optimal LP rounding algorithm for correlation clustering on complete and complete k-partite graphs, STOC 2015, pages 219 to 228"
    locator: the 2.06-approximation by LP rounding with a pivot step
  - paper: doi:10.1016/j.jcss.2004.10.012
    title: "Moses Charikar, Venkatesan Guruswami and Anthony Wirth, Clustering with qualitative information, Journal of Computer and System Sciences 71(3), 2005, pages 360 to 383"
    locator: the APX-hardness of minimizing disagreements on complete graphs, and the earlier 4-approximation
---

The pivot algorithm, called KwikCluster by Ailon, Charikar and Newman, solves [correlation clustering](/correlation-clustering/) on a complete graph whose pairs are labeled $+$ or $-$. It picks a vertex uniformly at random as the pivot, makes a cluster of the pivot and all its remaining $+$ neighbors, removes that cluster, and repeats on the rest. The expected number of disagreements is at most 3 times the optimum. The proof charges each mistake to a *bad triangle* (two $+$ edges and one $-$ edge) and shows that the hit probabilities, divided by 3, form a fractional packing of bad triangles, which is a lower bound on the optimum. It runs in $O(n + m)$ time for $m$ positive pairs, like one pass of randomized quicksort.

## In plain words

You have a list of people and, for each pair, a note that says "friends" or "not friends". You want to put them in groups so that friends are together and non-friends are apart, as much as you can.

Pick one person at random. Put that person and all of their friends who are still without a group into a new group. Then forget about these people, pick a random person among the rest, and do the same, until everyone has a group.

The notes can contradict each other, so some notes will be broken. On average, this simple rule breaks at most three times as many notes as the best possible grouping. The reason is that each broken note comes from a triple of people whose notes do not fit together, and every grouping must break a note in each such triple.

## The algorithm

The input is a symmetric $\pm$ labeling of all pairs of $V = \{1, \ldots, n\}$. Write $u \overset{+}{\sim} v$ for a $+$ pair.

```pseudo id=main
KWIKCLUSTER(V, +)
L1  R ← V                                   ▷ the vertices that have no cluster yet
L2  while R ≠ ∅
L3      pick a pivot p uniformly at random from R
L4      C ← {p} ∪ { v ∈ R : p +~ v }
L5      output the cluster C
L6      R ← R \ C
```

Ailon, Charikar and Newman write it as a recursive call on $R \setminus C$; the loop is the same thing. An equivalent view: draw a uniformly random order of $V$ first, and in line L3 take the first vertex of the order that is still in $R$. The implementation has both forms, and the exact tests average over all $n!$ orders.

**The cost.** A partition pays 1 for each $+$ pair that it splits and each $-$ pair that it joins. The optimum is $\mathrm{OPT}$.

## Example

Take five vertices with the $+$ pairs $01, 02, 12, 23, 34$ and $-$ on the other five pairs. The bad triangles are $\{0, 2, 3\}$, $\{1, 2, 3\}$ and $\{2, 3, 4\}$. The optimum is 1: the partition $\{0, 1, 2\}, \{3, 4\}$ splits only the $+$ pair $23$.

The result depends only on the first pivot here:

| first pivot | clusters | disagreements | bad triangles hit |
|---|---|---|---|
| 0 | $\{0, 1, 2\}$, then $\{3, 4\}$ | 1 ($+$ pair 23 split) | $\{0, 2, 3\}$ |
| 1 | $\{0, 1, 2\}$, then $\{3, 4\}$ | 1 | $\{1, 2, 3\}$ |
| 2 | $\{0, 1, 2, 3\}$, then $\{4\}$ | 3 ($-$ pairs 03, 13 joined; $+$ pair 34 split) | all three |
| 3 | $\{2, 3, 4\}$, then $\{0, 1\}$ | 3 ($-$ pair 24 joined; $+$ pairs 02, 12 split) | all three |
| 4 | $\{3, 4\}$, then $\{0, 1, 2\}$ | 1 | $\{2, 3, 4\}$ |

Each first pivot has probability $1/5$, so the expected cost is $(1 + 1 + 3 + 3 + 1)/5 = 9/5$, which is $1.8 \cdot \mathrm{OPT}$. The averages over all $5! = 120$ orders agree: cost 1 in 72 orders and cost 3 in 48. In each row, the number of disagreements equals the number of bad triangles hit, as the proof below says.

On the star with $+$ pairs $01, 02, 03$, the optimum is 2 and the expected cost is $9/4$: the center as first pivot (probability $1/4$) joins all three $-$ pairs, and a leaf as first pivot gives cost 2.

## Correctness

The output is a partition: each round removes a non-empty set $C$ that contains the pivot, so the loop ends after at most $n$ rounds, and each vertex lands in exactly one cluster.

**The approximation ratio.** Call a bad triangle $T$ *hit* if, at some round, all three vertices of $T$ are still in $R$ and the pivot is one of them.

1. *Each mistake comes from one hit triangle.* A pair that contains the pivot is never a mistake: $+$ neighbors join it and $-$ neighbors stay out. A pair $u, v$ with both in $R$ and the pivot $p \ne u, v$ is decided in this round if at least one of them joins $C$. It is a mistake exactly when $\{p, u, v\}$ is a bad triangle: if both join, then $p u$ and $p v$ are $+$, and the mistake means $u v$ is $-$; if one joins, then exactly one of $p u, p v$ is $+$, and the mistake means $u v$ is $+$. So the cost equals the number of hit bad triangles.
2. *Symmetry.* In each round the pivot is uniform on $R$. So, for a bad triangle $T$ with hit probability $p_T$, the probability that $T$ is hit with pivot $x$ is $p_T/3$ for each of its three vertices $x$.
3. *Packing.* For a pair $e$, the events "$T$ is hit with the pivot opposite to $e$", over the bad triangles $T \ni e$, each make a mistake on $e$ and are disjoint, since $e$ is decided once. So $\sum_{T \ni e} p_T/3 \le 1$.
4. *Lower bound.* Every partition makes a mistake in each bad triangle, so for any weights $\beta_T \ge 0$ with $\sum_{T \ni e} \beta_T \le 1$ for each pair, $\mathrm{OPT} \ge \sum_T \beta_T$. With $\beta_T = p_T/3$,

$$\mathbb{E}[\text{cost}] = \sum_T p_T = 3 \sum_T \beta_T \le 3 \cdot \mathrm{OPT}.$$

The full proof is in the correctness proof. The tests check each step exactly, with fractions, over all $n!$ orders of small random instances, and check $\mathbb{E}[\text{cost}] \le 3 \cdot \mathrm{OPT}$ against a brute-force optimum.

## Complexity

The costs are in the [real RAM](/real-ram/) model.

- **Time.** With adjacency lists of the $+$ pairs and a flag per vertex, line L4 scans the $+$ neighbors of the pivot, and each vertex is removed once. Each $+$ list is scanned at most once (when its owner is the pivot), so the total is $O(n + m)$ for $m$ $+$ pairs. Picking a uniform pivot from $R$ in $O(1)$ is easy with an array and swap-remove, or by fixing a random order first in $O(n)$. With an $n \times n$ matrix as input, as in the implementation, it is $O(n^2)$, which is linear in the input size.
- **Space.** $O(n)$ beyond the input.
- **Randomness.** One random permutation, $O(n \log n)$ random bits.

## Properties

- **The number of clusters is not an input.** It follows from the labels and the pivots.
- **Exact when the labels are consistent.** If there is no bad triangle, $E^+$ is a disjoint union of cliques, and each pivot takes exactly its clique, so the cost is 0.
- **Randomized.** The ratio 3 is in expectation. Running it several times and keeping the best result helps in practice.
- **Combinatorial.** No LP is solved, unlike the earlier 4-approximation of Charikar, Guruswami and Wirth.

## Variants and improvements

- **Weighted pairs.** With weights $w^+_{uv} + w^-_{uv} = 1$, take into $C$ the $v$ with $w^+_{pv} > 1/2$. Ailon, Charikar and Newman prove expected ratio 5 under these probability constraints, and 2 when the $w^-$ also satisfy the triangle inequality.
- **LP-based pivot.** Solve the LP relaxation and put $v$ into the pivot's cluster with a probability that depends on the LP value of $pv$: expected ratio 2.5 (Ailon, Charikar and Newman). Chawla, Makarychev, Schramm and Yaroslavtsev (2015) refined the rounding to 2.06, close to the integrality gap 2 of the LP.
- **Consensus clustering.** On the weights of $m$ input clusterings, the pivot rule with majority votes, combined with picking the best input clustering, gives ratio $11/7$ (Ailon, Charikar and Newman); see [consensus clustering](/consensus-clustering/).
- **Ranking.** The same pivot idea orders the vertices of a tournament like [randomized quicksort](/randomized-quicksort/) and gives expected ratio 3 for the [feedback arc set problem](/feedback-arc-set-problem/) in tournaments.
- **Parallel and streaming.** Because a random order fixes all pivots, many pivots can be processed in parallel rounds when they are not $+$ neighbors of each other.

## When to use it

Use the pivot algorithm when you have a $+$/$-$ label (or a similarity above or below a threshold) on each pair, you do not know the number of clusters, and you need a fast method with a guarantee. It is linear in the number of $+$ pairs and easy to run many times. Do not rely on it alone when an exact or near-exact answer matters on small inputs: an integer program or the LP-based pivot is better. On general graphs with missing pairs the ratio 3 does not hold.

## Pitfalls

- **Missing pairs.** The proof uses that every pair has a label. On a general graph, an unlabeled pair does not count, and the ratio fails.
- **A fixed pivot order.** Taking the pivots in input order (say, by index) loses the guarantee: an adversary can put a bad vertex first. In the example above, pivot 2 first costs 3.
- **Removing too early.** Line L4 must take only the neighbors that are still in $R$. Taking a $+$ neighbor that is already in an earlier cluster breaks the partition.
- **Reading one run as the expectation.** A single run can cost much more than $3 \cdot \mathrm{OPT}$; only the mean is bounded. Repeat and keep the best.

## Implementations

## History

Bansal, Blum and Chawla (2004) introduced correlation clustering and gave a constant factor for minimizing disagreements with a large constant. Charikar, Guruswami and Wirth (2005) improved it to 4 by LP rounding and proved APX-hardness. Ailon, Charikar and Newman (STOC 2005; JACM 2008) gave the simple pivot algorithm with expected ratio 3, the LP-based pivot with 2.5, and the same pivot analysis for ranking aggregation and feedback arc set in tournaments. Chawla, Makarychev, Schramm and Yaroslavtsev (2015) gave 2.06 by a refined LP rounding.

## References
