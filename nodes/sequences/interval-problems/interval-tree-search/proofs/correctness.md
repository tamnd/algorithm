---
title: Interval tree search reports exactly the matches and expands at most (k + 1) h nodes
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. $T$ is a binary search tree of intervals $\langle l, r \rangle$ whose in-order sequence is sorted by left end, so every interval in the left subtree of a node $x$ has $l \le x.l$ and every interval in its right subtree has $l \ge x.l$. Each node has $x.\mathit{max}$ equal to the largest right end in its subtree, and $\mathrm{nil}.\mathit{max} = -\infty$. The test $\mathrm{reach}$ is upward closed, so $\mathrm{reach}(r)$ and $r \le r'$ give $\mathrm{reach}(r')$; the test $\mathrm{start}$ is downward closed, so $\mathrm{start}(l)$ and $l' \le l$ give $\mathrm{start}(l')$. An interval *matches* when $\mathrm{reach}(r)$ and $\mathrm{start}(l)$. The height $h$ is the number of nodes on a longest root-to-leaf path.

**Lemma 1 (pruning by max).** If $\mathrm{reach}(x.\mathit{max})$ fails, no interval below $x$ matches.

*Proof.* Each right end $r$ below $x$ has $r \le x.\mathit{max}$. If $\mathrm{reach}(r)$ held, upward closure would give $\mathrm{reach}(x.\mathit{max})$. $\square$

**Lemma 2 (pruning by order).** If $\mathrm{start}(x.l)$ fails, then $x$ and every interval of its right subtree fail $\mathrm{start}$.

*Proof.* Each such interval has $l \ge x.l$. If $\mathrm{start}(l)$ held, downward closure would give $\mathrm{start}(x.l)$. $\square$

**Theorem 1 (REPORT).** REPORT$(x, \mathrm{reach}, \mathrm{start}, out)$ appends exactly the matching intervals below $x$, each once, in in-order, and terminates.

*Proof.* By induction on the number of nodes below $x$. Each call either returns at line L1 or makes calls only on the two children, which have fewer nodes, so the recursion terminates. If $x = \mathrm{nil}$ nothing is appended, which is right. If line L1 returns because $\mathrm{reach}(x.\mathit{max})$ fails, nothing matches below $x$ by Lemma 1. Otherwise line L2 appends the matches of the left subtree, by induction. If line L3 returns, then $x$ and its right subtree have no match by Lemma 2. Otherwise $\mathrm{start}(x.l)$ holds, so $x$ matches if and only if $\mathrm{reach}(x.r)$, the test of line L4, and line L5 appends the matches of the right subtree by induction. The left subtree, $x$ and the right subtree are disjoint and appended in in-order. $\square$

**Theorem 2 (SEARCH).** SEARCH returns a matching interval if one exists and nil otherwise, after at most $h$ passes of the loop.

*Proof.* Invariant: if some interval of $T$ matches, then one lies in the subtree of $x$, where the subtree of nil is empty. It holds with $x$ the root. Suppose it holds and the loop body runs, so $x$ does not match.

*Line L8 goes left.* Then $\mathrm{reach}(x.\mathit{left}.\mathit{max})$ holds, so the left subtree has an interval $\langle l', r' \rangle$ with $r' = x.\mathit{left}.\mathit{max}$ and $\mathrm{reach}(r')$. If no interval of the left subtree matches, this one fails $\mathrm{start}(l')$. Then $x$ and the intervals of the right subtree have $l \ge l'$ and fail $\mathrm{start}$ by downward closure, so nothing below $x$ matches; by the invariant nothing in $T$ matches, and the invariant holds for the left child. If some interval of the left subtree matches, it holds as well.

*Line L8 goes right.* Then the left subtree is empty or $\mathrm{reach}(x.\mathit{left}.\mathit{max})$ fails, and by Lemma 1 nothing in it matches; $x$ does not match. So any match below $x$ is in the right subtree.

Each pass moves one level down, so there are at most $h$ passes. If the loop stops at a node, the test of line L7 says that it matches. If it stops at nil, the invariant says that nothing matches. $\square$

**Theorem 3 (cost of REPORT).** Suppose REPORT$(T.\mathit{root})$ outputs $k$ intervals. Call a node *expanded* if a call on it passes line L1. Then at most $(k + 1) h$ nodes are expanded, and at most $\min(2 (k + 1) h, 2 n) + 1$ calls are made.

*Proof.* Let $f$ be the first node in in-order whose interval fails $\mathrm{start}$, if there is one. Since $\mathrm{start}$ is downward closed and the in-order sequence is sorted by left end, the nodes that pass $\mathrm{start}$ are exactly the nodes before $f$ in in-order, a prefix.

Let $v$ be expanded. Then $\mathrm{reach}(v.\mathit{max})$ holds, so some node $w$ below $v$, possibly $v$ itself, has $\mathrm{reach}(w.r)$.

*Case 1: $\mathrm{start}(w.l)$ holds.* Then $w$ matches. By Theorem 1 applied to the call on $v$, $w$ is output, so $v$ is an ancestor of an output, or the output itself.

*Case 2: $\mathrm{start}(w.l)$ fails.* Then $f$ exists, and $f$ is $w$ or comes before $w$ in in-order. We show that $f$ lies below $v$. The nodes below $v$ form a contiguous block of the in-order sequence, and $w$ is in it. If $v$ is on the leftmost path from the root, the block is a prefix of the in-order sequence, and it contains $f$, which is at or before $w$. Otherwise let $u$ be the lowest ancestor of $v$ such that $v$ is in the right subtree of $u$. Then $u$ is the node just before the block in in-order. The call on the right child of $u$ was made at line L5, so line L3 passed at $u$, and $\mathrm{start}(u.l)$ holds. So $u$ is before $f$, and $f$, which is at or before $w$, is after $u$: it lies in the block. In both cases $v$ is an ancestor of $f$ or $f$ itself.

Each node has at most $h$ ancestors including itself. So at most $k h$ nodes fall in Case 1 and at most $h$ in Case 2, which gives at most $(k + 1) h$ expanded nodes. No node is called twice, so at most $n$ are expanded. Each call is the root call or is made by an expanded node, which makes at most two calls, so there are at most $2 \min((k + 1) h, n) + 1$ calls, and each call does $O(1)$ work besides its calls. $\blacksquare$
