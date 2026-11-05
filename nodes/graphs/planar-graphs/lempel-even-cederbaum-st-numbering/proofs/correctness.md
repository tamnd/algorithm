---
title: Correctness of the st-numbering algorithm
proves: [correctness, termination]
status: full
---

**Setting.** $G$ is a finite undirected graph with $n \ge 2$ vertices, $s \ne t$, and the edge $st$ is treated as present. $T$ is the DFS tree of line L1, rooted at $s$. Since the search from $s$ follows $st$ first and the whole search from $t$ ends before $s$ looks at another edge, $t$ is a child of $s$, and every vertex reached later from $s$ is another child of $s$. $\mathrm{pre}(v)$ is the preorder number and $\mathrm{low}(v)$ is the vertex of smallest preorder among $v$, the descendants of $v$, and the ends of back edges from them.

**Termination and cost.** The search, the check and the loop each take finitely many steps, $O(n + m)$ in total.

## Line L2 is the right test

**Lemma 1.** Line L2 fails if and only if $G + st$ is disconnected or has a cut vertex. If it does not fail, then $t$ is the only child of $s$, and $\mathrm{low}(v)$ is a proper ancestor of $p(v)$ for every $v \notin \{s, t\}$.

*Proof.* If some vertex is not reached, $G + st$ is disconnected. Otherwise $T$ spans $G + st$, and by the standard characterization of cut vertices with low points (see the articulation point pages): the root $s$ is a cut vertex if and only if it has at least two children, and a non-root $u$ is a cut vertex if and only if it has a child $v$ with $\mathrm{pre}(\mathrm{low}(v)) \ge \mathrm{pre}(u)$. If $s$ has a second child $c$, then $p(c) = s$ and $\mathrm{low}(c) \ge \mathrm{pre}(s) = 0$ is detected by line L2. So line L2 checks exactly both conditions. When it passes, $\mathrm{pre}(\mathrm{low}(v)) < \mathrm{pre}(p(v))$, and $\mathrm{low}(v)$ is an ancestor of $v$ (the end of a back edge from the subtree of $v$ is an ancestor of $v$ in a DFS tree of an undirected graph, or lies in the subtree), so it is a proper ancestor of $p(v)$. $\square$

When $G + st$ is not 2-connected, no st-numbering exists. Suppose one exists, and let $u$ be any vertex. From every vertex $x \ne u$ there is a path of increasing numbers to $t$ and a path of decreasing numbers to $s$, and these two paths meet only in $x$, so at least one of them avoids $u$ (if $u = s$ or $u = t$, take the other one). So every vertex other than $u$ reaches $s$ or $t$ in $G + st - u$, and if neither $s$ nor $t$ is $u$, the edge $st$ joins them. So $G + st - u$ is connected for every $u$, and $G + st$ is connected; with $n \ge 3$ this means 2-connected, and for $n = 2$ the graph $G + st$ is $K_2$. So failing is the right answer.

From now on assume that line L2 passes.

## The list

The loop processes vertices in preorder, so $p(v)$ is in $L$ when $v$ is inserted. Insertions never change the relative order of vertices already in $L$.

**Lemma 2 (no jumping).** When $v$ is inserted next to $p(v)$, for every vertex $x \ne p(v)$ in $L$, the vertices $v$ and $p(v)$ lie on the same side of $x$, and they stay so forever.

*Proof.* $v$ is placed between $p(v)$ and its neighbour in $L$ on one side, so no vertex lies between $v$ and $p(v)$ at that moment. Relative order is never changed later. $\square$

For a vertex $x$ that has a child in $L$, let $c_x$ be the child of $x$ inserted most recently.

**Lemma 3 (sides of subtrees).** At every moment, for every $x$ with a child in $L$: all vertices of the subtree of $c_x$ that are in $L$ lie before $x$ if $\mathrm{sign}(x) = +$, and after $x$ if $\mathrm{sign}(x) = -$.

*Proof.* When $c_x$ is inserted, line L6 or L8 sets $\mathrm{sign}(x)$ to $+$ if $c_x$ goes before $x$ and to $-$ if it goes after, and the subtree of $c_x$ in $L$ is $\{c_x\}$. Afterwards, $\mathrm{sign}(x)$ changes only when a new child of $x$ is inserted, which replaces $c_x$. Every later vertex $v$ of the subtree of $c_x$ has its parent in that subtree, and $p(v) \ne x$; by Lemma 2 it lands on the same side of $x$ as $p(v)$, which by induction is the side of $c_x$. $\square$

**Lemma 4 (the low point is opposite the parent).** For every $v \notin \{s, t\}$, after its insertion, $\mathrm{low}(v)$ lies on the other side of $v$ from $p(v)$.

*Proof.* Let $w = \mathrm{low}(v)$, a proper ancestor of $p(v)$ by Lemma 1. Then $p(v)$ is in the subtree of the child of $w$ on the path to $v$, and this child is $c_w$ at the time $v$ is inserted, because in preorder the subtree of a child is processed completely before the next child. By Lemma 3, if $\mathrm{sign}(w) = -$ then $p(v)$ lies after $w$; line L6 puts $v$ directly before $p(v)$, so $w$ lies before $v$ and $p(v)$ after it. If $\mathrm{sign}(w) = +$, symmetrically $p(v)$ lies before $w$, line L8 puts $v$ directly after $p(v)$, and $w$ lies after $v$. $\square$

**Lemma 5.** $s$ is first and $t$ is last in the final list.

*Proof.* A vertex is inserted before $p(v)$ or after $p(v)$, and $p(v) \ne s$ for $v \notin \{s, t\}$ by Lemma 1, so nothing is inserted before $s$. A vertex is inserted after $t$ only if $p(v) = t$ and $\mathrm{sign}(\mathrm{low}(v)) = +$. Then $\mathrm{low}(v)$ is a proper ancestor of $t$, so it is $s$. The sign of $s$ is set to $-$ at line L3 and changes only when a child of $s$ is inserted, which never happens since $t$ is its only child. So nothing is inserted after $t$. $\square$

## Main theorem

**Theorem.** If line L2 passes, the numbering of line L9 is an st-numbering of $G + st$, and every vertex $v \notin \{s, t\}$ has neighbours in $G$ on both sides.

*Proof.* By Lemma 5, $\mathrm{num}(s) = 1$ and $\mathrm{num}(t) = n$. Let $v \notin \{s, t\}$. The parent $p(v)$ is a neighbour of $v$ in $G$ (the only tree edge not in $G$ might be $st$, and $v \ne t$). We find a neighbour on the other side, which by Lemma 4 is the side of $w = \mathrm{low}(v)$.

If $v$ has a back edge to $w$, then $w$ is such a neighbour.

Otherwise $w$ is reached from a proper descendant of $v$, so there is a child $c$ of $v$ with $\mathrm{low}(c) = w$. Suppose $\mathrm{sign}(w) = -$ when $v$ is inserted; then $v$ goes before $p(v)$ and $w$ lies before $v$. Between the insertions of $v$ and $c$ the loop inserts only descendants of $v$ (preorder), whose parents are $v$ or descendants of $v$; none of them is $w$, because $w$ is a proper ancestor of $p(v)$. So $\mathrm{sign}(w)$ is still $-$ when $c$ is inserted, and line L6 puts $c$ directly before $p(c) = v$. So $c$ lies on the side of $w$, opposite $p(v)$. The case $\mathrm{sign}(w) = +$ is symmetric. In both cases $c$ is a neighbour of $v$ in $G$ on the other side.

So every $v \notin \{s, t\}$ has a neighbour with a smaller number and one with a larger number. $\blacksquare$
