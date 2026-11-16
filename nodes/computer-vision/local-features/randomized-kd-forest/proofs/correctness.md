---
title: Correctness of the randomized k-d forest
proves: [correctness]
status: full
---

The forest holds a list of points $x^{(1)}, \dots, x^{(n)}$ in $\mathbb{R}^d$ and $T$ trees. A node is a leaf with a list of point indices, or an internal node with a dimension $j$, a split value $s$ and two children. The **cell** of a node is the set of $x \in \mathbb{R}^d$ that satisfy $x_j < s$ for each ancestor where the path goes left and $x_j \ge s$ for each ancestor where it goes right. Distances are squared Euclidean distances to the query $q$, $D(x) = \lVert x - q \rVert^2$.

**Invariant.** In each tree, every index $1, \dots, n$ is in exactly one leaf, and every point is in the cell of its leaf. Each leaf has at most $\ell$ points (the leaf size), or only equal points.

**Lemma 1 (MAKE ends and keeps the invariant).** Called on a nonempty list $S$ of indices whose points lie in the cell of the node, lines L2 to L7 end, and they produce a subtree whose leaves partition $S$ and in which every point is in the cell of its leaf.

*Proof.* By induction on $|S|$. If line L2 makes a leaf, the claim holds, because the points of $S$ lie in the cell. Else some dimension has positive variance, so line L4 has a candidate and line L5 picks a dimension $j$ with variance $> 0$ and mean $m$. A dimension with positive variance has a value below its mean and a value at least its mean, so both lists of line L6 are nonempty in exact arithmetic. If rounding makes one empty, the code splits below the largest value, and since the values are not all equal, both sides are again nonempty. So both lists are smaller than $S$. A point $i$ goes left exactly when $x^{(i)}_j < s$, which is the condition of the cell of the left child, and right exactly when $x^{(i)}_j \ge s$. The two lists partition $S$, and the induction hypothesis applies to each. $\square$

**Lemma 2 (BUILD and INSERT keep the invariant).** After line L1, and after each call of INSERT, the invariant holds for each tree.

*Proof.* Line L1 calls MAKE on all indices at the root, whose cell is $\mathbb{R}^d$, so Lemma 1 gives the invariant. For INSERT of a point $x$ with new index $i$: line L10 goes left exactly when $x_j < s$, so the leaf it reaches has $x$ in its cell. Line L11 adds $i$ to that leaf only, so $i$ is in exactly one leaf. If the leaf now has more than $\ell$ points, line L12 calls MAKE on its indices, whose points all lie in its cell, and Lemma 1 replaces the leaf by a subtree whose leaves partition the same indices and respect the cells. Other leaves do not change. $\square$

**Lemma 3 (the key is a lower bound).** For each queue entry $(b, v, o)$ of SEARCH, $b = \sum_t o_t^2$ and every point $x$ in the cell of $v$ has $|x_t - q_t| \ge |o_t|$ for each $t$. Hence every point stored in the subtree of $v$ has $D(x) \ge b$.

*Proof.* Line L14 puts each root with $b = 0$ and $o = 0$, and the claim holds. The walk of lines L18 to L22 from a popped entry keeps $b$ and $o$, and the cells along the walk are subsets of the cell of $v$. At a node with dimension $j$ and split $s$, let $\delta = q_j - s$. Line L21 pushes the far child with $o'_j = \delta$, the other offsets unchanged, and $b' = b - o_j^2 + \delta^2 = \sum_t o_t'^2$. If $\delta < 0$, the far child is the right child, whose cell has $x_j \ge s > q_j$, so $|x_j - q_j| \ge s - q_j = |\delta|$. If $\delta \ge 0$, the far child is the left child, whose cell has $x_j < s \le q_j$, so $|x_j - q_j| > q_j - s = \delta$. For $t \ne j$ the bound is inherited. By the invariant, each stored point of a subtree lies in the cell of its leaf, which is inside the cell of $v$. $\square$

**Lemma 4 (the partition of each tree).** At each test of line L15, for each tree, every leaf of the tree is either a leaf that line L23 has reached or a leaf in the subtree of exactly one queue entry.

*Proof.* The same as for a single tree: line L14 covers each tree by its root, and each pop at line L16 removes one subtree, which the walk splits into the pushed far subtrees and one reached leaf. $\square$

**Lemma 5 (one check per point).** Line L24 computes the distance of each point at most once per search, so the number of distance computations is at most $\min(n, C + \ell')$ for a budget $C$, where $\ell'$ is the size of the largest leaf.

*Proof.* Line L23 skips an index that is in the set of seen points, and line L24 adds an index to the set before it computes its distance. The test of line L15 is made before each leaf, so the count passes $C$ by less than one leaf. $\square$

**Theorem 1 (exact answer).** If SEARCH ends because the queue is empty or because of line L17, it returns the $k$ smallest distances over all stored points, or all of them if $n < k$.

*Proof.* The list keeps the $\min(k, m)$ smallest distances among the $m$ seen points, by the standard bounded selection with a max-heap. If the queue is empty, Lemma 4 says that each tree has reached all its leaves, so all points are seen. If line L17 stops the loop, let $b$ be the popped key and $r \le b$ the largest distance in the list. Take a point $x$ that has not been seen. Pick any tree. By the invariant, $x$ is in one leaf of that tree, and that leaf has not been reached, since reaching it would have marked $x$ as seen. By Lemma 4 that leaf is in the subtree of a queue entry or of the popped entry, whose key is at least $b$ because the queue is a min-priority queue. By Lemma 3, $D(x) \ge b \ge r$. So no unseen point is closer than the $k$-th item of the list. $\square$

**Theorem 2 (more checks do not hurt).** For budgets $C < C'$ and the same forest and query, the $i$-th distance returned with $C'$ is at most the $i$-th distance returned with $C$.

*Proof.* The steps of SEARCH depend on the budget only through the test at line L15. So the run with $C$ is a prefix of the run with $C'$, and it sees a subset of the points. The $i$-th smallest value of a superset is at most that of the subset. $\square$

**What is not proved.** Nothing above bounds the error when the budget stops the search. The claim that several randomized trees find the true neighbor more often than one tree at the same number of checks is a measured result of Silpa-Anan and Hartley and of Muja and Lowe, and the example on the main page is also a measurement. $\blacksquare$
