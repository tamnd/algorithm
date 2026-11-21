---
tag: 3CXF3J
kind: algorithm
slug: k-anonymity-approximation
name: O(k) approximation for k-anonymity
aliases:
- Aggarwal k-anonymity approximation
area: security-and-privacy/data-anonymization
level: advanced
summary: Groups records into clusters of at least k by a forest construction and suppresses differing cells, within O(k) of the fewest suppressions.
model: word-ram
complexity:
  vars: {n: the number of rows, d: the number of columns, k: the least size of a cluster}
  time: {worst: O(n^2 d + n^2 log n)}
  space: {extra: O(n^2)}
history:
  year: 2005
  people: [Gagan Aggarwal, Tomas Feder, Krishnaram Kenthapadi, Rajeev Motwani, Rina Panigrahy, Dilys Thomas, An Zhu]
  note: "Aggarwal et al. gave the forest algorithm with ratio O(k) for k-anonymity by cell suppression at ICDT 2005, improving the O(k log k) of Meyerson and Williams."
prereqs: [k-anonymity, k-anonymity-np-hardness, approximation-ratio, hamming-distance, spanning-tree]
see_also: [generalization-and-suppression, mondrian-anonymization, datafly, microaggregation, steiner-tree-problem, set-cover, k-means, mdav]
sources:
  - paper: doi:10.1007/978-3-540-30570-5_17
    title: "Gagan Aggarwal, Tomas Feder, Krishnaram Kenthapadi, Rajeev Motwani, Rina Panigrahy, Dilys Thomas and An Zhu, Anonymizing tables, Proceedings of ICDT 2005, LNCS 3363"
    locator: "pp. 246 to 258, the graph representation, the forest algorithm, the decomposition of large trees, the ratio 3k - 3 and its improvement to max(2k - 1, 3k - 5), and the lower bound for the graph representation"
  - paper: doi:10.1145/1055558.1055591
    title: "Adam Meyerson and Ryan Williams, On the complexity of optimal k-anonymity, Proceedings of the 23rd ACM Symposium on Principles of Database Systems (PODS 2004)"
    locator: "pp. 223 to 228, Section 4, the O(k log k) and O(k log m) approximations and the bound of Lemma 4.1"
  - paper: doi:10.1145/1247480.1247490
    title: "Hyoungmin Park and Kyuseok Shim, Approximate algorithms for k-anonymity, Proceedings of ACM SIGMOD 2007"
    locator: "pp. 67 to 78, the O(log k) approximation"
---

The O(k) approximation of Aggarwal et al. (2005) makes a table [k-anonymous](/k-anonymity/) by suppressing cells, and it suppresses at most $3k - 3$ times the fewest possible cells. Finding the fewest is [NP-hard](/k-anonymity-np-hardness/) for $k \ge 3$. The algorithm sees the rows as the vertices of a complete graph, with the [Hamming distance](/hamming-distance/) as the weight of an edge. It grows a forest in which each tree has at least $k$ vertices and whose total weight is at most the optimum. Then it splits each tree with more than $3k - 3$ rows into smaller trees. Each final tree is a cluster, and in each cluster the cells of each column where its rows differ are replaced by a star.

## In plain words

Two rows that differ in few columns are cheap to put together, because only those columns must be hidden. So let each small group of rows reach out to the nearest row outside it, and join that row's group. Stop when every group has at least $k$ rows. A group can become too big, which makes it costly: a column is hidden in all its rows when any two of them differ. So cut each big group into parts of at least $k$ rows, and at most $3k - 3$.

The cost of one group is at most its number of rows times the total length of its edges, and the total length of all edges is no more than the best possible cost. That gives the factor $3k - 3$.

## The problem

The input is a table of $n$ rows $v_1, \ldots, v_n$, each with $d$ values, and an integer $k$ with $2 \le k \le n$. A release replaces some cells by $*$ so that each row is equal to at least $k - 1$ other rows. Its cost is the number of stars, and OPT is the least cost. For a set $C$ of rows, $\delta(C)$ is the number of columns on which not all rows of $C$ are equal. The output is a partition of the rows into clusters of at least $k$ rows; each cluster $C$ is released with its $\delta(C)$ differing columns suppressed, at a cost of $|C| \, \delta(C)$. The value of $k$ is a policy choice.

## The algorithm

```pseudo id=main
ANONYMIZE(V, k)
L1  w(x, y) ← the number of columns where rows x and y differ, for all pairs
L2  F ← n trees of one vertex each; each vertex is the root of its tree
L3  while some tree of F has fewer than k vertices do
L4      T ← such a tree, with the least root; u ← root(T)
L5      x ← the vertex outside T with the least w(u, x), ties to the lower index
L6      add the edge u → x; T joins the tree of x, whose root stays the root
L7  P ← the trees of F
L8  while some tree of P has more than 3k - 3 row vertices do
L9      replace that tree by the two trees of DECOMPOSE(tree, k)
L10 for each tree of P, with rows C: replace by * the cells of C in the δ(C) columns where C differs
L11 return the clusters, the released table and its cost

DECOMPOSE(T, k)                    ▷ s = the number of row vertices of T, s ≥ 3k - 2
L12 u ← the row vertex of least index; root T at u
L13 c ← the neighbor of u with the most row vertices on its side of the edge u-c; φ ← that number
L14 if φ > s - k then u ← c and go to L13
L15 if φ ≥ k then return the two trees made by cutting the edge u-c
L16 A ← the sides of the neighbors of u, largest first, until their row vertices number at least k
L17 return (A joined to a new Steiner copy of u, the rest with u)
```

A *Steiner vertex* is a copy of the values of a row, but it is not a row. It joins the parts of $A$ with the same edge weights they had to $u$. Line L13 counts only row vertices. Ties in line L13 go to the neighbor of lower index. The walk of lines L13 and L14 only goes down in the tree rooted at the start vertex.

## Example

Take 7 binary rows with 4 columns and $k = 3$: row 1 = 0000, row 2 = 0001, row 3 = 0011, row 4 = 1111, row 5 = 1110, row 6 = 1100 and row 7 = 0101.

| step | small tree, root $u$ | nearest row outside | edge | weight |
|---|---|---|---|---|
| 1 | {1}, root 1 | 2 | 1 → 2 | 1 |
| 2 | {1, 2}, root 2 | 3 | 2 → 3 | 1 |
| 3 | {4}, root 4 | 5 | 4 → 5 | 1 |
| 4 | {4, 5}, root 5 | 6 | 5 → 6 | 1 |
| 5 | {7}, root 7 | 2 | 7 → 2 | 1 |

The forest has the trees {1, 2, 3, 7} and {4, 5, 6}, with total weight 5. Both have at most $3k - 3 = 6$ rows, so DECOMPOSE is not needed. The cluster {1, 2, 3, 7} differs in columns 2, 3 and 4, and the cluster {4, 5, 6} in columns 3 and 4. So rows 1, 2, 3 and 7 become 0\*\*\*, and rows 4, 5 and 6 become 11\*\*. The cost is $4 \cdot 3 + 3 \cdot 2 = 18$. A search over all partitions into clusters of at least 3 rows shows that 18 is the optimum here. The proven bound is only $(3k - 3) \cdot 5 = 30$.

## Correctness

The proof has three steps. The full proof is in proofs/correctness.md.

1. **The forest is cheap.** Let $d_{k-1}(u)$ be the distance from $u$ to its $(k - 1)$-th nearest other row. When line L6 adds the edge from $u$, its tree has at most $k - 1$ vertices, so one of the $k - 1$ rows nearest to $u$ is outside, and $w(u, x) \le d_{k-1}(u)$. Each vertex starts at most one edge, because it stops being a root. In an optimal release the cluster of $u$ has $k - 1$ other rows, and its number of differing columns is at least $d_{k-1}(u)$. Each row of that cluster pays at least that much, so the weight of the forest is at most OPT.
2. **A split keeps both parts large and adds no weight.** The walk of line L14 stops at a vertex where each side has at most $s - k$ row vertices. If one side has at least $k$, line L15 cuts it off. If not, line L16 collects sides until it has between $k$ and $2k - 2$ rows, and the rest keeps at least $s - (2k - 2) \ge k$ rows. The Steiner copy has the values of $u$, so no edge gets heavier.
3. **A cluster costs at most its tree.** Each column where two rows of a cluster $C$ differ changes along some edge of the path between them, so $\delta(C)$ is at most the weight of the tree. With at most $3k - 3$ rows per cluster, the cost is at most $(3k - 3)$ times the weight of the forest, which is at most $(3k - 3)\,$OPT.

## Complexity

Let $n$ be the number of rows and $d$ the number of columns. The model is the [word RAM](/word-ram/).

- Line L1 computes $n^2$ distances in $O(n^2 d)$ time and keeps them in $O(n^2)$ space.
- Lines L3 to L6 merge at most $n - 1$ times, and each merge scans the $n$ rows: $O(n^2)$.
- A split of a tree with $t$ vertices takes $O(t \log t)$ for the rooting, the walk and the sort of line L16, and it adds at most one Steiner vertex. Each split removes at least $k$ rows from a large tree, so at most $n / k$ splits happen, each on at most $2n$ vertices: $O(n^2 \log n)$ in total.
- Line L10 takes $O(n d)$.

In total $O(n^2 d + n^2 \log n)$ time and $O(n^2)$ space.

## Properties

- **Ratio $3k - 3$.** This is a theorem for all inputs with $k \ge 2$. With a finer split, Aggarwal et al. (2005) improve the ratio to $\max(2k - 1, 3k - 5)$, and they give better ratios for small cases: 1.5 for $k = 2$, and 2 for $k = 3$ with binary values.
- **Cluster sizes.** Each cluster has between $k$ and $3k - 3$ rows. Small clusters keep more detail.
- **Limit of the method.** The algorithm uses only the distances between rows. Aggarwal et al. (2005) show two tables with the same distances whose optimal costs differ by a factor of order $k$. So no algorithm that sees only the distances can have a ratio better than order $k$.
- **Measured quality.** The ratio is a worst case. On the example above, the result is optimal. How far it is from the optimum on real tables is a question of measurement, not of this proof.

## Variants and improvements

- **Meyerson and Williams (2004).** An $O(k \log k)$ ratio, $3k(1 + \ln 2k)$, by greedy [set cover](/set-cover/) over candidate clusters, in time exponential in $k$, and an $O(k \log d)$ ratio in polynomial time.
- **Park and Shim (2007).** An $O(\log k)$ ratio; see their paper for the conditions on the running time.
- **Generalization in place of suppression.** The same clustering idea works with ranges or hierarchy values in place of stars, as in [Mondrian](/mondrian-anonymization/), but the bound above is only for suppression.
- **Clustering with means.** [Microaggregation](/microaggregation/), for example by [MDAV](/mdav/), forms clusters of at least $k$ rows by distances and releases the means. It is a heuristic for numeric data.

## When to use it

Use it when the release must keep cells exactly or hide them, with no generalization hierarchy, and a provable bound on the loss is wanted, for example for categorical data with many columns. For numeric data, or when ranges are acceptable, [Mondrian](/mondrian-anonymization/) is faster and usually keeps more detail. For a uniform coding of each column, use full-domain [generalization](/generalization-and-suppression/).

## Pitfalls

- **Any vertex as the start of the edge in line L4.** The proof charges each edge to the vertex where it starts, once. If line L4 takes a vertex of $T$ that is not the root, one vertex can start two edges, and the bound $W(F) \le$ OPT fails.
- **The nearest vertex inside $T$ in line L5.** If line L5 looks at all rows, the nearest one can be in $T$ itself. The edge then closes a cycle and the tree does not grow, so the loop never ends. Take the nearest vertex outside $T$.
- **Joining $A$ to $u$ itself in line L17.** The parts of $A$ were joined only through $u$, and so were the other parts. If $A$ takes $u$, the rest falls apart into several pieces, which are not a tree, and the weight argument fails. Use a Steiner copy of $u$, which is not a row.
- **$k = 1$ in line L8.** Then $3k - 3 = 0$, and line L8 tries to split each tree forever. For $k = 1$ the table is already 1-anonymous with no stars, so return it.

## Implementations

## History

Meyerson and Williams (2004) proved that k-anonymity by suppression is NP-hard and gave the first approximation algorithms, with ratio $O(k \log k)$. Aggarwal, Feder, Kenthapadi, Motwani, Panigrahy, Thomas and Zhu (ICDT 2005) gave the forest algorithm with ratio $O(k)$, showed that a ternary alphabet is enough for NP-hardness, and showed that $O(k)$ is the best ratio for methods that use only the distances. Park and Shim (2007) later lowered the ratio to $O(\log k)$.

## References
