---
title: The priority search tree query reports exactly the points of the three-sided range in O(log n + k) time
proves: [correctness, termination, complexity]
status: full
---

**Setting.** $T$ is a priority search tree on $n \ge 1$ points: the positions $0, \dots, n - 1$ follow the order of $(p_x, p_y, \text{index})$, node $v$ covers a block $\beta(v)$, the children split it in the middle, and the height is $H = \lceil \log_2 n \rceil$. Its invariants (proved on the [priority search tree](/priority-search-tree/) page) are: (1) each position is stored at exactly one node, whose block contains it; (2) along every root path the keys $(p_y, p_x, j)$ of the stored points increase; (3) the children of an empty node are empty. The query is $[x_1, x_2] \times (-\infty, y_0]$ with $lo \le hi$ from line L1.

**Claim.** PST-QUERY reports each point with $x_1 \le p_x \le x_2$ and $p_y \le y_0$ exactly once, and no other point, in $O(\log n + k)$ time.

**Step 1 (three kinds of nodes).** Let $\Pi$ be the set of nodes on the search paths to the leaves of $lo$ and $hi$. Every node $w \notin \Pi$ has a highest ancestor-or-self $u \notin \Pi$, whose parent $v$ is in $\Pi$. Either $v$ is below the split node on the path to $lo$, the path goes to $\mathrm{lc}(v)$, and $u = \mathrm{rc}(v)$; or the mirror case on the path to $hi$; call these *inner* subtrees. Otherwise $u$ is the child of a path node that lies on the outer side of the paths, or a child of a node above the split node off the shared path; call these *outer* subtrees.

**Step 2 (positions of the subtrees).** For an inner subtree $u = \mathrm{rc}(v)$ on the path to $lo$: $lo \in \beta(\mathrm{lc}(v))$, and $\beta(u)$ comes right after it inside $\beta(\mathrm{lc}(v_s))$, where $v_s$ is the split node, so all its positions are $> lo$ and $< hi$, since $hi \in \beta(\mathrm{rc}(v_s))$. The mirror case is symmetric. For an outer subtree, its block is a block next to a path on the side away from $[lo, hi]$, so all its positions are $< lo$ or all are $> hi$. Hence its points are all outside the $x$-range.

**Step 3 (path nodes).** Line L2 reaches every nonempty node of $\Pi$: a path stops only at an empty node, and by (3) everything below it is empty. Line L3 reports $\mathrm{pt}(v)$ exactly when its position is in $[lo, hi]$, which is $x_1 \le p_x \le x_2$ since the positions are in $x$-order, and $p_y \le y_0$.

**Step 4 (inner subtrees).** Lines L4 and L5 call REPORT-IN-SUBTREE on every inner subtree whose parent is reached, once each. In it, a node $w$ is reached and reported exactly when every node from the subtree's root down to $w$, including $w$, is nonempty and stores a point with $p_y \le y_0$. By (2), the stored points on that chain have increasing keys, so their $y$-values do not decrease toward $w$; hence the condition holds exactly when $\mathrm{pt}(w)_y \le y_0$. With Step 2, a point stored in an inner subtree is reported exactly when it is in the range.

**Step 5 (correctness).** By (1) each point is stored at one node, which is on a path (Step 3), in an inner subtree (Step 4), or in an outer subtree, whose points are not in the range (Step 2) and which the query never enters. Each node is processed once. So each point of the range is reported exactly once and no other point.

**Step 6 (time).** The paths have at most $H + 1$ nodes each and share the root, so line L2 processes at most $2H + 1$ nodes, and lines L4 and L5 start at most one walk per path node below the split node, at most $2H$ walks. In a walk, each popped node is skipped at line L8 or reported at line L9. A skipped node is either the root of its walk or a child of a reported node, and a reported node has two children, so the pops number at most $2H + 2k$. With the two binary searches of line L1, the total is $O(\log n + H + k) = O(\log n + k)$. $\blacksquare$
