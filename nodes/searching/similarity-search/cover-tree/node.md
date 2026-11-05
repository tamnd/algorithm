---
tag: GE45W4
kind: data-structure
slug: cover-tree
name: Cover tree
aliases:
- Beygelzimer cover tree
- cover tree
area: searching/similarity-search
level: research
summary: Leveled metric tree with provable query bounds depending on the expansion constant of the data.
implements: [similarity-index]
model: real-ram
complexity:
  vars: {n: the number of points, c: the expansion constant of the points together with the query or inserted point, E: the time of one distance evaluation}
  time: {build: O(c^6 n log n E), insert: O(c^6 log n E), nearest: O(c^12 log n E)}
  space: {total: O(n)}
history:
  year: 2006
  people: [Alina Beygelzimer, Sham Kakade, John Langford]
  note: Beygelzimer, Kakade and Langford introduced the cover tree at ICML 2006 as a simpler structure with linear space after the navigating nets of Krauthgamer and Lee and the structure of Karger and Ruhl.
prereqs: [intrinsic-dimensionality, metric-space, k-nearest-neighbor-search]
see_also: [ball-tree, vantage-point-tree, gnat, m-tree, bk-tree, metric-space-indexing, k-nearest-neighbor-graph-construction, triangle-inequality]
sources:
  - paper: doi:10.1145/1143844.1143857
    title: Alina Beygelzimer, Sham Kakade and John Langford, Cover trees for nearest neighbor, Proceedings of the 23rd International Conference on Machine Learning (ICML), 2006
    locator: pages 97 to 104 (the invariants of nesting, covering and separation; Algorithm 1 for nearest neighbor search and Algorithm 2 for insertion; the bounds O(n) space, O(c^6 log n) insertion and O(c^12 log n) query in terms of the expansion constant c)
  - paper: doi:10.1145/509907.510013
    title: David R. Karger and Matthias Ruhl, Finding nearest neighbors in growth-restricted metrics, Proceedings of the 34th ACM Symposium on Theory of Computing (STOC), 2002
    locator: pages 741 to 750 (the expansion constant and the first nearest neighbor structure analyzed in terms of it)
  - paper: doi:10.1145/502807.502808
    title: Edgar Chávez, Gonzalo Navarro, Ricardo Baeza-Yates and José Luis Marroquín, Searching in metric spaces, ACM Computing Surveys 33(3), 2001
    locator: pages 273 to 321 (the general framework of metric indexes that prune by the triangle inequality)
---

A cover tree is a tree over points of a [metric space](/metric-space/) in which every level $i$ holds a set $C_i$ of points that are more than $2^i$ apart and that cover the next level down within $2^i$. The sets are nested, $C_i \subseteq C_{i-1}$, so a point that appears at some level appears at every level below it. Beygelzimer, Kakade and Langford showed that it uses $O(n)$ space, and that nearest neighbor search and insertion take $O(c^{12} \log n)$ and $O(c^6 \log n)$ distance evaluations, where $c$ is the expansion constant of the data, one form of [intrinsic dimensionality](/intrinsic-dimensionality/). The bounds do not depend on the ambient dimension, and for data with small $c$ they match the $O(\log n)$ of a balanced search tree.

## In plain words

Think of a map with zoom levels. At the most zoomed-out level there is a single city. Zoom in one step and more cities appear, each near a city that was already shown, and no two shown cities are too close together. Each zoom step halves both distances: "near" and "too close".

To find the city nearest to a place, start at the top and keep only the cities that could still lead to the nearest one. A city whose distance is much larger than the best one found cannot have a nearby city below it, because all cities below it are close to it. As you zoom in, the list of possible cities stays short when the data are not too spread out in many directions.

## The abstract type

A dynamic similarity index for a finite set $S$ in a metric space $(M, \delta)$, with:

- **insert**$(p)$: add $p$ to $S$.
- **nearest**$(q)$: return $p \in S$ with the least $\delta(q, p)$, exactly.

The usual extensions are $k$ nearest neighbors, range search and deletion; see Variants.

## Representation

Conceptually the tree has a level $C_i$ for every integer $i$, from a top level $C_{\text{top}} = \{\text{root}\}$ down to $C_{-\infty} = S$. Each point $p \in C_{i-1}$ has a parent in $C_i$. Three invariants hold for every $i$:

1. **Nesting:** $C_i \subseteq C_{i-1}$. A point $p \in C_i$ is also in $C_{i-1}$, and its parent there is itself.
2. **Covering:** every $p \in C_{i-1}$ has a parent $q \in C_i$ with $\delta(p, q) \le 2^i$.
3. **Separation:** any two distinct $p, q \in C_i$ satisfy $\delta(p, q) > 2^i$.

The **implicit tree** has a node $(p, i)$ for every $p \in C_i$, which is infinite. The **explicit tree** stores only the nodes where a point first appears below its parent: for each point $p$ and level $i$, the list of points whose highest level is $i - 1$ and whose parent at level $i$ is $p$. Every point other than the root is in exactly one such list, so the explicit tree has $n - 1$ entries and uses $O(n)$ space. All other nodes are "self children" and need no storage.

By the triangle inequality and covering, every descendant $r$ of a node $(p, i)$ satisfies

$$\delta(p, r) \le \sum_{j \le i} 2^j = 2^{i+1}.$$

This is the bound that drives both pruning and correctness.

## Operations

Write $\text{Children}(Q, i)$ for the set of children at level $i - 1$ of the nodes $Q \subseteq C_i$, including the nodes themselves, and $\delta(p, Q) = \min_{q \in Q} \delta(p, q)$. Insertion is a recursive descent that returns "parent found" or "no parent found". The first call is INSERT$(p, \{\text{root}\}, \text{top})$, after raising top until $\delta(p, \text{root}) \le 2^{\text{top}}$.

```pseudo id=main
INSERT(p, Q_i, i)
L1  Q ← Children(Q_i, i)
L2  if δ(p, Q) > 2^i then return "no parent found"
L3  Q_{i−1} ← {q ∈ Q : δ(p, q) ≤ 2^i}
L4  if INSERT(p, Q_{i−1}, i − 1) = "parent found" then return "parent found"
L5  if δ(p, Q_i) > 2^i then return "no parent found"
L6  pick q ∈ Q_i with δ(p, q) ≤ 2^i; make p a child of q at level i − 1; return "parent found"
```

Line L2 stops the descent when no point at level $i - 1$ is near enough to be a parent. A failure at level $i - 1$ means $p$ is far from every point of the lower levels, so line L6 makes $p$ a new point at level $i - 1$, under a parent at level $i$.

Search keeps, at each level, the set of nodes that can still have the nearest point among their descendants:

```pseudo id=nearest
NEAREST(p)
L7  Q_top ← {root}
L8  for i ← top down to bottom + 1, where bottom is the lowest level of any explicit node
L9    Q ← Children(Q_i, i); Q_{i−1} ← {q ∈ Q : δ(p, q) ≤ δ(p, Q) + 2^i}
L10 return the point of Q_bottom nearest to p
```

Below the lowest explicit level, every node is a self child, so the sets stop changing except by pruning, and the loop can stop.

## Example

Insert the points $0, 8, 4, 2, 6, 1, 7, 3$ on the real line, in this order, with $\delta(x, y) = |x - y|$. The root is 0. To cover 8 the top level rises to 3, since $8 \le 2^3$. The result:

| level $i$ | $C_i$ | new points and parents |
|---|---|---|
| 3 | 0 | root |
| 2 | 0, 8 | 8 under 0 ($\delta = 8 \le 2^3$) |
| 1 | 0, 4, 8 | 4 under 0 ($4 \le 2^2$) |
| 0 | 0, 2, 4, 6, 8 | 2 under 0, 6 under 8 ($2 \le 2^1$) |
| −1 | 0, 1, 2, 3, 4, 6, 7, 8 | 1 under 0, 7 under 8, 3 under 4 ($1 \le 2^0$) |

Each level is separated: points of $C_2$ are more than 4 apart, of $C_1$ more than 2, of $C_0$ more than 1, of $C_{-1}$ more than $1/2$. The explicit tree has $7 = n - 1$ entries.

Search for $q = 5.4$:

| $i$ | $Q$ = Children$(Q_i, i)$ with distances | $\delta(q, Q) + 2^i$ | kept $Q_{i-1}$ |
|---|---|---|---|
| 3 | 0 (5.4), 8 (2.6) | 10.6 | 0, 8 |
| 2 | 0 (5.4), 8 (2.6), 4 (1.4) | 5.4 | 0, 8, 4 |
| 1 | 0, 8, 4, 2 (3.4), 6 (0.6) | 2.6 | 8, 4, 6 |
| 0 | 8, 4, 6, 7 (1.6), 3 (2.4) | 1.6 | 4, 6, 7 |

The answer is 6 at distance 0.6. At the step $i = 1$ the points 0 and 2 are pruned, so the child 1 of 0 is never examined; at the step $i = 0$ the points 8 and 3 are pruned. The search evaluates distances to 7 of the 8 points; on larger sets the pruned subtrees are where the savings come from.

## Correctness

The proofs are in the proof file. The two main statements:

**Theorem 1 (insertion).** If the tree satisfies nesting, covering and separation, it satisfies them after INSERT$(p)$ for a point $p$ at positive distance from all stored points. The key lemma: if INSERT$(p, Q_j, j)$ returns "no parent found", then $\delta(p, r) > 2^l$ for every $l \le j$ and every $r \in C_l$, so $p$ can join every level $l \le i - 1$ without breaking separation.

**Theorem 2 (search).** NEAREST$(p)$ returns a nearest stored point. At each level the ancestor of a nearest point $p^*$ is kept, because it is within $2^i$ of $p^*$ and thus within $\delta(p, Q) + 2^i$ of $p$.

## Complexity

Model: real RAM in which a distance evaluation costs $E$; $c$ is the expansion constant of $S \cup \{p\}$ for the query or inserted point $p$. Beygelzimer, Kakade and Langford prove the bounds in the table for the explicit representation.

| operation | time | space |
|---|---|---|
| construction by $n$ insertions | $O(c^6 n \log n)$ evaluations | $O(n)$ |
| insert | $O(c^6 \log n)$ evaluations | $O(1)$ new entry |
| nearest neighbor | $O(c^{12} \log n)$ evaluations | $O(c^{\,O(1)})$ for the sets $Q_i$ |

The space bound is exact and holds for any metric: each point except the root is in one child list. The time bounds rest on two facts proved in the paper: each node has at most $c^4$ children in the explicit tree, and every point has depth $O(c^2 \log n)$ in it. For the uniform grid in $\mathbb{R}^D$, $c \approx 2^D$, so the factor $c^{12}$ is about $2^{12D}$, and the bounds are useful only when the intrinsic dimension is small. With no assumption on $c$, $c$ can be $n$ (see the simplex example of [intrinsic dimensionality](/intrinsic-dimensionality/)), and the search may evaluate all $n$ distances.

The bounds count levels of the explicit tree. A loop over all integer levels, as in the pseudocode and the reference code, runs $\log_2(\Delta)$ times, where $\Delta$ is the ratio of the largest to the smallest distance; implementations skip the levels at which no explicit node changes the sets.

## Variants

- **Base other than 2.** Use $b^i$ in place of $2^i$, with $b > 1$. A descendant of a node at level $i - 1$ is then within $\sum_{m \le i-1} b^m = b^i/(b - 1)$ of it, and the search keeps $q$ when $\delta(p, q) \le \delta(p, Q) + b^i/(b-1)$ at the level-$i$ step. A base below 2 gives more levels with fewer children each.
- **$k$ nearest neighbors.** Replace $\delta(p, Q)$ in line L9 by the $k$-th smallest distance in $Q$.
- **$(1 + \varepsilon)$-approximate search.** Stop the descent once $2^i$ is small compared with $\varepsilon \, \delta(p, Q)$ and return the nearest point of $Q$. By Lemma 1 of the proof every remaining candidate subtree is within $2^i$ of a point of $Q$, so with $2^i \le \varepsilon \, \delta(p, Q)/(1 + \varepsilon)$ the answer is within a factor $1 + \varepsilon$ of the nearest distance.
- **Batch construction and dual-tree search.** Build the tree from all points at once by splitting at each level, and answer many queries together with a cover tree of the queries, as in [k-nearest neighbor graph construction](/k-nearest-neighbor-graph-construction/).
- **Deletion.** Remove the node of $p$ and reinsert its children at the right levels.

## When to use it

- Exact nearest neighbor search in a general metric, or in a vector space of high ambient but low intrinsic dimension.
- When a guarantee in terms of the data's intrinsic dimension is wanted, together with linear space and dynamic insertion.
- Prefer a [k-d tree](/kd-tree/) for low-dimensional vectors (it is simpler and faster), and an approximate index such as [HNSW](/hnsw/) when the intrinsic dimension is high and exact answers are not needed.

## Pitfalls

- **Duplicates.** Two points at distance 0 break separation and make insertion descend forever. Store duplicates in a list at the first copy, as the reference code does.
- **The root level.** A new point farther than $2^{\text{top}}$ from the root needs a higher top level first; otherwise the first call fails.
- **Levels with no change.** Iterating over every integer level costs $\log_2 \Delta$ steps even for tiny data sets with very close or very far points. Jump between levels that have explicit nodes.
- **The constant $c^{12}$.** It is a worst-case factor, and it is huge even for moderate $c$. Measured performance is much better than the bound but still degrades with the intrinsic dimension.
- **Floating point.** The tests $\delta \le 2^i$ use computed distances; rounding can break separation by tiny amounts. Use exact powers of two and a consistent distance function.

## Implementations

## History

Karger and Ruhl introduced the expansion constant in 2002 and a nearest neighbor structure analyzed in terms of it. Beygelzimer, Kakade and Langford introduced the cover tree in 2006: a simpler structure with the nesting, covering and separation invariants, linear space independent of $c$, and the bounds in the table above.

## References
