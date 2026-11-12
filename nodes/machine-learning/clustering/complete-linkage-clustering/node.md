---
tag: 6884Z8
kind: algorithm
slug: complete-linkage-clustering
name: Complete-linkage clustering
aliases:
- farthest-neighbor clustering
area: machine-learning/clustering
level: core
summary: "Agglomerative clustering that merges the two clusters whose farthest pair of points is closest. Each merge height is the diameter of the new cluster."
solves: [hierarchical-clustering-problem]
model: real-ram
complexity:
  vars: {n: the number of points}
  time: {worst: "Θ(n^3)"}
  space: {extra: "Θ(n^2)"}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1948
  people: [Thorvald Sørensen, Daniel Defays]
  note: Sørensen (1948) grouped plant communities by this rule. Defays (1977) gave CLINK, a fast method in the style of SLINK that does not always give the same tree.
prereqs: [agglomerative-clustering]
see_also: [single-linkage-clustering, nearest-neighbor-chain, linkage-criterion, lance-williams-formula, k-center-problem, k-center-hardness, ward-method, dendrogram]
sources:
  - paper: "Thorvald Sørensen, A method of establishing groups of equal amplitude in plant sociology based on similarity of species content, Biologiske Skrifter 5(4) (1948), 1-34"
    locator: the grouping of samples so that each pair in a group has at least a given similarity
  - paper: doi:10.1093/comjnl/9.4.373
    title: "G. N. Lance and W. T. Williams, A general theory of classificatory sorting strategies 1. Hierarchical systems, The Computer Journal 9(4) (1967), 373-380"
    locator: the furthest neighbour strategy, its coefficients, and its space-dilating behavior
  - paper: doi:10.1093/comjnl/20.4.364
    title: "D. Defays, An efficient algorithm for a complete link method, The Computer Journal 20(4) (1977), 364-366"
    locator: the CLINK algorithm in O(n^2) time and O(n) memory, on the pointer representation
  - paper: doi:10.1093/comjnl/26.4.354
    title: "Fionn Murtagh, A survey of recent advances in hierarchical clustering algorithms, The Computer Journal 26(4) (1983), 354-359"
    locator: the reciprocal nearest neighbor methods, which give the exact complete link hierarchy in O(n^2) time
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schütze, Introduction to Information Retrieval
    locator: Chapter 17 (single-link and complete-link clustering, and the sensitivity of complete link to outliers)
  - book: isbn:9780130222787
    title: Anil K. Jain and Richard C. Dubes, Algorithms for Clustering Data
    locator: Chapter 3, Section 3.2 (the complete-link method and its graph form by cliques)
---

Complete-linkage clustering is [agglomerative clustering](/agglomerative-clustering/) with the complete [linkage](/linkage-criterion/): the dissimilarity of two clusters is the *largest* dissimilarity between a point of one and a point of the other. At each step, it merges the two clusters whose union has the smallest diameter, so each merge height is the diameter of the new cluster. The clusters are compact and of similar diameter, without the chaining of [single linkage](/single-linkage-clustering/), but they react strongly to outliers. The naive method takes $\Theta(n^3)$ time and $\Theta(n^2)$ memory. The [nearest-neighbor chain](/nearest-neighbor-chain/) gives the exact tree in $O(n^2)$ time. The fast CLINK algorithm of Defays (1977) does not compute exact complete linkage in general.

## In plain words

Two groups are as far apart as their two farthest members, one from each group. At each step, join the two groups that are closest in this sense.

So a join is allowed only when every item of one group is fairly close to every item of the other. The new group then has a small width: no two of its items are far apart. Groups stay round and tight, and a single long trail of items does not pull groups together.

One far item in a group, though, makes that group look far from all the others. So one odd item can change the tree a lot.

## The problem

The input is an $n \times n$ symmetric dissimilarity matrix $D$ with a zero diagonal. The output is the complete linkage hierarchy: the $n - 1$ merges of the greedy rule that always merges the two clusters $A$, $B$ with the smallest $\max_{a \in A, b \in B} D(a, b)$, with that value as the height. It solves the [hierarchical clustering problem](/hierarchical-clustering-problem/) for the complete linkage.

## The algorithm

The complete linkage row of the [Lance-Williams formula](/lance-williams-formula/) is a maximum: the farthest pair between $k$ and $i \cup j$ is the farther of the farthest pairs between $k$ and $i$ and between $k$ and $j$.

```pseudo id=main
COMPLETE-LINKAGE(D)                   ▷ D is an n × n dissimilarity matrix
L1  copy D, active ← {1, …, n}, size[i] ← 1, merges ← empty list
L2  while |active| > 1 do
L3      (i, j) ← the active pair with the smallest D[i, j], h ← D[i, j]
L4      for each k in active − {i, j} do
L5          D[i, k] ← D[k, i] ← max(D[i, k], D[j, k])
L6      append (i, j, h) to merges
L7      size[i] ← size[i] + size[j], remove j from active
L8  return merges
```

The cut into $k$ clusters undoes the last $k - 1$ merges.

## Example

Take the points $a, b, c, d, e, f$ at $0, 2, 3, 7, 13, 21$ on a line, with $D(x, y) = |x - y|$.

| step | merge | height | new values |
|---|---|---|---|
| 1 | $b$, $c$ | 1 | $D(a, bc) = 3$, $D(d, bc) = 5$, $D(e, bc) = 11$, $D(f, bc) = 19$ |
| 2 | $a$, $bc$ | 3 | $D(d, abc) = 7$, $D(e, abc) = 13$, $D(f, abc) = 21$ |
| 3 | $d$, $e$ | 6 | $D(abc, de) = 13$, $D(f, de) = 14$ |
| 4 | $abc$, $de$ | 13 | $D(f, abcde) = 21$ |
| 5 | $f$, $abcde$ | 21 | |

At step 3, the pair $d, e$ at 6 wins over $d, abc$ at 7: under single linkage $d$ would join $\{a, b, c\}$ at distance 4. Each height is the diameter of the new cluster: $\{a, b, c\}$ spans $0$ to $3$, and $\{a, \ldots, e\}$ spans $0$ to $13$. The cut into three clusters is $\{a, b, c\}$, $\{d, e\}$, $\{f\}$, with diameters 3, 6 and 0, against $\{a, b, c, d\}$, $\{e\}$, $\{f\}$ for single linkage.

**Not an optimal diameter clustering.** On the points $0, 1, 6, 9, 13$ with $k = 2$, complete linkage merges $\{0, 1\}$ at 1, $\{6, 9\}$ at 3 and $\{6, 9, 13\}$ at 7. Its two clusters $\{0, 1\}$, $\{6, 9, 13\}$ have the largest diameter 7. The partition $\{0, 1, 6\}$, $\{9, 13\}$ has the largest diameter 6. The greedy merge of $\{6, 9\}$ at the first chance is the mistake.

## Correctness

The invariant of the loop of line L2 is that $D[i, k]$ is the largest dissimilarity between the clusters in the active slots $i$ and $k$. Line L5 keeps it, because the largest value over the pairs of $C_k \times (C_i \cup C_j)$ is the larger of the largest values over $C_k \times C_i$ and over $C_k \times C_j$. So line L3 makes the greedy choice. The heights increase: when $i$ and $j$ are the closest pair, each new value $\max(D[i, k], D[j, k])$ is at least $D[i, j]$. From this, each height is the diameter of the new cluster. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Time.** The naive scan of line L3 takes $O(n^2)$ time in each of the $n - 1$ rounds, so the time is $\Theta(n^3)$. A heap of pairs gives $O(n^2 \log n)$, and the [nearest-neighbor chain](/nearest-neighbor-chain/) gives $O(n^2)$, both with the same tree when the dissimilarities are distinct.
- **Memory.** $\Theta(n^2)$ for the matrix. No exact method with $O(n)$ memory and $O(n^2)$ time is known in general, unlike single linkage, which has [SLINK](/slink/).
- **Lower bound.** For a general matrix, $\Omega(n^2)$ reads are needed.

## Properties

- **Heights are diameters.** The height of each merge is the diameter of the merged cluster, so a cut at height $h$ gives clusters of diameter at most $h$.
- **Monotone.** The linkage is reducible, so there are no inversions.
- **Space-dilating.** A growing cluster moves away from the other points, which gives compact clusters of similar size.
- **Not optimal for any $k$.** The example above shows that the cut at $k$ need not minimize the largest diameter. That problem is NP-hard, and a factor below 2 is NP-hard to reach in a general metric (see the [k-center hardness](/k-center-hardness/) page).
- **Order of ties matters.** With equal dissimilarities, the order in which ties break can change the tree, not only its drawing.
- **Invariant under increasing maps.** Only the order of the dissimilarities matters for the shape of the tree.

## Variants and improvements

- **[Nearest-neighbor chain](/nearest-neighbor-chain/).** Exact complete linkage in $O(n^2)$ time with $\Theta(n^2)$ memory.
- **CLINK.** Defays (1977) adapted the pointer representation of [SLINK](/slink/) to a complete link rule. It takes $O(n^2)$ time and $O(n)$ memory, but its tree depends on the order of the points, and in general it is not the tree of the greedy complete linkage rule. It gives one of the hierarchies that are valid under a weaker definition, so do not use it as a fast exact method.
- **Graph form.** For a threshold $h$, the complete linkage clusters are cliques of the graph of pairs with $D \le h$, but the method does not find a minimum cover by cliques, which is NP-hard.
- **Average linkage.** The [UPGMA](/upgma/) rule is less sensitive to outliers and is often a better default.

## When to use it

Use complete linkage when the clusters should be compact, with a bound on the distance between any two members, for example groups of documents that must all be similar to each other. Use it when the data has little noise. Prefer average or [Ward](/ward-method/) linkage when outliers are present, and single linkage when clusters have long shapes.

## Pitfalls

- **CLINK is not exact.** Libraries that call CLINK fast complete linkage give a different tree from the exact method on some inputs. Use the nearest-neighbor chain or the heap version for exact results.
- **Outliers.** One far point in a cluster sets the distance of the whole cluster to the others, so a single outlier can change many merges.
- **Ties.** With integer or rounded dissimilarities, ties are common, and the tree depends on the rule for ties.
- **It does not solve the diameter problem.** A cut of the tree is a heuristic for the minimum largest diameter, not an optimum.

## Implementations

## History

Sørensen (1948) used the rule to group samples in plant ecology, so that all pairs in a group share a level of similarity. Lance and Williams (1967) put it in their family as the furthest neighbour strategy and called it space-dilating. Defays (1977) gave CLINK in the style of [SLINK](/slink/), which is fast but not exact. Murtagh (1983) and later Müllner (2011) described exact $O(n^2)$ algorithms by reciprocal nearest neighbors.

## References
