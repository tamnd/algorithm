---
title: Canopies cover the data, and points closer than T1 - T2 share a canopy
proves: [correctness]
status: full
---

We use the pseudocode of the page. The input is a finite set $P$ of $n$ points, a cheap distance $c$ on $P$ with $c(p, p) = 0$ and $c(p, q) = c(q, p)$, and thresholds $T_1 > T_2 > 0$. A canopy with center $z$ is $K(z) = \{p \in P : c(z, p) < T_1\}$. The set $A$ holds the points that can still become centers.

**Lemma 1 (termination).** The loop of line L2 runs at most $n$ times.

*Proof.* Line L3 takes a center $z \in A$, and line L5 removes $z$ from $A$ because $c(z, z) = 0 < T_2$. So $|A|$ drops by at least one in each round. $\square$

**Lemma 2 (cover).** When the algorithm stops, each point $p$ lies within cheap distance less than $T_2$ of some center, and so in the canopy of that center.

*Proof.* At the start $p \in A$. The loop stops only when $A$ is empty, and line L5 is the only line that removes points from $A$. It removes $p$ while the center is $z$ only if $c(z, p) < T_2$. Then $c(z, p) < T_2 < T_1$, so line L4 put $p$ in $K(z)$. $\square$

**Lemma 3 (separated centers).** If $z$ was chosen before $z'$, then $c(z, z') \ge T_2$.

*Proof.* When $z'$ is chosen, it is still in $A$. If $c(z, z') < T_2$, line L5 would have removed $z'$ in the round of $z$. $\square$

So no center lies in the inner ball of radius $T_2$ of another center. If the cheap distance is a metric, the balls of radius $T_2/2$ around the centers are disjoint, so the number of canopies is at most the largest number of points of $P$ with pairwise distance at least $T_2$.

**Theorem (close pairs).** If $c$ satisfies the triangle inequality and $c(p, q) < T_1 - T_2$, then $p$ and $q$ share a canopy. So the second stage, which compares with the expensive distance only the pairs that share a canopy, sees every pair whose cheap distance is below $T_1 - T_2$.

*Proof.* By Lemma 2 there is a center $z$ with $c(z, p) < T_2$. Then $c(z, q) \le c(z, p) + c(p, q) < T_2 + (T_1 - T_2) = T_1$, so both $p$ and $q$ are in $K(z)$. $\blacksquare$

**Consequence for the second stage.** Suppose the second stage joins two points when their expensive distance $e$ is at most $\theta$, and the cheap distance satisfies $c \le e$. If $\theta < T_1 - T_2$, each pair with $e(p, q) \le \theta$ has $c(p, q) < T_1 - T_2$ and shares a canopy. Then single linkage at level $\theta$ inside the canopies gives exactly the same groups as single linkage at level $\theta$ on all pairs. Without such a relation between $c$ and $e$, canopy clustering gives no guarantee; it is a heuristic.
