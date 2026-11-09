---
title: GJK-DISTANCE terminates and returns the squared distance between the two hulls
proves: [correctness, termination]
status: full
---

**Notation.** $P, Q \subset \mathbb{R}^2$ are finite and nonempty, $M = \operatorname{conv} P - \operatorname{conv} Q$, and $D = \{p - q : p \in P, q \in Q\}$, a finite set. $\delta = \min_{m \in M} |m|$. For a finite set $W$, $\nu(W)$ is the point of $\operatorname{conv} W$ nearest to the origin; it exists and is unique because $\operatorname{conv} W$ is compact and convex and $|x|^2$ is strictly convex.

**Lemma 1.** $M = \operatorname{conv} D$, and $\delta = |m|$ for the unique nearest point $m$ of $M$.

*Proof.* A point $\sum_i \lambda_i p_i - \sum_j \mu_j q_j$ of $M$, with convex weights, equals $\sum_{i, j} \lambda_i \mu_j (p_i - q_j)$, a convex combination of $D$; conversely $D \subset M$ and $M$ is convex. $M$ is compact and convex, so the nearest point exists and is unique. $\square$

**Lemma 2.** $S_M(d) = S_P(d) - S_Q(-d)$ is a point of $D$ that maximizes $d \cdot m$ over $m \in M$.

*Proof.* $d \cdot (p - q) = d \cdot p + (-d) \cdot q$ is maximal over $p \in \operatorname{conv} P$ and $q \in \operatorname{conv} Q$ when both terms are maximal, and a linear function on a hull attains its maximum at a point of the finite set. $\square$

**Invariant.** At line L3, $W \subseteq D$, $1 \le |W| \le 3$ and $v = \nu(W)$.

*Proof.* After line L1, $W = \{p_1 - q_1\} \subseteq D$ and $v$ is its only point. Line L4 gives $w \in D$ by Lemma 2, so line L6 keeps $W \subseteq D$. Line L7 sets $v = \nu(W)$. Line L8 replaces $W$ by a subset $W'$ with $v \in \operatorname{conv} W'$; since $\operatorname{conv} W' \subseteq \operatorname{conv} W$ and $v$ is nearest in the larger set, $v = \nu(W')$. The subset is the vertex, edge or triangle of the closest feature, so $|W'| \le 3$. $\square$

**Lemma 3 (stop rule).** Let $v \in M$ and $w = S_M(-v)$. If $v \cdot v - v \cdot w \le 0$, then $|v| = \delta$.

*Proof.* By Lemma 2, $w$ minimizes $v \cdot m$ over $M$, so for every $m \in M$, $v \cdot m \ge v \cdot w \ge |v|^2$. If $v = 0$ the claim is trivial. Otherwise $|v| |m| \ge v \cdot m \ge |v|^2$ by the Cauchy-Schwarz inequality, so $|m| \ge |v|$ for all $m \in M$, and $v \in M$ gives $|v| = \delta$. $\square$

**Lemma 4 (progress).** If $v = \nu(W)$ and $v \cdot w < |v|^2$, then $|\nu(W \cup \{w\})| < |v|$.

*Proof.* The points $x(t) = v + t (w - v)$ for $t \in [0, 1]$ lie in $\operatorname{conv}(W \cup \{w\})$. $|x(t)|^2 = |v|^2 + 2 t\, v \cdot (w - v) + t^2 |w - v|^2$, and $v \cdot (w - v) = v \cdot w - |v|^2 < 0$, so $|x(t)|^2 < |v|^2$ for small $t > 0$. The nearest point of the larger hull is at least as near as $x(t)$. $\square$

**Theorem.** GJK-DISTANCE terminates and returns $\delta^2$, and at the return $v$ is the nearest point of $M$.

*Proof.* *Correctness.* If the algorithm returns at line L3, then $v = 0 \in M$ by the invariant and Lemma 1, so $\delta = 0$. If it returns at line L5, then $v \in M$ and $|v| = \delta$ by Lemma 3, and it returns $v \cdot v = \delta^2$.

*Termination.* Let $v_1, v_2, \dots$ and $W_1, W_2, \dots$ be the values at line L3 in successive passes. A pass that does not return has $v_i \cdot w < |v_i|^2$, so by Lemma 4 and the invariant $|v_{i+1}| = |\nu(W_i \cup \{w\})| < |v_i|$ (line L8 does not change $v$). So the norms $|v_i|$ strictly decrease. Since $v_i = \nu(W_i)$, equal sets would give equal norms, so the sets $W_i$ are pairwise distinct. They are subsets of $D$ with at most $3$ elements, and there are finitely many of those, so the loop stops after at most $\binom{|D|}{3} + \binom{|D|}{2} + |D|$ passes. $\blacksquare$
