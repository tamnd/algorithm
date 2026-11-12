---
tag: 5P8XRG
kind: algorithm
slug: nearest-neighbor-chain
name: Nearest-neighbor chain algorithm
aliases:
- NN-chain algorithm
- reciprocal nearest neighbor chain
area: machine-learning/clustering
level: advanced
summary: "Agglomerative clustering that follows nearest neighbors until two clusters are mutual nearest neighbors, then merges them: O(n^2) for reducible linkages."
solves: [hierarchical-clustering-problem]
model: real-ram
complexity:
  vars: {n: the number of points}
  time: {worst: "Θ(n^2)"}
  space: {extra: "Θ(n^2)"}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1982
  people: [Jean-Paul Benzécri, Fionn Murtagh]
  note: Benzécri (1982) built hierarchies by chains of reciprocal nearest neighbors. Murtagh (1983, 1985) gave the O(n^2) analysis and the condition of reducibility.
prereqs: [agglomerative-clustering, linkage-criterion]
see_also: [lance-williams-formula, ward-method, complete-linkage-clustering, single-linkage-clustering, slink, upgma, wpgma, dendrogram]
sources:
  - paper: "Jean-Paul Benzécri, Construction d'une classification ascendante hiérarchique par la recherche en chaîne des voisins réciproques, Les Cahiers de l'Analyse des Données 7(2) (1982), 209-218"
    locator: the construction of the hierarchy by chains of reciprocal nearest neighbors
  - paper: doi:10.1093/comjnl/26.4.354
    title: "Fionn Murtagh, A survey of recent advances in hierarchical clustering algorithms, The Computer Journal 26(4) (1983), 354-359"
    locator: the reducibility property, reciprocal nearest neighbors, and the nearest-neighbor chain in O(n^2) time
  - paper: "Fionn Murtagh, Multidimensional Clustering Algorithms, COMPSTAT Lectures 4, Physica-Verlag, Vienna (1985)"
    locator: the nearest-neighbor chain algorithm and its use for the Lance-Williams linkages
  - url: https://arxiv.org/abs/1109.2378
    title: "Daniel Müllner, Modern hierarchical, agglomerative clustering algorithms, arXiv:1109.2378 (2011)"
    locator: the nearest-neighbor chain algorithm, its proof of correctness, and the counterexample for centroid and median linkage
---

The nearest-neighbor chain algorithm computes the hierarchy of [agglomerative clustering](/agglomerative-clustering/) in $O(n^2)$ time for each *reducible* [linkage](/linkage-criterion/): single, complete, average (UPGMA), weighted (WPGMA) and Ward. It keeps a stack of clusters, the chain, in which each cluster is the nearest neighbor of the cluster below it. It extends the chain by nearest neighbors until the top two clusters are each other's nearest neighbor, merges those two, and goes on from the rest of the chain. The merges come in a different order from the greedy method, but with no ties they are the same merges at the same heights, so a sort by height gives the same [dendrogram](/dendrogram/). For centroid and median linkage, which are not reducible, the result can differ.

## In plain words

Start at any group and walk to its closest group. From there, walk to the closest group of that one, and so on. Each step goes to a closer pair, so the walk cannot go on for ever. It stops at two groups that are each other's closest group. Join these two.

The groups that you visited before the stop still point to their closest groups, and for the usual ways to measure the distance between groups, a join far away does not change who is closest. So you keep the path and go on walking from its end. Each group joins the path only a few times, so the whole work is about the size of the table of distances.

## The problem

The input is an $n \times n$ symmetric dissimilarity matrix $D$ and a reducible linkage $\mathcal{L}$, given by its [Lance-Williams](/lance-williams-formula/) update. A linkage is *reducible* if for disjoint clusters $I$, $J$, $K$,

$$\mathcal{L}(I, J) \le \min(\mathcal{L}(I, K), \mathcal{L}(J, K)) \implies \mathcal{L}(I \cup J, K) \ge \min(\mathcal{L}(I, K), \mathcal{L}(J, K)).$$

In words, the merge of two clusters that are closer to each other than to $K$ does not bring the union closer to $K$ than both parts. The output is the hierarchy of the [hierarchical clustering problem](/hierarchical-clustering-problem/) for $\mathcal{L}$, as the $n - 1$ merges in order of height. Two clusters $A$, $B$ are *reciprocal nearest neighbors* (RNN) if each is the nearest neighbor of the other.

## The algorithm

```pseudo id=main
NN-CHAIN(D, L)                        ▷ L is a reducible linkage
L1  active ← {1, …, n}, size[i] ← 1, found ← empty list
L2  chain ← empty stack
L3  while |active| > 1 do
L4      if chain is empty then push any active cluster
L5      a ← top of chain, prev ← the cluster below a (if any)
L6      b ← the active cluster ≠ a with the least D[a, b], with prev on a tie
L7      if b = prev then                ▷ a and b are reciprocal nearest neighbors
L8          pop a and b
L9          append (a, b, D[a, b]) to found
L10         for each k in active − {a, b}: D[a, k] ← the Lance-Williams value for a ∪ b
L11         size[a] ← size[a] + size[b], remove b from active
L12     else push b
L13 return found, sorted by height with a stable sort
```

The tie rule of line L6 keeps the chain from running in a circle when two values are equal. Line L10 is the same update as in the naive algorithm. Line L13 sorts the merges by height, because the chain finds them in another order.

## Example

Take the points $a, b, c, d, e, f$ at $0, 2, 3, 7, 13, 21$ on a line, with complete linkage. The chain starts at $a$.

| step | chain | nearest neighbor of the top | action |
|---|---|---|---|
| 1 | $a$ | $b$ at 2 | push $b$ |
| 2 | $a, b$ | $c$ at 1 | push $c$ |
| 3 | $a, b, c$ | $b$ at 1 | merge $b, c$ at 1 |
| 4 | $a$ | $bc$ at 3 | push $bc$ |
| 5 | $a, bc$ | $a$ at 3 | merge $a, bc$ at 3 |
| 6 | $abc$ | $d$ at 7 | push $d$ |
| 7 | $abc, d$ | $e$ at 6 | push $e$ |
| 8 | $abc, d, e$ | $d$ at 6 | merge $d, e$ at 6 |
| 9 | $abc$ | $de$ at 13 | push $de$ |
| 10 | $abc, de$ | $abc$ at 13 | merge $abc, de$ at 13 |
| 11 | $abcde$ | $f$ at 21 | push $f$, then merge at 21 |

At step 7 the chain goes from $d$ to $e$ at 6, which is less than the 7 from $abc$ to $d$, so the values along the chain decrease. Here the merges come in the order of height. On the points $0, 3, 10, 11$ with a chain that starts at $0$, the chain merges $\{0, 3\}$ at 3 first, and only then $\{10, 11\}$ at 1. Line L13 puts them in the right order.

**Centroid linkage is not reducible.** For the points $p_0 = (0, 3)$, $p_1 = (8, 6)$, $p_2 = (1, 11)$, $p_3 = (8, 1)$ with squared Euclidean distances, the greedy centroid method merges $\{p_1, p_3\}$ at 25, then adds $p_0$ at $257/4$ and $p_2$ at $698/9$. The chain from $p_0$ finds that $p_0$ and $p_2$ are reciprocal nearest neighbors at 65 and merges them, then $\{p_1, p_3\}$ at 25, then all at $137/2$. That is another hierarchy.

## Correctness

Three facts give the result. First, the chain stays valid after a merge: each cluster in the chain keeps the next one as its nearest neighbor, because by reducibility the new cluster is not closer to it than the old nearest neighbor. Second, the values along the chain strictly decrease, so no cluster appears twice, and the chain stops at an RNN pair. Third, with no ties, merging any RNN pair at any time gives the same hierarchy as the greedy method. This is shown by induction on the number of clusters: if the greedy method would first merge another pair $I$, $J$, then $I$, $J$ stays an RNN pair after the merge of $A$, $B$, and $A$, $B$ stays an RNN pair after the merge of $I$, $J$, so the two orders lead to the same state. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Time.** Each loop round either pushes a cluster or merges two. There are $n - 1$ merges, each pops two clusters, and at most one cluster is left on the chain, so there are at most $2n - 1$ pushes and $3n - 2$ rounds. Each round costs $O(n)$ for the scan of line L6 and the update of line L10. The total is $O(n^2)$, which is optimal, since $\Theta(n^2)$ reads of $D$ are needed in general.
- **Memory.** $\Theta(n^2)$ for the matrix, and $O(n)$ for the chain.
- **Ward and centroids.** For Ward's method on points of $\mathbb{R}^d$, the values can be computed from the centroids on demand, which gives $O(n^2 d)$ time and $O(n d)$ memory.

## Properties

- **Exact for reducible linkages.** With no ties, the output is the greedy hierarchy for single, complete, average, weighted and Ward linkage.
- **Monotone.** For a reducible linkage the heights never decrease, after the sort of line L13.
- **Order of discovery.** The merges are found in a different order from the heights. Any cut of the tree needs the sorted list.
- **Ties.** With ties, the output is still a monotone hierarchy, and each merge joins two clusters that are mutual nearest neighbors at that time. It can differ from a greedy run with another tie rule.
- **Not for centroid or median linkage.** These are not reducible. The algorithm still ends, but it can give another hierarchy.

## Variants and improvements

- **Several RNN pairs at a time.** One scan can find all RNN pairs and merge them in one round. This suits parallel machines.
- **Ward from centroids.** Keep only the centroids and sizes and compute the Ward values on demand, which gives $O(n d)$ memory.
- **Single linkage.** [SLINK](/slink/) or Prim's algorithm on the dense graph gives single linkage in $O(n^2)$ time with $O(n)$ memory, without the matrix.
- **Generic algorithm of Müllner.** For centroid and median linkage, a priority queue of nearest neighbors with lazy updates gives the exact greedy result, in $O(n^3)$ time in the worst case and often much less in practice.

## When to use it

Use the nearest-neighbor chain for complete, average, weighted or Ward linkage when the matrix fits in memory. It is the fastest exact method for these linkages, and it is simple. For single linkage, prefer an algorithm with $O(n)$ memory. For centroid or median linkage, use the generic or the naive algorithm.

## Pitfalls

- **Forgetting the sort.** The merges come out in the order of discovery. A dendrogram built from that order without the sort of line L13 is wrong.
- **The tie rule.** Without the preference for $\textit{prev}$ at line L6, two equal values can make the chain go back and forth for ever.
- **Non-reducible linkages.** Centroid and median linkage give a different tree, as the example shows. Some programs do not warn about this.
- **Ward on plain distances.** As in the naive method, the Ward update needs squared Euclidean distances.

## Implementations

## History

Benzécri (1982) built hierarchies by chains of reciprocal nearest neighbors. Murtagh (1983) gave the reducibility property as the condition under which the method gives the greedy hierarchy, and showed the $O(n^2)$ time. Murtagh (1985) described it in more detail. Müllner (2011) gave a full proof of correctness and showed by examples that centroid and median linkage are not safe.

## References
