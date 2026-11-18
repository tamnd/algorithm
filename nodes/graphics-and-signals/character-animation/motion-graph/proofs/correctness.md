---
title: The motion graph alignment is optimal, the transitions pass the filter, and pruning leaves a strongly connected graph
proves: [correctness]
status: full
---

We use the notation of the page.
The arithmetic is exact.
A window is a list of points $p_1, \dots, p_n$ with weights $w_i \ge 0$ that sum to 1.
$R_\theta$ turns a point about the vertical axis $y$: it maps $(x, y, z)$ to $(x\cos\theta + z\sin\theta,\ y,\ -x\sin\theta + z\cos\theta)$.
The transform $T_{\theta, x_0, z_0}$ applies $R_\theta$ and then adds $(x_0, 0, z_0)$.

## The alignment

**Lemma 1.** For a fixed $\theta$, the translation that minimizes $E(\theta, x_0, z_0) = \sum_i w_i |p_i - T_{\theta, x_0, z_0}(q_i)|^2$ is $(x_0, z_0) = (\bar x - (\bar x' \cos\theta + \bar z' \sin\theta),\ \bar z - (-\bar x' \sin\theta + \bar z' \cos\theta))$, where $\bar x, \bar z$ are the weighted means of the $p_i$ and $\bar x', \bar z'$ those of the $q_i$.

*Proof.*
The $y$ part of $E$ does not depend on $\theta$, $x_0$ or $z_0$.
The $x$ part is $\sum_i w_i (x_i - a_i - x_0)^2$ with $a_i$ the $x$ coordinate of $R_\theta q_i$.
It is a convex quadratic in $x_0$, and its derivative is zero at $x_0 = \sum_i w_i (x_i - a_i) = \bar x - (\bar x'\cos\theta + \bar z'\sin\theta)$, because the weights sum to 1 and $R_\theta$ is linear.
The $z$ part is the same. $\square$

**Lemma 2.** With the translation of Lemma 1, $E$ is smallest at $\theta = \operatorname{atan2}(S, C)$, where
$S = \sum_i w_i (x_i z_i' - x_i' z_i) - (\bar x \bar z' - \bar x' \bar z)$ and $C = \sum_i w_i (x_i x_i' + z_i z_i') - (\bar x \bar x' + \bar z \bar z')$.
If $S = C = 0$, every $\theta$ gives the same $E$.

*Proof.*
Put the optimal translation into $E$.
In the ground plane the residual of point $i$ is $u_i - R_\theta v_i$, with $u_i = (x_i - \bar x, z_i - \bar z)$ and $v_i = (x_i' - \bar x', z_i' - \bar z')$.
So $E = \text{const} + \sum_i w_i |u_i|^2 + \sum_i w_i |v_i|^2 - 2 \sum_i w_i\, u_i \cdot R_\theta v_i$, because $R_\theta$ keeps lengths.
A direct expansion gives $u \cdot R_\theta v = \cos\theta\,(u_x v_x + u_z v_z) + \sin\theta\,(u_x v_z - u_z v_x)$.
The weighted sums of these two brackets are $C$ and $S$, because $\sum_i w_i (x_i - \bar x)(x_i' - \bar x') = \sum_i w_i x_i x_i' - \bar x \bar x'$ and the same for the other products.
So $E = \text{const} - 2 (C\cos\theta + S\sin\theta)$, and $C\cos\theta + S\sin\theta = \sqrt{C^2 + S^2}\cos(\theta - \operatorname{atan2}(S, C))$ is largest at $\theta = \operatorname{atan2}(S, C)$. $\square$

**Theorem 1.** Line L3 returns a global minimizer of $E$ over all rotations about $y$ and all ground translations, and the frame distance $D(a, b)$ of line L2 is the minimum of $E$ for the windows that start at $a$ and $b$.

*Proof.*
For every $(\theta, x_0, z_0)$, Lemma 1 gives $E(\theta, x_0, z_0) \ge E(\theta, x_0^*(\theta), z_0^*(\theta))$, and Lemma 2 gives that this is at least its value at $\theta = \operatorname{atan2}(S, C)$.
The code computes exactly these $\theta$, $x_0$ and $z_0$. $\blacksquare$

## The transitions

**Theorem 2.** A pair $(a, b)$ is a transition if and only if $|a - b| \ge g$ (the minimum gap), $D(a, b) < \epsilon$ (the threshold), and no neighbor $(a + \delta_a, b + \delta_b)$ with $\delta_a, \delta_b \in \{-1, 0, 1\}$, not both zero, that is a pair of window starts has a smaller distance.

*Proof.*
The loop visits every pair of window starts once.
It skips the pair if $|a - b| < g$ or, at line L4, if $D(a, b) \ge \epsilon$.
It then rejects the pair exactly when a valid neighbor has a strictly smaller distance, and line L5 keeps the others. $\blacksquare$

So ties between neighbors keep both pairs, and the threshold test is strict.

## Pruning

Let $G$ be the graph of lines L6 and L7 and let $C$ be the vertex set that line L8 keeps: a largest strongly connected component of $G$, found by Tarjan's algorithm (we use its correctness from the tarjan-scc page).
Let $G[C]$ be the subgraph with the vertices $C$ and the edges of $G$ between them.

**Lemma 3.** If $u, v \in C$, every path from $u$ to $v$ in $G$ lies in $C$.

*Proof.*
Let $w$ be a vertex on such a path.
Then $u$ reaches $w$ along the path, and $w$ reaches $v$ along the path, and $v$ reaches $u$ because $u$ and $v$ are in one strongly connected component.
So $w$ and $u$ reach each other, and $w \in C$. $\square$

**Theorem 3.** In $G[C]$, every vertex reaches every other vertex.
If $|C| \ge 2$, every vertex of $G[C]$ has an edge out, so a walk in $G[C]$ can go on forever and never reaches a dead end.

*Proof.*
For $u, v \in C$ there is a path from $u$ to $v$ in $G$, and by Lemma 3 all its vertices and so all its edges are in $G[C]$.
If $|C| \ge 2$, take $u \in C$ and some $v \ne u$ in $C$; the first edge of a path from $u$ to $v$ in $G[C]$ leaves $u$. $\blacksquare$

**Theorem 4.** No strongly connected subgraph of $G$ has more vertices than $G[C]$.

*Proof.*
The vertex set of a strongly connected subgraph is inside one strongly connected component, and $C$ is a largest component. $\blacksquare$

## The blend weight

**Lemma 4.** The weight $\alpha(p) = 2\left(\frac{p + 1}{k}\right)^3 - 3\left(\frac{p + 1}{k}\right)^2 + 1$ is 1 at $p = -1$, 0 at $p = k - 1$, decreases on $[-1, k - 1]$, and has zero slope at both ends.

*Proof.*
With $s = (p + 1)/k \in [0, 1]$, $\alpha = 2s^3 - 3s^2 + 1$ is 1 at $s = 0$ and 0 at $s = 1$, and $d\alpha/ds = 6s(s - 1) \le 0$ with zeros at $s = 0$ and $s = 1$. $\square$
