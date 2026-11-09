---
tag: 6V8N6H
kind: definition
slug: level-sequence
name: Level sequence
aliases:
- Depth sequence of a rooted tree
- Level code
- Canonical level sequence
area: combinatorics/generating-partitions-and-trees
level: advanced
summary: The list of node depths in preorder; it uniquely encodes a rooted unlabeled tree and drives tree generation.
prereqs: [rooted-tree, preorder-traversal, lexicographic-order]
see_also: [rooted-tree-generation, beyer-hedetniemi, free-tree-generation, wright-richmond-odlyzko-mckay, dyck-word, ordered-tree-generation, tree-isomorphism, rooted-tree-representation]
sources:
  - url: https://page.math.tu-berlin.de/~felsner/SemWS17-18/Ruskey-Comb-Gen.pdf
    title: Frank Ruskey, Combinatorial Generation, working version, University of Victoria, 1995 to 2003
    locator: Section 4.6.2, Rooted Trees, Free Trees (the encoding e(T), canonic trees, Figures 4.9 and 4.10, Lemma 4.5)
  - paper: doi:10.1137/0209055
    title: Terry Beyer and Sandra Mitchell Hedetniemi, Constant time generation of rooted trees, SIAM Journal on Computing 9(4) (1980), 706 to 712
    locator: the whole paper (level sequences and their canonical form)
  - url: https://oeis.org/A000081
    title: OEIS A000081, Number of unlabeled rooted trees with n nodes
    locator: the terms 1, 1, 2, 4, 9, 20, 48, 115, 286, 719
---

The level sequence of an ordered rooted tree with $n$ nodes is the list $\ell_1, \ldots, \ell_n$ of the depths of its nodes in preorder, with the root at depth $0$. A list is a level sequence exactly when $\ell_1 = 0$ and $1 \le \ell_{i+1} \le \ell_i + 1$ for $i \ge 1$, and it determines the ordered tree. An unlabeled rooted tree has many orderings of its children, and the lexicographically largest of their level sequences is its *canonical* level sequence. Canonical level sequences are one to one with unlabeled rooted trees, and the [Beyer-Hedetniemi](/beyer-hedetniemi/) and [Wright-Richmond-Odlyzko-McKay](/wright-richmond-odlyzko-mckay/) algorithms generate trees by stepping through them.

## Definition

Let $T$ be an ordered rooted tree with $n \ge 1$ nodes, that is, a rooted tree in which the children of each node have a fixed order. Number the nodes $1, \ldots, n$ in [preorder](/preorder-traversal/), and let $\ell_i$ be the depth of node $i$, the number of edges from the root to it. The *level sequence* of $T$ is
$$e(T) = (\ell_1, \ell_2, \ldots, \ell_n).$$
Recursively, if the root has the subtrees $T_1, \ldots, T_m$ in this order, then $e(T) = 0,\ e(T_1) + 1,\ \ldots,\ e(T_m) + 1$, where $e(T_j) + 1$ adds $1$ to each entry.

**Characterization.** A sequence of integers is the level sequence of an ordered rooted tree if and only if $\ell_1 = 0$ and $1 \le \ell_{i+1} \le \ell_i + 1$ for $1 \le i < n$. The parent of node $i \ge 2$ is the last node $j < i$ with $\ell_j = \ell_i - 1$, so the sequence gives back the tree. There are $C_{n-1}$ such sequences, the [Catalan number](/catalan-numbers/), because they are in bijection with the [Dyck words](/dyck-word/) of length $2(n - 1)$.

**Canonical level sequence.** Two ordered trees are *isomorphic as rooted trees* if one becomes the other by reordering children. The *canonical level sequence* of an unlabeled rooted tree is the lexicographically largest level sequence among all its orderings. An ordered tree is *canonical* if its level sequence is canonical. Equivalently, an ordered tree is canonical if and only if, at every node, the level sequences of the child subtrees are in non-increasing lexicographic order, where a proper prefix counts as smaller.

The equivalence holds for two reasons. If two adjacent child subtrees $A, B$ have $e(A) < e(B)$, then swapping them gives a larger sequence, so a canonical tree has sorted children. And sorting the children at every node gives one sequence per isomorphism class, by induction on the height, so the sorted sequence is the largest one.

## Examples and non-examples

- **The four rooted trees with 4 nodes.** Their canonical level sequences are $0123$ (a path), $0122$, $0121$ and $0111$ (a star), in decreasing order.
- **Nine rooted trees with 5 nodes.** $01234$, $01233$, $01232$, $01231$, $01222$, $01221$, $01212$, $01211$, $01111$. The 14 ordered trees with 5 nodes fall into these nine classes; for example, $01121$, $01211$ and $01112$ are the three orderings of the tree whose root has a child with one child and two leaf children, and $01211$ is the largest.
- **A larger tree.** The sequences $0121123342$ and $0123432121$ describe isomorphic rooted trees with 10 nodes. The second is canonical: the root's children have the subtree codes $012321$, $01$ and $0$ (after subtracting $1$), in decreasing order.
- **Not canonical.** $0112$ is a level sequence, but not canonical: the root's children have the codes $0$ and $01$, and $0 < 01$. Its canonical form is $0121$.
- **Not a level sequence.** $0213$ jumps up by two levels, and $0101$ has a second node at depth $0$, which would be a second root. Both describe no rooted tree.
- **Counts.** The number of canonical level sequences of length $n$ is the number $a_n$ of unlabeled rooted trees: $1, 1, 2, 4, 9, 20, 48, 115, 286, 719$ for $n = 1, \ldots, 10$. The number of all level sequences is $C_{n-1}$: $1, 1, 2, 5, 14, 42, 132$ for $n = 1, \ldots, 7$.

## Related definitions

- **Dyck word.** For $i = 2, \ldots, n$, write $\ell_{i-1} - \ell_i + 1$ closing brackets followed by one opening bracket, then add $\ell_n$ closing brackets at the end. The result is the [Dyck word](/dyck-word/) of the ordered tree, so $0121$ gives $\texttt{(())()}$.
- **Parent array.** The array $\mathrm{par}[i]$, the position of the parent of node $i$, carries the same information. The rooted tree generators keep it next to the level sequence, so that the parent of any node is found in $O(1)$ time.
- **Rooted tree generation.** Listing the canonical level sequences of length $n$ in decreasing lexicographic order is [rooted tree generation](/rooted-tree-generation/). The successor of a canonical sequence changes its last entry larger than $1$ and repeats the subtree of that node's parent to the end.
- **Free trees.** A free tree is coded by the canonical level sequence of the tree rooted at a center, with a fixed choice between two centers; see [free tree generation](/free-tree-generation/).
- **Other canonical forms.** The [AHU algorithm](/ahu-algorithm/) and [tree hashing](/tree-hashing/) also give one code per isomorphism class and decide [tree isomorphism](/tree-isomorphism/) in linear time. The canonical level sequence is the form that is best suited to generation, because its lexicographic order has a simple successor.
- **Properties.** A canonical sequence of height $h$ starts with $0, 1, \ldots, h$, because the deepest subtree comes first at every node. Every prefix of a canonical sequence is canonical. If two consecutive entries equal $1$, then every later entry equals $1$.

## References
