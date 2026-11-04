---
title: Finger search and updates in a level-linked (2,4)-tree are correct
proves: [correctness, invariant, termination]
status: full
---

Write $(v.lo, v.hi]$ for the range of node $v$, with $-\infty$ and $+\infty$ allowed. The invariant has three parts.

- **(F1) Shape.** All bottom nodes are at the same depth. A non-root bottom node has 1 to 3 keys; an internal node has 2 to 4 children and one separator fewer; the root may be a bottom node with 0 to 3 keys.
- **(F2) Ranges.** The root has range $(-\infty, +\infty]$. An internal node $v$ with children $c_0, \ldots, c_{m-1}$ and separators $s_1 < \cdots < s_{m-1}$ has $c_j.lo = s_j$ and $c_j.hi = s_{j+1}$, where $s_0 = v.lo$ and $s_m = v.hi$. The keys of a bottom node are increasing and lie in its range.
- **(F3) Levels.** For each depth, $next$ and $prev$ link the nodes of that depth in left-to-right order.

**Lemma 1.** Under (F1) to (F3), the ranges of the nodes of one depth are disjoint and their union is $(-\infty, +\infty]$, and the left-to-right order of the nodes is the order of their ranges. The range of a node contains the ranges of its descendants.

*Proof.* By induction on the depth. At depth 0 it is the root. If it holds at depth $t$, (F2) splits each range at depth $t$ into the ranges of the children, in order, so it holds at depth $t + 1$. $\square$

**Lemma 2 (DESCEND).** If $v.lo < k \le v.hi$, DESCEND$(v, k)$ returns the bottom node below $v$ whose range holds $k$.

*Proof.* Line L8 picks the least $j$ with $k \le s_{j+1}$ (with $s_m = v.hi \ge k$, so $j$ exists). Then $k > s_j$: for $j = 0$ because $s_0 = v.lo < k$, and for $j > 0$ by the choice of $j$. So $c_j$ holds $k$ in its range, and the loop keeps the condition. The depth grows each round, so the loop ends at a bottom node, and by Lemma 1 it is the only bottom node whose range holds $k$. $\square$

**Lemma 3 (FINGER-SEARCH).** FINGER-SEARCH$(f, k)$ ends and returns the bottom node whose range holds $k$.

*Proof.* Each round of lines L2 to L5 either stops (line L4 or the test of line L2) at a node whose range holds $k$, or moves to the parent. The root's range holds $k$, so the climb ends after at most the height of the tree. Then Lemma 2 applies. $\square$

So a search reports $k$ present exactly when $k$ is a key of the returned bottom node, because by (F2) and Lemma 1, a key $k$ can only be in the bottom node whose range holds it.

**Insert.** If $k$ is already in $b$, nothing changes. Else line L12 puts $k$ into $b$ in sorted order, and $k$ lies in the range of $b$ by Lemma 3, so (F2) holds. Only the size condition of (F1) can fail, and only at $v$. Line L15 splits $v$:

- a bottom node with keys $a_1 < a_2 < a_3 < a_4$ becomes $v = (a_1, a_2)$ and $u = (a_3, a_4)$, with $s = a_2$; the ranges $(v.lo, a_2]$ and $(a_2, v.hi]$ hold the keys;
- an internal node with children $c_0, \ldots, c_4$ and separators $s_1, \ldots, s_4$ becomes $v$ with $c_0, c_1, c_2$ and $s_1, s_2$, and $u$ with $c_3, c_4$ and $s_4$, with $s = s_3$; the children keep their ranges, which satisfy (F2) in $v$ and $u$, since $c_2.hi = s_3 = v.hi$ and $c_3.lo = s_3 = u.lo$.

Linking $u$ just after $v$ keeps (F3). Line L17 puts $u$ after $v$ in the parent with $s$ between them, so the parent's separators become $\ldots, v.lo, s, v.hi, \ldots$ around $v$ and $u$, which is (F2) for the parent; they stay increasing because $v.lo < s < v.hi$. The parent has one more child and may now be overfull, which the next round handles. A split of the root (line L16) makes a new root with range $(-\infty, +\infty]$ and children $v$, $u$, one level higher; all bottom nodes stay at one depth. Each round goes one level up, so the loop ends. Line L19 returns the half of the split bottom node that holds $k$.

**Delete.** If $k$ is not in $b$, nothing changes. Else removing $k$ keeps (F2) at $b$. Only the minimum size can fail, at a non-root node $v$ with parent $p$ and adjacent sibling $w$; say $w$ is left of $v$ (the other case is the mirror image), with separator $t$ between them in $p$, so $w.hi = t = v.lo$.

- **Share, bottom.** The largest key $x$ of $w$ moves into $v$; the new separator is $t' = $ the new largest key of $w$, with $w.hi = v.lo = t'$. The keys of $w$ are $\le t'$, and the keys of $v$, now $x$ and the old ones, are $> t'$, since $x$ was the largest key of $w$ and the old keys of $v$ are $> t \ge x$. So (F2) holds.
- **Share, internal.** The last child $c$ of $w$, with range $(t', t]$, where $t'$ is the last separator of $w$, becomes the first child of $v$; $t$ moves down as the first separator of $v$, and $t'$ goes up into $p$ in the place of $t$, with $w.hi = v.lo = t'$. Each child keeps its range, and the ranges match the new separators. (F3) does not change: $c$ stays at its place in its level.
- **Merge.** $v$ joins $w$: the keys (bottom) or the children with $t$ between the two lists of separators (internal) go into $w$, with $w.hi = $ old $v.hi$; $t$ leaves $p$; $v$ is unlinked from its level. The ranges of the children do not change and match the new separators of $w$, the keys of $v$ lie in its old range, which is now part of the range of $w$, and the level order of the other nodes stays. The parent has one child fewer and may now be underfull, which the next round handles.

The sizes after a share or merge are in the bounds of (F1), because a share takes from a sibling above the minimum, and a merge joins a node below the minimum with a sibling at the minimum (0 + 1 keys or 1 + 2 children). If the root is left with one child, its range is the root's range $(-\infty, +\infty]$ by (F2), so making it the root keeps (F2), and all bottom nodes stay at one depth. Each round goes one level up, so the loop ends. The bottom node returned is $b$ or the node $b$ merged into; in both cases its range contains the old range of $b$, which holds $k$. $\blacksquare$
