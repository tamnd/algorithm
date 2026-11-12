---
title: Midpoint rooting returns the midpoint of a longest leaf-to-leaf path
proves: [correctness]
status: full
---

Let $U$ be an unrooted tree with at least two leaves, in which no vertex has degree 2, and with edge lengths $\ell(e) \ge 0$. Treat $U$ as a metric space: the points are the vertices and the points inside the edges, and $d(p, q)$ is the length of the unique path from $p$ to $q$. Let $D$ be the largest distance between two leaves. MIDPOINT-ROOT is claimed to return the point $m$ at distance $D/2$ from both ends of a longest leaf-to-leaf path, and, when all lengths are positive, this point is the same for every longest path.

## Part 1: a farthest point can be taken to be a leaf

**Claim.** For every point $p$ there is a leaf $y$ with $d(p, y) = \max_q d(p, q)$, where $q$ runs over all vertices.

*Proof.* Let $q$ be a vertex at the largest distance from $p$. If $q$ is not a leaf, it has degree at least 3, so it has a neighbour $q'$ that is not on the path from $p$ to $q$. Then $d(p, q') = d(p, q) + \ell(\{q, q'\}) \ge d(p, q)$, so $q'$ is also farthest. Repeat from $q'$. Each step moves away from $p$ along a path that never returns, so the steps end at a leaf after finitely many moves. $\square$

So lines L2 and L4, which look only at leaves, find the largest distance over all vertices.

## Part 2: the double sweep finds a longest path

**Claim.** The leaf $b$ of line L2 is an end of a longest leaf-to-leaf path, and $d(b, c) = D$ for the leaf $c$ of line L4.

*Proof.* Let $y, z$ be leaves with $d(y, z) = D$, let $P$ be the path from $y$ to $z$, and let $a$ be the start leaf of line L1. Since $b$ is farthest from $a$, $d(a, b) \ge d(a, y)$ and $d(a, b) \ge d(a, z)$. Let $p$ be the point of $P$ closest to $b$, so that the path $Q$ from $b$ to $p$ meets $P$ only at $p$, and $d(b, y) = d(b, p) + d(p, y)$ and $d(b, z) = d(b, p) + d(p, z)$. We show that $d(b, p) \ge \min(d(p, y), d(p, z))$.

*Case 1: the path from $a$ to $b$ does not pass through $p$.* Then $b \ne p$, and $a$ lies in the same part as $b$ when $p$ is removed from the tree. That part touches $p$ only through the last edge of $Q$, so the path from $a$ to $p$ ends along $Q$ and meets $Q$ first at a point $g \ne p$. So $d(a, z) = d(a, g) + d(g, p) + d(p, z)$ and $d(a, b) = d(a, g) + d(g, b)$. From $d(a, b) \ge d(a, z)$ we get $d(g, b) \ge d(g, p) + d(p, z)$, and so $d(b, p) = d(b, g) + d(g, p) \ge d(p, z)$.

*Case 2: the path from $a$ to $b$ passes through $p$.* Then $d(a, b) = d(a, p) + d(p, b)$. Let $q$ be the point of $P$ closest to $a$, and let $w \in \{y, z\}$ be an end of $P$ such that $p$ lies between $q$ and $w$ on $P$ (if $q = p$, either end). The path from $a$ to $w$ runs from $a$ to $q$, then along $P$ through $p$ to $w$, so $d(a, w) = d(a, p) + d(p, w)$. From $d(a, b) \ge d(a, w)$ we get $d(p, b) \ge d(p, w) \ge \min(d(p, y), d(p, z))$.

Now let $z'$ be the end of $P$ with the smaller distance to $p$ and $y'$ the other end. Then $d(b, y') = d(b, p) + d(p, y') \ge d(p, z') + d(p, y') = D$. So $b$ has a leaf at distance $D$, and line L4 finds a leaf $c$ with $d(b, c) = D$. $\square$

## Part 3: the walk stops at the midpoint

Line L3 roots $U$ at $b$, so $\operatorname{parent}[x]$ is the next vertex on the path from $x$ to $b$, and $db[x] = d(b, x)$. Write the path from $c$ to $b$ as $c = x_0, x_1, \ldots, x_k = b$. Then $db[x_0] = D \ge db[x_1] \ge \cdots \ge db[x_k] = 0$, since each step removes an edge of length $\ge 0$.

**Claim.** If $c \ne b$ and $D > 0$, the loop of line L7 stops with $x = x_j$, where $j$ is the smallest index with $db[x_{j+1}] \le h$, and then the point $m$ on the edge $\{x_{j+1}, x_j\}$ at distance $h - db[x_{j+1}]$ from $u = x_{j+1}$ has $d(b, m) = d(c, m) = D/2$.

*Proof.* The loop moves from $x_i$ to $x_{i+1}$ exactly while $db[x_{i+1}] > h$. Since $db[x_k] = 0 < h$, it stops at the first $j$ with $db[x_{j+1}] \le h$, and the loop condition held for every earlier index, so $db[x_j] > h$ (for $j = 0$, $db[x_0] = D > h$). So $db[u] \le h < db[x_j] = db[u] + \ell(\{u, x_j\})$, and $0 \le t = h - db[u] < \ell(\{u, x_j\})$. The point $m$ at distance $t$ from $u$ on this edge has $d(b, m) = db[u] + t = h = D/2$, and $d(c, m) = D - D/2 = D/2$ because $m$ is on the path from $b$ to $c$. $\square$

If $c = b$, then $D = 0$ and every leaf is at distance 0 from $b$; the implementation returns $b$ itself. If $D > 0$ and $t = 0$, the point $m$ is the vertex $u$.

## Part 4: the midpoint is the same for every longest path

**Claim.** Every leaf $y$ has $d(m, y) \le D/2$. If all lengths are positive, $m$ is the midpoint of every longest leaf-to-leaf path.

*Proof.* Let $g$ be the point where the path from $m$ to $y$ leaves the path $P$ from $b$ to $c$. Then $g$ is on the part of $P$ from $m$ to $c$ or on the part from $m$ to $b$; say from $m$ to $c$. The path from $b$ to $y$ runs along $P$ from $b$ through $m$ to $g$ and then to $y$, so $d(b, y) = d(b, m) + d(m, y) = D/2 + d(m, y)$. Since $d(b, y) \le D$, $d(m, y) \le D/2$. The other case is the same with $c$ in place of $b$.

Now let $y, z$ be leaves with $d(y, z) = D$. Then $D = d(y, z) \le d(y, m) + d(m, z) \le D/2 + D/2 = D$, so equality holds throughout: $d(y, m) = d(m, z) = D/2$ and $d(y, z) = d(y, m) + d(m, z)$. In a tree with positive lengths, $d(y, z) = d(y, m) + d(m, z)$ holds only if $m$ is on the path from $y$ to $z$, because otherwise the paths from $y$ and from $z$ to $m$ share the part from the point closest to $m$ on the $y$ to $z$ path, which has positive length. So $m$ is the point of the $y$ to $z$ path at distance $D/2$ from both ends. $\square$

So the returned point does not depend on the start leaf $a$ or on the choice among tied leaves in lines L2 and L4. Also, every point $p$ has $\max(d(p, b), d(p, c)) \ge D/2$, so $m$ minimizes the largest distance to a leaf: $m$ is the center of $U$.

## Part 5: exactness on ultrametric trees

**Claim.** Let $T$ be a rooted tree with root $\rho$, positive edge lengths, every inner vertex with at least two children, and every leaf at distance $H$ from $\rho$. Let $U$ be the unrooted tree from $T$ (if $\rho$ has two children, its two edges become one edge through the point $\rho$). Then MIDPOINT-ROOT on $U$ returns the point $\rho$.

*Proof.* Let $\delta(v) = d(\rho, v)$. For leaves $x \ne y$, the path from $x$ to $y$ goes up to $v = \operatorname{lca}(x, y)$ and down, so $d(x, y) = (H - \delta(v)) + (H - \delta(v)) = 2(H - \delta(v))$. This is at most $2H$, with equality if and only if $v = \rho$, since $\delta(v) > 0$ for $v \ne \rho$. The root $\rho$ has at least two children, so there are leaves in two different subtrees of $\rho$, and $D = 2H$. A path between two such leaves passes through $\rho$ at distance $H = D/2$ from both ends, so $\rho$ is its midpoint. By Part 4, $m = \rho$. $\square$

## Conclusion

By Parts 1 and 2, lines L1 to L5 compute $D$ and the ends $b$, $c$ of a longest leaf-to-leaf path. By Part 3, lines L6 to L8 return the point of that path at distance $D/2$ from both ends. By Part 4, with positive lengths this point is the same for every longest path and is the center of the tree, and by Part 5 it is the true root when the tree is ultrametric.
