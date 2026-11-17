---
title: Correctness of the greedy ultrametric contour map
proves: [correctness]
status: full
---

This proof covers lines L1 to L12 of the main page. The input is a label map on a grid of $W \times H$ pixels and a real strength $E(e) \ge 0$ on each grid edge $e$ between two 4-neighbors. The output gives a value $\mathrm{UCM}(e)$ to each grid edge. Nothing here says that the strengths come from a good contour detector. The proof is about the merge process on any strengths.

Notation. A *region* is a set of pixels that is connected in the 4-neighbor grid graph. For two adjacent regions $a$ and $b$, let $S(a, b)$ be the sum of $E(e)$ over the grid edges $e$ with one pixel in $a$ and one in $b$, and let $n(a, b) \ge 1$ be the number of such edges. The *mean strength* is $\mu(a, b) = S(a, b) / n(a, b)$. The algorithm keeps a partition $\mathcal{P}_k$ of the pixels after $k$ merges. $\mathcal{P}_0$ is the partition of line L1, and its regions are the *initial regions*.

**Lemma 1 (the records hold the true sums).** After line L4, and after each pass of lines L5 to L10, each pair $(a, b)$ of adjacent live regions has a record with exactly $S(a, b)$, $n(a, b)$ and the list of the adjacent pairs $\{x, y\}$ of initial regions with $x \subseteq a$ and $y \subseteq b$. The heap holds an entry $(\mu(a, b), a, b)$ for it. No record exists for a pair that is not adjacent.

*Proof.* Lines L2 and L3 visit each grid edge once and add its strength to the record of the pair of regions on its two sides, so the claim holds after L4, where each record lists its own pair. Suppose the claim holds before a merge of $a$ and $b$ into $c$. A grid edge with one side in $c$ and the other side in a region $r \notin \{a, b\}$ has its first side in $a$ or in $b$, and not in both, because $a \cap b = \emptyset$. So $S(c, r) = S(a, r) + S(b, r)$ and $n(c, r) = n(a, r) + n(b, r)$, where a missing record counts as zero, and the list of $(c, r)$ is the union of the lists of $(a, r)$ and $(b, r)$. Lines L9 and L10 compute exactly these, and the push after L10 adds the heap entry. Pairs that do not involve $a$ or $b$ keep their records, and their sums do not change, because their regions do not change. $\square$

**Lemma 2 (each accepted pop is a minimum over the live pairs).** The entry that passes line L6 has the least $(\mu, a, b)$ over all pairs of adjacent live regions.

*Proof.* A region id is never reused, and the record of a pair of live regions never changes while both regions live (Lemma 1). So every heap entry whose two regions are live holds the current mean of its pair, and every live pair has such an entry. Line L6 skips the entries with a dead region. The heap pops entries in the order of $(\mu, a, b)$, so the first entry that passes L6 is the least over the live pairs. $\square$

**Lemma 3 (the levels do not decrease).** Let $m_1, m_2, \ldots$ be the levels of the merges in the order of the loop. Then $m_1 \le m_2 \le \cdots$.

*Proof.* Let merge $k$ join $a$ and $b$ at level $m_k$. By Lemma 2, $\mu(x, y) \ge m_k$ for every live pair before the merge. After the merge, the pairs without $c$ are unchanged. For a pair $(c, r)$,
$$\mu(c, r) = \frac{S(a, r) + S(b, r)}{n(a, r) + n(b, r)} = \frac{n(a, r)\,\mu(a, r) + n(b, r)\,\mu(b, r)}{n(a, r) + n(b, r)},$$
a weighted mean with nonnegative weights of values that are at least $m_k$ (a missing record has weight zero). So $\mu(c, r) \ge m_k$, and every live pair after the merge has mean at least $m_k$. By Lemma 2, $m_{k+1} \ge m_k$. $\square$

**Lemma 4 (termination).** The loop stops after exactly $R - 1$ merges, where $R$ is the number of initial regions, and it ends with one region.

*Proof.* Each accepted pop replaces two live regions by one, so there are at most $R - 1$ merges. Each pass pops one entry, and a finite number of entries is pushed, so the loop stops. When it stops, the heap is empty, so by Lemma 1 no two live regions are adjacent. The grid graph is connected, so a partition into more than one region always has two adjacent regions. Hence one region is left, after $R - 1$ merges. $\square$

**Lemma 5 (the value of a grid edge).** Let $e = (p, q)$ be a grid edge. If $p$ and $q$ are in the same initial region, then $\mathrm{UCM}(e) = 0$. Otherwise $\mathrm{UCM}(e) = m_k$, where merge $k$ is the first merge after which $p$ and $q$ are in one region. That merge joins a region that contains $p$ and a region that contains $q$.

*Proof.* Let $x$ and $y$ be the initial regions of $p$ and $q$, with $x \ne y$. Before merge $k$, $x$ and $y$ lie in two different live regions $a \supseteq x$ and $b \supseteq y$, and merge $k$ joins exactly these two. The pair $\{x, y\}$ is adjacent, because $e$ joins them, so by Lemma 1 it is in the list of the record $(a, b)$, and line L8 sets its value to $m_k$. A pair is in the list of one record only, and line L8 runs once for the record $(a, b)$, so no other line writes this value. Line L11 copies the value of $\{x, y\}$ to $e$. Edges inside one initial region keep the value 0. $\square$

**Theorem 1 (thresholds give the partitions of the hierarchy).** Let $t \ge 0$ and let $k(t)$ be the number of merges with level at most $t$. The connected components of the graph on the pixels with the grid edges $e$ such that $\mathrm{UCM}(e) \le t$ are exactly the regions of $\mathcal{P}_{k(t)}$.

*Proof.* By Lemma 3, the merges with level at most $t$ are the first $k(t)$ merges. Take a grid edge $e = (p, q)$ with $\mathrm{UCM}(e) \le t$. By Lemma 5, either $p$ and $q$ share an initial region, or they share a region after merge $k$ with $m_k \le t$, so $k \le k(t)$. In both cases they share a region of $\mathcal{P}_{k(t)}$, and so does each pair of pixels joined by a path of such edges. So each component lies inside one region.

For the other direction, we show by induction on $j \le k(t)$ that each region of $\mathcal{P}_j$ is connected by edges with value at most $t$. For $j = 0$, each region is a connected set of pixels with equal labels, and the edges inside it have value 0 by Lemma 5. Merge $j$ joins two adjacent regions $a$ and $b$ at level $m_j \le t$. By Lemma 5, every grid edge between $a$ and $b$ gets the value $m_j$, and there is at least one such edge, because $a$ and $b$ are adjacent. With the induction hypothesis for $a$ and for $b$, the region $a \cup b$ is connected by edges with value at most $t$. So each region lies inside one component. $\square$

**Corollary (closed contours and nesting).** For $t \le t'$, each region of the partition at $t$ lies inside one region of the partition at $t'$, because $\mathcal{P}_{k(t')}$ comes from $\mathcal{P}_{k(t)}$ by more merges. The set of grid edges with $\mathrm{UCM}(e) > t$ is exactly the set of edges between two different regions of $\mathcal{P}_{k(t)}$. So the boundary at each threshold is a union of closed region boundaries, with no loose ends inside a region.

**Theorem 2 (the UCM is an ultrametric).** For pixels $p$ and $q$, let $d(p, q)$ be the least $t \ge 0$ such that $p$ and $q$ are in one component at threshold $t$. Then $d(p, p) = 0$, $d(p, q) = d(q, p)$, and
$$d(p, r) \le \max(d(p, q), d(q, r))$$
for all pixels $p, q, r$. Also $d(p, q) = \min_{\pi} \max_{e \in \pi} \mathrm{UCM}(e)$, where $\pi$ runs over the paths from $p$ to $q$ in the grid graph.

*Proof.* Symmetry and $d(p, p) = 0$ are clear. Let $t = \max(d(p, q), d(q, r))$. At threshold $t$, $p$ and $q$ are in one component, and $q$ and $r$ are in one component, because the partitions are nested (the corollary). So $p$ and $r$ are in one component at $t$, and $d(p, r) \le t$. For the path form, $p$ and $q$ are in one component at threshold $t$ if and only if some path joins them with all its edges at most $t$, which holds if and only if the minimax value of the paths is at most $t$. $\square$

$d$ is an ultrametric on the initial regions. On single pixels it is a pseudo-ultrametric, because two pixels of one initial region have distance 0. With one initial region per pixel it is an ultrametric on the pixels.

**Cost.** Let $R$ be the number of initial regions and $P$ the number of adjacent pairs among them. Lines L1 to L4 take $O(WH + P)$ time. The region adjacency graph is planar, because the regions are connected sets of pixels in the plane, and merging two adjacent regions keeps it planar. So $P \le 3R - 6$ for $R \ge 3$, and the same bound holds after each merge. A merge of $a$ and $b$ costs $O((\deg a + \deg b) \log Q)$ for the records and the heap, where $Q$ is the number of heap entries. Each degree is less than $R$, and $Q = O(R^2)$, so the merges cost $O(R^2 \log R)$ in the worst case and $O(R \log R)$ when all degrees stay bounded by a constant. Line L10 appends the shorter list to the longer one, so a pair of initial regions moves only to a list at least twice the size of its old list, at most $\log_2 P$ times. The lists cost $O(P \log P)$ in total. Line L11 takes $O(WH)$ time. The total is $O(WH + R^2 \log R)$ time and $O(WH + R^2)$ space in the worst case, in the real-RAM model, where $R \le WH$.
