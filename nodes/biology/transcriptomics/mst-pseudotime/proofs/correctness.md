---
title: The tree is a minimum spanning tree, the backbone is a longest path, and cells on a monotone curve are ordered exactly
proves: [correctness]
status: full
---

We prove what the steps compute. Lines L1 and L2 build a minimum spanning tree of the complete graph on the cells (Theorem 1). Line L3 finds a longest path of that tree (Theorem 2). When the cells lie on a curve along which the distance grows with the gap in time, the tree is the path of consecutive cells and the pseudotime gives the true order (Theorem 3). The cluster version places each cell between the two ends of the path of centers (Lemma 4). That the pseudotime of real cells follows the real process is a heuristic, and the tests measure it.

**Setting.** Cells $x_1, \dots, x_n$ in $\mathbb{R}^d$, $n \ge 2$, and the complete graph $K_n$ with weight $w(i, j) = \|x_i - x_j\|$. For a tree $T$ on the cells, $d_T(i, j)$ is the sum of the weights on the unique path from $i$ to $j$ in $T$. Line L5 returns $\tau_i = d_T(r, i)$ for the root $r$.

**Theorem 1 (Prim).** Lines L1 and L2 return a minimum spanning tree of $K_n$.

*Proof.* Let $S$ be the set of cells taken so far. The loop keeps, for each cell $v \notin S$, the value $\mathrm{best}(v) = \min_{u \in S}w(u, v)$ and a cell $u$ that reaches it: line L1 computes the weight to the new cell and line L2 lowers the value when it is smaller. So the next cell $u$ and its edge to $\mathrm{parent}(u)$ form a lightest edge across the cut $(S, V \setminus S)$. By induction, the edges taken so far are part of some minimum spanning tree $T^*$. If the new edge $e$ is not in $T^*$, adding $e$ to $T^*$ makes a cycle, which crosses the cut at another edge $f$ with $w(f) \ge w(e)$. Then $T^* + e - f$ is a spanning tree of weight at most $w(T^*)$ that contains all the edges taken so far and $e$. After $n$ rounds the $n - 1$ edges form a spanning tree that is part of a minimum spanning tree, so it is one. $\square$

**Theorem 2 (two searches).** Let $T$ be a tree with nonnegative weights, $s$ any vertex, $a$ a vertex farthest from $s$, and $b$ a vertex farthest from $a$. Then the path from $a$ to $b$ is a longest path of $T$.

We use one fact about tree distances first.

**Lemma 2a (four points).** For any four vertices $x, y, z, w$ of a tree with nonnegative weights, $d_T(x, y) + d_T(z, w) \le \max\big(d_T(x, z) + d_T(y, w),\ d_T(x, w) + d_T(y, z)\big)$.

*Proof.* The union of the tree paths between the four vertices is a subtree with at most four leaves. For some way of splitting the four vertices into two pairs, say $\{x, z\}$ and $\{y, w\}$ (the other splits are the same up to names), it is a path from a vertex $p$ to a vertex $q$, possibly with $p = q$, together with paths from $p$ to $x$ and to $z$ and from $q$ to $y$ and to $w$, where these paths share no edges. Then $d_T(x, y) + d_T(z, w)$ and $d_T(x, w) + d_T(y, z)$ both equal $d_T(x, p) + d_T(z, p) + d_T(y, q) + d_T(w, q) + 2d_T(p, q)$, and $d_T(x, z) + d_T(y, w)$ is the same sum without $2d_T(p, q)$. So the two largest of the three sums are equal, and each sum is at most the larger of the other two. $\square$

*Proof of Theorem 2.* Let $u$-$v$ be a longest path, of length $D$. By Lemma 2a with $x = s$, $y = a$, $z = u$, $w = v$, either $d_T(s, a) + D \le d_T(s, u) + d_T(a, v)$ or $d_T(s, a) + D \le d_T(s, v) + d_T(a, u)$. Because $a$ is farthest from $s$, $d_T(s, u) \le d_T(s, a)$ and $d_T(s, v) \le d_T(s, a)$. So $d_T(a, v) \ge D$ in the first case and $d_T(a, u) \ge D$ in the second. The farthest vertex $b$ from $a$ is at least that far, and no path is longer than $D$, so the path from $a$ to $b$ has length $D$. $\square$

**Theorem 3 (monotone curve).** Let $t_1 < t_2 < \dots < t_n$ and suppose $\|x_i - x_j\|$ is a strictly increasing function of $|t_i - t_j|$: $|t_i - t_j| < |t_k - t_l|$ implies $\|x_i - x_j\| < \|x_k - x_l\|$. Then the minimum spanning tree is unique and is the path $1, 2, \dots, n$, and with root 1 the pseudotime $\tau_i = \sum_{l < i}\|x_{l+1} - x_l\|$ is strictly increasing in $i$.

*Proof.* Take an edge $(i, j)$ with $j > i + 1$. On the cycle $i, i + 1, \dots, j, i$ every edge $(l, l + 1)$ with $i \le l < j$ has $t_{l+1} - t_l < t_j - t_i$, so it is strictly lighter than $(i, j)$. So $(i, j)$ is the unique heaviest edge of a cycle. If some minimum spanning tree $T$ contained it, removing it would split $T$ into two parts, and some edge $(l, l + 1)$ of the cycle joins the two parts; replacing $(i, j)$ by it gives a lighter spanning tree, a contradiction. So every minimum spanning tree uses only the edges $(l, l + 1)$, and the only spanning tree made of them is the path. The tree distance from 1 to $i$ is the sum of the path edges before $i$, and every edge has positive weight because $\|x_{l+1} - x_l\| > \|x_l - x_l\| = 0$. $\square$

Points on a line, and points on a helix piece $(\cos t, \sin t, ct)$ with $t$ in an interval shorter than $\pi$, satisfy the condition: the squared chord $2 - 2\cos\Delta + c^2\Delta^2$ is strictly increasing in $\Delta$ on $[0, \pi]$. Noise breaks it, which is why the order of noisy cells is only measured.

**Lemma 4 (projection).** In the cluster version, let the path of centers be $c_0, c_1, \dots, c_m$ with offsets $o_0 = 0$ and $o_{j+1} = o_j + \|c_{j+1} - c_j\|$. A cell of the cluster at position $i$ gets $\tau \in [o_{\max(i-1, 0)}, o_{\min(i+1, m)}]$, and the foot it uses is the nearest point to the cell on the segment it is projected on.

*Proof.* For a segment from $a$ to $b$ of length $L > 0$ the code sets $s = (p - a) \cdot (b - a)/L$ and clips it to $[0, L]$. The function $s \mapsto \|p - a - s(b - a)/L\|^2$ is a convex quadratic with its minimum at the unclipped $s$, so the clipped value is its minimum on $[0, L]$, which is the nearest point of the segment. The cell then gets $o_j + s$ with $s \in [0, L] = [0, o_{j+1} - o_j]$ for the edge $j \in \{i - 1, i\}$ with the nearer foot. $\square$

So the pseudotime of the cluster version is never below 0 or above the length of the path, and the cells of a cluster lie next to the cells of the clusters before and after it on the path. If two centers are the same point, $L = 0$ and the code would divide by zero; this needs two clusters with the same mean, which the input must avoid.

**What the lines compute.** Lines L1 and L2 are Theorem 1. Line L3 is Theorem 2. Line L4 takes the first end of the backbone as the root when no root is given; which end is the start of the process is not known from the data alone. Line L5 is the tree distance from the root, computed by a depth-first search, and Theorem 3 is the case where it gives the true order. Line L6 marks the cells of degree 3 or more, where the tree branches. Line L7 computes the centers, and line L8 is Lemma 4.

**Complexity.** Prim's algorithm takes $n$ rounds, each of which finds the minimum of at most $n$ values and computes at most $n$ distances in $O(d)$ time, so lines L1 and L2 take $O(n^2d)$ time and $O(n)$ extra space, with no distance matrix stored. The two searches of line L3 and the search of line L5 take $O(n)$ time each on a tree. The cluster version with $m$ clusters takes $O(nd)$ for the centers, $O(m^2d)$ for the tree and $O(nd)$ for the projections, after $O(nm)$ for grouping the cells by label in this code.

**What the tests check.** The test file checks the page example, Prim's tree against Kruskal's algorithm on random points and against all labeled trees from Pruefer sequences for $n \le 6$, the backbone length against the longest distance over all pairs, Theorem 3 on random points of a helix piece given in shuffled order, Lemma 4 on clusters along a line, the cell of an off-path cluster, and the errors. Two simulations are measurements, not theorems: the rank correlation of the pseudotime with the true time for noisy cells near a line, and a Y shape in which one branch point lies near the junction, together with many small branches caused by noise.
