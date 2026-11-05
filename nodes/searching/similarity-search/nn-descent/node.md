---
tag: 264YR6
kind: algorithm
slug: nn-descent
name: NN-Descent
aliases:
- nearest neighbor descent
area: searching/similarity-search
level: research
summary: Approximately builds a kNN graph by repeatedly refining neighbors of neighbors.
model: real-ram
complexity:
  vars: {n: the number of points, k: the list length, s: the sample size ⌈ρk⌉, D: the cost of one distance evaluation, R: the number of rounds}
  time: {round with sampling: O(n s (k + s) (D + k)), round without sampling: O(n k (n + k) (D + k)), total with sampling: O(R n s (k + s) (D + k))}
  space: {lists: Θ(n k)}
properties: {deterministic: false, online: false, exact: false}
history:
  year: 2011
  people: [Wei Dong, Moses Charikar, Kai Li]
  note: Dong, Charikar and Li proposed NN-Descent for generic similarity measures at WWW 2011.
prereqs: [k-nearest-neighbor-graph, k-nearest-neighbor-search]
see_also: [k-nearest-neighbor-graph, k-nearest-neighbor-graph-construction, navigable-small-world, hnsw, approximate-nearest-neighbor, metric-space, local-search, triangle-inequality]
sources:
  - paper: doi:10.1145/1963405.1963487
    title: Wei Dong, Moses Charikar and Kai Li, Efficient k-nearest neighbor graph construction for generic similarity measures, Proceedings of the 20th International World Wide Web Conference (WWW 2011)
    locator: pages 577 to 586 (the principle that a neighbor of a neighbor is likely a neighbor, the basic algorithm, the local join, the incremental search with new and old flags, sampling at rate ρ, the termination threshold δ, and the experiments on the empirical cost)
---

NN-Descent builds an approximate [k-nearest-neighbor graph](/k-nearest-neighbor-graph/) of $n$ points: for every point $v$, a list $B[v]$ of $k$ other points that should be its $k$ nearest. It starts from random lists and improves them in rounds. In each round, for every point $v$, it takes the points close to $v$ in the current graph, both those in $B[v]$ and those whose lists contain $v$, and compares them in pairs; when two of them are closer to each other than the worst entry of one of their lists, the list takes the other point. It stops when a round changes almost nothing. It only needs a distance function, not coordinates or the [triangle inequality](/triangle-inequality/). Dong, Charikar and Li proposed it in 2011, and reported that on their data it reached high recall with a number of distance evaluations far below the $n(n-1)/2$ of brute force. It has no worst-case guarantee of accuracy; what can be proved is that it terminates and that its result is locally optimal.

## In plain words

You want to know, for every person in a big crowd, their few closest friends, but measuring how close two people are takes time, so you cannot compare everyone with everyone.

Start by giving each person a few friends at random. Then repeat. Each person introduces their friends to each other, and also to the people who list them as a friend. Whenever two people meet who are closer than someone on one of their lists, that list drops its worst friend and takes the new one. A friend of a friend is often a good friend, so the lists get better fast.

To save work, only friendships that are new since the last round are introduced again. When a round changes almost no list, stop.

## The problem

Given $n$ objects with a dissimilarity $\sigma(u, v) = \sigma(v, u) \ge 0$ and a number $k$ with $1 \le k < n$, compute for every $v$ the $k$ objects $u \ne v$ of smallest $\sigma(v, u)$. Ties are broken by index, so we compare pairs $(\sigma(v, u), u)$ and every list has one exact answer. Brute force takes $n(n-1)/2$ evaluations of $\sigma$; the goal is far fewer, at the price of some wrong entries.

## The algorithm

Each entry of $B[v]$ is a point $u$ with its distance $\sigma(v, u)$ and a flag, *new* or *old*. An entry is new until it has taken part in one local join. The *reverse* lists are $R[v] = \{u : v \in B[u]\}$. Let $s = \lceil \rho k \rceil$ for a sampling rate $0 < \rho \le 1$; with no sampling, all entries are used.

```pseudo id=main
NN-DESCENT(P, k, ρ, δ)
L1  for each v do B[v] ← k random points u ≠ v with σ(v, u), all flagged new
L2  repeat
L3      for each v do old[v] ← the points of B[v] flagged old
L4      for each v do new[v] ← s points of B[v] flagged new, sampled; flag them old
L5      for each v do old'[v] ← {u : v ∈ old[u]}, new'[v] ← {u : v ∈ new[u]}
L6      c ← 0; for each v do
L7          old[v] ← old[v] ∪ sample(old'[v], s); new[v] ← new[v] ∪ sample(new'[v], s)
L8          for each pair u1 ≠ u2 with u1 ∈ new[v] and u2 ∈ new[v] ∪ old[v] do      ▷ the local join
L9              l ← σ(u1, u2)
L10             c ← c + UPDATE(B[u1], u2, l) + UPDATE(B[u2], u1, l)
L11 until c ≤ δ n k
L12 return B

UPDATE(B, u, l)       ▷ 1 if u entered B, else 0
    if u ∈ B or (l, u) ≥ the largest pair of B then return 0
    replace the largest pair of B by (l, u), flagged new; return 1
```

Line L1 starts from a random graph. Lines L3 and L4 split each list: the old entries were already joined in an earlier round, and the new ones are joined now; line L4 marks them old so that they are not joined again. Line L5 builds the reverse lists, and line L7 adds a sample of them, so that $v$ also introduces the points that point to it. Lines L8 to L10 are the *local join* around $v$: every pair with at least one new member is compared, once, and each of the two lists is offered the other point. A pair of two old members was already compared in an earlier round, so it is skipped. Line L11 stops when a round makes at most $\delta n k$ changes; $\delta = 0$ means "until nothing changes".

The local join looks at $v$ only as a meeting place: it never computes $\sigma(v, \cdot)$ again. It updates $B[v]$ through the joins around the neighbors of $v$, which is how a neighbor of a neighbor of $v$ reaches $B[v]$.

## Example

In the plane with the Euclidean distance, take $k = 2$, no sampling and $\delta = 0$, and the eight points $a = (0, 0)$, $b = (1, 0)$, $c = (2, 1)$, $d = (6, 0)$, $e = (7, 1)$, $f = (6, 2)$, $g = (1, 5)$, $h = (2, 6)$: three groups. The table shows the random start of line L1 and the lists after each round, as (point, distance) pairs.

| point | start $B$ | after round 1 | after round 2 | exact |
|---|---|---|---|---|
| a | d 6, g 5.0990 | g 5.0990, d 6 | b 1, c 2.2361 | b 1, c 2.2361 |
| b | e 6.0828, h 6.0828 | g 5, f 5.3852 | a 1, c 1.4142 | a 1, c 1.4142 |
| c | f 4.1231, a 2.2361 | a 2.2361, d 4.1231 | b 1.4142, a 2.2361 | b 1.4142, a 2.2361 |
| d | a 6, g 7.0711 | e 1.4142, c 4.1231 | e 1.4142, f 2 | e 1.4142, f 2 |
| e | b 6.0828, h 7.0711 | d 1.4142, f 1.4142 | d 1.4142, f 1.4142 | d 1.4142, f 1.4142 |
| f | c 4.1231, d 2 | e 1.4142, d 2 | e 1.4142, d 2 | e 1.4142, d 2 |
| g | d 7.0711, e 7.2111 | h 1.4142, c 4.1231 | h 1.4142, c 4.1231 | h 1.4142, c 4.1231 |
| h | f 5.6569, b 6.0828 | g 1.4142, c 5 | g 1.4142, c 5 | g 1.4142, c 5 |

The start costs 16 evaluations. Round 1 makes 14 updates with 20 evaluations. For example, $B[g] = \{d, e\}$, so $d$ and $e$ meet in the local join around $g$, and $d$ gets its true nearest neighbor $e$ although neither list held the other. Round 2 makes 7 updates with 23 evaluations, and round 3 makes none with 9, so the algorithm stops after 68 evaluations with the exact lists. Brute force needs only $\binom{8}{2} = 28$ here: the savings of NN-Descent appear only when $n$ is much larger than $k^2$.

## Correctness

NN-Descent is a heuristic: it does not always return the exact lists. The following holds for every input, and is proved in [the correctness proof](proofs/correctness.md). Write $\bar N[v] = B[v] \cup R[v]$.

1. **Valid lists.** At all times each $B[v]$ holds $k$ distinct points other than $v$, each with its correct distance, and the largest pair $(\sigma(v, u), u)$ of $B[v]$ never increases.
2. **Termination.** Every update lowers the sum, over all lists, of the ranks of their entries, by at least 1. So there are at most $n k (n - 1 - k)$ updates in total, and at most $n k (n - 1 - k) + 1$ rounds with $\delta = 0$, and at most $(n - 1 - k)/\delta + 1$ rounds with $\delta > 0$.
3. **Local optimality.** With no sampling and $\delta = 0$, at the end, for every $v$ and every two distinct $u_1, u_2 \in \bar N[v]$, either $u_2 \in B[u_1]$ or $(\sigma(u_1, u_2), u_2)$ is larger than every pair of $B[u_1]$. In particular, no point $w$ that shares a point $u$ with $v$, in the sense $v, w \in \bar N[u]$, would improve $B[v]$.

Local optimality does not give the exact graph. An update links two points that have a common neighbor in the undirected graph of all lists, so the connected components of that graph never merge. If the start splits the points into two parts with no list between them, a true neighbor in the other part is never found.

## Complexity

In the real RAM, with $D$ the cost of one evaluation of $\sigma$ and UPDATE done by a scan of the $k$ entries:

- **One round with sampling.** For each $v$, $|new[v]| \le 2s$ and $|old[v]| \le k + s$, so the local join makes at most $2s(k + 3s)$ evaluations, and each costs $O(D + k)$ with its two updates. A round costs $O(n s (k + s)(D + k))$, plus $O(nk)$ to build the reverse lists.
- **One round without sampling.** The reverse lists have total size $nk$ but one of them can have size $n - 1$; then $\sum_v |\bar N[v]|^2 \le 2nk^2 + 2nk(n - 1)$, so a round makes $O(nk(n + k))$ evaluations. This is why the sampling of reverse lists matters on skewed data.
- **The number of rounds.** The bound of the correctness section is only a worst case. Dong, Charikar and Li observed few rounds in practice and an empirical total of about $n^{1.14}$ evaluations on their data sets; this is a measurement, not a theorem.
- **Space.** $\Theta(nk)$ for the lists and the reverse lists.

## Properties

- **Randomized.** The start and the samples are random; the result depends on the seed.
- **Generic.** Only $\sigma$ is evaluated, and it need not be a metric.
- **Not exact.** The result is locally optimal (item 3 above), not the exact graph, and there is no bound on its recall that holds for all inputs.
- **Anytime.** After every round the lists are valid, and better than before; the loop can be stopped early.
- **Parallel.** The local joins of one round are independent except for the updates, which can be done with locks per list.

## Variants and improvements

- **Basic NN-Descent.** Without the local join, each $v$ computes $\sigma(v, w)$ for every $w$ in $\bar N[u]$ for every $u \in \bar N[v]$. The local join gives the same comparisons with about half the evaluations, since each pair is compared once around a common neighbor.
- **Incremental search.** The new and old flags of lines L3 and L4 avoid comparing the same pair twice in later rounds.
- **Sampling.** Dong, Charikar and Li sample both the forward and the reverse lists at rate $\rho$; smaller $\rho$ costs less per round and more rounds.
- **Better starts.** A start from [random projection trees](/rp-tree/) or another cheap partition puts close points together at once and cuts the number of rounds; PyNNDescent does this.
- **Graph indexes.** The approximate graph is a starting point for search graphs such as the [navigable small world](/navigable-small-world/) graph and [HNSW](/hnsw/), which add long links and prune short ones.

## When to use it

Use NN-Descent when the whole kNN graph is wanted, $n$ is large, $k$ is small, and some wrong entries are acceptable: for clustering, manifold learning and visualization (UMAP uses it), for recommendation, or to build a graph index. It suits distances that no tree handles well, such as the cosine or Jaccard distance in high dimension. When the exact graph is needed and the dimension is low, a [k-d tree](/kd-tree/) query per point is better.

## Pitfalls

- **Large $k$ or tiny $n$.** A round costs about $nk^2$ evaluations, so with $k^2$ close to $n$ it is no better than brute force, as in the example.
- **Disconnected start.** Components never merge, so a start built by a partition with no edges across parts can miss true neighbors for good. Random starts make this unlikely.
- **Hubs.** Without sampling of the reverse lists, a point that appears in many lists makes a quadratic local join.
- **Duplicates and ties.** Many points at distance 0 can fill a list with copies; break ties by index, as here, so that UPDATE stays well defined.
- **Reading recall from the stop rule.** A round with few updates means the lists are locally optimal, not that they are correct. Measure recall on a sample against brute force.

## Implementations

## History

Wei Dong, Moses Charikar and Kai Li introduced NN-Descent at WWW 2011, for kNN graphs under generic similarity measures, with the local join, the incremental flags and sampling. Leland McInnes's PyNNDescent library made it a common tool, and the UMAP method of dimension reduction builds its graph with it.

## References
