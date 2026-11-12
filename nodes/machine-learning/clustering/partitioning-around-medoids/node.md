---
tag: 52CM06
kind: algorithm
slug: partitioning-around-medoids
name: Partitioning around medoids
aliases:
- PAM
- k-medoids
- PAM BUILD and SWAP
area: machine-learning/clustering
level: core
summary: Local search that swaps medoids with non-medoid points while the total dissimilarity decreases.
solves: [k-median-problem]
model: real-ram
complexity:
  vars: {n: the number of objects, k: "the number of medoids (at most n)", s: "the number of swaps that SWAP makes"}
  time: {worst: "O(n^2 k + (s + 1) k (n - k) n)", best: "O(n^2 k)"}
  space: {extra: "Θ(n)"}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1987
  people: [Leonard Kaufman, Peter J. Rousseeuw]
  note: Kaufman and Rousseeuw gave PAM in 1987 and described it with its program in their 1990 book Finding Groups in Data; Schubert and Rousseeuw made the SWAP pass faster by a factor of about k in 2019.
prereqs: [k-median-problem, local-search, metric-space]
see_also: [k-means, k-median-problem, k-median-inapproximability, local-search, streaming-k-median, silhouette-coefficient, clustering-problem, hard-and-soft-clustering]
sources:
  - book: isbn:9780471878766
    title: Leonard Kaufman and Peter J. Rousseeuw, Finding Groups in Data
    locator: Chapter 2 (partitioning around medoids, program PAM), the BUILD and SWAP phases
  - paper: "L. Kaufman and P. J. Rousseeuw, Clustering by means of medoids, in Statistical Data Analysis Based on the L1-Norm and Related Methods, North-Holland, 1987, pp. 405-416"
    title: Kaufman and Rousseeuw 1987
    locator: the first description of the medoid method
  - paper: "E. Schubert and P. J. Rousseeuw, Fast and eager k-medoids clustering: O(k) runtime improvement of the PAM, CLARA, and CLARANS algorithms, Information Systems 101, 2021, article 101804"
    title: Schubert and Rousseeuw 2021
    locator: FastPAM1 (same result as PAM), FastPAM2, FasterPAM and the eager swap
  - paper: "V. Arya, N. Garg, R. Khandekar, A. Meyerson, K. Munagala and V. Pandit, Local search heuristics for k-median and facility location problems, SIAM Journal on Computing 33(3), 2004, pp. 544-562"
    title: Arya et al. 2004
    locator: the locality gap 3 + 2/p for p simultaneous swaps, which is 5 for single swaps
  - paper: "R. T. Ng and J. Han, Efficient and effective clustering methods for spatial data mining, Proceedings of VLDB 1994, pp. 144-155"
    title: Ng and Han 1994
    locator: CLARANS, a randomized search over single swaps, and the comparison with PAM and CLARA
---

Partitioning around medoids (PAM) is the classical local search for the [k-median problem](/k-median-problem/) on a dissimilarity matrix. It chooses $k$ of the given objects as medoids and assigns each object to its nearest medoid. A greedy BUILD phase picks a good first set of medoids. A SWAP phase then replaces one medoid by one non-medoid, always the replacement that lowers the total dissimilarity most, and stops when no replacement helps. The result is a local optimum for single swaps. In a metric its cost is at most 5 times the optimum.

## In plain words

You must choose $k$ of your objects as representatives, and each object is served by the representative that is most similar to it. The aim is that the sum of all the dissimilarities to the representatives is small.

PAM first builds a set of representatives one at a time: the first one is the most central object, and each next one is the object that helps most. Then it tries all exchanges of one representative for one other object, and makes the exchange that helps most. It repeats this until no exchange helps.

Because the representatives are real objects, PAM needs only the dissimilarities between objects, not coordinates or averages. This makes it useful for words, sequences or any data where a mean does not exist.

## The problem

The input is a symmetric $n \times n$ matrix $D$ of dissimilarities with $D[j][j] = 0$, and an integer $k$ with $1 \le k \le n$. For a set $M$ of $k$ objects (the medoids), the cost is

$$\mathrm{cost}(M) = \sum_{j=1}^{n} \min_{m \in M} D[j][m].$$

The goal is a set $M$ with a small cost. This is the discrete [k-median problem](/k-median-problem/) where the candidate centers are the objects. It is NP-hard, so PAM does not promise the optimum. If $D$ is a [metric](/metric-space/), the result is within a factor 5 of the optimum. PAM also runs when $D$ does not satisfy the [triangle inequality](/triangle-inequality/), but then it has no factor.

## The algorithm

```pseudo id=main
PAM(D, k)
    ▷ BUILD
L1  m1 ← the object i with the least row sum Σ_j D[j][i];  M ← [m1]
L2  for each object j do near[j] ← D[j][m1]
L3  while |M| < k do
L4      for each object i ∉ M do g(i) ← Σ_j max(near[j] − D[j][i], 0)
L5      add the i with the largest g(i) to M;  near[j] ← min(near[j], D[j][i]) for each j
    ▷ SWAP
L6  repeat
L7      for each medoid m ∈ M and each object h ∉ M do
L8          T(m, h) ← Σ_j (new_j − D_j)        ▷ change of the cost when h replaces m
L9      if the least T(m, h) is ≥ 0 then return M
L10     replace m by h in M for the pair (m, h) with the least T(m, h)
```

In line L8, $D_j$ is the dissimilarity of object $j$ to its nearest medoid $m_j$, and $E_j$ to its second nearest medoid. After $h$ replaces $m$, object $j$ has the new value $\mathrm{new}_j = \min(E_j, D[j][h])$ if $m_j = m$, and $\mathrm{new}_j = \min(D_j, D[j][h])$ if not. So each pair costs $O(n)$ time when $D_j$, $m_j$ and $E_j$ are computed once per pass. The value $g(i)$ in line L4 is the decrease of the cost when $i$ is added, so BUILD is the greedy algorithm for the same objective. Ties go to the smaller index.

## Example

Take seven points in the plane with the Manhattan distance, and $k = 2$: $x_0 = (9, 4)$, $x_1 = (5, 8)$, $x_2 = (0, 7)$, $x_3 = (3, 0)$, $x_4 = (2, 1)$, $x_5 = (5, 7)$, $x_6 = (3, 6)$.

| object | $x_0$ | $x_1$ | $x_2$ | $x_3$ | $x_4$ | $x_5$ | $x_6$ |
|---|---|---|---|---|---|---|---|
| row sum (L1) | 55 | 39 | 45 | 47 | 45 | 34 | 31 |
| gain $g$ with $M = [x_6]$ (L4) | 8 | 6 | 4 | 10 | 10 | 7 | 0 |

BUILD takes $x_6$, the most central point. Then $x_3$ and $x_4$ have the same gain 10, and the smaller index $x_3$ is added. The BUILD cost is $\mathrm{cost}(\{x_6, x_3\}) = 21$.

SWAP computes $T(m, h)$ for the 10 pairs:

| pass | medoids | cost | $T(m, h)$ for $m = $ first medoid | $T(m, h)$ for $m = x_3$ | action |
|---|---|---|---|---|---|
| 1 | $x_6, x_3$ | 21 | $h = x_0, x_1, x_2, x_4, x_5$: 12, 0, 6, 22, $-3$ | $h = x_0, x_1, x_2, x_4, x_5$: 2, 4, 6, 0, 3 | $x_5$ replaces $x_6$ |
| 2 | $x_5, x_3$ | 18 | $h = x_0, x_1, x_2, x_4, x_6$: 15, 3, 9, 25, 3 | $h = x_0, x_1, x_2, x_4, x_6$: 9, 15, 10, 0, 6 | stop |

The final medoids are $x_5$ and $x_3$ with cost 18. The clusters are $\{x_0, x_1, x_2, x_5, x_6\}$ and $\{x_3, x_4\}$. Among the 21 pairs of points, no pair has a cost below 18, so here PAM finds the optimum. The pair $(x_3, x_4)$ has $T = 0$ in both passes: a swap with no gain is not made.

## Correctness

BUILD keeps $\mathrm{near}[j]$ equal to the least dissimilarity from $j$ to the medoids, so $g(i)$ is the exact decrease of the cost when $i$ is added. In line L8, an object served by $m$ moves to its second nearest medoid or to $h$, and every other object keeps its medoid or moves to $h$; so $T(m, h)$ is the exact change of the cost. Each swap lowers the cost strictly, so no medoid set occurs twice and SWAP stops. When it stops, no single swap lowers the cost: the output is a single-swap local optimum. Arya et al. proved that in a metric such a local optimum costs at most $5\,\mathrm{OPT}$; the proof is on the correctness page.

## Complexity

- **BUILD.** Each of the $k - 1$ steps computes $g(i)$ for up to $n$ objects in $O(n)$ time each, so BUILD takes $O(n^2 k)$ time.
- **One SWAP pass.** There are $k(n - k)$ pairs and each costs $O(n)$, so a pass takes $O(k(n - k)n)$ time. Kaufman and Rousseeuw sum only over the $n - k$ non-medoids and count $O(k(n - k)^2)$.
- **Number of passes.** Each pass makes one swap. With integer dissimilarities each swap lowers the cost by at least 1, so there are at most $\mathrm{cost}(\text{BUILD}) - \mathrm{OPT}$ swaps. In general there is no polynomial bound on the number of passes, but in practice few passes are needed after BUILD.
- **Space.** The matrix $D$ takes $\Theta(n^2)$ memory; the algorithm needs $\Theta(n)$ more for $D_j$, $m_j$ and $E_j$.

## Properties

- **Medoids are objects.** A medoid is always one of the data objects, so the result is easy to show and to explain.
- **Any dissimilarity.** PAM reads only $D$. It needs no coordinates, and the triangle inequality matters only for the factor 5.
- **Robust to outliers.** The cost sums plain dissimilarities, not squares, so a far object moves the result less than in [k-means](/k-means/).
- **Deterministic.** With a fixed rule for ties, the output depends only on $D$ and $k$.
- **Local optimum.** No single swap improves the result. Swaps of $p$ medoids at a time give the factor $3 + 2/p$, but cost $O(n^p)$ more per pass.

## Variants and improvements

- **FastPAM1** (Schubert and Rousseeuw 2019) computes the gains of all $k$ swaps for one candidate $h$ in one scan of the objects. A pass then takes $O((n - k)n)$ time instead of $O(k(n - k)n)$, and the result is the same as that of PAM.
- **FastPAM2 and FasterPAM** do more than one swap per pass, or make a swap as soon as it lowers the cost. They are much faster, but they can stop at a different local optimum.
- **CLARA** (Kaufman and Rousseeuw 1990) runs PAM on some random samples and keeps the best medoids for the full data. It makes PAM usable for large $n$.
- **CLARANS** (Ng and Han 1994) tests random swaps and moves on at the first one that helps.
- **Alternating k-medoids** assigns the objects and then picks the medoid of each cluster, like [k-means](/k-means/). It is faster but often stops at worse local optima than PAM.
- **Greedy start only.** BUILD alone is a greedy algorithm for k-median. Many programs replace it with a random start or with [k-means++](/k-means-plus-plus/) seeding.

## When to use it

Use PAM when the data has a dissimilarity but no mean, when the centers must be real objects, or when outliers would move the means of [k-means](/k-means/). For $n$ up to some thousands, the full matrix fits in memory and PAM (or FastPAM1, for the same result) is a good choice. For larger data use CLARA, FasterPAM or a [streaming k-median](/streaming-k-median/) method. If a proven factor better than 5 is needed, use an approximation algorithm for the [k-median problem](/k-median-problem/).

## Pitfalls

- **Quadratic memory.** The matrix $D$ has $n^2$ entries; for $n = 10^5$ that is too large for most machines.
- **Not the optimum.** PAM finds a local optimum. The factor 5 holds only in a metric, and for a non-metric $D$ there is no bound.
- **Ties.** Different rules for ties in BUILD or SWAP can give different medoids. Fix the rule if the results must repeat.
- **The name k-medoids.** Some programs call the alternating method k-medoids. It is not PAM and its results are often worse.
- **Swaps with zero gain.** Make a swap only when $T(m, h) < 0$. A swap with $T = 0$ can make the search loop forever.

## Implementations

## History

Kaufman and Rousseeuw introduced the method in 1987 and described it in full, with the program PAM and the variant CLARA for large data, in their 1990 book. The cost is the old $p$-median objective of location theory, and swap heuristics of the same kind go back to Teitz and Bart in 1968. Ng and Han gave CLARANS in 1994. Arya et al. proved in 2001 (journal version 2004) that a single-swap local optimum is a 5-approximation in a metric. Schubert and Rousseeuw gave FastPAM in 2019 and FasterPAM in 2021.

## References
