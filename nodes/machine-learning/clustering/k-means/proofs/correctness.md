---
title: Lloyd's algorithm does not increase the cost, stops, and returns a fixed point
proves: [correctness]
status: full
---

We write $\phi(a, c) = \sum_{i} \|x_i - c_{a_i}\|^2$ for the cost of the labels $a$ with the centers $c$. Let $a^{(t)}$ be the labels after the assignment step of iteration $t$ (lines L4 to L6), and $c^{(t)}$ the centers after the update step of iteration $t$ (lines L8 to L10). Let $c^{(0)}$ be the initial centers.

**Lemma 1 (centroid).** For a finite non-empty set $P$ of points with mean $\mu$ and any $z \in \mathbb{R}^d$, $\sum_{x \in P} \|x - z\|^2 = \sum_{x \in P} \|x - \mu\|^2 + |P| \, \|\mu - z\|^2$.

*Proof.* Write $x - z = (x - \mu) + (\mu - z)$ and expand the square. The cross term is $2 \langle \sum_{x \in P} (x - \mu), \mu - z \rangle = 0$, because $\sum_{x \in P} (x - \mu) = 0$. $\square$

So the mean is the unique best center of a fixed cluster.

**Lemma 2 (one iteration).** If iteration $t \ge 2$ changes at least one label, then $\phi(a^{(t)}, c^{(t)}) < \phi(a^{(t-1)}, c^{(t-1)})$. In all cases the cost after the update step of iteration $t$ is at most the cost of $a^{(t)}$ with $c^{(t-1)}$.

*Proof.* Assignment step. Line L5 gives each point a nearest center of $c^{(t-1)}$, so $\|x_i - c^{(t-1)}_{a^{(t)}_i}\| \le \|x_i - c^{(t-1)}_{a^{(t-1)}_i}\|$ for each $i$. If the label of $x_i$ changes, then by the tie rule of line L5 the old center is not among the nearest, so the inequality is strict. Sum over $i$: $\phi(a^{(t)}, c^{(t-1)}) < \phi(a^{(t-1)}, c^{(t-1)})$ when a label changes.

Update step. The cost splits into one sum per cluster. For a non-empty cluster $P_j$, line L10 replaces the center by the mean, and by Lemma 1 the sum of the cluster does not increase. An empty cluster adds nothing and keeps its center. So $\phi(a^{(t)}, c^{(t)}) \le \phi(a^{(t)}, c^{(t-1)})$. Together with the assignment step this gives the claim. $\square$

**Lemma 3 (finitely many states).** At all times each center is an initial center or the mean of a non-empty subset of the points.

*Proof.* At the start each center is an initial center. Line L10 sets a center to the mean of $\{x_i : i \in P_j\}$ with $P_j \ne \emptyset$, and an empty cluster keeps its center. By induction on the iterations the claim holds. $\square$

**Theorem.** The loop of line L2 returns after finitely many iterations. At the return, each point is at a nearest center, each non-empty cluster has its mean as center, and the cost is at most the cost $\phi(a^{(1)}, c^{(0)})$ of the nearest-center labels of the initial centers.

*Proof.* By Lemma 3, each center lies in the finite set $S$ of the $k$ initial centers and the at most $2^n - 1$ means of non-empty subsets. So the pair $(a^{(t)}, c^{(t)})$ lies in the finite set $\{1, \ldots, k\}^n \times S^k$, and the cost $\phi(a^{(t)}, c^{(t)})$ takes finitely many values. By Lemma 2, the costs after iterations $2, 3, \ldots$ that change a label form a strictly decreasing sequence. A strictly decreasing sequence in a finite set has finitely many terms. So some iteration changes no label, and line L7 returns there.

At the return, iteration $t$ found no change. Line L5 computed a nearest center for each point with respect to $c^{(t-1)}$, and the labels equal $a^{(t-1)}$, so each point is at a nearest center of the returned centers $c^{(t-1)}$. If $t - 1 \ge 1$, the centers $c^{(t-1)}$ came from the update step with the same labels, so each non-empty cluster has its mean as center. (If $t = 1$, then $n = 0$ and there is nothing to prove, because the first iteration changes each label from NIL.) The cost bound follows from Lemma 2 and induction. $\square$

**Remark (local, not global).** A fixed point need not be optimal. The four corners $(0,0), (0,1), (w,0), (w,1)$ with $w > 1$ and the initial centers $(0,0)$ and $(0,1)$ give the fixed point with clusters bottom and top, of cost $w^2$, while the optimum is 1.

**Remark (without the tie rule).** If line L5 may pick any nearest center, a point at equal distance from two centers can switch at each iteration while the cost stays the same, and the loop need not stop. The tie rule removes this case, because then each change of label strictly lowers the cost.
