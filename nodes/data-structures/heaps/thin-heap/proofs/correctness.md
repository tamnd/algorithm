---
title: The thin-heap operations keep the thin-heap invariants
proves: [correctness]
status: full
---

We use the invariants of the page. (1) Heap order: each key is at least the key of its parent. (2) The children of each node $x$, in list order, have the ranks $c, c - 1, \ldots, 0$ for $c = r(x) - 1$ ($x$ normal) or $c = r(x) - 2$ ($x$ thin), where an empty list has $c = -1$. (3) Every root is normal. Write $r(\mathrm{NIL}) = -1$.

**Lemma 1 (rank bound).** A node of rank $k$ has at least $F_{k+1}$ nodes in its subtree, where $F_1 = F_2 = 1$ and $F_{j+2} = F_{j+1} + F_j$. So in a heap of $n$ items every rank is at most $\log_\varphi n + 1$.

*Proof.* By induction on $k$. For $k \le 1$ the subtree has at least $1 = F_{k+1}$ node. For $k \ge 2$, by (2) the node has children of ranks at least $k - 2, k - 3, \ldots, 0$, so by induction its subtree has at least $1 + \sum_{i=0}^{k-2} F_{i+1} = 1 + (F_{k+1} - 1) = F_{k+1}$ nodes, using $\sum_{j=1}^{m} F_j = F_{m+2} - 1$. Since $F_{k+1} \ge \varphi^{k-1}$, $n \ge \varphi^{k-1}$ and $k \le \log_\varphi n + 1$. $\square$

**Lemma 2 (link).** If $x$ and $y$ are normal roots of rank $k$ that satisfy (1) and (2) in their trees, LINK returns a normal root of rank $k + 1$ whose tree satisfies (1) and (2).

*Proof.* Line L1 makes $x.key \le y.key$, so heap order holds at the new edge. The children of $x$ had the ranks $k - 1, \ldots, 0$; now $y$, of rank $k$, comes first, so they are $k, k - 1, \ldots, 0$ and $x$ is normal with rank $k + 1$. The node $y$ keeps its children and its rank, and it was normal. $\square$

**Theorem 1 (insert, meld, delete-min).** These operations keep (1) to (3), and delete-min returns a smallest key.

*Proof.* Insert adds a root of rank 0 with no child, which is normal. Meld only joins two lists of roots. In delete-min, the minimum root $z$ holds a smallest key: by heap order, every key is at least the key of its root, and $H.min$ is the smallest root. The children of $z$ become roots. A thin child $c$ gets the rank $r(c.child) + 1$ at line L4. This changes no child list, and it makes $c$ normal, so (2) and (3) hold for all roots. Heap order has no parent condition for a root. Lemma 2 shows that each link keeps (1) to (3). At the end the smallest root is found again. $\square$

**The defect of decrease-key.** Say the heap has a *sibling defect at $y$* if $y$ is not a root, (1) holds, and (2) and (3) hold except that the node after $y$ in its sibling list has rank $r(y) - 2$ (with rank $-1$ if $y$ is the last child). Say it has a *parent defect at $y$* if (1) holds, and (2) and (3) hold except at $y$, whose children have the ranks $c, c - 1, \ldots, 0$ with $r(y) - c \in \{2, 3\}$. A parent defect with $r(y) - c = 2$ is not a defect at all when $y$ is not a root: $y$ is then thin.

**Lemma 3 (the hole left by a cut).** Suppose (1) to (3) hold except for one defect that is not at $u$ or below $u$, and let $u$ be a non-root node with rank $i$ and left neighbor $y$, that is, its parent if $u$ is a first child and its left sibling otherwise. After $u$ and its subtree are cut out of the list and $u$ becomes a root with rank $r(u.child) + 1$, the heap has a sibling defect at $y$ if $y$ was the left sibling of $u$, and a parent defect at $y$ if $y$ was the parent of $u$. The subtree of $u$ satisfies (1) to (3).

*Proof.* The node after $u$ in the list had rank $i - 1$, or $u$ was the last child and $i = 0$. If $y$ is the left sibling, its rank is $i + 1$, and after the cut its next node has rank $i - 1 = r(y) - 2$: a sibling defect. If $y$ is the parent, its first child had rank $i$ and $r(y) \in \{i + 1, i + 2\}$; now the first child has rank $c = i - 1$, so $r(y) - c \in \{2, 3\}$: a parent defect. All other lists are unchanged. The new rank of $u$ makes it normal and does not change its children. Heap order inside the subtree of $u$ holds as before, and $u$ has no parent. $\square$

**Lemma 4 (one step of the loop).** If the heap has a sibling or parent defect at $y$ before an iteration of lines L11 to L16, then after it either (1) to (3) hold, or there is a defect of one of the two kinds at the old left neighbor of $y$.

*Proof.* Heap order is not changed by a change of rank. The only move of a node from one parent to another is line L15, which moves the first child $w$ of $y$ to be a sibling of $y$, so the new parent of $w$ is the parent $p$ of $y$, and $w.key \ge y.key \ge p.key$.

*Parent defect, line L12.* If $y$ is a root, setting $r(y) = c + 1$ makes $y$ normal, and as a root it has no sibling condition. All invariants hold.

*Parent defect, line L13.* If $y$ is not a root and $r(y) = c + 2$, then $y$ is thin, which (2) allows. The rank of $y$ did not change, so its own list position is correct. All invariants hold.

*Parent defect, line L14.* If $r(y) = c + 3$ and $y$ is not a root, line L14 cuts $y$ and makes it a normal root. By Lemma 3, applied with $u = y$, the heap has a defect at the old left neighbor of $y$.

*Sibling defect, line L15.* Let $k = r(y)$. If $y$ is normal, its first child $w$ has rank $k - 1$, and its next child has rank $k - 2$. Line L15 moves $w$ right after $y$. Now the list of $y$'s parent reads $\ldots, k, k - 1, k - 2, \ldots$, which is correct, and the children of $y$ start at rank $k - 2$, so $y$ is thin, which is allowed for a non-root. All invariants hold.

*Sibling defect, line L16.* If $y$ is thin, its first child has rank $k - 2$. Line L16 sets $r(y) = k - 1$, so $y$ is normal, and its next node, of rank $k - 2$, is now correct. In the list that holds $y$, $y$ had rank $k$ and now has rank $k - 1$. If $y$ has a left sibling $z$, then $r(z) = k + 1 = r(y) + 2$: a sibling defect at $z$. If $y$ is a first child of $z$, then the first child of $z$ now has rank $k - 1$, one less than before, and $r(z) - (k - 1) \in \{2, 3\}$: a parent defect at $z$. $\square$

**Theorem 2 (decrease-key).** DECREASE-KEY keeps (1) to (3), and the heap holds the same items with the new key at $x$.

*Proof.* If $x$ is a root, lowering its key keeps heap order, because a root has no parent, and line L8 updates $H.min$. Otherwise line L9 cuts $x$. Inside its subtree, every key was at least the old key of $x$, which is at least the new key, so heap order holds there, and $x$ is a root. By Lemma 3 there is now one defect at the old left neighbor $y$. By Lemma 4, each iteration either removes the defect, and the procedure returns, or moves it to the left neighbor of $y$. Moving to a left sibling or to a parent goes along a path that cannot repeat a node: each move increases the rank of the current node or goes up a level, and there are finitely many nodes. The move from a parent defect at a root always returns at line L12. So the loop ends, and when it ends, (1) to (3) hold. No node is removed or created. $\blacksquare$
