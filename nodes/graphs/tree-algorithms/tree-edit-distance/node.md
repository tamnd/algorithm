---
tag: BWXJXN
kind: problem
slug: tree-edit-distance
name: Tree edit distance
aliases:
- Tai distance
area: graphs/tree-algorithms
level: advanced
summary: Minimum cost of node insertions, deletions and relabelings turning one ordered tree into another.
prereqs: [rooted-tree, edit-distance, tree-traversal]
see_also: [zhang-shasha-algorithm, graph-edit-distance, edit-distance, weighted-edit-distance, tree-isomorphism, edit-distance-seth-lower-bound, wagner-fischer-algorithm, ordered-tree-generation]
sources:
  - paper: doi:10.1145/322139.322143
    title: Kuo-Chung Tai, The tree-to-tree correction problem, Journal of the ACM 26(3), 422 to 433 (1979)
    locator: the edit operations on ordered labelled trees, the definition of a mapping, and the first polynomial algorithm
  - paper: doi:10.1137/0218082
    title: Kaizhong Zhang and Dennis Shasha, Simple fast algorithms for the editing distance between trees and related problems, SIAM Journal on Computing 18(6), 1245 to 1262 (1989)
    locator: the equivalence of edit sequences and mappings for metric costs, and the forest dynamic program
  - paper: doi:10.1016/j.tcs.2004.12.030
    title: Philip Bille, A survey on tree edit distance and related problems, Theoretical Computer Science 337(1 to 3), 217 to 239 (2005)
    locator: the survey of the ordered and unordered problems, the alignment and inclusion variants, and their algorithms and hardness results
  - paper: doi:10.1016/0020-0190(92)90136-J
    title: Kaizhong Zhang, Rick Statman and Dennis Shasha, On the editing distance between unordered labeled trees, Information Processing Letters 42(3), 133 to 139 (1992)
    locator: the NP-completeness of the edit distance between unordered labelled trees
  - paper: doi:10.1145/1644015.1644017
    title: Erik D. Demaine, Shay Mozes, Benjamin Rossman and Oren Weimann, An optimal decomposition algorithm for tree edit distance, ACM Transactions on Algorithms 6(1), Article 2 (2009)
    locator: the O(n^3) algorithm and the lower bound for decomposition strategies
---

The tree edit distance between two ordered labelled rooted trees is the least total cost of a sequence of node deletions, node insertions and node renames that turns the first tree into the second. It extends the [edit distance](/edit-distance/) of strings to trees: on two paths it is the edit distance of the label sequences. Tai defined it in 1979. For ordered trees it is solvable in polynomial time, by the [Zhang-Shasha algorithm](/zhang-shasha-algorithm/) in $O(n^4)$ worst-case time and $O(n^2 \log^2 n)$ on balanced trees, and in $O(n^3)$ time by the method of Demaine, Mozes, Rossman and Weimann. For unordered trees it is NP-hard. It is used to compare XML documents, parse trees, RNA structures and program versions.

## In plain words

Two family trees, two versions of a document outline, or two parse trees of a program look almost the same, and you want a number that says how far apart they are. You are allowed three kinds of changes. You can delete a node; its children then hang from its parent, in the same place. You can insert a node, which takes some neighbouring children of a node as its own. You can change the label of a node. Each change has a price. The tree edit distance is the lowest total price of changes that makes the first tree equal to the second.

The order of the children matters: a node with children A then B is not the same as one with B then A. If the order did not matter, the problem would become much harder.

## Definition

**Input.** Two ordered rooted trees $T_1$ and $T_2$ with $n_1$ and $n_2$ nodes. Tree $T_t$ has the nodes $0, \ldots, n_t - 1$, a root, an ordered list of children for each node, and a label from an alphabet $\Sigma$ on each node. The trees are not weighted; costs sit on the operations. A cost function $\gamma$ gives $\gamma(a \to \varepsilon) \ge 0$ for deleting a label $a$, $\gamma(\varepsilon \to b) \ge 0$ for inserting $b$, and $\gamma(a \to b) \ge 0$ for renaming $a$ to $b$. The unit cost model is $1$, $1$ and $[a \ne b]$.

**Edit operations.** Deleting a node $v$ with parent $u$ replaces $v$, in the list of children of $u$, by the children of $v$, in order. Inserting a node $v$ as a child of $u$ is the inverse: $v$ takes a run of consecutive children of $u$ as its children. Renaming changes a label. These operations also act on forests, ordered lists of trees.

**Output.** The tree edit distance $\delta(T_1, T_2)$, the least cost of a sequence of operations that turns $T_1$ into $T_2$, and often the operations or the matching of the nodes.

**Mappings.** A *mapping* is a set $M$ of pairs of nodes $(v, w)$, $v \in T_1$, $w \in T_2$, that uses each node at most once and keeps the ancestor relation and the left-to-right order between any two pairs. Its cost is the sum of the rename costs of its pairs, the deletion costs of the nodes of $T_1$ not in $M$, and the insertion costs of the nodes of $T_2$ not in $M$. When $\gamma$ is a metric, $\delta(T_1, T_2)$ is the least cost of a mapping, so the problem is to find a best mapping.

## Variants

- **Unit costs.** All operations cost $1$, except renaming to the same label, which costs $0$. The distance is then at most $n_1 + n_2$.
- **Unordered trees.** The children of a node form a set. The edit distance is then NP-complete, as Zhang, Statman and Shasha proved, and it is also hard to approximate. Restricted versions, such as the constrained edit distance where disjoint subtrees map to disjoint subtrees, are polynomial.
- **Tree alignment.** Insert nodes into both trees to make them equal in shape, then pay for the label differences. Alignment is a restriction of editing, so its value is at least the edit distance and can be larger; it is polynomial for ordered trees.
- **Tree inclusion.** Decide whether $T_2$ can be obtained from $T_1$ by deletions only.
- **Top-down and bottom-up distances.** Restrict the mappings so that a mapped node has a mapped parent (top-down), or so that whole subtrees are mapped (bottom-up). Both are faster and are used in file comparison tools.
- **Edit distance of strings.** For two paths, a mapping is a common subsequence, and the distance is the string [edit distance](/edit-distance/) of the label sequences, computed by [Wagner-Fischer](/wagner-fischer-algorithm/).
- **Graphs.** For general graphs, the corresponding problem is the [graph edit distance](/graph-edit-distance/), which is NP-hard.

## Examples

| $T_1$ | $T_2$ | unit cost distance | why |
|---|---|---|---|
| single node $a$ | single node $a$ | 0 | equal |
| single node $a$ | single node $b$ | 1 | one rename |
| path of $n$ nodes labelled $a$ | single node $a$ | $n - 1$ | delete $n - 1$ nodes |
| star, centre $x$, $k \ge 1$ leaves $x$ | path of $k + 1$ nodes $x$ | $2(k - 1)$ | a mapping keeps at most the centre and one leaf |
| $f(d(a, c(b)), e)$ | $f(c(d(a, b)), e)$ | 2 | delete $c$, then insert $c$ above $d$ |
| $r(a, b)$ | $r(b, a)$ | 2 | rename both leaves; $0$ if unordered |

The trees are written as label(children). In the star and path row, the leaves of the star are pairwise unrelated, while the nodes of the path all lie on one chain, so a mapping can pair at most one leaf, plus the centre with the top of the path. The unmapped $k - 1$ nodes on each side cost $2(k - 1)$. In the last row, mapping $a$ to $a$ and $b$ to $b$ together breaks the left-to-right order. The best mappings pair $r$ with $r$ and either rename both leaves or keep one leaf and delete and insert the other, at cost 2.

## Known algorithms

| algorithm | time | space | trees |
|---|---|---|---|
| Tai (1979) | $O(n_1 n_2 d_1^2 d_2^2)$ | $O(n_1 n_2 d_1^2 d_2^2)$ | ordered, depths $d_t$ |
| [Zhang-Shasha](/zhang-shasha-algorithm/) (1989) | $O(n_1 n_2 \min(d_1, \ell_1) \min(d_2, \ell_2))$, so $O(n^4)$ | $O(n_1 n_2)$ | ordered, $\ell_t$ leaves |
| Klein (1998) | $O(n^3 \log n)$ | $O(n^2)$ | ordered |
| Demaine, Mozes, Rossman, Weimann (2009) | $O(n^2 m (1 + \log(n/m)))$, so $O(n^3)$ | $O(nm)$ | ordered, sizes $m \le n$ |
| RTED, APTED (Pawlik and Augsten) | at most that of the above, chosen per input | $O(nm)$ | ordered |
| exhaustive search over mappings | exponential | | unordered |

Tai's bounds are as summarized by Bille. All the ordered algorithms are dynamic programs over sub-forests that differ in how they choose which root to remove next, a choice called a *path strategy* or a *decomposition*.

## Bounds

- **Upper bound.** $O(n^3)$ time for ordered trees with any costs, by Demaine et al.
- **Decomposition lower bound.** Every algorithm of the decomposition kind, which includes Zhang-Shasha, Klein and Demaine et al., needs $\Omega(n^2 m (1 + \log(n/m)))$ subproblems on some pairs of trees, so $O(n^3)$ is optimal for this class.
- **Conditional lower bound.** Bringmann, Gawrychowski, Mozes and Weimann showed that a truly subcubic algorithm for weighted tree edit distance, with an alphabet of size $\Theta(n)$, would give a truly subcubic algorithm for all-pairs shortest paths. For unit costs, faster algorithms are known.
- **String lower bound.** Since paths give the string edit distance, a truly subquadratic algorithm would refute SETH, see [the edit distance lower bound](/edit-distance-seth-lower-bound/).
- **Unordered trees.** NP-complete, so no polynomial algorithm unless P = NP.

## Reductions

- **String edit distance reduces to tree edit distance.** Turn each string into a path, or into a root whose children are the letters in order. A mapping of two such trees is an order-preserving matching of the letters, which is an alignment of the strings.
- **Tree edit distance to forests.** The dynamic programs solve the more general forest edit distance, and the tree case is the special case of one tree per forest.
- **Isomorphism.** $\delta(T_1, T_2) = 0$ under unit costs if and only if the two ordered trees are equal, with equal labels; so [tree isomorphism](/tree-isomorphism/) of ordered trees is the special case of distance zero, though it has a much faster linear-time test.

## Applications

- **Structured documents.** Comparing two versions of an XML or HTML document, and computing a change script between them.
- **Programs.** Comparing abstract syntax trees for code differencing, clone detection and grading.
- **Biology.** Comparing RNA secondary structures, which are trees, and phylogenetic or glycan trees.
- **Natural language.** Comparing parse trees and evaluating parsers.
- **Images and shapes.** Comparing shape skeletons and shock graphs represented as trees.

## References
