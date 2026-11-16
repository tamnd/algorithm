---
title: The circumcenter step keeps every visibility link, never leaves the convex hull of the robots, and gathers a group that sees each other in one round
proves: [correctness]
status: full
---

There are $r$ point robots in the plane at positions $p_1, \dots, p_r$, and a visibility radius $V > 0$. Robot $i$ sees robot $j$ when $\lVert p_i - p_j \rVert \le V$. In one round a set $A$ of active robots is chosen (all robots in the synchronous model, any subset in the semi-synchronous model). Every active robot computes its new position from the same snapshot, and the robots that are not active stay where they are. Line numbers refer to the pseudocode on the [Ando's circumcenter algorithm](/ando-circumcenter-algorithm/) page. For an active robot $i$ let $S_i$ be the set of robots it sees (line L3, $i$ included), $c_i$ the center of the smallest enclosing circle of $S_i$ (line L4), $m_{ij} = (p_i + p_j)/2$ and $B_{ij}$ the closed disk of radius $V/2$ around $m_{ij}$ (line L7). The new position is $p_i' = p_i + t_i (c_i - p_i)$ (line L9).

**Lemma 1 (the step is well defined).** For each $j \in S_i$ the set $T_{ij} = \{ s \in [0, 1] : p_i + s (c_i - p_i) \in B_{ij} \}$ is an interval $[0, \tau_{ij}]$ with $\tau_{ij} \ge 0$. The value $t_i$ after lines L5 to L8 is $\min(1, \min_j \tau_{ij})$, and $p_i + t_i (c_i - p_i) \in B_{ij}$ for every $j \in S_i$.

*Proof.* $\lVert p_i - m_{ij} \rVert = \lVert p_i - p_j \rVert / 2 \le V/2$ because $j \in S_i$, so $0 \in T_{ij}$. The disk $B_{ij}$ is convex, so the set of $s$ for which the point of the segment lies in it is an interval, and it contains $0$, so it is $[0, \tau_{ij}]$. In the implementation $\tau_{ij}$ is the larger root of the quadratic $\lVert p_i - m_{ij} + s (c_i - p_i) \rVert^2 = V^2 / 4$, clipped to $[0, 1]$. The minimum of the right ends of intervals that all start at $0$ is the right end of their intersection, which proves the last claim. $\square$

**Lemma 2 (visibility links are kept).** If $\lVert p_i - p_j \rVert \le V$ before a round, then $\lVert p_i' - p_j' \rVert \le V$ after the round, in the synchronous and in the semi-synchronous model.

*Proof.* The midpoint $m_{ij} = m_{ji}$ and the disk $B_{ij} = B_{ji}$ are the same for both robots. If robot $i$ is active, then $p_i' \in B_{ij}$ by Lemma 1, because $j \in S_i$. If it is not active, then $p_i' = p_i \in B_{ij}$, because $\lVert p_i - m_{ij} \rVert \le V/2$. The same holds for $j$. Two points of a disk of radius $V/2$ are at distance at most $V$. $\square$

**Lemma 3 (the center lies in the convex hull).** The center $c$ of the smallest enclosing circle of a finite set $S$ lies in the convex hull $\operatorname{conv}(S)$.

*Proof.* Let $R$ be the radius of the circle. Suppose $c \notin \operatorname{conv}(S)$ and let $h$ be the point of $\operatorname{conv}(S)$ nearest to $c$, so $h \ne c$. For every $q \in \operatorname{conv}(S)$ the angle at $h$ between $c - h$ and $q - h$ is at least a right angle, that is $(c - h) \cdot (q - h) \le 0$. Then $\lVert q - c \rVert^2 = \lVert q - h \rVert^2 + \lVert h - c \rVert^2 - 2 (q - h) \cdot (c - h) \ge \lVert q - h \rVert^2 + \lVert h - c \rVert^2 > \lVert q - h \rVert^2$. So every point of $S$ is strictly nearer to $h$ than to $c$, and the circle around $h$ through the farthest point of $S$ has a radius smaller than $R$ and contains $S$. This contradicts the choice of $c$. $\square$

**Lemma 4 (the robots never leave the convex hull).** Let $H = \operatorname{conv}\{p_1, \dots, p_r\}$. After a round every $p_i'$ lies in $H$. So the diameter of the configuration and the radius of its smallest enclosing circle never increase.

*Proof.* By Lemma 3, $c_i \in \operatorname{conv}(S_i) \subseteq H$. The new position $p_i' = (1 - t_i) p_i + t_i c_i$ with $t_i \in [0, 1]$ is a convex combination of two points of $H$, so it is in $H$. Robots that are not active stay in $H$. The diameter of a finite set equals the diameter of its convex hull, so the new diameter is at most the old one. The old smallest enclosing disk is convex and contains the old points, so it contains $H$ and every new point, and the new smallest enclosing circle has at most its radius. $\square$

**Lemma 5 (the target is a fixed point for gathered robots).** If all robots of $S_i$ are at one point, then $c_i = p_i$ and robot $i$ does not move. So once all robots meet, they stay together.

*Proof.* The smallest enclosing circle of one point is that point with radius $0$, so $c_i = p_i$ and $p_i' = p_i$ for every $t_i$. $\square$

**Theorem 1 (one round when the group is small).** Let $R$ be the radius of the smallest enclosing circle of all $r$ robots, with center $c$, and let $2R \le V$. Then after one synchronous round all robots are at $c$.

*Proof.* Every two robots are at distance at most $2R \le V$, so every robot sees all robots, $S_i$ is the whole set and $c_i = c$ for every $i$. Robot $i$ reaches $c$ when $t_i = 1$, that is, when $c \in B_{ij}$ for every $j$. By the parallelogram law, $\lVert c - m_{ij} \rVert^2 = \frac12 \lVert c - p_i \rVert^2 + \frac12 \lVert c - p_j \rVert^2 - \frac14 \lVert p_i - p_j \rVert^2 \le R^2 \le V^2 / 4$. So no constraint of line L8 cuts the step, and every robot moves to $c$. $\blacksquare$

**What is not proved here.** Lemmas 2 and 4 show that the visibility graph of the initial links stays connected and that the configuration does not spread. They do not show that the diameter goes to zero. That the robots of a connected start converge to one point, in the semi-synchronous model where each robot is active infinitely often, is the theorem of Ando, Oasa, Suzuki and Yamashita (1999), and Cortés, Martínez and Bullo (2006) give a proof through an invariance principle for set-valued maps that also covers higher dimensions. The bound of $\Theta(r)$ synchronous rounds on the line is from Martínez, Bullo, Cortés and Frazzoli (2007). These results, and the exact meeting in finite time that the synchronous runs of the implementation show, are not proved here.
