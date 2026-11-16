---
title: Correctness of best bin first search
proves: [correctness]
status: full
---

Fix a finite set of points $x^{(1)}, \dots, x^{(n)}$ in $\mathbb{R}^d$, a query $q$, a number $k \ge 1$ and a leaf budget $E \ge 1$, possibly $E = \infty$. The tree is the k-d tree of the main page. Each internal node $v$ has a split dimension $d_v$ and a split value $s_v$, which is a coordinate of a point of its subtree. Every point $x$ in the left subtree of $v$ has $x_{d_v} \le s_v$, and every point in the right subtree has $x_{d_v} \ge s_v$. A queue entry is a triple $(b, v, o)$ with a number $b$, a node $v$ and an offset vector $o \in \mathbb{R}^d$. Distances below are squared Euclidean distances, $D(x) = \lVert x - q \rVert^2$.

**Lemma 1 (the bound).** For every entry $(b, v, o)$ that line L2 or line L10 puts in the queue, $b = \sum_t o_t^2$, and every point $x$ in the subtree of $v$ has $|x_t - q_t| \ge |o_t|$ for each $t$. Hence $D(x) \ge b$.

*Proof.* Line L2 puts $(0, \text{root}, 0)$ in the queue, and both claims hold. Assume the claims for an entry $(b, v, o)$ that line L4 pops. Lines L6 to L11 walk down from $v$ and keep $b$ and $o$. Each node $w$ on this walk is in the subtree of $v$, so the points of its subtree also satisfy $|x_t - q_t| \ge |o_t|$. At $w$, with $j = d_w$ and $\delta = q_j - s_w$, line L10 pushes the far child with $o'$, where $o'_j = \delta$ and $o'_t = o_t$ for $t \ne j$, and with $b' = b - o_j^2 + \delta^2 = \sum_t o_t'^2$. For $t \ne j$ the claim for the far child follows from the claim for $w$. For $t = j$ there are two cases. If $\delta < 0$, the far child is the right child, so each of its points has $x_j \ge s_w > q_j$ and $|x_j - q_j| = x_j - q_j \ge s_w - q_j = |\delta|$. If $\delta \ge 0$, the far child is the left child, so $x_j \le s_w \le q_j$ and $|x_j - q_j| = q_j - x_j \ge q_j - s_w = \delta$. In both cases $|x_j - q_j| \ge |o'_j|$. Then $D(x) = \sum_t (x_t - q_t)^2 \ge \sum_t o_t'^2 = b'$. $\square$

**Lemma 2 (the partition).** At each test of line L3, every leaf of the tree is either a leaf that line L12 has examined or a leaf in the subtree of exactly one queue entry, and not both.

*Proof.* At the start the queue holds the root and no leaf is examined. When line L4 pops $(b, v, o)$, the leaves of the subtree of $v$ are no longer covered by the queue. The walk of lines L6 to L11 goes from $v$ to one leaf, and at each node it pushes the subtree of the other child. The subtrees of the pushed children and the final leaf partition the leaves of the subtree of $v$, and line L12 examines the final leaf. So the claim holds again at the next test of line L3. $\square$

**Lemma 3 (the order).** Let $b$ be the key that line L4 pops. Every entry that lines L6 to L11 push has a key $b' \ge b$. Hence the keys that line L4 pops do not decrease.

*Proof.* Use the notation of Lemma 1. If $o_j = 0$, then $b' = b + \delta^2 \ge b$. If $o_j < 0$, an earlier crossing on dimension $j$ put the subtree of $w$ on the side $x_j \ge s' > q_j$ of an earlier split $s'$, with $o_j = q_j - s'$. The split value $s_w$ is a coordinate of a point of this subtree, so $s_w \ge s' > q_j$. Then $\delta = q_j - s_w \le q_j - s' = o_j < 0$ and $\delta^2 \ge o_j^2$. The case $o_j > 0$ is symmetric. So $b' = b - o_j^2 + \delta^2 \ge b$. The queue is a min-priority queue, so after the pop every entry in it has a key at least $b$, and the new entries also have keys at least $b$. So the next pop has a key at least $b$. $\square$

**Lemma 4 (the best list).** After each execution of line L12, the list holds the $\min(k, m)$ smallest distances among the $m$ points of the examined leaves, with their indices.

*Proof.* Line L1 starts with an empty list. Line L12 takes each new point and keeps it if the list has fewer than $k$ items or if the point is closer than the worst item, which it then replaces. This is the standard bounded selection with a max-heap, so the claim holds by induction over the points. $\square$

**Theorem 1 (exact answer).** If the loop ends because the queue is empty or because of the test of line L5, the list that line L14 returns holds the $k$ smallest distances $D(x)$ over all points, or all $n$ points if $n < k$.

*Proof.* If the queue is empty, Lemma 2 says that every leaf is examined, and Lemma 4 gives the claim. If line L5 stops the loop, the list has $k$ items, and the popped key $b$ is at least the largest distance $r$ in the list. The popped entry and every entry still in the queue have keys at least $b$, because the queue is a min-priority queue. By Lemma 2 each point that is not examined is in the subtree of one of these entries, and by Lemma 1 its distance is at least $b \ge r$. So no point outside the list is closer than the $k$-th item of the list, and with Lemma 4 the list holds the $k$ smallest distances. $\square$

**Theorem 2 (more leaves do not hurt).** Let $E < E'$. Let $r_i(E)$ be the $i$-th distance in the list that the search returns with budget $E$. Then $r_i(E') \le r_i(E)$ for each $i$ for which both are defined.

*Proof.* The steps of the search depend on the budget only through the test at line L3. So the run with budget $E$ does the same steps as the run with budget $E'$ until it stops, and the leaves that it examines are the first leaves that the run with $E'$ examines. The run with $E'$ examines a superset of points. By Lemma 4 each run returns the smallest distances of its examined set, and the $i$-th smallest value of a superset is at most the $i$-th smallest value of the subset. $\square$

**Remark (what is not proved).** When the budget $E$ stops the loop, the answer can be wrong, and the page gives no bound on the error. The success rates on the main page are measurements, not consequences of these lemmas. The key $b$ is in fact the squared distance from $q$ to the box of the leaf cell, because by Lemma 3 the last crossing on each dimension is the tightest one, but the proofs above use only the lower bound of Lemma 1. $\blacksquare$
