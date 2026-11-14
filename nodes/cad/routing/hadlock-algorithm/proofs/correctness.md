---
title: Hadlock's search expands cells in order of detour number, and the path with the fewest detours is a shortest path
proves: [correctness, completeness, termination, running time, a-star equivalence]
status: full
---

Let $G$ be the graph of free cells, with an edge between cells that share a side. For cells $u, v$ let $\mathrm{md}(u, v)$ be the Manhattan distance of their coordinates. Let $\delta(v)$ be the length of a shortest path from $s$ to $v$ in $G$ and $L = \delta(t)$.

**Lemma 1 (each step is toward or a detour).** For neighbors $u, v$, $\mathrm{md}(v, t) - \mathrm{md}(u, t) \in \{-1, +1\}$.

*Proof.* A step changes one coordinate by 1, so it changes one term of the Manhattan distance by exactly 1, and the other term not at all. $\square$

**Lemma 2 (length identity).** Let $P$ be a path from $s$ to $v$ with $T$ toward steps and $D$ detours. Then its length is $|P| = T + D = \mathrm{md}(s, t) - \mathrm{md}(v, t) + 2D$.

*Proof.* By Lemma 1, each toward step lowers $\mathrm{md}(\cdot, t)$ by 1 and each detour raises it by 1. So $\mathrm{md}(v, t) = \mathrm{md}(s, t) - T + D$, which gives $T = \mathrm{md}(s, t) - \mathrm{md}(v, t) + D$ and $|P| = T + D$. $\square$

**Corollary 3.** For a fixed end $v$, the length of a path is $2D$ plus a constant. So a path to $v$ has the fewest detours if and only if it is a shortest path, and $\delta(v) = \mathrm{md}(s, t) - \mathrm{md}(v, t) + 2\,\mathrm{det}(v)$. In particular $L = \mathrm{md}(s, t) + 2\,\mathrm{det}(t)$. $\square$

Let $w(u, v) = 1$ if the step from $u$ to $v$ is a detour and 0 otherwise. Then $\mathrm{det}(v)$ is the least total weight of a path from $s$ to $v$ in the directed graph with these weights.

**Lemma 4 (deque order).** Consider each entry of the deque as the pair of a cell and the label it was given when it was added. At every moment the labels of the entries, from front to back, are non-decreasing, and the last is at most the first plus 1.

*Proof.* At the start the deque holds $(s, 0)$. Suppose the claim holds and line L3 removes the front entry, with label $k$, the least label in the deque. If the cell is expanded, its label is $k$, because a label only falls together with a new entry of the smaller value, and by the order that entry would have been removed first, making the cell done. Line L11 adds entries with label $k$ at the front and with label $k + 1$ at the back. All labels in the deque were in $\{k, k + 1\}$, so the order and the bound still hold. $\square$

**Lemma 5 (expanded labels are detour numbers).** When a cell $u$ is expanded on line L5, $\mathrm{det}(u)$ as stored equals its detour number, and the cells are expanded in non-decreasing order of it.

*Proof.* By Lemma 4 the labels of removed entries never decrease. This is the order of [Dijkstra's algorithm](/dijkstra/) with the non-negative weights $w$, and the usual argument applies. Suppose $u$ is the first cell expanded with a stored label $k$ larger than its detour number $k^*$. Take a path of weight $k^*$ from $s$ to $u$, and let $y$ be its first cell that is not done when $u$ is expanded, with $x$ the cell before it. The cell $x$ is done, and by the choice of $u$ its label is its detour number. When $x$ was expanded, lines L9 and L10 gave $y$ a label of at most $\mathrm{det}(x) + w(x, y) \le k^*$, because the weights on the path are non-negative, and added an entry with that label. That entry is still in the deque, so by Lemma 4 it would be removed before the entry of $u$ with label $k > k^*$, unless $y = u$, in which case the stored label of $u$ is at most $k^*$. Both cases contradict the choice of $u$. $\square$

**Theorem (shortest path).** If $t$ is reachable from $s$, the search expands $t$ and returns a path with $\mathrm{det}(t)$ detours. This path has length $L$. If $t$ is not reachable, it returns "no path".

*Proof.* Every reachable cell gets an entry, since the neighbor of an expanded cell that is not done always gets one, and every entry is removed before the deque empties. So a reachable $t$ is expanded. By Lemma 5 its label is $\mathrm{det}(t)$. The parent links satisfy $\mathrm{det}(v) = \mathrm{det}(\mathrm{parent}(v)) + w(\mathrm{parent}(v), v)$ at the time each parent is set, and parents are only set to expanded cells, whose labels no longer change. Following them from $t$ gives a path from $s$ with exactly $\mathrm{det}(t)$ detours. By Corollary 3 its length is $\mathrm{md}(s, t) + 2\,\mathrm{det}(t) = L$. If $t$ is not reachable it never gets an entry, and line L12 is reached. $\square$

**Theorem (A* view).** For a path of length $g$ from $s$ to $v$ with $D$ detours, $g + \mathrm{md}(v, t) = \mathrm{md}(s, t) + 2D$. The heuristic $h(v) = \mathrm{md}(v, t)$ is consistent on $G$, since $h(u) \le 1 + h(v)$ for neighbors. So ordering by $D$ is ordering by the A* key $g + h$.

*Proof.* The identity is Lemma 2 rearranged. Consistency is the triangle inequality of the Manhattan distance with $\mathrm{md}(u, v) = 1$. $\square$

**Lemma 6 (expanded cells are labeled by Lee).** Every cell $v \ne t$ that Hadlock expands has $\delta(v) < L$, so Lee's wave, which labels all cells with $\delta(v) < L$ before it stops, labels $v$.

*Proof.* By Lemma 5, $v$ is expanded before $t$ with $\mathrm{det}(v) \le \mathrm{det}(t)$. By Corollary 3, $\delta(v) = \mathrm{md}(s, t) - \mathrm{md}(v, t) + 2\,\mathrm{det}(v) \le L - \mathrm{md}(v, t) < L$, since $\mathrm{md}(v, t) \ge 1$ for $v \ne t$. $\square$

**Running time.** Lines L4 and L5 expand each cell at most once. Each expansion looks at 4 neighbors and adds at most 4 entries. So there are at most $4MN + 1$ entries and the time is $O(MN)$. The labels, parents and the deque take $O(MN)$ space. $\square$
