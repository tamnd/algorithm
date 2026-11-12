---
tag: 3X6R9R
kind: algorithm
slug: canopy-clustering
name: Canopy clustering
aliases:
- canopy clustering of McCallum, Nigam and Ungar
area: machine-learning/clustering
level: advanced
summary: Cheap overlapping pre-clustering used to limit the expensive distance computations of a later clustering step.
model: real-ram
complexity:
  vars: {n: the number of points, z: the number of canopies, s: the largest canopy size}
  time: {worst: "O(n z + z s^2)"}
  space: {extra: "O(n + z s)"}
properties: {online: false, deterministic: false, recursive: false}
history:
  year: 2000
  people: [Andrew McCallum, Kamal Nigam, Lyle H. Ungar]
  note: McCallum, Nigam and Ungar introduced canopies at KDD 2000 to cluster large sets of bibliographic citations, where the cheap distance came from an inverted index.
prereqs: [clustering-problem, metric-space]
see_also: [k-means, single-linkage-clustering, agglomerative-clustering, inverted-index, locality-sensitive-hashing, bfr-algorithm, birch, dbscan]
sources:
  - paper: "A. McCallum, K. Nigam and L. H. Ungar, Efficient clustering of high-dimensional data sets with application to reference matching, Proceedings of KDD 2000, pp. 169-178"
    title: McCallum, Nigam and Ungar 2000
    locator: "Section 2 (the canopy method with thresholds T1 > T2) and Section 3 (canopies with greedy agglomerative clustering, k-means and EM)"
  - book: isbn:9781108476348
    title: Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets, third edition
    locator: Chapter 7 (clustering), on clustering in non-Euclidean spaces and large data
---

Canopy clustering is a cheap first step for clustering large data, given by McCallum, Nigam and Ungar in 2000. It uses a cheap, rough distance and two thresholds $T_1 > T_2$. It picks a point as a center, puts all points within cheap distance $T_1$ into the center's canopy, and removes all points within $T_2$ from the list of possible centers. It repeats until no possible center is left. The canopies overlap, and every point is in at least one of them. A second, expensive clustering method then compares only the points that share a canopy. Canopy clustering is a heuristic: it gives no bound on the final clusters, but it can cut the number of expensive distance computations by a large factor.

## In plain words

Suppose you must group a million book references, and comparing two references carefully is slow. A rough test is fast: for example, count the words that the two references share.

Take any reference and, with the rough test, find all references that are fairly similar to it. They form a canopy. The references that are very similar to it cannot start a new canopy later. Take another reference that is still allowed, and do the same. Go on until each reference is in some canopy.

Canopies can overlap, so a reference can be in more than one. Now do the careful comparison only for references that share a canopy. References in different canopies are taken to be different without a careful look.

## The problem

The input is a set $P$ of $n$ points, a cheap distance $c$ (fast but rough), an expensive distance $e$ (slow but exact), and two thresholds $T_1 > T_2 > 0$. The goal is a cover of $P$ by overlapping subsets, the canopies, such that points that are close in $e$ share a canopy, and the canopies are small. The final clustering, for example by [agglomerative clustering](/agglomerative-clustering/), [k-means](/k-means/) or EM, then uses $e$ only inside the canopies.

## The algorithm

```pseudo id=main
CANOPIES(P, c, T1, T2)         ▷ T1 > T2 > 0
L1  A ← P                        ▷ the points that can still become centers
L2  while A is not empty do
L3      z ← a random point of A
L4      K(z) ← {p ∈ P : c(z, p) < T1}; output the canopy K(z)
L5      remove from A every p with c(z, p) < T2   (this removes z)
    ▷ second stage, here single linkage at level θ
L6  join p and q when they share a canopy and e(p, q) ≤ θ
```

Line L4 looks at all points of $P$, not only those in $A$, so a point removed by one center can still be in other canopies. That is the overlap. Line L5 is what stops the loop: a point within $T_2$ of a center never becomes a center itself.

The cheap distance is often computed with an [inverted index](/inverted-index/): for text, the points that share a rare word with $z$ are found from the index, and their number of shared words gives the cheap distance. Points with no shared word are never looked at.

## Example

Take the points $0, 1, 2, 3, 4, 5, 9, 10, 11$ on a line, with $c(p, q) = |p - q|$, $T_1 = 3$ and $T_2 = 1.5$. Suppose the random choices give the centers in the order $2, 10, 0, 5$.

| center | canopy $K(z)$ (distance $< 3$) | removed from $A$ (distance $< 1.5$) | $A$ after the step |
|---|---|---|---|
| 2 | $0, 1, 2, 3, 4$ | $1, 2, 3$ | $0, 4, 5, 9, 10, 11$ |
| 10 | $9, 10, 11$ | $9, 10, 11$ | $0, 4, 5$ |
| 0 | $0, 1, 2$ | $0$ | $4, 5$ |
| 5 | $3, 4, 5$ | $4, 5$ | empty |

The four canopies overlap in $0, 1, 2, 3, 4$. Pairs that share a canopy: 10 pairs in $\{0, \ldots, 4\}$, 3 pairs in $\{9, 10, 11\}$, and 2 more pairs $(3, 5)$ and $(4, 5)$, so 15 pairs. Without canopies there are $\binom{9}{2} = 36$ pairs. Every pair at distance below $T_1 - T_2 = 1.5$, that is, at distance 1, is among the 15.

## Correctness

Each round removes its center from $A$, so the loop stops after at most $n$ rounds. A point leaves $A$ only when it is within $T_2$ of a center, and $T_2 < T_1$, so it is in that center's canopy: the canopies cover $P$. Two centers are at cheap distance at least $T_2$, because the later one would have been removed otherwise.

If the cheap distance satisfies the [triangle inequality](/triangle-inequality/), two points at cheap distance below $T_1 - T_2$ always share a canopy: one of them is within $T_2$ of a center $z$, and then the other is within $T_1$ of $z$. So if the cheap distance never exceeds the expensive one, single linkage at a level $\theta < T_1 - T_2$ inside the canopies gives exactly the result of single linkage on all pairs. The proofs are on the correctness page.

## Complexity

- **Canopies.** Each round computes the cheap distance from the center to all $n$ points, so $z$ canopies take $O(nz)$ cheap distances. With an inverted index, a round looks only at points that share a term with the center, which is often much less than $n$.
- **Second stage.** Only pairs inside a canopy are compared: at most $\sum_{z} |K(z)|^2 / 2 \le z s^2 / 2$ expensive distances, where $s$ is the largest canopy. If each point is in a few canopies and the canopies are small, this is far below $n^2/2$.
- **Space.** The canopies take $O(\sum |K(z)|) \le O(zs)$ memory, plus $O(n)$ for $A$.

## Properties

- **Overlapping.** A point can be in many canopies. This is a cover, not a partition.
- **Random.** The result depends on the order of the centers. With a fixed seed it is deterministic.
- **Two thresholds.** A large $T_1$ makes large canopies and more expensive work; a small $T_2$ makes more canopies.
- **Any cheap distance.** The cheap distance needs no structure, but the guarantee for close pairs needs the triangle inequality.
- **Heuristic.** No bound on the final clusters holds without a relation between the cheap and the expensive distance.

## Variants and improvements

- **Canopy k-means.** Each center of [k-means](/k-means/) is linked to the canopies it starts in, and a point is compared only with centers that share a canopy with it.
- **Canopy EM.** The same restriction for the E-step of a mixture model, as in the original paper.
- **Canopies for record linkage.** In entity resolution, canopies are a form of blocking; [locality-sensitive hashing](/locality-sensitive-hashing/) is another one, with probability bounds.
- **Choosing $k$.** The number of canopies can be used as a first guess of $k$ for k-means.
- **Removal rule.** Some versions remove only the center from $A$ when $T_2$ is very small; then the canopies overlap much more.

## When to use it

Use canopies when the data is large, the expensive distance is slow, and a cheap distance is available that is roughly related to it. Examples are text, where shared rare words give a cheap distance, and records with many fields. If the full distance matrix is affordable, compute it and skip the canopies. If the points are in a low dimension, a spatial index such as a [kd-tree](/kd-tree/) finds close pairs exactly.

## Pitfalls

- **Wrong order of thresholds.** The method needs $T_1 > T_2$. With $T_1 \le T_2$ a point can be removed from $A$ without being in any canopy.
- **Too large canopies.** If $T_1$ is large, most points share a canopy and nothing is saved.
- **Misses.** Points close in the expensive distance but far in the cheap distance are never compared. Check that the cheap distance is not too rough.
- **Not a final clustering.** Canopies are a pre-clustering. Their overlaps must be resolved by the second stage.

## Implementations

## History

McCallum, Nigam and Ungar introduced canopies at KDD 2000. Their application was reference matching, the grouping of citations that refer to the same paper, for the Cora search engine of computer science papers; the cheap distance was computed from an inverted index of words. They used canopies with greedy agglomerative clustering, k-means and EM. The method became widely known as a pre-clustering step in large-scale machine learning programs, often before k-means.

## References
