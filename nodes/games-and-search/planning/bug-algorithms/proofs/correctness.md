---
title: Bug1 and Bug2 are complete, with bounds on the path length
proves: [correctness]
status: full
---

We use the model of the page. The obstacles are closed and pairwise disjoint, each boundary is a finite union of closed curves of finite length (loops), and only finitely many loops meet any bounded region. Write $\delta(x) = \lVert x - q_G \rVert$. A loop $C$ is a Jordan curve. The robot follows $C$ with the obstacle on one side, the *obstacle side*, and the other side is the *free side*. We assume, as Lumelsky and Stepanov do, that the m-line meets each loop in finitely many points.

**Lemma 1 (separation).** Let the robot follow the loop $C$, and let $L$ be a point of $C$ with $\delta(L) = \min_{y \in C} \delta(y)$. If the robot cannot move from $L$ toward $q_G$, then $q_G$ is not reachable from the robot.

*Proof.* Every point of the open segment from $L$ to $q_G$ is strictly closer to $q_G$ than $L$, so the segment meets $C$ only at $L$. The robot cannot move toward $q_G$, so the points of the segment near $L$ are on the obstacle side of $C$. The segment does not meet $C$ again, so $q_G$ is on the obstacle side too. The robot is on the free side, and the obstacle is closed, so every path from the robot to $q_G$ must cross $C$, a part of the obstacle. So no free path exists. $\square$

**Lemma 2 (Bug2 leave points).** Let Bug2 hit the loop $C$ at $H$. If $q_G$ is reachable, then the walk around $C$ from $H$ meets a point $Q$ that satisfies line L15 before it comes back to $H$.

*Proof.* The robot reached $H$ by moving toward $q_G$ along the m-line, so the points of the segment from $H$ to $q_G$ just after $H$ are on the obstacle side of $C$. As in Lemma 1, if $q_G$ were on the obstacle side, it would not be reachable. So $q_G$ is on the free side, and the segment from $H$ to $q_G$ meets $C$ again after $H$. It meets $C$ in finitely many points. Let $Q$ be the one closest to $q_G$. Then $Q \ne H$, so $\delta(Q) < \delta(H)$, and $Q$ is on the m-line because the segment from $H$ to $q_G$ is a part of it. The points of the segment just after $Q$ are not on $C$, and they are on the side of $C$ that holds $q_G$, the free side. They are not in another obstacle either, because the other obstacles are closed and disjoint from $C$, so they keep a positive distance from $Q$. So the robot can move from $Q$ toward $q_G$. A full walk around $C$ passes every point of $C$, so it passes $Q$ before it comes back to $H$. $\square$

**Theorem 1 (Bug1).** Bug1 stops. It returns success only at $q_G$, and it returns failure only if $q_G$ is not reachable. Its path does not enter the interior of an obstacle, and its length is at most $D + 1.5 P$.

*Proof.* The robot moves only on straight segments that stop at the first contact (line L3) and on boundaries (lines L6 and L7), so it never enters an obstacle.

Let $H_1, L_1, H_2, L_2, \dots$ be the hit and leave points, on the loops $C_1, C_2, \dots$. By line L6, $L_k$ is the point of $C_k$ closest to $q_G$, so $\delta(L_k) \le \delta(H_k)$. If line L8 returns failure at $L_k$, Lemma 1 shows that $q_G$ is not reachable. Otherwise the robot moves from $L_k$ straight toward $q_G$ by a positive length before it hits $H_{k+1}$, so $\delta(H_{k+1}) < \delta(L_k)$. Then $C_{k+1} \ne C_j$ for every $j \le k$: a point of $C_j$ at distance less than $\delta(L_k) \le \delta(L_j)$ from $q_G$ would contradict the choice of $L_j$. So each loop is hit at most once. All hit points lie within distance $D$ of $q_G$, and only finitely many loops meet that disk, so there are finitely many hits and the robot stops. When it stops by line L4, it is at $q_G$.

For the length, the straight part from $L_{k-1}$ to $H_k$ (with $L_0 = q_{start}$) moves toward $q_G$, so its length is $\delta(L_{k-1}) - \delta(H_k)$. The boundary part from $H_k$ to $L_k$ does not increase $\delta$ at its ends, since $\delta(L_k) \le \delta(H_k)$. So the straight parts add up to at most $\delta(q_{start}) - 0 = D$. On the loop $C_k$ the robot walks the full loop, of length $|C_k|$, and then at most $|C_k| / 2$ the shorter way to $L_k$. Each loop is used once, and each loop that is hit meets the disk of radius $D$ around $q_G$, so the boundary parts add up to at most $1.5 P$. $\blacksquare$

**Theorem 2 (Bug2).** Bug2 stops. It returns success only at $q_G$, and it returns failure only if $q_G$ is not reachable. Its path does not enter the interior of an obstacle, and its length is at most $D + \sum_i n_i p_i / 2$, where $n_i$ is the number of points where the m-line meets the boundary of obstacle $i$.

*Proof.* The robot is free for the same reason as in Theorem 1. If line L16 returns failure on the loop $C$, then the walk came back to $H$ without a point that satisfies line L15, and Lemma 2 shows that $q_G$ is not reachable.

Let $H_1, Q_1, H_2, Q_2, \dots$ be the hit and leave points. All of them are on the m-line, which is the segment from $q_{start}$ to $q_G$. Line L15 gives $\delta(Q_k) < \delta(H_k)$, and the move of line L12 from $Q_k$ has positive length, so $\delta(H_{k+1}) < \delta(Q_k)$. So the sequence $\delta(H_1) > \delta(Q_1) > \delta(H_2) > \cdots$ is strictly decreasing, and all these points are distinct points where the m-line meets a boundary. There are finitely many such points, so the robot stops, and when it stops by line L13 it is at $q_G$.

For the length, the straight parts are disjoint pieces of the m-line, so they add up to at most $D$. On obstacle $i$, each visit uses two distinct points of the m-line on its boundary, a hit point and a leave point, and no point is used twice. So obstacle $i$ is visited at most $n_i / 2$ times. In each visit the robot walks less than the full loop, so at most $p_i$. The boundary parts add up to at most $\sum_i n_i p_i / 2$. $\blacksquare$

**Remark.** The bound of Theorem 2 can be larger than that of Theorem 1, when the m-line crosses one obstacle many times. The proofs need exact knowledge of the position, a fixed m-line, and the general position assumption that the m-line meets each loop in finitely many points.
