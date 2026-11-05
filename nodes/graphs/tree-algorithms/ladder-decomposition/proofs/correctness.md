---
title: The ladder algorithm returns the level ancestor
proves: [correctness, termination]
status: full
---

Let the tree have vertices $0, \ldots, n - 1$, $n \ge 1$, and root $r$. Write $depth(x)$ for the number of edges from $r$ to $x$, $T_x$ for the subtree of $x$, and $h(x)$ for the number of vertices on a longest downward path from $x$, so $h(x) = 1$ for a leaf and $h(x) = 1 + \max_c h(c)$ over the children $c$ otherwise. For $0 \le d \le depth(x)$, $\mathrm{LA}(x, d)$ is the unique ancestor of $x$ at depth $d$. Lines L1 to L11 are those of the pseudocode on the page.

**Lemma 1 (heights).** After line L2, $h$ and $long$ are as defined: $long(v)$ is a child of $v$ with $h(long(v)) = h(v) - 1$, for every non-leaf $v$.

*Proof.* Reverse BFS order lists every vertex after all its children, so when $v$ is handled the values of its children are final. $\square$

**Lemma 2 (partition).** Every vertex $x$ lies on the long path of exactly one head, and the long path of a head $t$ has exactly $h(t)$ vertices, with depths $depth(t), depth(t) + 1, \ldots, depth(t) + h(t) - 1$.

*Proof.* Walk up from $x$ while the current vertex is the long child of its parent; the walk stops at a head $t$, and $x$ is on the long path of $t$. Any head whose long path contains $x$ is found by this walk, because the long path of a head goes down through long children only, and a head is not the long child of its parent, so it is unique. Along the long path, $h$ decreases by exactly 1 per step (Lemma 1) and the path ends at a leaf, where $h = 1$, so it has $h(t)$ vertices, one per depth. $\square$

**Lemma 3 (ladders).** For each head $t$ with long path $P$, $k = |P| = h(t)$, the ladder built in lines L5 and L6 is the list of the ancestors of the bottom vertex of $P$ at the depths $top, top + 1, \ldots, depth(t) + k - 1$, where $top = depth(t) - \min(k, depth(t)) = \max(0, depth(t) - h(t))$. Hence for every $x \in P$ and every $d$ with $top \le d \le depth(x)$, entry $d - top$ of the ladder is $\mathrm{LA}(x, d)$.

*Proof.* $A$ lists the $\min(k, depth(t))$ nearest proper ancestors of $t$, topmost first, which are the ancestors of $t$ at depths $top, \ldots, depth(t) - 1$; $P$ continues with one vertex per depth from $depth(t)$ down (Lemma 2), each the child of the one before. So the ladder lists one ancestor of the bottom vertex per depth, starting at depth $top$, and entry $j$ has depth $top + j$. For $x \in P$ and $d \le depth(x)$, the ancestor of the bottom vertex at depth $d$ is also the ancestor of $x$ at depth $d$, since $x$ is itself on that vertical path. $\square$

**Lemma 4 (jump pointers).** After line L7, $up[j][v]$ is the $2^j$-th ancestor of $v$ when $2^j \le depth(v)$.

*Proof.* By induction on $j$: $up[0][v]$ is the parent, and the $2^j$-th ancestor is the $2^{j-1}$-th ancestor of the $2^{j-1}$-th ancestor. When $2^j \le depth(v)$ both intermediate steps stay inside the tree, so the clamping of the root at line L1 is never used. The table has $\lceil \lg n \rceil \ge \lfloor \lg k \rfloor + 1$ levels for every $k \le n - 1$. $\square$

**Theorem.** LEVEL-ANCESTOR$(v, d)$ returns $\mathrm{LA}(v, d)$ if $0 \le d \le depth(v)$ and none otherwise, and all steps terminate.

*Proof.* Line L8 handles the invalid $d$. Let $k = depth(v) - d \ge 0$; if $k = 0$, line L9 returns $v = \mathrm{LA}(v, d)$. Otherwise let $i = \lfloor \lg k \rfloor$, so $2^i \le k < 2^{i+1}$, and $u = up[i][v]$, the ancestor of $v$ at depth $depth(v) - 2^i \ge d$ (Lemma 4). Then $\mathrm{LA}(v, d) = \mathrm{LA}(u, d)$, and $depth(u) - d = k - 2^i < 2^i$.

The path from $u$ down to $v$ has $2^i + 1$ vertices, so $h(u) \ge 2^i + 1$. Let $t$ be the head of the long path containing $u$. Since $u$ is on that path below $t$, $h(t) = h(u) + (depth(u) - depth(t)) \ge h(u)$. Now
$$depth(t) - d \le depth(u) - d < 2^i < h(u) \le h(t),$$
so $top(u) = \max(0, depth(t) - h(t)) \le d$. Also $d \le depth(u)$. By Lemma 3, entry $d - top(u)$ of the ladder of $u$ is $\mathrm{LA}(u, d) = \mathrm{LA}(v, d)$, which line L11 returns.

Termination: the BFS visits each vertex once, the walks of lines L4 and L5 have at most $k$ steps for a path of $k$ vertices, line L7 is a bounded double loop, and a query does a fixed number of steps. $\blacksquare$
