---
title: BBS outputs exactly the skyline, in order of mindist, and reads exactly the R-tree nodes whose lower corner no point dominates
proves: [correctness, termination, io.worst, time.worst]
status: full
---

We use the line numbers of the pseudocode. Smaller values are better. A point $p$ *dominates* $q$, written $p \prec q$, when $p_i \le q_i$ for every dimension $i$ and $p_i < q_i$ for some $i$. The skyline $\mathit{Sky}(P)$ of a multiset $P$ of points is the set of points of $P$ that no point of $P$ dominates. Each node $N$ of the R-tree has a minimum bounding rectangle with lower corner $\ell(N)$: every point $q$ stored below $N$ has $q \ge \ell(N)$ in every coordinate, and the corner of a child is at least the corner of its parent in every coordinate. For an entry $e$ (a node or a point) let $c(e)$ be $\ell(e)$ for a node and $e$ itself for a point, and let $\mathit{key}(e) = \sum_i c(e)_i$, its L1 distance from the origin when all values are not negative (for any values, the order is the same). An entry is *pruned* when some point of $S$ dominates $c(e)$, at line L4 or line L6.

**Lemma 1 (dominating a corner).** If $p \prec \ell(N)$, then $p$ dominates every point below $N$. If $p \prec q$, then $\mathit{key}(p) < \mathit{key}(q)$.

*Proof.* Let $q$ be below $N$. Then $p_i \le \ell(N)_i \le q_i$ for every $i$, and for the $i$ with $p_i < \ell(N)_i$ also $p_i < q_i$. For the second claim, add $p_i \le q_i$ over all $i$, with one strict inequality. $\square$

**Lemma 2 (keys do not decrease).** The keys of the popped entries form a non-decreasing sequence.

*Proof.* A child of a node has a corner at least the corner of the node in every coordinate, and a point below the node is at least its corner, so every pushed entry has a key at least the key of the entry popped in the same iteration. A min-heap that only receives keys at least the last popped key pops keys in non-decreasing order. $\square$

**Lemma 3 (what is popped before what).** Let $x$ be a point or a node, and suppose that no point of $\mathit{Sky}(P)$ ever prunes $x$ or one of its ancestors. Then $x$ is popped, and it is popped before every entry with a larger key.

*Proof.* By induction down the path from the root. The root is the first entry pushed (line L1). Suppose an ancestor $a$ of $x$ is popped. It is not pruned, so it is read, and its child $a'$ on the path is pushed unless it is pruned at line L6, which the hypothesis excludes. Once pushed, $a'$ is popped before any entry with a larger key, because the heap pops its smallest key, and $\mathit{key}(a') \le \mathit{key}(x)$. So $x$ is popped, before every entry of larger key that is popped after it is pushed, and by Lemma 2 before every entry of larger key at all. $\square$

**Lemma 4 (S holds only skyline points).** At every moment $S \subseteq \mathit{Sky}(P)$, and each point added to $S$ is added once.

*Proof.* Suppose a point $q$ is added at line L7 but some point $p \in P$ dominates $q$. Choose such a $p$ in $\mathit{Sky}(P)$: the domination order on $P$ is a strict partial order on a finite set, so the dominators of $q$ contain one that nothing dominates. We show that $p$ is in $S$ before $q$ is popped, so $q$ is pruned at line L4, a contradiction. By induction on the order of the pops, $S$ holds only skyline points before the pop of $q$, and a skyline point never dominates the corner of an ancestor of $p$ or $p$ itself, by Lemma 1, since that would make it dominate $p$. So Lemma 3 applies to $p$, and since $\mathit{key}(p) < \mathit{key}(q)$ by Lemma 1, $p$ is popped before $q$ and is added to $S$. Each point id is pushed at most once, because each node is read at most once (it is pushed once, by its parent), so it is added at most once. $\square$

**Theorem 1 (correctness).** BBS outputs every point of $\mathit{Sky}(P)$ exactly once and no other point, as a multiset of points with their duplicates, in non-decreasing order of key.

*Proof.* By Lemma 4 every output point is a skyline point, and output once. Let $p \in \mathit{Sky}(P)$. By Lemma 4 the pruning points are skyline points, and by Lemma 1 a skyline point that dominated $c(e)$ for an ancestor $e$ of $p$, or $p$ itself, would dominate $p$. So no ancestor of $p$ and not $p$ is pruned, and by Lemma 3 $p$ is popped and added. Two equal points do not dominate each other, so duplicates of a skyline point are all in the skyline and all output. The order follows from Lemma 2. Each iteration pops one entry and each entry is pushed at most once, so the loop of line L2 ends. $\blacksquare$

Since the points come out in order of key and $S$ is never changed except by adding, each output point is final when it is output: BBS is *progressive*.

**Theorem 2 (node reads).** BBS reads a node $N$, at line L5, if and only if no point of $P$ dominates $\ell(N)$, and it reads it once.

*Proof.* If no point dominates $\ell(N)$, then no point dominates the corner of an ancestor of $N$ either: a point $p \prec \ell(A)$ with $\ell(A) \le \ell(N)$ gives $p \prec \ell(N)$. So no point ever prunes $N$ or an ancestor, Lemma 3 gives that $N$ is popped, and it is not pruned, so it is read. Conversely, let some $p \in P$ dominate $\ell(N)$, and take $p \in \mathit{Sky}(P)$ as in Lemma 4. Then $\mathit{key}(p) < \mathit{key}(N)$ by the second part of Lemma 1, applied to the corner. By Lemma 3, $p$ is popped and added to $S$ before any entry of key $\mathit{key}(N)$, so when $N$ is checked at line L6 or line L4, $p \in S$ prunes it. $N$ is pushed only by its parent, which is read at most once, so $N$ is read at most once. $\blacksquare$

A node whose corner no point dominates is a node that *may contain* a skyline point, given only its rectangle: a point placed at its corner would be in the skyline. Papadias et al. call BBS I/O optimal in this sense.

**Theorem 3 (work).** Let $r$ be the number of nodes read, $C$ the node capacity, $s = |\mathit{Sky}(P)|$ and $d$ the number of dimensions. BBS pushes at most $r C + 1$ entries, uses $O(r C)$ heap space, and does $O(r C (\log(r C) + s d))$ work, with the dominance tests against $S$ done by a scan.

*Proof.* Each read node pushes at most $C$ children, and the root is pushed once. Each push and pop costs $O(\log(r C))$. Each entry is tested against $S$ at most twice (lines L6 and L4), and each test scans at most $s$ points in $O(d)$ each. $\blacksquare$
