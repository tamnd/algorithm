---
title: The two-dimensional range tree query reports exactly the points in the box in O(log^2 n + k) time
proves: [correctness, termination, complexity]
status: full
---

**Setting.** $T$ is a leaf-based binary tree whose leaves, from left to right, hold the points of $P$ in the order of $(p_x, p_y, \text{index})$, at positions $0, \dots, n - 1$, $n \ge 1$. Every internal node has two children, and the leaves of the subtree of a node $v$ form a contiguous block of positions, written $\beta(v)$. $A(v)$ is the list of the points of $\beta(v)$ sorted by $p_y$. The query box is $Q = [x_1, x_2] \times [y_1, y_2]$, closed. The height of $T$ is $H = \lceil \log_2 n \rceil$.

**Claim.** 2D-RANGE-QUERY terminates, reports each point of $P \cap Q$ exactly once and no other point, and runs in $O(H^2 + k)$ time.

**Step 1 (the leaf range).** The $x$-coordinates of the leaves do not decrease from left to right. So the positions with $x_1 \le p_x \le x_2$ form a block $[lo, hi]$, where $lo$ is the first position with $p_x \ge x_1$ and $hi$ the last with $p_x \le x_2$. If $lo > hi$ the block is empty and $P \cap Q = \emptyset$, and line L1 returns.

**Step 2 (the split node).** The root's block contains both $lo$ and $hi$. At an internal node whose block contains both, they are either in the same child's block, and the descent continues there, or in different children. So line L2 stops at the deepest node $v_s$ whose block contains both, after at most $H$ steps. If $v_s$ is a leaf, then $lo = hi$ is its position and line L3 tests its point, which is right by Step 1. Otherwise $lo \in \beta(\mathrm{lc}(v_s))$ and $hi \in \beta(\mathrm{rc}(v_s))$, since $lo \le hi$ and the left block precedes the right block.

**Step 3 (the left path).** Let $u_0 = \mathrm{lc}(v_s), u_1, \dots, u_t$ be the nodes visited by lines L5 to L7, where $u_{i+1}$ is the child of $u_i$ that contains $lo$ and $u_t$ is the leaf $lo$. Let $R_i$ be the set of positions in $\beta(\mathrm{lc}(v_s))$ that are $> lo$ and lie in $\beta(u_0) \setminus \beta(u_i)$. We show by induction on $i$ that the blocks queried at line L6 so far are disjoint and their union is $R_i$. For $i = 0$ the union is empty and $R_0 = \emptyset$. At step $i$: if $u_{i+1} = \mathrm{lc}(u_i)$, the right child's block consists of positions after $\beta(\mathrm{lc}(u_i)) \ni lo$, so all of them are $> lo$; line L6 queries exactly this block, and $R_{i+1} = R_i \cup \beta(\mathrm{rc}(u_i))$, a disjoint union. If $u_{i+1} = \mathrm{rc}(u_i)$, the left child's block consists of positions before $lo$, so $R_{i+1} = R_i$, and nothing is queried at line L7. At the end, $\beta(u_t) = \{lo\}$, so $R_t$ is the set of positions of $\beta(\mathrm{lc}(v_s))$ that are $> lo$.

Every position in $R_t$ is $> lo$ and, being in the left child of $v_s$, $< hi$. So every point queried on the left path lies in $[lo, hi]$, and the leaf $lo$ is tested at line L8.

**Step 4 (the right path).** By the mirror argument, the blocks queried on the path to $hi$ are disjoint, their union is the set of positions of $\beta(\mathrm{rc}(v_s))$ that are $< hi$, all of which are $> lo$, and the leaf $hi$ is tested at line L10.

**Step 5 (partition).** The positions of $[lo, hi]$ are: $lo$; the positions of $\beta(\mathrm{lc}(v_s))$ after $lo$; the positions of $\beta(\mathrm{rc}(v_s))$ before $hi$; and $hi$. These four sets are disjoint and, since $\beta(\mathrm{lc}(v_s))$ and $\beta(\mathrm{rc}(v_s))$ are consecutive blocks with $lo$ in the first and $hi$ in the second, their union is $[lo, hi]$. By Steps 3 and 4, each position of $[lo, hi]$ is handled exactly once: tested as an end leaf, or included in exactly one queried block.

**Step 6 (the $y$-test).** For a queried block $\beta(v)$, $A(v)$ holds exactly its points sorted by $p_y$, so the points with $y_1 \le p_y \le y_2$ form the slice between the first index with $p_y \ge y_1$ and the first index with $p_y > y_2$, which 1D-QUERY reports. Together with Steps 1 and 5, the query reports each point with $x_1 \le p_x \le x_2$ and $y_1 \le p_y \le y_2$ exactly once, and no other point.

**Step 7 (termination and time).** Each loop step moves to a child, so each path ends at a leaf after at most $H$ steps. Line L6 and its mirror run at most once per step, so there are at most $2H$ one-dimensional queries. Each does two binary searches on an array of at most $n$ entries, $O(\log n)$ time, plus $O(1)$ per reported point. Every point is reported once, so the total is $O(H + 2H \log n + k) = O(\log^2 n + k)$; a counting query adds slice lengths and takes $O(\log^2 n)$. $\blacksquare$
