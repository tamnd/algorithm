---
tag: Y3PPPP
kind: algorithm
slug: zhang-shasha-algorithm
name: Zhang-Shasha algorithm
aliases:
- Zhang-Shasha tree edit distance
area: graphs/tree-algorithms
level: research
summary: Compute tree edit distance in polynomial time via keyroot-based dynamic programming.
solves: [tree-edit-distance]
model: word-ram
complexity:
  vars: {n: the larger of the two tree sizes}
  time: {worst: O(n^4), balanced: O(n^2 log^2 n), best: Θ(n^2)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false}
prereqs: [tree-edit-distance, postorder-traversal, edit-distance, wagner-fischer-algorithm]
see_also: [graph-edit-distance, weighted-edit-distance, tree-isomorphism, ordered-tree-generation, rooted-tree, tree-traversal, edit-distance-seth-lower-bound, ahu-algorithm]
sources:
  - paper: doi:10.1137/0218082
    title: Kaizhong Zhang and Dennis Shasha, Simple fast algorithms for the editing distance between trees and related problems, SIAM Journal on Computing 18(6), 1245 to 1262 (1989)
    locator: the forest distance recurrences, the keyroots, the main algorithm and its time bound with the collapsed depth
  - paper: doi:10.1145/322139.322143
    title: Kuo-Chung Tai, The tree-to-tree correction problem, Journal of the ACM 26(3), 422 to 433 (1979)
    locator: the definition of the edit operations and of mappings, and the first polynomial algorithm
  - paper: doi:10.1016/j.tcs.2004.12.030
    title: Philip Bille, A survey on tree edit distance and related problems, Theoretical Computer Science 337(1 to 3), 217 to 239 (2005)
    locator: Section 3 (the classical algorithms of Tai, Zhang and Shasha, and Klein) and the decomposition view of the recursion
  - paper: doi:10.1145/1644015.1644017
    title: Erik D. Demaine, Shay Mozes, Benjamin Rossman and Oren Weimann, An optimal decomposition algorithm for tree edit distance, ACM Transactions on Algorithms 6(1), Article 2 (2009)
    locator: the O(n^3) algorithm and the lower bound for decomposition algorithms
---

The Zhang-Shasha algorithm computes the [tree edit distance](/tree-edit-distance/) between two ordered, labelled, rooted trees: the least total cost of node deletions, insertions and renames that turn one tree into the other. It is a dynamic program over forests. It numbers the nodes in [postorder](/postorder-traversal/), so that the descendants of a node together with the nodes to their left form an interval, and it fills one forest table for each pair of *keyroots*, the nodes that are the root or have a left sibling. Its time is $O(n_1 n_2 \min(d_1, \ell_1) \min(d_2, \ell_2))$ for trees with $n_t$ nodes, depth $d_t$ and $\ell_t$ leaves, which is $O(n^2 \log^2 n)$ for balanced trees and $O(n^4)$ in the worst case, and its space is $O(n_1 n_2)$.

## In plain words

Two documents are stored as trees, for example two versions of a web page or of a program. You want to know how different they are. You can delete a node, and its children move up to take its place. You can insert a node above some neighbouring children. You can rename a node. Each change has a cost, and the distance is the cheapest way to make the trees equal.

The algorithm works like the table for the edit distance of two strings, but on parts of trees. It looks at the rightmost node of each part and asks three questions: delete it, insert the other one, or match the two and solve their subtrees separately. To avoid solving the same parts again and again, it only starts a new table at special nodes, the ones that are first in a new branch.

## The problem

The input is two ordered rooted trees $T_1$ and $T_2$ with $n_1, n_2 \ge 1$ nodes. Tree $T_t$ has the nodes $0, \ldots, n_t - 1$, a root, and for each node the list of its children from left to right, and a label on each node. The trees are not weighted. A cost function $\gamma$ gives the cost $\gamma(a \to \varepsilon)$ of deleting a node with label $a$, $\gamma(\varepsilon \to b)$ of inserting one with label $b$, and $\gamma(a \to b)$ of renaming $a$ to $b$; the default is $1$, $1$, and $[a \ne b]$. The output is the tree edit distance $\delta(T_1, T_2)$.

A *mapping* from $T_1$ to $T_2$ is a set of pairs $(v, w)$ that uses each node at most once and keeps both the ancestor relation and the left-to-right relation between any two pairs. Its cost is the sum of $\gamma(v \to w)$ over its pairs, plus the deletion costs of the unmapped nodes of $T_1$ and the insertion costs of the unmapped nodes of $T_2$. The algorithm returns the least cost of a mapping. When $\gamma$ is a metric, this equals the least cost of a sequence of edit operations, as Tai and Zhang and Shasha show.

## The algorithm

Number the nodes of each tree $1, \ldots, n$ in postorder, and let $l(i)$ be the leftmost leaf of the subtree of $i$. For $i' \le i$, the nodes $l(i), \ldots, i'$ form a forest, written $T[l(i)..i']$, and $T[l(i')..i']$ is the subtree of $i'$. A *keyroot* is a node $i$ such that no node $j > i$ has $l(j) = l(i)$: the root, and each node with a left sibling. $\mathit{td}[i][j]$ is the distance between the subtrees of $i$ and $j$, and $\mathit{fd}$ is the forest table, with $\mathit{fd}[l(i) - 1][l(j) - 1]$ standing for two empty forests.

```pseudo id=main
ZHANG-SHASHA(T1, T2)
L1  number both trees in postorder; compute l1 and l2
L2  K1 ← the keyroots of T1, K2 ← the keyroots of T2, both in increasing order
L3  for each i in K1 do
L4      for each j in K2 do
L5          fd[l1(i) − 1][l2(j) − 1] ← 0
L6          for i1 ← l1(i) to i do fd[i1][l2(j) − 1] ← fd[i1 − 1][l2(j) − 1] + γ(i1 → ε)
L7          for j1 ← l2(j) to j do fd[l1(i) − 1][j1] ← fd[l1(i) − 1][j1 − 1] + γ(ε → j1)
L8          for i1 ← l1(i) to i do
L9              for j1 ← l2(j) to j do
L10                 if l1(i1) = l1(i) and l2(j1) = l2(j) then           ▷ two whole trees
L11                     fd[i1][j1] ← min(fd[i1 − 1][j1] + γ(i1 → ε), fd[i1][j1 − 1] + γ(ε → j1), fd[i1 − 1][j1 − 1] + γ(i1 → j1))
L12                     td[i1][j1] ← fd[i1][j1]
L13                 else fd[i1][j1] ← min(fd[i1 − 1][j1] + γ(i1 → ε), fd[i1][j1 − 1] + γ(ε → j1), fd[l1(i1) − 1][l2(j1) − 1] + td[i1][j1])
L14 return td[n1][n2]
```

The entry $\mathit{fd}[i_1][j_1]$ is the distance between the forests $T_1[l_1(i)..i_1]$ and $T_2[l_2(j)..j_1]$, whose rightmost roots are $i_1$ and $j_1$. The three terms delete $i_1$, insert $j_1$, or map $i_1$ to $j_1$; in the last case the subtrees of $i_1$ and $j_1$ are matched with each other, and the forests to their left are matched with each other. When both forests are whole trees (line L10), the subtrees without their roots are $T_1[l_1(i)..i_1 - 1]$ and $T_2[l_2(j)..j_1 - 1]$, and the result is a new subtree distance. Otherwise line L13 uses $\mathit{td}[i_1][j_1]$, which an earlier pair of keyroots has already computed.

## Example

Take $T_1 = f(d(a, c(b)), e)$ and $T_2 = f(c(d(a, b)), e)$, in the notation label(children). In postorder, $T_1$ is $a, b, c, d, e, f$ with $l_1 = (1, 2, 2, 1, 5, 1)$, and $T_2$ is $a, b, d, c, e, f$ with $l_2 = (1, 2, 1, 1, 5, 1)$.

```
     T1:      f                T2:      f
            /   \                     /   \
           d     e                   c     e
          / \                        |
         a   c                       d
             |                      / \
             b                     a   b
```

The keyroots are $K_1 = \{3, 5, 6\}$ (the nodes $c$, $e$, $f$) and $K_2 = \{2, 5, 6\}$ (the nodes $b$, $e$, $f$). The nine pairs fill the table $\mathit{td}$, with unit costs:

| $\mathit{td}$ | $a$ | $b$ | $d$ | $c$ | $e$ | $f$ |
|---|---|---|---|---|---|---|
| $a$ | 0 | 1 | 2 | 3 | 1 | 5 |
| $b$ | 1 | 0 | 2 | 3 | 1 | 5 |
| $c$ | 2 | 1 | 2 | 2 | 2 | 4 |
| $d$ | 3 | 3 | 1 | 2 | 4 | 4 |
| $e$ | 1 | 1 | 3 | 4 | 0 | 5 |
| $f$ | 5 | 5 | 3 | 3 | 5 | 2 |

For example, $\mathit{td}[d][d] = 1$: the subtree $d(a, c(b))$ becomes $d(a, b)$ by deleting $c$. The answer is $\mathit{td}[f][f] = 2$: delete $c$ in $T_1$, which gives $f(d(a, b), e)$, then insert $c$ above $d$. The optimal mapping pairs $a, b, d, e, f$ with the nodes of the same label.

The small cases: two single nodes have distance $0$ or the rename cost. A path of $n$ nodes and a single node with the same label as one of them have distance $n - 1$, and the algorithm has one keyroot per tree and fills an $n \times 1$ table. A star with centre $x$ and $k$ leaves labelled $x$ against a path of $k + 1$ nodes labelled $x$ has distance $2(k - 1)$ for $k \ge 1$: a mapping can keep only a root and one leaf of the star.

## Correctness

The full proof is in the [proof page](proofs/correctness). It rests on the forest recurrence: for forests $F$ and $G$ with rightmost roots $v$ and $w$,

$$\delta(F, G) = \min\big(\delta(F - v, G) + \gamma(v \to \varepsilon),\ \delta(F, G - w) + \gamma(\varepsilon \to w),\ \delta(F - T(v), G - T(w)) + \delta(T(v), T(w))\big),$$

and when $F = T(v)$ and $G = T(w)$ are whole trees, the last term is $\delta(T(v) - v, T(w) - w) + \gamma(v \to w)$. The proof shows that in an optimal mapping in which both $v$ and $w$ are mapped, they are mapped to each other, and then the mapping splits into a part inside the two subtrees and a part on the forests to their left. The second part of the proof shows that line L13 only reads entries of $\mathit{td}$ that an earlier pair of keyroots has written, because the highest node with the leftmost leaf of $i_1$ is a keyroot that comes before $i$ unless $l(i_1) = l(i)$.

## Complexity

- **Per pair.** The pair $(i, j)$ of keyroots costs $\Theta(|T_1(i)| \cdot |T_2(j)|)$ steps for the double loop of lines L8 and L9, where $T(i)$ is the subtree of $i$.
- **Sum.** So the time is $\Theta\big(\sum_{i \in K_1} |T_1(i)| \cdot \sum_{j \in K_2} |T_2(j)|\big)$. Each node lies in the subtree of at most $\min(d + 1, \ell)$ keyroots: its keyroot ancestors, and at most one keyroot per leaf, since the keyroots have distinct leftmost leaves. So $\sum_{i \in K} |T(i)| \le n \min(d + 1, \ell)$, which Zhang and Shasha call the collapsed depth bound.
- **Bounds.** The time is $O(n_1 n_2 \min(d_1, \ell_1) \min(d_2, \ell_2))$. For balanced trees, $d = O(\log n)$, which gives $O(n^2 \log^2 n)$. For a path, $\ell = 1$, which gives $\Theta(n_1 n_2)$. A caterpillar with $n/2$ leaves and depth $n/2$ gives $\Theta(n^4)$ when both trees are such.
- **Space.** The tables $\mathit{td}$ and $\mathit{fd}$ have $(n_1 + 1)(n_2 + 1)$ entries each, $\Theta(n_1 n_2)$ words. The postorder numbering uses an explicit stack, so the depth of a tree does not limit the program.

## Properties

- **Deterministic and exact.** It returns the exact distance for any non-negative costs, with no rounding when the costs are integers.
- **Ordered trees only.** The left-to-right order of the children matters. For unordered trees the problem is NP-hard, see [tree edit distance](/tree-edit-distance/).
- **Symmetric.** Swapping the trees and the roles of deletion and insertion gives the same value.
- **All subtree pairs.** As a by-product, $\mathit{td}$ holds the distance between every subtree of $T_1$ and every subtree of $T_2$.
- **Strings as a special case.** For two paths, the recurrence becomes the [Wagner-Fischer](/wagner-fischer-algorithm/) table of the [edit distance](/edit-distance/) of the label sequences, read from the leaf upward.

## Variants and improvements

- **Rightmost paths.** The same method with the rightmost leaf and reverse postorder. Which side is better depends on the shapes of the trees.
- **Klein's algorithm.** Klein chooses, at each step, to remove the root of the larger subtree from the left or the right, guided by a heavy path decomposition of one tree. This gives $O(n^3 \log n)$ time.
- **Demaine, Mozes, Rossman and Weimann.** A decomposition by heavy paths in both trees gives $O(n^2 m (1 + \log (n/m)))$ time for trees of sizes $m \le n$, which is $O(n^3)$, and is optimal among decomposition algorithms.
- **RTED and APTED.** Pawlik and Augsten choose the best path strategy for the given pair of trees, and are never worse than the classical algorithms. They are widely used in practice.
- **Unit costs.** For unit costs and distance at most $k$, there are faster algorithms whose time depends on $k$, and Mao gave a truly subcubic algorithm for unweighted tree edit distance.

## When to use it

Use the Zhang-Shasha algorithm for ordered labelled trees of up to a few thousand nodes, such as XML documents, parse trees, RNA secondary structures or abstract syntax trees, when the exact distance is wanted and the trees are bushy or balanced, where its time is close to $n^2$. It is simple, needs $O(n^2)$ space, and gives all subtree distances. For large deep trees with many leaves, use a cubic algorithm such as Demaine et al. or RTED.

## Pitfalls

- **Wrong keyroots.** A keyroot is the highest node with a given leftmost leaf. Using all nodes is still correct but slower; missing a keyroot makes line L13 read a value of $\mathit{td}$ that was never written.
- **Table offsets.** The forest table is indexed from $l(i) - 1$. Indices that start at $0$ in code must be shifted by one, as in the empty forest at $\mathit{fd}[l(i) - 1][l(j) - 1]$.
- **The rename term on forests.** In line L13, the third term uses $\mathit{td}[i_1][j_1]$ and the forests to the left of the two subtrees, not $\mathit{fd}[i_1 - 1][j_1 - 1]$. Mixing up lines L11 and L13 gives wrong values.
- **Costs that are not a metric.** If a rename costs more than a deletion plus an insertion, the mapping distance is still what the algorithm computes, but it can differ from the cost of the best edit sequence.
- **Deep recursion.** A recursive postorder fails on a path of $10^5$ nodes in Python. Number the nodes with an explicit stack.

## Implementations

## History

Tai defined the tree-to-tree correction problem in 1979, with the edit operations and the notion of a mapping, and gave the first polynomial algorithm. Zhang and Shasha published their simpler and faster algorithm in 1989, with the keyroots and the bound by the collapsed depth. Klein improved the worst case to $O(n^3 \log n)$ in 1998, and Demaine, Mozes, Rossman and Weimann reached $O(n^3)$, with a matching lower bound for decomposition strategies. Bille's survey of 2005 compares these methods.

## References
