---
title: BST deletion removes exactly the key and keeps the BST property
proves: [correctness, termination]
status: full
---

Let $T$ be a binary search tree with the strict [binary search tree property](/binary-search-tree-property/), correct parent pointers, $n$ nodes, and a map $M$ from its keys to their values. Let $k$ be a key. For a node $u$ write $\mathrm{sub}(u)$ for the nodes of its subtree.

**Claim.** TREE-DELETE$(T, k)$ stops. If $k$ is not a key of $T$, it returns false and changes nothing. Else it returns true, and afterwards the tree has the BST property, correct parent pointers, $n - 1$ nodes, and represents the map $M$ without $k$.

**Termination.** The search of line L1 and the walk of line L4 each move one level down per step, so each takes at most $h + 1$ steps. The rest has no loops.

**Not found.** By the correctness of [BST search](/bst-search/), line L1 returns NIL exactly when $k$ is not a key, and then line L2 returns false before any change.

**Lemma 1 (splice).** Let $z$ be a node with at most one child, and let $c$ be that child or NIL. Lines L7 to L11 give a tree with correct parent pointers and the nodes of the old tree except $z$, each with its key and value. Each pair $(u, w)$ where $w$ is in the left (right) subtree of $u$ in the new tree is a pair of the old tree with $w$ in the left (right) subtree of $u$. In particular, if the old tree has the BST property, so does the new one.

*Proof.* Lines L9 to L11 make the parent of $z$ (or the root field) point to $c$, and line L8 sets $c.p$ to the old parent of $z$. No other link changes, so all other parent pointers stay correct, and the nodes that stay reachable are all nodes except $z$. For the pairs, take a node $u$ and a node $w$ in its left subtree after the change (the right side is the mirror case). If $u$ is not an ancestor of $z$ in the old tree, its subtree did not change. If $u$ is an ancestor of $z$, its subtree lost only $z$, and the nodes of $\mathrm{sub}(c)$ moved up one level but stay on the same side of $u$ as $z$ was, because $\mathrm{sub}(c) \subseteq \mathrm{sub}(z)$. So $w$ was in the left subtree of $u$ in the old tree too. $\square$

**Case of at most one child.** If $z$ has at most one child at line L3, lines L4 to L6 are skipped, and Lemma 1 shows that the tree loses exactly the node of $k$. The map loses exactly $k$.

**Case of two children.** Let $z_0$ be the node of $k$, with left subtree $A$ and right subtree $B$, both non-empty. Line L4 sets $y$ to the node of $B$ with the smallest key, by the correctness of TREE-MINIMUM. Then $y.left = $ NIL, else the left child of $y$ would be a node of $B$ with a smaller key.

*$y$ is the successor.* Let $a = a(z_0)$ and $b = b(z_0)$ be the interval bounds of $z_0$ given by its ancestors, so that the keys of $T$ in $(a, b)$ are exactly the keys of $\mathrm{sub}(z_0)$. Each key of $T$ larger than $k$ and smaller than $y.key$ would be in $(a, b)$, because $a < k$ and $y.key < b$, so it would be in $\mathrm{sub}(z_0)$, and larger than $k$, so in $B$, and smaller than the minimum of $B$, which is impossible. So no key of $T$ lies strictly between $k$ and $y.key$.

*The copy keeps the order at $z_0$.* After line L5, $z_0$ holds $y.key$. Each key of $A$ is less than $k < y.key$. Each key of $B$ other than $y.key$ is greater than $y.key$. For each ancestor $u$ of $z_0$, the key $y.key$ was already in $\mathrm{sub}(z_0)$, on the same side of $u$, so the relation at $u$ still holds. Nodes inside $A$ and $B$ do not change. So, before the splice, each ancestor-descendant pair of nodes that does not involve the node $y$ satisfies the strict order condition. (The pair $(z_0, y)$ does not: both now hold $y.key$.)

*The splice.* Line L6 sets $z = y$, which has no left child. By Lemma 1, after lines L7 to L11 the node $y$ is gone, and each pair of the new tree is a pair of the tree before the splice, on the same side, that does not involve $y$. So each such pair satisfies the strict condition, and the new tree has the BST property with distinct keys. The key set is the old one without $k$: the value of $y.key$ is now at $z_0$ (line L5), and the key $k$ is no longer anywhere, because the only node that held it now holds $y.key$.

**Count.** Line L12 subtracts 1 from $T.n$, and exactly one node left the tree. $\blacksquare$
