---
tag: 4PEVCW
kind: problem
slug: free-tree-generation
name: Free unlabeled tree generation
aliases:
- Generating free trees
- Unrooted tree enumeration
- Listing trees up to isomorphism
area: combinatorics/generating-partitions-and-trees
level: advanced
summary: Enumerate all non-isomorphic trees with n nodes where no node is distinguished as root.
model: word-ram
complexity:
  vars: {n: the number of nodes, N: the number of free trees with n nodes}
  time: {worst: Θ(n + N)}
prereqs: [tree, tree-center, rooted-tree-generation]
see_also: [wright-richmond-odlyzko-mckay, rooted-tree-generation, beyer-hedetniemi, labeled-tree-generation, tree-center, tree-isomorphism, graph-generation, cayley-formula]
sources:
  - url: https://page.math.tu-berlin.de/~felsner/SemWS17-18/Ruskey-Comb-Gen.pdf
    title: Frank Ruskey, Combinatorial Generation, working version, University of Victoria, 1995 to 2003
    locator: Section 4.6.2, Rooted Trees, Free Trees (the table of t_n, formula (4.28), the rooted version of a free tree, Theorem 4.3, Algorithm 4.19 and Theorem 4.4)
  - paper: doi:10.1137/0215039
    title: Robert Alan Wright, Bruce Richmond, Andrew Odlyzko and Brendan D. McKay, Constant time generation of free trees, SIAM Journal on Computing 15(2) (1986), 540 to 548
    locator: the whole paper
  - url: https://oeis.org/A000055
    title: OEIS A000055, Number of trees with n unlabeled nodes
    locator: the terms, Otter's formula and the asymptotic constants
---

Free tree generation is the problem of listing every tree with $n$ nodes exactly once up to isomorphism, where a tree is a connected graph without cycles and no node is special. There are $t_n$ such trees, $1, 1, 1, 2, 3, 6, 11, 23, 47, 106, \ldots$, and $t_n$ grows like $2.956^n / n^{5/2}$. The standard solution roots each tree at its center and lists the resulting rooted trees with the [Wright-Richmond-Odlyzko-McKay algorithm](/wright-richmond-odlyzko-mckay/), in constant amortized time per tree.

## In plain words

A tree is a set of dots joined by lines so that every two dots are connected in exactly one way. Two trees are the same if you can move the dots of one to get the other, keeping the lines. You want one picture of each different tree.

The difficulty is that the same tree can be drawn in many ways. The fix is to pick one standard drawing. Every tree has a middle, the center: one node, or two nodes joined by a line. Hang the tree from its middle, put the largest branches first, and the drawing becomes unique. Then step through these drawings with a fast rule for rooted trees, and skip the drawings whose top is not the middle.

## Definition

A *free tree* is a connected acyclic graph. Two free trees are *isomorphic* if there is a bijection between their vertex sets that keeps adjacency. Let $\mathcal{T}_n$ be the set of isomorphism classes of free trees with $n$ vertices, and $t_n = |\mathcal{T}_n|$.

**Input:** an integer $n \ge 1$.

**Output:** a sequence that contains one representative of each class in $\mathcal{T}_n$ exactly once, given as an edge list, a parent array, or a canonical level sequence.

**Cost model.** The [word RAM](/word-ram/). The trees are visited in place: the generator keeps one tree and changes it, and the time counts these changes. Copying each tree out costs $\Theta(n)$ per tree, and is not counted.

## Variants

- **Labeled trees.** If the vertices carry the labels $1, \ldots, n$, there are $n^{n-2}$ trees by [Cayley's formula](/cayley-formula/), and the [Prüfer code](/pruefer-decoding/) lists them without any isomorphism test; see [labeled tree generation](/labeled-tree-generation/).
- **Rooted trees.** If one vertex is marked as the root, the problem is [rooted tree generation](/rooted-tree-generation/), with $a_n$ trees.
- **Restricted trees.** Trees with bounded maximum degree, such as the carbon skeletons of alkanes, with degree at most $4$; trees with bounded diameter or radius; trees with a given number of leaves or a given degree sequence. A filter on the output solves them, at the cost of the trees it rejects.
- **Order.** Decreasing lexicographic order of the rooted versions, which is the order of the standard algorithm; or orders in which consecutive trees differ by a small change.
- **Random generation.** Draw one tree uniformly from $\mathcal{T}_n$ without listing them all. Uniform sampling of unlabeled trees needs counting tables; a random labeled tree, which is easy to draw, is not uniform over $\mathcal{T}_n$.
- **Counting only.** Computing $t_n$ needs no generation; Otter's formula below gives it from the numbers $a_n$ of rooted trees.

## Examples

- $n = 4$: the path and the star $K_{1,3}$. Rooted at a center, their canonical level sequences are $0121$ and $0111$.
- $n = 5$: the path $01212$, the "chair" $01211$, a path of $4$ with a leaf on a middle node, and the star $01111$.
- $n = 6$: six trees, $012312$, $012212$, $012211$, $012121$, $012111$ and $011111$. The first is the path, which has two centers; it is rooted at one of them, and its first subtree is the other half of the path.

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $t_n$ | 1 | 1 | 1 | 2 | 3 | 6 | 11 | 23 | 47 | 106 | 235 | 551 | 1301 | 3159 | 7741 | 823065 |

## Known algorithms

| method | total time | notes |
|---|---|---|
| labeled trees by Prüfer codes, keep one per class | $\Omega(n^{n-2})$ | needs a canonical form per tree, hopeless beyond $n \approx 10$ |
| rooted trees by [Beyer-Hedetniemi](/beyer-hedetniemi/), keep the rooted versions ([generate and test](/generate-and-test/)) | $\Theta(n + a_n)$ | $a_n / t_n$ grows like $0.82\, n$ |
| [Wright-Richmond-Odlyzko-McKay](/wright-richmond-odlyzko-mckay/) | $\Theta(n + t_n)$ | constant amortized time |
| [orderly generation](/orderly-generation/) or [canonical augmentation](/canonical-augmentation/) of graphs, restricted to trees | polynomial per tree | general method, much slower for trees |

- **Generate and test from rooted trees.** Root each free tree at its center, with a fixed rule for two centers. A rooted tree is the rooted version of a free tree when its root has two highest subtrees of equal height, or of heights differing by one with a size and order condition. Listing all rooted trees and testing each is correct, but the ratio $a_n / t_n$ is $6.8$ for $n = 10$ and $15.6$ for $n = 20$.
- **Wright-Richmond-Odlyzko-McKay.** Apply the rooted tree successor; when the result fails the test, the first subtree of the root must change, so jump to the largest rooted tree with a smaller first subtree, and add a path as a second subtree if needed. The failures are rare, and the cost per tree is constant amortized.
- **Generic isomorph rejection.** Generators for general graphs, such as those built on [canonical labeling](/canonical-labeling/), also produce trees, but they pay a polynomial cost per tree.

## Bounds

- Every method must visit $t_n$ trees, so $\Omega(t_n)$ time is necessary in the in-place model. The Wright-Richmond-Odlyzko-McKay algorithm meets this bound.
- $t_n \sim C\, \alpha^n n^{-5/2}$ with $\alpha \approx 2.9558$ and $C \approx 0.5349$, where $\alpha$ is the same growth constant as for rooted trees. So listing is practical up to about $n = 25$, where $t_{25} = 104636890$.
- In the full output model, writing each tree costs $\Theta(n)$, and the total is $\Theta(n t_n)$.

## Reductions

- **Free trees to rooted trees.** The center of a tree is the middle vertex, or the middle edge, of every longest path, and it can be found in linear time by [leaf peeling](/tree-center-leaf-peeling/). Rooting at the center, with a rule for the two ends of a central edge, maps each free tree to one rooted tree. So free tree generation reduces to rooted tree generation with a filter, and free [tree isomorphism](/tree-isomorphism/) reduces to rooted tree isomorphism.
- **Otter's formula.** Otter's dissimilarity theorem, which compares the classes of vertices and of edges of a tree, gives
$$t_n = a_n - \frac{1}{2}\Big(\sum_{i=1}^{n-1} a_i a_{n-i} - [n \text{ even}]\, a_{n/2}\Big),$$
where $a_n$ counts rooted trees. Since each free tree has exactly one rooted version, the subtracted term equals the number of rooted trees whose root is not the chosen center.
- **Labeled to unlabeled.** Each class in $\mathcal{T}_n$ contains $n! / |\mathrm{Aut}(T)|$ labeled trees, where $\mathrm{Aut}(T)$ is the [automorphism group](/graph-automorphism-group/). This relates the two counts, but it does not give a fast generator.

## Applications

- Exhaustive checks of conjectures about trees, such as graceful labeling or bounds on graph invariants, on every tree up to a given size.
- Chemistry: the acyclic hydrocarbons are trees of carbon atoms with degree at most $4$, and their enumeration was one of the first uses of tree counting.
- Testing algorithms on trees, such as tree isomorphism, center and diameter computations, and dynamic programs on trees, on every shape of a small size.
- Building blocks for the generation of graphs with few cycles, such as unicyclic graphs.

## References
