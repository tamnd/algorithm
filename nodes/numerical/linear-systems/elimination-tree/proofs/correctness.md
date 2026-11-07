---
title: Correctness of the elimination tree algorithms
proves: [correctness, termination]
status: full
---

Structural model: $l_{ij} \ne 0$ means structurally nonzero. Column $j$ of $L$ has its nonzeros exactly at the neighbours $i > j$ of $j$ in the elimination graph $G_j$, where $G_1 = G$ and $G_{j+1}$ is obtained from $G_j$ by deleting $j$ and joining all its neighbours pairwise (the Schur complement pattern).

**Lemma 1 (fill paths).** For $u, v \ge j$, $u \ne v$, the edge $\{u, v\}$ is in $G_j$ if and only if $G$ has a path from $u$ to $v$ whose interior vertices are all smaller than $j$. Hence for $i > j$, $l_{ij} \ne 0$ if and only if $G$ has an $i$ to $j$ path with interior vertices smaller than $j$.

*Proof.* Induction on $j$; for $j = 1$ the paths have no interior and the claim is the definition of $G$. Suppose it holds for $j$. An edge $\{u, v\}$ with $u, v > j$ is in $G_{j+1}$ if it was in $G_j$ or if both $u$ and $v$ are neighbours of $j$ in $G_j$. By the hypothesis the first case gives a path with interior below $j$, and the second gives two paths $u \to j$ and $j \to v$ with interiors below $j$, whose concatenation (shortened to a simple path) has interior vertices at most $j$. Conversely, take a simple $u$ to $v$ path with interior below $j + 1$. If it avoids $j$ its interior is below $j$ and $\{u, v\} \in G_j$, so also in $G_{j+1}$. Otherwise it passes $j$ once, and the two pieces show that $u$ and $v$ are neighbours of $j$ in $G_j$, so they are joined in $G_{j+1}$. $\square$

**Lemma 2.** If $i > p > j$ and $l_{ij} \ne 0$, $l_{pj} \ne 0$, then $l_{ip} \ne 0$.

*Proof.* $i$ and $p$ are neighbours of $j$ in $G_j$, so they are adjacent in $G_{j+1}$; edges between surviving vertices are never removed, so they are adjacent in $G_p$, and $l_{ip} \ne 0$. $\square$

**Theorem 3 (ancestor property).** If $l_{ij} \ne 0$ and $i > j$, then $i$ is an ancestor of $j$.

*Proof.* Induction on $i - j$. Let $p = \mathrm{parent}(j)$, which exists and satisfies $p \le i$ by its definition as a minimum. If $p = i$ we are done. Otherwise $j < p < i$ and Lemma 2 gives $l_{ip} \ne 0$ with $i - p < i - j$, so $i$ is an ancestor of $p$, hence of $j$. $\square$

**Lemma 4.** If $i < j$ and $G$ has a path from $i$ to $j$ whose interior vertices are all smaller than $j$, then $j$ is an ancestor of $i$.

*Proof.* Induction on the path length. Let $w$ be the largest vertex of the path other than $j$; then $w \ge i$. The subpath from $w$ to $j$ has interior vertices smaller than $w$, so $l_{jw} \ne 0$ by Lemma 1 and $j$ is an ancestor of $w$ by Theorem 3. If $w = i$ we are done. Otherwise the subpath from $i$ to $w$ is shorter and has interior vertices below $w$, so $w$ is an ancestor of $i$ by induction. $\square$

**Theorem 5 (row subtrees).** For each $k$, $\{ j < k : l_{kj} \ne 0 \} = \bigcup_{i < k,\, a_{ki} \ne 0} \{ \text{nodes on the tree path from } i \text{ to } k \} \setminus \{k\}$.

*Proof.* If $a_{ki} \ne 0$ then $l_{ki} \ne 0$ and $k$ is an ancestor of $i$ (Theorem 3), so the path exists. For $\supseteq$, walk up the path from $i$: $l_{ki} \ne 0$, and if $l_{kj} \ne 0$ with $p = \mathrm{parent}(j) < k$, then $l_{pj} \ne 0$ and Lemma 2 gives $l_{kp} \ne 0$. For $\subseteq$, let $l_{kj} \ne 0$. By Lemma 1 there is a path $k, w_1, \ldots, w_s = j$ with $w_1, \ldots, w_{s-1} < j$. Put $i = w_1$, so $a_{ki} \ne 0$ and $i \le j$. If $i < j$, the path $w_1, \ldots, w_s$ satisfies Lemma 4, so $j$ is an ancestor of $i$. The ancestors of $i$ form a chain containing $j$ and $k$, and $j < k$, so $j$ lies on the path from $i$ to $k$. $\square$

**Theorem 6 (ETREE).** Let $F_k$ be the forest on $\{1, \ldots, k\}$ obtained from the elimination tree by deleting the edges to parents larger than $k$. After iteration $k$ of line L1: for $v \le k$, $\mathrm{parent}[v]$ is the true parent if it is at most $k$ and $0$ otherwise; and $\mathrm{anc}[v] = 0$ if $v$ is a root of $F_k$, while otherwise $\mathrm{anc}[v]$ is a proper ancestor of $v$ with $\mathrm{anc}[v] \le k$.

*Proof.* Induction on $k$; before iteration $1$ there is nothing to show. In iteration $k$, the nodes whose parent is $k$ are, by definition, the $j < k$ with $l_{kj} \ne 0$ and $l_{tj} = 0$ for $j < t < k$, that is the roots of $F_{k-1}$ in the row pattern of $k$. By Theorem 5 a root $r$ of $F_{k-1}$ is in that pattern exactly when its subtree in $F_{k-1}$ contains some $i$ with $a_{ki} \ne 0$ (if $r$ is on the path from such an $i$, $i$ is in its subtree; conversely $r$ and $k$ are both ancestors of $i$ and $r < k$, so $r$ is on the path).

Consider the climb of lines L4 to L7 from such an $i$. Every value it follows is an anc pointer, hence a proper ancestor, so the visited nodes increase strictly and the loop terminates. By the hypothesis, nodes that are not roots of $F_{k-1}$ have pointers into the same tree of $F_{k-1}$, unless they were reset to $k$ earlier in this iteration. If the climb meets no such node it ends at the root $r$ of the tree of $i$, where $\mathrm{anc}[r] = 0$, and line L6 sets $\mathrm{parent}[r] = k$, correctly. If it meets a node whose pointer is already $k$, that node was passed by an earlier climb of this iteration, which continued to the same root $r$ and set its parent. No other parents are set, since line L6 acts only at roots of $F_{k-1}$ reached from such an $i$, and those all have parent $k$. Every node passed is in a tree now hanging from $k$ and receives $\mathrm{anc} = k$, a proper ancestor; nodes not passed keep valid pointers, since adding the node $k$ above some roots keeps every ancestor an ancestor; and $\mathrm{anc}[k] = 0$ with $k$ a root of $F_k$. $\square$

**Theorem 7 (ROW-PATTERN).** It returns the row pattern of $k$, each node once, and clears its marks.

*Proof.* Only $k$ and output nodes are marked. A climb from $i$ with $a_{ki} \ne 0$ follows the tree path towards $k$, which is an ancestor of $i$ and is marked, so it stops, at the first marked node. The nodes it appends are on the path from $i$ to $k$, and all unmarked nodes on that path below the stopping node are appended. A marked node on the path other than $k$ was output by an earlier climb, which also passed everything above it up to $k$ or to another marked node, and so on up to $k$. So the union of the outputs is the union in Theorem 5, without repetition. Line L15 clears exactly what was marked. $\square$

**Theorem 8 (equivalent orderings).** Let $\sigma$ be an ordering of $1, \ldots, n$ in which every node comes before its parent (a postorder is one). Eliminating $G$ in the order $\sigma$ gives the same filled graph $G^+$ (the graph of $L + L^T$) as the original order. Hence the column counts are permuted by $\sigma$ and the new tree is the old one relabelled.

*Proof.* Every neighbour $w$ of $v$ in $G^+$ is comparable with $v$ in the tree (Theorem 3), so the neighbours of $v$ that come after $v$ in $\sigma$ are its ancestors, which are its neighbours larger than $v$ in the original order: the pattern of column $v$ of $L$. These form a clique of $G^+$, because the elimination game made them one. So $\sigma$ is a perfect elimination ordering of $G^+$, and eliminating $G^+$ in order $\sigma$ adds nothing. Fill under $\sigma$ is given by the paths of Lemma 1 with $\sigma$ in place of the numbering; a path in $G$ is a path in $G^+ \supseteq G$, so the filled graph of $G$ under $\sigma$ is contained in that of $G^+$, which is $G^+$.

Conversely let $\{i, j\} \in G^+$ with $j < i$, so $j$ is a descendant of $i$ and $\sigma$ puts $j$ before $i$. Lemma 1 gives a path from $i$ to $j$ in $G$ whose interior vertices are smaller than $j$; for each interior $w$, the piece from $w$ to $j$ satisfies Lemma 4, so $w$ is a descendant of $j$ and comes before $j$ in $\sigma$. This is a fill path in the order $\sigma$, so $\{i, j\}$ is in the filled graph under $\sigma$. The parent of a node is its smallest higher neighbour in $G^+$, and the higher neighbours are the same set in both orders; as they form a chain of ancestors, the smallest is the same node. $\square$

**Termination.** Every loop is over a finite list except the climbs, which strictly increase the current node (Theorems 6 and 7), and the depth first search, which emits each node once. $\blacksquare$
