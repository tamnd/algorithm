---
title: Density peak clustering gives each point the cluster of the first center on its chain of nearest denser points
proves: [correctness]
status: full
---

We use the pseudocode of the page. Let $D$ have $n \ge 1$ points with distances $d(i, j)$, and let $\rho_i$ be the local density of line L1. Line L2 sorts the points into the order $q_1, \ldots, q_n$ by $\rho$ from high to low, and equal $\rho$ by index from low to high. Write $j \succ i$ ("$j$ is denser than $i$") if $j$ comes before $i$ in this order. This is a strict total order, and $q_1$ is its largest element.

**Lemma 1 (the definitions).** After lines L3 to L5, for each $i \ne q_1$, $\delta_i = \min_{j \succ i} d(i, j)$, and $\mathrm{nn}_i$ is a point $j \succ i$ with $d(i, j) = \delta_i$, the earliest such point in the order. For $q_1$, $\delta = \max_j d(q_1, j)$ and $\mathrm{nn}$ is undefined.

*Proof.* For $i = q_r$ with $r \ge 2$, the points $j \succ i$ are exactly $q_1, \ldots, q_{r-1}$, and line L5 scans them in order and keeps the first strict minimum. Line L3 is the convention of Rodriguez and Laio for the densest point. $\square$

With $\rho$ and $\delta$ defined in this way, the decision graph of the paper is the set of pairs $(\rho_i, \delta_i)$, and line L6 selects the centers $Z$ from it. The only property the assignment needs is $q_1 \in Z$.

**Lemma 2 (chains end at a center).** Define the parent of $i \notin Z$ as $\mathrm{nn}_i$. Then $\mathrm{nn}_i \succ i$, so following parents from any point gives a sequence that strictly rises in the order. It cannot go on forever, and it can only stop at a center, because every non-center has a parent and $q_1$, the only point with no parent, is a center. So each point $i$ has a well defined first center $z(i)$ on its chain $i, \mathrm{nn}_i, \mathrm{nn}_{\mathrm{nn}_i}, \ldots$, and the parent links form a forest whose roots are the centers.

**Theorem (assignment).** Lines L7 to L9 give each center its own label, and each point $i$ the label of $z(i)$. So the clusters are the trees of the forest of Lemma 2, one for each center, and they partition $D$.

*Proof.* By induction on the position in the order. Line L7 visits the points in the order $q_1, \ldots, q_n$. A center gets a new label in line L8, and $z(i) = i$ for a center. A non-center $i$ has $\mathrm{nn}_i \succ i$, which was visited earlier, so its label is already set, and by the induction hypothesis it equals the label of $z(\mathrm{nn}_i) = z(i)$. Line L9 copies it. $\square$

This is the single pass assignment that Rodriguez and Laio describe: after the centers are found, each other point goes to the cluster of its nearest neighbor of higher density. The tie rule makes "higher density" a total order, so the parent of every non-center is defined even when many points have the same $\rho$, as happens with the cutoff kernel, whose values are integers.

**The halo.** For a cluster $c$, the border region is the set of its points within $d_c$ of a point of another cluster. Line L10 sets $\rho_b(c)$ to the largest density in that region, or $-\infty$ if the region is empty. Line L11 marks as halo the points of $c$ with $\rho_i \le \rho_b(c)$; the paper keeps as the cluster core the points with a density higher than $\rho_b$. The labels do not change.

**Determinism.** With the tie rule, $\rho$, $\delta$, the parents and the labels are functions of the input sequence, and of nothing else. The partition does not depend on the input order when all $\rho_i$ are different and no point has two nearest denser points at the same distance, because then the tie rule is never used.

**Cost.** Line L1 computes all $n(n-1)$ distances, $\Theta(n^2 d)$ time. Line L2 sorts, $O(n \log n)$. Lines L4 and L5 compare each point with all earlier points, $\Theta(n^2 d)$ in total. Lines L7 to L9 take $\Theta(n)$ time, and the halo takes $\Theta(n^2 d)$. The extra space is $\Theta(n)$ when distances are computed again when needed, or $\Theta(n^2)$ when the distance matrix is stored.
