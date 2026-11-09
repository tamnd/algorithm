---
title: The kd-tree search takes O(n) time in the worst case, and this is tight
proves: [time.worst, space.extra]
status: full
---

**Upper bound.** SEARCH is called on each node at most once, because each call recurses only into the two children of its node, and on at most $n + 1$ nil children of visited nodes. Each call on a node does $O(d)$ work: one squared distance in line L6 and $O(1)$ comparisons in lines L7 to L10. So a query costs $O(dn)$, which is $O(n)$ for fixed $d$.

**The bound is tight.** Let $P$ be the $n$ distinct lattice points on the circle $x^2 + y^2 = R^2$, in any kd-tree, and $q = (0, 0)$, so $\|q - r\|^2 = R^2$ for every $r \in P$. After the first node, $best.d2 = R^2$. At a node with point $p$ and axis $a$, line L10 skips the far side only if $\mathrm{diff}^2 = p[a]^2 \ge R^2$, that is, $p[a] = \pm R$, so $p$ is one of $(\pm R, 0)$ or $(0, \pm R)$ and $a$ is the axis in which it is extreme. Take $p = (R, 0)$ with axis $x$: $\mathrm{diff} = -R < 0$, so the far side is the right subtree, whose points have $x \ge R$. The only point of $P$ with $x \ge R$ is $(R, 0)$ itself, stored at this node, so the skipped subtree is empty. The other three cases are symmetric. So no point is ever skipped, and the search visits all $n$ nodes: $\Omega(n)$ time. The test with $R = 5525$ confirms that every node is visited.

**Space.** Besides the tree, the search stores $best$ and one frame per active call. The active calls form a root-to-node path, so the extra space is $O(h)$ for a tree of height $h$, which is $O(\log n)$ for a tree built by medians, since each subtree then has at most half the points of its parent's subtree. $\blacksquare$
