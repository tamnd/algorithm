---
tag: W1HHC1
kind: problem
slug: tree-isomorphism
name: Tree isomorphism
aliases:
- rooted tree isomorphism
- unordered tree isomorphism
- unrooted tree isomorphism
area: graphs/graph-isomorphism
level: intro
summary: Decide whether two trees are isomorphic; solvable in linear time for rooted and unrooted trees.
model: word-ram
complexity:
  vars: {n: the number of vertices of each tree}
  time: {worst: Θ(n)}
prereqs: [tree, rooted-tree, graph-isomorphism-definition]
see_also: [ahu-algorithm, tree-center, graph-isomorphism-problem, canonical-labeling, weisfeiler-leman, tree-edit-distance, subgraph-isomorphism, planar-graph-isomorphism]
sources:
  - book: isbn:9780201000290
    title: Alfred V. Aho, John E. Hopcroft and Jeffrey D. Ullman, The Design and Analysis of Computer Algorithms, Addison-Wesley, 1974
    locator: Section 3.2, Radix sorting (Example 3.2, isomorphism of rooted trees in linear time)
  - book: isbn:9783540435506
    title: Gabriel Valiente, Algorithms on Trees and Graphs, Springer, 2002
    locator: Chapter 4, Tree isomorphism (ordered and unordered trees, and subtree isomorphism)
  - paper: "David W. Matula, Subtree isomorphism in O(n^(5/2)), Annals of Discrete Mathematics 2, 91 to 106 (1978)"
    locator: the whole paper (subtree isomorphism by bipartite matching)
  - paper: "Steven Lindell, A logspace algorithm for tree canonization, Proceedings of the 24th ACM Symposium on Theory of Computing (STOC 1992), 400 to 404"
    locator: the whole paper
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A1.4, Subgraph isomorphism (the comment on the case of a forest pattern and a tree host)
---

Tree isomorphism asks whether two trees have the same shape: whether there is a bijection between their vertices that maps edges to edges. It is the [graph isomorphism problem](/graph-isomorphism-problem/) restricted to trees, and unlike the general problem it is solved in linear time, by the [AHU algorithm](/ahu-algorithm/) for rooted trees and by rooting at the [centers](/tree-center/) for free trees. The problem has a rooted version, where roots must map to roots, and ordered versions, where the order of children counts. It is the standard example of an isomorphism problem that a canonical form solves completely.

## In plain words

You have two trees drawn on paper, with the points named differently. You want to know whether one drawing can be turned into the other by renaming the points, so that two points are linked in one drawing exactly when their new names are linked in the other. For trees, you can answer fast. Give each point a description built from the descriptions of the points below it, starting at the bottom. Two trees have the same shape when their top descriptions are equal. If the trees have no fixed top, start from the middle point, which every renaming must keep in the middle.

## Definition

A **free tree** is a connected acyclic graph $T = (V, E)$. A **rooted tree** is a pair $(T, r)$ with $r \in V$. The trees are undirected and unlabeled; vertex colors or labels are a variant below.

**Free tree isomorphism.**
- Input: trees $T_1 = (V_1, E_1)$ and $T_2 = (V_2, E_2)$, as edge lists.
- Output: yes when there is a bijection $\varphi : V_1 \to V_2$ with $\{u, v\} \in E_1 \iff \{\varphi(u), \varphi(v)\} \in E_2$; otherwise no.

**Rooted tree isomorphism.** Input $(T_1, r_1)$, $(T_2, r_2)$; the bijection must also satisfy $\varphi(r_1) = r_2$.

**Ordered tree isomorphism.** Each vertex has a sequence of children; the bijection must map the $j$-th child of $v$ to the $j$-th child of $\varphi(v)$.

The search versions ask for $\varphi$, and the canonization version asks for a string $\mathrm{can}(T)$ with $\mathrm{can}(T_1) = \mathrm{can}(T_2) \iff T_1 \cong T_2$.

## Variants

- **Rooted versus free.** A free-tree instance reduces to at most two rooted instances by rooting at the centers. A rooted instance is not a free instance: the path $a - b - c$ rooted at $a$ and rooted at $b$ are isomorphic as free trees but not as rooted trees.
- **Ordered trees.** Two ordered trees are isomorphic exactly when their preorder parenthesis strings are equal, so the problem is string equality.
- **Labeled or colored trees.** Vertices carry labels that the bijection must keep. AHU handles this by putting the label at the front of each key.
- **Subtree isomorphism.** Decide whether a tree $P$ is isomorphic to a subgraph of a tree $T$. This is polynomial (Matula 1978, by bipartite matching at each vertex). If the pattern may be a forest, the problem becomes NP-complete.
- **Tree edit distance.** Measure how far two trees are from isomorphic; see [tree edit distance](/tree-edit-distance/) and the [Zhang-Shasha algorithm](/zhang-shasha-algorithm/) for ordered trees.
- **Counting.** The number of isomorphisms between two isomorphic rooted trees equals $|\mathrm{Aut}(T_1, r_1)|$, which is the product, over all vertices $v$, of $m!$ for each group of $m$ children of $v$ with equal AHU codes.

## Examples

**Small trees.** The numbers of non-isomorphic free trees with 2 to 8 vertices are 1, 1, 2, 3, 6, 11, 23. The numbers of non-isomorphic rooted trees are 1, 2, 4, 9, 20, 48, 115.

**Path and star.** The path $P_4$ and the star $K_{1,3}$ are both trees with 4 vertices. They are not isomorphic: the star has a vertex of degree 3.

**Same degrees, different trees.** Let $A$ have the edges $01, 02, 03, 14, 15, 26, 67$ and $B$ the edges $02, 21, 03, 04, 15, 17, 76$. Both have 8 vertices and the degree sequence $(3, 3, 2, 2, 1, 1, 1, 1)$. In $A$ the two vertices of degree 3 (0 and 1) are adjacent; in $B$ they (0 and 1) are not, so no isomorphism exists. The degree sequence alone does not decide tree isomorphism.

**A rooted pair.** Root $T_1$ at 0 with children 1, 2, 3, where 1 has two leaf children and 2 has a child with one leaf child. Root $T_3$ at 0 with children 1, 2, 3, where 1 has three children and one of them has a leaf child. Both have 8 vertices and 1, 3, 3 and 1 vertices at levels 0 to 3, but the [AHU algorithm](/ahu-algorithm/) separates them at level 1, where the children's multisets differ.

## Known algorithms

| algorithm | version | time |
|---|---|---|
| [AHU algorithm](/ahu-algorithm/) | rooted, and free via centers | $\Theta(n)$ with radix sort |
| AHU with parenthesis strings | rooted | $O(n^2)$ worst case, simple |
| [Color refinement](/weisfeiler-leman/) | free | $O(n \log n)$; it identifies trees |
| Lindell (1992) | free and rooted, canonization | logarithmic space |
| Matula (1978) | subtree isomorphism | $O(n^{5/2})$ |
| [Brute force over permutations](/graph-isomorphism-problem/) | any | $O(n! \cdot n)$ |

[Tree centers](/tree-center/) are found by peeling leaves in $O(n)$ time.

## Bounds

- **Upper bound.** $\Theta(n)$ time on the [word RAM](/word-ram/) for rooted, free and ordered trees, worst case, by AHU.
- **Lower bound.** $\Omega(n)$: an algorithm that does not read some edge cannot tell the tree from one where that edge is moved.
- **Space.** Logarithmic space suffices (Lindell 1992).

## Reductions

- **Free to rooted.** Find the centers ($O(n)$) and make at most two rooted calls.
- **Rooted to free.** Attach $n + 1$ new leaves to each root. The root is then the only vertex of degree more than $n$, so every isomorphism of the new free trees maps root to root, and the new free trees are isomorphic exactly when the rooted trees are.
- **To graph isomorphism.** Trees are graphs, so any graph isomorphism algorithm applies. The reverse fails: tree isomorphism is much easier than [graph isomorphism](/graph-isomorphism-problem/), which is not known to be in polynomial time.
- **As a subroutine.** [Planar graph isomorphism](/planar-graph-isomorphism/) reduces to isomorphism of triconnected components plus isomorphism of a colored tree of components.

## Applications

- Comparing parse trees, phylogenetic trees and hierarchical data without order, such as JSON objects with unordered keys.
- Chemistry: acyclic molecules are trees, and canonical codes of trees are used to store them without duplicates.
- Generating all trees of a given size without repeats, by keeping only trees whose code is canonical.
- As a step in isomorphism tests for planar graphs, interval graphs and other classes with tree decompositions.

## References
