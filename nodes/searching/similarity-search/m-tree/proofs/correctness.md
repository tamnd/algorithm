---
title: The M-tree keeps its covering invariants under insertion, and its range and k-NN searches are exact
proves: [correctness]
status: full
---

We use the names of the pseudocode on the page. $(U, d)$ is a metric space. For a node $N$, $\mathrm{obj}(N)$ is the multiset of objects in the leaf entries below $N$. A routing entry $e$ with child $C$ *covers* when $d(e.\mathrm{obj}, y) \le e.\mathrm{radius}$ for all $y \in \mathrm{obj}(C)$. The invariants are (I1) every routing entry covers; (I2) every non-root entry has $e.d_p = d(e.\mathrm{obj}, p)$, where $p$ is the routing object of the entry that points to its node; (I3) all leaves are at one depth; (I4) every node has at most $M$ entries, and every non-root node at least $b = \lfloor (M+1)/2 \rfloor$.

**Lemma 1 (radius of a split).** Let $o$ be an object and $E$ a set of entries of one node, all covering. If $\rho = \max_{e \in E} (d(o, e.\mathrm{obj}) + e.\mathrm{radius})$, with radius 0 for leaf entries, then $d(o, y) \le \rho$ for every object $y$ of every entry of $E$ (the object of a leaf entry, or an object below a routing entry).

*Proof.* For a leaf entry $y = e.\mathrm{obj}$ and $d(o, y) \le \rho$. For a routing entry, $d(o, y) \le d(o, e.\mathrm{obj}) + d(e.\mathrm{obj}, y) \le d(o, e.\mathrm{obj}) + e.\mathrm{radius} \le \rho$ by the triangle inequality and (I1). $\square$

**Lemma 2 (insertion).** If the tree satisfies (I1) to (I4) before INSERT$(x)$, it does after, and its objects are the old ones plus $x$.

*Proof.* Let $N_0, N_1, \ldots, N_h$ be the nodes on the path chosen by lines L20 and L21, from the root to a leaf, and $e_i$ the entry of $N_i$ chosen there. After line L20 or L21, $d(x, e_i.\mathrm{obj}) \le e_i.\mathrm{radius}$, and radii only grow, so each $e_i$ covers its old objects and $x$. No other entry gains an object. Line L18 adds $x$ to $N_h$ with $d_p = d(x, e_{h-1}.\mathrm{obj})$, passed down in line L22, which is (I2) for it.

Now consider a split of a node $N$ with $M + 1$ entries in lines L24 to L27. The balanced partition of line L25 gives the two promoted objects alternate turns until no entry is free, so the parts have $\lceil (M+1)/2 \rceil$ and $\lfloor (M+1)/2 \rfloor = b$ entries: (I4) for the new nodes. By Lemma 1 the new routing entries cover. Line L26 sets the $d_p$ of every entry to its distance to the routing object of its new parent entry, which gives (I2) inside the new nodes, and line L22 sets the $d_p$ of the two new routing entries to their distance to $p$, the routing object of the node that now holds them. The new entries replace $e$ in that node, which holds one more entry; its routing entry, if any, covers the same objects as before, so (I1) holds there. If that node now has $M + 1$ entries, line L23 splits it in turn. If the root splits, line L17 makes a new root with two entries and no $d_p$, and every leaf gets one level deeper, so (I3) holds; otherwise no depth changes. The new root has 2 entries, which (I4) allows. $\square$

**Theorem 1 (range).** If (I1) and (I2) hold, RANGE$(\text{root}, q, r, \text{none})$ reports exactly the objects $y$ of the tree with $d(q, y) \le r$, with multiplicity.

*Proof.* By induction on the height of $N$, RANGE$(N, q, r, d(q, o_N))$, where $o_N$ is the routing object of the entry pointing to $N$ (none for the root), reports exactly the answers in $\mathrm{obj}(N)$. Each leaf entry is reported only if line L5 found $d(q, y) \le r$. Suppose an answer $y$ is not reported; then an entry $e$ on its path was skipped. If line L2 skipped it, then by (I2), $e.d_p = d(e.\mathrm{obj}, o_N)$ and $d_{qp} = d(q, o_N)$, so by the triangle inequality $d(q, e.\mathrm{obj}) \ge |d_{qp} - e.d_p| > r + e.\mathrm{radius}$. If line L6 skipped it, $d(q, e.\mathrm{obj}) > r + e.\mathrm{radius}$ directly. For a leaf entry with radius 0 and $y = e.\mathrm{obj}$ this says $d(q, y) > r$. For a routing entry, (I1) gives $d(q, y) \ge d(q, e.\mathrm{obj}) - d(e.\mathrm{obj}, y) > r + e.\mathrm{radius} - e.\mathrm{radius} = r$. Either way $y$ is not an answer, a contradiction. $\square$

**Theorem 2 ($k$ nearest).** If (I1) and (I2) hold and the tree stores $n$ objects, KNN$(q, k)$ returns $\min(k, n)$ objects whose distances are the $\min(k, n)$ least distances from $q$ to the stored objects.

*Proof.* For an entry $e$ define $\mathrm{lb}(e) = \max(d(q, e.\mathrm{obj}) - e.\mathrm{radius}, 0)$. By (I1) and the triangle inequality, every object $y$ below $e$ has $d(q, y) \ge \mathrm{lb}(e)$; for a leaf entry $\mathrm{lb}(e) = d(q, y)$. As in Theorem 1, the test of line L12 skips $e$ only if $d(q, e.\mathrm{obj}) - e.\mathrm{radius} > \tau$, and then every object below $e$ has distance greater than $\tau$.

The value $\tau$ is $\infty$ while $|B| < k$ and then the largest distance in $B$; it never increases, because an object enters a full $B$ only if its distance is below $\tau$, and the farthest is dropped. Call an object *lost* if it is never offered to $B$ in line L14. An object $y$ is lost only if (a) an entry above it or its own entry was skipped by line L12 or not added in line L15 at a moment with threshold $\tau_0$, so $d(q, y) > \tau_0$; or (b) the search stopped in line L10 while a node above $y$ was still in PQ, or below a node in PQ, with $d_{\min} > \tau_1$ at that moment, and each node in PQ has $d_{\min} \ge$ the popped one, so $d(q, y) \ge d_{\min} > \tau_1$. Since $\tau$ only decreases, in both cases $d(q, y) > \tau_f$, the final threshold.

If fewer than $k$ objects were offered, then $\tau_f = \infty$, nothing is lost, and $B$ holds all $n < k$ objects. Otherwise $|B| = k$ at the end, and $B$ holds the $k$ least distances among the offered objects, all at most $\tau_f$; every lost object has distance greater than $\tau_f$. So the $k$ distances in $B$ are the $k$ least distances of all stored objects. $\square$

**Lemma 3 (height).** Under (I3) and (I4) with $M \ge 3$, a tree of height $h \ge 2$ levels holds $n \ge 2 b^{h-1}$ objects, so $h \le 1 + \log_b(n/2)$.

*Proof.* The root has at least 2 entries when it is internal, since it was made by a split of the root in line L17. Every other internal node has at least $b$ children, and every leaf at least $b$ entries, and $b \ge 2$ for $M \ge 3$. By (I3) there are at least $2 b^{h-2}$ leaves, each with at least $b$ objects. $\blacksquare$
