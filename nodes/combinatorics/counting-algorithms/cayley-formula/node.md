---
tag: SQY9VT
kind: theorem
slug: cayley-formula
name: Cayley's formula
aliases:
- Cayley's tree formula
- labeled trees count n^(n-2)
- Cayley's theorem on trees
area: combinatorics/counting-algorithms
level: core
summary: For n at least 1, there are n^(n-2) trees on n labeled vertices, so the complete graph K_n has n^(n-2) spanning trees.
prereqs: [tree, double-counting, rule-of-product]
see_also: [prufer-sequence, pruefer-decoding, labeled-tree-generation, matrix-tree-theorem, counting-spanning-trees, counting-connected-labeled-graphs, rooted-tree, uniform-spanning-tree-sampling]
sources:
  - book: isbn:9780521006019
    title: J. H. van Lint and R. M. Wilson, A Course in Combinatorics, second edition, Cambridge University Press, 2001
    locator: Chapter 2, Trees (Cayley's theorem with several proofs)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3.4.4, Enumeration of trees (labeled trees and Cayley's formula)
  - paper: doi:10.1006/jcta.1998.2919
    title: Jim Pitman, Coalescent random forests, Journal of Combinatorial Theory, Series A 85(2), 165 to 193, 1999
    locator: Section 1 (the double-counting proof of Cayley's formula by building rooted forests one edge at a time)
---

Cayley's formula says that for each $n \ge 1$, the number of [trees](/tree/) with vertex set $[n] = \{1, \ldots, n\}$ is $n^{n-2}$. Equivalently, the complete graph $K_n$ has $n^{n-2}$ spanning trees. The formula has many proofs: a bijection with sequences (the [Prüfer sequence](/prufer-sequence/)), a determinant (the [matrix-tree theorem](/matrix-tree-theorem/)), generating functions, and the short double-counting proof below. It is the base case of the counts of connected structures, and it gives a simple way to pick a uniformly random labeled tree.

## Statement

Notation: $[n] = \{1, \ldots, n\}$. A *labeled tree* on $[n]$ is a connected graph with vertex set $[n]$ and no cycles; two labeled trees are the same only if they have the same edge set. A *rooted tree* is a tree with one marked vertex. A *rooted forest* is a graph with no cycles in which each component has one marked vertex.

**Theorem (Cayley's formula).** For each integer $n \ge 1$, the number $T_n$ of labeled trees on $[n]$ is

$$T_n = n^{n-2}.$$

For $n = 1$ this reads $1^{-1} = 1$: the single vertex is the one tree.

**Corollaries.** For $n \ge 1$: there are $n^{n-1}$ rooted labeled trees on $[n]$, and the complete graph $K_n$ has $n^{n-2}$ spanning trees.

## In plain words

Take a fixed set of numbered points. A tree joins all of them with lines so that you can go from each point to each other point, and there is exactly one way to do so without going back. How many different trees can you draw on the same numbered points?

For three points, there are three trees: one point sits in the middle each time. For four points, there are sixteen: twelve paths and four stars. Cayley's formula says the count is the number of points raised to the power of the number of points minus two.

One proof builds a tree by adding one line at a time and counts the ways to do this in two different orders. Both counts must agree, and that gives the formula.

## Proof

The proof is the double-counting argument of Pitman (1999). Fix $n \ge 2$; the case $n = 1$ is checked directly. Direct each edge of a rooted tree away from the root, so that each vertex other than the root has exactly one incoming edge. Let $\mathcal{S}$ be the set of pairs $(T, \sigma)$ where $T$ is a rooted labeled tree on $[n]$ and $\sigma$ is an ordering $e_1, e_2, \ldots, e_{n-1}$ of its $n - 1$ directed edges. We count $\mathcal{S}$ in two ways.

*First count.* There are $n T_n$ rooted trees, because each of the $T_n$ trees has $n$ choices of root, and $(n-1)!$ orderings of the edges of each. So $|\mathcal{S}| = n T_n (n-1)!$.

*Second count.* Build the sequence $e_1, \ldots, e_{n-1}$ one edge at a time, starting from the forest $F_0$ of $n$ isolated vertices, each its own root. Let $F_j$ be the directed graph with edges $e_1, \ldots, e_j$.

*Claim.* For each $(T, \sigma) \in \mathcal{S}$ and each $j$, the graph $F_j$ is a rooted forest with $n - j$ components, in which the roots are the vertices with no incoming edge, and $e_{j+1} = (u, v)$ goes from some vertex $u$ to a root $v$ of a component of $F_j$ that does not contain $u$.

*Proof of the claim.* $F_j$ is a subgraph of the tree $T$, so it has no cycle, and it has $n - j$ components because each edge of a forest joins two components. Each vertex has at most one incoming edge in $T$, hence in $F_j$, and each component $K$ of $F_j$ is a tree with $|K| - 1$ edges, each of which enters a distinct vertex of $K$. So exactly one vertex of $K$ has no incoming edge; call it the root of $K$. The edge $e_{j+1} = (u, v)$ is the only edge of $T$ into $v$, so $v$ has no incoming edge in $F_j$ and is a root. If $u$ were in the component of $v$, then $F_{j+1}$ would contain a cycle, which a subgraph of $T$ cannot. $\square$

Conversely, start from $F_0$ and, at step $j + 1$, add any directed edge $(u, v)$ where $v$ is a root of $F_j$ and $u$ is outside the component of $v$. The result $F_{j+1}$ is again a rooted forest whose roots are the vertices with no incoming edge: the two components of $u$ and $v$ merge, and the root of the merged component is the root of $u$'s component. After $n - 1$ steps there is one component, a rooted tree $T$, and the order of the added edges is an ordering $\sigma$ of its edges. So the sequences of choices are in bijection with $\mathcal{S}$.

Count the choices. At step $j + 1$, the forest $F_j$ has $n - j$ components. The vertex $u$ can be any of the $n$ vertices, and then $v$ can be the root of any of the $n - j - 1$ components that do not contain $u$. So there are $n(n - j - 1)$ choices, whatever the earlier choices were. By the [rule of product](/rule-of-product/),

$$|\mathcal{S}| = \prod_{j=0}^{n-2} n (n - j - 1) = n^{n-1} (n-1)!.$$

*Conclusion.* $n T_n (n-1)! = n^{n-1} (n-1)!$, so $T_n = n^{n-2}$. $\blacksquare$

The corollaries follow: a rooted tree is a tree with a choice of one of $n$ roots, which gives $n \cdot n^{n-2} = n^{n-1}$, and a spanning tree of $K_n$ is the same thing as a labeled tree on its vertex set.

## Consequences

### Worked examples

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| $n^{n-2}$ (OEIS A000272) | 1 | 1 | 3 | 16 | 125 | 1296 | 16807 | 262144 | 4782969 | 100000000 |

For $n = 4$ the 16 trees are the $4!/2 = 12$ labeled paths and the 4 stars, one for each choice of center. For $n = 5$ the 125 trees have three shapes: $5!/2 = 60$ paths, 5 stars, and 60 trees with one vertex of degree 3 (choose the center in 5 ways, then the neighbor of the center that has a further neighbor in 4 ways, then that further neighbor in 3 ways). The sum is $60 + 5 + 60 = 125$.

### Where the formula is used

- **Prüfer codes.** The [Prüfer sequence](/prufer-sequence/) is a bijection between labeled trees on $[n]$ and sequences in $[n]^{n-2}$, which is a second proof. It gives linear-time [ranking and decoding](/pruefer-decoding/), and a uniformly random labeled tree from $n - 2$ uniform random numbers, as in [labeled tree generation](/labeled-tree-generation/).
- **The matrix-tree theorem.** The [matrix-tree theorem](/matrix-tree-theorem/) counts the spanning trees of any graph by a determinant. For $K_n$ the reduced Laplacian is $nI - J$ of order $n - 1$, with determinant $n^{n-2}$, which is a third proof. For other graphs, see [counting spanning trees](/counting-spanning-trees/).
- **Rooted forests.** The same edge-by-edge count, stopped after $n - k$ edges, shows that the number of rooted forests on $[n]$ with $k$ trees is $\binom{n}{k} k \, n^{n-k-1}$, and with $k$ given roots it is $k \, n^{n-k-1}$. Adding a new vertex $0$ joined to all roots shows that there are $(n+1)^{n-1}$ rooted forests on $[n]$ in total.
- **Counting connected graphs.** Trees are the connected graphs with the fewest edges, $n - 1$. The count of [connected labeled graphs](/counting-connected-labeled-graphs/) with $n - 1$ edges is $n^{n-2}$, which is a check on the general recurrence.
- **Exponential generating functions.** The EGF $R(x) = \sum_{n \ge 1} n^{n-1} x^n / n!$ of rooted trees satisfies $R(x) = x e^{R(x)}$, the start of the Lagrange inversion method in [exponential generating functions](/exponential-generating-functions/).

## Tightness

The formula is exact for every $n \ge 1$. The labels matter: up to isomorphism, the number of trees is much smaller (1, 1, 1, 2, 3, 6, 11, 23 for $n = 1, \ldots, 8$), and there is no closed form; see [free tree generation](/free-tree-generation/). The value $n = 0$ is a convention: the empty graph is not connected in most definitions, while OEIS A000272 sets the value to 1.

## History

Borchardt proved the formula in 1860 with determinants. Cayley stated it in 1889 in a short paper, and his name stuck. Prüfer gave the bijective proof with sequences in 1918. Pitman's double-counting proof, given above, is from 1999.

## References
